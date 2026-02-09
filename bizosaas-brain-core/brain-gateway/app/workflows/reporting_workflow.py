from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

@workflow.defn
class ClientReportingWorkflow:
    @workflow.run
    async def run(self, tenant_id: str, report_type: str = "weekly") -> Dict[str, Any]:
        """
        AI Performance Reporting Workflow:
        1. Aggregate data from GA4, Ads, Search Console.
        2. Generate AI insights and summary.
        3. Create PDF report.
        4. Deliver via Email/Slack.
        """
        # Step 1: Data Aggregation
        metrics = await workflow.execute_activity(
            "aggregate_performance_data_activity",
            args=[tenant_id, report_type],
            start_to_close_timeout=timedelta(minutes=10)
        )

        # Step 2: AI Insight Generation
        insights = await workflow.execute_activity(
            "generate_report_insights_activity",
            args=[tenant_id, metrics],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Step 3: PDF Generation
        pdf_info = await workflow.execute_activity(
            "generate_pdf_report_activity",
            args=[tenant_id, metrics, insights],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Step 4: Final Delivery
        await workflow.execute_activity(
            "deliver_client_report_activity",
            args=[tenant_id, pdf_info],
            start_to_close_timeout=timedelta(minutes=3)
        )

        return {
            "status": "delivered",
            "report_url": pdf_info.get("url"),
            "timestamp": workflow.now().isoformat()
        }
