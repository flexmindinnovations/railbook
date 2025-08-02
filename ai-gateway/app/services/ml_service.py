"""
ML Prediction Service
====================

Machine Learning service for waitlist prediction and other ML tasks.
Uses factory pattern for different ML models.
"""

from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from ..services.base import BaseService
from ..core.config import get_settings, get_model_config


class MLService(BaseService):
    """Machine Learning service for predictions."""
    
    def __init__(self):
        super().__init__()
        self.settings = get_settings()
        self.model_config = get_model_config()
        self._models = {}  # Would store loaded ML models
    
    async def predict_waitlist_confirmation(
        self, 
        train_number: str,
        class_code: str,
        journey_date: str,
        waitlist_position: int,
        quota: str = "GENERAL"
    ) -> Dict[str, Any]:
        """
        Predict waitlist confirmation probability.
        
        Args:
            train_number: 5-digit train number
            class_code: Class code (SL, 3A, 2A, etc.)
            journey_date: Journey date (YYYY-MM-DD)
            waitlist_position: Current waitlist position
            quota: Booking quota
            
        Returns:
            Dict with prediction results
        """
        self.logger.info(
            "Waitlist prediction request",
            train=train_number,
            class_code=class_code,
            waitlist_pos=waitlist_position
        )
        
        # Feature extraction
        features = self._extract_features(
            train_number, class_code, journey_date, waitlist_position, quota
        )
        
        # Make prediction (mock implementation)
        probability = self._calculate_confirmation_probability(features)
        
        # Generate confidence interval
        confidence_interval = self._calculate_confidence_interval(probability)
        
        # Estimate confirmation date
        estimated_date = self._estimate_confirmation_date(
            journey_date, probability, waitlist_position
        )
        
        return {
            "train_number": train_number,
            "class_code": class_code,
            "journey_date": journey_date,
            "current_waitlist_position": waitlist_position,
            "confirmation_probability": probability,
            "probability_category": self._get_probability_category(probability),
            "estimated_confirmation_date": estimated_date,
            "confidence_interval": confidence_interval,
            "ml_model_version": self.model_config.WAITLIST_MODEL_VERSION,
            "prediction_timestamp": datetime.utcnow().isoformat()
        }
    
    def _extract_features(
        self,
        train_number: str,
        class_code: str,
        journey_date: str,
        waitlist_position: int,
        quota: str
    ) -> Dict[str, Any]:
        """Extract features for ML model."""
        journey_dt = datetime.strptime(journey_date, '%Y-%m-%d')
        
        return {
            "train_number": int(train_number),
            "class_numeric": self._encode_class(class_code),
            "days_to_journey": (journey_dt - datetime.now()).days,
            "waitlist_position": waitlist_position,
            "quota_numeric": self._encode_quota(quota),
            "is_weekend": journey_dt.weekday() >= 5,
            "month": journey_dt.month,
            "day_of_week": journey_dt.weekday()
        }
    
    def _calculate_confirmation_probability(self, features: Dict[str, Any]) -> float:
        """
        Calculate confirmation probability using ML model.
        This is a mock implementation - would use actual trained model.
        """
        base_prob = 0.7
        
        # Adjust based on waitlist position
        position_factor = max(0.1, 1.0 - (features["waitlist_position"] * 0.02))
        
        # Adjust based on days to journey
        days_factor = min(1.2, 1.0 + (features["days_to_journey"] * 0.01))
        
        # Adjust based on class
        class_factors = {"SL": 1.1, "3A": 0.9, "2A": 0.8, "1A": 0.7}
        class_factor = class_factors.get(
            self._decode_class(features["class_numeric"]), 1.0
        )
        
        # Weekend penalty
        weekend_factor = 0.9 if features["is_weekend"] else 1.0
        
        probability = base_prob * position_factor * days_factor * class_factor * weekend_factor
        return max(0.05, min(0.95, probability))
    
    def _calculate_confidence_interval(self, probability: float) -> Tuple[float, float]:
        """Calculate 95% confidence interval."""
        margin = 0.1  # 10% margin of error
        lower = max(0.0, probability - margin)
        upper = min(1.0, probability + margin)
        return (lower, upper)
    
    def _estimate_confirmation_date(
        self, 
        journey_date: str, 
        probability: float, 
        waitlist_position: int
    ) -> Optional[str]:
        """Estimate when ticket might get confirmed."""
        if probability < 0.3:
            return None  # Unlikely to confirm
        
        journey_dt = datetime.strptime(journey_date, '%Y-%m-%d')
        
        # Estimate days before journey when confirmation might happen
        if probability > 0.8:
            days_before = min(15, waitlist_position // 2)
        elif probability > 0.6:
            days_before = min(10, waitlist_position // 3)
        else:
            days_before = min(5, waitlist_position // 5)
        
        estimated_dt = journey_dt - timedelta(days=days_before)
        
        # Don't predict past dates
        if estimated_dt < datetime.now():
            return None
        
        return estimated_dt.strftime('%Y-%m-%d')
    
    def _get_probability_category(self, probability: float) -> str:
        """Convert probability to user-friendly category."""
        if probability >= 0.8:
            return "Very High"
        elif probability >= 0.6:
            return "High"
        elif probability >= 0.4:
            return "Medium"
        elif probability >= 0.2:
            return "Low"
        else:
            return "Very Low"
    
    def _encode_class(self, class_code: str) -> int:
        """Encode class code to numeric value."""
        class_mapping = {"SL": 1, "3A": 2, "2A": 3, "1A": 4, "CC": 5, "EC": 6, "2S": 7}
        return class_mapping.get(class_code, 1)
    
    def _decode_class(self, class_numeric: int) -> str:
        """Decode numeric class to string."""
        class_mapping = {1: "SL", 2: "3A", 3: "2A", 4: "1A", 5: "CC", 6: "EC", 7: "2S"}
        return class_mapping.get(class_numeric, "SL")
    
    def _encode_quota(self, quota: str) -> int:
        """Encode quota to numeric value."""
        quota_mapping = {"GENERAL": 1, "LADIES": 2, "SENIOR_CITIZEN": 3, "TATKAL": 4}
        return quota_mapping.get(quota, 1)
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process ML prediction request."""
        if all(key in data for key in ["train_number", "class_code", "journey_date", "current_waitlist_position"]):
            return await self.predict_waitlist_confirmation(
                data["train_number"],
                data["class_code"],
                data["journey_date"],
                data["current_waitlist_position"],
                data.get("quota", "GENERAL")
            )
        else:
            raise ValueError("Missing required fields for waitlist prediction")
