#!/bin/bash
# Mirror Companion — One-command Pi setup
# Run this on your Raspberry Pi: bash setup.sh

set -e

echo "========================================="
echo "  Mirror Companion — Pi Setup"
echo "========================================="
echo ""

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# --- System dependencies ---
echo "[1/6] Installing system dependencies..."
sudo apt update -qq
sudo apt install -y -qq \
    python3 python3-pip python3-venv \
    portaudio19-dev \
    ffmpeg \
    chromium-browser \
    nodejs npm \
    git

# Ensure Node.js is recent enough (need 18+)
NODE_VERSION=$(node -v 2>/dev/null | cut -d'.' -f1 | tr -d 'v')
if [ -z "$NODE_VERSION" ] || [ "$NODE_VERSION" -lt 18 ]; then
    echo "  Node.js too old or missing. Installing Node 20..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install -y -qq nodejs
fi
echo "  Node.js: $(node -v), npm: $(npm -v)"

# --- Backend setup ---
echo ""
echo "[2/6] Setting up Python backend..."
cd "$PROJECT_DIR/backend"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
deactivate
echo "  Backend dependencies installed."

# --- Frontend setup ---
echo ""
echo "[3/6] Setting up React frontend..."
cd "$PROJECT_DIR/frontend"
npm install --silent
npm run build
echo "  Frontend built."

# --- Environment file ---
echo ""
echo "[4/6] Checking .env file..."
cd "$PROJECT_DIR"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  Created .env from template."
    echo "  !! IMPORTANT: Edit .env and add your OpenAI API key !!"
    echo "  Run: nano $PROJECT_DIR/.env"
else
    echo "  .env already exists."
fi

# --- Systemd services ---
echo ""
echo "[5/6] Installing systemd services..."
PI_USER=$(whoami)
PI_HOME=$(eval echo ~$PI_USER)

# Update service files with correct paths and username
sed "s|/home/pi/mirror-companion|$PROJECT_DIR|g; s|User=pi|User=$PI_USER|g" \
    "$PROJECT_DIR/systemd/mirror-backend.service" | sudo tee /etc/systemd/system/mirror-backend.service > /dev/null

sed "s|/home/pi/mirror-companion|$PROJECT_DIR|g; s|User=pi|User=$PI_USER|g" \
    "$PROJECT_DIR/systemd/mirror-frontend.service" | sudo tee /etc/systemd/system/mirror-frontend.service > /dev/null

sudo systemctl daemon-reload
sudo systemctl enable mirror-backend.service
sudo systemctl enable mirror-frontend.service
echo "  Services installed and enabled."

# --- Summary ---
echo ""
echo "[6/6] Setup complete!"
echo ""
echo "========================================="
echo "  Next steps:"
echo "========================================="
echo ""
echo "  1. Add your OpenAI API key:"
echo "     nano $PROJECT_DIR/.env"
echo ""
echo "  2. Start the backend:"
echo "     sudo systemctl start mirror-backend"
echo ""
echo "  3. Start the frontend kiosk:"
echo "     sudo systemctl start mirror-frontend"
echo ""
echo "  Or for development (manual start):"
echo "     # Terminal 1 — Backend"
echo "     cd $PROJECT_DIR/backend"
echo "     source venv/bin/activate"
echo "     python main.py"
echo ""
echo "     # Terminal 2 — Frontend"
echo "     cd $PROJECT_DIR/frontend"
echo "     npm run dev"
echo ""
echo "  View logs:"
echo "     journalctl -u mirror-backend -f"
echo "     journalctl -u mirror-frontend -f"
echo ""
echo "  Access from another device on your network:"
echo "     Mirror:    http://$(hostname).local:5173"
echo "     Dashboard: http://$(hostname).local:5173/dashboard"
echo "     API:       http://$(hostname).local:8000/health"
echo ""
echo "========================================="
