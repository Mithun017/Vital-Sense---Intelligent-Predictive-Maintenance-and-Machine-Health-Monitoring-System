@echo off
setlocal
echo ==========================================================
echo    VITAL SENSE AI - UNIFIED SYSTEM STARTUP
echo ==========================================================
echo.

:: 1. Start Backend (Port 8000)
echo [+] Starting AI Brain (Backend)...
start "Vital Sense Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --port 8000"

:: 2. Start Frontend (Port 5173)
echo [+] Starting AI Dashboard (Frontend)...
start "Vital Sense Frontend" cmd /k "cd frontend && npm run dev"

:: Wait for services to initialize
timeout /t 5 /nobreak > nul

:: 3. Start Standard Simulators (M-101 and M-102)
echo [+] Launching Machine Simulators...
start "M-101 Simulator" cmd /k "cd simulation && python simulate_sensors.py --id M-101"
start "M-102 Simulator" cmd /k "cd simulation && python simulate_sensors.py --id M-102"

:: 4. Start Virtual Hardware Terminal (ESP32)
echo [+] Launching Virtual Hardware Simulation...
start "Virtual ESP32 Terminal" cmd /k "python simulation\virtual_esp32.py"

:: 5. Auto-open Dashboard
echo.
echo [+] System is ready! Redirecting to Dashboard...
timeout /t 3 /nobreak > nul
start http://localhost:5173

echo.
echo ==========================================================
echo    ALL SERVICES RUNNING - CLOSE WINDOWS TO STOP
echo ==========================================================
pause
