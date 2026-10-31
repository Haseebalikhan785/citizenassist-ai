@echo off
REM CitizenAssist AI - Start Script for Windows
REM Starts the website on http://localhost:8000

echo ============================================
echo   CitizenAssist AI - Starting...
echo   Intelligent Public Service Navigator
echo ============================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo ERROR: Virtual environment not found. Run setup.bat first.
    exit /b 1
)

REM Activate venv
call venv\Scripts\activate.bat

REM Check if database exists
if not exist "data\citizenassist.db" (
    echo Database not found. Initializing...
    python -m backend.app.init_db
)

REM Check if frontend is built
if not exist "frontend\dist" (
    echo Frontend not built. Building...
    cd frontend
    call npm run build
    cd ..
)

echo   Starting server...
echo.
echo   Website: http://localhost:8000
echo   Press Ctrl+C to stop
echo.

REM Start the server
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
