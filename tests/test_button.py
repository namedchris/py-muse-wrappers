import pytest
from py_muse_wrappers.touchpad.touchpad import Touchpad


def test_level_setter_missing_bargraph_high(mock_device_factory):
    """Test that ValueError is raised when bargraph_high is not set."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    
    button.bargraph_low = 0
    
    with pytest.raises(ValueError, match="Cannot set level when bargraph range is undefined"):
        button.level = 50


def test_level_setter_missing_bargraph_low(mock_device_factory):
    """Test that ValueError is raised when bargraph_low is not set."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    
    button.bargraph_high = 100
    
    with pytest.raises(ValueError, match="Cannot set level when bargraph range is undefined"):
        button.level = 50


def test_level_setter_level_is_none(mock_device_factory):
    """Test that ValueError is raised when level is None."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    
    button.bargraph_low = 0
    button.bargraph_high = 100
    
    with pytest.raises(ValueError, match="Level is not defined"):
        button.level = None


def test_level_clamps_above_high(mock_device_factory, capsys):
    """Test that level is clamped when it exceeds bargraph_high."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    
    button.bargraph_low = 0
    button.bargraph_high = 100
    button.level = 150  
  
    assert button.level == 100


def test_level_clamps_below_low(mock_device_factory, capsys):
    """Test that level is clamped when it is below bargraph_low."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    
    button.bargraph_low = 50
    button.bargraph_high = 100
    button.level = 25
    
    assert button.level == 50

def test_level_within_range(mock_device_factory, capsys):
    """Test that level is not clamped when it's within range."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    
    button.bargraph_low = 0
    button.bargraph_high = 100
    button.level = 50
    
    assert button.level == 50


# Tests for button command methods


def test_set_text(mock_device_factory):
    """Test set_text command."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.text = "Hello World"
    
    assert any("^TXT-13,0,Hello World" in cmd for port, cmd in muse_device.commands)


def test_set_button_visible_true(mock_device_factory):
    """Test set_button_visible with visible=True."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.visible = True
    
    assert any("^SHO-13,1" in cmd for port, cmd in muse_device.commands)


def test_set_button_visible_false(mock_device_factory):
    """Test set_button_visible with visible=False."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.visible = False
    
    assert any("^SHO-13,0" in cmd for port, cmd in muse_device.commands)


def test_set_button_enabled_true(mock_device_factory):
    """Test set_button_enabled with enabled=True."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.enabled = True
    
    assert any("^ENA-13,1" in cmd for port, cmd in muse_device.commands)


def test_set_button_enabled_false(mock_device_factory):
    """Test set_button_enabled with enabled=False."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.enabled = False
    
    assert any("^ENA-13,0" in cmd for port, cmd in muse_device.commands)


def test_set_button_focus_true(mock_device_factory):
    """Test set_button_focus with focused=True."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.focused = True
    
    assert any("^BSF-13,1" in cmd for port, cmd in muse_device.commands)


def test_set_button_focus_false(mock_device_factory):
    """Test set_button_focus with focused=False."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.focused = False
    
    assert any("^BSF-13,0" in cmd for port, cmd in muse_device.commands)


def test_set_background_color(mock_device_factory):
    """Test set_background_color command."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.background_color = 65535
    
    assert any("^BCF-13,0,65535" in cmd for port, cmd in muse_device.commands)


def test_background_color_none_sends_nothing(mock_device_factory):
    """Test that background_color=None doesn't send a command."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.background_color = None
    
    assert not any("^BCF-" in cmd for port, cmd in muse_device.commands)


def test_set_button_opacity(mock_device_factory):
    """Test set_button_opacity command."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.opacity = 200
    
    assert any("^BOP-13,0,200" in cmd for port, cmd in muse_device.commands)


def test_opacity_none_sends_nothing(mock_device_factory):
    """Test that opacity=None doesn't send a command."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.opacity = None
    
    assert not any("^BOP-" in cmd for port, cmd in muse_device.commands)


def test_set_video_fill(mock_device_factory):
    """Test set_video_fill command."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.video_fill = "video.mp4"
    
    assert any("^BOS-13,0,video.mp4" in cmd for port, cmd in muse_device.commands)


