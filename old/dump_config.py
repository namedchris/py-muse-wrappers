#!/usr/bin/env python3
"""
Script to read panel CSV configuration and dump the parsed objects to stdout.
"""
import sys
from panel import parse_panel_csv


def dump_config(csv_path: str):
    """Parse CSV and print all config objects"""

    print(f"Parsing: {csv_path}")
    print("=" * 80)

    config = parse_panel_csv(csv_path)

    print(f"\nPanel Name: {config.name}")
    print(f"Total Pages: {len(config.pages)}")
    print()

    for page_name, page_config in config.pages.items():
        print("-" * 80)
        print(f"Page: {page_name}")
        print(f"  Total Buttons: {len(page_config.buttons)}")
        print()

        for button_key, button_config in page_config.buttons.items():
            print(f"  Button: {button_config.name}")
            print(f"    Key: {button_key}")
            print(f"    Channel: Port {button_config.channel_port}, Code {button_config.channel_code}")
            print(f"    Address: Port {button_config.address_port}, Code {button_config.address_code}")
            if button_config.level_port is not None:
                print(f"    Level: Port {button_config.level_port}, Code {button_config.level_code}")
            print()

    print("=" * 80)
    print(f"\nSummary:")
    print(f"  Pages: {len(config.pages)}")
    total_buttons = sum(len(page.buttons) for page in config.pages.values())
    print(f"  Total Buttons: {total_buttons}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dump_config.py <csv_file>")
        print("Example: python dump_config.py EOC-202.CSV")
        sys.exit(1)

    csv_file = sys.argv[1]
    dump_config(csv_file)
