# TrialMatch AI - Clinical Trial Matcher

> AI-powered platform that automatically matches patients with relevant clinical trials in India by analyzing medical records and comparing them against active trials from CTRI (Clinical Trials Registry India).

## 🎯 Project Overview

**Problem:** Healthcare & Life Sciences - AI solution that improves efficiency and support within healthcare ecosystems  
**Target:** AI for Bharat Hackathon  
**Goal:** Reduce trial discovery time from months to minutes and increase trial enrollment rates by 50%

### Key Features

- 📄 **Medical Document Processing** - Upload and analyze medical reports (PDF/images) using AI
- 🔍 **Intelligent Matching** - AI-powered matching algorithm with 0-100% confidence scores
- 🌍 **Multilingual Support** - Support for Hindi, Tamil, Telugu, Bengali, Marathi
- 📍 **Location-Based Search** - Find trials near patient location
- 🔒 **HIPAA-Compliant** - Secure handling of medical data

## 🏗️ Architecture

**Serverless Microservices Architecture** using AWS services:

```
┌─────────────┐
│   Client    │ (React Web App)
└──────┬──────┘
       │
┌──────▼──────┐
│ API Gateway │
└──────┬──────┘
       │
┌──────▼──────────────────────────┐
│   Lambda Functions (Python)     │
│  - Auth Service                  │
│  - Upload Service                │
│  - Matching Service              │
│  - Search Service                │
└──────┬──────────────────────────┘
       │
┌──────▼──────────────────────────┐
│   AWS AI/ML Services             │
│  - Textract (OCR)                │
│  - Comprehend Medical (NER)      │
│  - Translate (i18n)              │
│  - Bedrock (Explanations)        │
└──────────────────────────────────┘
       │
┌──────▼──────────────────────────┐
│   Data Layer                     │
│  - MySQL RDS (User/Trials)      │
│  - S3 (Documents)                │
│  - OpenSearch (Trial Search)     │
│  - Redis (Cache)                 │
└──────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Docker** and Docker Compose
- **AWS Account** (for production) or LocalStack (for development)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd clinical-trial-matcher

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 2. Start Development Services

```bash
# Start all services (MySQL, Redis, LocalStack, OpenSearch)
docker-compose up -d

# Wait for services to be ready (check health status)
docker-compose ps
```

### 3. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations (when implemented)
# alembic upgrade head

# Start development server
uvicorn src.main:app --reload
```

Backend will be available at: http://localhost:8000

### 4. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:5173

## 🐳 Docker Services

The development environment includes the following services:

| Service | Port | Description |
|---------|------|-------------|
| **MySQL** | 3306 | Primary database for users, trials, matches |
| **Redis** | 6379 | Caching layer for performance |
| **LocalStack** | 4566 | AWS services emulation (S3, Textract, etc.) |
| **OpenSearch** | 9200 | Full-text search for clinical trials |
| **OpenSearch Dashboards** | 5601 | Search analytics (debug profile only) |

### Service Management

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f [service-name]

# Stop all services
docker-compose down

# Reset all data
docker-compose down -v
```

### Health Checks

```bash
# Check service status
docker-compose ps

# Test individual services
curl http://localhost:3306  # MySQL (will show connection error - normal)
curl http://localhost:6379  # Redis (will show connection error - normal)
curl http://localhost:4566/_localstack/health  # LocalStack
curl http://localhost:9200/_cluster/health  # OpenSearch
```

## 📁 Project Structure

```
clinical-trial-matcher/
├── backend/                 # Python FastAPI backend
│   ├── src/                # Application source code
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Database models (SQLAlchemy)
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Utilities
│   │   ├── config.py       # Configuration
│   │   └── main.py         # FastAPI app entry point
│   ├── tests/              # Backend tests
│   ├── docs/               # Backend documentation
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Backend environment template
├── frontend/               # React TypeScript frontend
│   ├── src/                # Application source code
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── stores/         # Zustand state management
│   │   └── utils/          # Frontend utilities
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   └── .env.example        # Frontend environment template
├── docker/                 # Docker configuration
│   ├── mysql/              # MySQL initialization scripts
│   └── localstack/         # LocalStack AWS setup
├── .kiro/                  # Project specifications
│   └── specs/              # Requirements, design, tasks
├── docker-compose.yml      # Development services
└── README.md               # This file
```

## 🔧 Configuration

### Backend Environment Variables

Key variables in `backend/.env`:

```bash
# Database (MySQL)
DATABASE_URL=mysql://user:password@localhost:3306/trialmatch

