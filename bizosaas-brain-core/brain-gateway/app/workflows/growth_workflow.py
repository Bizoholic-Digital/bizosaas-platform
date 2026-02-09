from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

@workflow.defn
class SocialListeningWorkflow:
    @workflow.run
    async def run(self, tenant_id: str, keywords: List[str]) -> Dict[str, Any]:
        """
        Social Listening Workflow:
        1. Monitor social media and web for brand mentions/keywords.
        2. Analyze sentiment and relevance of mentions.
        3. Draft AI engagement responses for proactive marketing.
        """
        # Step 1: Monitor Mentions
        mentions = await workflow.execute_activity(
            "monitor_brand_mentions_activity",
            args=[tenant_id, keywords],
            start_to_close_timeout=timedelta(minutes=10)
        )

        # Step 2: Analyze Mentions
        analyzed_mentions = await workflow.execute_activity(
            "analyze_mentions_activity",
            args=[tenant_id, mentions],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Step 3: Draft Proactive Responses
        engagement_drafts = await workflow.execute_activity(
            "draft_proactive_engagement_activity",
            args=[tenant_id, analyzed_mentions],
            start_to_close_timeout=timedelta(minutes=5)
        )

        return {
            "status": "monitored",
            "mentions_found": len(mentions),
            "engagement_opportunities": len(engagement_drafts),
            "timestamp": workflow.now().isoformat()
        }

@workflow.defn
class TopicalClusterWorkflow:
    @workflow.run
    async def run(self, tenant_id: str, main_topic: str) -> Dict[str, Any]:
        """
        Topical Clustering Workflow:
        1. Research sub-topics and long-tail keywords for a main pillar topic.
        2. Group keywords into topical clusters.
        3. Generate a content hierarchy and internal linking plan.
        """
        # Step 1: Keyword Research
        keywords = await workflow.execute_activity(
            "research_topical_keywords_activity",
            args=[main_topic],
            start_to_close_timeout=timedelta(minutes=10)
        )

        # Step 2: Cluster Keywords
        clusters = await workflow.execute_activity(
            "cluster_keywords_activity",
            args=[keywords],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Step 3: Generate Content Plan
        content_plan = await workflow.execute_activity(
            "generate_topical_content_plan_activity",
            args=[tenant_id, main_topic, clusters],
            start_to_close_timeout=timedelta(minutes=10)
        )

        return {
            "status": "planned",
            "main_topic": main_topic,
            "clusters_created": len(clusters),
            "plan_url": content_plan.get("url"),
            "timestamp": workflow.now().isoformat()
        }
