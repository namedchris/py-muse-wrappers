import csv
from typing import Optional, Dict
from devices.device import Device
from devices.callbacks import ButtonCallback
from components.buttons.buttons import Button


class Touchpad(Device):
    """
    Touchpad device wrapper with optional CSV configuration loading.

    Extends Device to add panel configuration from TPDesign CSV exports.
    """

    def __init__(self, name: str, config_file: Optional[str] = None):
        """
        Initialize touchpad with optional configuration file.

        Args:
            name: Device name for context.devices.get()
            config_file: Optional path to TPDesign CSV configuration file
        """
        super().__init__(name)
        self._config = None
        self.pages = {}
        if config_file:
            self._config = self._parse_config(config_file)
            self._create_buttons()

    def _parse_config(self, csv_path: str) -> Dict:
        """
        Parse panel configuration CSV file.

        Args:
            csv_path: Path to CSV file

        Returns:
            Dict with panel config: {'name': str, 'pages': {page_name: {'name': str, 'buttons': {...}}}}
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

        pages = {}
        current_page_name = None

        for row in reader:
            if not row or not any(row):  # Empty row
                break

            # Check if this is a page header (only has one column with content)
            if len(row) == 1 and row[0].strip():
                current_page_name = row[0].strip().strip('"')
                if current_page_name not in pages:
                    pages[current_page_name] = {
                        'name': current_page_name,
                        'buttons': {}
                    }
                continue

            # This is a button row
            if current_page_name and len(row) >= 4:
                # Skip if button name is empty
                if not row[1].strip():
                    continue

                button_name = row[1].strip().strip('"')

                # Parse channel (format: "port:code") - strip spaces
                channel_str = row[2].strip()
                if not channel_str:
                    continue
                channel_parts = channel_str.split(':')
                channel_port = int(channel_parts[0].strip())
                channel_code = int(channel_parts[1].strip())

                # Parse address (format: "port:code") - strip spaces
                address_str = row[3].strip()
                if not address_str:
                    continue
                address_parts = address_str.split(':')
                address_port = int(address_parts[0].strip())
                address_code = int(address_parts[1].strip())

                # Parse level if present
                level_port = None
                level_code = None
                if len(row) > 4 and row[4].strip():
                    level_parts = row[4].strip().split(':')
                    level_port = int(level_parts[0].strip())
                    level_code = int(level_parts[1].strip())

                button_config = {
                    'name': button_name,
                    'channel_port': channel_port,
                    'channel_code': channel_code,
                    'address_port': address_port,
                    'address_code': address_code,
                    'level_port': level_port,
                    'level_code': level_code
                }

                # Use button name + codes as key to handle duplicate names
                button_key = f"{button_name}_{address_port}_{address_code}"
                pages[current_page_name]['buttons'][button_key] = button_config

        return {'name': panel_name, 'pages': pages}

    def _create_buttons(self):
        """Create Button components from parsed config."""
        if self._config is None:
            return

        for page_name, page_config in self._config['pages'].items():
            self.pages[page_name] = {}

            for button_key, button_config in page_config['buttons'].items():
                # Create ButtonCallback and register with device
                callback = self.make_button_callback(
                    button_config['address_port'],
                    button_config['address_code']
                )

                # Create send_command callback for this button's address port
                port = button_config['address_port']
                send_command = lambda cmd, p=port: self.device.port[p - 1].send_command(cmd)

                # Create Button
                button = Button(
                    name=button_config['name'],
                    port=button_config['address_port'],
                    address_code=button_config['address_code'],
                    channel=button_config['channel_code'],
                    callback=callback,
                    send_command=send_command
                )

                self.pages[page_name][button_key] = button

    def dump_config(self):
        """Print panel configuration to stdout."""
        if self._config is None:
            print("No configuration loaded")
            return

        print("=" * 80)
        print(f"Panel Name: {self._config['name']}")
        print(f"Total Pages: {len(self._config['pages'])}")
        print()

        for page_name, page_config in self._config['pages'].items():
            print("-" * 80)
            print(f"Page: {page_name}")
            print(f"  Total Buttons: {len(page_config['buttons'])}")
            print()

            for button_key, button_config in page_config['buttons'].items():
                print(f"  Button: {button_config['name']}")
                print(f"    Key: {button_key}")
                print(f"    Channel: Port {button_config['channel_port']}, Code {button_config['channel_code']}")
                print(f"    Address: Port {button_config['address_port']}, Code {button_config['address_code']}")
                if button_config['level_port'] is not None:
                    print(f"    Level: Port {button_config['level_port']}, Code {button_config['level_code']}")
                print()

        print("=" * 80)
        print(f"\nSummary:")
        print(f"  Pages: {len(self._config['pages'])}")
        total_buttons = sum(len(page['buttons']) for page in self._config['pages'].values())
        print(f"  Total Buttons: {total_buttons}")
