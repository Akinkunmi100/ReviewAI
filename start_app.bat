@echo off
REM Full Application Startup Script
REM This script starts both backend and frontend servers

echo ========================================
echo Product Review Engine - Full Startup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run quick_start.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

echo Starting Backend Server...
echo.

REM Start backend in a new window
start "Product Review Engine - Backend" cmd /k "cd /d %~dp0 && venv\Scripts\activate && echo Starting FastAPI backend on http://localhost:8001 && echo. && uvicorn api:app --reload --port 8001"

REM Wait a moment for backend to initialize
timeout /t 3 /nobreak > nul

echo Backend server starting...
echo.

REM Check if frontend dependencies are installed
if not exist "frontend\node_modules\" (
    echo Frontend dependencies not found. Installing...
    cd frontend
    call npm install
    cd ..
    echo.
)

echo Starting Frontend Server...
echo.

REM Start frontend in a new window
start "Product Review Engine - Frontend" cmd /k "cd /d %~dp0\frontend && echo Starting Vite dev server on http://localhost:5173 && echo. && npm run dev"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:5173
echo.
echo Two new windows have opened:
echo 1. Backend (FastAPI) - Port 8001
echo 2. Frontend (React/Vite) - Port 5173
echo.
echo Wait a few seconds, then open your browser to:
echo http://localhost:5173
echo.
echo To stop the servers, close both command windows.
echo.

timeout /t 5 /nobreak > nul

REM Try to open browser automatically
start http://localhost:5173

echo.
echo Browser should open automatically.
echo If not, manually go to: http://localhost:5173
echo.
pause
