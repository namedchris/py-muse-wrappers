"""
Example showing how Panel, Page, Button would inherit from Component.
"""
from component import Component
from typing import Any


class Button(Component):
    """Button component - leaf node in hierarchy"""

    def __init__(self, name: str, port: int, address: int, channel: int, send_command_callback):
        super().__init__(name)
        self.port = port
        self.address = address
        self.channel = channel
        self._send_command = send_command_callback

        # Initialize state
        self.state = {
            "text": "",
            "visible": True,
            "enabled": True,
            "is_on": False,
            "background_color": None,
            "opacity": None
        }

    def render(self):
        """Render button state to touchpad"""
        # Send commands based on current state
        if self.state.get("text"):
            self._send_command(f"^TXT-{self.address},0,{self.state['text']}")

        self._send_command(f"^SHO-{self.address},{1 if self.state['visible'] else 0}")
        self._send_command(f"^ENA-{self.address},{1 if self.state['enabled'] else 0}")

        if self.state.get("background_color"):
            self._send_command(f"^BCF-{self.address},0,{self.state['background_color']}")


class Page(Component):
    """Page component - contains buttons"""

    def __init__(self, name: str, panel: Any):
        super().__init__(name)
        self.panel = panel

        # Initialize state
        self.state = {
            "active": False
        }

    def add_button(self, button: Button):
        """Add a button to this page"""
        self.add_subcomponent(button)

    def get_button(self, name: str) -> Button:
        """Get button by name (searches list)"""
        for button in self.subcomponents:
            if button.name == name:
                return button
        return None

    def render(self):
        """Render page state (page-level rendering if needed)"""
        # Page-level rendering logic here (if any)
        pass
        # Subcomponent rendering happens in render_all()


class Panel(Component):
    """Panel component - top level, contains pages"""

    def __init__(self, name: str, device: Any):
        super().__init__(name)
        self._device = device

        # Initialize state
        self.state = {
            "current_page": None
        }

    def send_command(self, port: int, cmd: str):
        """Send command to device"""
        self._device.port[port - 1].send_command(cmd)

    def add_page(self, page: Page):
        """Add a page to this panel"""
        self.add_subcomponent(page)

    def get_page(self, name: str) -> Page:
        """Get page by name (searches list)"""
        for page in self.subcomponents:
            if page.name == name:
                return page
        return None

    def render(self):
        """Render panel state (panel-level rendering if needed)"""
        # Panel-level rendering logic here (if any)
        pass
        # Subcomponent rendering happens in render_all()


# === Usage Example ===

# Create hierarchy
# panel = Panel("EOC-202", touchpad_device)
# page = Page("Tiled Mode", panel)
# button = Button("Display One", port=1, address=1, channel=1, send_command_callback=lambda cmd: panel.send_command(1, cmd))

# Build hierarchy (list-based)
# page.add_button(button)
# panel.add_page(page)

# Access by name (searches list)
# button = page.get_button("Display One")

# Or iterate over subcomponents
# for page in panel.subcomponents:
#     print(f"Page: {page.name}")
#     for button in page.subcomponents:
#         print(f"  Button: {button.name}")

# Update state using attribute access (preferred for actual Button class)
# button.text = "Display 1"
# button.background_color = "Blue"

# Or direct dict access (also works)
# button.state["text"] = "Display 1"
# button.state["background_color"] = "Blue"

# Render everything
# panel.render_all()

# Save state (exports entire hierarchy as list structure)
# panel.save_state("panel_state.json")

# Load state (matches subcomponents by index)
# panel.load_state("panel_state.json")
# panel.render_all()  # Sync with loaded state
