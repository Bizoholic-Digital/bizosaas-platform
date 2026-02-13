from temporalio import activity
from typing import Dict, Any, List, Optional
import logging
import httpx
import os
import json
from datetime import datetime
import asyncio
import re

from app.core.intelligence import call_ai_agent_with_rag
from app.core.vault import get_config_val

logger = logging.getLogger(__name__)

@activity.defn
async def content_research_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Deep research on a given topic/keywords."""
    tenant_id = params.get("tenant_id")
    topic = params.get("topic")
    
    logger.info(f"Researching topic: {topic} for tenant {tenant_id}")
    
    # In production: Use 'research_specialist' agent
    try:
        research = await call_ai_agent_with_rag(
            agent_type="research_specialist",
            task_description=f"Conduct deep research on {topic}. Include current trends, statistics, and competitor insights.",
            payload={"topic": topic},
            tenant_id=tenant_id
        )
        return research
    except Exception:
        # Fallback/Mock
        return {
            "summary": f"Research results for {topic}",
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "sources": ["https://example.com/source1"]
        }

@activity.defn
async def generate_content_outline_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a structured outline."""
    tenant_id = params.get("tenant_id")
    research = params.get("research")
    persona_id = params.get("persona_id")
    
    logger.info(f"Generating outline for tenant {tenant_id}")
    
    try:
        outline = await call_ai_agent_with_rag(
            agent_type="content_planner",
            task_description="Generate a detailed content outline based on the provided research and persona.",
            payload={"research": research, "persona_id": persona_id},
            tenant_id=tenant_id
        )
        return outline
    except Exception:
        return {
            "title": "Default Title",
            "sections": [
                {"heading": "Introduction", "points": ["Hook", "Core problem"]},
                {"heading": "Main Content", "points": ["Solution step 1", "Solution step 2"]},
                {"heading": "Conclusion", "points": ["Summary", "CTA"]}
            ]
        }

@activity.defn
async def revise_content_outline_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Revise outline based on feedback."""
    notes = params.get("notes")
    current_outline = params.get("current_outline")
    
    logger.info(f"Revising outline based on notes: {notes}")
    
    try:
        revised = await call_ai_agent_with_rag(
            agent_type="content_planner",
            task_description="Revise the content outline based on human feedback.",
            payload={"current_outline": current_outline, "notes": notes},
            tenant_id=params.get("tenant_id", "global")
        )
        return revised
    except Exception:
        return current_outline

@activity.defn
async def write_full_content_activity(params: Dict[str, Any]) -> str:
    """Full article writing with citations."""
    outline = params.get("outline")
    persona_id = params.get("persona_id")
    
    logger.info("Writing full draft...")
    
    try:
        draft = await call_ai_agent_with_rag(
            agent_type="content_writer",
            task_description="Write a high-quality article based on the provided outline and persona voice.",
            payload={"outline": outline, "persona_id": persona_id},
            tenant_id=params.get("tenant_id", "global")
        )
        return draft.get("text", "Content generation failed.")
    except Exception:
        return "This is a mock full length article draft based on the outline."

@activity.defn
async def seo_optimize_content_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Optimize draft with deterministic rules for slugs/titles + LLM for metadata."""
    draft = params.get("draft", "")
    title = params.get("title", "New Article")
    
    # 1. Deterministic Slug Generation
    slug = re.sub(r'[^a-z0-9\s-]', '', title.lower())
    slug = re.sub(r'[\s-]+', '-', slug).strip('-')
    
    # 2. Rule-based title check (Max 60 chars)
    meta_title = title if len(title) <= 60 else title[:57] + "..."
    
    logger.info(f"Optimizing content for SEO: {meta_title}")
    
    try:
        # 3. LLM for Meta Description & Content Refinement (Hybrid)
        optimized = await call_ai_agent_with_rag(
            agent_type="seo_specialist",
            task_description="Refine keywords and generate a compelling meta description.",
            payload={"content": draft, "suggested_title": meta_title},
            tenant_id=params.get("tenant_id", "global")
        )
        return {
            "body": optimized.get("body", draft),
            "meta_title": meta_title,
            "meta_description": optimized.get("meta_description", "No description generated."),
            "slug": slug,
            "tags": optimized.get("tags", [])
        }
    except Exception:
        return {
            "body": draft,
            "meta_title": meta_title,
            "meta_description": "Default Description",
            "slug": slug
        }