# AWS Services (LocalStack for development)
AWS_REGION=ap-south-1
LOCALSTACK_ENDPOINT=http://localhost:4566
USE_LOCALSTACK=true

# Security
SECRET_KEY=your-secret-key-change-in-production-min-32-chars

# File Upload
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_TYPES=pdf,jpg,jpeg,png
```

### Frontend Environment Variables

Key variables in `frontend/.env`:

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/v1

# Features
VITE_ENABLE_MULTILINGUAL=true
VITE_SUPPORTED_LANGUAGES=en,hi,ta,te,bn,mr

# Upload Configuration
VITE_MAX_FILE_SIZE_MB=10
VITE_ALLOWED_FILE_TYPES=pdf,jpg,jpeg,png
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest tests/test_auth.py  # Run specific test file
```

### Frontend Tests

```bash
cd frontend
npm test                  # Run tests
npm run test:coverage     # Run with coverage
```

## 📚 API Documentation

Once the backend is running, API documentation is available at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🌐 Multilingual Support

The platform supports 5 Indian languages:

- **English** (en) - Default
- **Hindi** (hi) - हिंदी
- **Tamil** (ta) - தமிழ்
- **Telugu** (te) - తెలుగు
- **Bengali** (bn) - বাংলা
- **Marathi** (mr) - मराठी

## 🔒 Security Features

- **Authentication:** JWT-based with secure password hashing
- **Data Encryption:** TLS in transit, AES-256 at rest
- **Privacy:** HIPAA-compliant data handling
- **Rate Limiting:** 100 requests/minute per user
- **Input Validation:** Comprehensive sanitization

## 📊 Performance Targets

- **API Response Time:** <3 seconds for search
- **Document Processing:** <30 seconds per document
- **Concurrent Users:** 100 users (MVP), 10,000 users (Phase 2)
- **Uptime:** 99.5%

## 🚀 Deployment

### Development
- Local development with Docker Compose
- LocalStack for AWS service emulation

### Production (AWS)
- **Compute:** AWS Lambda (serverless)
- **Database:** RDS MySQL with encryption
- **Storage:** S3 with encryption at rest
- **Search:** Amazon OpenSearch
- **Cache:** ElastiCache Redis
- **AI/ML:** Textract, Comprehend Medical, Bedrock

## 📈 Success Metrics

### MVP Success Criteria
- ✅ 50+ synthetic trials in database
- ✅ 90% accuracy in medical entity extraction
- ✅ <5 second search response time
- ✅ 5 supported languages
- ✅ Successful demo with 10 test cases

### Post-Launch Metrics
- 1,000 users in first 3 months
- 70% user satisfaction score
- 30% conversion to trial inquiry
- 50% reduction in trial discovery time

## 🤝 Contributing

1. Follow the existing code structure
2. Write tests for new features
3. Update documentation
4. Follow security best practices
5. Test with multiple languages

## 📄 License

Proprietary - AI for Bharat Hackathon Project

## 🆘 Troubleshooting

### Common Issues

**Docker services not starting:**
```bash
# Check Docker is running
docker --version
docker-compose --version

# Reset Docker state
docker-compose down -v
docker system prune -f
docker-compose up -d
```

**Backend connection errors:**
```bash
# Check environment variables
cat backend/.env

# Verify database connection
docker-compose logs mysql

# Test LocalStack
curl http://localhost:4566/_localstack/health
```

**Frontend build errors:**
```bash
# Clear node modules
rm -rf frontend/node_modules
cd frontend && npm install

# Check environment
cat frontend/.env
```

### Getting Help

1. Check the logs: `docker-compose logs -f [service]`
2. Verify environment variables are set correctly
3. Ensure all services are healthy: `docker-compose ps`
4. Review the troubleshooting section in individual README files

---

**Built with ❤️ for AI for Bharat Hackathon**