from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

@workflow.defn
class ReputationManagementWorkflow:
    @workflow.run
    async def run(self, tenant_id: str, platforms: List[str]) -> Dict[str, Any]:
        """
        Autonomous Reputation Management workflow:
        1. Scrape latest reviews from GMB, Yelp, etc.
        2. Analyze sentiment and classify reviews.
        3. Draft AI-personalized responses.
        4. Publish or queue for review based on HITL settings.
        """
        # Step 1: Fetch Latest Reviews
        reviews = await workflow.execute_activity(
            "fetch_latest_reviews_activity",
            args=[tenant_id, platforms],
            start_to_close_timeout=timedelta(minutes=5)
        )

        if not reviews:
            return {"status": "no_new_reviews", "count": 0}

        # Step 2: Analyze and Draft Responses
        processed_reviews = await workflow.execute_activity(
            "process_reviews_and_draft_responses_activity",
            args=[tenant_id, reviews],
            start_to_close_timeout=timedelta(minutes=10)
        )

        # Step 3: Handle Based on HITL (Implicit in Activity or Signal)
        # For simplicity, we assume the activity handles initial status (PENDING_REVIEW)
        # If HITL is disabled, it can push immediately
        
        publish_result = await workflow.execute_activity(
            "publish_review_responses_activity",
            args=[tenant_id, processed_reviews],
            start_to_close_timeout=timedelta(minutes=5)
        )

        return {
            "status": "completed",
            "reviews_processed": len(reviews),
            "responses_published": publish_result.get("published_count", 0),
            "timestamp": workflow.now().isoformat()
        }
