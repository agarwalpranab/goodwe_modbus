#!/usr/bin/env python3
"""Validation script for Goodwe Modbus integration."""
import json
import os
import sys
import yaml

def check_file_exists(path, description):
    """Check if a file exists."""
    if os.path.exists(path):
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description} missing: {path}")
        return False

def check_json_valid(path, description):
    """Check if JSON file is valid."""
    try:
        with open(path) as f:
            json.load(f)
        print(f"✓ {description} valid: {path}")
        return True
    except Exception as e:
        print(f"✗ {description} invalid: {path} - {e}")
        return False

def check_yaml_valid(path, description):
    """Check if YAML file is valid."""
    try:
        with open(path) as f:
            yaml.safe_load(f)
        print(f"✓ {description} valid: {path}")
        return True
    except Exception as e:
        print(f"✗ {description} invalid: {path} - {e}")
        return False

def check_python_syntax(path, description):
    """Check if Python file has valid syntax."""
    try:
        with open(path) as f:
            compile(f.read(), path, 'exec')
        print(f"✓ {description} syntax valid: {path}")
        return True
    except SyntaxError as e:
        print(f"✗ {description} syntax error: {path} - {e}")
        return False

def main():
    """Run all validation checks."""
    print("=" * 60)
    print("Goodwe Modbus Integration Validation")
    print("=" * 60)
    
    all_passed = True
    
    # Check core files
    print("\n📁 Core Integration Files:")
    all_passed &= check_file_exists("custom_components/goodwe_modbus/__init__.py", "Init file")
    all_passed &= check_file_exists("custom_components/goodwe_modbus/config_flow.py", "Config flow")
    all_passed &= check_file_exists("custom_components/goodwe_modbus/const.py", "Constants")
    all_passed &= check_file_exists("custom_components/goodwe_modbus/coordinator.py", "Coordinator")
    all_passed &= check_file_exists("custom_components/goodwe_modbus/sensor.py", "Sensor platform")
    all_passed &= check_file_exists("custom_components/goodwe_modbus/manifest.json", "Manifest")
    
    # Check Python syntax
    print("\n🐍 Python Syntax Validation:")
    all_passed &= check_python_syntax("custom_components/goodwe_modbus/__init__.py", "Init")
    all_passed &= check_python_syntax("custom_components/goodwe_modbus/config_flow.py", "Config flow")
    all_passed &= check_python_syntax("custom_components/goodwe_modbus/const.py", "Constants")
    all_passed &= check_python_syntax("custom_components/goodwe_modbus/coordinator.py", "Coordinator")
    all_passed &= check_python_syntax("custom_components/goodwe_modbus/sensor.py", "Sensor")
    
    # Check JSON files
    print("\n📄 JSON Validation:")
    all_passed &= check_json_valid("custom_components/goodwe_modbus/manifest.json", "Manifest")
    all_passed &= check_json_valid("custom_components/goodwe_modbus/translations/en.json", "Translations")
    all_passed &= check_json_valid("hacs.json", "HACS config")
    
    # Check YAML files
    print("\n📝 YAML Validation:")
    all_passed &= check_yaml_valid("custom_components/goodwe_modbus/services.yaml", "Services")
    
    # Check documentation
    print("\n📚 Documentation:")
    all_passed &= check_file_exists("README.md", "Main README")
    all_passed &= check_file_exists("custom_components/goodwe_modbus/README.md", "Integration README")
    all_passed &= check_file_exists("LICENSE", "License")
    
    # Check test files
    print("\n🧪 Test Files:")
    all_passed &= check_file_exists("tests/__init__.py", "Tests init")
    all_passed &= check_file_exists("tests/conftest.py", "Test fixtures")
    all_passed &= check_file_exists("tests/test_structure.py", "Structure tests")
    all_passed &= check_file_exists("tests/test_config_flow.py", "Config flow tests")
    all_passed &= check_file_exists("tests/test_init.py", "Init tests")
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All validation checks passed!")
        print("=" * 60)
        return 0
    else:
        print("❌ Some validation checks failed!")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