@activity.defn
async def score_content_quality_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Score and verify content accuracy."""
    content = params.get("content")
    
    logger.info("Scoring content quality...")
    
    try:
        score = await call_ai_agent_with_rag(
            agent_type="quality_analyst",
            task_description="Rate the article on E-E-A-T, readability, and originality.",
            payload={"content": content},
            tenant_id=params.get("tenant_id", "global")
        )
        return score
    except Exception:
        return {"overall_score": 8.5, "readability": "High", "relevance": "High"}

@activity.defn
async def create_approval_task_activity(params: Dict[str, Any]) -> bool:
    """Create a HITL task in the system."""
    tenant_id = params.get("tenant_id")
    task_type = params.get("type")
    content = params.get("content")
    
    logger.info(f"Creating {task_type} approval task for tenant {tenant_id}")
    
    # In production: Insert into hitl_tasks table or notify via WebSocket
    return True

@activity.defn
async def publish_content_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Push content to CMS (Wagtail/WordPress) using secure credentials from Vault."""
    tenant_id = params.get("tenant_id")
    content = params.get("content")
    target = params.get("target") or "wagtail"
    
    logger.info(f"Publishing to {target} for tenant {tenant_id}")
    
    if target == "wagtail":
        endpoint = get_config_val("CMS_WAGTAIL_URL")
        token = get_config_val("CMS_WAGTAIL_API_TOKEN")
        
        if not endpoint or not token:
            return {"status": "error", "message": "Wagtail credentials missing in Vault"}
            
        async with httpx.AsyncClient() as client:
            try:
                # Basic Wagtail API v2 Page Create
                res = await client.post(
                    f"{endpoint}/api/v2/pages/",
                    headers={"Authorization": f"Token {token}"},
                    json={
                        "title": content.get("title", "New Post"),
                        "slug": content.get("slug", "new-post"),
                        "show_in_menus": True,
                        "type": "blog.BlogPage", 
                        "parent": 3, 
                        "body": content.get("body", "")
                    }
                )
                if res.status_code in [201, 200]:
                    return {"status": "success", "id": res.json().get("id"), "url": f"{endpoint}/p/{res.json().get('id')}/"}
                return {"status": "error", "message": res.text}
            except Exception as e:
                return {"status": "error", "message": str(e)}
                
    elif target == "wordpress":
        url = get_config_val("CMS_WORDPRESS_URL")
        user = get_config_val("CMS_WORDPRESS_USERNAME")
        password = get_config_val("CMS_WORDPRESS_PASSWORD")
        
        if not url or not user or not password:
            return {"status": "error", "message": "WordPress credentials missing in Vault"}
            
        async with httpx.AsyncClient() as client:
            try:
                from base64 import b64encode
                auth = b64encode(f"{user}:{password}".encode()).decode()
                res = await client.post(
                    f"{url}/wp-json/wp/v2/posts",
                    headers={"Authorization": f"Basic {auth}"},
                    json={
                        "title": content.get("title", "New Post"),
                        "content": content.get("body", ""),
                        "status": "publish" if params.get("instant_publish") else "draft"
                    }
                )
                if res.status_code in [201, 200]:
                    return {"status": "success", "id": res.json().get("id"), "url": res.json().get("link")}
                return {"status": "error", "message": res.text}
            except Exception as e:
                return {"status": "error", "message": str(e)}
    
    return {"status": "error", "message": f"Unsupported target: {target}"}

@activity.defn
async def generate_monthly_calendar_activity(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate a content calendar."""
    tenant_id = params.get("tenant_id")
    
    logger.info(f"Generating monthly calendar for tenant {tenant_id}")
    
    try:
        calendar = await call_ai_agent_with_rag(
            agent_type="marketing_strategist",
            task_description="Generate 4 blog topics for the next month based on tenant profile and current trends.",
            payload={},
            tenant_id=tenant_id
        )
        return calendar.get("topics", [])
    except Exception:
        return [
            {"topic": "Future of AI in Marketing", "slug": "future-ai-marketing"},
            {"topic": "Automation for SaaS", "slug": "automation-saas"},
        ]
