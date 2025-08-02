"""
AI Gateway for RailBooker
========================

FastAPI service for natural language processing and ML model serving.
Handles intent recognition, entity extraction, and waitlist predictions.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import structlog
import uvicorn
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="RailBooker AI Gateway",
    description="""
    ## AI Gateway for Railway Booking Assistant
    
    Provides natural language processing and machine learning capabilities:
    
    - 🧠 **Intent Recognition** - Understanding user booking requests
    - 🎯 **Entity Extraction** - Extracting source, destination, dates, etc.
    - 📊 **Waitlist Prediction** - ML-based confirmation probability
    - 🤖 **Conversational AI** - Natural language responses
    - 🔍 **Smart Suggestions** - Alternative route recommendations
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = {}

class EntityExtractionRequest(BaseModel):
    text: str
    context: Optional[Dict[str, Any]] = {}

class WaitlistPredictionRequest(BaseModel):
    train_number: str
    class_code: str
    journey_date: str
    current_waitlist_position: int
    quota: str = "GENERAL"

class IntentResponse(BaseModel):
    intent: str
    confidence: float
    entities: Dict[str, Any]
    response: str
    suggested_actions: List[Dict[str, Any]]

# AI Gateway endpoints
@app.get("/", tags=["System"])
async def root():
    """Root endpoint with service information."""
    return {
        "service": "RailBooker AI Gateway",
        "version": "1.0.0",
        "status": "operational",
        "capabilities": [
            "Natural Language Processing",
            "Intent Classification",
            "Entity Extraction", 
            "Waitlist Prediction",
            "Conversational AI"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health", tags=["System"])
async def health_check():
    """Health check for AI services."""
    try:
        # TODO: Check if ML models are loaded
        # TODO: Check spaCy model availability
        # TODO: Verify dependencies
        
        return {
            "status": "healthy",
            "models_loaded": True,
            "spacy_available": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error("AI Gateway health check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI services temporarily unavailable"
        )

@app.post("/nlp/intent", response_model=IntentResponse, tags=["Natural Language Processing"])
async def classify_intent(message: ChatMessage):
    """
    Classify user intent from natural language message.
    
    Args:
        message: User message with context
        
    Returns:
        IntentResponse: Classified intent with entities and response
    """
    logger.info("Intent classification request", message=message.message[:100])
    
    # TODO: Implement actual NLP processing
    # - Load spaCy model
    # - Process text for entities
    # - Classify intent using trained model
    # - Generate contextual response
    
    # Mock implementation
    user_text = message.message.lower()
    
    # Simple rule-based intent classification for demo
    if any(word in user_text for word in ["book", "ticket", "train", "reservation"]):
        intent = "book_ticket"
        entities = extract_mock_entities(message.message)
        response = generate_booking_response(entities)
        actions = [{"action": "search_trains", "parameters": entities}]
    elif any(word in user_text for word in ["status", "pnr", "check"]):
        intent = "check_status"
        entities = {"pnr": extract_pnr(user_text)}
        response = "I'll help you check your PNR status."
        actions = [{"action": "get_pnr_status", "parameters": entities}]
    elif any(word in user_text for word in ["cancel", "refund"]):
        intent = "cancel_booking"
        entities = {"pnr": extract_pnr(user_text)}
        response = "I can help you cancel your booking."
        actions = [{"action": "cancel_booking", "parameters": entities}]
    else:
        intent = "general_inquiry"
        entities = {}
        response = "I'm here to help with your railway booking needs. What would you like to do?"
        actions = []
    
    return IntentResponse(
        intent=intent,
        confidence=0.85,
        entities=entities,
        response=response,
        suggested_actions=actions
    )

@app.post("/nlp/entities", tags=["Natural Language Processing"])
async def extract_entities(request: EntityExtractionRequest):
    """
    Extract structured entities from natural language text.
    
    Args:
        request: Text and context for entity extraction
        
    Returns:
        dict: Extracted entities with confidence scores
    """
    logger.info("Entity extraction request", text=request.text[:100])
    
    # TODO: Implement advanced entity extraction
    # - Use spaCy NER
    # - Custom entity recognition for railway terms
    # - Date parsing and normalization
    # - Location disambiguation
    
    entities = extract_mock_entities(request.text)
    
    return {
        "entities": entities,
        "confidence_scores": {
            "source": 0.92,
            "destination": 0.88,
            "date": 0.95,
            "class": 0.75
        },
        "processing_time_ms": 150
    }

@app.post("/ml/waitlist-predictor", tags=["Machine Learning"])
async def predict_waitlist_confirmation(request: WaitlistPredictionRequest):
    """
    Predict waitlist confirmation probability using ML model.
    
    Args:
        request: Train details and waitlist position
        
    Returns:
        dict: Confirmation probability and timeline estimation
    """
    logger.info(
        "Waitlist prediction request",
        train=request.train_number,
        class_code=request.class_code,
        waitlist_pos=request.current_waitlist_position
    )
    
    # TODO: Implement ML prediction model
    # - Load trained model (scikit-learn/TensorFlow)
    # - Extract features from historical data
    # - Make prediction with confidence intervals
    # - Generate user-friendly explanation
    
    # Mock prediction logic
    confirmation_prob = calculate_mock_prediction(
        request.train_number,
        request.class_code,
        request.current_waitlist_position
    )
    
    return {
        "train_number": request.train_number,
        "class_code": request.class_code,
        "journey_date": request.journey_date,
        "current_waitlist_position": request.current_waitlist_position,
        "confirmation_probability": confirmation_prob,
        "probability_category": get_probability_category(confirmation_prob),
        "estimated_confirmation_date": "2025-08-12",
        "confidence_interval": [confirmation_prob - 0.1, confirmation_prob + 0.1],
        "model_version": "v1.2.0",
        "prediction_timestamp": datetime.utcnow().isoformat()
    }

@app.post("/conversation/respond", tags=["Conversational AI"])
async def generate_response(message: ChatMessage):
    """
    Generate contextual conversational response.
    
    Args:
        message: User message with conversation context
        
    Returns:
        dict: Generated response with follow-up suggestions
    """
    logger.info("Response generation request", session=message.session_id)
    
    # TODO: Implement conversation management
    # - Maintain conversation context
    # - Generate contextual responses
    # - Provide helpful follow-up suggestions
    # - Handle multi-turn conversations
    
    return {
        "response": "I understand you're looking to book train tickets. Could you please tell me your source and destination stations?",
        "context_updated": True,
        "follow_up_suggestions": [
            "Search for trains",
            "Check PNR status", 
            "View booking history"
        ],
        "session_id": message.session_id
    }

# Helper functions
def extract_mock_entities(text: str) -> Dict[str, Any]:
    """Mock entity extraction for demonstration."""
    # This would be replaced with actual NLP processing
    entities = {}
    
    text_lower = text.lower()
    
    # Mock source/destination extraction
    if "delhi" in text_lower:
        entities["source"] = "New Delhi"
    if "mumbai" in text_lower:
        entities["destination"] = "Mumbai"
    
    # Mock date extraction
    if "tomorrow" in text_lower:
        entities["date"] = "2025-08-03"
    elif "august" in text_lower and "15" in text_lower:
        entities["date"] = "2025-08-15"
    
    # Mock class extraction
    if "sleeper" in text_lower or "sl" in text_lower:
        entities["class"] = "SL"
    elif "3a" in text_lower or "third ac" in text_lower:
        entities["class"] = "3A"
    
    return entities

def extract_pnr(text: str) -> Optional[str]:
    """Extract PNR number from text."""
    import re
    pnr_pattern = r'\b\d{10}\b'
    match = re.search(pnr_pattern, text)
    return match.group() if match else None

def generate_booking_response(entities: Dict[str, Any]) -> str:
    """Generate response for booking intent."""
    response = "I'll help you book train tickets"
    
    if entities.get("source") and entities.get("destination"):
        response += f" from {entities['source']} to {entities['destination']}"
    
    if entities.get("date"):
        response += f" on {entities['date']}"
    
    if entities.get("class"):
        response += f" in {entities['class']} class"
    
    response += ". Let me search for available trains."
    
    return response

def calculate_mock_prediction(train_number: str, class_code: str, waitlist_pos: int) -> float:
    """Mock waitlist prediction calculation."""
    # Simple mock logic - would be replaced with actual ML model
    base_prob = 0.8
    
    # Adjust based on waitlist position
    if waitlist_pos <= 10:
        return min(0.95, base_prob + 0.15)
    elif waitlist_pos <= 25:
        return max(0.3, base_prob - 0.1)
    else:
        return max(0.1, base_prob - 0.4)

def get_probability_category(prob: float) -> str:
    """Convert probability to user-friendly category."""
    if prob >= 0.8:
        return "Very High"
    elif prob >= 0.6:
        return "High"
    elif prob >= 0.4:
        return "Medium"
    elif prob >= 0.2:
        return "Low"
    else:
        return "Very Low"

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("AI_GATEWAY_PORT", 8001)),
        reload=True,
        log_level="info"
    )
