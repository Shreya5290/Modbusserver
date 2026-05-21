# Modbus Server UI

A user-friendly web interface for simulating a Modbus TCP server. Perfect for testing and development.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python app.py
   ```

3. **Open in browser:**
   ```
   http://localhost:5000
   ```

## Features

✅ **Easy Web Interface** - No command-line needed
✅ **Holding Registers** - Read/Write register values
✅ **Coils** - Read/Write coil states
✅ **Real-time Status** - Monitor server status
✅ **No Installation Hassles** - Just run and go

## How to Use

### Reading Registers
1. Set the start address (0-99)
2. Set how many registers to read (1-100)
3. Click **Read** button
4. View results instantly

### Writing Registers
1. Enter values separated by commas (e.g., `100,200,300`)
2. Set the start address
3. Click **Write** button
4. Confirmation message appears

### Coils
Same process as registers - read existing coil states or write new values (0 or 1).

## Requirements

- Python 3.8+
- pymodbus 3.6.1
- Flask 3.0.0
- Flask-CORS 4.0.0

## Server Details

- **Modbus Port:** 5020
- **Web UI Port:** 5000
- **Host:** localhost
- **Registers:** 100 Holding Registers, 100 Coils, 100 Discrete Inputs, 100 Input Registers

## Testing with External Tools

You can also connect Modbus clients to `localhost:5020`:
- **Python Client** - see `client_example.py`
- **QModbus** - GUI client
- **modbus-cli** - Command line tool

## Troubleshooting

**Port already in use?**
- Change port in `app.py` (web UI port) or edit the code for Modbus port

**Can't see values change?**
- Click "Refresh" or check the status indicator

**Server shows offline?**
- Restart the application
- Check Python version (3.8+ required)

## License

MIT

