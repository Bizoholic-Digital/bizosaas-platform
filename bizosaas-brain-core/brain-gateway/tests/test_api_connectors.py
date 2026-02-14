from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from app.connectors.registry import ConnectorRegistry

client = TestClient(app)

from app.middleware.auth import get_current_user

# Mock Auth
async def override_get_current_user():
    from app.domain.ports.identity_port import AuthenticatedUser
    return AuthenticatedUser(
        id="user_1",
        email="test@example.com",
        name="Test User",
        roles=["admin"],
        tenant_id="test_tenant"
    )

app.dependency_overrides[get_current_user] = override_get_current_user

def test_list_connector_types():
    response = client.get("/api/connectors/types")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Check if our new connectors are present
    ids = [c["id"] for c in data]
    assert "fluentcrm" in ids # id in get_config() is "fluentcrm"
    assert "woocommerce" in ids
    assert "trello" in ids
    assert "plane" in ids
    assert "lago" in ids

@patch("app.connectors.trello.TrelloConnector.validate_credentials", return_value=True)
def test_connect_trello(mock_validate):
    credentials = {"api_key": "test", "api_token": "test"}
    response = client.post("/api/connectors/trello/connect", json=credentials)
    assert response.status_code == 200
    assert response.json()["status"] == "connected"

def test_get_connector_status_disconnected():
    response = client.get("/api/connectors/unknown/status")
    assert response.json()["status"] == "disconnected"
