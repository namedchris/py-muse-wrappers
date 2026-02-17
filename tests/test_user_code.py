from py_muse_wrappers.touchpad.touchpad import Touchpad

def test():
    # Create touchpad with config
    touchpad = Touchpad("AMX-10001", "tests/test_config.CSV")

    # Get a button
    button = touchpad.find_button_by_name("Cancel")
    assert button is not None
    # Track calls
    calls = []

    button.callback.set_on_click(lambda: calls.append('click'))
    button.callback.set_on_release(lambda: calls.append('release'))

    # Mock event
    class Event:
        def __init__(self, value):
            self.value = value

    # Test
    button.callback(Event(True))
    button.callback(Event(False))

    assert calls == ['click', 'release']
    print("All tests passed!")
