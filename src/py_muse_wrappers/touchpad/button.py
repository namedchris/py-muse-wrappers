from typing import Callable, Optional
from .component import Component
from py_muse_wrappers.common.callbacks import ButtonCallback

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


    def __init__(self, callback: ButtonCallback, name: str, address_port: int, address_code: int, set_selected: Callable, set_level: Callable, send_command: Optional[Callable[[str], None]] = None):
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

        # Call parent init
        super().__init__(name)

        # Set core attributes
        self.name = name
        self.address_port = address_port
        self.address = address_code
        self.set_selected = set_selected # underlying channel reference
        self.callback = callback
        self.send_command = send_command
        self.set_level =self.make_level_setter(set_level)    # Wrap set_level with clamping logic

        # Set state attributes with defaults 
        self.is_selected = False
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
        self.level = 0
        self.streaming_url = None
        self.subpage_padding = None

        # Clear dirty flags after initialization (defaults shouldn't be dirty)
        # Build instance-level command map after attribute initialization to avoid sending default values as commands
        self.command_map = {
            'text': self.set_text,
            'visible': self.set_button_visible,
            'enabled': self.set_button_enabled,
            'focused': self.set_button_focus,
            'background_color': self.set_background_color,
            'opacity': self.set_button_opacity,
            'bitmap': self.set_state_bitmap,
            'bitmap_index': self.set_state_bitmap,
            'bitmap_justification': self.set_state_bitmap,
            'bitmap_x': self.set_state_bitmap,
            'bitmap_y': self.set_state_bitmap,
            'video_fill': self.set_video_fill,
            'bargraph_high': self.set_bargraph_high,
            'bargraph_low': self.set_bargraph_low,
            'level': self.set_level,
            'streaming_url': self.set_streaming_media,
            'subpage_padding': self.set_subpage_padding,
            'is_selected': lambda: self.set_selected(self.is_selected)
        }

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
        if hasattr(self, 'command_map') and name in self.command_map:
            self.command_map[name]()  

    # adds clamping to set_level
    def make_level_setter(self,set_level):
        """
        Clamp level to bargraph range if both are set.
        """
        def func():
            if self.bargraph_low is None or self.bargraph_high is None:
                raise ValueError("Cannot set level when bargraph range is undefined. Set bargraph_low and bargraph_high before setting level.") 
            if self.level is None:
                raise ValueError("Level is not defined. Cannot set level without a value.")
            clamped_level = max(self.bargraph_low, min(self.bargraph_high, self.level))
            if clamped_level != self.level:
                print(f"Clamping level from {self.level} to {clamped_level}")
                self.level = clamped_level  # Update level to clamped value, __setattr__ will try again with clamped value
            else: 
                set_level(self.level)

        return func


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

    def set_button_focus(self):
        """
        Button Focus Command.
        """
        value = 1 if self.focused else 0
        cmd_string = f"^BSF-{self.address},{value}"
        self.send_command(cmd_string)

    def submit_button_text(self):
        """
        Button Submit Text Command.
        Causes button text area to send its text as a string to the NetLinx Master.
        """
        cmd_string = f"^BSM-{self.address}"
        self.send_command(cmd_string)


    def clear_page_flip(self):
        """
        Clear Page Flip Command.
        Clear all page flips from button release event action.
        """
        cmd_string = f"^CPF-{self.address}"
        self.send_command(cmd_string)

    def set_bargraph_high(self):
        """
        Set Bargraph High Range Command.
        """
        if self.bargraph_low is not None:
            if self.bargraph_high <= self.bargraph_low:     
                raise ValueError(f"bargraph_high ({self.bargraph_high}) must be greater than bargraph_low ({self.bargraph_low})")

        print(f"Setting bargraph high: {self.bargraph_high} for button {self.name} at address {self.address}")
        cmd_string = f"^GLH-{self.address},{self.bargraph_high}"
        self.send_command(cmd_string)

    def set_bargraph_low(self):
        """
        Set Bargraph Low Range Command.
        """
        if self.bargraph_high is not None:
            if self.bargraph_low >= self.bargraph_high:
                raise ValueError(f"bargraph_low ({self.bargraph_low}) must be less than bargraph_high ({self.bargraph_high})")           
        print(f"Setting bargraph low: {self.bargraph_low} for button {self.name} at address {self.address}")
        cmd_string = f"^GLL-{self.address},{self.bargraph_low}"
        self.send_command(cmd_string)


    def set_button_enabled(self):
        """
        Button Enable Command.
        """
        value = 1 if self.enabled else 0
        cmd_string = f"^ENA-{self.address},{value}"
        self.send_command(cmd_string)


    def subpage_hide_all(self):
        """
        Subpage Hide All Command.
        Hide all subpages in a subpage viewer button.
        """
        cmd_string = f"^SHA-{self.address}"
        self.send_command(cmd_string)

    def set_button_visible(self):
        value = 1 if self.visible else 0
        cmd_string = f"^SHO-{self.address},{value}"
        self.send_command(cmd_string)

    def set_subpage_padding(self):
        if self.subpage_padding is not None:
            cmd_string = f"^SPD-{self.address},{self.subpage_padding}"
            self.send_command(cmd_string)


    # ============================================================================
    # Button State (from button_state_txt)
    # ============================================================================
    def set_background_color(self):
        """
        Background Color Fill Command.
        """
        if self.background_color is not None:
            # Use state "0" for all states
            cmd_string = f"^BCF-{self.address},0,{self.background_color}"
            self.send_command(cmd_string)

    def set_state_bitmap(self):
        """
        Set State Bitmap Command.
        """
        if self.bitmap is not None:
            index = self.bitmap_index
            just = self.bitmap_justification

            parts = [f"^BMP-{self.address}", "0", self.bitmap, str(index)]

            if just is not None:
                parts.append(str(just))
                if just == 0:  # Absolute positioning
                    x = self.bitmap_x
                    y = self.bitmap_y
                    if x is not None and y is not None:
                        parts.append(str(x))
                        parts.append(str(y))

            cmd_string = ",".join(parts)
            self.send_command(cmd_string)


    def query_state_bitmap(self):
        """
        Query State Bitmap Command.
        """
        cmd_string = f"?BMP-{self.address},0"
        self.send_command(cmd_string)

    def set_button_opacity(self):
        """
        Button Opacity Command.
        """
        if self.opacity is not None:
            cmd_string = f"^BOP-{self.address},0,{self.opacity}"
            self.send_command(cmd_string)

    def set_video_fill(self):
        """
        Button State Video Fill Command.
        """
        if self.video_fill is not None:
            cmd_string = f"^BOS-{self.address},0,{self.video_fill}"
            self.send_command(cmd_string)


    def query_video_fill(self):
        """
        Query Button State Video Fill Command.
        """
        cmd_string = f"?BOS-{self.address},0"
        self.send_command(cmd_string)


    def query_bitmap_justification(self):
        """
        Query Bitmap Justification Command.
        """
        cmd_string = f"?JSB-{self.address},0"
        self.send_command(cmd_string)

    def set_streaming_media(self):
        """
        Button State Streaming Digital Media Command.
        """
        if self.streaming_url is not None:
            cmd_string = f"^SDM-{self.address},0,{self.streaming_url}"
            self.send_command(cmd_string)

    def set_text(self):
        """
        Set State Text Command.
        """
        cmd_string = f"^TXT-{self.address},0,{self.text}"
        self.send_command(cmd_string)


    def query_text(self):
        """
        Query State Text Command.
        """
        cmd_string = f"?TXT-{self.address},0"
        self.send_command(cmd_string)

    #endregion

