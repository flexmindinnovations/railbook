"""
Request/Response Models
======================

Pydantic mo    model_config = {
        "json_schema_extra": {
            "example": {
                "train_number": "12951",
                "class_code": "3A",
                "journey_date": "2024-08-15",
                "current_waitlist_position": 25,
                "quota": "GENERAL"
            }
        }
    }PI request and response validation.
Follows OpenAPI specification for consistent API documentation.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator


class ChatMessage(BaseModel):
    """Chat message model for conversational AI."""
    
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    session_id: Optional[str] = Field(None, description="Conversation session ID")
    user_id: Optional[str] = Field(None, description="User identifier")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Conversation context")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "I want to book a train ticket from Delhi to Mumbai",
                "session_id": "sess_12345",
                "user_id": "user_67890",
                "context": {"previous_intent": "greeting"}
            }
        }
    }


class EntityExtractionRequest(BaseModel):
    """Entity extraction request model."""
    
    text: str = Field(..., min_length=1, max_length=2000, description="Text for entity extraction")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "Book 2 tickets from New Delhi to Mumbai on August 15th in 3AC",
                "context": {"user_preferences": {"class": "3AC"}}
            }
        }
    }


class WaitlistPredictionRequest(BaseModel):
    """Waitlist prediction request model."""
    
    train_number: str = Field(..., pattern=r'^\d{5}$', description="5-digit train number")
    class_code: str = Field(..., pattern=r'^(SL|3A|2A|1A|CC|EC|2S)$', description="Train class code")
    journey_date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$', description="Journey date (YYYY-MM-DD)")
    current_waitlist_position: int = Field(..., ge=1, le=500, description="Current waitlist position")
    quota: str = Field(default="GENERAL", description="Booking quota")
    
    @field_validator('journey_date')
    @classmethod
    def validate_future_date(cls, v):
        """Ensure journey date is not in the past."""
        from datetime import datetime
        journey_dt = datetime.strptime(v, '%Y-%m-%d')
        if journey_dt.date() < datetime.now().date():
            raise ValueError('Journey date cannot be in the past')
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "train_number": "12951",
                "class_code": "3A", 
                "journey_date": "2025-08-15",
                "current_waitlist_position": 25,
                "quota": "GENERAL"
            }
        }
    }
