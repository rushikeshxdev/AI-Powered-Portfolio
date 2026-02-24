#!/usr/bin/env python3
"""
Backend health check script.

This script:
- Verifies all required files exist (resume.json, .env, etc.)
- Checks database connection
- Checks if all Python modules can be imported
- Provides a comprehensive health report
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple


def print_header(message: str) -> None:
    """Print a formatted header message."""
    print("\n" + "=" * 70)
    print(f"  {message}")
    print("=" * 70 + "\n")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"✗ {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"⚠ {message}")


def check_required_files() -> Tuple[bool, List[str]]:
    """Check if all required files exist."""
    print_header("Checking Required Files")
    
    backend_dir = Path(__file__).parent
    required_files = [
        "data/resume.json",
        ".env",
        "requirements.txt",
        "alembic.ini",
        "src/main.py",
        "src/database.py",
        "src/schemas.py",
    ]
    
    missing_files = []
    all_exist = True
    
    for file_path in required_files:
        full_path = backend_dir / file_path
        if full_path.exists():
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} - NOT FOUND")
            missing_files.append(file_path)
            all_exist = False
    
    return all_exist, missing_files


def check_environment_variables() -> Tuple[bool, List[str]]:
    """Check if required environment variables are set."""
    print_header("Checking Environment Variables")
    
    # Load .env file if it exists
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        print_success(f".env file found")
        # Try to load it
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            print_success("Environment variables loaded from .env")
        except ImportError:
            print_warning("python-dotenv not installed, cannot load .env file")
        except Exception as e:
            print_error(f"Failed to load .env file: {e}")
    else:
        print_error(".env file not found")
    
    required_vars = [
        "DATABASE_URL",
        "OPENROUTER_API_KEY",
    ]
    
    missing_vars = []
    all_set = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "KEY" in var or "SECRET" in var or "PASSWORD" in var:
                masked_value = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
                print_success(f"{var} = {masked_value}")
            else:
                print_success(f"{var} = {value[:50]}...")
        else:
            print_error(f"{var} - NOT SET")
            missing_vars.append(var)
            all_set = False
    
    return all_set, missing_vars


def check_python_modules() -> Tuple[bool, List[str]]:
    """Check if all required Python modules can be imported."""
    print_header("Checking Python Modules")
    
    required_modules = [
        ("fastapi", "FastAPI"),
        ("sqlalchemy", "SQLAlchemy"),
        ("pydantic", "Pydantic"),
        ("chromadb", "ChromaDB"),
        ("sentence_transformers", "Sentence Transformers"),
        ("httpx", "HTTPX"),
        ("slowapi", "SlowAPI"),
        ("alembic", "Alembic"),
        ("pytest", "Pytest"),
        ("dotenv", "python-dotenv"),
    ]
    
    missing_modules = []
    all_imported = True
    
    for module_name, display_name in required_modules:
        try:
            __import__(module_name)
            print_success(f"{display_name} ({module_name})")
        except ImportError:
            print_error(f"{display_name} ({module_name}) - NOT INSTALLED")
            missing_modules.append(module_name)
            all_imported = False
    
    return all_imported, missing_modules


def check_database_connection() -> bool:
    """Check if database connection works."""
    print_header("Checking Database Connection")
    
    try:
        # Import database module
        from src.database import engine
        from sqlalchemy import text
        import asyncio
        
        async def test_connection():
            """Test database connection."""
            async with engine.begin() as conn:
                result = await conn.execute(text("SELECT 1"))
                result.fetchone()
        
        # Run async test
        asyncio.run(test_connection())
        print_success("Database connection successful")
        return True
        
    except ImportError as e:
        print_error(f"Failed to import database module: {e}")
        return False
    except Exception as e:
        print_error(f"Database connection failed: {e}")
        print("  Make sure DATABASE_URL is set correctly in .env")
        print("  Make sure the database server is running")
        return False


def check_vector_store() -> bool:
    """Check if vector store (ChromaDB) is accessible."""
    print_header("Checking Vector Store")
    
    try:
        from src.services.vector_store import VectorStore
        
        # Try to initialize vector store
        vector_store = VectorStore(persist_directory="/app/chroma_data")
        count = vector_store.get_collection_count()
        
        print_success(f"Vector store accessible (collection count: {count})")
        return True
        
    except ImportError as e:
        print_error(f"Failed to import vector store module: {e}")
        return False
    except Exception as e:
        print_error(f"Vector store check failed: {e}")
        print("  This might be normal if the RAG system hasn't been initialized yet")
        return False


def check_src_modules() -> Tuple[bool, List[str]]:
    """Check if all src modules can be imported."""
    print_header("Checking Source Modules")
    
    src_modules = [
        "src.main",
        "src.database",
        "src.schemas",
        "src.models.chat_message",
        "src.repositories.chat_repository",
        "src.services.embedding_service",
        "src.services.vector_store",
        "src.services.openrouter_client",
        "src.services.rag_engine",
        "src.middleware.security_headers",
        "src.middleware.request_id",
    ]
    
    failed_modules = []
    all_imported = True
    
    for module_name in src_modules:
        try:
            __import__(module_name)
            print_success(f"{module_name}")
        except ImportError as e:
            print_error(f"{module_name} - FAILED: {e}")
            failed_modules.append(module_name)
            all_imported = False
        except Exception as e:
            print_warning(f"{module_name} - WARNING: {e}")
    
    return all_imported, failed_modules


def main() -> int:
    """Main entry point."""
    print("\n" + "=" * 70)
    print("  Backend Health Check")
    print("=" * 70)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Add backend directory to Python path
    sys.path.insert(0, str(backend_dir))
    
    # Track overall health
    all_checks_passed = True
    critical_failures = []
    
    # Check required files
    files_ok, missing_files = check_required_files()
    if not files_ok:
        all_checks_passed = False
        critical_failures.append(f"Missing files: {', '.join(missing_files)}")
    
    # Check environment variables
    env_ok, missing_vars = check_environment_variables()
    if not env_ok:
        all_checks_passed = False
        critical_failures.append(f"Missing environment variables: {', '.join(missing_vars)}")
    
    # Check Python modules
    modules_ok, missing_modules = check_python_modules()
    if not modules_ok:
        all_checks_passed = False
        critical_failures.append(f"Missing Python modules: {', '.join(missing_modules)}")
    
    # Only check these if basic requirements are met
    if files_ok and env_ok and modules_ok:
        # Check source modules
        src_ok, failed_src = check_src_modules()
        if not src_ok:
            all_checks_passed = False
            critical_failures.append(f"Failed source modules: {', '.join(failed_src)}")
        
        # Check database connection
        db_ok = check_database_connection()
        if not db_ok:
            all_checks_passed = False
            critical_failures.append("Database connection failed")
        
        # Check vector store (non-critical)
        vector_ok = check_vector_store()
        if not vector_ok:
            print_warning("Vector store check failed (this may be normal if not initialized)")
    
    # Print summary
    print_header("Health Check Summary")
    
    if all_checks_passed:
        print_success("All critical checks passed!")
        print("\nThe backend is ready to run.")
        print("To start the server: uvicorn src.main:app --reload")
        return 0
    else:
        print_error("Some checks failed!")
        print("\nCritical failures:")
        for failure in critical_failures:
            print(f"  - {failure}")
        print("\nPlease fix the issues above before running the backend.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
