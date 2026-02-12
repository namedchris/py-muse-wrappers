from typing import Callable, Optional
from components.component import Component
from callbacks import ButtonCallback
from . import commands

# Justification constants
JUSTIFICATION_ABSOLUTE = 0
JUSTIFICATION_TOP_LEFT = 1
JUSTIFICATION_TOP_CENTER = 2
JUSTIFICATION_TOP_RIGHT = 3
JUSTIFICATION_MIDDLE_LEFT = 4
JUSTIFICATION_MIDDLE_CENTER = 5
JUSTIFICATION_MIDDLE_RIGHT = 6
JUSTIFICATION_BOTTOM_LEFT = 7
JUSTIFICATION_BOTTOM_CENTER = 8
JUSTIFICATION_BOTTOM_RIGHT = 9
JUSTIFICATION_SCALE = 10


class Button(Component):
    """
    Button component with command methods and automatic dirty tracking.

    Buttons are leaf nodes in the component hierarchy.

    State attributes can be set via attribute access:
        button.text = "Hello"
        button.opacity = 200

    Changes are tracked automatically and sent to the device on render():
        button.text = "World"
        button.visible = False
        button.render()  # Only sends commands for text and visible
    """

    # Define which attributes are state (renderable) attributes
    STATE_ATTRIBUTES = {
        'text', 'visible', 'enabled', 'focused',
        'background_color', 'opacity',
        'bitmap', 'bitmap_index', 'bitmap_justification', 'bitmap_x', 'bitmap_y',
        'video_fill', 'bargraph_high', 'bargraph_low', 'level',
        'streaming_url', 'subpage_padding', 'is_on'
    }

    # Map state attributes to command functions (class-level, shared by all instances)
    _ATTR_TO_COMMAND = {
        'text': commands.set_text,
        'visible': commands.set_button_visible,
        'enabled': commands.set_button_enabled,
        'focused': commands.set_button_focus,
        'background_color': commands.set_background_color,
        'opacity': commands.set_button_opacity,
        'video_fill': commands.set_video_fill,
        'bargraph_high': commands.set_bargraph_high,
        'bargraph_low': commands.set_bargraph_low,
        'streaming_url': commands.set_streaming_media,
        'subpage_padding': commands.set_subpage_padding,
        # Bitmap is special - all 5 attrs trigger same command
        'bitmap': commands.set_state_bitmap,
        'bitmap_index': commands.set_state_bitmap,
        'bitmap_justification': commands.set_state_bitmap,
        'bitmap_x': commands.set_state_bitmap,
        'bitmap_y': commands.set_state_bitmap,
        # Note: channel and level changes use a different api and are manipulated directly by assignment, e.g., channel = true
    }

    def __init__(self, name: str, port: int, address_code: int, channel: int, callback: ButtonCallback, send_command: Optional[Callable[[str], None]] = None):
        """
        Initialize button.

        Args:
            name: Button identifier
            port: Port number
            address: Button address
            channel: Button channel
            callback: ButtonCallback for button events
            send_command: Optional callback to send commands (if None, commands are no-ops)
        """
        # Track which attributes have been modified since last render
        self._dirty_attrs = set()

        # Call parent init
        super().__init__(name)

        # Set core attributes
        self.port = port
        self.address = address_code
        self.channel = channel
        self.callback = callback
        self.send_command = send_command

        # Set state attributes with defaults (triggers __setattr__)
        self.is_on = False
        self.text = ""
        self.visible = True
        self.enabled = True
        self.focused = False
        self.background_color = None
        self.opacity = None
        self.bitmap = None
        self.bitmap_index = 1
        self.bitmap_justification = None
        self.bitmap_x = None
        self.bitmap_y = None
        self.video_fill = None
        self.bargraph_high = None
        self.bargraph_low = None
        self.level = None
        self.streaming_url = None
        self.subpage_padding = None

        # Clear dirty flags after initialization (defaults shouldn't be dirty)
        self._dirty_attrs.clear()

    def __setattr__(self, name, value):
        """
        Override attribute assignment to track state changes.

        When a state attribute is set (e.g., button.opacity = 12):
        1. Store value as normal object attribute
        2. Add associated command callable to dirty set
        """
        # Always do normal assignment
        object.__setattr__(self, name, value)

        # Add command callable to dirty set if attribute has one
        if name in self._ATTR_TO_COMMAND:
            self._dirty_attrs.add(self._ATTR_TO_COMMAND[name])



    def render(self, force=False):
        """
        Render button state to device by sending commands for dirty callables.

        Only sends commands for callables that have been marked dirty since the
        last render() call. The set automatically handles deduplication.

        This is idempotent and safe to call multiple times (sends nothing if no changes).

        Args:
            force: If True, marks all command callables as dirty to force full re-render
        """
        if self._send_command is None:
            return
        if force:
            # Mark all command callables as dirty
            self._dirty_attrs = set(self._ATTR_TO_COMMAND.values())
        
        # Call each dirty command function (set automatically deduplicates)
        for command in self._dirty_attrs:
            command(self)

        # Clear dirty flags after successful render
        self._dirty_attrs.clear()

