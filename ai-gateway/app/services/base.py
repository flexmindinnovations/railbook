"""
Base Service Class
==================

Abstract base class for all service implementations.
Follows dependency injection and strategy patterns.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..core.logging import get_logger


class BaseService(ABC):
    """Abstract base service class."""
    
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
    
    @abstractmethod
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results."""
        pass
    
    def validate_input(self, data: Dict[str, Any], required_fields: list) -> bool:
        """Validate input data has required fields."""
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            self.logger.error("Missing required fields", missing=missing_fields)
            return False
        return True
