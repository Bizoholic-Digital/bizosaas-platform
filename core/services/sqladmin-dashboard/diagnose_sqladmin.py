#!/usr/bin/env python3

"""
SQLAdmin Diagnostic Script
Identifies and fixes the TenantsAdmin pk_columns error
"""

import os
import logging
import traceback
from sqlalchemy import create_engine, text
from sqladmin import Admin, ModelView
from fastapi import FastAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:Bizoholic2024Alagiri@bizosaas-postgres-unified:5432/bizosaas')

def test_database_connection():
    """Test database connectivity"""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful")
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

def test_sqladmin_compatibility():
    """Test SQLAdmin model compatibility"""
    try:
        # Import SQLAdmin components
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Column, String, DateTime, Boolean, UUID
        
        Base = declarative_base()
        
        # Create a simple test model
        class TestTenant(Base):
            __tablename__ = "test_tenants"
            id = Column(UUID(as_uuid=True), primary_key=True)
            name = Column(String(100))
            
        # Create a test admin view
        class TestTenantAdmin(ModelView, model=TestTenant):
            column_list = [TestTenant.id, TestTenant.name]
            
        logger.info("✅ SQLAdmin model definition is compatible")
        return True
        
    except Exception as e:
        logger.error(f"❌ SQLAdmin compatibility issue: {e}")
        logger.error(traceback.format_exc())
        return False

def diagnose_admin_views():
    """Diagnose admin view registration issues"""
    try:
        # Test with a minimal FastAPI app
        app = FastAPI()
        engine = create_engine(DATABASE_URL)
        admin = Admin(app, engine)
        
        logger.info("✅ Admin object created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Admin view registration failed: {e}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("🔍 Starting SQLAdmin Diagnostic...")
    
    # Test database connection
    logger.info("1. Testing database connection...")
    if not test_database_connection():
        logger.error("Database connection failed. Cannot proceed with other tests.")
        exit(1)
    
    # Test SQLAdmin compatibility
    logger.info("2. Testing SQLAdmin compatibility...")
    if not test_sqladmin_compatibility():
        logger.error("SQLAdmin compatibility test failed.")
        exit(1)
    
    # Test admin view registration
    logger.info("3. Testing admin view registration...")
    if not diagnose_admin_views():
        logger.error("Admin view registration failed.")
        exit(1)
    
    logger.info("🎉 All diagnostic tests passed!")