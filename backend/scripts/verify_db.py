"""Database verification script.

This script verifies that the database is properly set up and accessible.

Usage:
    python scripts/verify_db.py
"""

import asyncio
import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from dotenv import load_dotenv
from src.database import engine


async def verify_database():
    """Verify database connection and schema."""
    # Load environment variables
    load_dotenv()
    
    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL environment variable is not set!")
        return False
    
    print(f"Verifying database connection...")
    
    try:
        # Test connection
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            await result.fetchone()
        
        print("✓ Database connection successful")
        
        # Check if chat_messages table exists
        async with engine.connect() as conn:
            result = await conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'chat_messages'
                );
            """))
            table_exists = (await result.fetchone())[0]
        
        if table_exists:
            print("✓ chat_messages table exists")
            
            # Check table structure
            async with engine.connect() as conn:
                result = await conn.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'chat_messages'
                    ORDER BY ordinal_position;
                """))
                columns = await result.fetchall()
            
            print("\nTable structure:")
            print("-" * 60)
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                print(f"  {col[0]:<20} {col[1]:<30} {nullable}")
            
            # Check indexes
            async with engine.connect() as conn:
                result = await conn.execute(text("""
                    SELECT indexname, indexdef
                    FROM pg_indexes
                    WHERE tablename = 'chat_messages';
                """))
                indexes = await result.fetchall()
            
            print("\nIndexes:")
            print("-" * 60)
            for idx in indexes:
                print(f"  {idx[0]}")
            
            print("\n✓ Database verification complete!")
            return True
        else:
            print("✗ chat_messages table does not exist")
            print("  Run 'python scripts/init_db.py' to create the table")
            return False
            
    except Exception as e:
        print(f"✗ Error verifying database: {e}")
        return False
    finally:
        await engine.dispose()


def main():
    """Main entry point."""
    print("=" * 60)
    print("AI Portfolio - Database Verification")
    print("=" * 60)
    print()
    
    success = asyncio.run(verify_database())
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
