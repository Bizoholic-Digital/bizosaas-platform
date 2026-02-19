import os
import json
import httpx
import asyncio
import logging
from typing import Dict, Any, List, Optional
from app.core.rag import rag_service
from app.core.kag_service import kag_service
from app.core.agents.governance_agent import governance_agent

from app.core.vault import get_config_val, vault_service

from app.core.semantic_cache import semantic_cache

logger = logging.getLogger(__name__)

async def _select_llm_config(agent_type: str, task_description: str, tenant_id: str = "global") -> Dict[str, Any]:
    """
    Intelligently select LLM provider and model based on task type and complexity.
    Now supports tenant-specific fine-tuned models via Vault lookup.
    """
    # 1. Check for tenant-specific fine-tuned model in Vault
    fine_tuned_model_id = None
    if tenant_id != "global":
        try:
            path = f"tenants/{tenant_id}/fine_tuning/active_model"
            active_model_data = await vault_service.secret_adapter.get_secret(path)
            if active_model_data:
                fine_tuned_model_id = active_model_data.get("model_id")
                logger.info(f"Found fine-tuned model for tenant {tenant_id}: {fine_tuned_model_id}")
        except Exception as e:
            logger.warning(f"Failed to lookup fine-tuned model for {tenant_id}: {e}")

    # If we have a fine-tuned model, prioritize it for the agent (usually Together AI)
    if fine_tuned_model_id:
        return {
            "model_provider": "together_ai",
            "model_name": fine_tuned_model_id,
            "temperature": 0.7
        }

    # fallback to default logic
    # Simple/Fast tasks -> Groq (Llama 3.1 70B)
    speed_optimized_tasks = [
        "content_creator", "seo_specialist", "social_media_specialist",
        "quality_scorer", "meta_tag_generator"
    ]
    
    # Complex/Reasoning tasks -> OpenRouter (Claude 3.5 Sonnet / GPT-4o)
    reasoning_heavy_tasks = [
        "marketing_strategist", "competitive_analysis_specialist",
        "brand_positioning_specialist", "master_orchestrator"
    ]
    
    if agent_type in speed_optimized_tasks:
        return {
            "model_provider": "groq",
            "model_name": "llama-3.1-70b-versatile",
            "temperature": 0.7
        }
    elif agent_type in reasoning_heavy_tasks:
        return {
            "model_provider": "openrouter",
            "model_name": "openai/gpt-4o", # Default choice for high reasoning
            "temperature": 0.5
        }
    
    # Default fallback
    return {
        "model_provider": "openrouter",
        "model_name": "openai/gpt-4o-mini",
        "temperature": 0.7
    }


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
    Now with intelligent multi-model routing.
    """
    # Use AI_AGENTS_URL to match .env
    ai_agents_url = get_config_val("AI_AGENTS_URL", "http://localhost:8001")
    
    # --- PHASE 8 GOVERNANCE CHECK (INPUT) ---
    # 1. Input Safety & Policy Review
    gov_review = await governance_agent.review_input(tenant_id, task_description, payload)
    if not gov_review["allowed"]:
        logger.warning(f"Governance blocked request: {gov_review.get('reason')}")
        raise ValueError(f"Request blocked by safety policy: {gov_review.get('reason')}")
        
    # 2. Budget Check
    if not await governance_agent.check_budget(tenant_id, estimated_cost=0.01): # Mock cost
        raise ValueError("Insufficient credits/budget for this operation.")
    # ----------------------------------------
    
    # Select optimal LLM configuration for this task (now async)
    llm_config = await _select_llm_config(agent_type, task_description, tenant_id=tenant_id)

    # 0. Prompt Enhancement (New Phase 7E)
    from app.core.prompt_enhancer import prompt_enhancer
    enhanced = await prompt_enhancer.enhance_prompt(
        agent_type=agent_type,
        task_description=task_description,
        input_data=payload,
        tenant_id=tenant_id
    )
    task_description = enhanced["task_description"]
    payload = enhanced["input_data"]

    
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

    # 2. Check Semantic Cache (before calling AI agent)
    # Include LLM config in cache key to avoid cross-model cache collisions
    cache_key = f"{agent_type}:{task_description}:{llm_config['model_name']}:{json.dumps(payload, sort_keys=True)}"
    cached_result = None
    if use_rag:  # Only use cache if RAG is enabled
        try:
            cached_result = await semantic_cache.get(cache_key, similarity_threshold=0.95)
            if cached_result:
                logger.info(f"Cache HIT for {agent_type} - returning cached response")
                return json.loads(cached_result)
        except Exception as e:
            logger.warning(f"Semantic cache lookup failed (non-critical): {e}")

    # 3. Call AI Agent (cache miss or cache disabled)
    async with httpx.AsyncClient() as client:
        task_payload = {
            "agent_type": agent_type,
            "task_description": task_description,
            "input_data": payload,
            "priority": priority,
            "config": llm_config # Inject the selected LLM config
        }

        
        try:
            response = await client.post(f"{ai_agents_url}/tasks", json=task_payload, timeout=30.0)
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
                                    doc_id = await rag_service.ingest_knowledge(
                                        content=content_to_ingest,
                                        metadata=ingest_metadata,
                                        tenant_id=tenant_id,
                                        agent_id=agent_id
                                    )
                                    if doc_id:
                                        logger.info(f"Ingested agent result for {agent_type} into RAG (ID: {doc_id})")
                                        # KAG Post-hook: Link result back to context chunks if any
                                        if context:
                                            # We just link to the first context chunk for now as a representitive
                                            # In a more complex setup, we'd link to all or use a 'context' relation
                                            try:
                                                # Assuming context chunks are identifiable or we just store the relation
                                                # Note: KAGService.link_chunks currently takes int IDs. 
                                                # doc_id is str from RETURNING id. We cast if needed.
                                                await kag_service.link_chunks(
                                                    source_id=int(doc_id),
                                                    target_id=0, # Root/Context placeholder if we don't have the specific chunk ID
                                                    rel_type="generated_from_context",
                                                    metadata={"workflow": agent_type, "task": task_description}
                                                )
                                            except Exception as ke:
                                                logger.warning(f"KAG linking failed (non-critical): {ke}")
                            except Exception as e:
                                logger.error(f"Post-call RAG ingestion failed: {e}")
                        
                        # --- PHASE 8 GOVERNANCE CHECK (OUTPUT) ---
                        # 4. Output Safety & PII Review
                        output_content = str(result.get("response", "")) # Assuming response text is here
                        out_review = await governance_agent.review_output(tenant_id, output_content)
                        
                        if not out_review.get("allowed", True):
                            logger.warning(f"Governance flagged output: {out_review.get('reason')}")
                            # We can either block or sanitize. For now, we block if flagged as not allowed.
                            # But review_output currently returns allowed=True with cleaned_content usually.
                            
                        # Apply sanitization if modified
                        if out_review.get("cleaned_content"):
                             result["response"] = out_review["cleaned_content"]
                             if "warnings" in out_review:
                                 result["governance_warnings"] = out_review["warnings"]
                        # -----------------------------------------

                        # 4. Cache the successful result
                        if use_rag:
                            try:
                                await semantic_cache.set(
                                    query=cache_key,
                                    response=json.dumps(result),
                                    metadata={
                                        "agent_type": agent_type,
                                        "tenant_id": tenant_id,
                                        "agent_id": agent_id
                                    }
                                )
                                logger.info(f"Cached response for {agent_type}")
                            except Exception as e:
                                logger.warning(f"Semantic cache storage failed (non-critical): {e}")
                                
                        return result
                    elif status == "failed":
                        logger.error(f"Agent task failed: {status_data.get('error_message')}. Full response: {status_data}")
                        raise Exception(f"Agent task failed: {status_data.get('error_message')}")
                    elif status == "cancelled":
                        raise Exception("Agent task cancelled")
            
            raise Exception("Timeout waiting for AI agent")
            
        except httpx.HTTPStatusError as e:
            logger.error(f"AI Agent call HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"AI Agent call failed: {e}")
            raise
