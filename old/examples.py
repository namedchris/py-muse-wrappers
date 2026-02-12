"""
Example usage of the panel wrapper

This demonstrates how to use the wrapper in a MUSE Python script.
"""

# === Basic Setup ===
from mojo import context
from panel import load_panel

# Get the touchpad device from MUSE context
touchpad = context.devices.get("AMX-10001")

# Load panel configuration from CSV
panel = load_panel(touchpad, "EOC-202.CSV")

# === Access buttons by page ===
tiled_mode_page = panel.get_page("Tiled Mode")
display_one = tiled_mode_page.get_button("Display One_1_1")

# Use button methods - commands automatically route to correct port
display_one.show_hide(True)
display_one.set_text("1", "Display 1")
display_one.enable(True)

# === Access stream selector buttons ===
stream_page = panel.get_page("Stream Selector")
confirm_btn = stream_page.get_button("Confirm_2_42")
cancel_btn = stream_page.get_button("Cancel_2_41")

# Set button states
confirm_btn.set_background_color("1", "Green")
cancel_btn.set_background_color("1", "Red")

# === Iterate through all pages and buttons ===
for page in panel.subcomponents:
    print(f"Page: {page.name}")
    for button in page.subcomponents:
        print(f"  Button: {button.name}")
        print(f"    Port: {button.port}, Address: {button.address}, Channel: {button.channel}")

# === Set up button event handlers ===
def on_display_one_press(update):
    print(f"Display One pressed! State: {update.value}")
    # Do something when button is pressed

# Note: Button events are handled through MUSE's watch mechanism on the device
# The wrapper provides the command sending, but events come from the device itself
# Example:
# touchpad.port[0].button[1].watch(on_display_one_press)

context.run(globals())
