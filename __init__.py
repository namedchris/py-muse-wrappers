"""
py-muse-wrappers
================

Python wrapper for AMX MUSE touchpad panels (Modero X Series G5).
Provides a clean component-based abstraction layer with state management.

## Project Status

Currently implementing the core rendering and state management system.

## Architecture Overview

### Component Hierarchy Pattern
Uses a hierarchical component tree where each component manages its own state:
- Panel (top level) → Pages → Buttons (leaf nodes)
- Each component has a `state` dict for storing UI state
- Components can have subcomponents (parent-child relationships)

### Key Design Decisions

1. **State Storage**: Direct Python objects only
   - State lives in `component.state` dicts
   - NO dataclasses, NO automatic JSON (removed state.py)
   - Serialization will be handled by a custom provider later (see serialization.py)

2. **Command Architecture**:
   - Buttons are NOT "dumb" - they know how to send commands
   - `send_command` callback is OPTIONAL (allows offline testing)
   - All button command methods check `if self._send_command is None: return`

3. **Rendering**: Phoenix LiveView model (server-side state authority)
   - State managed server-side
   - `render()` pushes state changes to "dumb" display client
   - No diffing yet (manual render), but could add later

4. **Event-Driven**: Eventually will support state machines for complex state transitions

## MUSE API Quick Reference

```python
from mojo import context

# Get device (auto-named AMX-<device_number>)
touchpad = context.devices.get("AMX-10001")

# Send commands (0-indexed ports!)
touchpad.port[0].send_command("^TXT-500,0,Hello")  # Port 1, Button 500

# Watch button events
def on_button_press(update):
    print(f"Button {update.id} = {update.value}")  # True/False

touchpad.port[0].button[500].watch(on_button_press)

context.run(globals())
```

**CRITICAL**: MUSE uses 0-based port arrays (port[0] = NetLinx Port 1)
Our wrapper handles this: `panel.send_command(port, cmd)` does `port[port-1]`

## G5 Command API Quick Reference

All commands documented in docs/g5_guide.txt. Key patterns:

```python
# Command format (state: 0=all, 1=off, 2=on)
"^TXT-<addr>,<state>,<text>"              # Set text
"^BCF-<addr>,<state>,<color>"             # Background color (name or #RRGGBB)
"^SHO-<addr>,<0|1>"                       # Show(1)/Hide(0)
"^ENA-<addr>,<0|1>"                       # Enable(1)/Disable(0)
"^BMP-<addr>,<state>,<bitmap>"            # Set bitmap/image
"^BOP-<addr>,<state>,<opacity>"           # Opacity 0-255
```

Address can be a range: "500.504&510.515" = buttons 500-504 and 510-515

## File Structure

### Core Implementation
- `component.py` - Base Component class with state dict and hierarchy
  - Has `export_state()` / `import_state()` for Python dict snapshots
  - Removed `save_state()` / `load_state()` (JSON serialization moved out)

- `buttons.py` - BaseButton class with ALL NetLinx command methods
  - Inherits from Component
  - Optional `send_command` callback (defaults to None)
  - All methods check for None before sending

- `panel.py` - Panel and Page classes, CSV parser
  - `Panel` - Top-level container, has MUSE device reference
  - `Page` - Contains buttons
  - `parse_panel_csv()` - Loads AMX TPDesign export CSV
  - `load_panel()` - Convenience function to create Panel from CSV + device

- `serialization.py` - Placeholder for future JSON/persistence (TODO)

### Examples & Utils
- `component_example.py` - Shows component hierarchy pattern
- `examples.py` - Basic usage examples (UPDATED to use subcomponents)
- `dump_config.py` - View parsed CSV configuration
- `state_example.py` - DEPRECATED (references old state.py)
- `init_state.py` - DEPRECATED (references old state.py)

### Documentation
- `docs/README.md` - Updated with component-based architecture
- `docs/g5_guide.txt` - G5 command reference (NetLinx syntax)
- `docs/muse_doc_extract.txt` - MUSE controller docs
- `docs/muse_thing_api.txt` - MUSE HControl API (Python examples)

### Configuration
- `EOC-202.CSV` - Example panel configuration

## Current Implementation Status

### ✅ Complete
- Component hierarchy (Panel → Page → Button)
- CSV parser for TPDesign exports
- All NetLinx button commands implemented
- Optional send_command callbacks
- State dict structure on all components
- Export/import state as Python dicts
- Documentation updated

### 🚧 TODO (Critical)
1. **Implement `button.render()`** - Sync state dict to device
   ```python
   def render(self):
       # Read self.state dict
       # Send commands to sync state to touchpad
       if self.state.get("text"):
           self.set_text("0", self.state["text"])
       # etc...
   ```

2. **Decide on render strategy**:
   - Option 1: Manual render (simple, explicit)
   - Option 2: Shadow state (track last rendered, only send diffs)
   - Option 3: State machines (transitions trigger renders)
   - Option 4: Something else?

3. **State machines** (for complex state transitions)
   - Event-driven state transitions
   - Auto-render on state entry
   - Trivial persistence (just save FSM state + context)

4. **Serialization provider** (if needed)
   - Implement JSON save/load in serialization.py
   - Use export_state() / import_state()

## Next Steps

1. Implement basic `render()` in buttons.py
2. Test with actual MUSE device
3. Add state machine support if needed
4. Add serialization if needed

## Important Notes

- **Port Numbering**: MUSE is 0-indexed, NetLinx is 1-indexed
  - Our wrapper abstracts this (users pass 1-based, we convert)

- **Button States**:
  - "0" = all states
  - "1" = off state
  - "2" = on state
  - Can use ranges: "1-256"

- **Button Addressing**:
  - From CSV: address_code (like 1, 2, 500, etc.)
  - Can be ranges in commands: "500.504" or "500.504&510.515"

- **No State Diffing Yet**:
  - Currently render() will send all state properties
  - Could add dirty tracking later if needed
  - LiveView model = server has authority, push updates

## Design Philosophy

Keep it simple:
- Direct Python objects over abstractions
- Explicit over implicit (manual render > auto-magic)
- Flat is better than nested (state dicts > dataclasses)
- Can always add complexity later if needed

## Questions to Resolve

1. Should render() send all fields or track dirty state?
2. Do we need state machines? (Seems like yes for complex buttons)
3. Do we need JSON persistence? (Probably yes eventually)
4. Should we support batch rendering? Context managers?

## References

- AMX G5 Programming Guide: docs/g5_guide.txt
- MUSE Programming Guide: docs/muse_doc_extract.txt
- MUSE Thing API: docs/muse_thing_api.txt
- TPDesign5: For creating panel configurations

---

For new sessions, read this file first to catch up on project status.
"""
