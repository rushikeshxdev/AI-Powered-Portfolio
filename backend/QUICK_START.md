# Backend Quick Start

## First Time Setup

**Option 1: Using Python directly**
```bash
cd backend
python setup_backend.py
```

**Option 2: Using convenience scripts**

Windows:
```cmd
cd backend
setup.bat
```

macOS/Linux:
```bash
cd backend
chmod +x setup.sh
./setup.sh
```

Follow the on-screen instructions!

---

## Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

---

## Common Commands

```bash
# Start development server
uvicorn src.main:app --reload

# Run tests
pytest

# Run health check
python check_backend.py

# Database migrations
alembic upgrade head

# Format code
black src/ tests/

# View API docs
# Visit: http://localhost:8000/docs
```

---

## Troubleshooting

**PowerShell execution policy error?**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Database connection error?**
- Check `.env` file exists
- Verify DATABASE_URL is correct
- Ensure PostgreSQL is running

**Module not found?**
- Activate virtual environment
- Run: `pip install -r requirements.txt`

---

For detailed instructions, see **SETUP_GUIDE.md**
