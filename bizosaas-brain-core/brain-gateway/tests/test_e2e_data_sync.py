import pytest
import uuid
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock, AsyncMock
from app.domain.ports.identity_port import AuthenticatedUser

client = TestClient(app)

@pytest.fixture
def mock_user():
    return AuthenticatedUser(
        id=str(uuid.uuid4()),
        email="sync_manager@example.com",
        name="Sync Manager",
        roles=["admin"],
        tenant_id=str(uuid.uuid4())
    )

@pytest.mark.asyncio
async def test_data_sync_flow_e2e(mock_user):
    # 1. Mock Authentication
    from app.dependencies import get_current_user as get_user_deps
    from app.middleware.auth import get_current_user as get_user_middleware
    app.dependency_overrides[get_user_deps] = lambda: mock_user
    app.dependency_overrides[get_user_middleware] = lambda: mock_user
    
    # 2. Mock SecretService
    mock_secret_service = AsyncMock()
    mock_secret_service.get_connector_credentials.return_value = {"api_key": "test_key"}
    
    from app.dependencies import get_secret_service
    app.dependency_overrides[get_secret_service] = lambda: mock_secret_service
    
    try:
        connector_id = "hubspot"
        resource = "contacts"
        
        # 3. Mock ConnectorRegistry
        with patch("app.connectors.registry.ConnectorRegistry.create_connector") as mock_create_connector:
            mock_connector = AsyncMock()
            mock_connector.sync_data.return_value = [{"id": "1", "email": "test@example.com"}]
            mock_create_connector.return_value = mock_connector
            
            # 4. Trigger Sync
            response = client.get(f"/api/connectors/{connector_id}/sync/{resource}")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["email"] == "test@example.com"
            
            # 5. Verify connector was called correctly
            mock_create_connector.assert_called_once()
            mock_connector.sync_data.assert_called_once_with(resource)

    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_wordpress_plugin_discovery_e2e(mock_user):
    # 1. Mock Authentication
    from app.dependencies import get_current_user as get_user_deps
    from app.middleware.auth import get_current_user as get_user_middleware
    app.dependency_overrides[get_user_deps] = lambda: mock_user
    app.dependency_overrides[get_user_middleware] = lambda: mock_user
    
    # 2. Mock SecretService
    mock_secret_service = AsyncMock()
    mock_secret_service.get_connector_credentials.return_value = {"url": "http://wp.com", "username": "admin", "application_password": "pwd"}
    
    from app.dependencies import get_secret_service
    app.dependency_overrides[get_secret_service] = lambda: mock_secret_service
    
    try:
        connector_id = "wordpress"
        
        # 3. Mock WordPressConnector
        with patch("app.connectors.wordpress.WordPressConnector.discover_plugins") as mock_discover:
            mock_discover.return_value = [{"slug": "fluentcrm", "name": "FluentCRM"}]
            
            # 4. Trigger Discovery
            response = client.get(f"/api/connectors/{connector_id}/plugins")
            
            assert response.status_code == 200
            data = response.json()
            assert "plugins" in data
            assert data["plugins"][0]["slug"] == "fluentcrm"

    finally:
        app.dependency_overrides.clear()
