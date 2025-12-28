@echo off
echo ========================================
echo Product Review Engine - Backend Starter
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run setup_venv.bat first to create it.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if activation was successful
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment!
    pause
    exit /b 1
)

echo Virtual environment activated!
echo.

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create a .env file with your GROQ_API_KEY
    echo You can copy .env.example and add your key.
    echo.
    pause
    exit /b 1
)

echo Starting FastAPI backend server...
echo Server will be available at: http://localhost:8001
echo API documentation at: http://localhost:8001/docs
echo.
echo Press CTRL+C to stop the server
echo.

uvicorn api:app --reload --port 8001

REM If server stops, deactivate venv
deactivate
