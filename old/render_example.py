"""
Example showing the new render system with automatic dirty tracking.

This demonstrates:
1. Loading a panel from CSV
2. Updating button state via attribute access (button.text = "...")
3. Automatic dirty tracking - only changed attributes trigger commands
4. Manual rendering with render()
"""

from mojo import context
from panel import load_panel

# Get touchpad device
touchpad = context.devices.get("AMX-10001")

# Load panel from CSV
panel = load_panel(touchpad, "EOC-202.CSV")

# Get a button
page = panel.get_page("Tiled Mode")
button = page.get_button("Display One_1_1")

# === Example 1: Simple attribute changes ===
print("=== Simple Attribute Changes ===")
button.text = "Display 1"
button.background_color = "Blue"
button.visible = True
button.enabled = True

button.render()  # Sends 4 commands (all marked dirty)

# === Example 2: Redundant render (dirty tracking optimization) ===
print("\n=== Redundant Render ===")
button.render()  # Sends 0 commands (nothing marked dirty)
button.render()  # Sends 0 commands (nothing marked dirty)

# === Example 3: Partial update ===
print("\n=== Partial Update ===")
button.background_color = "Green"  # Change one attribute
button.render()  # Sends 1 command (only background_color is dirty)

# === Example 4: Multiple updates ===
print("\n=== Multiple Updates ===")
button.text = "LIVE"
button.background_color = "Red"
button.opacity = 200
button.render()  # Sends 3 commands (3 attributes marked dirty)

# === Example 5: Force full re-render ===
print("\n=== Force Full Re-render ===")
button.render_all(force=True)  # Marks all attributes dirty and sends all commands

# === Example 6: FSM-style usage ===
print("\n=== FSM-Style Usage ===")

def transition_to_streaming():
    """Simulates FSM transition with attribute access"""
    button.text = "STREAMING"
    button.background_color = "Green"
    button.is_on = True  # Logical state (not rendered)
    button.render()  # Only sends changed attributes

def transition_to_error():
    """Simulates FSM transition with attribute access"""
    button.text = "ERROR"
    button.background_color = "Red"
    button.is_on = False
    button.render()  # Only sends changed attributes

transition_to_streaming()  # Efficient render
transition_to_error()  # Efficient render

# === Example 7: Complex bitmap state ===
print("\n=== Complex Bitmap Example ===")
button.bitmap = "camera_icon.png"
button.bitmap_index = 1
button.bitmap_justification = 5  # JUSTIFICATION_MIDDLE_CENTER
button.text = ""  # Clear text when showing icon
button.render()  # Sends 2 commands: set_state_bitmap (once for all bitmap attrs) and set_text

# === Example 8: Mark all dirty (force next render) ===
print("\n=== Mark All Dirty ===")
button.mark_all_dirty()
button.render()  # Will re-send all current state values

# === Example 9: Bargraph button ===
print("\n=== Bargraph Button ===")
bargraph_button = page.get_button("Volume_1_20")
bargraph_button.bargraph_low = 0
bargraph_button.bargraph_high = 100
bargraph_button.level = 50
bargraph_button.text = "Volume: 50%"
bargraph_button.render()

# === Example 10: Reading state ===
print("\n=== Reading State ===")
print(f"Button text: {button.state['text']}")
print(f"Button opacity: {button.state['opacity']}")
print(f"Button is_on: {button.state['is_on']}")
print(f"Full state dict: {button.state}")

# Required at end
context.run(globals())
