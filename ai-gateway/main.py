"""
AI Gateway for RailBooker - Refactored
======================================

Modular FastAPI service following industry-standard design patterns:
- Layered Architecture (API -> Service -> Data)
- Dependency Injection 
- Strategy Pattern for ML algorithms
- Factory Pattern for service creation
- Repository Pattern for data access
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.api.routes import router


def create_app() -> FastAPI:
    """
    Application factory pattern.
    Creates and configures FastAPI application.
    """
    settings = get_settings()
    
    # Setup logging
    setup_logging(settings.log_level)
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        description="""
        ## Modular AI Gateway for Railway Booking Assistant
        
        **Architecture**: Clean, layered design following industry best practices
        
        ### 🏗️ Design Patterns Implemented:
        - **Layered Architecture** - Separation of concerns (API/Service/Data)
        - **Dependency Injection** - Loose coupling and testability
        - **Strategy Pattern** - Pluggable ML algorithms  
        - **Factory Pattern** - Service creation and configuration
        - **Repository Pattern** - Data access abstraction
        
        ### 🧠 AI Capabilities:
        - 🎯 **Intent Recognition** - Understanding user booking requests
        - 📋 **Entity Extraction** - Extracting source, destination, dates, etc.
        - 📊 **Waitlist Prediction** - ML-based confirmation probability
        - 🤖 **Conversational AI** - Natural language responses
        - 🔍 **Smart Suggestions** - Alternative route recommendations
        
        ### 📁 Module Structure:
        ```
        app/
        ├── api/          # HTTP layer (FastAPI routes)
        ├── services/     # Business logic layer  
        ├── models/       # Pydantic schemas
        ├── core/         # Configuration & utilities
        └── utils/        # Helper functions
        ```
        """,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(router)
    
    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
        log_level=settings.log_level
    )
