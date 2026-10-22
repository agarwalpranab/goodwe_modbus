"""Shared constants — sensor registry lifted from the HA integration."""
from __future__ import annotations
from typing import Final

# Inverter protocol options
PROTOCOL_UDP: Final = "UDP"
PROTOCOL_TCP: Final = "TCP"

# Inverter family options (must match goodwe library strings exactly)
INVERTER_FAMILIES: Final = ["auto", "ET", "EH", "BT", "BH", "ES", "EM", "BP", "DT", "MS", "NS", "XS"]

# All sensor keys and their metadata.
# Keys must match what goodwe.Inverter.read_runtime_data() returns.
SENSOR_TYPES: dict[str, dict] = {
    "vpv1": {
        "name": "PV1 Voltage",
        "unit": "V",
        "icon": "mdi:solar-power",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "vpv2": {
        "name": "PV2 Voltage",
        "unit": "V",
        "icon": "mdi:solar-power",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "ipv1": {
        "name": "PV1 Current",
        "unit": "A",
        "icon": "mdi:current-dc",
        "device_class": "current",
        "state_class": "measurement",
    },
    "ipv2": {
        "name": "PV2 Current",
        "unit": "A",
        "icon": "mdi:current-dc",
        "device_class": "current",
        "state_class": "measurement",
    },
    "vgrid": {
        "name": "Grid Voltage",
        "unit": "V",
        "icon": "mdi:transmission-tower",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "igrid": {
        "name": "Grid Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    "fgrid": {
        "name": "Grid Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    "pgrid": {
        "name": "Grid Power",
        "unit": "W",
        "icon": "mdi:transmission-tower",
        "device_class": "power",
        "state_class": "measurement",
    },
    "work_mode": {
        "name": "Work Mode",
        "unit": None,
        "icon": "mdi:state-machine",
        "device_class": None,
        "state_class": None,
    },
    "temperature": {
        "name": "Inverter Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "error_codes": {
        "name": "Error Codes",
        "unit": None,
        "icon": "mdi:alert-circle",
        "device_class": None,
        "state_class": None,
    },
    "e_day": {
        "name": "Energy Today",
        "unit": "kWh",
        "icon": "mdi:solar-power",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "e_total": {
        "name": "Energy Total",
        "unit": "kWh",
        "icon": "mdi:solar-power",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "h_total": {
        "name": "Hours Total",
        "unit": "h",
        "icon": "mdi:clock-outline",
        "device_class": None,
        "state_class": "total_increasing",
    },
    "ppv": {
        "name": "PV Power",
        "unit": "W",
        "icon": "mdi:solar-power",
        "device_class": "power",
        "state_class": "measurement",
    },
    "battery_soc": {
        "name": "Battery State of Charge",
        "unit": "%",
        "icon": "mdi:battery",
        "device_class": "battery",
        "state_class": "measurement",
    },
    "battery_voltage": {
        "name": "Battery Voltage",
        "unit": "V",
        "icon": "mdi:battery-charging",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "battery_current": {
        "name": "Battery Current",
        "unit": "A",
        "icon": "mdi:current-dc",
        "device_class": "current",
        "state_class": "measurement",
    },
    "battery_power": {
        "name": "Battery Power",
        "unit": "W",
        "icon": "mdi:battery-charging",
        "device_class": "power",
        "state_class": "measurement",
    },
    "battery_mode": {
        "name": "Battery Mode",
        "unit": None,
        "icon": "mdi:battery-sync",
        "device_class": None,
        "state_class": None,
    },
    "load_power": {
        "name": "Load Power",
        "unit": "W",
        "icon": "mdi:home-lightning-bolt",
        "device_class": "power",
        "state_class": "measurement",
    },
    "backup_power": {
        "name": "Backup Power",
        "unit": "W",
        "icon": "mdi:power-plug",
        "device_class": "power",
        "state_class": "measurement",
    },
}
