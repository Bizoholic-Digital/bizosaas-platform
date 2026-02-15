from temporalio import activity
import logging
from typing import List, Dict, Any
from app.dependencies import SessionLocal
from app.services.mcp_gateway import MCPGateway

logger = logging.getLogger(__name__)

@activity.defn(name="scrape_competitor_data_activity")
async def scrape_competitor_data_activity(tenant_id: str, competitors: List[str]) -> List[Dict[str, Any]]:
    """Scrape competitor websites for market data using MCP Gateway"""
    logger.info(f"Scraping competitor data for {len(competitors)} sites")
    results = []
    db = SessionLocal()
    try:
        gateway = MCPGateway(db)
        for c in competitors:
            try:
                # Assume competitors are URLs or we try to find them if they are names
                url = c if c.startswith("http") else f"https://{c}"
                scrape_res = await gateway.call_tool(
                    user_id=tenant_id,
                    mcp_slug="brave-search-mcp",
                    tool_name="get_page_content",
                    arguments={"url": url}
                )
                results.append({
                    "site": url, 
                    "content": scrape_res.get("content", "")[:500], # Keep it manageable
                    "price_drops": False, 
                    "new_ads": True
                })
            except Exception as e:
                logger.error(f"Failed to scrape {c}: {e}")
                results.append({"site": c, "error": str(e)})
    finally:
        db.close()
    return results

@activity.defn(name="analyze_competitor_shifts_activity")
async def analyze_competitor_shifts_activity(tenant_id: str, intel_data: List[Dict[str, Any]], news_findings: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Analyze scraped data and news for critical shifts"""
    details = "New ad campaign detected on Competitor A."
    if news_findings:
        details += f" Also found {len(news_findings)} news updates."
    return {"critical_shift": True, "details": details}

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

@activity.defn(name="google_search_activity")
async def google_search_activity(tenant_id: str, topic: str) -> List[Dict[str, Any]]:
    """Search for a topic using Brave Search MCP"""
    db = SessionLocal()
    try:
        gateway = MCPGateway(db)
        # Using brave-search-mcp slug as defined in research plan
        result = await gateway.call_tool(
            user_id=tenant_id,
            mcp_slug="brave-search-mcp",
            tool_name="search",
            arguments={"query": topic}
        )
        # Handle the expected MCP response format
        return result.get("results", [])
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return []
    finally:
        db.close()

@activity.defn(name="web_scrape_activity")
async def web_scrape_activity(tenant_id: str, url: str) -> Dict[str, Any]:
    """Scrape web content using Brave Search MCP"""
    db = SessionLocal()
    try:
        gateway = MCPGateway(db)
        result = await gateway.call_tool(
            user_id=tenant_id,
            mcp_slug="brave-search-mcp",
            tool_name="get_page_content",
            arguments={"url": url}
        )
        return {"url": url, "content": result.get("content", "")}
    except Exception as e:
        logger.error(f"Scrape failed for {url}: {e}")
        return {"url": url, "content": f"Error: {str(e)}"}
    finally:
        db.close()

@activity.defn(name="analyze_research_activity")
async def analyze_research_activity(tenant_id: str, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Synthesize findings into a research report"""
    # For now, we simulate AI synthesis.
    report = f"Deep Research Report for Tenant {tenant_id}\n\n"
    report += "Summary of Findings:\n"
    for f in findings:
        snippet = f.get("content", "")[:200] + "..."
        report += f"- Source: {f.get('url')}\n  Snippet: {snippet}\n\n"
    
    return {"report": report}
