"""
Billing Sync Workflow - Daily sync of usage events to Lago.

This Temporal workflow:
1. Fetches pending billing events from the database
2. Batches them for efficient API calls  
3. Sends to Lago via their Events API
4. Marks events as synced or failed
"""

from datetime import timedelta
from temporalio import workflow, activity
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


@activity.defn
async def fetch_pending_events(batch_size: int = 500) -> List[Dict[str, Any]]:
    """
    Fetch pending billing events from the database.
    Returns events in Lago-ready format.
    """
    from app.dependencies import get_db
    from app.models.billing_event import BillingEvent, BillingEventService
    
    db = next(get_db())
    try:
        service = BillingEventService(db)
        events = service.get_pending_events(limit=batch_size)
        
        return [
            {
                "id": str(event.id),
                "lago_event": event.to_lago_event()
            }
            for event in events
        ]
    finally:
        db.close()


@activity.defn
async def sync_events_to_lago(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Send events to Lago's batch events API.
    """
    import httpx
    import os
    
    if not events:
        return {"synced": 0, "failed": 0}
    
    lago_api_url = os.environ.get("LAGO_API_URL", "http://lago-api:3000")
    lago_api_key = os.environ.get("LAGO_API_KEY", "")
    
    if not lago_api_key:
        logger.warning("LAGO_API_KEY not configured, skipping sync")
        return {"synced": 0, "failed": 0, "error": "API key not configured"}
    
    lago_events = [e["lago_event"] for e in events]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{lago_api_url}/api/v1/events/batch",
                headers={
                    "Authorization": f"Bearer {lago_api_key}",
                    "Content-Type": "application/json"
                },
                json={"events": lago_events},
                timeout=30.0
            )
            
            if response.status_code in [200, 201, 202]:
                return {
                    "synced": len(events),
                    "failed": 0,
                    "event_ids": [e["id"] for e in events]
                }
            else:
                logger.error(f"Lago sync failed: {response.status_code} - {response.text}")
                return {
                    "synced": 0,
                    "failed": len(events),
                    "error": response.text,
                    "event_ids": [e["id"] for e in events]
                }
    except Exception as e:
        logger.error(f"Lago sync error: {e}")
        return {
            "synced": 0,
            "failed": len(events),
            "error": str(e),
            "event_ids": [e["id"] for e in events]
        }


@activity.defn
async def mark_events_synced(event_ids: List[str], success: bool) -> None:
    """
    Mark events as synced or failed in the database.
    """
    from app.dependencies import get_db
    from app.models.billing_event import BillingEventService
    import uuid
    
    db = next(get_db())
    try:
        service = BillingEventService(db)
        uuids = [uuid.UUID(eid) for eid in event_ids]
        
        if success:
            service.mark_synced(uuids)
        else:
            service.mark_failed(uuids)
    finally:
        db.close()


@workflow.defn
class BillingSyncWorkflow:
    """
    Daily workflow to sync usage events to Lago.
    Runs as a scheduled Temporal workflow.
    """
    
    @workflow.run
    async def run(self, batch_size: int = 500) -> Dict[str, Any]:
        total_synced = 0
        total_failed = 0
        
        # Process in batches until no more pending events
        while True:
            # Fetch pending events
            events = await workflow.execute_activity(
                fetch_pending_events,
                args=[batch_size],
                start_to_close_timeout=timedelta(seconds=30)
            )
            
            if not events:
                break
            
            # Sync to Lago
            result = await workflow.execute_activity(
                sync_events_to_lago,
                args=[events],
                start_to_close_timeout=timedelta(seconds=60)
            )
            
            # Mark events in database
            if result.get("event_ids"):
                await workflow.execute_activity(
                    mark_events_synced,
                    args=[result["event_ids"], result["synced"] > 0],
                    start_to_close_timeout=timedelta(seconds=30)
                )
            
            total_synced += result.get("synced", 0)
            total_failed += result.get("failed", 0)
            
            # If we got fewer events than batch_size, we're done
            if len(events) < batch_size:
                break
        
        return {
            "status": "completed",
            "total_synced": total_synced,
            "total_failed": total_failed
        }
