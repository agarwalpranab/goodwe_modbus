"""Constants for the Goodwe Modbus integration."""
from typing import Final

DOMAIN: Final = "goodwe_modbus"

# Configuration
CONF_PROTOCOL: Final = "protocol"
CONF_COMM_ADDR: Final = "comm_addr"

# Protocol types
PROTOCOL_UDP: Final = "UDP"
PROTOCOL_TCP: Final = "TCP"

# Default values
DEFAULT_NAME: Final = "Goodwe Inverter"
DEFAULT_PORT_UDP: Final = 8899
DEFAULT_PORT_TCP: Final = 502
DEFAULT_COMM_ADDR: Final = 0xF7
DEFAULT_SCAN_INTERVAL: Final = 30

# Sensor types
SENSOR_TYPES = {
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

# Made with Bob
