"""
Train search and information API endpoints.
Handles train search, route information, and availability.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
import structlog

from app.database.connection import get_db
from app.database.models import Train, Station, TrainRoute, TrainClass

router = APIRouter()
logger = structlog.get_logger()


@router.get("/search")
async def search_trains(
    source: str = Query(..., description="Source station code or name"),
    destination: str = Query(..., description="Destination station code or name"),
    journey_date: date = Query(..., description="Journey date (YYYY-MM-DD)"),
    class_preference: Optional[str] = Query(None, description="Preferred class (SL, 3A, 2A, 1A)"),
    db: Session = Depends(get_db)
):
    """
    Search for trains between source and destination.
    
    Args:
        source: Source station code or name
        destination: Destination station code or name  
        journey_date: Date of journey
        class_preference: Optional class preference
        db: Database session
        
    Returns:
        List[dict]: Available trains with schedule and fare information
    """
    logger.info(
        "Train search request",
        source=source,
        destination=destination,
        date=journey_date.isoformat()
    )
    
    # TODO: Implement train search logic
    # - Validate station codes/names
    # - Find trains running on specified route
    # - Check train availability for the date
    # - Calculate fare for different classes
    # - Return sorted results by departure time
    
    # Mock response for now
    return [
        {
            "train_number": "12345",
            "train_name": "Express Train",
            "source_station": {
                "code": "NDLS",
                "name": "New Delhi"
            },
            "destination_station": {
                "code": "CSTM", 
                "name": "Mumbai CST"
            },
            "departure_time": "08:30",
            "arrival_time": "20:45",
            "duration": "12h 15m",
            "running_days": "Daily",
            "classes": [
                {
                    "class_code": "SL",
                    "class_name": "Sleeper",
                    "available_seats": 45,
                    "waiting_list": 0,
                    "fare": 485.0,
                    "status": "AVAILABLE"
                },
                {
                    "class_code": "3A",
                    "class_name": "Third AC",
                    "available_seats": 12,
                    "waiting_list": 8,
                    "fare": 1275.0,
                    "status": "WAITING"
                }
            ]
        }
    ]


@router.get("/{train_number}")
async def get_train_details(
    train_number: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific train.
    
    Args:
        train_number: Train number
        db: Database session
        
    Returns:
        dict: Complete train information including route
    """
    logger.info("Train details request", train_number=train_number)
    
    # TODO: Implement train details logic
    # - Fetch train from database
    # - Get complete route with timings
    # - Get class configuration
    # - Return comprehensive train info
    
    return {
        "train_number": train_number,
        "train_name": "Sample Express",
        "type": "Express",
        "source": "New Delhi",
        "destination": "Mumbai Central", 
        "total_distance": 1384,
        "running_days": "Daily",
        "route": [
            {
                "sequence": 1,
                "station_code": "NDLS",
                "station_name": "New Delhi",
                "arrival_time": None,
                "departure_time": "08:30",
                "halt_duration": 0,
                "distance": 0
            },
            {
                "sequence": 2,
                "station_code": "JHS",
                "station_name": "Jhansi Junction",
                "arrival_time": "13:45",
                "departure_time": "13:50",
                "halt_duration": 5,
                "distance": 415
            }
        ],
        "classes": [
            {
                "class_code": "SL",
                "total_seats": 72,
                "base_fare": 485.0
            }
        ]
    }


@router.get("/{train_number}/availability")
async def check_availability(
    train_number: str,
    source: str,
    destination: str,
    journey_date: date,
    class_code: str,
    quota: str = "GENERAL",
    db: Session = Depends(get_db)
):
    """
    Check seat availability for specific train and class.
    
    Args:
        train_number: Train number
        source: Source station code
        destination: Destination station code
        journey_date: Journey date
        class_code: Class code (SL, 3A, etc.)
        quota: Booking quota (GENERAL, TATKAL, etc.)
        db: Database session
        
    Returns:
        dict: Availability status and waitlist information
    """
    logger.info(
        "Availability check",
        train_number=train_number,
        class_code=class_code,
        date=journey_date.isoformat()
    )
    
    # TODO: Implement availability check
    # - Validate train and route
    # - Check seat availability for date
    # - Get current waitlist status
    # - Calculate fare
    
    return {
        "train_number": train_number,
        "class_code": class_code,
        "available_seats": 23,
        "current_status": "AVAILABLE",
        "waitlist_count": 0,
        "rac_count": 0,
        "fare": {
            "base_fare": 485.0,
            "reservation_charges": 40.0,
            "total_fare": 525.0
        },
        "last_updated": datetime.utcnow().isoformat()
    }


@router.get("/stations/search")
async def search_stations(
    query: str = Query(..., min_length=2, description="Station name or code to search"),
    limit: int = Query(10, le=50, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Search for railway stations by name or code.
    
    Args:
        query: Search query (station name or code)
        limit: Maximum results to return
        db: Database session
        
    Returns:
        List[dict]: Matching stations
    """
    logger.info("Station search", query=query)
    
    # TODO: Implement station search
    # - Search by code or name
    # - Use fuzzy matching for names
    # - Return sorted by relevance
    
    return [
        {
            "code": "NDLS",
            "name": "New Delhi",
            "city": "New Delhi",
            "state": "Delhi",
            "zone": "NR",
            "is_junction": True
        },
        {
            "code": "CSTM",
            "name": "Mumbai CST",
            "city": "Mumbai",
            "state": "Maharashtra", 
            "zone": "CR",
            "is_terminus": True
        }
    ]
