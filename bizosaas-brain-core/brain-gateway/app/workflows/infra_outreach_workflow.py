from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

@workflow.defn
class OutreachAutomationWorkflow:
    @workflow.run
    async def run(self, tenant_id: str, prospects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        AI Outreach Automation Workflow:
        1. Analyze prospect site (Digital Audit).
        2. Draft highly personalized AI outreach messages.
        3. Send messages via email/LinkedIn.
        4. Track follow-ups and responses.
        """
        # Step 1: Personalized Research
        prospect_research = await workflow.execute_activity(
            "research_prospects_activity",
            args=[prospects],
            start_to_close_timeout=timedelta(minutes=15)
        )

        # Step 2: AI Message Drafting
        drafts = await workflow.execute_activity(
            "draft_personalized_outreach_activity",
            args=[tenant_id, prospect_research],
            start_to_close_timeout=timedelta(minutes=10)
        )

        # Step 3: Delivery
        delivery_res = await workflow.execute_activity(
            "deliver_outreach_messages_activity",
            args=[tenant_id, drafts],
            start_to_close_timeout=timedelta(minutes=5)
        )

        return {
            "status": "outreached",
            "prospects_targeted": len(prospects),
            "successfully_sent": delivery_res.get("sent_count"),
            "timestamp": workflow.now().isoformat()
        }

@workflow.defn
class AutoSSLMaintenanceWorkflow:
    @workflow.run
    async def run(self, domains: List[str]) -> Dict[str, Any]:
        """
        Infrastructure Reliability Workflow:
        1. Check SSL certificate expiration for all domains.
        2. Trigger renewal if within threshold (e.g., 30 days).
        3. Verify successful renewal and propagation.
        """
        while True:
            for domain in domains:
                # Step 1: Check Expiry
                expiry_status = await workflow.execute_activity(
                    "check_ssl_expiry_activity",
                    args=[domain],
                    start_to_close_timeout=timedelta(seconds=30)
                )

                # Step 2: Trigger Renewal if needed
                if expiry_status.get("days_left") < 30:
                    await workflow.execute_activity(
                        "renew_ssl_certificate_activity",
                        args=[domain],
                        start_to_close_timeout=timedelta(minutes=10)
                    )

                # Step 3: Verify Propagation
                await workflow.execute_activity(
                    "verify_ssl_propagation_activity",
                    args=[domain],
                    start_to_close_timeout=timedelta(minutes=5)
                )
            
            # Sleep for 24 hours before next check
            await workflow.sleep(timedelta(hours=24))
