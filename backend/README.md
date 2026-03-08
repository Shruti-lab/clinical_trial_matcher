# Clinical Trial Matcher - Backend

AI-powered platform for matching patients with clinical trials in India.

## Quick Start

### Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

### Run

**Development server:**
```bash
uvicorn src.main:app --reload
```

**Run tests:**
```bash
pytest
```

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── src/              # Application source code
│   ├── api/          # API endpoints
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   ├── utils/        # Utilities
│   ├── config.py     # Configuration
│   └── main.py       # App entry point
├── tests/            # Test suite
├── docs/             # Documentation
└── requirements.txt  # Dependencies
```

## Requirements

- Python 3.11+
- MySQL 8.0+
- Redis 6+
- AWS account

## Documentation

See [docs/README.md](docs/README.md) for detailed documentation.

## License

Proprietary - AI for Bharat Hackathon Project
