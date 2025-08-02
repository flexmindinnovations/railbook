"""
API Routes for AI Gateway
=========================  

FastAPI route handlers following REST principles and dependency injection.
Separates HTTP layer from business logic.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from typing import Dict, Any

from ..models.requests import ChatMessage, EntityExtractionRequest, WaitlistPredictionRequest
from ..models.responses import (
    IntentResponse, EntityExtractionResponse, WaitlistPredictionResponse,
    ConversationResponse, HealthCheckResponse
)
from ..services.nlp_service import NLPService
from ..services.ml_service import MLService
from ..core.logging import get_logger

# Create router
router = APIRouter()
logger = get_logger(__name__)

# Dependency injection
def get_nlp_service() -> NLPService:
    """Get NLP service instance."""
    return NLPService()

def get_ml_service() -> MLService:
    """Get ML service instance."""
    return MLService()


@router.get("/", tags=["System"])
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


@router.get("/health", response_model=HealthCheckResponse, tags=["System"])
async def health_check():
    """Health check for AI services."""
    try:
        # TODO: Implement actual health checks
        # - Check ML model loading status
        # - Verify SpaCy model availability  
        # - Test database connections
        # - Validate external service connectivity
        
        return HealthCheckResponse(
            status="healthy",
            models_loaded=True,
            spacy_available=True,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error("AI Gateway health check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI services temporarily unavailable"
        )


@router.post("/nlp/intent", response_model=IntentResponse, tags=["Natural Language Processing"])
async def classify_intent(
    message: ChatMessage,
    nlp_service: NLPService = Depends(get_nlp_service)
):
    """
    Classify user intent from natural language message.
    
    Args:
        message: User message with context
        nlp_service: Injected NLP service
        
    Returns:
        IntentResponse: Classified intent with entities and response
    """
    try:
        logger.info("Intent classification request", message_length=len(message.message))
        
        result = await nlp_service.classify_intent(
            message.message, 
            message.context
        )
        
        return IntentResponse(**result)
        
    except Exception as e:
        logger.error("Intent classification failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Intent classification failed"
        )


@router.post("/nlp/entities", response_model=EntityExtractionResponse, tags=["Natural Language Processing"])
async def extract_entities(
    request: EntityExtractionRequest,
    nlp_service: NLPService = Depends(get_nlp_service)
):
    """
    Extract structured entities from natural language text.
    
    Args:
        request: Text and context for entity extraction
        nlp_service: Injected NLP service
        
    Returns:
        EntityExtractionResponse: Extracted entities with confidence scores
    """
    try:
        logger.info("Entity extraction request", text_length=len(request.text))
        
        start_time = datetime.utcnow()
        entities = await nlp_service.extract_entities(request.text, request.context)
        end_time = datetime.utcnow()
        
        processing_time = int((end_time - start_time).total_seconds() * 1000)
        
        # Generate confidence scores (mock implementation)
        confidence_scores = {
            entity: 0.85 + (hash(str(value)) % 15) / 100  # Mock confidence
            for entity, value in entities.items()
        }
        
        return EntityExtractionResponse(
            entities=entities,
            confidence_scores=confidence_scores,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error("Entity extraction failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Entity extraction failed"
        )


@router.post("/ml/waitlist-predictor", response_model=WaitlistPredictionResponse, tags=["Machine Learning"])
async def predict_waitlist_confirmation(
    request: WaitlistPredictionRequest,
    ml_service: MLService = Depends(get_ml_service)
):
    """
    Predict waitlist confirmation probability using ML model.
    
    Args:
        request: Train details and waitlist position
        ml_service: Injected ML service
        
    Returns:
        WaitlistPredictionResponse: Confirmation probability and timeline
    """
    try:
        logger.info(
            "Waitlist prediction request",
            train=request.train_number,
            class_code=request.class_code,
            waitlist_pos=request.current_waitlist_position
        )
        
        result = await ml_service.predict_waitlist_confirmation(
            request.train_number,
            request.class_code,
            request.journey_date,
            request.current_waitlist_position,
            request.quota
        )
        
        return WaitlistPredictionResponse(**result)
        
    except Exception as e:
        logger.error("Waitlist prediction failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Waitlist prediction failed"
        )


@router.post("/conversation/respond", response_model=ConversationResponse, tags=["Conversational AI"])
async def generate_response(
    message: ChatMessage,
    nlp_service: NLPService = Depends(get_nlp_service)
):
    """
    Generate contextual conversational response.
    
    Args:
        message: User message with conversation context
        nlp_service: Injected NLP service
        
    Returns:
        ConversationResponse: Generated response with follow-up suggestions
    """
    try:
        logger.info("Response generation request", session=message.session_id)
        
        # Classify intent first
        intent_result = await nlp_service.classify_intent(
            message.message,
            message.context
        )
        
        # Generate follow-up suggestions based on intent
        follow_up_suggestions = []
        if intent_result["intent"] == "book_ticket":
            follow_up_suggestions = [
                "Search for trains",
                "Check seat availability", 
                "View train schedule"
            ]
        elif intent_result["intent"] == "check_status":
            follow_up_suggestions = [
                "Enter PNR number",
                "Check another booking",
                "Get refund information"
            ]
        else:
            follow_up_suggestions = [
                "Book train tickets",
                "Check PNR status",
                "Get train information"
            ]
        
        return ConversationResponse(
            response=intent_result["response"],
            context_updated=True,
            follow_up_suggestions=follow_up_suggestions,
            session_id=message.session_id
        )
        
    except Exception as e:
        logger.error("Response generation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Response generation failed"
        )
