# Backend Setup Guide

This guide provides step-by-step instructions for setting up the backend development environment.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Setup (Automated)](#quick-setup-automated)
- [Manual Setup](#manual-setup)
- [Activating Virtual Environment](#activating-virtual-environment)
- [Installing Dependencies](#installing-dependencies)
- [Configuration](#configuration)
- [Running the Backend](#running-the-backend)
- [Running Tests](#running-tests)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **PostgreSQL** (for database) - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git** (for version control) - [Download Git](https://git-scm.com/downloads/)

### Verify Python Installation

Open a terminal and run:

```bash
python --version
```

or

```bash
python3 --version
```

You should see Python 3.8 or higher.

---

## Quick Setup (Automated)

We provide an automated setup script that handles everything for you:

```bash
cd backend
python setup_backend.py
```

The script will:
1. ✓ Check your Python version
2. ✓ Create a virtual environment
3. ✓ Provide activation instructions
4. ✓ Install all dependencies
5. ✓ Run health checks
6. ✓ Show you next steps

**Follow the on-screen instructions!**

---

## Manual Setup

If you prefer to set up manually or the automated script fails, follow these steps:

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
```

**Windows (CMD):**
```cmd
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment

See [Activating Virtual Environment](#activating-virtual-environment) section below.

### Step 4: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- FastAPI (web framework)
- SQLAlchemy (database ORM)
- ChromaDB (vector database)
- Sentence Transformers (embeddings)
- And many more...

### Step 6: Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and set your configuration:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
OPENROUTER_API_KEY=your_api_key_here
```

### Step 7: Run Health Check

```bash
python check_backend.py
```

This will verify:
- All required files exist
- Environment variables are set
- Python modules are installed
- Database connection works
- Source modules can be imported

---

## Activating Virtual Environment

You need to activate the virtual environment every time you open a new terminal.

### Windows

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**If you get an execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

**Command Prompt (CMD):**
```cmd
venv\Scripts\activate.bat
```

### macOS/Linux

```bash
source venv/bin/activate
```

### Verification

After activation, you should see `(venv)` at the beginning of your terminal prompt:

```
(venv) C:\path\to\backend>
```

or

```
(venv) user@machine:~/backend$
```

### Deactivating

To deactivate the virtual environment:

```bash
deactivate
```

---

## Installing Dependencies

After activating the virtual environment, install dependencies:

```bash
pip install -r requirements.txt
```

### What Gets Installed?

The `requirements.txt` includes:

**Core Framework:**
- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation

**Database:**
- `sqlalchemy` - ORM
- `asyncpg` - PostgreSQL driver
- `alembic` - Database migrations

**AI/ML:**
- `sentence-transformers` - Text embeddings
- `chromadb` - Vector database
- `httpx` - HTTP client for OpenRouter API

**Development:**
- `pytest` - Testing framework
- `black` - Code formatter
- `flake8` - Linter
- `mypy` - Type checker

---

## Configuration

### Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/portfolio_db

# OpenRouter API Configuration
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here

# Optional: Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# Optional: Logging
LOG_LEVEL=INFO
```

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:pass@localhost/db` |
| `OPENROUTER_API_KEY` | API key for OpenRouter | `sk-or-v1-...` |

### Database Setup

1. **Install PostgreSQL** if not already installed

2. **Create a database:**

```sql
CREATE DATABASE portfolio_db;
```

3. **Update DATABASE_URL** in `.env` with your credentials

4. **Run migrations:**

```bash
alembic upgrade head
```

---

## Running the Backend

### Development Server

Start the development server with auto-reload:

```bash
uvicorn src.main:app --reload
```

The server will start at: `http://localhost:8000`

### API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Production Server

For production, use:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Running Tests

### Run All Tests

```bash
pytest
```

or use the test runner script:

```bash
python run_tests.py
```

### Run Specific Tests

```bash
# Run a specific test file
pytest tests/test_chat.py

# Run a specific test function
pytest tests/test_chat.py::test_create_chat_message

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html
```

### Test Coverage

View coverage report:

```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

---

## Troubleshooting

### Common Issues

#### 1. Python Version Error

**Problem:** `Python 3.8+ is required`

**Solution:**
- Install Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
- Make sure to add Python to PATH during installation
- Verify with: `python --version`

#### 2. Virtual Environment Activation Error (Windows PowerShell)

**Problem:** `Execution policy error`

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 3. pip Not Found

**Problem:** `pip: command not found`

**Solution:**
- Make sure virtual environment is activated
- Try: `python -m pip install -r requirements.txt`

#### 4. Database Connection Error

**Problem:** `Database connection failed`

**Solution:**
- Verify PostgreSQL is running
- Check DATABASE_URL in `.env`
- Ensure database exists: `CREATE DATABASE portfolio_db;`
- Check credentials are correct

#### 5. Module Import Errors

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

#### 6. Port Already in Use

**Problem:** `Address already in use`

**Solution:**
- Use a different port: `uvicorn src.main:app --port 8001`
- Or kill the process using port 8000

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -ti:8000 | xargs kill -9
```

#### 7. ChromaDB/Vector Store Errors

**Problem:** `Vector store initialization failed`

**Solution:**
- This is often normal on first run
- Initialize the RAG system: See `INITIALIZATION_GUIDE.md`
- Check `chroma_data` directory permissions

#### 8. Alembic Migration Errors

**Problem:** `Can't locate revision identified by 'xyz'`

**Solution:**
```bash
# Reset migrations (WARNING: This will drop all tables)
alembic downgrade base
alembic upgrade head
```

#### 9. OpenRouter API Errors

**Problem:** `Invalid API key` or `401 Unauthorized`

**Solution:**
- Verify OPENROUTER_API_KEY in `.env`
- Get a valid API key from [OpenRouter](https://openrouter.ai/)
- Ensure no extra spaces in the key

#### 10. Slow Dependency Installation

**Problem:** Installation takes too long

**Solution:**
- Use a faster mirror: `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
- Or upgrade pip: `pip install --upgrade pip`

### Getting Help

If you encounter issues not covered here:

1. **Check the logs:** `logs/app.log`
2. **Run health check:** `python check_backend.py`
3. **Check documentation:**
   - `README.md` - Project overview
   - `DATABASE.md` - Database setup
   - `INITIALIZATION_GUIDE.md` - RAG system setup
4. **Search for error messages** in the codebase or online

---

## Additional Resources

### Useful Commands

```bash
# Health check
python check_backend.py

# Run tests
python run_tests.py

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/

# Database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1

# View logs
tail -f logs/app.log  # macOS/Linux
Get-Content logs/app.log -Wait  # Windows PowerShell
```

### Project Structure

```
backend/
├── src/                    # Source code
│   ├── main.py            # FastAPI application
│   ├── database.py        # Database configuration
│   ├── schemas.py         # Pydantic schemas
│   ├── models/            # SQLAlchemy models
│   ├── repositories/      # Data access layer
│   ├── services/          # Business logic
│   └── middleware/        # Custom middleware
├── tests/                 # Test files
├── alembic/              # Database migrations
├── data/                 # Data files (resume.json)
├── logs/                 # Application logs
├── venv/                 # Virtual environment (created)
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── .env.example         # Example environment file
└── setup_backend.py     # This setup script
```

### Development Workflow

1. **Activate virtual environment**
2. **Make code changes**
3. **Run tests:** `pytest`
4. **Format code:** `black .`
5. **Check types:** `mypy src/`
6. **Run server:** `uvicorn src.main:app --reload`
7. **Test endpoints:** Visit http://localhost:8000/docs

---

## Next Steps

After successful setup:

1. ✓ Review the API documentation at `/docs`
2. ✓ Initialize the RAG system (see `INITIALIZATION_GUIDE.md`)
3. ✓ Run database migrations: `alembic upgrade head`
4. ✓ Test the endpoints (see `ENDPOINT_TESTING.md`)
5. ✓ Start building features!

---

**Happy coding! 🚀**
