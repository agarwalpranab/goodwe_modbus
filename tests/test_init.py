"""Test the Goodwe Modbus integration initialization."""
from unittest.mock import patch

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.goodwe_modbus.const import (
    CONF_PROTOCOL,
    DOMAIN,
    PROTOCOL_UDP,
)


async def test_setup_entry(hass: HomeAssistant, mock_connect, mock_inverter) -> None:
    """Test successful setup of entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Goodwe TEST123456",
        data={
            CONF_HOST: "192.168.1.100",
            CONF_PROTOCOL: PROTOCOL_UDP,
        },
        unique_id="TEST123456",
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.goodwe_modbus.connect",
        return_value=mock_inverter,
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert DOMAIN in hass.data
    assert entry.entry_id in hass.data[DOMAIN]
    assert "coordinator" in hass.data[DOMAIN][entry.entry_id]
    assert "inverter" in hass.data[DOMAIN][entry.entry_id]


async def test_setup_entry_connection_error(hass: HomeAssistant) -> None:
    """Test setup fails when connection fails."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Goodwe TEST123456",
        data={
            CONF_HOST: "192.168.1.100",
            CONF_PROTOCOL: PROTOCOL_UDP,
        },
        unique_id="TEST123456",
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.goodwe_modbus.connect",
        side_effect=Exception("Connection failed"),
    ):
        result = await hass.config_entries.async_setup(entry.entry_id)

    assert result is False
    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_unload_entry(hass: HomeAssistant, mock_connect, mock_inverter) -> None:
    """Test successful unload of entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Goodwe TEST123456",
        data={
            CONF_HOST: "192.168.1.100",
            CONF_PROTOCOL: PROTOCOL_UDP,
        },
        unique_id="TEST123456",
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.goodwe_modbus.connect",
        return_value=mock_inverter,
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.entry_id not in hass.data[DOMAIN]

# Made with Bob
