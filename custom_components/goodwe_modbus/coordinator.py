"""DataUpdateCoordinator for Goodwe Modbus integration."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from goodwe import Inverter

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class GoodweModbusDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Goodwe inverter data."""

    def __init__(
        self,
        hass: HomeAssistant,
        inverter: Inverter,
        scan_interval: int = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        """Initialize the coordinator."""
        self.inverter = inverter
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the inverter."""
        try:
            # Read runtime data from the inverter
            runtime_data = await self.inverter.read_runtime_data()

            # Convert the runtime data to a dictionary
            data = {}
            for sensor in runtime_data.keys():
                value = runtime_data.get(sensor)
                if value is not None:
                    data[sensor] = value

            _LOGGER.debug("Successfully fetched data from inverter: %s", data)
            return data

        except Exception as err:
            _LOGGER.error("Error communicating with inverter: %s", err)
            raise UpdateFailed(f"Error communicating with inverter: {err}") from err

# Made with Bob
