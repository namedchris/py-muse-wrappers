from typing import Callable, Optional
from components.component import Component
from devices.callbacks import ButtonCallback

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
        button.render()  # Only sends for text and visible
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
    _ATTR_TO_COMMAND = {}

    # Adds function mappings to _ATTR_TO_COMMAND
    def register_command(*attributes, mapping = _ATTR_TO_COMMAND):
        def decorator(func, mapping = mapping):
            for attribute in attributes:
                mapping[attribute] = func
            return func
        return decorator
    
    def __init__(self, callback: ButtonCallback, name: str, address_port: int, address_code: int, channel_port:int, channel_code: int, level_port:int = None, level_address: int =None, level_code: int= None,  send_command: Optional[Callable[[str], None]] = None):
        """
        Initialize button.

        Args:
            name: Button identifier
            port: Port number
            address: Button address
            channel: Button channel
            callback: ButtonCallback for button events
            send_command: Optional callback to send (if None, are no-ops)
        """
        # Track which attributes have been modified since last render
        self._dirty_attrs = set()

        # Call parent init
        super().__init__(name)

        # Set core attributes
        self.address_port = address_port
        self.address = address_code
        self.channel_port = channel_port
        self.channel = channel_code
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
        Render button state to device by sending for dirty callables.

        Only sends for callables that have been marked dirty since the
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
    
