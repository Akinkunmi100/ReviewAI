@echo off
REM Quick Start Script for Product Review Engine
REM This script will help you run the health check and start the application

echo ========================================
echo Product Review Engine - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Installing/Updating dependencies...
pip install -r requirements.txt --quiet
echo Dependencies installed!
echo.

echo ========================================
echo Running Comprehensive Health Check...
echo ========================================
echo.

python comprehensive_check.py

echo.
echo ========================================
echo Health check complete!
echo ========================================
echo.

pause
