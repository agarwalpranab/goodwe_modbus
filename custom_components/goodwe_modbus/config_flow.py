"""Config flow for Goodwe Modbus integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from goodwe import connect

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv

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

_LOGGER = logging.getLogger(__name__)


async def validate_input(data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    host = data[CONF_HOST]
    port = data.get(CONF_PORT)
    protocol = data[CONF_PROTOCOL]
    comm_addr = data.get(CONF_COMM_ADDR, DEFAULT_COMM_ADDR)

    try:
        # Attempt to connect to the inverter
        if protocol == PROTOCOL_UDP:
            inverter = await connect(host, port or DEFAULT_PORT_UDP, comm_addr)
        else:  # TCP
            inverter = await connect(host, port or DEFAULT_PORT_TCP, comm_addr)

        # Try to read runtime data to verify connection
        await inverter.read_runtime_data()

        # Get serial number for unique ID
        serial_number = inverter.serial_number

        return {
            "title": f"Goodwe {serial_number}",
            "serial_number": serial_number,
        }
    except CannotConnect:
        raise
    except Exception as err:
        _LOGGER.error("Error connecting to Goodwe inverter: %s", err)
        raise CannotConnect from err


class GoodweModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Goodwe Modbus."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Set unique ID based on serial number
                await self.async_set_unique_id(info["serial_number"])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=info["title"], data=user_input)

        # Show form with protocol selection
        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PROTOCOL, default=PROTOCOL_UDP): vol.In(
                    [PROTOCOL_UDP, PROTOCOL_TCP]
                ),
                vol.Optional(CONF_PORT): cv.port,
                vol.Optional(CONF_COMM_ADDR, default=DEFAULT_COMM_ADDR): cv.positive_int,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> GoodweModbusOptionsFlowHandler:
        """Get the options flow for this handler."""
        return GoodweModbusOptionsFlowHandler()


class GoodweModbusOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Goodwe Modbus integration."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): cv.positive_int,
                }
            ),
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

# Made with Bob
