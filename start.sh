#!/bin/bash
# CitizenAssist AI - Start Script
# Starts the website on http://localhost:8000

set -e

echo "============================================"
echo "  CitizenAssist AI - Starting..."
echo "  Intelligent Public Service Navigator"
echo "============================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

# Activate venv
source venv/bin/activate

# Check if database exists
if [ ! -f "data/citizenassist.db" ]; then
    echo "Database not found. Initializing..."
    PYTHONPATH=. python -m backend.app.init_db
fi

# Check if frontend is built
if [ ! -d "frontend/dist" ]; then
    echo "Frontend not built. Building..."
    cd frontend && npm run build && cd ..
fi

echo "  Starting server..."
echo ""
echo "  ┌─────────────────────────────────────────┐"
echo "  │                                         │"
echo "  │   Website: http://localhost:8000         │"
echo "  │                                         │"
echo "  │   Press Ctrl+C to stop                  │"
echo "  │                                         │"
echo "  └─────────────────────────────────────────┘"
echo ""

# Start the server
PYTHONPATH=. python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
