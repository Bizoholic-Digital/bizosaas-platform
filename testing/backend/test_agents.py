import pytest
from unittest.mock import Mock, patch
import sys

from app.services.agent_service import AgentService
from app.models.agent import AgentOptimization
from sqlalchemy.orm import Session
import uuid

@pytest.fixture
def db_session():
    return Mock(spec=Session)

def test_get_agent_optimizations(db_session):
    mock_query = db_session.query.return_value
    mock_all = mock_query.filter.return_value.order_by.return_value.all
    mock_all.return_value = [Mock(spec=AgentOptimization)]
    
    mock_all_no_filter = mock_query.order_by.return_value.all
    mock_all_no_filter.return_value = [Mock(spec=AgentOptimization)]
    
    results = AgentService.get_agent_optimizations(db_session)
    assert len(results) == 1

def test_approve_optimization(db_session):
    mock_opt = Mock(spec=AgentOptimization)
    db_session.query.return_value.filter.return_value.first.return_value = mock_opt
    AgentService.approve_optimization(db_session, "id")
    assert mock_opt.status == "approved"

@pytest.mark.asyncio
async def test_agent_chat_logic():
    # Use patch.dict to mock sys.modules for problematic dependencies
    # This prevents the real app.dependencies from being imported and failing
    with patch.dict("sys.modules", {
        "app.dependencies": Mock(),
        "adapters.identity": Mock(),
        "adapters.identity.mock_adapter": Mock(),
    }):
        from app.api.agents import generate_agent_response, AgentConfig
        
        mock_agent = AgentConfig(
            id="marketing-strategist", name="Marketing Strategist",
            description="...", role="Expert", capabilities=[], tools=[], icon="", color=""
        )
        
        # Test marketing response
        response = generate_agent_response(mock_agent, "How is my campaign?")
        assert "CTR" in response
