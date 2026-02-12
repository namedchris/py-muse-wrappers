"""
Test script for button dirty tracking and render system.
"""

# Add parent directory to path for imports
import sys
sys.path.insert(0, '/mnt/c/Users/crmorga/projects/py-muse-wrappers')

from components.buttons.buttons import Button

# Track commands sent
commands_sent = []

def mock_send_command(cmd):
    """Mock send_command that captures commands."""
    commands_sent.append(cmd)
    print(f"  COMMAND: {cmd}")

print("=" * 70)
print("Test 1: Basic State Change via Attribute Access")
print("=" * 70)
button = Button("test_button", port=1, address=500, channel=1, send_command=mock_send_command)
print(f"Initial dirty attrs: {button._dirty_attrs}")
print(f"Initial text: {repr(button.state['text'])}")
print(f"Initial opacity: {button.state['opacity']}")

print("\nSetting button.text = 'Hello'")
button.text = "Hello"
print(f"Dirty attrs after setting text: {button._dirty_attrs}")
print(f"Text value: {repr(button.state['text'])}")

print("\nCalling button.render()")
commands_sent.clear()
button.render()
print(f"Dirty attrs after render: {button._dirty_attrs}")
print(f"Commands sent: {len(commands_sent)}")

print("\nCalling button.render() again (should send nothing)")
commands_sent.clear()
button.render()
print(f"Commands sent: {len(commands_sent)}")

print("\n" + "=" * 70)
print("Test 2: Multiple Changes")
print("=" * 70)
button.text = "World"
button.visible = False
button.opacity = 200
print(f"Dirty attrs: {button._dirty_attrs}")

print("\nCalling button.render()")
commands_sent.clear()
button.render()
print(f"Commands sent: {len(commands_sent)}")
print(f"Dirty attrs after render: {button._dirty_attrs}")

print("\n" + "=" * 70)
print("Test 3: Bitmap Multi-Attribute")
print("=" * 70)
button.bitmap = "icon.png"
button.bitmap_justification = 5
button.bitmap_x = 100
button.bitmap_y = 50
print(f"Dirty attrs: {button._dirty_attrs}")

print("\nCalling button.render()")
commands_sent.clear()
button.render()
print(f"Commands sent (should be 1, not 4): {len(commands_sent)}")

print("\n" + "=" * 70)
print("Test 4: Force Re-render")
print("=" * 70)
print("\nCalling button.render_all(force=True)")
commands_sent.clear()
button.render_all(force=True)
print(f"Commands sent: {len(commands_sent)}")

print("\n" + "=" * 70)
print("Test 5: Reading State")
print("=" * 70)
button.text = "Test Read"
button.opacity = 150
print(f"Reading button.state['text']: {repr(button.state['text'])}")
print(f"Reading button.state['opacity']: {button.state['opacity']}")

print("\n" + "=" * 70)
print("Test 6: None send_command")
print("=" * 70)
button_no_cmd = Button("test", 1, 500, 1, send_command=None)
button_no_cmd.text = "Test"
print(f"Dirty attrs: {button_no_cmd._dirty_attrs}")
print("Calling button.render() (should not error)")
button_no_cmd.render()
print("Success - no errors")

print("\n" + "=" * 70)
print("Test 7: mark_all_dirty()")
print("=" * 70)
button.mark_all_dirty()
print(f"Dirty attrs after mark_all_dirty(): {len(button._dirty_attrs)} attrs")
commands_sent.clear()
button.render()
print(f"Commands sent: {len(commands_sent)}")

print("\n" + "=" * 70)
print("All tests completed successfully!")
print("=" * 70)
