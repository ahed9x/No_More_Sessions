![Apache License 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
# Automation Tool
keep sessions opened, no more session ending!!!
## Overview
This Automation Tool is a Tkinter-based GUI application designed to automate mouse clicking on specific screen areas. It allows users to select or take screenshots of target images and set parameters for the automation process. The tool uses `pyautogui` for GUI automation, `PIL` for image handling, and `pynput` for mouse event listening.


## Features
- **Image Selection**: Select or capture screenshots of target images for automation.
- **Wait and Run Time Settings**: Set the wait time before starting automation and the total run time.
- **Automated Clicking**: Automates clicking on specified images if found on the screen.
- **Responsive GUI**: Runs automation in a separate thread to keep the GUI responsive.

## Requirements
- Python 3.x
- `tkinter`
- `pyautogui`
- `Pillow`
- `pynput`

## Installation
1. Install Python 3.x from the [official website](https://www.python.org/).
2. Install the required libraries using pip:
   ```bash
   pip install pyautogui Pillow pynput
