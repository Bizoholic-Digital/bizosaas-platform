from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

with workflow.unsafe.imports_passed_through():
    from app.services.workflow_discovery import run_discovery_cycle

@workflow.defn
class DiscoveryWorkflow:
    @workflow.run
    async def run(self) -> Dict[str, Any]:
        """
        Periodically runs the workflow discovery agent to identify optimization opportunities.
        """
        # In a real scenario, this would be an activity
        # But for the sake of the discovery cycle logic, we execute the service method
        # and return the results.
        
        results = await workflow.execute_activity(
            "run_discovery_cycle_activity",
            start_to_close_timeout=timedelta(minutes=10)
        )
        return results

@workflow.defn
class ContinuousImprovementWorkflow:
    @workflow.run
    async def run(self) -> None:
        """
        Infinite loop for continuous platform improvement (KAG).
        """
        while True:
            await workflow.execute_workflow(
                DiscoveryWorkflow,
                id=f"discovery-cycle-{workflow.now().isoformat()}",
                start_to_close_timeout=timedelta(minutes=15)
            )
            # Sleep for 24 hours before next discovery cycle
            await workflow.sleep(timedelta(hours=24))
