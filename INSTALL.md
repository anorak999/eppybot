# EppyBot Installation Guide

## 🚀 Make EppyBot a Clickable Desktop Application

There are **three methods** to run EppyBot as a desktop application with a clickable icon:

---

## Method 1: Quick Desktop Launcher (Recommended)

### Step 1: Install to Applications Menu

```bash
# Copy the desktop file to your local applications directory
cp packaging/eppybot.desktop.template ~/.local/share/applications/eppybot.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/
```

### Step 2: Launch EppyBot

- **From Application Menu**: Search for "EppyBot" in your application launcher
- **From Desktop**: Right-click desktop → Create Launcher → Search "EppyBot"

---

## Method 2: Desktop Shortcut

### Create a shortcut on your desktop:

```bash
# Copy desktop file to Desktop
cp packaging/eppybot.desktop.template ~/Desktop/

# Make it executable
chmod +x ~/Desktop/eppybot.desktop

# Trust the launcher (if needed)
gio set ~/Desktop/eppybot.desktop metadata::trusted true
```

Now you'll have a clickable icon on your desktop!

---

## Method 3: Create Standalone Executable with PyInstaller

### Install PyInstaller:

```bash
pip3 install pyinstaller
```

### Create Executable:

```bash
cd <PROJECT_ROOT>

# Create standalone executable
pyinstaller --onefile \
    --windowed \
    --name=EppyBot \
    --icon=eppybot_icon.png \
    --add-data="eppybot_icon.png:." \
    eppybot.py
```

### Find Your Executable:

The executable will be in: `dist/EppyBot`

You can then:
- Double-click to run
- Move to `/usr/local/bin/` for system-wide access
- Create a desktop shortcut pointing to it

---

## Method 4: System-Wide Installation (Advanced)

### Install for all users:

```bash
# Copy desktop file to system applications
sudo cp packaging/eppybot.desktop.template /usr/share/applications/

# Copy icon to system icons
sudo cp eppybot_icon.png /usr/share/pixmaps/

# Update desktop database
sudo update-desktop-database
```

---

## 📋 Quick Start Commands

### Option A: Application Menu (Easiest)
```bash
cp packaging/eppybot.desktop.template ~/.local/share/applications/eppybot.desktop
update-desktop-database ~/.local/share/applications/
```
Then search for "EppyBot" in your app launcher!

### Option B: Desktop Icon
```bash
cp packaging/eppybot.desktop.template ~/Desktop/
chmod +x ~/Desktop/eppybot.desktop
```
Double-click the icon on your desktop!

### Option C: Run from Terminal
```bash
cd <PROJECT_ROOT>
./eppybot.sh
```

---

## 🎨 Icon Information

- **Icon File**: `eppybot_icon.png`
- **Design**: Modern black & white camera/enhancement symbol
- **Format**: PNG with transparency
- **Location**: `eppybot_icon.png`

---

## 🔧 Troubleshooting

### Icon doesn't show up?
```bash
# Refresh icon cache
gtk-update-icon-cache ~/.local/share/icons/ -f
```

### Desktop file not trusted?
```bash
chmod +x ~/Desktop/eppybot.desktop
gio set ~/Desktop/eppybot.desktop metadata::trusted true
```

### Permission denied?
```bash
chmod +x packaging/eppybot.sh
chmod +x packaging/eppybot.desktop.template
```

---

## 📦 Files Created

- `eppybot.py` - Main application
- `eppybot.desktop` - Desktop entry file
- `eppybot.sh` - Launch script
- `eppybot_icon.png` - Application icon
- `INSTALL.md` - This file

---

## 🎯 Recommended: Method 1 (Application Menu)

For the best experience, use **Method 1** to add EppyBot to your application menu. This integrates it properly with your desktop environment and makes it accessible from your app launcher.

```bash
# One command to install:
cp packaging/eppybot.desktop.template ~/.local/share/applications/eppybot.desktop && update-desktop-database ~/.local/share/applications/
```

Then just search for "EppyBot" in your application launcher! 🚀
