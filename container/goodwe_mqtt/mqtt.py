"""MQTT publisher with optional Home Assistant discovery support."""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

import aiomqtt

from .config import MqttConfig
from .const import SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


class MqttPublisher:
    """Publishes inverter readings to an MQTT broker.

    When *ha_discovery* is enabled, a single call to
    :meth:`publish_discovery` emits HA auto-discovery config payloads so the
    inverter sensors appear automatically in Home Assistant (or any other
    discovery-compatible system).

    Each subsequent call to :meth:`publish_data` updates every sensor's
    state topic atomically.
    """

    def __init__(self, cfg: MqttConfig) -> None:
        self._cfg = cfg
        self._client: aiomqtt.Client | None = None
        self._discovery_sent = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def connect(self) -> None:
        """Create the MQTT client connection."""
        cfg = self._cfg
        _LOGGER.info("Connecting to MQTT broker at %s:%d", cfg.host, cfg.port)

        kwargs: dict[str, Any] = {
            "hostname": cfg.host,
            "port": cfg.port,
            "identifier": cfg.client_id,
            "keepalive": 60,
        }
        if cfg.username:
            kwargs["username"] = cfg.username
        if cfg.password:
            kwargs["password"] = cfg.password

        self._client = aiomqtt.Client(**kwargs)
        await self._client.__aenter__()
        _LOGGER.info("Connected to MQTT broker")

    async def disconnect(self) -> None:
        if self._client is not None:
            await self._client.__aexit__(None, None, None)
            self._client = None

    # ------------------------------------------------------------------
    # Publishing
    # ------------------------------------------------------------------

    async def publish_discovery(self, inverter_info: dict[str, str]) -> None:
        """Emit HA MQTT discovery config messages for all sensor types."""
        if not self._cfg.ha_discovery:
            return
        if self._client is None:
            raise RuntimeError("MQTT client not connected")

        serial = inverter_info.get("serial_number", "unknown")
        model = inverter_info.get("model_name", "Goodwe Inverter")
        firmware = inverter_info.get("firmware", "unknown")

        device_payload = {
            "identifiers": [f"goodwe_{serial}"],
            "name": f"Goodwe {model}",
            "manufacturer": "Goodwe",
            "model": model,
            "sw_version": firmware,
        }

        prefix = self._cfg.ha_discovery_prefix
        topic_prefix = self._cfg.topic_prefix

        for sensor_key, sensor_cfg in SENSOR_TYPES.items():
            state_topic = f"{topic_prefix}/{serial}/sensor/{sensor_key}/state"
            unique_id = f"goodwe_{serial}_{sensor_key}"

            config: dict[str, Any] = {
                "name": sensor_cfg["name"],
                "unique_id": unique_id,
                "state_topic": state_topic,
                "device": device_payload,
            }
            if sensor_cfg.get("unit"):
                config["unit_of_measurement"] = sensor_cfg["unit"]
            if sensor_cfg.get("device_class"):
                config["device_class"] = sensor_cfg["device_class"]
            if sensor_cfg.get("state_class"):
                config["state_class"] = sensor_cfg["state_class"]
            if sensor_cfg.get("icon"):
                config["icon"] = sensor_cfg["icon"]

            discovery_topic = f"{prefix}/sensor/{unique_id}/config"
            await self._client.publish(
                discovery_topic,
                payload=json.dumps(config),
                retain=True,
            )
            _LOGGER.debug("Published HA discovery for %s → %s", sensor_key, discovery_topic)

        self._discovery_sent = True
        _LOGGER.info("Published HA MQTT discovery for %d sensors (serial=%s)", len(SENSOR_TYPES), serial)

    async def publish_data(
        self, data: dict[str, Any], inverter_info: dict[str, str]
    ) -> None:
        """Publish one sensor reading per key in *data*."""
        if self._client is None:
            raise RuntimeError("MQTT client not connected")

        serial = inverter_info.get("serial_number", "unknown")
        topic_prefix = self._cfg.topic_prefix

        # Publish every individual sensor on its own topic
        for key, value in data.items():
            topic = f"{topic_prefix}/{serial}/sensor/{key}/state"
            payload = str(value) if not isinstance(value, str) else value
            await self._client.publish(topic, payload=payload)

        # Also publish a single JSON snapshot on a summary topic
        summary_topic = f"{topic_prefix}/{serial}/state"
        await self._client.publish(
            summary_topic,
            payload=json.dumps(data, default=str),
        )

        _LOGGER.info("Published %d sensor readings to MQTT (topic prefix: %s/%s)", len(data), self._cfg.topic_prefix, serial)

    async def publish_with_reconnect(
        self,
        data: dict[str, Any],
        inverter_info: dict[str, str],
    ) -> None:
        """Publish data, reconnecting once on transient MQTT failures."""
        try:
            if not self._discovery_sent:
                await self.publish_discovery(inverter_info)
            await self.publish_data(data, inverter_info)
        except Exception as exc:
            _LOGGER.warning("MQTT publish failed (%s) — reconnecting", exc)
            try:
                await self.disconnect()
            except Exception:
                pass
            await self.connect()
            self._discovery_sent = False
            await self.publish_discovery(inverter_info)
            await self.publish_data(data, inverter_info)
