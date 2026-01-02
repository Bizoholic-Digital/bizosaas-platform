import asyncio
from datetime import timedelta
from typing import Dict, Any
from temporalio import workflow

# Import activities
with workflow.unsafe.imports_passed_through():
    from app.activities.audit_activities import (
        perform_seo_audit,
        perform_social_audit,
        perform_ppc_audit,
        generate_audit_report
    )

@workflow.def
class DigitalPresenceAuditWorkflow:
    @workflow.run
    async def run(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Background workflow to audit a company's digital presence.
        1. SEO Audit (website content, speed, meta tags)
        2. Social Audit (platforms, engagement, frequency)
        3. PPC Audit (ads, landing pages)
        4. Consolidated Report Generation
        """
        
        # Parallel execution of audits
        seo_task = workflow.execute_activity(
            perform_seo_audit,
            company_data,
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        social_task = workflow.execute_activity(
            perform_social_audit,
            company_data,
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        ppc_task = workflow.execute_activity(
            perform_ppc_audit,
            company_data,
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        # Wait for all audits to complete
        seo_results, social_results, ppc_results = await asyncio.gather(
            seo_task, social_task, ppc_task
        )
        
        # Generate consolidated report
        final_report = await workflow.execute_activity(
            generate_audit_report,
            {
                "company": company_data,
                "seo": seo_results,
                "social": social_results,
                "ppc": ppc_results
            },
            start_to_close_timeout=timedelta(minutes=2)
        )
        
        return final_report
