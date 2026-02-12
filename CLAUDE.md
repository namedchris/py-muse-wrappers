# py-muse-wrappers - Project Context for Claude

**Read this file first when starting a new session.**

## Project Overview

Python wrapper for AMX MUSE touchpad panels (Modero X Series G5). Provides a component-based abstraction layer with state management for controlling touchscreen panels in AV control systems.

## Current Status: Code in Transition 🔄

**IMPORTANT**: The codebase is currently being restructured. `components/buttons/buttons.py` is the canonical implementation. Other files (panel.py, examples, etc.) are outdated and will be updated to match buttons.py later.

**Current Focus**: Updating Button constructor to integrate with MUSE device for channel/level references

**Recently Completed**:
- Automatic dirty tracking with `__setattr__` override ✅
- 18 state attributes (16 renderable + 2 logical) ✅
- State-to-command mapping via command functions ✅
- `render()` only sends commands for dirty attributes ✅

**Next**: Complete MUSE device integration for channels/levels

## Key Architecture Decisions

### 1. State Storage: Python Objects Only
- State lives in `component.state` dicts (plain Python dicts)
- **NO dataclasses**, **NO automatic JSON**
- Deleted `state.py` (old dataclass-based system)
- JSON serialization will be handled by separate provider later (`serialization.py` is TODO)

### 2. Component Hierarchy Pattern
```
Panel (top)
  └─ Page
      └─ Button (leaf nodes)
```

### 4. Rendering Philosophy: Dirty Tracking with Manual Render
- Server-side state authority
- State changes via attribute access automatically mark attributes as "dirty"
- Manual `render()` call → only sends commands for dirty attributes
- Device is "dumb display" (no client side code outside of configurable events)
- Automatic diffing via `__setattr__` override and dirty tracking

### 5. Level and Channel Updates
- **Level and channel do NOT use send_command** - they use direct MUSE API references
- Button stores references to MUSE device objects:
  - `self._channel_ref = device.port[channel_port-1].channel[channel_code]`
  - `self._level_ref = device.port[level_port-1].level[level_code]` (if level defined)
- Setting attributes updates the references:
  - `button.level = 50` → `self._level_ref.value = 50`
  - Channel on/off updates `self._channel_ref.value`
- These are set in Button constructor and don't go through dirty tracking

### 5. Event-Driven Future
- Will add state machines for complex button states
- Persistence via event sourcing or state snapshots

## Critical API Knowledge

### MUSE Python API
```python
from mojo import context

# Get device by name (AMX-<device_number> in URL mode)
touchpad = context.devices.get("AMX-10001")

# Send commands - PORTS ARE 0-INDEXED!
touchpad.port[0].send_command("^TXT-500,0,Hello")  # Port 1

# Watch button events
def on_button_press(update):
    print(f"Button {update.id} = {update.value}")
    # update.path = "port/0/button/500"

touchpad.port[0].button[500].watch(on_button_press)

# Required at end of script
context.run(globals())
```

**CRITICAL**: MUSE uses 0-based port arrays
- NetLinx "Port 1" = `touchpad.port[0]`
- Our wrapper handles this: `panel.send_command(1, cmd)` → `device.port[0].send_command(cmd)`

### G5 Command Format
Commands are NetLinx strings sent via `send_command()`:

```python
# Button state: 0=all states, 1=off, 2=on
"^TXT-<addr>,<state>,<text>"        # Set text
"^BCF-<addr>,<state>,<color>"       # Background color (#RRGGBB or name)
"^SHO-<addr>,<0|1>"                 # Show(1) / Hide(0)
"^ENA-<addr>,<0|1>"                 # Enable(1) / Disable(0)
"^BMP-<addr>,<state>,<image>"       # Set bitmap
"^BOP-<addr>,<state>,<0-255>"       # Set opacity
```

Address ranges: `"500.504&510.515"` = buttons 500-504 AND 510-515

## File Structure

### Core Implementation (In Transition)
- **`components/component.py`** - Base class with state dict, subcomponents, export/import ✅
- **`components/buttons/buttons.py`** - Button class with automatic dirty tracking ✅ **[CANONICAL]**
- **`components/buttons/commands.py`** - All NetLinx button command functions (29 methods) ✅
- **`components/buttons/__init__.py`** - Module init
- **`panel.py`** - Panel/Page classes, CSV parser ⚠️ **OUTDATED** (imports old BaseButton)
- **`serialization.py`** - TODO placeholder for JSON save/load

### Examples (Outdated - Need Updates)
- **`component_example.py`** - ⚠️ Uses old patterns
- **`examples.py`** - ⚠️ Needs update to use new Button
- **`dump_config.py`** - CSV viewer (still valid) ✓
- **`test_dirty_tracking.py`** - ⚠️ Uses old Button signature
- **`render_example.py`** - ⚠️ Unknown status

