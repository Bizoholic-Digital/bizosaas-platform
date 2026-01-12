from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any

# Activities are imported by the worker, but we reference them here by name
# check_fluent_crm_lead, tag_fluent_crm_contact, generate_ai_marketing_content

@workflow.defn
class LeadNurtureWorkflow:
    @workflow.run
    async def run(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        email = lead_data.get("email")
        
        # 1. Verification
        lead_info = await workflow.execute_activity(
            "check_fluent_crm_lead",
            {"email": email, "tenant_id": lead_data.get("tenant_id", "default")},
            start_to_close_timeout=timedelta(seconds=10)
        )
        
        # 2. Add 'bizoholic-prospect' tag
        await workflow.execute_activity(
            "tag_fluent_crm_contact",
            {"email": email, "tag": "bizoholic-prospect", "tenant_id": lead_data.get("tenant_id", "default")},
            start_to_close_timeout=timedelta(seconds=10)
        )
        
        # 3. Decision Point: First Touch
        content = await workflow.execute_activity(
            "generate_ai_marketing_content",
            {"user": lead_data, "tone": "professional", "goal": "nurture"},
            start_to_close_timeout=timedelta(seconds=60)
        )
        
        # 4. Wait for Engagement (Simulated)
        await workflow.sleep(timedelta(days=2))
        
        # 5. Follow-up Logic...
        return {
            "status": "nurturing",
            "lead": email,
            "days_active": 2
        }
