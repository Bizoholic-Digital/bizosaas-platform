import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.connectors.registry import ConnectorRegistry
from app.core.rag import rag_service
from app.dependencies import get_secret_service
from app.domain.services.secret_service import SecretService

logger = logging.getLogger(__name__)

class AnalyticsSyncEngine:
    """
    Syncs data from client analytics (GA4, GSC, Shopify) 
    and converts them into semantic KAG patterns in RAG.
    """
    
    def __init__(self, secret_service: SecretService):
        self.secret_service = secret_service

    async def sync_tenant(self, tenant_id: str):
        """Perform full sync for a specific tenant"""
        logger.info(f"Starting analytics sync for tenant: {tenant_id}")
        
        # 1. Discover active connectors
        connector_ids = await self.secret_service.list_tenant_connectors(tenant_id)
        
        tasks = []
        if "google-analytics" in connector_ids:
            tasks.append(self._sync_ga4(tenant_id))
        if "google-search-console" in connector_ids:
            tasks.append(self._sync_gsc(tenant_id))
        if "shopify" in connector_ids:
            tasks.append(self._sync_shopify(tenant_id))
            
        if not tasks:
            logger.info(f"No analytics connectors found for tenant {tenant_id}")
            return
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in results:
            if isinstance(res, Exception):
                logger.error(f"Sync task failed: {res}")

    async def _sync_ga4(self, tenant_id: str):
        """Sync and semanticize GA4 data"""
        logger.info(f"Syncing GA4 for {tenant_id}")
        creds = await self.secret_service.get_connector_credentials(tenant_id, "google-analytics")
        connector = ConnectorRegistry.create_connector("google-analytics", tenant_id, creds)
        
        # Get basic report for top pages
        try:
            report = await connector.sync_data("basic_report")
            rows = report.get("rows", [])
            
            for row in rows[:10]:  # Semanticize top 10 pages
                page = row.get("dimensionValues", [{}])[0].get("value", "unknown")
                sessions = row.get("metricValues", [{}])[0].get("value", "0")
                
                content = f"Traffic Insight: The page '{page}' received {sessions} sessions in the last 30 days."
                metadata = {
                    "source": "analytics_insight",
                    "type": "traffic",
                    "connector": "ga4",
                    "page": page,
                    "sessions": int(sessions)
                }
                
                await rag_service.ingest_knowledge(content, metadata, tenant_id=tenant_id)
                
        except Exception as e:
            logger.error(f"GA4 Semanticizer failed: {e}")

    async def _sync_gsc(self, tenant_id: str):
        """Sync and semanticize Google Search Console data"""
        logger.info(f"Syncing GSC for {tenant_id}")
        creds = await self.secret_service.get_connector_credentials(tenant_id, "google-search-console")
        connector = ConnectorRegistry.create_connector("google-search-console", tenant_id, creds)
        
        try:
            # Sync performance with query/page dimensions
            performance = await connector.sync_data("performance", params={"dimensions": ["query", "page"]})
            rows = performance.get("rows", [])
            
            for row in rows[:15]:  # Semanticize top 15 queries
                query = row.get("keys", [""])[0]
                page = row.get("keys", ["", ""])[1]
                clicks = row.get("clicks", 0)
                
                content = f"Search Intent: Users are finding the page '{page}' using the search query '{query}' ({clicks} clicks)."
                metadata = {
                    "source": "analytics_insight",
                    "type": "search_intent",
                    "connector": "gsc",
                    "query": query,
                    "page": page,
                    "clicks": clicks
                }
                
                await rag_service.ingest_knowledge(content, metadata, tenant_id=tenant_id)
                
        except Exception as e:
            logger.error(f"GSC Semanticizer failed: {e}")

    async def _sync_shopify(self, tenant_id: str):
        """Sync and semanticize Shopify order/product data"""
        logger.info(f"Syncing Shopify for {tenant_id}")
        creds = await self.secret_service.get_connector_credentials(tenant_id, "shopify")
        connector = ConnectorRegistry.create_connector("shopify", tenant_id, creds)
        
        try:
            # Sync orders to see what's selling
            orders_data = await connector.sync_data("orders", params={"status": "any", "limit": 50})
            orders = orders_data.get("data", [])
            
            product_counts = {}
            for order in orders:
                for item in order.get("line_items", []):
                    name = item.get("title")
                    product_counts[name] = product_counts.get(name, 0) + 1
            
            # Semanticize top sellers
            sorted_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)
            for name, count in sorted_products[:10]:
                content = f"Product Momentum: '{name}' is a top seller with {count} recent orders."
                metadata = {
                    "source": "analytics_insight",
                    "type": "momentum",
                    "connector": "shopify",
                    "product": name,
                    "sales_count": count
                }
                
                await rag_service.ingest_knowledge(content, metadata, tenant_id=tenant_id)
                
        except Exception as e:
            logger.error(f"Shopify Semanticizer failed: {e}")

# Factory function for dependency injection
async def get_analytics_sync_engine() -> AnalyticsSyncEngine:
    secret_service = await get_secret_service()
    return AnalyticsSyncEngine(secret_service)
