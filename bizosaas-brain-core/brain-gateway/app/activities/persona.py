from temporalio import activity
from typing import Dict, Any, List, Optional
import logging
import httpx
import os
import json
import asyncio

from app.core.intelligence import call_ai_agent_with_rag

logger = logging.getLogger(__name__)

@activity.defn
async def analyze_website_activity(tenant_id: str, website_url: str) -> Dict[str, Any]:
    """Crawl and extract brand-relevant data from website."""
    logger.info(f"Analyzing website {website_url} for tenant {tenant_id}")
    
    try:
        insights = await call_ai_agent_with_rag(
            agent_type="research_specialist",
            task_description=f"Analyze the website {website_url} to extract brand identity, target audience, and key messaging.",
            payload={"website_url": website_url},
            tenant_id=tenant_id
        )
        return insights
    except Exception:
        # Fallback
        return {"extracted_content": f"Mocked insights from {website_url}"}

@activity.defn
async def extract_brand_voice_activity(tenant_id: str, website_insights: Dict[str, Any], onboarding_data: Dict[str, Any]) -> Dict[str, Any]:
    """Identify tone, style, and vocabulary from insights and onboarding data."""
    logger.info(f"Extracting brand voice for tenant {tenant_id}")
    
    try:
        brand_voice = await call_ai_agent_with_rag(
            agent_type="content_strategist",
            task_description="Based on website insights and onboarding data, define the brand's tone, voice, and key vocabulary.",
            payload={"website_insights": website_insights, "onboarding_data": onboarding_data},
            tenant_id=tenant_id
        )
        return brand_voice
    except Exception:
        return {"tone": "Professional", "style": "Clear and concise", "vocabulary": ["efficiency", "growth"]}

@activity.defn
async def generate_core_persona_activity(tenant_id: str, brand_voice: Dict[str, Any]) -> Dict[str, Any]:
    """Create a consolidated core brand persona."""
    logger.info(f"Generating core persona for tenant {tenant_id}")
    
    try:
        core_persona = await call_ai_agent_with_rag(
            agent_type="persona_specialist",
            task_description="Generate a detailed core brand persona including values, mission, and distinct voice markers.",
            payload={"brand_voice": brand_voice},
            tenant_id=tenant_id
        )
        return core_persona
    except Exception:
        return {
            "name": "Default Brand Persona",
            "voice": brand_voice.get("tone", "Professional"),
            "values": ["Trust", "Innovation"]
        }

@activity.defn
async def adapt_platform_personas_activity(tenant_id: str, core_persona: Dict[str, Any]) -> Dict[str, Any]:
    """Create platform-specific variants of the core persona."""
    logger.info(f"Adapting personas for platforms for tenant {tenant_id}")
    
    try:
        variants = await call_ai_agent_with_rag(
            agent_type="marketing_strategist",
            task_description="Adapt the core persona for LinkedIn, Instagram, Twitter, and Email marketing.",
            payload={"core_persona": core_persona},
            tenant_id=tenant_id
        )
        return variants
    except Exception:
        return {
            "linkedin": {"tone": "Expert", "focus": "B2B insights"},
            "instagram": {"tone": "Visual", "focus": "Lifestyle/Behind-the-scenes"},
            "twitter": {"tone": "Witty", "focus": "Current events/Brevity"},
            "email": {"tone": "Personal", "focus": "Direct value/Nurturing"}
        }
