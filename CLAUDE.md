# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python wrapper library for AMX MUSE G5 touchpad panels. Provides a clean abstraction layer with automatic state management, dirty tracking, and hierarchical component structure for building touchpad control interfaces.

## Development Commands

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_user_code.py

# Run with verbose output
pytest -v
```

### Viewing Panel Configuration
```bash
# Parse and display TPDesign CSV configuration
python3 -c "from devices.touchpad import Touchpad; t = Touchpad('AMX-10001', 'tests/EOC-202.CSV'); t.dump_config()"
```

## Architecture

### Component Hierarchy Pattern
The library uses a hierarchical component system where each component manages its own state:

- **Component** (`components/component.py`) - Abstract base class with:
  - `state` dict for arbitrary state storage
  - `_subcomponents` list for hierarchy
  - `render()` and `render_all()` methods
  - `export_state()` / `import_state()` for state serialization

- **Button** (`components/buttons/buttons.py`) - Leaf component with:
  - Automatic dirty tracking via `__setattr__` override
  - State attributes (text, visible, enabled, opacity, etc.) mapped to command functions
  - `render()` only sends commands for modified attributes since last render

- **Device/Touchpad** (`devices/`) - Device abstraction with:
  - Automatic 0-based to 1-based port conversion
  - CSV config parsing for TPDesign exports
  - Button creation with callback registration
  - `send_command` delegation to MUSE device ports

### Key Design Patterns

1. **Dirty Tracking**: Button state changes are tracked automatically. Setting `button.text = "foo"` marks the text command as dirty, and `button.render()` only sends modified commands.

2. **Command Functions**: All G5 NetLinx commands are implemented as pure functions in `components/buttons/commands.py`. They take a Button object and read from `button.state` or `button` attributes.

3. **Callbacks**: ButtonCallback objects provide `on_click` and `on_release` handlers, registered via MUSE's watch() API.

4. **State Serialization**: Component state can be exported as nested dicts and imported back, preserving hierarchy.

## Port Number Conventions

**Critical**: Port numbers are 1-indexed in NetLinx commands but 0-indexed in Python MUSE API:
- CSV config has port numbers as 1-indexed (e.g., "1:10")
- Internal Python code uses 0-indexed (e.g., `device.port[0]`)
- Device class handles conversion automatically in `make_button_callback()`

## Button State Ranges

When sending button commands, state parameter meanings:
- `"0"` = all states
- `"1"` = off state
- `"2"` = on state

## CSV Configuration Format

TPDesign CSV exports have this structure:
```
"Panel Name"

Function codes utilized:

Page Name,Button Name,Channel Port:Code,Address Port:Code,Level Port:Code,Description
"Page Name"
,"Button Name", 1:10, 1:10,
```

The parser in `touchpad.py`:
- Creates pages dict from page headers (single column rows)
- Parses button rows with port:code format
- Uses `button_name_port_code` as unique key for duplicate button names

## Typical Usage Flow

1. **Create Touchpad**: `touchpad = Touchpad("AMX-10001", "config.csv")`
2. **Get Button**: `button = touchpad.pages["Page Name"]["button_key"]`
3. **Set State**: `button.text = "Hello"` (tracked as dirty)
4. **Render**: `button.render()` (sends only dirty commands)
5. **Wire Events**: `button.callback.set_on_click(lambda: handle_click())`

## Code Style Preferences

From CLAUDE_BEHAVIOR.md - the user prefers:
- Only implement what is explicitly requested (no extra features)
- Write simple, concise code (avoid over-engineering)
- Don't add verbose docstrings, type hints, or comments unless needed
- Don't use global variables in test code
- Keep test code minimal and focused

## File Organization

```
devices/
  device.py       - Base Device wrapper
  touchpad.py     - Touchpad with CSV config loading
  callbacks.py    - ButtonCallback for events
components/
  component.py    - Base Component abstraction
  buttons/
    buttons.py    - Button component with dirty tracking
    commands.py   - G5 command functions (pure functions)
tests/
  test_*.py       - pytest test files
docs/
  *.txt           - G5 API reference documentation
```

## Working with Button Commands

All G5 NetLinx commands are in `components/buttons/commands.py` as pure functions that:
- Take only a Button object as parameter
- Read from `button.state` dict or button attributes
- Call `button.send_command(cmd_string)` to send to device
- Are automatically invoked by dirty tracking on render()

To add new commands:
1. Add command function to `commands.py`
2. Add state attribute to `Button.STATE_ATTRIBUTES` set
3. Add mapping in `Button._ATTR_TO_COMMAND` dict

## Testing Without MUSE Controller

The Device class gracefully handles missing MUSE controller:
- `context.devices.get()` failures are logged as warnings
- `send_command` and callback registration become no-ops
- Tests can run without live hardware by checking if `device.device` is None
