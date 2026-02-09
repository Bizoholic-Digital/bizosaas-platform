from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

@workflow.defn
class CompetitorIntelWorkflow:
    @workflow.run
    async def run(self, tenant_id: str, competitors: List[str]) -> Dict[str, Any]:
        """
        Competitor Intelligence Workflow:
        1. Scrape competitor sites for pricing and ads.
        2. Detect changes and new campaigns.
        3. Trigger alerts or strategy refinement.
        """
        # Step 1: Scrape Competitors
        intel_data = await workflow.execute_activity(
            "scrape_competitor_data_activity",
            args=[tenant_id, competitors],
            start_to_close_timeout=timedelta(minutes=15)
        )

        # Step 2: Analyze Shifts
        analysis = await workflow.execute_activity(
            "analyze_competitor_shifts_activity",
            args=[tenant_id, intel_data],
            start_to_close_timeout=timedelta(minutes=10)
        )

        # Step 3: Trigger Alerts
        if analysis.get("critical_shift"):
            await workflow.execute_activity(
                "trigger_intel_alert_activity",
                args=[tenant_id, analysis],
                start_to_close_timeout=timedelta(minutes=3)
            )

        return {
            "status": "monitored",
            "competitors_tracked": len(competitors),
            "alerts_triggered": 1 if analysis.get("critical_shift") else 0,
            "timestamp": workflow.now().isoformat()
        }

@workflow.defn
class LeadScoringWorkflow:
    @workflow.run
    async def run(self, tenant_id: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI Lead Scoring Workflow:
        1. Enrich lead data via external APIs.
        2. Score lead based on RAG/KAG pattern matching.
        3. Route high-priority leads to sales.
        """
        # Step 1: Data Enrichment
        enriched_lead = await workflow.execute_activity(
            "enrich_lead_data_activity",
            args=[lead_data],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Step 2: AI Scoring
        scoring_res = await workflow.execute_activity(
            "score_lead_activity",
            args=[tenant_id, enriched_lead],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Step 3: Routing
        if scoring_res.get("score", 0) > 80:
            await workflow.execute_activity(
                "route_to_sales_activity",
                args=[tenant_id, enriched_lead, scoring_res],
                start_to_close_timeout=timedelta(minutes=2)
            )

        return {
            "status": "scored",
            "score": scoring_res.get("score"),
            "category": scoring_res.get("category"),
            "timestamp": workflow.now().isoformat()
        }
