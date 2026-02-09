import pytest
import sys
import os
from unittest.mock import Mock, patch, AsyncMock
import uuid

# Add the gateway to sys.path
GATEWAY_PATH = "/home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway"
if GATEWAY_PATH not in sys.path:
    sys.path.insert(0, GATEWAY_PATH)

from app.services.mcp_orchestrator import McpOrchestrator
from app.models.mcp import UserMcpInstallation

@pytest.mark.asyncio
async def test_provision_mcp_success():
    installation_id = uuid.uuid4()
    mock_installation = Mock(spec=UserMcpInstallation)
    mock_installation.id = installation_id
    mock_installation.status = "pending"
    
    # Patch SessionLocal in app.database
    with patch("app.database.SessionLocal") as mock_session_local:
        mock_db = mock_session_local.return_value
        mock_db.query.return_value.filter.return_value.first.return_value = mock_installation
        
        # Patch sleep to avoid real wait
        with patch("asyncio.sleep", new_callable=AsyncMock):
            await McpOrchestrator.provision_mcp(installation_id)
            
            # Check status transitions
            assert mock_installation.status == "active"
            assert mock_db.commit.call_count >= 2
            mock_db.close.assert_called_once()

@pytest.mark.asyncio
async def test_deprovision_mcp():
    installation_id = uuid.uuid4()
    mock_installation = Mock(spec=UserMcpInstallation)
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_installation
    
    await McpOrchestrator.deprovision_mcp(installation_id, mock_db)
    
    assert mock_installation.status == "terminated"
    mock_db.commit.assert_called_once()
