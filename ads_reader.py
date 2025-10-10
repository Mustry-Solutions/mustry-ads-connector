#!/usr/bin/env python3
"""
Beckhoff ADS Reader
Reads tag values from a Beckhoff PLC and prints them every second.
"""

import pyads
import time
import sys
import json
import logging
from typing import Dict, Any


class ADSReader:
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize ADS connection from config file

        Args:
            config_path: Path to JSON configuration file
        """
        # Reduce ADS logging to minimize frame warnings in output
        logging.getLogger('pyads').setLevel(logging.ERROR)

        self.config = self.load_config(config_path)
        self.plc_ip = self.config['plc']['ip']
        self.plc_port = self.config['plc']['port']
        self.read_interval = self.config['settings']['read_interval']
        self.plc = None
        self.tags = self.config['tags']

    def connect(self):
        """Establish connection to PLC"""
        try:
            # Create connection with AMS Net ID format
            self.plc = pyads.Connection(f'{self.plc_ip}.1.1', self.plc_port)

            # Set connection timeout to reduce frame warnings
            self.plc.set_timeout(5000)  # 5 seconds timeout

            self.plc.open()
            print(f"Connected to PLC at {self.plc_ip}:{self.plc_port}")
            return True
        except Exception as e:
            print(f"Failed to connect to PLC: {e}")
            return False

    def disconnect(self):
        """Close connection to PLC"""
        if self.plc:
            self.plc.close()
            print("Disconnected from PLC")

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from JSON file

        Args:
            config_path: Path to configuration file

        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file '{config_path}' not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in config file: {e}")
            sys.exit(1)

    def add_tag(self, tag_name: str, data_type: str = 'auto', description: str = ""):
        """
        Add a tag to monitor

        Args:
            tag_name: Name of the PLC variable/tag
            data_type: Data type ('auto', 'bool', 'int', 'real', 'string')
            description: Optional description
        """
        self.tags.append({
            'name': tag_name,
            'data_type': data_type,
            'description': description
        })

    def read_tag_value(self, tag_name: str, data_type: str = 'auto') -> Any:
        """
        Read a single tag value

        Args:
            tag_name: Name of the tag
            data_type: Expected data type

        Returns:
            Tag value or None if error
        """
        try:
            if data_type == 'auto':
                return self.plc.read_by_name(tag_name)
            elif data_type == 'bool':
                return self.plc.read_by_name(tag_name, pyads.PLCTYPE_BOOL)
            elif data_type == 'int':
                return self.plc.read_by_name(tag_name, pyads.PLCTYPE_INT)
            elif data_type == 'real':
                return self.plc.read_by_name(tag_name, pyads.PLCTYPE_REAL)
            elif data_type == 'string':
                return self.plc.read_by_name(tag_name, pyads.PLCTYPE_STRING)
            else:
                return self.plc.read_by_name(tag_name)
        except Exception as e:
            print(f"Error reading tag '{tag_name}': {e}")
            return None

    def read_all_tags(self) -> Dict[str, Any]:
        """
        Read all configured tags

        Returns:
            Dictionary with tag names as keys and values as values
        """
        values = {}
        for tag in self.tags:
            value = self.read_tag_value(tag['name'], tag.get('data_type', 'auto'))
            values[tag['name']] = value
        return values

    def print_tag_values(self, values: Dict[str, Any]):
        """Print tag values in a formatted way"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{timestamp}] Tag Values:")
        print("-" * 50)

        if not values:
            print("No tag values to display")
            return

        for tag in self.tags:
            tag_name = tag['name']
            value = values.get(tag_name)
            description = tag.get('description', '')
            desc_text = f" ({description})" if description else ""

            if value is not None:
                print(f"  {tag_name:30} = {value}{desc_text}")
            else:
                print(f"  {tag_name:30} = ERROR{desc_text}")

    def run_continuous_read(self, interval: float = None):
        """
        Continuously read and print tag values

        Args:
            interval: Time interval between reads in seconds (uses config if None)
        """
        if not self.plc:
            print("Not connected to PLC. Call connect() first.")
            return

        if not self.tags:
            print("No tags configured in config file.")
            return

        if interval is None:
            interval = self.read_interval

        print(f"Starting continuous read with {interval}s interval...")
        print(f"PLC: {self.plc_ip}:{self.plc_port}")
        print(f"Tags: {len(self.tags)} configured")
        print("Press Ctrl+C to stop")

        try:
            while True:
                values = self.read_all_tags()
                self.print_tag_values(values)
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\nStopping continuous read...")
        except Exception as e:
            print(f"Error during continuous read: {e}")


def main():
    """Main function - uses config file for setup"""
    config_file = "config.json"

    # Check for custom config file argument
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    print(f"Loading configuration from: {config_file}")

    # Create reader instance from config
    reader = ADSReader(config_file)

    print(f"Configuration loaded:")
    print(f"  PLC: {reader.plc_ip}:{reader.plc_port}")
    print(f"  Read interval: {reader.read_interval}s")
    print(f"  Tags: {len(reader.tags)} configured")

    # Connect and start reading
    if reader.connect():
        try:
            reader.run_continuous_read()
        finally:
            reader.disconnect()
    else:
        print("Failed to connect to PLC")
        sys.exit(1)


if __name__ == "__main__":
    main()