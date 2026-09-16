# Testing the Goodwe Modbus Integration

This guide explains how to manually test the integration before installing it in Home Assistant.

## Prerequisites

1. Install the goodwe library:
```bash
pip install goodwe
```

2. Know your inverter's IP address (check your router's DHCP client list)

## Manual Testing with main.py

The `main.py` script allows you to test the connection to your Goodwe inverter without Home Assistant.

### Basic Usage

**Test with UDP (default, recommended):**
```bash
python3 main.py --host 192.168.1.100 --protocol UDP
```

**Test with TCP:**
```bash
python3 main.py --host 192.168.1.100 --protocol TCP
```

### Advanced Options

**Custom port:**
```bash
python3 main.py --host 192.168.1.100 --protocol UDP --port 8899
```

**Custom communication address:**
```bash
python3 main.py --host 192.168.1.100 --protocol UDP --comm-addr 0xF7
```

### Expected Output

If successful, you should see:
```
======================================================================
Goodwe Modbus Connection Test
======================================================================

Connection Details:
  Host: 192.168.1.100
  Port: 8899
  Protocol: UDP
  Comm Address: 247 (0xF7)

----------------------------------------------------------------------

🔌 Connecting to inverter at 192.168.1.100:8899...
✓ Connected successfully!

📋 Inverter Information:
  Serial Number: TEST123456
  Model Name: GW5000-ES
  Firmware: 1.0.0
  Rated Power: 5000W

📊 Reading runtime data...

✓ Successfully retrieved 20 data points

======================================================================
Runtime Data:
======================================================================

PV Production:
----------------------------------------------------------------------
  Vpv1..........................        250.50 V
  Vpv2..........................        248.30 V
  Ipv1..........................          5.20 A
  Ipv2..........................          5.10 A
  Ppv...........................      2,600.00 W

Grid:
----------------------------------------------------------------------
  Vgrid.........................        230.00 V
  Igrid.........................         11.30 A
  Fgrid.........................         50.00 Hz
  Pgrid.........................      2,598.00 W

Battery:
----------------------------------------------------------------------
  Battery Soc...................         85.00 %
  Battery Voltage...............         52.50 V
  Battery Current...............         10.50 A
  Battery Power.................        551.00 W
  Battery Mode..................              3

Energy:
----------------------------------------------------------------------
  E Day.........................         12.50 kWh
  E Total.......................      1,234.50 kWh
  H Total.......................      5,000.00 h

System:
----------------------------------------------------------------------
  Work Mode.....................              1
  Temperature...................         45.50 °C
  Error Codes...................              0
  Load Power....................      1,500.00 W
  Backup Power..................          0.00 W

======================================================================
✅ Test completed successfully!
======================================================================
```

## Troubleshooting

### Connection Errors

**Error: "Connection refused" or "Cannot connect"**
- Verify the IP address is correct
- Check if the inverter is online: `ping 192.168.1.100`
- Ensure the inverter's WiFi/Ethernet module is working
- Try both UDP and TCP protocols

**Error: "Timeout"**
- The inverter might be in sleep mode (no solar production)
- Check network connectivity
- Verify firewall settings aren't blocking the connection
- Try increasing the timeout (if your inverter is slow to respond)

**Error: "goodwe library not installed"**
```bash
pip install goodwe
```

### Protocol Selection

- **UDP (Port 8899)**: Default and recommended for most Goodwe inverters
- **TCP (Port 502)**: Standard Modbus TCP, use if UDP doesn't work

### Finding Your Inverter's IP

1. **Router Method**: Check your router's DHCP client list
2. **Network Scanner**: Use apps like Fing, Advanced IP Scanner, or nmap
3. **Inverter Display**: Some models show the IP on the display

**Tip**: Set a static IP or DHCP reservation for your inverter to prevent the IP from changing.

## Running Structure Tests

To verify the integration structure:

```bash
python3 -m pytest tests/test_structure.py -v
```

Expected output:
```
============================= test session starts ==============================
...
tests/test_structure.py::test_manifest_exists PASSED                     [  7%]
tests/test_structure.py::test_manifest_valid PASSED                      [ 15%]
...
============================== 13 passed in 0.05s ==============================
```

## Running Validation Script

To validate all files:

```bash
python3 validate_integration.py
```

Expected output:
```
============================================================
Goodwe Modbus Integration Validation
============================================================

📁 Core Integration Files:
✓ Init file: custom_components/goodwe_modbus/__init__.py
✓ Config flow: custom_components/goodwe_modbus/config_flow.py
...

============================================================
✅ All validation checks passed!
============================================================
```

## Next Steps

Once manual testing is successful:

1. **Install in Home Assistant**:
   - Copy `custom_components/goodwe_modbus` to your HA `custom_components` directory
   - Restart Home Assistant
   - Go to Settings → Devices & Services → Add Integration
   - Search for "Goodwe Modbus"

2. **Configure**:
   - Enter your inverter's IP address
   - Select protocol (UDP or TCP)
   - Optionally set custom port and communication address
   - Click Submit

3. **Verify**:
   - Check that the device appears in Devices & Services
   - Verify all sensors are showing data
   - Check the logbook for any errors

## Support

If you encounter issues:

1. Check the Home Assistant logs: Settings → System → Logs
2. Enable debug logging in `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.goodwe_modbus: debug
   ```
3. Run the manual test script to isolate connection issues
4. Check the [GitHub Issues](https://github.com/pranab/goodwe_modbus/issues)

## Example Scenarios

### Scenario 1: First Time Setup
```bash
# Test connection
python3 main.py --host 192.168.1.100 --protocol UDP

# If successful, install in Home Assistant
# If failed, try TCP
python3 main.py --host 192.168.1.100 --protocol TCP
```

### Scenario 2: Connection Issues
```bash
# Verify inverter is reachable
ping 192.168.1.100

# Test both protocols
python3 main.py --host 192.168.1.100 --protocol UDP
python3 main.py --host 192.168.1.100 --protocol TCP

# Try different ports
python3 main.py --host 192.168.1.100 --protocol UDP --port 8899
python3 main.py --host 192.168.1.100 --protocol TCP --port 502
```

### Scenario 3: Validation Before Deployment
```bash
# Run all validations
python3 validate_integration.py

# Run structure tests
python3 -m pytest tests/test_structure.py -v

# Test actual connection
python3 main.py --host YOUR_INVERTER_IP --protocol UDP