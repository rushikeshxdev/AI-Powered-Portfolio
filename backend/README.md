# AI Portfolio Backend

Backend API for AI-powered portfolio website with RAG-based chat assistant.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Vector Store**: ChromaDB
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **LLM**: OpenRouter (meta-llama/llama-3.1-8b-instruct:free)
- **Server**: Uvicorn

## Project Structure

```
backend/
├── src/                    # Source code
│   ├── __init__.py
│   └── main.py            # FastAPI application entry point
├── tests/                 # Test files
│   └── __init__.py
├── data/                  # Data files (resume.json, etc.)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your configuration
# - Set DATABASE_URL to your PostgreSQL connection string
# - Set OPENROUTER_API_KEY from https://openrouter.ai/
# - Update ALLOWED_ORIGINS with your frontend URL
# - Generate SECRET_KEY using: openssl rand -hex 32
```

### 4. Run the Application

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python src/main.py
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. Verify Installation

```bash
# Check health endpoint
curl http://localhost:8000/api/health

# Expected response (when all services are healthy):
# {"status":"healthy","timestamp":"2024-01-01T00:00:00Z","services":{"database":true,"vector_store":true}}
```

## API Endpoints

### Current Endpoints

- `GET /` - Root endpoint with API information
- `GET /api/health` - Health check endpoint (checks database and vector store connectivity)

### Upcoming Endpoints

- `POST /api/chat` - Submit chat question and receive streaming response
- `GET /api/chat/history/{session_id}` - Retrieve chat history
- `DELETE /api/chat/history/{session_id}` - Clear chat history

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_example.py
```

### Code Quality

```bash
# Format code with black
black src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `OPENROUTER_API_KEY` | OpenRouter API key | Yes | - |
| `ALLOWED_ORIGINS` | Comma-separated CORS origins | Yes | localhost:5173 |
| `SECRET_KEY` | Secret key for security | Yes | - |
| `ENVIRONMENT` | Environment (development/production) | No | development |

## Next Steps

1. Set up database models and migrations (Task 1.2)
2. Create resume.json with portfolio data (Task 1.3)
3. Implement configuration management (Task 1.4)
4. Implement RAG system components (Tasks 2.x)
5. Implement chat endpoints (Tasks 4.x)

## License

Private project for portfolio demonstration.
