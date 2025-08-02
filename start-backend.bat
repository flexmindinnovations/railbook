@echo off
REM Backend startup script using global venv

REM Change to project root
cd /d "%~dp0"

REM Activate global virtual environment
call venv\Scripts\activate.bat

REM Change to backend directory
cd backend

REM Start the backend server
echo 🚀 Starting RailBooker Backend API...
echo 📍 URL: http://127.0.0.1:8000
echo 📖 Docs: http://127.0.0.1:8000/docs

uvicorn main:app --reload --host 127.0.0.1 --port 8000