#region Button Commande

    # ============================================================================
    # Button (from button_txt)
    # ============================================================================

    def query_subpage_events(self):
        """
        Query assigned subpage custom event numbers for subpage viewer button.

        Args:
            button: The button object.
        """
        cmd_string = f"?SCE-{self.address}"
        self.send_command(cmd_string)

    @register_command('focused')
    def set_button_focus(button):
        """
        Button Focus Command. Reads from button.state["focused"].

        Args:
            button: The button object.
        """
        value = 1 if button.state.get("focused") else 0
        cmd_string = f"^BSF-{button.address},{value}"
        button.send_command(cmd_string)


    def submit_button_text(button):
        """
        Button Submit Text Command.
        Causes button text area to send its text as a string to the NetLinx Master.

        Args:
            button: The button object.
        """
        cmd_string = f"^BSM-{button.address}"
        button.send_command(cmd_string)


    def clear_page_flip(button):
        """
        Clear Page Flip Command.
        Clear all page flips from button release event action.

        Args:
            button: The button object.
        """
        cmd_string = f"^CPF-{button.address}"
        button.send_command(cmd_string)

    @register_command('bargraph_high')
    def set_bargraph_high(button):
        """
        Set Bargraph High Range Command. Reads from button.state["bargraph_high"].

        Args:
            button: The button object.
        """
        high_value = button.state.get("bargraph_high")
        if high_value is not None:
            cmd_string = f"^GLH-{button.address},{high_value}"
            button.send_command(cmd_string)

    @register_command('bargraph_low')
    def set_bargraph_low(button):
        """
        Set Bargraph Low Range Command. Reads from button.state["bargraph_low"].

        Args:
            button: The button object.
        """
        low_value = button.state.get("bargraph_low")
        if low_value is not None:
            cmd_string = f"^GLL-{button.address},{low_value}"
            button.send_command(cmd_string)

    
    @register_command('enabled')
    def set_button_enabled(button):
        """
        Button Enable Command. Reads from button.state["enabled"].

        Args:
            button: The button object.
        """
        value = 1 if button.state.get("enabled", True) else 0
        cmd_string = f"^ENA-{button.address},{value}"
        button.send_command(cmd_string)


    def subpage_hide_all(button):
        """
        Subpage Hide All Command.
        Hide all subpages in a subpage viewer button.

        Args:
            button: The button object.
        """
        cmd_string = f"^SHA-{button.address}"
        button.send_command(cmd_string)

    @register_command('visible')
    def set_button_visible(button):
        """
        Button Show/Hide Command. Reads from button.state["visible"].

        Args:
            button: The button object.
        """
        value = 1 if button.state.get("visible", True) else 0
        cmd_string = f"^SHO-{button.address},{value}"
        button.send_command(cmd_string)

    @register_command('subpage_padding')
    def set_subpage_padding(button):
        """
        Subpage Padding Command. Reads from button.state["subpage_padding"].

        Args:
            button: The button object.
        """
        padding = button.state.get("subpage_padding")
        if padding is not None:
            cmd_string = f"^SPD-{button.address},{padding}"
            button.send_command(cmd_string)


    # ============================================================================
    # Button State (from button_state_txt)
    # ============================================================================
    @register_command('background_color')
    def set_background_color(button):
        """
        Background Color Fill Command. Reads from button.state["background_color"].

        Args:
            button: The button object.
        """
        color = button.state.get("background_color")
        if color is not None:
            # Use state "0" for all states
            cmd_string = f"^BCF-{button.address},0,{color}"
            button.send_command(cmd_string)

    @register_command('bitmap','bitmap_index','bitmap_justification','bitmap_x','bitmap_y')
    def set_state_bitmap(button):
        """
        Set State Bitmap Command. Reads from button.state["bitmap"], "bitmap_index",
        "bitmap_justification", "bitmap_x", "bitmap_y".

        Args:
            button: The button object.
        """
        bitmap = button.state.get("bitmap")
        if bitmap is not None:
            index = button.state.get("bitmap_index", 1)
            just = button.state.get("bitmap_justification")

            parts = [f"^BMP-{button.address}", "0", bitmap, str(index)]

            if just is not None:
                parts.append(str(just))
                if just == 0:  # Absolute positioning
                    x = button.state.get("bitmap_x")
                    y = button.state.get("bitmap_y")
                    if x is not None and y is not None:
                        parts.append(str(x))
                        parts.append(str(y))

            cmd_string = ",".join(parts)
            button.send_command(cmd_string)


    def query_state_bitmap(button):
        """
        Query State Bitmap Command.

        Args:
            button: The button object.
        """
        cmd_string = f"?BMP-{button.address},0"
        button.send_command(cmd_string)

    @register_command('opacity')
    def set_button_opacity(button):
        """
        Button Opacity Command. Reads from button.state["opacity"].

        Args:
            button: The button object.
        """
        opacity = button.state.get("opacity")
        if opacity is not None:
            cmd_string = f"^BOP-{button.address},0,{opacity}"
            button.send_command(cmd_string)

    @register_command('video_fill')
    def set_video_fill(button):
        """
        Button State Video Fill Command. Reads from button.state["video_fill"].

        Args:
            button: The button object.
        """
        video_state = button.state.get("video_fill")
        if video_state is not None:
            cmd_string = f"^BOS-{button.address},0,{video_state}"
            button.send_command(cmd_string)


    def query_video_fill(button):
        """
        Query Button State Video Fill Command.

        Args:
            button: The button object.
        """
        cmd_string = f"?BOS-{button.address},0"
        button.send_command(cmd_string)


    def query_bitmap_justification(button):
        """
        Query Bitmap Justification Command.

        Args:
            button: The button object.
        """
        cmd_string = f"?JSB-{button.address},0"
        button.send_command(cmd_string)

    @register_command('streaming_url')
    def set_streaming_media(button):
        """
        Button State Streaming Digital Media Command. Reads from button.state["streaming_url"].

        Args:
            button: The button object.
        """
        url = button.state.get("streaming_url")
        if url is not None:
            cmd_string = f"^SDM-{button.address},0,{url}"
            button.send_command(cmd_string)

    @register_command('text')
    def set_text(button):
        """
        Set State Text Command. Reads from button.state["text"].

        Args:
            button: The button object.
        """
        text = button.state.get("text", "")
        cmd_string = f"^TXT-{button.address},0,{text}"
        button.send_command(cmd_string)


    def query_text(button):
        """
        Query State Text Command.

        Args:
            button: The button object.
        """
        cmd_string = f"?TXT-{button.address},0"
        button.send_command(cmd_string)

    #endregion

