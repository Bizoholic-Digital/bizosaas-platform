from datetime import timedelta
from temporalio import workflow
from typing import List, Dict, Any

# Import activities
with workflow.unsafe.imports_passed_through():
    from app.activities.performance import (
        analyze_agent_performance_activity,
        generate_optimization_suggestions_activity,
        analyze_campaign_metrics_activity,
        optimize_ad_spend_activity
    )

@workflow.defn
class AutonomousOptimizationWorkflow:
    """
    Workflow that periodically analyzes all agents and suggests optimizations.
    """
    @workflow.run
    async def run(self, agent_ids: List[str]) -> Dict[str, Any]:
        results = []
        for agent_id in agent_ids:
            # 1. Analyze Performance
            metrics = await workflow.execute_activity(
                analyze_agent_performance_activity,
                agent_id,
                start_to_close_timeout=timedelta(minutes=2)
            )
            
            # 2. Generate Suggestions
            suggestions = await workflow.execute_activity(
                generate_optimization_suggestions_activity,
                agent_id,
                metrics,
                start_to_close_timeout=timedelta(minutes=5)
            )
            
            results.append({
                "agent_id": agent_id,
                "suggestion_count": len(suggestions)
            })
            
        return {"status": "success", "processed_agents": results}

@workflow.defn
class CampaignOptimizationWorkflow:
    """
    Workflow that analyzes marketing campaigns and suggests budget adjustments.
    """
    @workflow.run
    async def run(self, connector_ids: List[str]) -> Dict[str, Any]:
        optimizations = []
        for connector_id in connector_ids:
            # 1. Fetch Metrics
            metrics = await workflow.execute_activity(
                analyze_campaign_metrics_activity,
                connector_id,
                start_to_close_timeout=timedelta(minutes=5)
            )
            
            # 2. Optimize Spend
            suggestions = await workflow.execute_activity(
                optimize_ad_spend_activity,
                metrics,
                start_to_close_timeout=timedelta(minutes=2)
            )
            
            optimizations.extend(suggestions)
            
        return {"status": "success", "recommendations": optimizations}
