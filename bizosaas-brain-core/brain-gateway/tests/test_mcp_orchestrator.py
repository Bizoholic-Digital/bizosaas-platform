import pytest
import asyncio
from unittest.mock import MagicMock, patch
from uuid import uuid4
from app.services.mcp_orchestrator import McpOrchestrator
from app.models.mcp import UserMcpInstallation

@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session

@pytest.mark.asyncio
async def test_provision_mcp_success(mock_db_session):
    installation_id = uuid4()
    mock_installation = UserMcpInstallation(id=installation_id, status="pending")
    
    # Mock SessionLocal and its actions
    with patch("app.dependencies.SessionLocal", return_value=mock_db_session):
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_installation
        
        # We need to mock asyncio.sleep to speed up tests
        with patch("asyncio.sleep", return_value=None):
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
