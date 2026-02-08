"""
Temporal Workflow Executor
Deploys and manages approved workflows using Temporal.
"""

import asyncio
from typing import Dict, Any, Optional
from datetime import timedelta
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker
import logging

logger = logging.getLogger(__name__)


@activity.defn
async def execute_workflow_step(step_definition: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a single workflow step based on its definition.
    This is the atomic unit of workflow execution.
    """
    action = step_definition.get("action")
    
    if action == "wait":
        duration = step_definition.get("duration", "1h")
        # Parse duration (e.g., "1h", "24h", "30m")
        await asyncio.sleep(_parse_duration(duration))
        return {"status": "completed", "action": action}
    
    elif action == "llm_generate":
        # Call LLM service to generate content
        from app.core.llm_service import generate_content
        prompt = step_definition.get("prompt")
        context = step_definition.get("context", [])
        result = await generate_content(prompt, context)
        return {"status": "completed", "action": action, "output": result}
    
    elif action == "send_email":
        # Send email via email service
        from app.services.email_service import send_email
        template = step_definition.get("template")
        recipient = step_definition.get("recipient")
        await send_email(template, recipient)
        return {"status": "completed", "action": action}
    
    elif action == "send_sms":
        # Send SMS via communication service
        from app.services.sms_service import send_sms
        message = step_definition.get("message")
        phone = step_definition.get("phone")
        await send_sms(message, phone)
        return {"status": "completed", "action": action}
    
    elif action == "post_to_linkedin":
        # Post to LinkedIn via MCP
        from app.services.mcp_executor import execute_mcp_action
        result = await execute_mcp_action("linkedin", "create_post", step_definition)
        return {"status": "completed", "action": action, "result": result}
    
    elif action == "crawl_site":
        # Crawl website for SEO analysis
        from app.services.seo_crawler import crawl_site
        depth = step_definition.get("depth", 3)
        result = await crawl_site(depth)
        return {"status": "completed", "action": action, "pages_crawled": result}
    
    elif action == "fetch_inventory":
        # Fetch inventory from e-commerce platform
        from app.services.inventory_service import fetch_inventory
        platform = step_definition.get("from")
        inventory = await fetch_inventory(platform)
        return {"status": "completed", "action": action, "inventory": inventory}
    
    elif action == "update_inventory":
        # Update inventory across platforms
        from app.services.inventory_service import update_inventory
        platforms = step_definition.get("on", [])
        delta = step_definition.get("delta")
        await update_inventory(platforms, delta)
        return {"status": "completed", "action": action}
    
    else:
        logger.warning(f"Unknown action: {action}")
        return {"status": "skipped", "action": action, "reason": "unknown_action"}


@workflow.defn
class AgenticWorkflow:
    """
    Temporal workflow that executes agent-proposed automation sequences.
    """
    
    @workflow.run
    async def run(self, workflow_blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete workflow based on the blueprint.
        """
        workflow_id = workflow.info().workflow_id
        logger.info(f"Starting agentic workflow: {workflow_id}")
        
        steps = workflow_blueprint.get("steps", [])
        config = workflow_blueprint.get("config", {})
        results = []
        
        for i, step in enumerate(steps):
            logger.info(f"Executing step {i+1}/{len(steps)}: {step.get('action')}")
            
            # Check for conditional execution
            condition = step.get("condition")
            if condition and not await self._evaluate_condition(condition, results):
                logger.info(f"Skipping step {i+1} due to condition: {condition}")
                continue
            
            # Execute step with retry logic
            max_retries = config.get("max_retries", 3)
            timeout = config.get("timeout", 30)
            
            for attempt in range(max_retries):
                try:
                    result = await workflow.execute_activity(
                        execute_workflow_step,
                        step,
                        start_to_close_timeout=timedelta(seconds=timeout)
                    )
                    results.append(result)
                    break
                except Exception as e:
                    logger.error(f"Step {i+1} failed (attempt {attempt+1}/{max_retries}): {e}")
                    if attempt == max_retries - 1:
                        # Final attempt failed
                        if config.get("notifyOnError", True):
                            await self._notify_admin_error(workflow_id, step, str(e))
                        raise
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        logger.info(f"Workflow {workflow_id} completed successfully")
        return {
            "status": "completed",
            "workflow_id": workflow_id,
            "steps_executed": len(results),
            "results": results
        }
    
    async def _evaluate_condition(self, condition: str, previous_results: list) -> bool:
        """
        Evaluate a condition based on previous step results.
        """
        # Simple condition evaluation
        if condition == "if_not_recovered":
            # Check if previous email step resulted in recovery
            for result in previous_results:
                if result.get("action") == "send_email" and result.get("output", {}).get("recovered"):
                    return False
            return True
        return True
    
    async def _notify_admin_error(self, workflow_id: str, step: Dict, error: str):
        """
        Notify admin of workflow execution error.
        """
        logger.error(f"Notifying admin of error in workflow {workflow_id}: {error}")
        # TODO: Send notification via admin notification service


def _parse_duration(duration_str: str) -> int:
    """
    Parse duration string (e.g., "1h", "30m") to seconds.
    """
    if duration_str.endswith("h"):
        return int(duration_str[:-1]) * 3600
    elif duration_str.endswith("m"):
        return int(duration_str[:-1]) * 60
    elif duration_str.endswith("s"):
        return int(duration_str[:-1])
    return 60  # Default to 1 minute


class TemporalWorkflowManager:
    """
    Manager for deploying and monitoring Temporal workflows.
    """
    
    def __init__(self, temporal_url: str = "localhost:7233"):
        self.temporal_url = temporal_url
        self.client: Optional[Client] = None
    
    async def connect(self):
        """Connect to Temporal server."""
        import os
        import base64
        
        # Prioritize and trim addresses
        env_addr = os.getenv("TEMPORAL_ADDRESS", "").strip() or os.getenv("TEMPORAL_HOST", "").strip()
        if env_addr:
            self.temporal_url = env_addr
        # Check for file paths
        temporal_cert_path = os.getenv("TEMPORAL_MTLS_CERT")
        temporal_key_path = os.getenv("TEMPORAL_MTLS_KEY")
        
        # Check for direct content (Base64 encoded)
        temporal_cert_content_b64 = os.getenv("TEMPORAL_MTLS_CERT_CONTENT")
        temporal_key_content_b64 = os.getenv("TEMPORAL_MTLS_KEY_CONTENT")

        val_cert_data = None
        val_key_data = None

        if temporal_cert_content_b64 and temporal_key_content_b64:
            try:
                val_cert_data = base64.b64decode(temporal_cert_content_b64)
                val_key_data = base64.b64decode(temporal_key_content_b64)
            except Exception as e:
                logger.error(f"Failed to decode base64 certs: {e}")
                val_cert_data = None
                val_key_data = None
                
        if not val_cert_data and temporal_cert_path and temporal_key_path:
             if os.path.exists(temporal_cert_path) and os.path.exists(temporal_key_path):
                with open(temporal_cert_path, "rb") as f:
                    val_cert_data = f.read()
                with open(temporal_key_path, "rb") as f:
                    val_key_data = f.read()
            
        namespace = os.getenv("TEMPORAL_NAMESPACE", "default").strip()
        if val_cert_data and val_key_data:
            self.client = await Client.connect(
                self.temporal_url,
                namespace=namespace,
                tls=True,
                tls_client_cert_config={"client_cert": val_cert_data, "client_private_key": val_key_data}
            )
        else:
            self.client = await Client.connect(self.temporal_url, namespace=namespace)
        logger.info(f"Connected to Temporal at {self.temporal_url}")
    
    async def deploy_workflow(self, workflow_id: str, workflow_blueprint: Dict[str, Any]) -> str:
        """
        Deploy an approved workflow to Temporal.
        """
        if not self.client:
            await self.connect()
        
        # Start the workflow
        handle = await self.client.start_workflow(
            AgenticWorkflow.run,
            workflow_blueprint,
            id=workflow_id,
            task_queue="agentic-workflows"
        )
        
        logger.info(f"Deployed workflow {workflow_id} to Temporal")
        return handle.id
    
    async def start_worker(self):
        """
        Start a Temporal worker to execute workflows.
        This should run as a background service.
        """
        if not self.client:
            await self.connect()
        
        worker = Worker(
            self.client,
            task_queue="agentic-workflows",
            workflows=[AgenticWorkflow],
            activities=[execute_workflow_step]
        )
        
        logger.info("Starting Temporal worker for agentic workflows...")
        await worker.run()


# Singleton instance
temporal_manager = TemporalWorkflowManager()


async def deploy_approved_workflow(workflow_id: str, workflow_blueprint: Dict[str, Any]) -> str:
    """
    Helper function to deploy an approved workflow.
    Called from the workflow_governance API.
    """
    return await temporal_manager.deploy_workflow(workflow_id, workflow_blueprint)
