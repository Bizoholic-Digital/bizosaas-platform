from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from app.activities.migration_activities import (
        migrate_plane_workspace_activity,
        get_migration_preview_activity
    )

@workflow.defn
class PlanMigrationWorkflow:
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates data migration from Plan.so to BizOSaaS.
        """
        # 1. Get Preview
        preview_res = await workflow.execute_activity(
            get_migration_preview_activity,
            params,
            start_to_close_timeout=timedelta(minutes=2),
        )
        
        if preview_res["status"] == "error":
            return {"status": "failed", "error": preview_res["message"]}

        # 2. Execute Migration
        # Note: In a real scenario, we might pause for HITL approval here
        migration_res = await workflow.execute_activity(
            migrate_plane_workspace_activity,
            params,
            start_to_close_timeout=timedelta(hours=1), # Migration can take time
        )
        
        if migration_res["status"] == "error":
            return {"status": "failed", "error": migration_res["message"]}
            
        return {
            "status": "completed",
            "preview": preview_res["preview"],
            "results": migration_res
        }
