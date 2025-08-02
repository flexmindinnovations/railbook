#!/bin/bash
# AI Gateway startup script using global venv

# Change to project root
cd "$(dirname "$0")"

# Activate global virtual environment
source venv/bin/activate

# Change to ai-gateway directory
cd ai-gateway

# Start the AI gateway server
echo "🤖 Starting RailBooker AI Gateway..."
echo "📍 URL: http://127.0.0.1:8001"
echo "🧠 AI Services: Intent Classification, Waitlist Prediction"

uvicorn main:app --reload --host 127.0.0.1 --port 8001
