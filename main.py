#!/usr/bin/env python3
"""Manual test script for Goodwe Modbus integration.

This script allows you to test the connection to your Goodwe inverter
and retrieve data without needing Home Assistant.

Usage:
    python3 main.py --host 192.168.1.100 --protocol UDP
    python3 main.py --host 192.168.1.100 --protocol TCP --port 502
"""
import argparse
import asyncio
import json
import sys
from typing import Any

try:
    from goodwe import connect
except ImportError:
    print("Error: goodwe library not installed")
    print("Install it with: pip install goodwe")
    sys.exit(1)


async def test_connection(
    host: str,
    port: int,
    protocol: str,
    comm_addr: int = 0xF7
) -> None:
    """Test connection to Goodwe inverter and retrieve data.
    
    Args:
        host: IP address of the inverter
        port: Port number (8899 for UDP, 502 for TCP)
        protocol: Protocol type (UDP or TCP)
        comm_addr: Communication address (default: 0xF7/247)
    """
    print("=" * 70)
    print("Goodwe Modbus Connection Test")
    print("=" * 70)
    print(f"\nConnection Details:")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  Protocol: {protocol}")
    print(f"  Comm Address: {comm_addr} (0x{comm_addr:02X})")
    print("\n" + "-" * 70)
    
    try:
        # Connect to inverter
        print(f"\n🔌 Connecting to inverter at {host}:{port}...")
        inverter = await connect(host, port, comm_addr)
        print(f"✓ Connected successfully!")
        
        # Get inverter information
        print(f"\n📋 Inverter Information:")
        print(f"  Serial Number: {inverter.serial_number}")
        print(f"  Model Name: {inverter.model_name}")
        if hasattr(inverter, 'firmware'):
            print(f"  Firmware: {inverter.firmware}")
        if hasattr(inverter, 'rated_power'):
            print(f"  Rated Power: {inverter.rated_power}W")
        
        # Read runtime data
        print(f"\n📊 Reading runtime data...")
        runtime_data = await inverter.read_runtime_data()
        
        print(f"\n✓ Successfully retrieved {len(runtime_data)} data points")
        print("\n" + "=" * 70)
        print("Runtime Data:")
        print("=" * 70)
        print(json.dumps(runtime_data, indent=2, default=str))
        
        
        # Organize data by category
        categories = {
            "PV Production": ["vpv1", "vpv2", "vpv3", "vpv4", "ipv1", "ipv2", 
            "ipv3", "ipv4", "ppv"],
            "Grid": ["vgrid", "igrid", "fgrid", "pgrid"],
            "Battery": ["battery_soc", "battery_voltage", "battery_current", 
                       "battery_power", "battery_mode"],
            "Energy": ["e_day", "e_total", "h_total"],
            "System": ["work_mode", "temperature", "error_codes", "load_power", 
                      "backup_power"],
        }
        
        # Display data by category
        for category, keys in categories.items():
            category_data = {k: v for k, v in runtime_data.items() if k in keys}
            if category_data:
                print(f"\n{category}:")
                print("-" * 70)
                for key, value in category_data.items():
                    # Format the key nicely
                    display_key = key.replace("_", " ").title()
                    
                    # Add units based on key
                    if "voltage" in key or key.startswith("v"):
                        unit = "V"
                    elif "current" in key or key.startswith("i"):
                        unit = "A"
                    elif "power" in key or key.startswith("p"):
                        unit = "W"
                    elif "frequency" in key or key.startswith("f"):
                        unit = "Hz"
                    elif "temperature" in key:
                        unit = "°C"
                    elif "soc" in key:
                        unit = "%"
                    elif "e_day" in key or "e_total" in key:
                        unit = "kWh"
                    elif "h_total" in key:
                        unit = "h"
                    else:
                        unit = ""
                    
                    # Format value
                    if isinstance(value, (int, float)):
                        formatted_value = f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"
                    else:
                        formatted_value = str(value)
                    
                    print(f"  {display_key:.<30} {formatted_value:>15} {unit}")
        
        # Display any remaining data
        displayed_keys = set()
        for keys in categories.values():
            displayed_keys.update(keys)
        
        other_data = {k: v for k, v in runtime_data.items() if k not in displayed_keys}
        if other_data:
            print(f"\nOther Data:")
            print("-" * 70)
            for key, value in other_data.items():
                display_key = key.replace("_", " ").title()
                formatted_value = str(value) if value is not None else "N/A"
                print(f"  {display_key:.<30} {formatted_value:>15}")
        
        print("\n" + "=" * 70)
        print("✅ Test completed successfully!")
        print("=" * 70)
        
    except ConnectionError as e:
        print(f"\n❌ Connection Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Check if the IP address is correct")
        print("  2. Verify the inverter is online and reachable")
        print("  3. Try pinging the inverter: ping {host}")
        print("  4. Check if the port is correct (UDP: 8899, TCP: 502)")
        print("  5. Ensure no firewall is blocking the connection")
        sys.exit(1)
        
    except TimeoutError as e:
        print(f"\n❌ Timeout Error: {e}")
        print("\nTroubleshooting:")
        print("  1. The inverter might be offline or unreachable")
        print("  2. Check network connectivity")
        print("  3. Try increasing the timeout (if supported)")
        print("  4. Verify the protocol (UDP vs TCP)")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {type(e).__name__}: {e}")
        print("\nPlease check:")
        print("  1. Goodwe library is installed: pip install goodwe")
        print("  2. All connection parameters are correct")
        print("  3. The inverter model is supported")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test Goodwe Modbus connection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test UDP connection (default port 8899)
  python3 main.py --host 192.168.1.100 --protocol UDP
  
  # Test TCP connection (default port 502)
  python3 main.py --host 192.168.1.100 --protocol TCP
  
  # Test with custom port
  python3 main.py --host 192.168.1.100 --protocol UDP --port 8899
  
  # Test with custom communication address
  python3 main.py --host 192.168.1.100 --protocol UDP --comm-addr 247
        """
    )
    
    parser.add_argument(
        "--host",
        required=True,
        help="IP address of the Goodwe inverter"
    )
    
    parser.add_argument(
        "--protocol",
        choices=["UDP", "TCP"],
        default="UDP",
        help="Protocol to use (default: UDP)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        help="Port number (default: 8899 for UDP, 502 for TCP)"
    )
    
    parser.add_argument(
        "--comm-addr",
        type=lambda x: int(x, 0),  # Allows both decimal and hex (0xF7)
        default=0xF7,
        help="Communication address (default: 0xF7/247)"
    )
    
    args = parser.parse_args()
    
    # Set default port based on protocol if not specified
    if args.port is None:
        args.port = 8899 if args.protocol == "UDP" else 502
    
    # Run the async test
    try:
        asyncio.run(test_connection(
            host=args.host,
            port=args.port,
            protocol=args.protocol,
            comm_addr=args.comm_addr
        ))
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(130)


if __name__ == "__main__":
    main()

# Made with Bob
