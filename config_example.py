#!/usr/bin/env python3
"""
Example configuration for ADS Reader
Copy this file to config.py and modify for your setup.
"""

from ads_reader import ADSReader

def create_reader():
    """Create and configure ADS reader"""

    # PLC Configuration
    PLC_IP = "192.168.1.100"  # Change to your PLC IP
    PLC_PORT = 851  # ADS port (851 is default for runtime)

    # Create reader
    reader = ADSReader(PLC_IP, PLC_PORT)

    # Add your tags here
    # Syntax: reader.add_tag("tag_name", "data_type")
    # data_type options: 'auto', 'bool', 'int', 'real', 'string'

    reader.add_tag("MAIN.bStart", "bool")
    reader.add_tag("MAIN.nCounter", "int")
    reader.add_tag("MAIN.rTemperature", "real")
    reader.add_tag("MAIN.sStatus", "string")

    # Add more tags as needed
    # reader.add_tag("GVL.bRunning", "bool")
    # reader.add_tag("GVL.nSpeed", "int")

    return reader

def main():
    """Run the configured reader"""
    reader = create_reader()

    if reader.connect():
        try:
            reader.run_continuous_read(interval=1.0)  # Read every 1 second
        finally:
            reader.disconnect()
    else:
        print("Failed to connect to PLC")

if __name__ == "__main__":
    main()