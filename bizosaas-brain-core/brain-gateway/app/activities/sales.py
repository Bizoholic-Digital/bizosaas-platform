from temporalio import activity
from typing import Dict, Any
import logging
import httpx
import os
import asyncio

logger = logging.getLogger(__name__)

@activity.defn
async def execute_sales_strategy_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the Sales Intelligence Agent via the AI Agents Service."""
    tenant_id = params.get("tenant_id", "default")
    sales_context = params.get("sales_context", {})
    mode = params.get("mode", "lead_qualification")
    
    logger.info(f"Executing Sales Strategy ({mode}) for tenant: {tenant_id}")
    
    ai_agents_url = os.getenv("AI_AGENTS_SERVICE_URL", "http://brain-ai-agents:8000")
    
    async with httpx.AsyncClient() as client:
        # 1. Submit Task
        payload = {
            "agent_type": "sales_intelligence",
            "task_description": f"Perform {mode} analysis",
            "input_data": {
                "sales_context": sales_context,
                "mode": mode,
                "pipeline_value": params.get("pipeline_value", "Unknown"),
                "growth_target": params.get("growth_target", "Not specified")
            },
            "priority": "normal"
        }
        
        try:
            response = await client.post(f"{ai_agents_url}/tasks", json=payload, timeout=10.0)
            response.raise_for_status()
            task_data = response.json()
            task_id = task_data["task_id"]
            logger.info(f"Submitted sales agent task {task_id}")
            
            # 2. Poll for Completion
            max_retries = 60 # 2 minutes
            for _ in range(max_retries):
                await asyncio.sleep(2)
                status_resp = await client.get(f"{ai_agents_url}/tasks/{task_id}")
                if status_resp.status_code == 200:
                    status_data = status_resp.json()
                    status = status_data["status"]
                    
                    if status == "completed":
                        return status_data["result_data"]
                    elif status == "failed":
                        raise Exception(f"Sales agent task failed: {status_data.get('error_message')}")
                    elif status == "cancelled":
                        raise Exception("Sales agent task cancelled")
                        
            raise Exception("Timeout waiting for sales agent")
            
        except httpx.RequestError as e:
            logger.error(f"Failed to communicate with AI Agents service: {e}")
            return {
                "error": "Service Unreachable",
                "details": str(e)
            }
        except Exception as e:
            logger.error(f"Error in sales strategy activity: {e}")
            raise
