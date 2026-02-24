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

### Quick Setup (Recommended)

Run the automated setup script:

```bash
cd backend
python setup_backend.py
```

The script will:
- ✓ Check Python version (3.8+ required)
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Run health checks
- ✓ Provide next steps

**For detailed instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

**For quick reference, see [QUICK_START.md](QUICK_START.md)**

### Manual Setup

If you prefer manual setup:

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows PowerShell: `.\venv\Scripts\Activate.ps1`
   - Windows CMD: `venv\Scripts\activate.bat`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run health check:**
   ```bash
   python check_backend.py
   ```

### Running the Application

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload

# The API will be available at:
# - API: http://localhost:8000
# - Interactive docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
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

## Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Comprehensive setup instructions with troubleshooting
- **[QUICK_START.md](QUICK_START.md)** - Quick reference for common commands
- **[DATABASE.md](DATABASE.md)** - Database setup and migrations
- **[INITIALIZATION_GUIDE.md](INITIALIZATION_GUIDE.md)** - RAG system initialization
- **[ENDPOINT_TESTING.md](ENDPOINT_TESTING.md)** - API endpoint testing guide

## Next Steps

1. Set up database models and migrations (Task 1.2)
2. Create resume.json with portfolio data (Task 1.3)
3. Implement configuration management (Task 1.4)
4. Implement RAG system components (Tasks 2.x)
5. Implement chat endpoints (Tasks 4.x)

## License

Private project for portfolio demonstration.
