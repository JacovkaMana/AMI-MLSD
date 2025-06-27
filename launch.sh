#!/bin/bash

# Exit on any error
set -e

# Define variables
PORT=7860
VENV_DIR="venv"
PYTHON_VERSION="python3"
PIP_VERSION="pip3"
APP_FILE="ui.py"

# Check if Python is installed
if ! command -v $PYTHON_VERSION &> /dev/null; then
    echo "Error: Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v $PIP_VERSION &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

# Create and activate virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    $PYTHON_VERSION -m venv $VENV_DIR
fi
source $VENV_DIR/bin/activate


# Check if app file exists
if [ ! -f "$APP_FILE" ]; then
    echo "Error: $APP_FILE not found in the current directory."
    exit 1
fi

# Launch Gradio app
echo "Launching Gradio app on port $PORT with public sharing..."
$PYTHON_VERSION $APP_FILE --port $PORT --share

# Deactivate virtual environment on exit
deactivate