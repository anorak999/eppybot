# EppyBot - Professional Image Enhancement Suite

## Overview

EppyBot is a sleek, modern desktop application designed for enhancing images to ultra-high-quality 4K UHD resolution. It incorporates advanced AI-inspired processing techniques and provides professional-grade controls to help you achieve stunning visual results. With its intuitive black and white user interface, EppyBot offers both convenient presets and fine-grained manual adjustments for brightness, contrast, saturation, and sharpening. It also supports batch processing for enhancing multiple images at once.

## Features

-   **AI-Inspired Enhancement:** Utilizes advanced algorithms for superior image quality.
-   **4K UHD Upscaling:** Upscale images to impressive 4K Ultra High Definition.
-   **Modern UI:** Intuitive and professional black and white interface.
-   **Enhancement Presets:** Quickly apply "Natural," "Vivid," "Portrait," "Landscape," or "Professional" enhancement profiles.
-   **Manual Controls:** Fine-tune upscale factor, sharpening strength, contrast, color saturation, and brightness.
-   **Batch Processing:** Enhance multiple images simultaneously.
-   **Output Formats:** Save enhanced images as PNG (lossless) or JPG (optimized).
-   **Real-time Comparison:** View original and enhanced images side-by-side.

## Installation and Usage (Standalone Executable)

This section guides you on how to download and run the pre-built standalone executable of EppyBot on Linux.

### Download

The standalone executable for EppyBot can be found in the `dist` directory after a successful build.

### Running the Application

1.  **Navigate to the `dist` directory:**
    ```bash
    cd /home/anorak/Works/eppybot/dist
    ```
2.  **Run the EppyBot executable:**
    ```bash
    ./EppyBot
    ```
    *(Note: You might need to give execute permissions first: `chmod +x EppyBot`)*

### Creating a Desktop Shortcut (Optional, for Linux)

To create a convenient desktop shortcut, you can use the provided `.desktop` file.

1.  **Copy the `.desktop` file:**
    ```bash
    cp /home/anorak/Works/eppybot/eppybot.desktop ~/.local/share/applications/
    ```
2.  **Edit the `.desktop` file:** Open the copied file with a text editor (e.g., `gedit ~/.local/share/applications/eppybot.desktop`) and ensure the `Exec` and `Icon` paths point to the correct locations of your executable and icon file.

    Example `eppybot.desktop` content:
    ```ini
    [Desktop Entry]
    Name=EppyBot
    Comment=Professional Image Enhancement Suite
    Exec=/home/anorak/Works/eppybot/dist/EppyBot
    Icon=/home/anorak/Works/eppybot/eppybot_icon.png
    Terminal=false
    Type=Application
    Categories=Graphics;
    ```
    *Make sure to replace `/home/anorak/Works/eppybot/dist/EppyBot` with the actual path to your executable and `/home/anorak/Works/eppybot/eppybot_icon.png` with the actual path to the icon if they are different.*

3.  **Make it executable:**
    ```bash
    chmod +x ~/.local/share/applications/eppybot.desktop
    ```
    The EppyBot application should now appear in your application menu.

## Usage Guide

1.  **Launch EppyBot:** Run the standalone executable or click on your desktop shortcut.
2.  **Upload Image(s):**
    *   Click "SELECT IMAGE" to choose a single image.
    *   Check "Batch Mode (Multiple Files)" and then click "SELECT IMAGE" to choose multiple images for batch processing.
3.  **Choose Enhancement Settings:**
    *   Select one of the pre-defined "ENHANCEMENT PRESETS" (Natural, Vivid, Portrait, Landscape, Professional) for quick results.
    *   Alternatively, adjust the "MANUAL CONTROLS" sliders for Upscale Factor, Sharpen, Contrast, Saturation, and Brightness to fine-tune the enhancement to your liking.
4.  **Select Output Format:** Choose between PNG (lossless, higher quality, larger file size) or JPG (optimized, smaller file size).
5.  **Enhance:** Click "ENHANCE IMAGE" to start the processing. For batch mode, you will be prompted to select an output directory.
6.  **Save/Export:** Once enhancement is complete, click "SAVE / EXPORT" to save your enhanced image(s) to your desired location.

## Building from Source (For Developers)

If you wish to run EppyBot from its Python source code or modify it, follow these steps.

### Prerequisites

-   Python 3.x
-   `pip` (Python package installer)

### Setup

1.  **Clone the repository (or navigate to the project directory):**
    ```bash
    cd /home/anorak/Works/eppybot
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Note: If `requirements.txt` does not exist, you can create one with `pip freeze > requirements.txt` or manually list the dependencies: `pip install Pillow`)

### Running from Source

```bash
python eppybot.py
```

### Building a Standalone Executable (For Developers)

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd /home/anorak/Works/eppybot
    ```
3.  **Clean previous builds (optional but recommended):**
    ```bash
    rm -rf build dist
    ```
4.  **Build using the provided spec file:**
    ```bash
    pyinstaller --noconfirm EppyBot.spec
    ```
    The executable will be generated in the `dist` directory.

## Troubleshooting

-   **"command not found" for `pyinstaller`:** If `pyinstaller` is installed but not found, it might be in `~/.local/bin`. Ensure this directory is in your system's PATH, or use the full path to the executable: `~/.local/bin/pyinstaller`.
-   **Application icon not showing on Linux executable:** This is a PyInstaller limitation on Linux. The icon is bundled but needs to be explicitly set via a `.desktop` file for proper display in application menus.
-   **Image loading/saving errors:** Ensure you have the necessary permissions for the directories you are trying to access.

---

**EppyBot** - *Enhance your vision.*