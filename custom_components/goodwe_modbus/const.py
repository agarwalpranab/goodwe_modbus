"""Constants for the Goodwe Modbus integration."""
from __future__ import annotations

from typing import Any, Final

DOMAIN: Final = "goodwe_modbus"

# Configuration
CONF_PROTOCOL: Final = "protocol"
CONF_COMM_ADDR: Final = "comm_addr"
CONF_FAMILY: Final = "family"

# Protocol types
PROTOCOL_UDP: Final = "UDP"
PROTOCOL_TCP: Final = "TCP"

# Inverter families (must match goodwe library strings exactly)
INVERTER_FAMILIES: Final = ["auto", "ET", "EH", "BT", "BH", "ES", "EM", "BP", "DT", "MS", "NS", "XS"]
DEFAULT_FAMILY: Final = "auto"

# Default values
DEFAULT_NAME: Final = "Goodwe Inverter"
DEFAULT_PORT_UDP: Final = 8899
DEFAULT_PORT_TCP: Final = 502
DEFAULT_COMM_ADDR: Final = 0xF7
DEFAULT_SCAN_INTERVAL: Final = 30

# Sensor metadata is built dynamically from the goodwe library's own sensor
# definitions (Inverter.sensors()).  The tables below only map the unit / kind
# reported by the library to Home Assistant sensor attributes.

# unit reported by goodwe -> (HA unit, device_class, state_class, icon)
_UNIT_MAP: Final[dict[str, tuple[str, str | None, str | None, str | None]]] = {
    "V": ("V", "voltage", "measurement", "mdi:flash"),
    "A": ("A", "current", "measurement", "mdi:current-dc"),
    "W": ("W", "power", "measurement", "mdi:flash"),
    "VA": ("VA", "apparent_power", "measurement", "mdi:flash"),
    "var": ("var", "reactive_power", "measurement", "mdi:flash"),
    "kWh": ("kWh", "energy", "total_increasing", "mdi:solar-power"),
    "Hz": ("Hz", "frequency", "measurement", "mdi:sine-wave"),
    "C": ("°C", "temperature", "measurement", "mdi:thermometer"),
    "%": ("%", None, "measurement", "mdi:percent"),
    "h": ("h", None, "total_increasing", "mdi:clock-outline"),
}

# goodwe SensorKind name -> icon (used when the unit gives no better icon)
_KIND_ICONS: Final[dict[str, str]] = {
    "PV": "mdi:solar-power",
    "AC": "mdi:transmission-tower",
    "UPS": "mdi:power-plug",
    "BAT": "mdi:battery",
    "GRID": "mdi:transmission-tower",
    "BMS": "mdi:battery",
}


def build_sensor_meta(sensor_id: str, name: str | None, unit: str | None, kind: Any) -> dict[str, Any]:
    """Build Home Assistant sensor metadata from a goodwe sensor definition."""
    kind_name = getattr(kind, "name", None)
    meta: dict[str, Any] = {
        "name": name or sensor_id.replace("_", " ").title(),
        "unit": None,
        "icon": _KIND_ICONS.get(kind_name or "", "mdi:information-outline"),
        "device_class": None,
        "state_class": None,
    }
    if unit in _UNIT_MAP:
        ha_unit, device_class, state_class, icon = _UNIT_MAP[unit]
        meta.update(unit=ha_unit, device_class=device_class, state_class=state_class)
        # Kind-based icon wins for PV/battery; otherwise use the unit icon.
        if kind_name not in ("PV", "BAT", "BMS") and icon:
            meta["icon"] = icon
    elif unit:
        meta["unit"] = unit
        meta["state_class"] = "measurement"

    if unit == "%" and "soc" in sensor_id.lower():
        meta["device_class"] = "battery"
    return meta


def build_sensor_types(inverter: Any) -> dict[str, dict[str, Any]]:
    """Return {sensor_id: metadata} for every sensor the inverter defines."""
    return {
        s.id_: build_sensor_meta(s.id_, s.name, s.unit, s.kind)
        for s in inverter.sensors()
    }

# Made with Bob
