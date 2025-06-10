"""
Database module initialization.
"""
import asyncio
import traceback
from pathlib import Path

from app.db.mongodb import mongodb
from app.db.postgres import create_db_and_tables
from app.utils.platform import get_app_dir, get_data_dir


def init_directories():
    """
    Initialize required directories for database files.
    """
    # Create data directories
    data_dir = get_data_dir()
    db_dir = data_dir / "db"
    db_dir.mkdir(exist_ok=True)
    
    # Create subdirectories for different databases
    postgres_dir = db_dir / "postgres"
    postgres_dir.mkdir(exist_ok=True)
    
    mongodb_dir = db_dir / "mongodb"
    mongodb_dir.mkdir(exist_ok=True)
    
    print(f"Database directories initialized at {db_dir}")
    return db_dir


def init_db():
    """
    Initialize database connections and create tables.
    """
    # Initialize directories
    init_directories()
    # Create PostgreSQL tables
    try:
        create_db_and_tables()
        print("PostgreSQL tables created successfully")
    except Exception as e:
        print(f"PostgreSQL connection error: {e}")
        print(f"Exception details: {traceback.format_exc()}")
        # Continue even if PostgreSQL is not available
    
    # Check MongoDB connection
    try:
        mongodb_client = mongodb.client
        # Await the async ping command
        asyncio.get_event_loop().run_until_complete(mongodb_client.admin.command('ping'))
        print("MongoDB connection successful")
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        print(f"Exception details: {traceback.format_exc()}")
        # Continue even if MongoDB is not available
