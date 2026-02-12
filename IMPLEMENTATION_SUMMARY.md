# State Delta Tracking Implementation Summary

## Overview

Implemented automatic dirty tracking for button state management using `__setattr__` override. This allows for intuitive attribute-based state changes with automatic change detection.

## What Was Implemented

### 1. Attribute Access Pattern ✅

**Before (dict-based):**
```python
button.state["text"] = "Hello"
button.state["opacity"] = 200
button.render()
```

**After (attribute-based with automatic dirty tracking):**
```python
# Write using attribute access
button.text = "Hello"
button.opacity = 200
button.render()  # Only sends commands for text and opacity

# Read using dict access
value = button.state['text']
```

### 2. Automatic Dirty Tracking ✅

- `__setattr__` intercepts attribute assignments
- Stores values in internal `state` dict
- Automatically marks attributes as "dirty" in `_dirty_attrs` set
- `render()` only sends commands for dirty attributes
- Dirty flags cleared after successful render

### 3. State-to-Command Mapping ✅

**Simple 1:1 Mappings (11 attributes → 11 commands):**
- `text` → `set_text()`
- `visible` → `set_button_visible()`
- `enabled` → `set_button_enabled()`
- `focused` → `set_button_focus()`
- `background_color` → `set_background_color()`
- `opacity` → `set_button_opacity()`
- `video_fill` → `set_video_fill()`
- `bargraph_high` → `set_bargraph_high()`
- `bargraph_low` → `set_bargraph_low()`
- `streaming_url` → `set_streaming_media()`
- `subpage_padding` → `set_subpage_padding()`

\].level[level_code].value`

### 4. Key Methods Implemented ✅

**`__setattr__(name, value)`**
- Intercepts attribute assignments
- Stores state attributes in `state` dict
- Marks attributes as dirty
- Allows normal assignment for non-state attributes
- Reading state must use `button.state['key']` (no `__getattr__` override)

**`send_command(cmd_string)`**
- Wrapper around `_send_command` callback
- Handles None check (no-op if device not connected)

**`render(force=False)`**
- Sends commands only for dirty attributes
- Handles bitmap multi-attribute case (sends once)
- Clears dirty flags after rendering
- Idempotent (safe to call multiple times)

### Basic Usage
```python
from components.buttons.buttons import Button

# Create button
button = Button("test", port=1, address=500, channel=1,
                send_command=device_send_command)

# Set attributes (automatically marked dirty)
button.text = "Hello"
button.opacity = 200

# Render (sends 2 commands)
button.render()

# Render again (sends nothing - no dirty attrs)
button.render()
```

