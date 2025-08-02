-- RailBooker Database Schema
-- Comprehensive schema for Indian Railway Booking System

-- Core Geographic and Infrastructure Tables
CREATE TABLE states (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(5) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state_id INTEGER REFERENCES states(id),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_major_city BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(10) NOT NULL UNIQUE,
    city_id INTEGER REFERENCES cities(id),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    zone VARCHAR(10), -- Railway zone (WR, CR, NR, etc.)
    division VARCHAR(50),
    is_junction BOOLEAN DEFAULT FALSE,
    is_terminus BOOLEAN DEFAULT FALSE,
    platform_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Train Information Tables
CREATE TABLE trains (
    id SERIAL PRIMARY KEY,
    number VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50), -- Express, Superfast, Local, etc.
    source_station_id INTEGER REFERENCES stations(id),
    destination_station_id INTEGER REFERENCES stations(id),
    total_distance INTEGER, -- in kilometers
    running_days VARCHAR(7), -- SMTWTFS format
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE train_classes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(5) NOT NULL, -- 1A, 2A, 3A, SL, CC, 2S, etc.
    name VARCHAR(50) NOT NULL,
    description TEXT,
    is_ac BOOLEAN DEFAULT FALSE,
    is_sleeper BOOLEAN DEFAULT FALSE,
    comfort_level INTEGER DEFAULT 1 -- 1-5 scale
);

CREATE TABLE train_class_config (
    id SERIAL PRIMARY KEY,
    train_id INTEGER REFERENCES trains(id),
    class_id INTEGER REFERENCES train_classes(id),
    total_seats INTEGER NOT NULL,
    base_fare DECIMAL(10, 2),
    is_available BOOLEAN DEFAULT TRUE,
    UNIQUE(train_id, class_id)
);

-- Route and Schedule Tables
CREATE TABLE train_routes (
    id SERIAL PRIMARY KEY,
    train_id INTEGER REFERENCES trains(id),
    station_id INTEGER REFERENCES stations(id),
    sequence_number INTEGER NOT NULL,
    arrival_time TIME,
    departure_time TIME,
    halt_duration INTEGER DEFAULT 0, -- in minutes
    distance_from_source INTEGER, -- cumulative distance
    platform_number VARCHAR(10),
    is_technical_halt BOOLEAN DEFAULT FALSE,
    UNIQUE(train_id, sequence_number),
    UNIQUE(train_id, station_id)
);

-- Booking and User Management Tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    address TEXT,
    city_id INTEGER REFERENCES cities(id),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_auth (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Booking System Tables
CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pnr VARCHAR(10) UNIQUE NOT NULL,
    user_id UUID REFERENCES users(id),
    train_id INTEGER REFERENCES trains(id),
    class_id INTEGER REFERENCES train_classes(id),
    source_station_id INTEGER REFERENCES stations(id),
    destination_station_id INTEGER REFERENCES stations(id),
    journey_date DATE NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'PENDING', -- CONFIRMED, WAITLISTED, CANCELLED, RAC
    total_fare DECIMAL(12, 2),
    payment_status VARCHAR(20) DEFAULT 'PENDING',
    quota VARCHAR(20) DEFAULT 'GENERAL', -- GENERAL, TATKAL, PREMIUM_TATKAL, LADIES, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE passengers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID REFERENCES bookings(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL,
    seat_number VARCHAR(10),
    berth_preference VARCHAR(20), -- LOWER, MIDDLE, UPPER, SIDE_LOWER, SIDE_UPPER
    current_status VARCHAR(20) DEFAULT 'WAITLISTED', -- CONFIRMED, WAITLISTED, RAC, CANCELLED
    waitlist_number INTEGER,
    rac_number INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI and ML Support Tables
CREATE TABLE booking_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    train_id INTEGER REFERENCES trains(id),
    class_id INTEGER REFERENCES train_classes(id),
    journey_date DATE NOT NULL,
    quota VARCHAR(20),
    current_waitlist_position INTEGER,
    confirmation_probability DECIMAL(5, 4), -- 0.0000 to 1.0000
    predicted_confirmation_date DATE,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(train_id, class_id, journey_date, quota, current_waitlist_position)
);

CREATE TABLE user_queries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    session_id VARCHAR(100),
    query_text TEXT NOT NULL,
    intent VARCHAR(50), -- book_ticket, check_status, get_alternatives, etc.
    extracted_entities JSONB, -- {source, destination, date, class, etc.}
    response_text TEXT,
    confidence_score DECIMAL(5, 4),
    is_successful BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Historical Data for ML Training
CREATE TABLE historical_bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    original_booking_id UUID,
    train_id INTEGER,
    class_id INTEGER,
    journey_date DATE,
    booking_date TIMESTAMP,
    initial_status VARCHAR(20),
    final_status VARCHAR(20),
    waitlist_movement JSONB, -- Track waitlist position changes
    confirmation_date TIMESTAMP,
    cancellation_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Performance
CREATE INDEX idx_stations_code ON stations(code);
CREATE INDEX idx_trains_number ON trains(number);
CREATE INDEX idx_bookings_pnr ON bookings(pnr);
CREATE INDEX idx_bookings_user_id ON bookings(user_id);
CREATE INDEX idx_bookings_journey_date ON bookings(journey_date);
CREATE INDEX idx_train_routes_train_station ON train_routes(train_id, station_id);
CREATE INDEX idx_user_queries_session ON user_queries(session_id);
CREATE INDEX idx_booking_predictions_lookup ON booking_predictions(train_id, class_id, journey_date);

-- Insert Basic Data
INSERT INTO train_classes (code, name, description, is_ac, is_sleeper, comfort_level) VALUES
('1A', 'First AC', 'First Class Air Conditioned', TRUE, TRUE, 5),
('2A', 'Second AC', 'Second Class Air Conditioned', TRUE, TRUE, 4),
('3A', 'Third AC', 'Third Class Air Conditioned', TRUE, TRUE, 3),
('SL', 'Sleeper', 'Sleeper Class', FALSE, TRUE, 2),
('CC', 'Chair Car', 'Chair Car AC', TRUE, FALSE, 3),
('2S', 'Second Sitting', 'Second Class Sitting', FALSE, FALSE, 1),
('GEN', 'General', 'General Unreserved', FALSE, FALSE, 1);
