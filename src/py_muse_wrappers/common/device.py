import logging
from .callbacks import ButtonCallback

logger = logging.getLogger(__name__)


class Device:
    """
    Wrapper for MUSE device objects.

    Handles 0-based to 1-based port conversion automatically.
    """

    def __init__(self, name):
        """
        Initialize wrapper with a MUSE device.

        Args:
            name: Device name for context.devices.get()
        """
        self.device = None
        try:
            from mojo import context
            self.device = context.devices.get(name)
        except Exception as e:
            logger.warning(f"Failed to get device '{name}': {e} (running without controller?)")

    def make_button_callback(self, port: int, address: int):
        port = port - 1
        callback = ButtonCallback()
        try:
            if self.device:
                self.device.port[port].button[address].watch(callback)
        except Exception as e:
            logger.warning(f"Failed to watch button at port {port + 1}, address {address}: {e} (running without controller?)")
        return callback
