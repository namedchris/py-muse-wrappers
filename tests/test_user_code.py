from devices.touchpad import Touchpad

def test():
    # Create touchpad with config
    touchpad = Touchpad("AMX-10001", "tests/EOC-202.CSV")

    # Get a button
    first_page = list(touchpad.pages.keys())[0]
    first_button_key = list(touchpad.pages[first_page].keys())[0]
    button = touchpad.pages[first_page][first_button_key]

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
