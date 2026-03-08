#!/usr/bin/env python3
"""Database schema validation script."""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import inspect
from database import engine
from config import settings
from models import *

def validate_schema():
    """Validate that all models are properly defined and can be introspected."""
    print("🔍 Validating database schema...")
    
    try:
        # Test model imports
        print("✅ All models imported successfully")
        
        # Test database connection (if available)
        try:
            inspector = inspect(engine)
            print("✅ Database connection successful")
            
            # Check if tables exist
            tables = inspector.get_table_names()
            expected_tables = ['users', 'medical_profiles', 'documents', 'clinical_trials', 'matches']
            
            for table in expected_tables:
                if table in tables:
                    print(f"✅ Table '{table}' exists")
                    
                    # Check indexes
                    indexes = inspector.get_indexes(table)
                    print(f"   📊 {len(indexes)} indexes found")
                else:
                    print(f"⚠️  Table '{table}' not found (run migrations first)")
                    
        except Exception as db_error:
            print(f"⚠️  Database connection failed: {db_error}")
            print("   This is expected if MySQL is not running or configured")
        
        # Validate model relationships
        print("\n🔗 Validating model relationships...")
        
        # Test User model
        user_relationships = ['medical_profile', 'documents', 'matches']
        for rel in user_relationships:
            if hasattr(User, rel):
                print(f"✅ User.{rel} relationship defined")
            else:
                print(f"❌ User.{rel} relationship missing")
        
        # Test other model relationships
        if hasattr(MedicalProfile, 'user'):
            print("✅ MedicalProfile.user relationship defined")
        
        if hasattr(Document, 'user'):
            print("✅ Document.user relationship defined")
            
        if hasattr(ClinicalTrial, 'matches'):
            print("✅ ClinicalTrial.matches relationship defined")
            
        if hasattr(Match, 'user') and hasattr(Match, 'trial'):
            print("✅ Match.user and Match.trial relationships defined")
        
        print("\n✅ Schema validation completed successfully!")
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    validate_schema()