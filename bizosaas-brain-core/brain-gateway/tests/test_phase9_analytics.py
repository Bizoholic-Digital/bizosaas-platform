"""
Unit Tests for Phase 9: Multi-tenant Analytics Dashboard
Tests analytics activities, workflows, and API endpoints.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

# Mock langcache before importing activities
import sys
sys.modules['langcache'] = MagicMock()

from app.activities.analytics import (
    aggregate_workflow_metrics_activity,
    aggregate_tenant_usage_activity,
    aggregate_campaign_performance_activity,
    generate_platform_insights_activity
)
from app.workflows.analytics_workflow import PlatformAnalyticsWorkflow


class TestAnalyticsActivities:
    """Test suite for analytics aggregation activities."""
    
    @pytest.mark.asyncio
    async def test_aggregate_workflow_metrics(self):
        """Test workflow metrics aggregation activity."""
        with patch('app.activities.analytics.get_db') as mock_db:
            # Mock database session
            mock_session = MagicMock()
            mock_db.return_value = iter([mock_session])
            
            # Mock query results
            mock_session.query.return_value.filter.return_value.scalar.return_value = 100
            mock_session.query.return_value.filter.return_value.group_by.return_value.all.return_value = [
                ("ContentCreationWorkflow", 50),
                ("SocialContentWorkflow", 30)
            ]
            
            result = await aggregate_workflow_metrics_activity(24)
            
            assert "total_executions" in result
            assert "success_rate" in result
            assert "avg_duration_seconds" in result
            assert "total_cost_usd" in result
            assert "workflow_breakdown" in result
            assert result["time_range_hours"] == 24
    
    @pytest.mark.asyncio
    async def test_aggregate_tenant_usage(self):
        """Test tenant usage aggregation activity."""
        with patch('app.activities.analytics.get_db') as mock_db:
            mock_session = MagicMock()
            mock_db.return_value = iter([mock_session])
            
            # Mock tenant data
            mock_tenant = MagicMock()
            mock_tenant.id = "tenant-123"
            mock_tenant.name = "Test Tenant"
            mock_session.query.return_value.all.return_value = [mock_tenant]
            
            # Mock metrics
            mock_session.query.return_value.filter.return_value.scalar.return_value = 50
            
            result = await aggregate_tenant_usage_activity()
            
            assert "total_tenants" in result
            assert "tenant_metrics" in result
            assert "generated_at" in result
    
    @pytest.mark.asyncio
    async def test_aggregate_campaign_performance(self):
        """Test campaign performance aggregation activity."""
        with patch('app.activities.analytics.get_db') as mock_db:
            mock_session = MagicMock()
            mock_db.return_value = iter([mock_session])
            
            # Mock campaign metrics
            mock_session.query.return_value.scalar.return_value = 100
            mock_session.query.return_value.filter.return_value.scalar.return_value = 1000
            
            result = await aggregate_campaign_performance_activity()
            
            assert "total_campaigns" in result
            assert "active_campaigns" in result
            assert "total_impressions" in result
            assert "total_clicks" in result
            assert "platform_ctr" in result
            assert "platform_conversion_rate" in result
    
    @pytest.mark.asyncio
    async def test_generate_platform_insights(self):
        """Test platform insights generation activity."""
        workflow_metrics = {
            "total_executions": 100,
            "success_rate": 85.5,
            "avg_duration_seconds": 350,
            "total_cost_usd": 1200,
            "time_range_hours": 24
        }
        
        tenant_usage = {
            "total_tenants": 5,
            "tenant_metrics": [
                {"tenant_name": "Top Tenant", "total_cost_usd": 500}
            ]
        }
        
        campaign_performance = {
            "platform_ctr": 1.5,
            "total_campaigns": 20
        }
        
        result = await generate_platform_insights_activity(
            workflow_metrics,
            tenant_usage,
            campaign_performance
        )
        
        assert "insights" in result
        assert "summary" in result
        assert isinstance(result["insights"], list)
        assert "total_insights" in result["summary"]


class TestPlatformAnalyticsWorkflow:
    """Test suite for PlatformAnalyticsWorkflow."""
    
    @pytest.mark.asyncio
    async def test_platform_analytics_workflow_execution(self):
        """Test complete platform analytics workflow execution."""
        from temporalio.testing import WorkflowEnvironment
        from temporalio.worker import Worker
        
        async with await WorkflowEnvironment.start_time_skipping() as env:
            # Mock activities
            async def mock_workflow_metrics(hours: int):
                return {
                    "total_executions": 100,
                    "success_rate": 95.0,
                    "avg_duration_seconds": 120,
                    "total_cost_usd": 50.0,
                    "workflow_breakdown": [],
                    "time_range_hours": hours
                }
            
            async def mock_tenant_usage():
                return {
                    "total_tenants": 3,
                    "tenant_metrics": []
                }
            
            async def mock_campaign_performance():
                return {
                    "total_campaigns": 10,
                    "active_campaigns": 5,
                    "platform_ctr": 2.5,
                    "platform_conversion_rate": 3.0
                }
            
            async def mock_insights(wf, tenant, campaign):
                return {
                    "insights": [],
                    "summary": {"total_insights": 0}
                }
            
            # Create worker with mocked activities
            async with Worker(
                env.client,
                task_queue="test-queue",
                workflows=[PlatformAnalyticsWorkflow],
                activities=[
                    mock_workflow_metrics,
                    mock_tenant_usage,
                    mock_campaign_performance,
                    mock_insights
                ]
            ):
                # Execute workflow
                result = await env.client.execute_workflow(
                    PlatformAnalyticsWorkflow.run,
                    args=["hourly", 24],
                    id="test-analytics-workflow",
                    task_queue="test-queue"
                )
                
                assert result is not None
                assert "snapshot_id" in result
                assert "snapshot_type" in result
                assert result["snapshot_type"] == "hourly"
                assert "workflow_metrics" in result
                assert "tenant_usage" in result
                assert "campaign_performance" in result
                assert "insights" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