### Documentation
- **`docs/README.md`** - Updated with component architecture ✓
- **`docs/g5_guide.txt`** - NetLinx command reference (54K lines)
- **`docs/muse_doc_extract.txt`** - MUSE programming guide
- **`docs/muse_thing_api.txt`** - HControl API with Python examples

### Config
- **`EOC-202.CSV`** - Example panel config from TPDesign

## What's Complete ✅

1. Component hierarchy (Panel → Page → Button)
2. CSV parser (`parse_panel_csv()` in panel.py)
3. All 29 NetLinx button commands implemented
4. Optional send_command callbacks (None-safe)
5. State dict on all components
6. Export/import state as Python dicts
7. Documentation updated

## What's Recently Completed ✅

### 1. Automatic Dirty Tracking with `__setattr__` Override - IMPLEMENTED!
Full dirty tracking system:
- `__setattr__` intercepts attribute assignments (e.g., `button.text = "Hello"`)
- Automatically marks attributes as "dirty" when changed
- `render()` only sends commands for dirty attributes
- Tracks `_dirty_attrs` set to know what changed
- `render_all(force=True)` to mark all attributes dirty
- `mark_all_dirty()` to force full re-render
- Reading state uses dict access: `button.state['text']`

### 2. Attribute Access Pattern
State can be set via attributes, read via dict:
```python
# Setting: Use attribute access (automatic dirty tracking)
button.text = "Hello"
button.opacity = 200

### 3. Comprehensive State Attributes
Added ALL mutable button state from G5 docs:

**Text:** `text`

**Visibility/Interaction:** `visible`, `enabled`, `focused`

**Appearance:** `background_color`, `opacity`

**Bitmap:** `bitmap`, `bitmap_index`, `bitmap_justification`, `bitmap_x`, `bitmap_y`

**Video:** `video_fill` (0=off, 1=URL, 101=MPL)

**Bargraph:** `bargraph_high`, `bargraph_low`, `level`

**Streaming:** `streaming_url`

**Subpage:** `subpage_padding`

**Logical (not rendered):** `is_on` (for FSM use)

**Special (direct MUSE API):** `level` (uses `device.port[].level[].value`, not commands)

### 4. Automatic Dirty Tracking Rendering
Implemented automatic change detection:
- Only sends commands for changed attributes
- Efficient for FSM transitions (set multiple attrs, render once)
- Idempotent (safe to call repeatedly)
- Bitmap multi-attribute optimization (5 attrs → 1 command)
- Level and channel handled separately (direct MUSE API, not dirty tracked)

## What's NOT Done 🚧

### 1. Channel and Level Integration (Next Priority)

**Approach: Callback pattern within mutate → render flow**

Keep channel/level in the existing state management pattern for consistency:
```python
button.channel = True   # Mutate state (marks dirty)
button.level = 50       # Mutate state (marks dirty)
button.render()         # Callbacks fire for dirty channel/level
```

**Implementation plan:**
1. Add `channel` to `STATE_ATTRIBUTES` in Button class
2. Add `channel_callback` and `level_callback` parameters to Button constructor
3. Add channel/level to `_ATTR_TO_COMMAND` mapping (but they call callbacks instead of send_command)
4. In `render()`, call callbacks for dirty channel/level attributes
5. Panel/Page auto-creates callbacks from MUSE device when wiring up buttons

**Auto-callback creation example:**
```python
# In Page.__init__ when creating buttons:
button = Button(
    name=button_config.name,
    address_port=button_config.address_port,
    address_code=button_config.address_code,
    channel_port=button_config.channel_port,
    channel_code=button_config.channel_code,
    send_command=lambda cmd: panel.send_command(port, cmd),
    channel_callback=lambda val: device.port[channel_port-1].channel[channel_code].value = val,
    level_callback=lambda val: device.port[level_port-1].level[level_code].value = val  # if level defined
)
```

**Benefits:**
- ✅ Testable via dependency injection (mock callbacks)
- ✅ Consistent with existing mutate → render pattern
- ✅ Automated (Panel wires up callbacks from device)
- ✅ Intuitive user API (`button.channel = True` instead of accessing device directly)
- ✅ No tight coupling to MUSE device in Button class




### 4. JSON Serialization
If needed, implement in `serialization.py`:
```python
def save_json(component, filepath):
    state = component.export_state()
    json.dump(state, open(filepath, 'w'))

def load_json(component, filepath):
    state = json.load(open(filepath))
    component.import_state(state)
