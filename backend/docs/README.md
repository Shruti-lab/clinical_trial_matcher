# Clinical Trial Matcher - Backend Documentation

## Overview

This is the backend service for the Clinical Trial Matcher platform, an AI-powered solution for matching patients with relevant clinical trials in India.

## Technology Stack

- **Framework:** FastAPI
- **Database:** MySQL with SQLAlchemy ORM
- **Cloud Services:** AWS (S3, Textract, Comprehend Medical, Bedrock)
- **Caching:** Redis
- **Testing:** pytest

## Project Structure

```
backend/
├── src/
│   ├── api/          # API route handlers
│   ├── models/       # SQLAlchemy database models
│   ├── schemas/      # Pydantic schemas for validation
│   ├── services/     # Business logic services
│   ├── utils/        # Utility functions
│   ├── config.py     # Application configuration
│   └── main.py       # FastAPI application entry point
├── tests/            # Test suite
├── docs/             # Documentation
└── requirements.txt  # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- MySQL 8.0+
- Redis 6+
- AWS account with appropriate credentials

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
alembic upgrade head
```

### Running the Application

Development server:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`

### Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

## API Endpoints

See the [API Documentation](http://localhost:8000/docs) for detailed endpoint information.

## Development Guidelines

- Follow PEP 8 style guide
- Use type hints for all functions
- Write tests for all new features
- Keep functions small and focused
- Document complex logic with comments

## License

Proprietary - AI for Bharat Hackathon Project
