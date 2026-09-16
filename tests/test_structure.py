"""Test the basic structure of the integration."""
import os
import json


def test_manifest_exists():
    """Test that manifest.json exists."""
    manifest_path = "custom_components/goodwe_modbus/manifest.json"
    assert os.path.exists(manifest_path), "manifest.json should exist"


def test_manifest_valid():
    """Test that manifest.json is valid JSON."""
    manifest_path = "custom_components/goodwe_modbus/manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    # Check required fields
    assert "domain" in manifest
    assert manifest["domain"] == "goodwe_modbus"
    assert "name" in manifest
    assert "requirements" in manifest
    assert "goodwe>=0.3.0" in manifest["requirements"]
    assert "config_flow" in manifest
    assert manifest["config_flow"] is True


def test_init_exists():
    """Test that __init__.py exists."""
    init_path = "custom_components/goodwe_modbus/__init__.py"
    assert os.path.exists(init_path), "__init__.py should exist"


def test_config_flow_exists():
    """Test that config_flow.py exists."""
    config_flow_path = "custom_components/goodwe_modbus/config_flow.py"
    assert os.path.exists(config_flow_path), "config_flow.py should exist"


def test_sensor_exists():
    """Test that sensor.py exists."""
    sensor_path = "custom_components/goodwe_modbus/sensor.py"
    assert os.path.exists(sensor_path), "sensor.py should exist"


def test_const_exists():
    """Test that const.py exists."""
    const_path = "custom_components/goodwe_modbus/const.py"
    assert os.path.exists(const_path), "const.py should exist"


def test_coordinator_exists():
    """Test that coordinator.py exists."""
    coordinator_path = "custom_components/goodwe_modbus/coordinator.py"
    assert os.path.exists(coordinator_path), "coordinator.py should exist"


def test_translations_exist():
    """Test that translations exist."""
    translations_path = "custom_components/goodwe_modbus/translations/en.json"
    assert os.path.exists(translations_path), "translations/en.json should exist"


def test_translations_valid():
    """Test that translations are valid JSON."""
    translations_path = "custom_components/goodwe_modbus/translations/en.json"
    with open(translations_path) as f:
        translations = json.load(f)
    
    # Check required sections
    assert "config" in translations
    assert "step" in translations["config"]
    assert "user" in translations["config"]["step"]


def test_services_yaml_exists():
    """Test that services.yaml exists."""
    services_path = "custom_components/goodwe_modbus/services.yaml"
    assert os.path.exists(services_path), "services.yaml should exist"


def test_readme_exists():
    """Test that README exists."""
    readme_path = "custom_components/goodwe_modbus/README.md"
    assert os.path.exists(readme_path), "README.md should exist"


def test_hacs_json_exists():
    """Test that hacs.json exists."""
    hacs_path = "hacs.json"
    assert os.path.exists(hacs_path), "hacs.json should exist"


def test_hacs_json_valid():
    """Test that hacs.json is valid."""
    hacs_path = "hacs.json"
    with open(hacs_path) as f:
        hacs = json.load(f)

    assert "name" in hacs
    assert "render_readme" in hacs
    assert "homeassistant" in hacs

# Made with Bob
