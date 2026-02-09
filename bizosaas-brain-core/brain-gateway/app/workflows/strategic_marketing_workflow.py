from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any

# Import activity definition (referenced by name string in execute_activity)

@workflow.defn
class StrategicMarketingWorkflow:
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates the Strategic Marketing Agent to develop and refine a campaign strategy.
        Interact with the AI Agents service to get high-level strategy, then breaks it down.
        """
        tenant_id = params.get("tenant_id", "default")
        company_info = params.get("company_info", {})
        goals = params.get("goals", {})
        budget = params.get("budget", 10000)
        
        # 1. Execute Marketing Strategist Agent
        # This calls the activity we just added which talks to the ai-agents service
        strategy_result = await workflow.execute_activity(
            "execute_marketing_strategy_activity",
            {
                "tenant_id": tenant_id,
                "company_info": company_info,
                "goals": goals,
                "budget": budget,
                "timeline": params.get("timeline", "3 months")
            },
            start_to_close_timeout=timedelta(minutes=5) # Allow time for LLM generation
        )
        
        # 2. (Optional) Parse strategy to identify required content
        # For now, we'll just return the strategy, but we could trigger content creation here
        
        # Example: specific content generation based on strategy output
        # content_result = await workflow.execute_activity("generate_ai_marketing_content", ...)

        return {
            "status": "strategy_developed",
            "strategy": strategy_result,
            "generated_at": workflow.now().isoformat()
        }
