@echo off
REM AI Gateway startup script using global venv

REM Change to project root
cd /d "%~dp0"

REM Activate global virtual environment
call venv\Scripts\activate.bat

REM Change to ai-gateway directory
cd ai-gateway

REM Start the AI gateway server
echo 🤖 Starting RailBooker AI Gateway...
echo 📍 URL: http://127.0.0.1:8001
echo 🧠 AI Services: Intent Classification, Waitlist Prediction

uvicorn main:app --reload --host 127.0.0.1:8001 --port 8001
