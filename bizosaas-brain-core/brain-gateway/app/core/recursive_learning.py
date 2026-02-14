import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.analytics_sync import get_analytics_sync_engine
from app.core.fine_tuning_pipeline import FineTuningPipeline
from app.core.vault import get_config_val, vault_service
from app.connectors.registry import ConnectorRegistry

logger = logging.getLogger(__name__)

class RecursiveLearningOrchestrator:
    """
    Coordinates the recursive learning cycle:
    Analytics Sync -> Dataset Export -> Fine-Tuning Job -> Model Handover
    """
    
    def __init__(self):
        self.fine_tuning_pipeline = FineTuningPipeline()

    async def run_learning_cycle(self, tenant_id: str = "default"):
        """
        Executes a full learning iteration for a tenant.
        """
        logger.info(f"🚀 Starting Recursive Learning Cycle for tenant: {tenant_id}")
        
        # 1. Sync Analytics (Ground Truth)
        try:
            sync_engine = await get_analytics_sync_engine()
            await sync_engine.sync_tenant(tenant_id)
            logger.info("✅ Step 1: Analytics Sync completed.")
        except Exception as e:
            logger.error(f"❌ Step 1 failed: Analytics Sync error: {e}")
            # We continue anyway if we have existing data in RAG
        
        # 2. Trigger Fine-Tuning Pipeline
        try:
            job_id = await self.fine_tuning_pipeline.run_pipeline(tenant_id=tenant_id)
            if job_id:
                logger.info(f"✅ Step 2: Fine-Tuning job triggered. Job ID: {job_id}")
                
                # 3. Register job for Handover (Passive monitoring)
                # In a real setup, we would use a webhook or a Temporal workflow
                # For this implementation, we'll store the pending job ID in Vault
                await self._register_pending_job(tenant_id, job_id)
                return job_id
            else:
                logger.warning("⚠️ Step 2: No job triggered (potentially no new high-quality data).")
                return None
        except Exception as e:
            logger.error(f"❌ Step 3 failed: Fine-tuning trigger error: {e}")
            return None

    async def _register_pending_job(self, tenant_id: str, job_id: str):
        """Store pending job ID in Vault for later handover check"""
        path = f"tenants/{tenant_id}/fine_tuning/pending"
        await vault_service.secret_adapter.store_secret(
            path=path,
            secret_data={"job_id": job_id, "status": "running", "timestamp": datetime.utcnow().isoformat()}
        )
        logger.info(f"Registered pending job {job_id} in Vault.")

    async def check_and_handover(self, tenant_id: str):
        """
        Checks if a pending job is finished and updates the MultiModelRouter.
        """
        path = f"tenants/{tenant_id}/fine_tuning/pending"
        pending = await vault_service.secret_adapter.get_secret(path)
        
        if not pending or pending.get("status") != "running":
            return
            
        job_id = pending.get("job_id")
        logger.info(f"Checking status for job {job_id}...")
        
        # Check Together AI status
        api_key = get_config_val("TOGETHER_AI_API_KEY")
        connector = ConnectorRegistry.create_connector("together_ai", tenant_id=tenant_id, credentials={"api_key": api_key})
        
        try:
            status_resp = await connector.perform_action("get_job", {"job_id": job_id})
            status = status_resp.get("status")
            
            if status == "completed":
                model_id = status_resp.get("model_id")
                logger.info(f"🎉 Job {job_id} completed! New model: {model_id}")
                
                # Update Handover
                target_path = f"tenants/{tenant_id}/fine_tuning/active_model"
                await vault_service.secret_adapter.store_secret(
                    path=target_path,
                    secret_data={"model_id": model_id, "job_id": job_id, "updated_at": datetime.utcnow().isoformat()}
                )
                
                # Mark pending as done
                await vault_service.secret_adapter.store_secret(
                    path=path,
                    secret_data={"job_id": job_id, "status": "done"}
                )
                
                logger.info(f"✅ Handover complete for {tenant_id}. System will now use {model_id}.")
                
            elif status == "failed":
                logger.error(f"❌ Job {job_id} failed.")
                await vault_service.secret_adapter.store_secret(
                    path=path,
                    secret_data={"job_id": job_id, "status": "failed"}
                )
        except Exception as e:
            logger.error(f"Handover check failed: {e}")

async def get_recursive_learning_orchestrator() -> RecursiveLearningOrchestrator:
    return RecursiveLearningOrchestrator()
