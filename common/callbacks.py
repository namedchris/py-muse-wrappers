class ButtonCallback():
    """Button-specific callback with on_click and on_release handlers."""

    def __init__(self):
        """Initialize to noops to avoid checks later."""
        self._on_click = lambda: None
        self._on_release = lambda: None

    def set_on_click(self, handler):
        """Set the on_click handler."""
        self._on_click = handler
        return self

    def get_on_click(self):
        """Get the on_click handler."""
        return self._on_click

    def pop_on_click(self):
        """Remove and return the on_click handler."""
        handler = self._on_click
        self._on_click = lambda: None
        return handler

    def set_on_release(self, handler):
        """Set the on_release handler."""
        self._on_release = handler
        return self

    def get_on_release(self):
        """Get the on_release handler."""
        return self._on_release

    def pop_on_release(self):
        """Remove and return the on_release handler."""
        handler = self._on_release
        self._on_release = lambda: None
        return handler

    def __call__(self, event):
        if event.value:
            self._on_click()
        else:
            self._on_release()
