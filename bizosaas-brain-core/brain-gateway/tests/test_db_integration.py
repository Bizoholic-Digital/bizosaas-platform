import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Tenant
from app.dependencies import SessionLocal, engine
import uuid

def test_database_connectivity():
    """Verify that the engine can connect and perform basic operations."""
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    assert connection is not None
    connection.close()

def test_database_crud():
    """Verify CRUD operations on the database."""
    db = SessionLocal()
    tenant_id = uuid.uuid4()
    try:
        # Create
        new_tenant = Tenant(
            id=tenant_id,
            name="Test Integration Tenant",
            slug=f"test-tenant-{tenant_id.hex[:8]}",
            status="active"
        )
        db.add(new_tenant)
        db.commit()
        
        # Read
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        assert tenant is not None
        assert tenant.name == "Test Integration Tenant"
        
        # Update
        tenant.name = "Updated Tenant Name"
        db.commit()
        db.refresh(tenant)
        assert tenant.name == "Updated Tenant Name"
        
        # Delete
        db.delete(tenant)
        db.commit()
        
        tenant_deleted = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        assert tenant_deleted is None
    finally:
        db.close()
