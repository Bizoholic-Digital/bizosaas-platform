import pytest
import uuid
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock, AsyncMock
from domain.ports.identity_port import AuthenticatedUser
from app.dependencies import get_current_user
from app.models import Base, Tenant
from app.models.campaign import Campaign, CampaignChannel

client = TestClient(app)

@pytest.fixture
def mock_user():
    return AuthenticatedUser(
        id=str(uuid.uuid4()),
        email="campaign_manager@example.com",
        name="Campaign Manager",
        roles=["admin"],
        tenant_id=str(uuid.uuid4())
    )

@pytest.mark.asyncio
async def test_campaign_lifecycle_e2e(mock_user):
    # 1. Mock Authentication
    from app.dependencies import get_current_user as get_user_deps
    from app.middleware.auth import get_current_user as get_user_middleware
    app.dependency_overrides[get_user_deps] = lambda: mock_user
    app.dependency_overrides[get_user_middleware] = lambda: mock_user
    
    try:
        # 2. Create Campaign
        campaign_payload = {
            "name": "Summer Blast Sale",
            "goal": "Increase sales by 20%",
            "channels": [
                {
                    "channel_type": "email",
                    "connector_id": "mailchimp",
                    "config": {"subject": "Hot Deals!", "list_id": "list_123"}
                }
            ]
        }
        
        response = client.post("/api/campaigns/", json=campaign_payload)
        assert response.status_code == 200
        campaign_data = response.json()
        assert campaign_data["name"] == "Summer Blast Sale"
        campaign_id = campaign_data["id"]
        
        # 3. List Campaigns
        response = client.get("/api/campaigns/")
        assert response.status_code == 200
        campaigns = response.json()
        assert any(c["id"] == campaign_id for c in campaigns)
        
        # 4. Get Specific Campaign
        response = client.get(f"/api/campaigns/{campaign_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Summer Blast Sale"
        
        # 5. Publish Campaign (Mocking external connector)
        # We need to mock _get_connector in CampaignService to return a mock connector
        with patch("app.services.campaign_service.CampaignService._get_connector") as mock_get_conn:
            mock_connector = AsyncMock()
            mock_connector.create_campaign.return_value = MagicMock(id="ext_campaign_789")
            mock_get_conn.return_value = mock_connector
            
            response = client.post(f"/api/campaigns/{campaign_id}/publish")
            assert response.status_code == 200
            result = response.json()
            assert result["status"] == "published"
            assert len(result["results"]) > 0
            assert result["results"][0]["remote_id"] == "ext_campaign_789"

    finally:
        app.dependency_overrides.clear()
