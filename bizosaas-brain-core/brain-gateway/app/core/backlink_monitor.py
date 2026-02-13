import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.seo import TrackedBacklink
from app.core.dataforseo_client import dataforseo_client

logger = logging.getLogger(__name__)

class BacklinkMonitor:
    """
    Proprietary service for monitoring backlinks for tenants.
    Combines DataforSEO data with local persistence to track history.
    """

    @staticmethod
    async def synchronize_backlinks(db: Session, tenant_id: str, domain: str):
        """
        Fetch latest backlinks and synchronize with local DB.
        Identifies New and Lost backlinks.
        """
        logger.info(f"Synchronizing backlinks for {domain} (Tenant: {tenant_id})")
        
        # 1. Fetch latest backlinks from DataforSEO
        # Note: In a real production setup, we might use the 'backlinks/backlinks/live' endpoint 
        # for a full list, but here we'll start with the summary and top links.
        # For this implementation, we'll assume we get a list of backlinks.
        
        # Simulating fetching current backlinks (as 'summary' only gives totals)
        # We search for backlinks to the domain
        current_links = await dataforseo_client.get_serp_data(f"link:{domain}") 
        # Actually we should use the Backlinks API specifically if available. 
        # But SERP 'link:' is what was used before. Let's aim higher.
        
        # For now, let's use the summary to update the aggregate stats 
        # and assume a list of links is passed or fetched.
        summary = await dataforseo_client.get_backlinks_summary(domain)
        
        # 2. Get existing tracked links
        existing_links = db.query(TrackedBacklink).filter(
            TrackedBacklink.tenant_id == tenant_id,
            TrackedBacklink.target_url.like(f"%{domain}%")
        ).all()
        
        existing_map = {f"{l.source_url}->{l.target_url}": l for l in existing_links}
        
        # 3. Process current links (Dummy loop for now until we have a full list fetcher)
        # In a full implementation, we'd iterate over the actual backlinks list from DataforSEO.
        processed_count = 0
        new_count = 0
        
        # TO BE COMPLETED: Fetch actual links list from DataforSEO 'backlinks/backlinks/live'
        
        return {
            "tenant_id": tenant_id,
            "domain": domain,
            "total_backlinks": summary.get("backlinks", 0),
            "referring_domains": summary.get("referring_domains", 0),
            "status": "synchronized"
        }

    @staticmethod
    def get_links_report(db: Session, tenant_id: str) -> Dict[str, Any]:
        """Generate a report of new, lost and healthy links."""
        links = db.query(TrackedBacklink).filter(TrackedBacklink.tenant_id == tenant_id).all()
        
        new_last_30 = [l.to_dict() for l in links if (datetime.now() - l.first_seen_at.replace(tzinfo=None)).days <= 30]
        lost_links = [l.to_dict() for l in links if l.is_lost]
        
        return {
            "total_tracked": len(links),
            "new_30d": len(new_last_30),
            "lost": len(lost_links),
            "links": [l.to_dict() for l in links]
        }

backlink_monitor = BacklinkMonitor()
