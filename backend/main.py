"""
RailBooker Backend API
======================

Main FastAPI application for the RailBooker platform.
Handles railway ticket booking, AI assistance, and user management.

Author: RailBooker Development Team
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import structlog
import uvicorn
from datetime import datetime
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Import configuration and database
from app.core.config import settings
from app.database.connection import engine, create_tables
from app.api.v1.routers import auth, trains, bookings, ai_assistant, users

# Application lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    # Startup
    logger.info("Starting RailBooker API server")
    await create_tables()
    logger.info("Database tables created/verified")
    
    yield
    
    # Shutdown
    logger.info("Shutting down RailBooker API server")

# Create FastAPI app with comprehensive configuration
app = FastAPI(
    title="RailBooker API",
    description="""
    ## RailBooker - AI-Powered Railway Booking System
    
    A comprehensive API for Indian Railway ticket booking with AI assistance.
    
    ### Features:
    - 🤖 **AI-Powered Booking Assistant** - Natural language booking interface
    - 🎯 **Waitlist Prediction** - ML-based confirmation probability
    - 🚂 **Train Search & Booking** - Complete booking management
    - 📱 **Real-time Updates** - Live PNR status and notifications
    - 🔒 **Secure Authentication** - JWT-based user management
    
    ### Key Endpoints:
    - `/api/v1/auth/` - User authentication and management
    - `/api/v1/trains/` - Train search and information
    - `/api/v1/bookings/` - Booking management and PNR operations
    - `/api/v1/ai/` - AI assistant and natural language processing
    """,
    version="1.0.0",
    contact={
        "name": "RailBooker Support",
        "email": "support@railbooker.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Security and middleware configuration
security = HTTPBearer()

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Add production URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Trusted host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.railbooker.com"]
)

# API Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(trains.router, prefix="/api/v1/trains", tags=["Trains & Routes"])  
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["Bookings & PNR"])
app.include_router(ai_assistant.router, prefix="/api/v1/ai", tags=["AI Assistant"])
app.include_router(users.router, prefix="/api/v1/users", tags=["User Management"])

# Health check and system status endpoints
@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information."""
    return {
        "service": "RailBooker API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "docs": "/docs",
        "features": [
            "AI-Powered Booking Assistant",
            "Waitlist Prediction",
            "Real-time Train Search",
            "Secure User Management"
        ]
    }

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # TODO: Add database connection check
        # TODO: Add Redis connection check
        # TODO: Add external API checks
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "database": "connected",
                "redis": "connected", 
                "ai_models": "loaded"
            }
        }
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable"
        )

@app.get("/metrics", tags=["System"])
async def metrics():
    """Prometheus metrics endpoint."""
    # TODO: Implement Prometheus metrics
    return {"message": "Metrics endpoint - TODO: Implement Prometheus integration"}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(
        "Unhandled exception",
        path=request.url.path,
        method=request.method,
        error=str(exc)
    )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("BACKEND_PORT", 8000)),
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )
