#!/bin/bash
# EppyBot Launcher Script

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Launch EppyBot
cd "$SCRIPT_DIR"
python3 eppybot.py
