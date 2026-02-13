# MUSE Panel Wrapper

Python wrapper library for AMX MUSE G5 touchpad panels. Simplifies touchpad control with automatic state management and a clean component-based API.

## What It Does

This library provides a Pythonic interface for authoring projects for the AMX Muse platform.

## Key Features

- **CSV Configuration Loading** - Import a programmer's report from TPdesign for automatic Touchpad setup.
- **Standardized indexing** - Everything is one-indexed. No more off-by-one errors!
- **Searchable components** - Avoid indexes all together! Just call find_by_name!
- **Testable user code** - Logic and configuration is completely seperated from the Muse framework. You can finally test your project without specialized hardware!
- **Wraps G5 api** -No more combing through documation to find the proper command strings. If you eant to change a background color, just update the attribute on the button object and call render(). Python takes care of the rest. 

## Installation

Clone this repository into your MUSE project directory:

```bash
git clone <repo-url> py-muse-wrappers
```

## Basic Usage

```python
from devices.touchpad import Touchpad

# Load touchpad with configuration
touchpad = Touchpad("AMX-10001", "programmers_report.csv")

# Access a button
button = touchpad.find_by_name("power")

# Update button properties
button.text = "Power"
button.visible = True
button.enabled = True

# Changes are sent to device on render
button.render()

# Set event handlers
button.callback.set_on_click(lambda: print("Button clicked!"))
button.callback.set_on_release(lambda: print("Button released!"))
```


## Testing

```bash
pytest
```

## License

LGPL v3 - See [LICENSE](LICENSE) file for details.

This library is licensed under the GNU Lesser General Public License v3.0. You can freely use this library in your proprietary AMX control projects. If you modify the library itself and distribute it, those modifications must remain open source under LGPL v3.

