#!/bin/bash
# Hindi to Hinglish Converter Launcher for Unix/Linux/Mac

echo "Hindi to Hinglish Converter"
echo "============================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Installing dependencies..."
    venv/bin/pip install -r requirements.txt
fi

# Run the application
if [ $# -eq 0 ]; then
    echo "Launching GUI..."
    venv/bin/python main.py
else
    echo "Running with arguments: $@"
    venv/bin/python main.py "$@"
fi
