import sys
from unittest.mock import MagicMock, AsyncMock, patch

# Mock langcache for environment where it is not installed
mock_langcache = MagicMock()
sys.modules["langcache"] = mock_langcache

import pytest
from app.activities.performance import (
    analyze_agent_performance_activity,
    generate_optimization_suggestions_activity,
    analyze_campaign_metrics_activity,
    optimize_ad_spend_activity
)
from app.workflows.optimization_workflow import AutonomousOptimizationWorkflow, CampaignOptimizationWorkflow

@pytest.mark.asyncio
async def test_analyze_agent_performance_activity():
    result = await analyze_agent_performance_activity("test-agent")
    assert result["agent_id"] == "test-agent"
    assert "avg_latency" in result
    assert "success_rate" in result

@pytest.mark.asyncio
async def test_generate_optimization_suggestions_activity():
    # Mock DB and Engine
    mock_db = MagicMock()
    mock_engine = AsyncMock()
    mock_engine._analyze_llm_costs.return_value = []
    
    metrics = {"agent_id": "test-agent", "avg_latency": 3.0, "success_rate": 0.9}
    
    with patch("app.activities.performance.SessionLocal", return_value=mock_db), \
         patch("app.activities.performance.CostOptimizationEngine", return_value=mock_engine):
        
        result = await generate_optimization_suggestions_activity("test-agent", metrics)
        
        # Should have at least the latency suggestion
        assert len(result) >= 1
        assert any(s["type"] == "latency" for s in result)

@pytest.mark.asyncio
async def test_analyze_campaign_metrics_activity():
    result = await analyze_campaign_metrics_activity("conn-123")
    assert result["connector_id"] == "conn-123"
    assert len(result["campaigns"]) > 0

@pytest.mark.asyncio
async def test_optimize_ad_spend_activity():
    campaign_data = {
        "campaigns": [
            {"id": "low_roi", "roi": 1.0},
            {"id": "high_roi", "roi": 4.0}
        ]
    }
    result = await optimize_ad_spend_activity(campaign_data)
    assert len(result) == 2
    assert any(r["action"] == "Reduce Budget" for r in result)
    assert any(r["action"] == "Increase Budget" for r in result)
