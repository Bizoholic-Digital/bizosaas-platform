from temporalio import activity
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

@activity.defn(name="scrape_competitor_data_activity")
async def scrape_competitor_data_activity(tenant_id: str, competitors: List[str]) -> List[Dict[str, Any]]:
    """Scrape competitor websites for market data"""
    logger.info(f"Scraping competitor data for {len(competitors)} sites")
    return [{"site": c, "price_drops": False, "new_ads": True} for c in competitors]

@activity.defn(name="analyze_competitor_shifts_activity")
async def analyze_competitor_shifts_activity(tenant_id: str, intel_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze scraped data for critical shifts"""
    return {"critical_shift": True, "details": "New ad campaign detected on Competitor A."}

@activity.defn(name="trigger_intel_alert_activity")
async def trigger_intel_alert_activity(tenant_id: str, analysis: Dict[str, Any]) -> None:
    """Send alert to the tenant about competitor movements"""
    logger.warning(f"INTEL_ALERT for tenant {tenant_id}: {analysis['details']}")

@activity.defn(name="enrich_lead_data_activity")
async def enrich_lead_data_activity(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich lead data with company info, etc."""
    return {**lead_data, "company_size": "50-200", "industry": "Technology"}

@activity.defn(name="score_lead_activity")
async def score_lead_activity(tenant_id: str, lead: Dict[str, Any]) -> Dict[str, Any]:
    """Score lead using AI patterns"""
    return {"score": 85, "category": "hot"}

@activity.defn(name="route_to_sales_activity")
async def route_to_sales_activity(tenant_id: str, lead: Dict[str, Any], score: Dict[str, Any]) -> None:
    """Route lead to CRM/Sales team"""
    logger.info(f"Routing HOT LEAD {lead.get('email')} to sales for tenant {tenant_id}")
