from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

@workflow.defn
class RankTrackerWorkflow:
    @workflow.run
    async def run(self, tenant_id: str, domains: List[str], keywords: List[str]) -> Dict[str, Any]:
        """
        Autonomous SEO workflow that tracks keyword rankings for given domains.
        """
        # Step 1: Initialize SEO context via RAG
        seo_context = await workflow.execute_activity(
            "get_seo_context_activity",
            args=[tenant_id, keywords],
            start_to_close_timeout=timedelta(minutes=2)
        )

        # Step 2: Fetch current rankings for keywords
        rankings_data = await workflow.execute_activity(
            "fetch_keyword_rankings_activity",
            args=[domains, keywords],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Step 3: Analyze shifts and notify (if critical)
        await workflow.execute_activity(
            "analyze_ranking_shifts_activity",
            args=[tenant_id, rankings_data],
            start_to_close_timeout=timedelta(minutes=3)
        )

        return {
            "status": "completed",
            "keywords_tracked": len(keywords),
            "domains": domains,
            "timestamp": workflow.now().isoformat()
        }
