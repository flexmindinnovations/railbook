@echo off
REM RailBooker Project - Prevent File Restoration
REM This script ensures deleted files stay deleted

echo Cleaning up any restored files...

REM Remove individual requirements.txt files
if exist "backend\requirements.txt" del /f /q "backend\requirements.txt"
if exist "ai-gateway\requirements.txt" del /f /q "ai-gateway\requirements.txt"

REM Remove .env.example files
if exist ".env.example" del /f /q ".env.example"
if exist "backend\.env.example" del /f /q "backend\.env.example"
if exist "ai-gateway\.env.example" del /f /q "ai-gateway\.env.example"

REM Remove individual .env files (keeping root .env)
if exist "backend\.env" del /f /q "backend\.env"
if exist "ai-gateway\.env" del /f /q "ai-gateway\.env"

REM Remove Dockerfiles
if exist "backend\Dockerfile" del /f /q "backend\Dockerfile"
if exist "ai-gateway\Dockerfile" del /f /q "ai-gateway\Dockerfile"

REM Clean __pycache__ directories (project only, not venv)
for /d /r "backend" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /d /r "ai-gateway" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo Cleanup complete. Only root-level configuration files should exist.
pause
