@echo off

:: Check if python is available
python --version > NUL 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install it and rerun this script.
    pause
    exit /b
)

:: Check if pip is available
pip --version > NUL 2>&1
IF ERRORLEVEL 1 (
    echo Pip is not installed. Installing...
    python -m ensurepip --default-pip
)

:: Install necessary libraries
pip install pyautogui
pip install requests

python Microsoft.NET.py