from temporalio import activity
from typing import Dict, Any, List, Optional
import logging
import httpx
import os
import json
from app.core.intelligence import call_ai_agent_with_rag

logger = logging.getLogger(__name__)

POSTIZ_API_URL = os.getenv("POSTIZ_API_URL", "https://api.postiz.bizoholic.com")
POSTIZ_API_KEY = os.getenv("POSTIZ_API_KEY")

@activity.defn
async def generate_twitter_post_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a highly engaging X/Twitter thread or post."""
    tenant_id = params.get("tenant_id")
    topic = params.get("topic")
    context = params.get("context")
    persona_id = params.get("persona_id")
    
    logger.info(f"Generating Twitter content for {tenant_id} on {topic}")
    
    try:
        result = await call_ai_agent_with_rag(
            agent_type="twitter_writer",
            task_description=f"Create a viral Twitter post/thread about {topic}. Use the provided context and brand persona.",
            payload={
                "topic": topic,
                "context": context,
                "persona_id": persona_id,
                "format": "thread" if params.get("as_thread") else "single"
            },
            tenant_id=tenant_id
        )
        return result
    except Exception as e:
        logger.error(f"Twitter post generation failed: {e}")
        return {"text": f"Check out our new insights on {topic}! #AI #Marketing", "type": "single"}

@activity.defn
async def generate_linkedin_post_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a professional LinkedIn post with storytelling."""
    tenant_id = params.get("tenant_id")
    topic = params.get("topic")
    context = params.get("context")
    persona_id = params.get("persona_id")
    
    logger.info(f"Generating LinkedIn content for {tenant_id}")
    
    try:
        result = await call_ai_agent_with_rag(
            agent_type="linkedin_writer",
            task_description=f"Write a thought-leadership LinkedIn post about {topic}. Ensure it follows professional storytelling best practices.",
            payload={"topic": topic, "context": context, "persona_id": persona_id},
            tenant_id=tenant_id
        )
        return result
    except Exception as e:
        logger.error(f"LinkedIn post generation failed: {e}")
        return {"text": f"I've been thinking a lot about {topic} lately...", "type": "post"}

@activity.defn
async def generate_instagram_facebook_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate visual-focused content for IG/FB."""
    tenant_id = params.get("tenant_id")
    topic = params.get("topic")
    
    logger.info(f"Generating IG/FB content for {tenant_id}")
    
    try:
        result = await call_ai_agent_with_rag(
            agent_type="instagram_writer",
            task_description=f"Create a visual-first social post for Instagram and Facebook about {topic}. Include image generation prompts.",
            payload={"topic": topic, "persona_id": params.get("persona_id")},
            tenant_id=tenant_id
        )
        return result
    except Exception as e:
        logger.error(f"IG/FB generation failed: {e}")
        return {"caption": f"Exciting things happening with {topic}!", "image_prompt": "A modern workspace with AI elements"}

@activity.defn
async def schedule_social_post_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Bridge to Postiz API for scheduling."""
    content = params.get("content")
    platform = params.get("platform")
    scheduled_at = params.get("scheduled_at")
    tenant_id = params.get("tenant_id")
    
    logger.info(f"Scheduling {platform} post for {tenant_id} at {scheduled_at}")
    
    if not POSTIZ_API_KEY:
        logger.warning("POSTIZ_API_KEY not set. Mocking success.")
        return {"status": "scheduled", "post_id": "mock-post-123"}
        
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{POSTIZ_API_URL}/posts",
                json={
                    "content": content,
                    "platform": platform,
                    "schedule": scheduled_at,
                    "tenant_id": tenant_id
                },
                headers={"Authorization": f"Bearer {POSTIZ_API_KEY}"},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Postiz scheduling failed: {e}")
            raise activity.ApplicationError(f"Failed to schedule post: {str(e)}")
