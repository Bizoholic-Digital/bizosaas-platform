from temporalio import activity
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

@activity.defn(name="aggregate_performance_data_activity")
async def aggregate_performance_data_activity(tenant_id: str, report_type: str) -> Dict[str, Any]:
    """Aggregate data from multiple sources"""
    logger.info(f"Aggregating {report_type} data for tenant {tenant_id}")
    return {
        "visitors": 1500,
        "conversions": 45,
        "ad_spend": 250.0,
        "top_keywords": ["ai marketing", "saas automation"]
    }

@activity.defn(name="generate_report_insights_activity")
async def generate_report_insights_activity(tenant_id: str, metrics: Dict[str, Any]) -> str:
    """Generate AI-driven insights from metrics"""
    logger.info(f"Generating insights for tenant {tenant_id}")
    return f"Your traffic increased by 15% this week! Focusing on the keyword 'ai marketing' is yielding high ROI."

@activity.defn(name="generate_pdf_report_activity")
async def generate_pdf_report_activity(tenant_id: str, metrics: Dict[str, Any], insights: str) -> Dict[str, Any]:
    """Generate the actual PDF file"""
    logger.info(f"Generating PDF report for tenant {tenant_id}")
    return {
        "url": f"https://cdn.bizoholic.net/reports/{tenant_id}/report-{activity.info().workflow_id}.pdf",
        "file_id": "rep_123456"
    }

@activity.defn(name="deliver_client_report_activity")
async def deliver_client_report_activity(tenant_id: str, pdf_info: Dict[str, Any]) -> None:
    """Deliver the report to the client via email/slack"""
    logger.info(f"Delivering report for tenant {tenant_id} to URL: {pdf_info['url']}")
