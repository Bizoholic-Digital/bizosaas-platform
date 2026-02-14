import asyncio
import unittest
import json
from unittest.mock import MagicMock, patch, AsyncMock

# Mock dependencies before import
import sys
sys.modules['app.core.rag'] = MagicMock()
sys.modules['app.dependencies'] = MagicMock()

from app.core.analytics_sync import AnalyticsSyncEngine

class TestAnalyticsSync(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_secret_service = MagicMock()
        self.mock_secret_service.get_connector_credentials = AsyncMock()
        self.mock_secret_service.list_tenant_connectors = AsyncMock()
        self.engine = AnalyticsSyncEngine(self.mock_secret_service)

        
    @patch('app.core.analytics_sync.ConnectorRegistry')
    @patch('app.core.analytics_sync.rag_service')
    async def test_ga4_semanticizer(self, mock_rag, mock_registry):
        tenant_id = "test_tenant"
        mock_rag.ingest_knowledge = AsyncMock()
        
        # Mock connector data
        mock_connector = AsyncMock()
        mock_registry.create_connector.return_value = mock_connector
        mock_connector.sync_data.return_value = {
            "rows": [
                {
                    "dimensionValues": [{"value": "/home"}],
                    "metricValues": [{"value": "100"}]
                }
            ]
        }
        
        await self.engine._sync_ga4(tenant_id)
        
        # Verify RAG ingestion
        mock_rag.ingest_knowledge.assert_called_once()
        args, kwargs = mock_rag.ingest_knowledge.call_args
        content = args[0]
        metadata = args[1]
        
        self.assertIn("The page '/home' received 100 sessions", content)
        self.assertEqual(metadata["page"], "/home")
        self.assertEqual(metadata["sessions"], 100)
        self.assertEqual(kwargs["tenant_id"], tenant_id)

    @patch('app.core.analytics_sync.ConnectorRegistry')
    @patch('app.core.analytics_sync.rag_service')
    async def test_gsc_semanticizer(self, mock_rag, mock_registry):
        tenant_id = "test_tenant"
        mock_rag.ingest_knowledge = AsyncMock()
        
        # Mock connector data
        mock_connector = AsyncMock()
        mock_registry.create_connector.return_value = mock_connector
        mock_connector.sync_data.return_value = {
            "rows": [
                {
                    "keys": ["buy shoes", "https://site.com/shoes"],
                    "clicks": 50
                }
            ]
        }
        
        await self.engine._sync_gsc(tenant_id)
        
        # Verify RAG ingestion
        mock_rag.ingest_knowledge.assert_called_once()
        args, _ = mock_rag.ingest_knowledge.call_args
        content = args[0]
        self.assertIn("search query 'buy shoes' (50 clicks)", content)

    @patch('app.core.analytics_sync.ConnectorRegistry')
    @patch('app.core.analytics_sync.rag_service')
    async def test_shopify_semanticizer(self, mock_rag, mock_registry):
        tenant_id = "test_tenant"
        mock_rag.ingest_knowledge = AsyncMock() # Ensure it is awaitable
        
        # Mock connector data
        mock_connector = AsyncMock()
        mock_registry.create_connector.return_value = mock_connector
        mock_connector.sync_data.return_value = {
            "data": [
                {
                    "line_items": [{"title": "Blue T-Shirt"}]
                },
                {
                    "line_items": [{"title": "Blue T-Shirt"}]
                },
                {
                    "line_items": [{"title": "Red Cap"}]
                }
            ]
        }
        
        await self.engine._sync_shopify(tenant_id)
        
        # Verify RAG ingestion
        # Should have exactly two calls (one for T-shirt, one for Cap)
        self.assertEqual(mock_rag.ingest_knowledge.call_count, 2)

        
        # Check T-shirt call
        calls = mock_rag.ingest_knowledge.call_args_list
        tshirt_call = [c for c in calls if "Blue T-Shirt" in c[0][0]][0]
        self.assertIn("Blue T-Shirt' is a top seller with 2 recent orders", tshirt_call[0][0])


if __name__ == "__main__":
    unittest.main()
