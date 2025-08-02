"""
Database models for the RailBooker application.
Defines SQLAlchemy models for all database tables.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Text, DECIMAL, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database.connection import Base


class State(Base):
    """Indian states and union territories."""
    __tablename__ = "states"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(5), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    cities = relationship("City", back_populates="state")


class City(Base):
    """Cities in India."""
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id"))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    is_major_city = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    state = relationship("State", back_populates="cities")
    stations = relationship("Station", back_populates="city")
    users = relationship("User", back_populates="city")


class Station(Base):
    """Railway stations."""
    __tablename__ = "stations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(10), nullable=False, unique=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    zone = Column(String(10))
    division = Column(String(50))
    is_junction = Column(Boolean, default=False)
    is_terminus = Column(Boolean, default=False)
    platform_count = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    city = relationship("City", back_populates="stations")
    trains_source = relationship("Train", foreign_keys="Train.source_station_id", back_populates="source_station")
    trains_destination = relationship("Train", foreign_keys="Train.destination_station_id", back_populates="destination_station")
    train_routes = relationship("TrainRoute", back_populates="station")
    bookings_source = relationship("Booking", foreign_keys="Booking.source_station_id", back_populates="source_station")
    bookings_destination = relationship("Booking", foreign_keys="Booking.destination_station_id", back_populates="destination_station")


class TrainClass(Base):
    """Train class definitions (1A, 2A, 3A, SL, etc.)."""
    __tablename__ = "train_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(5), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    is_ac = Column(Boolean, default=False)
    is_sleeper = Column(Boolean, default=False)
    comfort_level = Column(Integer, default=1)
    
    # Relationships
    train_configs = relationship("TrainClassConfig", back_populates="train_class")
    bookings = relationship("Booking", back_populates="train_class")
    predictions = relationship("BookingPrediction", back_populates="train_class")


class Train(Base):
    """Train information."""
    __tablename__ = "trains"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(200), nullable=False)
    type = Column(String(50))
    source_station_id = Column(Integer, ForeignKey("stations.id"))
    destination_station_id = Column(Integer, ForeignKey("stations.id"))
    total_distance = Column(Integer)
    running_days = Column(String(7))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    source_station = relationship("Station", foreign_keys=[source_station_id], back_populates="trains_source")
    destination_station = relationship("Station", foreign_keys=[destination_station_id], back_populates="trains_destination")
    class_configs = relationship("TrainClassConfig", back_populates="train")
    routes = relationship("TrainRoute", back_populates="train")
    bookings = relationship("Booking", back_populates="train")
    predictions = relationship("BookingPrediction", back_populates="train")


class TrainClassConfig(Base):
    """Train class configuration (seats, fare, etc.)."""
    __tablename__ = "train_class_config"
    
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    class_id = Column(Integer, ForeignKey("train_classes.id"))
    total_seats = Column(Integer, nullable=False)
    base_fare = Column(DECIMAL(10, 2))
    is_available = Column(Boolean, default=True)
    
    # Relationships
    train = relationship("Train", back_populates="class_configs")
    train_class = relationship("TrainClass", back_populates="train_configs")


class TrainRoute(Base):
    """Train route with station stops."""
    __tablename__ = "train_routes"
    
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    sequence_number = Column(Integer, nullable=False)
    arrival_time = Column(Time)
    departure_time = Column(Time)
    halt_duration = Column(Integer, default=0)
    distance_from_source = Column(Integer)
    platform_number = Column(String(10))
    is_technical_halt = Column(Boolean, default=False)
    
    # Relationships
    train = relationship("Train", back_populates="routes")
    station = relationship("Station", back_populates="train_routes")


class User(Base):
    """User accounts."""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(15), unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String(10))
    address = Column(Text)
    city_id = Column(Integer, ForeignKey("cities.id"))
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    city = relationship("City", back_populates="users")
    auth = relationship("UserAuth", back_populates="user", uselist=False)
    bookings = relationship("Booking", back_populates="user")
    queries = relationship("UserQuery", back_populates="user")


class UserAuth(Base):
    """User authentication details."""
    __tablename__ = "user_auth"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="auth")


class Booking(Base):
    """Booking records."""
    __tablename__ = "bookings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    pnr = Column(String(10), unique=True, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    train_id = Column(Integer, ForeignKey("trains.id"))
    class_id = Column(Integer, ForeignKey("train_classes.id"))
    source_station_id = Column(Integer, ForeignKey("stations.id"))
    destination_station_id = Column(Integer, ForeignKey("stations.id"))
    journey_date = Column(Date, nullable=False, index=True)
    booking_date = Column(DateTime, server_default=func.now())
    status = Column(String(20), default='PENDING')
    total_fare = Column(DECIMAL(12, 2))
    payment_status = Column(String(20), default='PENDING')
    quota = Column(String(20), default='GENERAL')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    train = relationship("Train", back_populates="bookings")
    train_class = relationship("TrainClass", back_populates="bookings")
    source_station = relationship("Station", foreign_keys=[source_station_id], back_populates="bookings_source")
    destination_station = relationship("Station", foreign_keys=[destination_station_id], back_populates="bookings_destination")
    passengers = relationship("Passenger", back_populates="booking")


class Passenger(Base):
    """Passenger details for bookings."""
    __tablename__ = "passengers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id", ondelete="CASCADE"))
    name = Column(String(200), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    seat_number = Column(String(10))
    berth_preference = Column(String(20))
    current_status = Column(String(20), default='WAITLISTED')
    waitlist_number = Column(Integer)
    rac_number = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    booking = relationship("Booking", back_populates="passengers")


class BookingPrediction(Base):
    """ML predictions for waitlist confirmation."""
    __tablename__ = "booking_predictions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    train_id = Column(Integer, ForeignKey("trains.id"))
    class_id = Column(Integer, ForeignKey("train_classes.id"))
    journey_date = Column(Date, nullable=False)
    quota = Column(String(20))
    current_waitlist_position = Column(Integer)
    confirmation_probability = Column(DECIMAL(5, 4))
    predicted_confirmation_date = Column(Date)
    model_version = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    train = relationship("Train", back_populates="predictions")
    train_class = relationship("TrainClass", back_populates="predictions")


class UserQuery(Base):
    """User AI queries and responses."""
    __tablename__ = "user_queries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    session_id = Column(String(100), index=True)
    query_text = Column(Text, nullable=False)
    intent = Column(String(50))
    extracted_entities = Column(JSONB)
    response_text = Column(Text)
    confidence_score = Column(DECIMAL(5, 4))
    is_successful = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="queries")
