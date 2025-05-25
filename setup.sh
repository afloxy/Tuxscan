#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting TuxScan Setup and Installation...${NC}"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}pip3 is not installed. Please install pip3 first.${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies directly
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install colorama==0.4.6 jinja2==3.1.2 pyinstaller==6.3.0

# Create dist directory if it doesn't exist
if [ ! -d "dist" ]; then
    echo -e "${YELLOW}Creating dist directory...${NC}"
    mkdir dist
fi

# Build the binary
echo -e "${YELLOW}Building binary...${NC}"
pyinstaller --onefile --name tuxscan tuxscan/__main__.py

# Create global installation directory if it doesn't exist
echo -e "${YELLOW}Installing binary globally...${NC}"
sudo mkdir -p /usr/local/bin

# Copy binary to global location
sudo cp dist/tuxscan /usr/local/bin/
sudo chmod +x /usr/local/bin/tuxscan

# Clean up build files
echo -e "${YELLOW}Cleaning up build files...${NC}"
rm -rf build/
rm -rf tuxscan.egg-info/
rm -rf __pycache__/
rm -rf venv/
rm -f setup.py  # Remove setup.py as it's no longer needed

echo -e "${GREEN}Setup and Installation completed successfully!${NC}"
echo -e "${YELLOW}You can now use TuxScan from anywhere by typing:${NC}"
echo "tuxscan /path/to/scan" 