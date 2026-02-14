import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from app.domain.ports.identity_port import AuthenticatedUser
from app.dependencies import get_current_user

client = TestClient(app)

@pytest.fixture
def mock_user():
    return AuthenticatedUser(
        id="user_new_123",
        email="onboarding@example.com",
        name="New User",
        roles=["admin"],
        tenant_id="tenant_new_456"
    )

@pytest.mark.asyncio
async def test_onboarding_flow(mock_user):
    # 1. Mock Authentication
    from app.dependencies import get_current_user as get_user_deps
    from app.middleware.auth import get_current_user as get_user_middleware
    app.dependency_overrides[get_user_deps] = lambda: mock_user
    app.dependency_overrides[get_user_middleware] = lambda: mock_user
    
    try:
        # 2. Check recommendations for new user
        response = client.get("/api/discovery/recommendations")
        assert response.status_code == 200
        recommendations = response.json()
        assert len(recommendations) > 0
        assert any(r["id"] == "mailchimp" for r in recommendations)

        # 3. Simulate connecting Google (Dry Run)
        payload = {
            "access_token": "mock_google_token",
            "selected_connectors": ["gmail", "calendar"],
            "dry_run": True
        }
        with patch("app.api.onboarding.discover_google_services", return_value={"status": "success", "discovered": ["gmail", "calendar"]}):
             response = client.post("/api/onboarding/google/discover", json=payload)
             assert response.status_code == 200
             assert "discovered" in response.json()

        # 4. Finalize connecting a connector (e.g. Trello)
        trello_credentials = {"api_key": "abc", "api_token": "def"}
        with patch("app.connectors.trello.TrelloConnector.validate_credentials", return_value=True):
            response = client.post("/api/connectors/trello/connect", json=trello_credentials)
            assert response.status_code == 200
            assert response.json()["status"] == "connected"

        # 5. Verify the connector is now listed
        response = client.get("/api/connectors")
        assert response.status_code == 200
        connectors = response.json()
        trello = next((c for c in connectors if c["id"] == "trello"), None)
        assert trello is not None
        assert trello["status"] == "connected"

        # 6. Check overall health
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] in ["healthy", "degraded"]
        
    finally:
        app.dependency_overrides.clear()
