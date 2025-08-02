"""
Core Configuration for AI Gateway
=================================

Centralized configuration management using dependency injection pattern.
Follows 12-factor app principles for configuration.
"""

import os
from functools import lru_cache
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment from project root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    app_name: str = "RailBooker AI Gateway"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Server
    host: str = "0.0.0.0"
    port: int = int(os.getenv("AI_GATEWAY_PORT", 8001))
    log_level: str = os.getenv("LOG_LEVEL", "info").lower()
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # ML Models
    ml_model_path: str = os.getenv("ML_MODEL_PATH", "./models/")
    spacy_model: str = os.getenv("SPACY_MODEL", "en_core_web_sm")
    
    # External Services (for future integration)
    redis_url: Optional[str] = os.getenv("REDIS_URL")
    database_url: Optional[str] = os.getenv("DATABASE_URL")
    
    # API Keys (for external ML services)
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    huggingface_api_key: Optional[str] = os.getenv("HUGGINGFACE_API_KEY")
    
    # Rate Limiting
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", 60))
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


class ModelConfig:
    """ML Model configuration."""
    
    # Intent Classification
    INTENT_MODEL_VERSION = "v1.2.0"
    INTENT_CONFIDENCE_THRESHOLD = 0.7
    
    # Entity Extraction
    NER_MODEL_VERSION = "v1.1.0"
    ENTITY_CONFIDENCE_THRESHOLD = 0.8
    
    # Waitlist Prediction
    WAITLIST_MODEL_VERSION = "v2.0.0"
    PREDICTION_CONFIDENCE_THRESHOLD = 0.75
    
    # Supported intents
    SUPPORTED_INTENTS = [
        "book_ticket",
        "check_status", 
        "cancel_booking",
        "get_train_info",
        "check_availability",
        "general_inquiry"
    ]
    
    # Supported entities
    SUPPORTED_ENTITIES = [
        "source_station",
        "destination_station", 
        "journey_date",
        "train_class",
        "passenger_count",
        "pnr_number",
        "train_number"
    ]


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


@lru_cache() 
def get_model_config() -> ModelConfig:
    """Get cached model configuration."""
    return ModelConfig()
