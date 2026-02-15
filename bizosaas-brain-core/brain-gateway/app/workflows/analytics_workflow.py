"""
Analytics Workflow
Orchestrates periodic platform-wide analytics aggregation.
"""

from temporalio import workflow
from datetime import timedelta
from typing import Dict, Any
import uuid

with workflow.unsafe.imports_passed_through():
    from app.activities.analytics import (
        aggregate_workflow_metrics_activity,
        aggregate_tenant_usage_activity,
        aggregate_campaign_performance_activity,
        generate_platform_insights_activity
    )


@workflow.defn
class PlatformAnalyticsWorkflow:
    """
    Orchestrates the collection and aggregation of platform-wide analytics.
    
    This workflow runs periodically (hourly/daily) to generate analytics snapshots.
    """
    
    @workflow.run
    async def run(self, snapshot_type: str = "hourly", time_range_hours: int = 24) -> Dict[str, Any]:
        """
        Execute platform analytics aggregation.
        
        Args:
            snapshot_type: Type of snapshot (hourly, daily, weekly)
            time_range_hours: Number of hours to aggregate data for
            
        Returns:
            Dictionary containing all aggregated metrics and insights
        """
        workflow_id = workflow.info().workflow_id
        
        # Step 1: Aggregate workflow metrics
        workflow_metrics = await workflow.execute_activity(
            aggregate_workflow_metrics_activity,
            time_range_hours,
            start_to_close_timeout=timedelta(seconds=60)
        )
        
        # Step 2: Aggregate tenant usage
        tenant_usage = await workflow.execute_activity(
            aggregate_tenant_usage_activity,
            start_to_close_timeout=timedelta(seconds=60)
        )
        
        # Step 3: Aggregate campaign performance
        campaign_performance = await workflow.execute_activity(
            aggregate_campaign_performance_activity,
            start_to_close_timeout=timedelta(seconds=60)
        )
        
        # Step 4: Generate insights
        insights = await workflow.execute_activity(
            generate_platform_insights_activity,
            args=[workflow_metrics, tenant_usage, campaign_performance],
            start_to_close_timeout=timedelta(seconds=30)
        )
        
        # Combine all results
        return {
            "snapshot_id": str(uuid.uuid4()),
            "snapshot_type": snapshot_type,
            "workflow_metrics": workflow_metrics,
            "tenant_usage": tenant_usage,
            "campaign_performance": campaign_performance,
            "insights": insights
        }
