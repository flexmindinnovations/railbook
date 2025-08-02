"""
Core application configuration using Pydantic Settings.
Manages environment variables and application settings.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://railbooker_user:railbooker_pass@localhost:5432/railbooker_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security Settings
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI/ML Configuration
    ML_MODEL_PATH: str = "../model-serving/models/"
    SPACY_MODEL: str = "en_core_web_sm"
    
    # External APIs
    IRCTC_API_BASE_URL: str = "https://api.irctc.co.in"
    PAYMENT_GATEWAY_URL: str = "https://api.paymentgateway.com"
    
    # Environment Settings
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Additional Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RailBooker"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
