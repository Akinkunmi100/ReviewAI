@echo off
echo Setting up virtual environment for the project...

:: Check if venv directory already exists
if exist "venv" (
    echo Virtual environment already exists.
    echo Activating existing virtual environment...
    call venv\Scripts\activate
    echo Virtual environment activated.
    echo You can now install dependencies with: pip install -r requirements.txt
    goto :end
)

:: Try to create virtual environment using different Python installations
echo Creating new virtual environment...

:: First try with system Python
python -m venv venv 2>nul
if %errorlevel% equ 0 (
    echo Virtual environment created successfully with system Python.
    call venv\Scripts\activate
    echo Virtual environment activated.
    echo You can now install dependencies with: pip install -r requirements.txt
    goto :end
)

:: If that fails, try with Anaconda Python
echo Trying with Anaconda Python...
C:\Users\MSI\anaconda3\python.exe -m venv venv 2>nul
if %errorlevel% equ 0 (
    echo Virtual environment created successfully with Anaconda Python.
    call venv\Scripts\activate
    echo Virtual environment activated.
    echo You can now install dependencies with: pip install -r requirements.txt
    goto :end
)

:: If both fail, show error
echo ❌ Failed to create virtual environment with both Python installations.
echo Please check your Python installations and try again.

:end
echo.
echo To use this virtual environment in the future:
echo 1. Open a new terminal in VS Code
echo 2. Run: venv\Scripts\activate
echo 3. Your prompt should show (venv) when activated