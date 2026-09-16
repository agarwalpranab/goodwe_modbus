"""Test the Goodwe Modbus config flow."""
from unittest.mock import patch

import pytest
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.goodwe_modbus.config_flow import CannotConnect
from custom_components.goodwe_modbus.const import (
    CONF_COMM_ADDR,
    CONF_FAMILY,
    CONF_PROTOCOL,
    DEFAULT_COMM_ADDR,
    DEFAULT_FAMILY,
    DOMAIN,
    PROTOCOL_UDP,
)


async def test_form_udp(hass: HomeAssistant, mock_connect, mock_setup_entry) -> None:
    """Test we get the form and can setup with UDP."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_HOST: "192.168.1.100",
            CONF_PROTOCOL: PROTOCOL_UDP,
            CONF_FAMILY: DEFAULT_FAMILY,
            CONF_COMM_ADDR: DEFAULT_COMM_ADDR,
        },
    )
    await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Goodwe TEST123456"
    assert result2["data"] == {
        CONF_HOST: "192.168.1.100",
        CONF_PROTOCOL: PROTOCOL_UDP,
        CONF_FAMILY: DEFAULT_FAMILY,
        CONF_COMM_ADDR: DEFAULT_COMM_ADDR,
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_tcp(hass: HomeAssistant, mock_connect, mock_setup_entry) -> None:
    """Test we can setup with TCP."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_HOST: "192.168.1.100",
            CONF_PROTOCOL: "TCP",
            CONF_FAMILY: "ET",
            CONF_PORT: 502,
            CONF_COMM_ADDR: DEFAULT_COMM_ADDR,
        },
    )
    await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Goodwe TEST123456"


async def test_form_cannot_connect(hass: HomeAssistant, mock_connect) -> None:
    """Test we handle cannot connect error."""
    mock_connect.side_effect = CannotConnect

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_HOST: "192.168.1.100",
            CONF_PROTOCOL: PROTOCOL_UDP,
            CONF_FAMILY: DEFAULT_FAMILY,
        },
    )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_form_unknown_error(hass: HomeAssistant) -> None:
    """Test we handle unknown error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.goodwe_modbus.config_flow.validate_input",
        side_effect=Exception("Unexpected error"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOST: "192.168.1.100",
                CONF_PROTOCOL: PROTOCOL_UDP,
                CONF_FAMILY: DEFAULT_FAMILY,
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}


async def test_form_already_configured(
    hass: HomeAssistant, mock_connect, mock_setup_entry
) -> None:
    """Test we handle already configured."""
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

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_HOST: "192.168.1.100",
            CONF_PROTOCOL: PROTOCOL_UDP,
            CONF_FAMILY: DEFAULT_FAMILY,
        },
    )

    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "already_configured"

# Made with Bob
