#!/usr/bin/env python3
"""Database initialization script."""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent))

from database import create_tables, engine
from models.base import Base
from config import settings

def init_database():
    """Initialize the database with all tables."""
    print(f"Initializing database at: {settings.database_url}")
    
    try:
        # Create all tables
        print("Creating database tables...")
        create_tables()
        print("✅ Database tables created successfully!")
        
        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute("SHOW TABLES")
            tables = [row[0] for row in result]
            print(f"📋 Created tables: {', '.join(tables)}")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()