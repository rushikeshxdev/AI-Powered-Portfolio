@echo off
REM Backend Setup Script for Windows
REM This batch file runs the Python setup script

echo.
echo ====================================================================
echo   Backend Setup for Windows
echo ====================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Running setup script...
echo.

REM Run the Python setup script
python setup_backend.py

REM Check if setup was successful
if errorlevel 1 (
    echo.
    echo Setup encountered errors. Please review the output above.
    echo.
    pause
    exit /b 1
)

echo.
echo Setup complete!
echo.
pause
