@echo off
REM RailBooker Development Setup Script for Windows
REM Run this script to set up the complete development environment

echo 🚂 Setting up RailBooker Development Environment...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create necessary directories
echo 📁 Creating project directories...
if not exist "logs" mkdir logs
if not exist "data\postgres" mkdir data\postgres
if not exist "data\redis" mkdir data\redis
if not exist "model-serving\models" mkdir model-serving\models

REM Copy environment files
echo ⚙️ Setting up environment configuration...
if not exist "backend\.env" (
    copy "backend\.env.example" "backend\.env"
    echo ✅ Created backend\.env from template
)

REM Build and start services
echo 🐳 Building and starting Docker services...
docker-compose up -d --build

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check service health
echo 🔍 Checking service health...
curl -f http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend API is not responding
) else (
    echo ✅ Backend API is healthy
)

curl -f http://localhost:8001/health >nul 2>&1
if errorlevel 1 (
    echo ❌ AI Gateway is not responding
) else (
    echo ✅ AI Gateway is healthy
)

REM Display service URLs
echo.
echo 🎉 RailBooker Development Environment is ready!
echo.
echo 📊 Service URLs:
echo    Backend API:    http://localhost:8000
echo    API Docs:       http://localhost:8000/docs
echo    AI Gateway:     http://localhost:8001
echo    AI Docs:        http://localhost:8001/docs
echo    PostgreSQL:     localhost:5432
echo    Redis:          localhost:6379
echo.
echo 🔧 Development Commands:
echo    View logs:      docker-compose logs -f
echo    Stop services:  docker-compose down
echo    Restart:        docker-compose restart
echo    Shell access:   docker-compose exec backend bash
echo.
echo 📚 Next Steps:
echo    1. Check API documentation at http://localhost:8000/docs
echo    2. Test AI Gateway at http://localhost:8001/docs
echo    3. Start developing the frontend
echo    4. Add sample data to the database
echo.
pause
