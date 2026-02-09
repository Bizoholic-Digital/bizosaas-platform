"""
Scheduled Discovery Job
Runs the WorkflowDiscoveryAgent on a schedule to continuously identify new automation opportunities.
"""

import asyncio
import logging
from datetime import datetime
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker
from app.services.workflow_discovery import WorkflowDiscoveryAgent, run_discovery_cycle
from app.dependencies import get_db

logger = logging.getLogger(__name__)


@activity.defn
async def run_workflow_discovery() -> dict:
    """
    Activity that runs the workflow discovery cycle.
    """
    try:
        result = await run_discovery_cycle()
        logger.info(f"Discovery cycle completed: {result}")
        return result
    except Exception as e:
        logger.error(f"Discovery cycle failed: {e}")
        raise


@workflow.defn
class ScheduledDiscoveryWorkflow:
    """
    Temporal workflow that runs workflow discovery on a schedule.
    """
    
    @workflow.run
    async def run(self) -> dict:
        """
        Execute the discovery cycle.
        """
        logger.info("Starting scheduled workflow discovery...")
        
        result = await workflow.execute_activity(
            run_workflow_discovery,
            start_to_close_timeout=workflow.timedelta(minutes=30)
        )
        
        logger.info(f"Scheduled discovery completed: {result}")
        return result


async def start_discovery_scheduler(temporal_url: str = "localhost:7233"):
    """
    Start the Temporal worker for scheduled discovery.
    This should run as a background service.
    """
    client = await Client.connect(temporal_url)
    
    # Start the workflow on a schedule (daily at 2 AM)
    handle = await client.start_workflow(
        ScheduledDiscoveryWorkflow.run,
        id="workflow-discovery-scheduler",
        task_queue="discovery-scheduler",
        cron_schedule="0 2 * * *"  # Daily at 2 AM
    )
    
    logger.info(f"Started scheduled discovery workflow: {handle.id}")
    
    # Start worker
    worker = Worker(
        client,
        task_queue="discovery-scheduler",
        workflows=[ScheduledDiscoveryWorkflow],
        activities=[run_workflow_discovery]
    )
    
    logger.info("Discovery scheduler worker started")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(start_discovery_scheduler())
