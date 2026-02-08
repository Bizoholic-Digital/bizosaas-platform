import pytest
import asyncio
import os
from unittest.mock import MagicMock, patch
from uuid import uuid4
from app.services.mcp_orchestrator import McpOrchestrator
from app.models.mcp import UserMcpInstallation
from app.models.workflow import Workflow

@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session

@pytest.mark.asyncio
async def test_provision_mcp_success(mock_db_session):
    installation_id = uuid4()
    mock_mcp = MagicMock()
    mock_mcp.name = "Test MCP"
    mock_mcp.slug = "test-mcp"
    mock_installation = UserMcpInstallation(id=installation_id, status="pending", user_id="test-user")
    mock_installation.mcp = mock_mcp
    
    # Mock specific queries
    def query_side_effect(model):
        q = MagicMock()
        if model == UserMcpInstallation:
            q.filter.return_value.first.return_value = mock_installation
        elif model == Workflow:
            q.filter.return_value.first.return_value = None # Force creation of new workflow
        return q

    mock_db_session.query.side_effect = query_side_effect
    
    # Mock SessionLocal and its actions
    with patch("app.dependencies.SessionLocal", return_value=mock_db_session):
        # Mock McpInstallationService to avoid Vault calls
        with patch("app.services.mcp_installation_service.McpInstallationService.get_decrypted_config", return_value={"api_key": "test"}):
            # Mock get_workflow_port to avoid Temporal calls
            with patch("app.dependencies.get_workflow_port", side_effect=Exception("No Temporal")):
                # We need to mock asyncio.sleep to speed up tests
                with patch("asyncio.sleep", return_value=None):
                    # Ensure TEMPORAL_HOST is NOT set to trigger fallback
                    with patch.dict("os.environ", {}, clear=False):
                        if "TEMPORAL_HOST" in os.environ:
                            del os.environ["TEMPORAL_HOST"]
                        
                        await McpOrchestrator.provision_mcp(installation_id)
                        
                        assert mock_installation.status == "active"
                        assert mock_db_session.commit.call_count >= 2
                        mock_db_session.close.assert_called_once()

@pytest.mark.asyncio
async def test_provision_mcp_not_found(mock_db_session):
    installation_id = uuid4()
    
    with patch("app.dependencies.SessionLocal", return_value=mock_db_session):
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        await McpOrchestrator.provision_mcp(installation_id)
        
        mock_db_session.commit.assert_not_called()
        mock_db_session.close.assert_called_once()

@pytest.mark.asyncio
async def test_deprovision_mcp(mock_db_session):
    installation_id = uuid4()
    mock_installation = UserMcpInstallation(id=installation_id, status="active")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_installation
    
    await McpOrchestrator.deprovision_mcp(installation_id, mock_db_session)
    
    assert mock_installation.status == "terminated"
    mock_db_session.commit.assert_called_once()
