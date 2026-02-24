#!/bin/bash
# Backend Setup Script for macOS/Linux
# This shell script runs the Python setup script

echo ""
echo "===================================================================="
echo "  Backend Setup for macOS/Linux"
echo "===================================================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  - macOS: brew install python3"
    echo "  - Ubuntu/Debian: sudo apt-get install python3"
    echo "  - Fedora: sudo dnf install python3"
    echo ""
    exit 1
fi

# Display Python version
echo "Python version:"
python3 --version
echo ""

echo "Running setup script..."
echo ""

# Run the Python setup script
python3 setup_backend.py

# Check if setup was successful
if [ $? -ne 0 ]; then
    echo ""
    echo "Setup encountered errors. Please review the output above."
    echo ""
    exit 1
fi

echo ""
echo "Setup complete!"
echo ""
