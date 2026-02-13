from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, Optional, List

# Define the workflow
@workflow.defn
class ContentCreationWorkflow:
    """
    Phased Content Creation Workflow:
    1. Research: Deep research on a given topic/keywords.
    2. Outline: Generate a structured outline.
    3. HITL Gate: Wait for client approval or revision on outline.
    4. Writing: Generate full-length draft based on approved outline.
    5. SEO: Optimize draft with meta tags and schema.
    6. Quality Check: Score and verify content accuracy.
    7. HITL Gate: Final client approval.
    8. Publishing: Push to designated CMS (Wagtail, WP).
    """

    def __init__(self) -> None:
        self._approval_status: Optional[str] = None
        self._revision_notes: Optional[str] = None
        self._current_phase: str = "started"

    @workflow.signal
    async def approve_phase(self, phase: str, notes: str = "") -> None:
        self._approval_status = "approved"
        self._revision_notes = notes

    @workflow.signal
    async def request_revision(self, phase: str, notes: str) -> None:
        self._approval_status = "revision"
        self._revision_notes = notes

    @workflow.query
    def get_current_phase(self) -> str:
        return self._current_phase

    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tenant_id = params.get("tenant_id")
        topic = params.get("topic")
        persona_id = params.get("persona_id")
        require_approval = params.get("require_approval", True)
        
        # 1. Research
        self._current_phase = "researching"
        research = await workflow.execute_activity(
            "content_research_activity",
            args=[{"tenant_id": tenant_id, "topic": topic}],
            start_to_close_timeout=timedelta(minutes=10)
        )
        
        # 2. Outline Generation
        self._current_phase = "outlining"
        outline = await workflow.execute_activity(
            "generate_content_outline_activity",
            args=[{"tenant_id": tenant_id, "research": research, "persona_id": persona_id}],
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        # 3. HITL - Outline Approval
        if require_approval:
            self._current_phase = "awaiting_outline_approval"
            # Create a task in the HITL system
            await workflow.execute_activity(
                "create_approval_task_activity",
                args=[{"tenant_id": tenant_id, "type": "outline", "content": outline}],
                start_to_close_timeout=timedelta(seconds=60)
            )
            
            # Wait for signal
            await workflow.wait_condition(lambda: self._approval_status is not None)
            
            if self._approval_status == "revision":
                self._current_phase = "revising_outline"
                outline = await workflow.execute_activity(
                    "revise_content_outline_activity",
                    args=[{"tenant_id": tenant_id, "current_outline": outline, "notes": self._revision_notes}],
                    start_to_close_timeout=timedelta(minutes=5)
                )
                self._approval_status = None # Reset for next phase
            else:
                self._approval_status = None # Reset for next phase

        # 4. Writing Draft
        self._current_phase = "writing"
        draft = await workflow.execute_activity(
            "write_full_content_activity",
            args=[{"tenant_id": tenant_id, "outline": outline, "persona_id": persona_id}],
            start_to_close_timeout=timedelta(minutes=15)
        )
        
        # 5. SEO Optimization
        self._current_phase = "optimizing"
        optimized_content = await workflow.execute_activity(
            "seo_optimize_content_activity",
            args=[{"tenant_id": tenant_id, "draft": draft}],
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        # 6. Quality & Accuracy Scoring
        self._current_phase = "checking_quality"
        quality_score = await workflow.execute_activity(
            "score_content_quality_activity",
            args=[{"content": optimized_content}],
            start_to_close_timeout=timedelta(minutes=3)
        )
        
        # 7. HITL - Final Approval
        if require_approval:
            self._current_phase = "awaiting_final_approval"
            await workflow.execute_activity(
                "create_approval_task_activity",
                args=[{"tenant_id": tenant_id, "type": "final_draft", "content": optimized_content}],
                start_to_close_timeout=timedelta(seconds=60)
            )
            
            await workflow.wait_condition(lambda: self._approval_status is not None)
            
            if self._approval_status == "revision":
                self._current_phase = "revising_draft"
                optimized_content = await workflow.execute_activity(
                    "revise_full_content_activity",
                    args=[{"tenant_id": tenant_id, "current_content": optimized_content, "notes": self._revision_notes}],
                    start_to_close_timeout=timedelta(minutes=10)
                )

        # 8. Publishing
        self._current_phase = "publishing"
        publish_res = await workflow.execute_activity(
            "publish_content_activity",
            args=[{"tenant_id": tenant_id, "content": optimized_content, "target": params.get("target_cms", "wagtail")}],
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        self._current_phase = "completed"
        return {
            "status": "completed",
            "publish_results": publish_res,
            "quality_score": quality_score
        }

@workflow.defn
class ContentCalendarWorkflow:
    """
    Monthly Content Planning & Orchestration:
    1. Analyze audience and trends.
    2. Generate a 30-day content calendar.
    3. Spawn child ContentCreationWorkflows for each topic.
    """
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tenant_id = params.get("tenant_id")
        
        # 1. Generate Calendar
        topics = await workflow.execute_activity(
            "generate_monthly_calendar_activity",
            args=[{"tenant_id": tenant_id}],
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        # 2. Spawn Child Workflows
        child_workflow_ids = []
        for topic_info in topics:
            child_id = f"content-{tenant_id}-{topic_info['slug']}"
            await workflow.execute_child_workflow(
                ContentCreationWorkflow.run,
                topics=topic_info,
                id=child_id,
            )
            child_workflow_ids.append(child_id)
            
        return {
            "status": "calendar_initiated",
            "topics_count": len(topics),
            "workflow_ids": child_workflow_ids
        }
