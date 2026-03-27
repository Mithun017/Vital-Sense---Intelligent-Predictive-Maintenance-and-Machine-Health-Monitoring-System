@echo off
setlocal
echo ==========================================================
echo    VITAL SENSE AI - COMPLETE PROJECT SETUP
echo ==========================================================
echo.

:: 1. Backend Setup (Python)
echo [+] Setting up Python Backend...
cd backend
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies.
    pause
    exit /b 1
)
cd ..

:: 2. Frontend Setup (Node.js)
echo.
echo [+] Setting up React Dashboard...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Node.js dependencies.
    pause
    exit /b 1
)
cd ..

:: 3. Wokwi Setup (Hardware Simulation)
echo.
echo [+] Setting up Wokwi Hardware Simulation...
powershell -Command "iwr https://wokwi.com/ci/install.ps1 -useb | iex"

echo.
echo ==========================================================
echo    SETUP COMPLETE!
echo ==========================================================
echo Actions Taken:
echo - Python dependencies installed (Backend)
echo - Node behaviors and components installed (Frontend)
echo - Wokwi CLI installed (Hardware)
echo.
echo Launching your Advanced AI Predictive Maintenance project...
timeout /t 3 /nobreak > nul
call run_start.bat
