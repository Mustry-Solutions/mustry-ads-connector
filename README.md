# ADS Connector

A Python-based tool for reading data from Beckhoff PLCs using the ADS (Automation Device Specification) protocol.

## Overview

This tool connects to a Beckhoff PLC via ADS and continuously reads configured tags/variables, displaying their values at regular intervals. It's designed for monitoring PLC variables in real-time.

## Features

- **JSON-based Configuration**: Easy setup through a configuration file
- **Continuous Reading**: Automatically reads PLC tags at configurable intervals
- **Multiple Data Types**: Supports auto-detection and explicit types (bool, int, real, string)
- **Error Handling**: Graceful error handling with informative messages
- **Flexible Tag Management**: Add and monitor multiple PLC variables

## Requirements

- Python 3.x
- pyads >= 3.5.0

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd ads-connector
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `config.json` file based on your PLC setup:

```json
{
  "plc": {
    "ip": "192.168.1.177",
    "port": 851
  },
  "settings": {
    "read_interval": 1.0
  },
  "tags": [
    {
      "name": "MAIN.ToggleBit",
      "data_type": "auto",
      "description": "Example toggle bit"
    }
  ]
}
```

### Configuration Parameters

- **plc.ip**: IP address of your PLC
- **plc.port**: ADS port (typically 851 for TwinCAT runtime)
- **settings.read_interval**: Time in seconds between reads
- **tags**: Array of PLC variables to monitor
  - **name**: PLC variable name (e.g., "MAIN.VariableName")
  - **data_type**: Data type ("auto", "bool", "int", "real", "string")
  - **description**: Optional description for the tag

## Usage

Run the reader with default config file (`config.json`):

```bash
python ads_reader.py
```

Or specify a custom config file:

```bash
python ads_reader.py path/to/custom_config.json
```

The program will:
1. Load the configuration
2. Connect to the PLC
3. Continuously read and display tag values
4. Press `Ctrl+C` to stop

### Example Output

```
Loading configuration from: config.json
Configuration loaded:
  PLC: 192.168.1.177:851
  Read interval: 1.0s
  Tags: 1 configured
Connected to PLC at 192.168.1.177:851
Starting continuous read with 1.0s interval...
Press Ctrl+C to stop

[2025-01-15 10:30:45] Tag Values:
--------------------------------------------------
  MAIN.ToggleBit                 = True (Example toggle bit)
```

## Project Structure

- `ads_reader.py` - Main application and ADSReader class
- `config.json` - Runtime configuration (not in repo, created by user)
- `config_example.py` - Example configuration reference
- `ads_config.yaml` - Alternative YAML configuration format
- `requirements.txt` - Python dependencies
- `deploy.sh` - Deployment script

## Troubleshooting

### Connection Issues

- Verify PLC IP address is correct
- Ensure the PLC is reachable on the network
- Check that the ADS port is correct (default: 851)
- Verify ADS routes are configured on the PLC

### Tag Reading Errors

- Confirm tag names match exactly (case-sensitive)
- Ensure tags exist in the PLC program
- Check that data types are compatible

## License

This project is provided as-is for PLC monitoring purposes.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
