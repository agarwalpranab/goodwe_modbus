"""Sensor platform for Goodwe Modbus integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_TYPES
from .coordinator import GoodweModbusDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Goodwe Modbus sensors from a config entry."""
    coordinator: GoodweModbusDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]
    inverter = hass.data[DOMAIN][entry.entry_id]["inverter"]

    # Create sensor entities for all available sensor types
    entities = []
    for sensor_key, sensor_config in SENSOR_TYPES.items():
        # Only create sensor if data is available
        if sensor_key in coordinator.data:
            entities.append(
                GoodweModbusSensor(
                    coordinator,
                    entry,
                    sensor_key,
                    sensor_config,
                    inverter,
                )
            )

    async_add_entities(entities)


class GoodweModbusSensor(CoordinatorEntity[GoodweModbusDataUpdateCoordinator], SensorEntity):
    """Representation of a Goodwe Modbus sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: GoodweModbusDataUpdateCoordinator,
        entry: ConfigEntry,
        sensor_key: str,
        sensor_config: dict[str, Any],
        inverter: Any,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_key = sensor_key
        self._attr_name = sensor_config["name"]
        self._attr_native_unit_of_measurement = sensor_config.get("unit")
        self._attr_icon = sensor_config.get("icon")
        raw_device_class = sensor_config.get("device_class")
        self._attr_device_class = (
            SensorDeviceClass(raw_device_class) if raw_device_class else None
        )
        raw_state_class = sensor_config.get("state_class")
        self._attr_state_class = (
            SensorStateClass(raw_state_class) if raw_state_class else None
        )
        self._attr_unique_id = f"{inverter.serial_number}_{sensor_key}"
        self._inverter = inverter

        # Device info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, inverter.serial_number)},
            name=f"Goodwe {inverter.model_name}",
            manufacturer="Goodwe",
            model=inverter.model_name,
            sw_version=inverter.firmware,
            configuration_url=f"http://{entry.data[CONF_HOST]}",
        )

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        value = self.coordinator.data.get(self._sensor_key)
        
        # Handle special cases for certain sensor types
        if self._sensor_key == "work_mode" and isinstance(value, int):
            # Convert work mode integer to string representation
            work_modes = {
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
            return work_modes.get(value, f"Unknown ({value})")
        
        if self._sensor_key == "battery_mode" and isinstance(value, int):
            # Convert battery mode integer to string representation
            battery_modes = {
                0: "No battery or battery disconnected",
                1: "Standby",
                2: "Discharge",
                3: "Charge",
            }
            return battery_modes.get(value, f"Unknown ({value})")
        
        if self._sensor_key == "error_codes" and isinstance(value, int):
            # Convert error codes to human-readable format
            if value == 0:
                return "No Error"
            return f"Error Code: {value}"
        
        return value

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            super().available
            and self.coordinator.data is not None
            and self._sensor_key in self.coordinator.data
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        attributes = {}
        
        # Add inverter information
        if hasattr(self._inverter, "serial_number"):
            attributes["serial_number"] = self._inverter.serial_number
        if hasattr(self._inverter, "model_name"):
            attributes["model"] = self._inverter.model_name
        if hasattr(self._inverter, "firmware"):
            attributes["firmware"] = self._inverter.firmware
        
        return attributes if attributes else None

# Made with Bob
