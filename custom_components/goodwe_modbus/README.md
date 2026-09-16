# Goodwe Modbus Integration for Home Assistant

A Home Assistant custom integration for Goodwe solar inverters using the Modbus protocol (both UDP and TCP).

## Features

- **Dual Protocol Support**: Works with both UDP (default) and TCP Modbus protocols
- **Comprehensive Monitoring**: Tracks PV production, grid interaction, battery status, and more
- **Easy Configuration**: Simple UI-based setup through Home Assistant's integration page
- **Local Network**: All communication happens locally on your network - no cloud required
- **Real-time Updates**: Configurable polling interval (default: 30 seconds)
- **Device Integration**: Properly integrated as a device with all sensors grouped together

## Supported Sensors

The integration provides the following sensors:

### Solar Production
- PV1/PV2 Voltage and Current
- Total PV Power
- Energy Today
- Energy Total
- Total Operating Hours

### Grid Monitoring
- Grid Voltage, Current, and Frequency
- Grid Power (import/export)

### Battery (if equipped)
- Battery State of Charge (SOC)
- Battery Voltage and Current
- Battery Power (charge/discharge)
- Battery Mode

### System Status
- Inverter Temperature
- Work Mode
- Error Codes
- Load Power
- Backup Power

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/goodwe_modbus` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

### Adding the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Goodwe Modbus"
4. Enter your inverter's configuration:
   - **IP Address**: The local IP address of your Goodwe inverter
   - **Protocol**: Select UDP (default, port 8899) or TCP (port 502)
   - **Port** (optional): Custom port if different from defaults
   - **Communication Address** (optional): Modbus address (default: 247/0xF7)

### Finding Your Inverter's IP Address

You can find your inverter's IP address by:
1. Checking your router's DHCP client list
2. Using a network scanner app
3. Checking the inverter's WiFi module settings

**Tip**: Set a static IP or DHCP reservation for your inverter to prevent connection issues.

### Options

After adding the integration, you can configure:
- **Update Interval**: How often to poll the inverter (default: 30 seconds)

## Network Requirements

### Firewall Configuration

The integration communicates directly with your inverter on your local network:
- **UDP Mode**: Port 8899 (default)
- **TCP Mode**: Port 502 (Modbus TCP standard)

Ensure your Home Assistant instance can reach the inverter on these ports. Most home networks allow this by default.

### Security Considerations

- All communication is local - no data leaves your network
- The integration uses read-only Modbus commands
- No authentication is required (standard for Modbus devices)
- Consider network segmentation if you have security concerns

## Troubleshooting

### Cannot Connect to Inverter

1. **Verify IP Address**: Ensure the IP address is correct and the inverter is online
2. **Check Protocol**: Try switching between UDP and TCP
3. **Network Access**: Verify Home Assistant can reach the inverter (ping test)
4. **Firewall**: Check if any firewall is blocking the connection
5. **Port Conflicts**: Ensure no other service is using the same port

### Sensors Not Updating

1. **Check Logs**: Look for errors in Home Assistant logs
2. **Increase Interval**: Try increasing the scan interval if you see timeout errors
3. **Inverter Status**: Ensure the inverter is operating normally
4. **Network Stability**: Check for network connectivity issues

### Missing Sensors

Some sensors may not appear if:
- Your inverter model doesn't support that feature
- The inverter hasn't collected that data yet (e.g., battery sensors without a battery)
- The sensor value is not available in the current operating mode

## Supported Inverter Models

This integration uses the `goodwe` Python library and should work with most Goodwe inverter models that support Modbus communication, including:

- ES Series (Energy Storage)
- EM Series (Grid-tied)
- ET Series (Hybrid)
- EH Series
- BT Series
- BH Series
- And more

**Note**: Specific sensor availability depends on your inverter model and configuration.

## Development

### Requirements

- Python 3.11+
- Home Assistant 2024.1.0+
- goodwe Python library (>=0.3.0)

### Testing

The integration includes comprehensive tests. To run them:

```bash
pytest tests/
```

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

- **Issues**: Report bugs or request features on GitHub
- **Discussions**: Join the Home Assistant community forums
- **Documentation**: Check the goodwe library documentation for protocol details

## License

This integration is provided as-is under the MIT License.

## Credits

- Built using the [goodwe](https://github.com/marcelblijleven/goodwe) Python library
- Inspired by the Home Assistant community's solar monitoring needs

## Changelog

### Version 1.0.0
- Initial release
- UDP and TCP protocol support
- Comprehensive sensor coverage
- UI-based configuration
- Options flow for scan interval
- Full Home Assistant integration standards compliance