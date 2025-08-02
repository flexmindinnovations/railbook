"""
Logging Configuration
====================

Centralized logging setup using structlog for better observability.
"""

import structlog
from typing import Any, Dict


def setup_logging(log_level: str = "info") -> None:
    """Configure structured logging for the application."""
    
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if log_level == "debug" else structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> Any:
    """Get a configured logger instance."""
    return structlog.get_logger(name)
