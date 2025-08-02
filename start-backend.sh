#!/bin/bash
# Backend startup script using global venv

# Change to project root
cd "$(dirname "$0")"

# Activate global virtual environment
source venv/bin/activate

# Change to backend directory
cd backend

# Start the backend server
echo "🚀 Starting RailBooker Backend API..."
echo "📍 URL: http://127.0.0.1:8000"
echo "📖 Docs: http://127.0.0.1:8000/docs"

uvicorn main:app --reload --host 127.0.0.1 --port 8000
