"""Shared constants and helpers for building sensor metadata dynamically.

Sensor metadata (id, name, unit, kind) is taken from the goodwe library's
``Inverter.sensors()`` definitions at connect time.  This module only maps
those attributes to Home Assistant discovery fields.
"""
from __future__ import annotations
from typing import Any, Final

# Inverter protocol options
PROTOCOL_UDP: Final = "UDP"
PROTOCOL_TCP: Final = "TCP"

# Inverter family options (must match goodwe library strings exactly)
INVERTER_FAMILIES: Final = ["auto", "ET", "EH", "BT", "BH", "ES", "EM", "BP", "DT", "MS", "NS", "XS"]

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

# goodwe SensorKind name -> icon (used when the unit gives no icon)
_KIND_ICONS: Final[dict[str, str]] = {
    "PV": "mdi:solar-power",
    "AC": "mdi:transmission-tower",
    "UPS": "mdi:power-plug",
    "BAT": "mdi:battery",
    "GRID": "mdi:transmission-tower",
    "BMS": "mdi:battery",
}


def build_sensor_meta(sensor_id: str, name: str, unit: str | None, kind: Any) -> dict[str, Any]:
    """Build HA discovery metadata for one sensor from goodwe's definition."""
    kind_name = getattr(kind, "name", None)
    meta: dict[str, Any] = {
        "name": name or sensor_id,
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
