"""
Integration Tests for Brain Gateway API
Tests: INT-001 through INT-007
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
from datetime import datetime

# Test database setup
TEST_DATABASE_URL = "postgresql://test:test@localhost:5432/bizosaas_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def test_db():
    """Create test database"""
    from app.core.database import Base
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


@pytest.fixture
def redis_client():
    """Create Redis test client"""
    client = redis.Redis(host='localhost', port=6379, db=15, decode_responses=True)
    yield client
    client.flushdb()


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
        
        response = test_client.post(
            "/api/campaigns",
            json=payload,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Verify response schema
        assert "id" in data
        assert "name" in data
        assert "created_at" in data
        assert data["name"] == payload["name"]
        assert data["type"] == payload["type"]
    
    def test_campaign_list_contract(self, test_client):
        """Test campaign list API contract"""
        response = test_client.get(
            "/api/campaigns",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response schema
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "per_page" in data
        assert isinstance(data["items"], list)
    
    def test_error_response_contract(self, test_client):
        """Test error response follows standard format"""
        response = test_client.post(
            "/api/campaigns",
            json={},  # Invalid payload
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 422
        data = response.json()
        
        # Verify error schema
        assert "error" in data
        assert "message" in data
        assert "details" in data or "errors" in data


class TestDatabaseIntegration:
    """INT-002: Brain Gateway ↔ PostgreSQL ORM tests"""
    
    def test_campaign_crud_operations(self, db_session):
        """Test complete CRUD operations for campaigns"""
        from app.models.campaign import Campaign
        
        # CREATE
        campaign = Campaign(
            name="Test Campaign",
            type="email",
            tenant_id="tenant-123",
            budget=1000
        )
        db_session.add(campaign)
        db_session.commit()
        
        assert campaign.id is not None
        
        # READ
        retrieved = db_session.query(Campaign).filter_by(id=campaign.id).first()
        assert retrieved.name == "Test Campaign"
        
        # UPDATE
        retrieved.budget = 2000
        db_session.commit()
        
        updated = db_session.query(Campaign).filter_by(id=campaign.id).first()
        assert updated.budget == 2000
        
        # DELETE
        db_session.delete(updated)
        db_session.commit()
        
        deleted = db_session.query(Campaign).filter_by(id=campaign.id).first()
        assert deleted is None
    
    def test_tenant_isolation_at_db_level(self, db_session):
        """Test tenant isolation is enforced at database level"""
        from app.models.campaign import Campaign
        
        # Create campaigns for different tenants
        campaign1 = Campaign(name="Campaign 1", tenant_id="tenant-1", type="email")
        campaign2 = Campaign(name="Campaign 2", tenant_id="tenant-2", type="email")
        
        db_session.add_all([campaign1, campaign2])
        db_session.commit()
        
        # Query with tenant filter
        tenant1_campaigns = db_session.query(Campaign).filter_by(tenant_id="tenant-1").all()
        
        assert len(tenant1_campaigns) == 1
        assert tenant1_campaigns[0].name == "Campaign 1"
    
    def test_database_transaction_rollback(self, db_session):
        """Test transaction rollback on error"""
        from app.models.campaign import Campaign
        
        try:
            campaign = Campaign(
                name="Test Campaign",
                type="email",
                tenant_id="tenant-123"
            )
            db_session.add(campaign)
            db_session.flush()
            
            # Simulate error
            raise Exception("Simulated error")
            
        except Exception:
            db_session.rollback()
        
        # Verify nothing was committed
        campaigns = db_session.query(Campaign).filter_by(name="Test Campaign").all()
        assert len(campaigns) == 0


class TestCacheIntegration:
    """INT-003: Brain Gateway ↔ Redis cache tests"""
    
    def test_cache_set_and_get(self, redis_client):
        """Test basic cache operations"""
        from app.core.cache import set_cache, get_cache
        
        key = "test:campaign:123"
        value = {"id": "123", "name": "Test Campaign"}
        
        # Set cache
        set_cache(redis_client, key, value, ttl=300)
        
        # Get cache
        cached = get_cache(redis_client, key)
        
        assert cached == value
    
    def test_cache_expiration(self, redis_client):
        """Test cache TTL expiration"""
        from app.core.cache import set_cache, get_cache
        import time
        
        key = "test:expiring"
        value = "test-value"
        
        # Set with 1 second TTL
        set_cache(redis_client, key, value, ttl=1)
        
        # Should exist immediately
        assert get_cache(redis_client, key) == value
        
        # Wait for expiration
        time.sleep(2)
        
        # Should be gone
        assert get_cache(redis_client, key) is None
    
    def test_cache_invalidation_on_update(self, redis_client, db_session):
        """Test cache is invalidated when data is updated"""
        from app.models.campaign import Campaign
        from app.core.cache import get_cache, invalidate_cache
        
        # Create campaign
        campaign = Campaign(
            id="camp-123",
            name="Test Campaign",
            tenant_id="tenant-123",
            type="email"
        )
        db_session.add(campaign)
        db_session.commit()
        
        # Cache it
        cache_key = f"campaign:{campaign.id}"
        redis_client.set(cache_key, campaign.name)
        
        # Update campaign
        campaign.name = "Updated Campaign"
        db_session.commit()
        
        # Invalidate cache
        invalidate_cache(redis_client, cache_key)
        
        # Cache should be empty
        assert redis_client.get(cache_key) is None


class TestWebhookHandling:
    """INT-004: Webhook delivery and handling tests"""
    
    def test_webhook_registration(self, test_client):
        """Test webhook endpoint registration"""
        payload = {
            "url": "https://example.com/webhook",
            "events": ["campaign.created", "campaign.updated"],
            "secret": "webhook-secret-123"
        }
        
        response = test_client.post(
            "/api/webhooks",
            json=payload,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["url"] == payload["url"]
    
    def test_webhook_delivery(self, test_client):
        """Test webhook is delivered on event"""
        from unittest.mock import patch
        
        # Register webhook
        webhook_payload = {
            "url": "https://example.com/webhook",
            "events": ["campaign.created"]
        }
        
        test_client.post(
            "/api/webhooks",
            json=webhook_payload,
            headers={"Authorization": "Bearer test-token"}
        )
        
        # Trigger event
        with patch('app.core.webhooks.deliver_webhook') as mock_deliver:
            campaign_payload = {
                "name": "Test Campaign",
                "type": "email"
            }
            
            test_client.post(
                "/api/campaigns",
                json=campaign_payload,
                headers={"Authorization": "Bearer test-token"}
            )
            
            # Verify webhook was triggered
            mock_deliver.assert_called()
    
    def test_webhook_retry_on_failure(self):
        """Test webhook retry logic on delivery failure"""
        from app.core.webhooks import deliver_webhook_with_retry
        from unittest.mock import Mock
        
        webhook = {
            "url": "https://example.com/webhook",
            "secret": "secret"
        }
        
        event = {"type": "campaign.created", "data": {}}
        
        # Mock failed deliveries
        with patch('requests.post') as mock_post:
            mock_post.side_effect = [
                Mock(status_code=500),  # Fail
                Mock(status_code=500),  # Fail
                Mock(status_code=200),  # Success
            ]
            
            result = deliver_webhook_with_retry(webhook, event, max_retries=3)
            
            assert result is True
            assert mock_post.call_count == 3


class TestTemporalWorkflows:
    """INT-005: Temporal workflow execution tests"""
    
    @pytest.mark.asyncio
    async def test_campaign_workflow_execution(self):
        """Test campaign creation workflow"""
        from app.workflows.campaign import create_campaign_workflow
        
        workflow_input = {
            "name": "Test Campaign",
            "type": "email",
            "tenant_id": "tenant-123"
        }
        
        result = await create_campaign_workflow(workflow_input)
        
        assert result["status"] == "completed"
        assert "campaign_id" in result
    
    @pytest.mark.asyncio
    async def test_workflow_error_handling(self):
        """Test workflow handles errors gracefully"""
        from app.workflows.campaign import create_campaign_workflow
        
        # Invalid input
        workflow_input = {}
        
        with pytest.raises(ValueError):
            await create_campaign_workflow(workflow_input)


class TestAuthentikSSO:
    """INT-006: Authentik SSO integration tests"""
    
    def test_sso_login_redirect(self, test_client):
        """Test SSO login redirects to Authentik"""
        response = test_client.get("/auth/sso/login")
        
        assert response.status_code == 302
        assert "authentik" in response.headers["Location"]
    
    def test_sso_callback_handling(self, test_client):
        """Test SSO callback creates session"""
        from unittest.mock import patch
        
        with patch('app.auth.sso.verify_authentik_token') as mock_verify:
            mock_verify.return_value = {
                "user_id": "user-123",
                "email": "test@example.com",
                "tenant_id": "tenant-123"
            }
            
            response = test_client.get(
                "/auth/sso/callback?code=test-code&state=test-state"
            )
            
            assert response.status_code == 302
            assert "session" in response.cookies


class TestLagoBilling:
    """INT-007: Lago billing API integration tests"""
    
    def test_create_customer_in_lago(self):
        """Test customer creation in Lago"""
        from app.integrations.lago import create_lago_customer
        
        customer_data = {
            "external_id": "tenant-123",
            "name": "Test Company",
            "email": "billing@test.com"
        }
        
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 201
            mock_post.return_value.json.return_value = {
                "customer": {"lago_id": "lago-123"}
            }
            
            result = create_lago_customer(customer_data)
            
            assert result["lago_id"] == "lago-123"
    
    def test_create_subscription(self):
        """Test subscription creation in Lago"""
        from app.integrations.lago import create_subscription
        
        subscription_data = {
            "external_customer_id": "tenant-123",
            "plan_code": "pro-monthly"
        }
        
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 201
            mock_post.return_value.json.return_value = {
                "subscription": {"lago_id": "sub-123"}
            }
            
            result = create_subscription(subscription_data)
            
            assert result["lago_id"] == "sub-123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
