# Goodwe Modbus Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Home Assistant custom integration for Goodwe solar inverters using the Modbus protocol. Supports both UDP and TCP communication for local monitoring of your solar energy system.

## ✨ Features

- 🔌 **Dual Protocol Support**: Works with both UDP (default, port 8899) and TCP (port 502) Modbus protocols
- 📊 **Comprehensive Monitoring**: 20+ sensors tracking PV production, grid interaction, battery status, and system health
- 🎨 **Easy Configuration**: Simple UI-based setup through Home Assistant's integration page
- 🏠 **Local Network**: All communication happens locally - no cloud required, ensuring privacy and reliability
- ⚡ **Real-time Updates**: Configurable polling interval (default: 30 seconds)
- 🔧 **Device Integration**: Properly integrated as a device with all sensors grouped together
- 🔒 **Secure**: Read-only Modbus commands, local network communication only
- 📱 **Home Assistant Standards**: Follows all Home Assistant coding, documentation, and integration standards

## 📋 Requirements

- Home Assistant 2024.1.0 or newer
- Goodwe inverter with network connectivity (WiFi or Ethernet)
- Local network access to the inverter
- Python goodwe library (automatically installed)

## 🚀 Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/pranab/goodwe_modbus`
6. Select "Integration" as the category
7. Click "Install"
8. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/pranab/goodwe_modbus/releases)
2. Extract the `custom_components/goodwe_modbus` directory to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## ⚙️ Configuration

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

- Check your router's DHCP client list
- Use a network scanner app (e.g., Fing, Advanced IP Scanner)
- Check the inverter's WiFi module settings

**💡 Tip**: Set a static IP or DHCP reservation for your inverter to prevent connection issues.

### Options

After adding the integration, you can configure:
- **Update Interval**: How often to poll the inverter (default: 30 seconds, minimum: 10 seconds)

## 📊 Available Sensors

### Solar Production
- PV1/PV2 Voltage (V)
- PV1/PV2 Current (A)
- Total PV Power (W)
- Energy Today (kWh)
- Energy Total (kWh)
- Total Operating Hours (h)

### Grid Monitoring
- Grid Voltage (V)
- Grid Current (A)
- Grid Frequency (Hz)
- Grid Power (W) - positive for export, negative for import

### Battery (if equipped)
- Battery State of Charge (%)
- Battery Voltage (V)
- Battery Current (A)
- Battery Power (W) - positive for discharge, negative for charge
- Battery Mode (Standby/Charge/Discharge)

### System Status
- Inverter Temperature (°C)
- Work Mode (Wait/Normal/Fault/etc.)
- Error Codes
- Load Power (W)
- Backup Power (W)

## 🔧 Supported Inverter Models

This integration uses the [goodwe](https://github.com/marcelblijleven/goodwe) Python library and should work with most Goodwe inverter models that support Modbus communication, including:

- **ES Series** (Energy Storage)
- **EM Series** (Grid-tied)
- **ET Series** (Hybrid)
- **EH Series**
- **BT Series**
- **BH Series**

**Note**: Specific sensor availability depends on your inverter model and configuration.

## 🌐 Network Requirements

### Firewall Configuration

The integration communicates directly with your inverter on your local network:
- **UDP Mode**: Port 8899 (default)
- **TCP Mode**: Port 502 (Modbus TCP standard)

Most home networks allow this by default. Ensure your Home Assistant instance can reach the inverter on these ports.

### Security Considerations

✅ All communication is local - no data leaves your network  
✅ Uses read-only Modbus commands  
✅ No authentication required (standard for Modbus devices)  
✅ Consider network segmentation for enhanced security

## 🐛 Troubleshooting

### Cannot Connect to Inverter

1. **Verify IP Address**: Ensure the IP address is correct and the inverter is online
2. **Check Protocol**: Try switching between UDP and TCP
3. **Network Access**: Verify Home Assistant can reach the inverter (ping test)
4. **Firewall**: Check if any firewall is blocking the connection
5. **Port Conflicts**: Ensure no other service is using the same port

### Sensors Not Updating

1. **Check Logs**: Look for errors in Home Assistant logs (Settings → System → Logs)
2. **Increase Interval**: Try increasing the scan interval if you see timeout errors
3. **Inverter Status**: Ensure the inverter is operating normally
4. **Network Stability**: Check for network connectivity issues

### Missing Sensors

Some sensors may not appear if:
- Your inverter model doesn't support that feature
- The inverter hasn't collected that data yet (e.g., battery sensors without a battery)
- The sensor value is not available in the current operating mode

## 📖 Documentation

- [Integration Documentation](custom_components/goodwe_modbus/README.md)
- [Goodwe Library Documentation](https://github.com/marcelblijleven/goodwe)
- [Home Assistant Integration Standards](https://developers.home-assistant.io/docs/creating_integration_manifest)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/pranab/goodwe_modbus.git
cd goodwe_modbus

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built using the [goodwe](https://github.com/marcelblijleven/goodwe) Python library by Marcel Blijleven
- Inspired by the Home Assistant community's solar monitoring needs
- Thanks to all contributors and testers

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/pranab/goodwe_modbus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pranab/goodwe_modbus/discussions)
- **Home Assistant Community**: [Community Forum](https://community.home-assistant.io/)

## 🗺️ Roadmap

- [ ] Add support for inverter settings modification
- [ ] Implement battery charge/discharge control
- [ ] Add energy dashboard integration
- [ ] Support for multiple inverters
- [ ] Advanced diagnostics and debugging tools

---

**⭐ If you find this integration useful, please consider giving it a star on GitHub!**