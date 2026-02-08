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

@workflow.defn
class MarketingCampaignWorkflow:
    @workflow.run
    async def run(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate a multi-channel social media campaign."""
        topic = campaign_data.get("topic")
        platforms = campaign_data.get("platforms", ["instagram", "linkedin"])
        tenant_id = campaign_data.get("tenant_id", "default")
        
        # 1. Generate Content
        gen_result = await workflow.execute_activity(
            "generate_social_posts",
            {"topic": topic, "platforms": platforms},
            start_to_close_timeout=timedelta(seconds=60)
        )
        
        # 2. Wait for Approval (Wait 5 mins for simulation, or could use Signals)
        # For now, we auto-approve if topic is not 'high-risk'
        posts = gen_result.get("posts", {})
        
        # 3. Publish
        publish_result = await workflow.execute_activity(
            "publish_to_social_channels",
            {"posts": posts, "tenant_id": tenant_id},
            start_to_close_timeout=timedelta(seconds=60)
        )
        
        return {
            "status": "campaign_completed",
            "topic": topic,
            "published_count": publish_result.get("published_count", 0),
            "platforms": platforms
        }

@workflow.defn
class AdOrchestrationWorkflow:
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Automatically manage and optimize ad budgets across channels."""
        tenant_id = params.get("tenant_id", "default")
        current_budgets = params.get("current_budgets", {})
        
        # 1. Run Optimization Activity
        result = await workflow.execute_activity(
            "optimize_ad_budgets",
            {"tenant_id": tenant_id, "current_budgets": current_budgets},
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        # 2. In a real scenario, this would loop or schedule next run
        # await workflow.sleep(timedelta(days=1))
        
        return {
            "status": "optimization_complete",
            "new_budgets": result.get("new_budgets"),
            "recommendations": result.get("recommendations")
        }
