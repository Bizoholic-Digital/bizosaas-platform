from temporalio import activity
from typing import Dict, Any, Optional
import logging
import httpx
import os
import asyncio

logger = logging.getLogger(__name__)

@activity.defn
async def generate_documentation_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"
    Trigger the DocumentationAgent in the ai-agents service to generate documentation.
    \"\"\"
    tenant_id = params.get("tenant_id", "default")
    task_type = params.get("task_type")  # e.g., "api_doc_generation", "user_guide_generation"
    input_data = params.get("input_data", {})
    
    logger.info(f"Generating documentation for tenant: {tenant_id}, task_type: {task_type}")
    
    ai_agents_url = os.getenv("AI_AGENTS_SERVICE_URL", "http://brain-ai-agents:8000")
    
    async with httpx.AsyncClient() as client:
        # Submit task to ai-agents service
        payload = {
            "agent_type": "documentation_agent",
            "task_type": task_type,
            "input_data": input_data,
            "priority": params.get("priority", "normal")
        }
        
        try:
            # Note: We use the /tasks endpoint as seen in other activities
            response = await client.post(f"{ai_agents_url}/tasks", json=payload, timeout=30.0)
            response.raise_for_status()
            task_data = response.json()
            task_id = task_data.get("task_id")
            
            if not task_id:
                raise Exception("No task_id returned from AI Agents service")
                
            logger.info(f"Submitted documentation task {task_id}")
            
            # Poll for completion
            max_retries = 90  # 90 * 2s = 3 minutes timeout
            for _ in range(max_retries):
                await asyncio.sleep(2)
                status_resp = await client.get(f"{ai_agents_url}/tasks/{task_id}")
                if status_resp.status_code == 200:
                    status_data = status_resp.json()
                    status = status_data.get("status")
                    
                    if status == "completed":
                        return {
                            "status": "success",
                            "result": status_data.get("result_data"),
                            "task_id": task_id
                        }
                    elif status == "failed":
                        raise Exception(f"Documentation task failed: {status_data.get('error_message')}")
                    elif status == "cancelled":
                        raise Exception("Documentation task cancelled")
            
            raise Exception("Timeout waiting for documentation agent")
            
        except httpx.RequestError as e:
            logger.error(f"Failed to communicate with AI Agents service: {e}")
            raise
        except Exception as e:
            logger.error(f"Error in documentation activity: {e}")
            raise

@activity.defn
async def update_docusaurus_content_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"
    Update the Docusaurus site content with generated documentation.
    \"\"\"
    content = params.get("content")
    relative_path = params.get("relative_path")  # Path relative to docusaurus docs folder
    
    if not content or not relative_path:
        raise ValueError("Content and relative_path are required")
        
    # BizoSaaS Documentation root
    # Based on previous initialization: bizosaas-brain-core/docs/bizosaas-docs/
    # We'll use the environment variable if available, or a default
    docs_root = os.getenv("DOCUSAURUS_PATH", "/home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/docs/bizosaas-docs")
    target_file = os.path.join(docs_root, "docs", relative_path)
    
    logger.info(f"Updating Docusaurus content at: {target_file}")
    
    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return {"status": "success", "file_path": target_file}
    except Exception as e:
        logger.error(f"Failed to update Docusaurus content: {e}")
        raise
