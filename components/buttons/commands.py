"""
Moved from Buttons class. To move it back replace button ref with self

Button command functions for G5 panels.

All functions take ONLY a Button object and read parameters from button.state or button attributes.
"""


# ============================================================================
# Button Commands (from button_commands.txt)
# ============================================================================

def query_subpage_events(button):
    """
    Query assigned subpage custom event numbers for subpage viewer button.

    Args:
        button: The button object.
    """
    cmd_string = f"?SCE-{button.address}"
    button.send_command(cmd_string)


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


def set_button_visible(button):
    """
    Button Show/Hide Command. Reads from button.state["visible"].

    Args:
        button: The button object.
    """
    value = 1 if button.state.get("visible", True) else 0
    cmd_string = f"^SHO-{button.address},{value}"
    button.send_command(cmd_string)


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
# Button State Commands (from button_state_commands.txt)
# ============================================================================

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
