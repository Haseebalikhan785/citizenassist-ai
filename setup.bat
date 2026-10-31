@echo off
REM CitizenAssist AI - Setup Script for Windows
REM Run this once to set up the project

echo ============================================
echo   CitizenAssist AI - Setup
echo   Intelligent Public Service Navigator
echo ============================================
echo.

REM Check prerequisites
echo [1/8] Checking prerequisites...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python 3 is required. Install from https://www.python.org/downloads/
    exit /b 1
)
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is required. Install from https://nodejs.org/
    exit /b 1
)
where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: npm is required. Install Node.js from https://nodejs.org/
    exit /b 1
)

python --version
node --version
npm --version

REM Create virtual environment
echo.
echo [2/8] Creating Python virtual environment...
if not exist "venv" (
    python -m venv venv
    echo   Created venv\
) else (
    echo   venv\ already exists, skipping
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install backend dependencies
echo.
echo [3/8] Installing backend dependencies...
pip install -r backend\requirements.txt --quiet
echo   Backend dependencies installed

REM Install frontend dependencies
echo.
echo [4/8] Installing frontend dependencies...
cd frontend
call npm install --silent
echo   Frontend dependencies installed

REM Build frontend
echo.
echo [5/8] Building frontend...
call npm run build
echo   Frontend built to frontend\dist\
cd ..

REM Create .env from .env.example if it doesn't exist
echo.
echo [6/8] Setting up environment...
if not exist ".env" (
    copy .env.example .env >nul
    REM Generate random SECRET_KEY
    for /f %%i in ('python -c "import secrets; print(secrets.token_urlsafe(32))"') do set SECRET_KEY=%%i
    python -c "import sys; content=open('.env').read(); content=content.replace('SECRET_KEY=change-me-to-a-random-string', 'SECRET_KEY=%SECRET_KEY%'); open('.env','w').write(content)"
    echo   Created .env with random SECRET_KEY
) else (
    echo   .env already exists, skipping
)

REM Initialize database and seed data
echo.
echo [7/8] Initializing database and seeding data...
python -m backend.app.init_db
echo   Database initialized and seeded

REM Create data directories
if not exist "data\documents" mkdir data\documents
if not exist "data\uploads" mkdir data\uploads

echo.
echo [8/8] Setup complete!
echo.
echo ============================================
echo   SETUP COMPLETE
echo ============================================
echo.
echo   Login credentials are in LOCAL_CREDENTIALS.txt
echo.
if exist "LOCAL_CREDENTIALS.txt" (
    type LOCAL_CREDENTIALS.txt
)
echo.
echo   To start the website, run:
echo     start.bat
echo.
echo   To add AI features, paste your Gemini API key
echo   in .env (GEMINI_API_KEY=your-key-here)
echo   Get a free key at: https://aistudio.google.com/apikey
echo.
