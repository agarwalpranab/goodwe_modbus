"""The Goodwe Modbus integration."""
from __future__ import annotations

import logging

from goodwe import connect

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
    CONF_COMM_ADDR,
    CONF_PROTOCOL,
    DEFAULT_COMM_ADDR,
    DEFAULT_PORT_TCP,
    DEFAULT_PORT_UDP,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PROTOCOL_TCP,
    PROTOCOL_UDP,
)
from .coordinator import GoodweModbusDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Goodwe Modbus from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data.get(CONF_PORT)
    protocol = entry.data[CONF_PROTOCOL]
    comm_addr = entry.data.get(CONF_COMM_ADDR, DEFAULT_COMM_ADDR)
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    # Determine the correct port based on protocol
    if port is None:
        port = DEFAULT_PORT_UDP if protocol == PROTOCOL_UDP else DEFAULT_PORT_TCP

    try:
        # Connect to the inverter
        _LOGGER.debug(
            "Connecting to Goodwe inverter at %s:%s using %s protocol",
            host,
            port,
            protocol,
        )
        inverter = await connect(host, port, comm_addr)

        # Verify connection by reading runtime data
        await inverter.read_runtime_data()

        _LOGGER.info(
            "Successfully connected to Goodwe inverter %s", inverter.serial_number
        )

    except Exception as err:
        _LOGGER.error("Failed to connect to Goodwe inverter: %s", err)
        raise ConfigEntryNotReady(
            f"Failed to connect to Goodwe inverter at {host}:{port}"
        ) from err

    # Create the data update coordinator
    coordinator = GoodweModbusDataUpdateCoordinator(
        hass, inverter, scan_interval=scan_interval
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Store the coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "inverter": inverter,
    }

    # Forward the setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register update listener for options changes
    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        # Remove the entry from hass.data
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


# Made with Bob