def test_set_streaming_media(mock_device_factory):
    """Test set_streaming_media command."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.streaming_url = "http://example.com/stream"
    
    assert any("^SDM-13,0,http://example.com/stream" in cmd for port, cmd in muse_device.commands)


def test_set_subpage_padding(mock_device_factory):
    """Test set_subpage_padding command."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.subpage_padding = 10
    
    assert any("^SPD-13,10" in cmd for port, cmd in muse_device.commands)


def test_subpage_padding_none_sends_nothing(mock_device_factory):
    """Test that subpage_padding=None doesn't send a command."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.subpage_padding = None
    
    assert not any("^SPD-" in cmd for port, cmd in muse_device.commands)


def test_set_bitmap_with_index_only(mock_device_factory):
    """Test set_state_bitmap with bitmap and index."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.bitmap = "image.png"
    button.bitmap_index = 2
    
    assert any("^BMP-13,0,image.png,2" in cmd for port, cmd in muse_device.commands)


def test_set_bitmap_with_justification_scale(mock_device_factory):
    """Test set_state_bitmap with scale justification."""
    from py_muse_wrappers.touchpad.button import JUSTIFICATION_SCALE
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.bitmap = "image.png"
    button.bitmap_index = 1
    button.bitmap_justification = JUSTIFICATION_SCALE
    
    assert any("^BMP-13,0,image.png,1,10" in cmd for port, cmd in muse_device.commands)


def test_set_bitmap_with_justification_absolute(mock_device_factory):
    """Test set_state_bitmap with absolute justification and coordinates."""
    from py_muse_wrappers.touchpad.button import JUSTIFICATION_ABSOLUTE
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.bitmap = "image.png"
    button.bitmap_index = 1
    button.bitmap_justification = JUSTIFICATION_ABSOLUTE
    button.bitmap_x = 50
    button.bitmap_y = 75
    
    assert any("^BMP-13,0,image.png,1,0,50,75" in cmd for port, cmd in muse_device.commands)


def test_set_bitmap_with_justification_top_left(mock_device_factory):
    """Test set_state_bitmap with top-left justification."""
    from py_muse_wrappers.touchpad.button import JUSTIFICATION_TOP_LEFT
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.bitmap = "image.png"
    button.bitmap_index = 1
    button.bitmap_justification = JUSTIFICATION_TOP_LEFT
    
    assert any("^BMP-13,0,image.png,1,1" in cmd for port, cmd in muse_device.commands)


def test_bitmap_none_sends_nothing(mock_device_factory):
    """Test that bitmap=None doesn't send a command."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.bitmap = None
    
    assert not any("^BMP-" in cmd for port, cmd in muse_device.commands)


def test_set_bargraph_high_valid(mock_device_factory, capsys):
    """Test set_bargraph_high with valid range."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.bargraph_low = 0
    button.bargraph_high = 100
    
    assert any("^GLH-13,100" in cmd for port, cmd in muse_device.commands)
    captured = capsys.readouterr()
    assert "Setting bargraph high: 100" in captured.out


def test_set_bargraph_high_invalid_range(mock_device_factory):
    """Test set_bargraph_high raises error when high <= low."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    
    button.bargraph_low = 100
    
    with pytest.raises(ValueError, match="bargraph_high.*must be greater than bargraph_low"):
        button.bargraph_high = 100


def test_set_bargraph_low_valid(mock_device_factory, capsys):
    """Test set_bargraph_low with valid range."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    muse_device = touchpad.device
    
    muse_device.commands.clear()
    button.bargraph_high = 100
    button.bargraph_low = 0
    
    assert any("^GLL-13,0" in cmd for port, cmd in muse_device.commands)
    captured = capsys.readouterr()
    assert "Setting bargraph low: 0" in captured.out


def test_set_bargraph_low_invalid_range(mock_device_factory):
    """Test set_bargraph_low raises error when low >= high."""
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV", mock_device_factory)
    button = touchpad.find_button_by_name("Cancel")
    
    button.bargraph_high = 100
    
    with pytest.raises(ValueError, match="bargraph_low.*must be less than bargraph_high"):
        button.bargraph_low = 100
