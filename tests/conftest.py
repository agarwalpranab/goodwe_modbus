"""Fixtures for Goodwe Modbus integration tests."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant import loader


@pytest.fixture
def mock_inverter():
    """Mock Goodwe inverter."""
    inverter = MagicMock()
    inverter.serial_number = "TEST123456"
    inverter.model_name = "GW5000-ES"
    inverter.firmware = "1.0.0"
    
    # Mock runtime data
    runtime_data = {
        "vpv1": 250.5,
        "vpv2": 248.3,
        "ipv1": 5.2,
        "ipv2": 5.1,
        "ppv": 2600,
        "vgrid": 230.0,
        "igrid": 11.3,
        "fgrid": 50.0,
        "pgrid": 2598,
        "work_mode": 1,
        "temperature": 45.5,
        "error_codes": 0,
        "e_day": 12.5,
        "e_total": 1234.5,
        "h_total": 5000,
        "battery_soc": 85,
        "battery_voltage": 52.5,
        "battery_current": 10.5,
        "battery_power": 551,
        "battery_mode": 3,
        "load_power": 1500,
        "backup_power": 0,
    }
    
    inverter.read_runtime_data = AsyncMock(return_value=runtime_data)
    
    return inverter


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(hass: HomeAssistant) -> None:
    """Automatically enable custom integrations for all tests."""
    hass.data.pop(loader.DATA_CUSTOM_COMPONENTS, None)


@pytest.fixture
def mock_connect(mock_inverter):
    """Mock goodwe.connect function."""
    with patch("custom_components.goodwe_modbus.config_flow.connect") as mock:
        mock.return_value = mock_inverter
        yield mock


@pytest.fixture
def mock_setup_entry():
    """Mock setup entry."""
    with patch(
        "custom_components.goodwe_modbus.async_setup_entry",
        return_value=True,
    ) as mock:
        yield mock

# Made with Bob
