from temporalio import activity
import logging
from app.services.workflow_discovery import run_discovery_cycle

logger = logging.getLogger(__name__)

@activity.defn(name="run_discovery_cycle_activity")
async def run_discovery_cycle_activity() -> dict:
    """
    Activity wrapper for the discovery cycle service.
    """
    logger.info("Starting autonomous discovery cycle activity")
    try:
        results = await run_discovery_cycle()
        return results
    except Exception as e:
        logger.error(f"Discovery cycle activity failed: {e}")
        return {"status": "error", "message": str(e)}
