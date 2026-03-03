@echo off
chcp 65001 >nul
echo Hindi to Hinglish Converter
echo ============================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    venv\Scripts\pip install -r requirements.txt
)

REM Run the application
if "%~1"=="" (
    echo Launching GUI...
    venv\Scripts\python main.py
) else (
    echo Running with arguments: %*
    venv\Scripts\python main.py %*
)
