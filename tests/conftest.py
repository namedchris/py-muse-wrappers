import pytest

class MockButton:
    def __init__(self):
        self._callback = None

    def watch(self, callback):
        self._callback = callback

class MockButtonArray:
    def __init__(self):
        self._buttons = {}

    def __getitem__(self, address):
        if address not in self._buttons:
            self._buttons[address] = MockButton()
        return self._buttons[address]

class MockChannelArray:
    def __init__(self):
        self._channels = {}

    def __getitem__(self, code):
        return self._channels.get(code)

    def __setitem__(self, code, value):
        self._channels[code] = value

class MockLevelArray:
    def __init__(self):
        self._levels = {}

    def __getitem__(self, code):
        return self._levels.get(code)

    def __setitem__(self, code, value):
        self._levels[code] = value

class MockPort:
    def __init__(self, device, port_num):
        self.device = device
        self.port_num = port_num
        self.button = MockButtonArray()
        self.channel = MockChannelArray()
        self.level = MockLevelArray()

    def send_command(self, command):
        self.device.commands.append((self.port_num, command))

class MockPortArray:
    def __init__(self, device):
        self.device = device
        self._ports = {}

    def __getitem__(self, port_num):
        if port_num not in self._ports:
            self._ports[port_num] = MockPort(self.device, port_num)
        return self._ports[port_num]

class MockMuseDevice:
    def __init__(self):
        self.port = MockPortArray(self)
        self.commands = []

@pytest.fixture
def mock_device_factory():
    def factory(name):
        return MockMuseDevice()
    return factory
