#!/bin/bash

set -e  # stop on error

echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

echo "Installing Python 3 and pip..."
sudo apt install -y python3 python3-pip python3-venv

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
# pip install numpy matplotlib networkx <- later addition

echo "Setup complete!"
cd src
python3 main.py


