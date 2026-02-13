import os
import json
import httpx
import asyncio
import logging
from typing import Dict, Any, List, Optional
from app.core.rag import rag_service
from app.core.kag_service import kag_service

from app.core.vault import get_config_val

logger = logging.getLogger(__name__)

async def call_ai_agent_with_rag(
    agent_type: str, 
    task_description: str, 
    payload: Dict[str, Any], 
    tenant_id: str = "global",
    agent_id: str = "global",
    priority: str = "normal",
    use_rag: bool = True,
    auto_ingest: bool = True
) -> Dict[str, Any]:
    """
    Consolidated helper to call AI Agents with RAG context injection and result ingestion.
    """
    ai_agents_url = get_config_val("AI_AGENTS_SERVICE_URL", "http://brain-ai-agents:8000")
    
    # 1. RAG Context Retrieval
    context = []
    if use_rag:
        try:
            # We use the task description and payload parameters for grounding
            search_query = f"{task_description} {json.dumps(payload)}"[:500] 
            context = await rag_service.retrieve_context(
                query=search_query,
                agent_id=agent_id,
                filters={"tenant_id": tenant_id}
            )
            if context:
                payload["rag_context"] = context
                logger.info(f"Injected {len(context)} context chunks for {agent_type}")
        except Exception as e:
            logger.error(f"RAG retrieval failed: {e}")

    # 2. Call AI Agent
    async with httpx.AsyncClient() as client:
        task_payload = {
            "agent_type": agent_type,
            "task_description": task_description,
            "input_data": payload,
            "priority": priority
        }
        
        try:
            response = await client.post(f"{ai_agents_url}/tasks", json=task_payload, timeout=10.0)
            response.raise_for_status()
            task_data = response.json()
            task_id = task_data["task_id"]
            
            # Poll for completion
            max_retries = 60 # Increased timeout
            for _ in range(max_retries):
                await asyncio.sleep(2)
                status_resp = await client.get(f"{ai_agents_url}/tasks/{task_id}")
                if status_resp.status_code == 200:
                    status_data = status_resp.json()
                    status = status_data["status"]
                    if status == "completed":
                        result = status_data["result_data"]
                        
                        # 3. Passive Knowledge Ingestion
                        if auto_ingest and result:
                            try:
                                # Store the result back into RAG for future reference
                                # We store a summary or key parts if it's too large
                                content_to_ingest = json.dumps(result)
                                if len(content_to_ingest) > 5: # Only ingest if there's actual content
                                    ingest_metadata = {
                                        "source": "agent_result",
                                        "agent_type": agent_type,
                                        "task": task_description,
                                        "timestamp": os.getenv("CURRENT_TIME", ""),
                                        "tenant_id": tenant_id
                                    }
                                    await rag_service.ingest_knowledge(
                                        content=content_to_ingest,
                                        metadata=ingest_metadata,
                                        tenant_id=tenant_id,
                                        agent_id=agent_id
                                    )
                                    logger.info(f"Ingested agent result for {agent_type} into RAG")
                            except Exception as e:
                                logger.error(f"Post-call RAG ingestion failed: {e}")
                                
                        return result
                    elif status == "failed":
                        raise Exception(f"Agent task failed: {status_data.get('error_message')}")
                    elif status == "cancelled":
                        raise Exception("Agent task cancelled")
            
            raise Exception("Timeout waiting for AI agent")
            
        except Exception as e:
            logger.error(f"AI Agent call failed: {e}")
            raise
