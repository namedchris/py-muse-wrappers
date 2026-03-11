import logging
from .callbacks import ButtonCallback
from typing import Callable
logger = logging.getLogger(__name__)

def default_device_factory(name: str):
        device = None
        try:
            from mojo import context
            return context.devices.get(name)
        except Exception as e:
            logger.error(f"Failed to get device '{name}': {e} \nHint: \n\t Running tests without controller? Provide an appropriate device factory fixture.")
            raise e

class Device:
    """
    Wrapper for MUSE device objects.

    Handles 0-based to 1-based port conversion automatically.
    """

    def __init__(self, name: str, device_factory: Callable = default_device_factory):
        """
        Initialize wrapper with a MUSE device.

        Args:
            name: Device name for context.devices.get()
        """
        self.device = device_factory(name)

    def make_button_callback(self, port: int, address: int):
        callback = ButtonCallback()
        self.device.port[port].button[address].watch(callback)
        return callback
