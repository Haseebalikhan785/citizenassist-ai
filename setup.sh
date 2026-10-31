#!/bin/bash
# CitizenAssist AI - Setup Script
# Run this once to set up the project

set -e

echo "============================================"
echo "  CitizenAssist AI - Setup"
echo "  Intelligent Public Service Navigator"
echo "============================================"
echo ""

# Check prerequisites
echo "[1/8] Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "ERROR: Python 3 is required. Install from https://www.python.org/downloads/"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "ERROR: Node.js is required. Install from https://nodejs.org/"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "ERROR: npm is required. Install Node.js from https://nodejs.org/"; exit 1; }

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "  Python: $PYTHON_VERSION"
echo "  Node: $(node --version)"
echo "  npm: $(npm --version)"

# Create virtual environment
echo ""
echo "[2/8] Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Created venv/"
else
    echo "  venv/ already exists, skipping"
fi

# Activate venv
source venv/bin/activate

# Install backend dependencies
echo ""
echo "[3/8] Installing backend dependencies..."
pip install -r backend/requirements.txt --quiet 2>&1 | tail -5
echo "  Backend dependencies installed"

# Install frontend dependencies
echo ""
echo "[4/8] Installing frontend dependencies..."
cd frontend
npm install --silent 2>&1 | tail -3
echo "  Frontend dependencies installed"

# Build frontend
echo ""
echo "[5/8] Building frontend..."
npm run build 2>&1 | tail -5
echo "  Frontend built to frontend/dist/"
cd ..

# Create .env from .env.example if it doesn't exist
echo ""
echo "[6/8] Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    # Generate random SECRET_KEY
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/SECRET_KEY=change-me-to-a-random-string/SECRET_KEY=$SECRET_KEY/" .env
    else
        sed -i "s/SECRET_KEY=change-me-to-a-random-string/SECRET_KEY=$SECRET_KEY/" .env
    fi
    echo "  Created .env with random SECRET_KEY"
else
    echo "  .env already exists, skipping"
fi

# Initialize database and seed data
echo ""
echo "[7/8] Initializing database and seeding data..."
PYTHONPATH=. python -m backend.app.init_db
echo "  Database initialized and seeded"

# Create data directories
mkdir -p data/documents data/uploads

echo ""
echo "[8/8] Setup complete!"
echo ""
echo "============================================"
echo "  SETUP COMPLETE"
echo "============================================"
echo ""
echo "  Login credentials are in LOCAL_CREDENTIALS.txt"
echo ""
if [ -f "LOCAL_CREDENTIALS.txt" ]; then
    cat LOCAL_CREDENTIALS.txt
fi
echo ""
echo "  To start the website, run:"
echo "    ./start.sh"
echo ""
echo "  To add AI features, paste your Gemini API key"
echo "  in .env (GEMINI_API_KEY=your-key-here)"
echo "  Get a free key at: https://aistudio.google.com/apikey"
echo ""
