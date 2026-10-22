"""Configuration loaded from environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional


def _env(key: str, default: str | None = None) -> str | None:
    return os.environ.get(key, default)


def _env_required(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(f"Required environment variable '{key}' is not set.")
    return value


def _env_int(key: str, default: int) -> int:
    raw = os.environ.get(key)
    if raw is None or raw.strip() == "":   # treat empty string same as unset
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable '{key}' must be an integer, got: {raw!r}") from exc


def _env_bool(key: str, default: bool) -> bool:
    raw = os.environ.get(key, "").strip().lower()
    if not raw:
        return default
    return raw in ("1", "true", "yes")


@dataclass
class InverterConfig:
    host: str
    port: int
    protocol: str          # "UDP" or "TCP"
    family: str            # "auto", "ET", "EH", etc.
    comm_addr: int
    scan_interval: int     # seconds between polls


@dataclass
class MqttConfig:
    host: str
    port: int
    username: Optional[str]
    password: Optional[str]
    topic_prefix: str
    # Home Assistant MQTT discovery
    ha_discovery: bool
    ha_discovery_prefix: str
    client_id: str


@dataclass
class AppConfig:
    inverter: InverterConfig
    mqtt: MqttConfig
    log_level: str


def load_config() -> AppConfig:
    """Build AppConfig from environment variables."""
    protocol = (_env("INVERTER_PROTOCOL", "UDP") or "UDP").upper()
    default_port = 8899 if protocol == "UDP" else 502

    inverter = InverterConfig(
        host=_env_required("INVERTER_HOST"),
        port=_env_int("INVERTER_PORT", default_port),
        protocol=protocol,
        family=_env("INVERTER_FAMILY", "auto") or "auto",
        comm_addr=_env_int("INVERTER_COMM_ADDR", 0xF7),
        scan_interval=_env_int("SCAN_INTERVAL", 30),
    )

    mqtt = MqttConfig(
        host=_env_required("MQTT_HOST"),
        port=_env_int("MQTT_PORT", 1883),
        username=_env("MQTT_USERNAME"),
        password=_env("MQTT_PASSWORD"),
        topic_prefix=_env("MQTT_TOPIC_PREFIX", "goodwe") or "goodwe",
        ha_discovery=_env_bool("MQTT_HA_DISCOVERY", True),
        ha_discovery_prefix=_env("MQTT_HA_DISCOVERY_PREFIX", "homeassistant") or "homeassistant",
        client_id=_env("MQTT_CLIENT_ID", "goodwe-modbus") or "goodwe-modbus",
    )

    return AppConfig(
        inverter=inverter,
        mqtt=mqtt,
        log_level=(_env("LOG_LEVEL", "INFO") or "INFO").upper(),
    )
