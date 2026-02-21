import csv
import logging
from typing import Optional, Dict, List
from py_muse_wrappers.common.device import Device, default_device_factory
from py_muse_wrappers.common.callbacks import ButtonCallback
from .button import Button
from .page import Page
from .component import Component

logger = logging.getLogger(__name__)

class Touchpad(Device):
    """
    Touchpad device wrapper with optional CSV configuration loading.

    Extends Device to add panel configuration from TPDesign CSV exports.
    """

    def __init__(self, name: str, config_file: Optional[str] = None, device_factory=default_device_factory):
        """
        Initialize touchpad with optional configuration file.

        Args:
            name: Device name for context.devices.get()
            config_file: Optional path to TPDesign CSV configuration file
            device_factory: Device factory for creating muse device
        """
        super().__init__(name, device_factory)
        config = dict()
        if config_file:
            config = self._parse_csv_config(config_file) 
        self.pages = config.get('pages')
        self.buttons = config.get('buttons')
            

    def _parse_csv_config(self, csv_path: str) -> Dict:
        """
        Parse panel configuration CSV file.

        Args:
            csv_path: Path to CSV file

        Returns:
            Dict with component objects: {'pages': [pages]. 'buttons': {buttons}
        """
        with open(csv_path, 'r') as f:
            lines = f.readlines()

        # Get panel name from first line
        panel_name = lines[0].strip().strip('"')

        # Find the function codes section
        function_section_start = None
        for i, line in enumerate(lines):
            if "Function codes utilized:" in line:
                function_section_start = i + 3  # Skip blank line and header
                break

        if function_section_start is None:
            raise ValueError("Could not find function codes section in CSV")

        # Parse CSV data starting from function codes
        reader = csv.reader(lines[function_section_start:])

        pages = []
        buttons = []
        current_page_name = None

        for row in reader:
            if not row or not any(row):  # Empty row
                break

            # Check if this is a page header (only has one column with content)
            if len(row) == 1 and row[0].strip():
                current_page_name = row[0].strip().strip('"')
                pages.append(Page(current_page_name))
                continue

            # This is a button row
            if current_page_name and len(row) >= 4:
                # Skip if button name is empty
                if not row[1].strip():
                    continue

                button_name = row[1].strip().strip('"')
                level_port = None
                level_code = None
                set_selected = lambda value: None
                set_level = lambda value: None
                send_command = None
                try:
                    # Parse channel (format: "port:code") - strip spaces
                    channel_str = row[2].strip()
                    if not channel_str:
                        continue
                    channel_parts = channel_str.split(':')
                    channel_port = int(channel_parts[0].strip())
                    channel_code = int(channel_parts[1].strip())
                    def set_selected(value):
                        self.device.port[channel_port].channel[channel_code] = value
                except Exception as e:
                    logger.error(f"Failed to define set_selected callable: {e} ")

                try:                    
                    # Parse address (format: "port:code") - strip spaces
                    address_str = row[3].strip()
                    if not address_str:
                        continue
                    address_parts = address_str.split(':')
                    address_port = int(address_parts[0].strip())
                    address_code = int(address_parts[1].strip())
                except Exception as e:
                    logger.error(f"Failed to parse button port and address: {e}")
                
                try:
                    # Parse level if present
                    if len(row) > 4 and row[4].strip():
                        level_parts = row[4].strip().split(':')
                        level_port = int(level_parts[0].strip())
                        level_code = int(level_parts[1].strip())
                    def set_level(value):
                        self.device.port[level_port].level[level_code] = value

                except Exception as e:
                    logger.error(f"Failed to define set_level callable: {e}")

                try:
                    def send_command(command):
                        self.device.port[address_port].send_command(command)
                except Exception as e:
                    logger.error(f"Failed to define button send command: {e}")

                button = Button(
                    name= button_name,
                    address_port=address_port,
                    address_code=address_code,
                    set_selected = set_selected,
                    set_level=set_level,
                    callback=self.make_button_callback(address_port, address_code),
                    send_command=send_command
                )   
                buttons.append(button)
        config = {'pages':pages,'buttons':buttons}
        return config
 
    def find_component_by_name(self, name: str) -> Optional[Component]:
        """Find first component by name."""
        cs = self.pages
        return next((c for c in cs if c.name == name),None)

    def find_components_by_name(self, name: str) -> List[Component]:
        """Find all components by name."""
        cs = self.pages+self.buttons
        return [c for c in cs if c.name == name]

    def find_page_by_name(self, name: str) -> Optional[Component]:
        """Find first component by name."""
        cs = self.pages
        return next((c for c in cs if c.name == name),None)

    def find_pages_by_name(self, name: str) -> List[Component]:
        """Find all components by name."""
        cs = self.pages
        return [c for c in cs if c.name == name]
    
    def find_button_by_name(self, name: str) -> Optional[Component]:
        """Find first component by name."""
        cs = self.buttons
        return next((c for c in cs if c.name == name),None)

    def find_buttons_by_name(self, name: str) -> List[Component]:
        """Find all components by name."""
        cs = self.buttons
        return [c for c in cs if c.name == name]