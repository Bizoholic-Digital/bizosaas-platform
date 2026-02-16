"""
Alerting Workflow.

Orchestrates the periodic checking of alerts.
"""

from datetime import timedelta
from typing import Dict, Any

from temporalio import workflow
from temporalio.common import RetryPolicy

# Import activities
with workflow.unsafe.imports_passed_through():
    from app.activities.alerts import check_platform_alerts_activity


@workflow.defn
class AlertMonitoringWorkflow:
    """
    Workflow that triggers the alert check activity.
    Designed to be scheduled (e.g., every 5-15 minutes).
    """

    @workflow.run
    async def run(self) -> Dict[str, Any]:
        """
        Execute alert monitoring.
        
        Returns:
            Review of alert processing
        """
        # Configure activity options
        activity_options = workflow.ActivityOptions(
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=5),
                maximum_interval=timedelta(minutes=1),
                maximum_attempts=3
            )
        )
        
        # Execute alert check
        result = await workflow.execute_activity(
            check_platform_alerts_activity,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=5),
                maximum_interval=timedelta(minutes=1),
                maximum_attempts=3
            )
        )
        
        return result
