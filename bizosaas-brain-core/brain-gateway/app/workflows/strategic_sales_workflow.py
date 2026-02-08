from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any

@workflow.defn
class StrategicSalesWorkflow:
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates the Strategic Sales Intelligence Agent.
        """
        tenant_id = params.get("tenant_id", "default")
        sales_context = params.get("sales_context", {})
        mode = params.get("mode", "lead_qualification")
        
        # 1. Execute Sales Intelligence Agent
        sales_result = await workflow.execute_activity(
            "execute_sales_strategy_activity",
            {
                "tenant_id": tenant_id,
                "sales_context": sales_context,
                "mode": mode,
                "pipeline_value": params.get("pipeline_value"),
                "growth_target": params.get("growth_target")
            },
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        return {
            "status": "analysis_completed",
            "report": sales_result,
            "generated_at": workflow.now().isoformat()
        }
