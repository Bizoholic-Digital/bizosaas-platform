from temporalio import workflow
from datetime import timedelta
from typing import Dict, Any, List, Optional

with workflow.unsafe.imports_passed_through():
    from app.activities.social_content import (
        generate_twitter_post_activity,
        generate_linkedin_post_activity,
        generate_instagram_facebook_activity,
        schedule_social_post_activity
    )
    from app.activities.content_pipeline import create_approval_task_activity

@workflow.defn
class SocialContentWorkflow:
    def __init__(self) -> None:
        self._status = "initializing"
        self._approved = False
        self._revision_notes = ""
        self._final_content = None

    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tenant_id = params.get("tenant_id")
        platform = params.get("platform", "twitter").lower()
        topic = params.get("topic")
        
        # 1. Generation Phase
        self._status = "generating"
        activity_map = {
            "twitter": generate_twitter_post_activity,
            "x": generate_twitter_post_activity,
            "linkedin": generate_linkedin_post_activity,
            "instagram": generate_instagram_facebook_activity,
            "facebook": generate_instagram_facebook_activity
        }
        
        target_activity = activity_map.get(platform, generate_twitter_post_activity)
        
        draft = await workflow.execute_activity(
            target_activity,
            params,
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        self._final_content = draft
        
        # 2. HITL Approval Phase
        if params.get("require_approval", True):
            self._status = "awaiting_approval"
            # Create a task for the human in the loop
            await workflow.execute_activity(
                create_approval_task_activity,
                {
                    "tenant_id": tenant_id,
                    "type": f"social_post_{platform}",
                    "content": draft,
                    "workflow_id": workflow.info().workflow_id
                },
                start_to_close_timeout=timedelta(minutes=1)
            )
            
            # Wait for signal (up to 7 days)
            await workflow.wait_condition(lambda: self._approved or self._revision_notes != "", timeout=timedelta(days=7))
            
            if not self._approved:
                self._status = "revising"
                # If revision notes are provided, we could re-run generation with notes.
                # For Phase 4 MVP, we'll mark as revised and end.
                return {"status": "revision_requested", "notes": self._revision_notes}

        # 3. Scheduling Phase
        self._status = "scheduling"
        schedule_result = await workflow.execute_activity(
            schedule_social_post_activity,
            {
                "tenant_id": tenant_id,
                "platform": platform,
                "content": self._final_content,
                "scheduled_at": params.get("scheduled_at")
            },
            start_to_close_timeout=timedelta(minutes=2)
        )
        
        self._status = "completed"
        return {
            "status": "published",
            "platform": platform,
            "result": schedule_result,
            "content": self._final_content
        }

    @workflow.signal
    async def approve_post(self, notes: Optional[str] = None) -> None:
        self._approved = True

    @workflow.signal
    async def request_revision(self, notes: str) -> None:
        self._revision_notes = notes

    @workflow.query
    def get_status(self) -> str:
        return self._status

    @workflow.query
    def get_draft(self) -> Any:
        return self._final_content
