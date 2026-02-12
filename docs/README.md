# MUSE Panel Wrapper

Python wrapper for AMX MUSE touchpad panels. Provides a clean abstraction layer with state management.

## Architecture

The wrapper uses a **component hierarchy** pattern where each component manages its own state:

- **Component** (`component.py`) - Base class with state dict and hierarchical structure
- **Panel/Page/Button** (`panel.py`, `buttons.py`) - Components with state and command methods
- **Serialization** (`serialization.py`) - Custom provider for JSON/etc. (TODO)
- **Workflow**: Events → Update Component State → Render Components → Export State

## Quick Start

### 1. Load Panel Configuration

```python
from mojo import context
from panel import load_panel

touchpad = context.devices.get("AMX-10001")
panel = load_panel(touchpad, "EOC-202.CSV")
```

### 2. Update State

```python
# Get button component
page = panel.get_page("Tiled Mode")
button = page.get_button("Display One_1_1")

# Modify state dict
button.state["text"] = "Display 1"
button.state["visible"] = True
button.state["enabled"] = True
button.state["background_color"] = "Blue"
```

### 3. Render to Touchpad

```python
# Render entire panel hierarchy
panel.render_all()

# Or render single button
button.render()
```

### 4. Wire Up Events

```python
# Get button reference
page = panel.get_page("Tiled Mode")
button = page.get_button("Display One_1_1")

def on_button_press(update):
    # Update state
    button.state["is_on"] = update.value

    # Render changes
    button.render()

    # Export and save state (using custom serialization provider - TODO)
    # state_data = panel.export_state()
    # serialization.save_json(state_data, "panel_state.json")

# Wire up event handler (implementation depends on MUSE event system)
# touchpad.on_channel_event(button.channel, on_button_press)
```

### 5. Save/Load State

```python
# Export state as Python dict
state_data = panel.export_state()

# Import state from Python dict
panel.import_state(state_data)
panel.render_all()  # Sync touchpad with loaded state

# TODO: JSON serialization will be handled by custom serialization provider
# from serialization import StateSerializer
# StateSerializer.save_json(panel, "panel_state.json")
# StateSerializer.load_json(panel, "panel_state.json")
```

## File Structure

```
component.py        - Base Component class with state and hierarchy
buttons.py          - BaseButton class with all command methods
panel.py            - Panel, Page classes and CSV parser
serialization.py    - Custom serialization provider (TODO)
examples.py         - Basic usage examples
component_example.py - Component hierarchy usage example
dump_config.py      - View parsed CSV configuration
```

## Command Line Tools

### View Panel Configuration
```bash
python3 dump_config.py EOC-202.CSV
```
Shows all pages, buttons, ports, and addresses from the CSV.


## State Structure

Each component has a `state` dict. For buttons, the typical structure is:

```python
button.state = {
    "text": "",
    "is_on": False,
    "enabled": True,
    "visible": True,
    "background_color": None,
    "text_color": None,
    "bitmap": None,
    "opacity": None,  # 0-255
    "level": None,
    # Add any custom fields you need
    "stream_url": "http://example.com/stream",
    "custom_data": {...}
}
```

### Working with State
```python
# Get components
page = panel.get_page("Tiled Mode")
button = page.get_button("Display One_1_1")

# Update state
button.state["text"] = "Display 1"
button.state["is_on"] = True
button.state["custom_data"] = {"foo": "bar"}

# Panel-level state
panel.state["current_mode"] = "tiled"

# Page-level state
page.state["layout"] = "2x2"
```

All state is exported/imported as nested Python dicts via `export_state()` / `import_state()`.

## Button Commands

All NetLinx commands from the G5 guide are implemented on `BaseButton`. Examples:

```python
button = page.get_button("Display One_1_1")

# Basic commands
button.show_hide(True)
button.enable(True)
button.set_text("1", "Display 1")
button.set_background_color("1", "Blue")

# State commands
button.set_bitmap("1", "image.png")
button.set_opacity("1", 200)
button.animate(0, 5, 10)

# Subpage commands
button.subpage_show("menu1", 0, 10)
button.subpage_hide("menu2", 10)

# Bargraph commands
button.set_bargraph_high(255)
button.set_bargraph_low(0)
```

See `buttons.py` for complete command reference.

## Panel CSV Format

The wrapper parses AMX TPDesign export CSV files. Format:

```csv
"Panel Name"

Function codes utilized:

Page Name,Button Name,Channel Port:Code,Address Port:Code,Level Port:Code,Description
"Page Name"
,"Button Name", 1:10, 1:10,
```

## Workflow Example

```python
from mojo import context
from panel import load_panel

# Setup
touchpad = context.devices.get("AMX-10001")
panel = load_panel(touchpad, "EOC-202.CSV")

# Initialize state for all buttons
for page in panel.subcomponents:
    for button in page.subcomponents:
        button.state["enabled"] = True
        button.state["visible"] = True
        button.state["text"] = button.name

# Render initial state
panel.render_all()

# Wire up events
def on_button_press(update):
    # Find the button (implementation depends on event data)
    page = panel.get_page("Page Name")
    button = page.get_button("Button_1_1")

    # Update state
    button.state["is_on"] = update.value

    # Render changes
    button.render()

    # Export state (for saving later)
    state_data = panel.export_state()

# Register with MUSE event system
# touchpad.on_channel_event(channel, on_button_press)

context.run(globals())
```

## Notes

- Port numbers are 1-indexed in NetLinx but 0-indexed in Python arrays
- Button state ranges: "0" = all states, "1" = off state, "2" = on state
- Commands automatically route to correct port based on button configuration
- State is stored directly in component `state` dicts
- `export_state()` / `import_state()` work with Python dicts
- JSON serialization will be handled by custom provider (see `serialization.py`)
