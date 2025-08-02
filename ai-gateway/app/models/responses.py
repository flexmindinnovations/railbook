"""
Response Models
==============

Pydantic models for API responses with proper v2 configuration.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class IntentResponse(BaseModel):
    """Intent classification response model."""
    
    intent: str = Field(..., description="Classified intent")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    entities: Dict[str, Any] = Field(..., description="Extracted entities")
    response: str = Field(..., description="Generated response text")
    suggested_actions: List[Dict[str, Any]] = Field(default_factory=list, description="Suggested follow-up actions")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "intent": "book_ticket",
                "confidence": 0.92,
                "entities": {
                    "source": "New Delhi",
                    "destination": "Mumbai",
                    "date": "2025-08-15",
                    "class": "3A"
                },
                "response": "I'll help you book train tickets from New Delhi to Mumbai on August 15th in 3AC class.",
                "suggested_actions": [
                    {"action": "search_trains", "parameters": {"route": "NDLS-CSTM"}}
                ]
            }
        }
    }


class EntityExtractionResponse(BaseModel):
    """Entity extraction response model."""
    
    entities: Dict[str, Any] = Field(..., description="Extracted entities")
    confidence_scores: Dict[str, float] = Field(..., description="Confidence score for each entity")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "entities": {
                    "source_station": "New Delhi",
                    "destination_station": "Mumbai Central",
                    "journey_date": "2025-08-15",
                    "train_class": "3A"
                },
                "confidence_scores": {
                    "source_station": 0.95,
                    "destination_station": 0.92,
                    "journey_date": 0.98,
                    "train_class": 0.85
                },
                "processing_time_ms": 120
            }
        }
    }


class WaitlistPredictionResponse(BaseModel):
    """Waitlist prediction response model."""
    
    train_number: str = Field(..., description="Train number")
    class_code: str = Field(..., description="Class code")
    journey_date: str = Field(..., description="Journey date")
    current_waitlist_position: int = Field(..., description="Current waitlist position")
    confirmation_probability: float = Field(..., ge=0.0, le=1.0, description="Confirmation probability")
    probability_category: str = Field(..., description="Human-readable probability category")
    estimated_confirmation_date: Optional[str] = Field(None, description="Estimated confirmation date")
    confidence_interval: List[float] = Field(..., description="Prediction confidence interval")
    ml_model_version: str = Field(..., description="ML model version used")
    prediction_timestamp: str = Field(..., description="Prediction timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "train_number": "12951",
                "class_code": "3A",
                "journey_date": "2025-08-15",
                "current_waitlist_position": 25,
                "confirmation_probability": 0.78,
                "probability_category": "High",
                "estimated_confirmation_date": "2025-08-12",
                "confidence_interval": [0.68, 0.88],
                "ml_model_version": "v2.0.0",
                "prediction_timestamp": "2025-08-02T10:30:00Z"
            }
        }
    }


class ConversationResponse(BaseModel):
    """Conversational AI response model."""
    
    response: str = Field(..., description="Generated response text")
    context_updated: bool = Field(..., description="Whether conversation context was updated")
    follow_up_suggestions: List[str] = Field(default_factory=list, description="Follow-up suggestions")
    session_id: Optional[str] = Field(None, description="Session identifier")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "response": "I understand you want to book train tickets. Could you tell me your source and destination?",
                "context_updated": True,
                "follow_up_suggestions": [
                    "Search for trains",
                    "Check PNR status",
                    "View booking history"
                ],
                "session_id": "sess_12345"
            }
        }
    }


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Service status")
    models_loaded: bool = Field(..., description="Whether ML models are loaded")
    spacy_available: bool = Field(..., description="Whether SpaCy is available")
    timestamp: str = Field(..., description="Health check timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "models_loaded": True,
                "spacy_available": True,
                "timestamp": "2025-08-02T10:30:00Z"
            }
        }
    }
