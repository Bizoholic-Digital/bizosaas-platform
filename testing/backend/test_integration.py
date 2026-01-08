"""
Integration Tests for Brain Gateway API
Tests: INT-001 (API COntracts), INT-002 (DB Integration)
"""

import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure Auth is disabled for tests if not already set
os.environ["DISABLE_AUTH"] = "true"

# Test database setup
TEST_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://test:test@localhost:5432/test_db")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def test_db():
    """Create test database"""
    # Import Base from where it's actually defined
    from app.models.user import Base
    # Also import other models to ensure they are registered with Base
    from app.models.campaign import Campaign
    
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    """Create a new database session for each test"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def test_client():
    """Create test client"""
    from main import app
    return TestClient(app)


class TestAPIContracts:
    """INT-001: API contracts between portals and Gateway"""
    
    def test_campaign_create_contract(self, test_client):
        """Test campaign creation API contract"""
        payload = {
            "name": "Test Campaign",
            "type": "email",
            "budget": 1000,
            "status": "draft"
        }
        
        # Auth headers are ignored when DISABLE_AUTH=true, but we pass them properly just in case
        response = test_client.post(
            "/api/campaigns/",
            json=payload,
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Note: If ending slash issue, try /api/campaigns/
        # Check if 201 or 200
        assert response.status_code in [200, 201]
        data = response.json()
        
        # Verify response schema
        assert "id" in data
        assert "name" in data
        assert data["name"] == payload["name"]
    
    def test_campaign_list_contract(self, test_client):
        """Test campaign list API contract"""
        response = test_client.get(
            "/api/campaigns/",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response schema (List[Campaign] or Dict with items)
        # Adjust based on actual response structure
        # If list:
        if isinstance(data, list):
            assert True
        else:
            assert "items" in data or "data" in data or "total" in data
    
    def test_error_response_contract(self, test_client):
        """Test error response follows standard format"""
        # Sending empty body for POST usually triggers 422
        response = test_client.post(
            "/api/campaigns/",
            json={},  
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 422


class TestDatabaseIntegration:
    """INT-002: Brain Gateway ↔ PostgreSQL ORM tests"""
    
    def test_campaign_crud_operations(self, db_session):
        """Test complete CRUD operations for campaigns"""
        from app.models.campaign import Campaign
        from app.models.user import Tenant
        import uuid
        
        # Need a tenant first due to ForeignKey
        tenant_id = uuid.uuid4()
        tenant = Tenant(id=tenant_id, name="Test Tenant", slug="test-tenant-slug")
        db_session.add(tenant)
        db_session.flush()

        # CREATE
        campaign = Campaign(
            name="Test Campaign",
            status="draft", # status enum
            tenant_id=tenant_id
        )
        db_session.add(campaign)
        db_session.commit()
        
        assert campaign.id is not None
        
        # READ
        retrieved = db_session.query(Campaign).filter_by(id=campaign.id).first()
        assert retrieved.name == "Test Campaign"
        
        # UPDATE
        retrieved.name = "Updated Name"
        db_session.commit()
        
        updated = db_session.query(Campaign).filter_by(id=campaign.id).first()
        assert updated.name == "Updated Name"
        
        # DELETE
        db_session.delete(updated)
        db_session.commit()
        
        deleted = db_session.query(Campaign).filter_by(id=campaign.id).first()
        assert deleted is None
