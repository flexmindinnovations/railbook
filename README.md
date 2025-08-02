# 🚂 RailBooker - AI-Powered Railway Booking System

## Overview

RailBooker is a modern, scalable railway ticket booking platform built with AI assistance. It provides intelligent booking recommendations, waitlist predictions, and natural language interaction for Indian Railway ticket booking.

## 🎯 Key Features

- **🤖 AI-Powered Booking Assistant** - Natural language booking interface
- **📊 Waitlist Prediction** - ML-based confirmation probability analysis
- **🔍 Smart Train Search** - Intelligent route recommendations
- **📱 Real-time Updates** - Live PNR status and notifications
- **🎨 Modern UI/UX** - Responsive design with intuitive interface
- **🔒 Secure Authentication** - JWT-based user management
- **⚡ High Performance** - Microservices architecture with caching

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Frontend     │    │   AI Gateway    │    │     Backend     │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (FastAPI)     │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │  Model Serving  │              │
         │              │   (ML Models)   │              │
         │              └─────────────────┘              │
         │                                               │
         └───────────────────────┬───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │    Database     │
                    │  (PostgreSQL)   │
                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop
- Git
- Node.js 18+ (for frontend development)
- Python 3.11+ (for local development)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/railbooker.git
cd railbooker
```

### 2. Setup Development Environment

**Windows:**
```cmd
setup-dev.bat
```

**Linux/macOS:**
```bash
chmod +x setup-dev.sh
./setup-dev.sh
```

### 3. Access Services

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **AI Gateway**: http://localhost:8001
- **AI Documentation**: http://localhost:8001/docs

## 📁 Project Structure

```
railbooker/
├── backend/                 # FastAPI backend service
│   ├── app/
│   │   ├── api/v1/         # API routes
│   │   ├── core/           # Configuration
│   │   ├── database/       # Models and DB connection
│   │   └── services/       # Business logic
│   ├── requirements.txt
│   └── Dockerfile
├── ai-gateway/             # AI/ML service
│   ├── models/             # ML models
│   ├── nlp/                # NLP processing
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React frontend (TBD)
├── database/               # Database schemas and migrations
├── model-serving/          # ML model serving
├── scheduler/              # Background jobs
├── infra/                  # Infrastructure as code
├── docs/                   # Documentation
└── docker-compose.yml      # Development environment
```

## 🛠️ Development Guide

### Backend Development

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run locally**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

3. **Database migrations** (TODO):
   ```bash
   alembic upgrade head
   ```

### AI Gateway Development

1. **Install dependencies**:
   ```bash
   cd ai-gateway
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. **Run locally**:
   ```bash
   uvicorn main:app --reload --port 8001
   ```

### API Testing

Use the interactive API documentation:
- Backend: http://localhost:8000/docs
- AI Gateway: http://localhost:8001/docs

## 📊 Database Schema

### Core Tables

- **stations** - Railway stations with codes and locations
- **trains** - Train information and schedules
- **users** - User accounts and profiles
- **bookings** - Ticket bookings and PNR records
- **passengers** - Passenger details for bookings
- **user_queries** - AI chat interactions
- **booking_predictions** - ML prediction results

### Key Relationships

```sql
users (1) ──── (n) bookings (1) ──── (n) passengers
bookings (n) ──── (1) trains
bookings (n) ──── (1) stations (source/destination)
```

## 🤖 AI Features

### Natural Language Processing

The AI Gateway provides several NLP capabilities:

1. **Intent Classification**
   - Book ticket
   - Check PNR status
   - Cancel booking
   - General inquiry

2. **Entity Extraction**
   - Source/destination stations
   - Journey dates
   - Class preferences
   - Passenger information

3. **Conversation Management**
   - Context-aware responses
   - Multi-turn conversations
   - Follow-up suggestions

### Machine Learning Models

1. **Waitlist Prediction Model**
   - Predicts confirmation probability
   - Based on historical booking data
   - Considers seasonal patterns

2. **Route Recommendation Engine**
   - Suggests alternative routes
   - Considers user preferences
   - Optimizes for time/cost

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### AI Gateway Tests
```bash
cd ai-gateway
pytest
```

### Integration Tests
```bash
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📈 Performance & Monitoring

### Metrics

- **Response Time**: < 2 seconds for API calls
- **Throughput**: 10,000+ concurrent users
- **Availability**: 99.9% uptime target

### Monitoring Stack (TODO)

- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **ELK Stack** - Logging and analytics

## 🚀 Deployment

### Production Deployment (TODO)

1. **Container Registry**:
   ```bash
   docker build -t railbooker/backend:latest backend/
   docker push railbooker/backend:latest
   ```

2. **Kubernetes Deployment**:
   ```bash
   kubectl apply -f infra/k8s/
   ```

3. **CI/CD Pipeline** - GitHub Actions

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Standards

- **Code Style**: Black (Python), Prettier (JavaScript)
- **Type Checking**: mypy (Python), TypeScript
- **Testing**: pytest (Python), Jest (JavaScript)
- **Documentation**: Follow existing patterns

## 📝 API Documentation

### Core Endpoints

#### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

#### Train Search
- `GET /api/v1/trains/search` - Search trains
- `GET /api/v1/trains/{train_number}` - Train details
- `GET /api/v1/trains/{train_number}/availability` - Check availability

#### Booking Management
- `POST /api/v1/bookings/create` - Create booking
- `GET /api/v1/bookings/pnr/{pnr}` - PNR status
- `POST /api/v1/bookings/{booking_id}/cancel` - Cancel booking

#### AI Assistant
- `POST /api/v1/ai/chat` - Process chat message
- `POST /api/v1/ai/extract-booking-info` - Extract booking data
- `POST /api/v1/ai/predict-waitlist` - Waitlist prediction

## 🎯 Roadmap

### Phase 1: Foundation ✅
- [x] Database schema design
- [x] Backend API structure
- [x] AI Gateway setup
- [x] Docker containerization

### Phase 2: Core Features (In Progress)
- [ ] User authentication system
- [ ] Train search implementation
- [ ] Basic booking functionality
- [ ] NLP processing pipeline

### Phase 3: AI Features
- [ ] Waitlist prediction model
- [ ] Route recommendation engine
- [ ] Conversational AI improvements
- [ ] Smart form auto-fill

### Phase 4: Frontend
- [ ] React application setup
- [ ] Chat interface
- [ ] Booking forms
- [ ] User dashboard

### Phase 5: Advanced Features
- [ ] Real-time notifications
- [ ] Payment integration
- [ ] Mobile app
- [ ] Performance optimization

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Solution Architect**: System design and architecture
- **Backend Developer**: API development and database design
- **AI Engineer**: ML models and NLP processing
- **Frontend Developer**: User interface and experience
- **DevOps Engineer**: Infrastructure and deployment

## 📞 Support

For support, email support@railbooker.com or join our [Discord community](https://discord.gg/railbooker).

---

**Built with ❤️ for Indian Railway travelers**
