#!/bin/bash
set -e

echo "Setting up Python 3.11 environment with uv..."

# Check if Python 3.11 is available
if ! command -v python3.11 &> /dev/null; then
    echo "Python 3.11 is not installed. Please install it first."
    echo "On Ubuntu/Debian: sudo apt update && sudo apt install python3.11 python3.11-venv"
    exit 1
fi

# Check if uv is installed, install it if not
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    python3.11 -m pip install uv
fi

# Create project directories
mkdir -p google_results x_results

# Create a Python 3.11 virtual environment using uv
echo "Creating virtual environment with Python 3.11..."
uv venv --python=3.11

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install browser-use
playwright install --with-deps chromium

# Run the search script
# echo "Running search script..."
# python search_keywords.py

echo "Done!"
