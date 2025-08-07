@echo off
echo 🔍 Checking Ollama status...

REM Check if Ollama is already running using PowerShell
powershell -Command "if (Test-NetConnection -ComputerName localhost -Port 11434 -WarningAction SilentlyContinue).TcpTestSucceeded { exit 0 } else { exit 1 }"

if %errorlevel% equ 0 (
    echo ✅ Ollama is already running
) else (
    echo 🚀 Starting Ollama...
    start /B ollama serve
    timeout /t 5 /nobreak > nul
)

echo 🎮 Starting Adventure Learning Quest...
call python src/app.py
pause