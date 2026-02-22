"""Database initialization script.

This script initializes the database by running Alembic migrations.
It should be run once when setting up a new environment.

Usage:
    python scripts/init_db.py
"""

import asyncio
import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from alembic.config import Config
from alembic import command
from dotenv import load_dotenv


async def init_database():
    """Initialize the database by running migrations."""
    # Load environment variables
    load_dotenv()
    
    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL environment variable is not set!")
        print("Please set it in your .env file or environment.")
        sys.exit(1)
    
    print(f"Initializing database...")
    print(f"Database URL: {database_url.split('@')[1] if '@' in database_url else 'localhost'}")
    
    try:
        # Create Alembic configuration
        alembic_cfg = Config(str(backend_dir / "alembic.ini"))
        alembic_cfg.set_main_option("script_location", str(backend_dir / "alembic"))
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)
        
        # Run migrations to head
        print("\nRunning migrations...")
        command.upgrade(alembic_cfg, "head")
        
        print("\n✓ Database initialized successfully!")
        print("✓ All migrations applied.")
        
    except Exception as e:
        print(f"\n✗ Error initializing database: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    print("=" * 60)
    print("AI Portfolio - Database Initialization")
    print("=" * 60)
    print()
    
    asyncio.run(init_database())


if __name__ == "__main__":
    main()
