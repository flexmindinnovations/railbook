#!/bin/bash

# RailBooker Development Setup Script
# Run this script to set up the complete development environment

set -e

echo "🚂 Setting up RailBooker Development Environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p logs
mkdir -p data/postgres
mkdir -p data/redis
mkdir -p model-serving/models

# Copy environment files
echo "⚙️ Setting up environment configuration..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env from template"
fi

# Build and start services
echo "🐳 Building and starting Docker services..."
docker-compose up -d --build

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is healthy"
else
    echo "❌ Backend API is not responding"
fi

if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ AI Gateway is healthy"
else
    echo "❌ AI Gateway is not responding"
fi

# Display service URLs
echo ""
echo "🎉 RailBooker Development Environment is ready!"
echo ""
echo "📊 Service URLs:"
echo "   Backend API:    http://localhost:8000"
echo "   API Docs:       http://localhost:8000/docs"
echo "   AI Gateway:     http://localhost:8001"
echo "   AI Docs:        http://localhost:8001/docs"
echo "   PostgreSQL:     localhost:5432"
echo "   Redis:          localhost:6379"
echo ""
echo "🔧 Development Commands:"
echo "   View logs:      docker-compose logs -f"
echo "   Stop services:  docker-compose down"
echo "   Restart:        docker-compose restart"
echo "   Shell access:   docker-compose exec backend bash"
echo ""
echo "📚 Next Steps:"
echo "   1. Check API documentation at http://localhost:8000/docs"
echo "   2. Test AI Gateway at http://localhost:8001/docs"
echo "   3. Start developing the frontend"
echo "   4. Add sample data to the database"
echo ""
