"""Goodwe inverter poller — no Home Assistant dependency."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable, Awaitable, cast, Optional

from goodwe import connect, Inverter

from .config import InverterConfig
from .const import build_sensor_meta

_LOGGER = logging.getLogger(__name__)

# Work mode integer → human-readable label (mirrors sensor.py)
WORK_MODES: dict[int, str] = {
    0: "Wait",
    1: "Normal",
    2: "Fault",
    3: "Permanent Fault",
    4: "Check",
    5: "PV Charge",
    6: "Battery Discharge",
    7: "Battery Charge",
    8: "Combined",
    9: "Backup",
    10: "Off-grid",
}

# Battery mode integer → human-readable label
BATTERY_MODES: dict[int, str] = {
    0: "No battery or battery disconnected",
    1: "Standby",
    2: "Discharge",
    3: "Charge",
}

DataCallback = Callable[[dict[str, Any]], Awaitable[None]]


def _coerce_value(key: str, value: Any) -> Any:
    """Apply the same value transformations used in sensor.py."""
    if key == "work_mode" and isinstance(value, int):
        return WORK_MODES.get(value, f"Unknown ({value})")
    if key == "battery_mode" and isinstance(value, int):
        return BATTERY_MODES.get(value, f"Unknown ({value})")
    if key == "error_codes" and isinstance(value, int):
        return "No Error" if value == 0 else f"Error Code: {value}"
    return value


class InverterPoller:
    """Connects to a Goodwe inverter and polls it on a fixed interval.

    On every successful poll the *on_data* callback is awaited with a plain
    ``dict[str, Any]`` of sensor readings.  Metadata about the inverter
    (serial, model, firmware) is exposed via :attr:`inverter_info` once
    connected.
    """

    def __init__(self, cfg: InverterConfig, on_data: DataCallback) -> None:
        self._cfg = cfg
        self._on_data = on_data
        self._inverter: Optional[Inverter] = None
        self.inverter_info: dict[str, str] = {}
        # sensor id -> HA discovery metadata, built from the inverter's own definitions
        self.sensor_meta: dict[str, dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def run(self) -> None:
        """Connect then poll forever.  Reconnects automatically on errors."""
        await self._connect_with_retry()
        while True:
            await self._poll_once()
            await asyncio.sleep(self._cfg.scan_interval)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _connect_with_retry(self, max_attempts: int = 0) -> None:
        """Keep trying to connect.  *max_attempts=0* means infinite."""
        attempt = 0
        delay = 5
        while True:
            attempt += 1
            try:
                await self._connect()
                return
            except Exception as exc:
                _LOGGER.error(
                    "Connection attempt %d failed: %s — retrying in %ds",
                    attempt,
                    exc,
                    delay,
                )
                if max_attempts and attempt >= max_attempts:
                    raise
                await asyncio.sleep(delay)
                delay = min(delay * 2, 60)

    async def _connect(self) -> None:
        cfg = self._cfg
        family_arg: str | None = None if cfg.family == "auto" else cfg.family

        _LOGGER.info(
            "Connecting to inverter at %s:%d (protocol=%s, family=%s, comm_addr=0x%02X)",
            cfg.host,
            cfg.port,
            cfg.protocol,
            cfg.family,
            cfg.comm_addr,
        )

        inverter = await connect(
            cfg.host,
            cfg.port,
            family=cast(str, family_arg),
            comm_addr=cfg.comm_addr,
        )

        # Verify connection
        await inverter.read_runtime_data()

        self._inverter = inverter
        self.sensor_meta = {
            s.id_: build_sensor_meta(s.id_, s.name, s.unit, s.kind)
            for s in inverter.sensors()
        }
        self.inverter_info = {
            "serial_number": getattr(inverter, "serial_number", "unknown"),
            "model_name": getattr(inverter, "model_name", "unknown"),
            "firmware": getattr(inverter, "firmware", "unknown"),
        }

        _LOGGER.info(
            "Connected to Goodwe %s  (serial=%s  firmware=%s)",
            self.inverter_info["model_name"],
            self.inverter_info["serial_number"],
            self.inverter_info["firmware"],
        )

    async def _poll_once(self) -> None:
        if self._inverter is None:
            return
        try:
            runtime = await self._inverter.read_runtime_data()
            data: dict[str, Any] = {}
            for key in runtime.keys():
                raw = runtime.get(key)
                if raw is not None:
                    data[key] = _coerce_value(key, raw)

            _LOGGER.info("Polled %d sensor values from inverter", len(data))
            await self._on_data(data)

        except Exception as exc:
            _LOGGER.error("Poll failed: %s — will reconnect", exc)
            self._inverter = None
            await self._connect_with_retry()