```

## Important Notes

### Port Numbering
- NetLinx/G5 docs: 1-based (Port 1, Port 2)
- MUSE Python API: 0-based arrays (`port[0]`, `port[1]`)
- **Our wrapper uses 1-based** (user-friendly), converts internally

### Button State Numbers
- `"0"` = all button states
- `"1"` = off state (unpressed)
- `"2"` = on state (pressed)
- Can use ranges: `"1-256"`

### Button State Dictionary (Complete)
All renderable state attributes in `buttons.py`:
```python
self.state = {
    # Logical state (not rendered)
    "is_on": False,

    # Text
    "text": "",

    # Visibility/Interaction
    "visible": True,
    "enabled": True,
    "focused": False,

    # Appearance - Colors/Opacity
    "background_color": None,  # Name or #RRGGBB
    "opacity": None,  # 0-255

    # Appearance - Bitmap
    "bitmap": None,
    "bitmap_index": 1,  # 1-5
    "bitmap_justification": None,  # 0-10
    "bitmap_x": None,
    "bitmap_y": None,

    # Video
    "video_fill": None,  # 0/1/101

    # Bargraph
    "bargraph_high": None,
    "bargraph_low": None,
    "level": None,  # NOTE: Uses direct MUSE API (_level_ref.value), not commands

    # Streaming
    "streaming_url": None,

    # Subpage
    "subpage_padding": None,  # 0-100
}
```

**Note**: FSMs can add custom fields!

**Level attribute special case**: Setting `button.level = 50` updates the MUSE device reference `button._level_ref.value = 50` directly, not through commands. This bypasses dirty tracking.

### Dirty Tracking Implementation Details

**How it works:**
1. `__setattr__` intercepts all attribute assignments
2. State attributes are stored in `self.state` dict
3. Changed attributes are added to `self._dirty_attrs` set
4. `render()` iterates over dirty attrs and calls corresponding command functions
5. Dirty flags are cleared after successful render

**Attribute-to-Command Mapping:**
- Simple 1:1: `text` → `set_text()`, `opacity` → `set_button_opacity()`, etc.
- Multi-attribute: All 5 bitmap attrs → `set_state_bitmap()` (called once)
- Logical only: `is_on` (no rendering)
- Direct API: `level` (uses `_level_ref.value`, not commands)
- Channel: Uses `_channel_ref.value` for on/off (not in state attributes)

**Usage Example:**
```python
# Set attributes (automatically marked dirty)
button.text = "Hello"
button.opacity = 200
button.visible = False

# Render (sends 3 commands)
button.render()

# Render again (sends nothing - no dirty attrs)
button.render()

# Force full re-render
button.render_all(force=True)  # or button.mark_all_dirty()
```

### CSV Format
TPDesign export format. Button key = `"{name}_{address_port}_{address_code}"`

Example: Button "Display One" at address 1:1 → `"Display One_1_1"`

## Next Session Action Items

1. ~~**Implement `render()`** in buttons.py~~ ✅ DONE
2. ~~Decide on render strategy~~ ✅ DONE - Dirty tracking with `__setattr__`
3. ~~Add all G5 state attributes~~ ✅ DONE - 18 state attributes
4. ~~Implement automatic dirty tracking~~ ✅ DONE - `__setattr__` override
5. **Implement level and channel integration** (next priority)
   - Store `_channel_ref` and `_level_ref` in Button constructor
   - Override `__setattr__` for `level` to update `_level_ref.value`
   - Add methods for channel on/off
6. **Test with actual MUSE device**
7. **Implement state machine support** (design FSM integration)
8. Implement serialization if needed

## Questions to Ask User

1. ~~What render strategy do you prefer?~~ ✅ ANSWERED - Dirty tracking with manual render
2. Do you need JSON persistence? When/how often will state be saved?
3. Do your buttons have complex state transitions that need FSMs?
4. ~~Any other state properties?~~ ✅ ANSWERED - All 18 state attributes implemented

## Common Gotchas

- ⚠️ Don't forget `context.run(globals())` at end of MUSE scripts
- ⚠️ Ports are 0-indexed in MUSE, 1-indexed in docs
- ⚠️ Button address ranges use `.` and `&`: `"500.504&510.515"`
- ⚠️ State "0" = all states (both on and off)
- ⚠️ Send commands check for None, but won't error if device disconnected
- ⚠️ **Use attribute access** (`button.text = "Hello"`) for automatic dirty tracking
- ⚠️ Direct dict access (`button.state["text"] = "Hello"`) bypasses dirty tracking
- ⚠️ Remember to call `render()` after setting attributes - changes aren't sent automatically

## Useful Commands

```bash
# View config
python dump_config.py EOC-202.CSV

# Convert PDF docs (already done)
pdftotext docs/g5_guide.pdf docs/g5_guide.txt
```

---
