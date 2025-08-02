"""
NLP Service
===========

Natural Language Processing service for intent classification and entity extraction.
Uses strategy pattern for different NLP algorithms.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from ..services.base import BaseService
from ..core.config import get_settings, get_model_config


class NLPService(BaseService):
    """NLP service for intent classification and entity extraction."""
    
    def __init__(self):
        super().__init__()
        self.settings = get_settings()
        self.model_config = get_model_config()
        self._intent_patterns = self._load_intent_patterns()
        self._entity_patterns = self._load_entity_patterns()
    
    async def classify_intent(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Classify user intent from text.
        
        Args:
            text: User input text
            context: Additional context information
            
        Returns:
            Dict containing intent, confidence, and entities
        """
        self.logger.info("Classifying intent", text_length=len(text))
        
        text_lower = text.lower()
        best_intent = "general_inquiry"
        best_confidence = 0.5
        
        # Pattern-based intent classification (would be replaced with ML model)
        for intent, patterns in self._intent_patterns.items():
            confidence = self._calculate_pattern_confidence(text_lower, patterns)
            if confidence > best_confidence:
                best_intent = intent
                best_confidence = confidence
        
        # Extract entities
        entities = await self.extract_entities(text, context)
        
        # Generate contextual response
        response = self._generate_intent_response(best_intent, entities)
        
        # Create suggested actions
        actions = self._create_suggested_actions(best_intent, entities)
        
        return {
            "intent": best_intent,
            "confidence": best_confidence,
            "entities": entities,
            "response": response,
            "suggested_actions": actions
        }
    
    async def extract_entities(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Extract entities from text.
        
        Args:
            text: Input text
            context: Additional context
            
        Returns:
            Dict of extracted entities
        """
        self.logger.info("Extracting entities", text_length=len(text))
        
        entities = {}
        
        # Extract different entity types
        entities.update(self._extract_locations(text))
        entities.update(self._extract_dates(text))
        entities.update(self._extract_train_classes(text))
        entities.update(self._extract_numbers(text))
        entities.update(self._extract_pnr(text))
        
        return entities
    
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load intent classification patterns."""
        return {
            "book_ticket": [
                "book", "ticket", "train", "reservation", "reserve", "journey",
                "travel", "seat", "berth", "coach"
            ],
            "check_status": [
                "status", "pnr", "check", "confirm", "booking", "ticket status",
                "reservation status", "confirm ticket"
            ],
            "cancel_booking": [
                "cancel", "refund", "cancellation", "cancel ticket",
                "cancel booking", "refund ticket"
            ],
            "get_train_info": [
                "train", "schedule", "timing", "arrival", "departure",
                "train number", "route", "stops"
            ],
            "check_availability": [
                "availability", "available", "seats", "berths", "quota",
                "vacant", "waiting list", "confirm availability"
            ]
        }
    
    def _load_entity_patterns(self) -> Dict[str, str]:
        """Load entity extraction patterns."""
        return {
            "pnr": r'\b\d{10}\b',
            "train_number": r'\b\d{4,5}\b', 
            "phone": r'\b\d{10}\b',
            "date_dmy": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',
            "date_mdy": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
        }
    
    def _calculate_pattern_confidence(self, text: str, patterns: List[str]) -> float:
        """Calculate confidence score based on pattern matching."""
        matches = sum(1 for pattern in patterns if pattern in text)
        return min(0.95, 0.3 + (matches * 0.15))
    
    def _extract_locations(self, text: str) -> Dict[str, str]:
        """Extract source and destination locations."""
        # Major Indian cities and railway stations
        cities = {
            'delhi': 'New Delhi', 'mumbai': 'Mumbai', 'chennai': 'Chennai',
            'kolkata': 'Kolkata', 'bangalore': 'Bangalore', 'hyderabad': 'Hyderabad',
            'pune': 'Pune', 'ahmedabad': 'Ahmedabad', 'jaipur': 'Jaipur',
            'lucknow': 'Lucknow', 'kanpur': 'Kanpur', 'nagpur': 'Nagpur'
        }
        
        entities = {}
        text_lower = text.lower()
        
        found_cities = []
        for key, value in cities.items():
            if key in text_lower:
                found_cities.append(value)
        
        if len(found_cities) >= 2:
            entities['source_station'] = found_cities[0]
            entities['destination_station'] = found_cities[1]
        elif len(found_cities) == 1:
            entities['station'] = found_cities[0]
        
        return entities
    
    def _extract_dates(self, text: str) -> Dict[str, str]:
        """Extract journey dates."""
        entities = {}
        text_lower = text.lower()
        
        # Relative dates
        if 'today' in text_lower:
            entities['journey_date'] = datetime.now().strftime('%Y-%m-%d')
        elif 'tomorrow' in text_lower:
            entities['journey_date'] = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        elif 'day after tomorrow' in text_lower:
            entities['journey_date'] = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        
        # Pattern-based dates
        for pattern_name, pattern in self._entity_patterns.items():
            if 'date' in pattern_name:
                matches = re.findall(pattern, text)
                if matches:
                    entities['raw_date'] = matches[0]
        
        return entities
    
    def _extract_train_classes(self, text: str) -> Dict[str, str]:
        """Extract train class information."""
        class_mapping = {
            'sleeper': 'SL', 'sl': 'SL',
            '3ac': '3A', '3a': '3A', 'third ac': '3A',
            '2ac': '2A', '2a': '2A', 'second ac': '2A',
            '1ac': '1A', '1a': '1A', 'first ac': '1A',
            'cc': 'CC', 'chair car': 'CC',
            'ec': 'EC', 'executive': 'EC'
        }
        
        text_lower = text.lower()
        for key, value in class_mapping.items():
            if key in text_lower:
                return {'train_class': value}
        
        return {}
    
    def _extract_numbers(self, text: str) -> Dict[str, Any]:
        """Extract numerical entities like passenger count."""
        entities = {}
        
        # Passenger count
        passenger_patterns = [
            r'(\d+)\s+passenger', r'(\d+)\s+ticket', r'(\d+)\s+seat',
            r'(\d+)\s+person', r'for\s+(\d+)'
        ]
        
        for pattern in passenger_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                count = int(matches[0])
                if 1 <= count <= 6:  # Valid passenger count
                    entities['passenger_count'] = count
                break
        
        return entities
    
    def _extract_pnr(self, text: str) -> Dict[str, str]:
        """Extract PNR numbers."""
        pnr_matches = re.findall(self._entity_patterns['pnr'], text)
        if pnr_matches:
            return {'pnr_number': pnr_matches[0]}
        return {}
    
    def _generate_intent_response(self, intent: str, entities: Dict[str, Any]) -> str:
        """Generate contextual response based on intent and entities."""
        responses = {
            "book_ticket": self._generate_booking_response(entities),
            "check_status": "I'll help you check your booking status. Please provide your PNR number.",
            "cancel_booking": "I can help you cancel your booking. Please provide your PNR number.",
            "get_train_info": "I can provide train information. Please specify the train number or route.",
            "check_availability": "I'll check seat availability for you. Please provide the route and date.",
            "general_inquiry": "I'm here to help with your railway booking needs. What would you like to do?"
        }
        
        return responses.get(intent, responses["general_inquiry"])
    
    def _generate_booking_response(self, entities: Dict[str, Any]) -> str:
        """Generate booking-specific response."""
        response = "I'll help you book train tickets"
        
        if entities.get("source_station") and entities.get("destination_station"):
            response += f" from {entities['source_station']} to {entities['destination_station']}"
        
        if entities.get("journey_date"):
            response += f" on {entities['journey_date']}"
        
        if entities.get("train_class"):
            response += f" in {entities['train_class']} class"
        
        if entities.get("passenger_count"):
            count = entities['passenger_count']
            response += f" for {count} passenger{'s' if count > 1 else ''}"
        
        response += ". Let me search for available trains."
        return response
    
    def _create_suggested_actions(self, intent: str, entities: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create suggested follow-up actions."""
        actions = []
        
        if intent == "book_ticket":
            if entities.get("source_station") and entities.get("destination_station"):
                actions.append({
                    "action": "search_trains",
                    "parameters": {
                        "source": entities["source_station"],
                        "destination": entities["destination_station"],
                        "date": entities.get("journey_date")
                    }
                })
        elif intent == "check_status" and entities.get("pnr_number"):
            actions.append({
                "action": "get_pnr_status",
                "parameters": {"pnr": entities["pnr_number"]}
            })
        
        return actions
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process NLP request."""
        if "message" in data:
            return await self.classify_intent(data["message"], data.get("context"))
        elif "text" in data:
            entities = await self.extract_entities(data["text"], data.get("context"))
            return {"entities": entities}
        else:
            raise ValueError("Invalid input data")
