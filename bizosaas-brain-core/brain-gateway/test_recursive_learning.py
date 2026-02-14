import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio
from datetime import datetime
import sys

# Mock dependencies BEFORE importing application code
mock_langcache = MagicMock()
sys.modules["langcache"] = mock_langcache

# Mock semantic_cache to avoid Redis connection issues
mock_semantic_cache = MagicMock()
sys.modules["app.core.semantic_cache"] = mock_semantic_cache

# Mock app.dependencies and sqlalchemy.event
sys.modules["app.dependencies"] = MagicMock()
sys.modules["sqlalchemy.event"] = MagicMock()

# Mock FineTuningPipeline and other IO-heavy components
with patch("app.core.fine_tuning_pipeline.sa.create_engine"), \
     patch("app.core.analytics_sync.sa.create_engine"):
    from app.core.recursive_learning import RecursiveLearningOrchestrator
from app.core.intelligence import _select_llm_config

class TestRecursiveLearning(unittest.IsolatedAsyncioTestCase):
    @patch("app.core.recursive_learning.FineTuningPipeline")
    def setUp(self, mock_pipeline_class):
        self.orchestrator = RecursiveLearningOrchestrator()
        # The orchestrator's pipeline is now a mock
        self.mock_pipeline = self.orchestrator.fine_tuning_pipeline

    @patch("app.core.recursive_learning.vault_service")
    @patch("app.core.recursive_learning.get_analytics_sync_engine")
    async def test_run_learning_cycle(self, mock_get_sync, mock_vault):
        tenant_id = "test_tenant"
        job_id = "ft-job-123"
        
        # Mock Sync Engine
        mock_sync = AsyncMock()
        mock_get_sync.return_value = mock_sync
        
        # Mock Pipeline
        self.mock_pipeline.run_pipeline = AsyncMock(return_value=job_id)
        
        # Mock Vault
        mock_vault.secret_adapter = MagicMock()
        mock_vault.secret_adapter.store_secret = AsyncMock()
        
        result = await self.orchestrator.run_learning_cycle(tenant_id)
        
        self.assertEqual(result, job_id)
        mock_sync.sync_tenant.assert_called_once_with(tenant_id)
        self.mock_pipeline.run_pipeline.assert_called_once_with(tenant_id=tenant_id)
        
        # Verify job registration in Vault
        mock_vault.secret_adapter.store_secret.assert_called_once()
        args, kwargs = mock_vault.secret_adapter.store_secret.call_args
        self.assertIn(f"tenants/{tenant_id}/fine_tuning/pending", kwargs["path"])
        self.assertEqual(kwargs["secret_data"]["job_id"], job_id)

    @patch("app.core.recursive_learning.vault_service")
    @patch("app.core.recursive_learning.ConnectorRegistry")
    @patch("app.core.recursive_learning.get_config_val")
    async def test_handover_success(self, mock_get_config, mock_registry, mock_vault):
        tenant_id = "test_tenant"
        job_id = "ft-job-123"
        model_id = "together:llama-fine-tuned-v1"
        
        # Mock pending job in Vault
        mock_vault.secret_adapter.get_secret = AsyncMock(return_value={
            "job_id": job_id, "status": "running"
        })
        mock_vault.secret_adapter.store_secret = AsyncMock()
        
        # Mock Together AI Connector
        mock_connector = AsyncMock()
        mock_registry.create_connector.return_value = mock_connector
        mock_connector.perform_action.return_value = {
            "status": "completed",
            "model_id": model_id
        }
        
        await self.orchestrator.check_and_handover(tenant_id)
        
        # Verify active_model update in Vault
        self.assertEqual(mock_vault.secret_adapter.store_secret.call_count, 2)
        
        calls = mock_vault.secret_adapter.store_secret.call_args_list
        active_model_call = [c for c in calls if "active_model" in c[1]["path"]][0]
        self.assertEqual(active_model_call[1]["secret_data"]["model_id"], model_id)

    @patch("app.core.intelligence.vault_service")
    async def test_router_handover_integration(self, mock_vault):
        tenant_id = "test_tenant"
        model_id = "together:llama-fine-tuned-v1"
        
        # Mock Vault response for active model
        mock_vault.secret_adapter.get_secret = AsyncMock(return_value={
            "model_id": model_id
        })
        
        # Test routing for this tenant
        config = await _select_llm_config("content_writer", "Write a blog post", tenant_id=tenant_id)
        
        self.assertEqual(config["model_name"], model_id)
        self.assertEqual(config["model_provider"], "together_ai")
        
        # Test fallback for other tenants
        mock_vault.secret_adapter.get_secret = AsyncMock(return_value=None)
        config_fallback = await _select_llm_config("content_writer", "Write a blog post", tenant_id="other")
        self.assertNotEqual(config_fallback["model_name"], model_id)

if __name__ == "__main__":
    unittest.main()
