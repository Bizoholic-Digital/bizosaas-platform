from temporalio import activity
from typing import Dict, Any, List, Optional
import logging
import httpx
import os
from datetime import datetime
import asyncio
from app.connectors.registry import ConnectorRegistry

logger = logging.getLogger(__name__)

# Helper to get connector (in real scenarios, this would fetch credentials from Vault/DB)
async def get_fluent_crm_connector(tenant_id: str = "default") -> Any:
    # Use environment fallbacks for development/system workflows
    creds = {
        "url": os.getenv("FLUENTCRM_WP_URL"),
        "username": os.getenv("FLUENTCRM_WP_USER"),
        "application_password": os.getenv("FLUENTCRM_WP_APP_PASSWORD")
    }
    return ConnectorRegistry.create_connector("fluentcrm", tenant_id, creds)

@activity.defn
async def check_fluent_crm_lead(params: Dict[str, Any]) -> Dict[str, Any]:
    """Check if a lead exists in FluentCRM."""
    email = params.get("email")
    tenant_id = params.get("tenant_id", "default")
    
    logger.info(f"Checking FluentCRM lead for: {email} (Tenant: {tenant_id})")
    
    try:
        connector = await get_fluent_crm_connector(tenant_id)
        contact = await connector.get_contact_by_email(email)
        
        if contact:
            return {
                "exists": True,
                "id": contact.id,
                "email": contact.email,
                "first_name": contact.first_name,
                "tags": contact.tags
            }
        return {"exists": False, "email": email}
    except Exception as e:
        logger.error(f"Failed to check FluentCRM lead: {e}")
        # Return negative exists but log error to not break workflow if it can handle missing lead
        return {"exists": False, "error": str(e)}

@activity.defn
async def tag_fluent_crm_contact(params: Dict[str, Any]) -> bool:
    """Add a tag to a FluentCRM contact."""
    email = params.get("email")
    tag = params.get("tag")
    tenant_id = params.get("tenant_id", "default")
    
    logger.info(f"Tagging {email} with {tag} in FluentCRM")
    
    try:
        connector = await get_fluent_crm_connector(tenant_id)
        contact = await connector.get_contact_by_email(email)
        if contact:
            # FluentCRM update_contact can take tags
            new_tags = list(set((contact.tags or []) + [tag]))
            await connector.update_contact(contact.id, {"tags": new_tags})
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to tag FluentCRM contact: {e}")
        return False

@activity.defn
async def generate_ai_marketing_content(params: Dict[str, Any]) -> str:
    """Use AI to generate personalized marketing content."""
    user_data = params.get("user", {})
    tone = params.get("tone", "professional")
    goal = params.get("goal", "nurture")
    
    logger.info(f"Generating AI content for {user_data.get('email')} with tone {tone}")
    
    # In a real scenario, this would call the LLMConnector or an AgentService
    # For now, we simulate a sophisticated response
    first_name = user_data.get("first_name") or "there"
    
    if goal == "nurture":
        return f"Hi {first_name}, we noticed you've been exploring our platform recently. We'd love to help you get the most out of our automation features. Have you tried setting up your first MCP yet?"
    
    return f"Hello {first_name}, just checking in to see if you have any questions about our premium plans."

@activity.defn
async def generate_social_posts(params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate platform-specific social media posts for a product/event."""
    topic = params.get("topic")
    platforms = params.get("platforms", ["instagram", "linkedin", "twitter"])
    brand_voice = params.get("brand_voice", "innovative")
    
    logger.info(f"Generating social posts for topic: {topic}")
    
    # Mocking AI result
    posts = {}
    if "instagram" in platforms:
        posts["instagram"] = {
            "caption": f"🚀 Big news! Exploring {topic} in a whole new way. #BizoSaaS #Automation #Growth",
            "image_prompt": f"A minimalist, high-tech abstract representation of {topic} in neon blues and indigos."
        }
    if "linkedin" in platforms:
        posts["linkedin"] = {
            "content": f"We are excited to share our latest insights on {topic}. At BizoSaaS, we're dedicated to redefining multi-channel orchestration. Read more on our blog. #FinTech #SaaS #AI",
            "article_summary": f"Deep dive into {topic}."
        }
    if "twitter" in platforms:
        posts["twitter"] = {
            "text": f"Stop thinking about {topic} manually. Start orchestrating. ⚡️ #SaaS #Automation"
        }
        
    return {
        "topic": topic,
        "posts": posts,
        "status": "generated"
    }

@activity.defn
async def publish_to_social_channels(params: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate publishing content to various social media APIs."""
    posts = params.get("posts", {})
    tenant_id = params.get("tenant_id", "default")
    
    results = {}
    for platform, content in posts.items():
        logger.info(f"Publishing to {platform} for tenant {tenant_id}")
        # In production, this would call Meta Graph API, LinkedIn API, etc.
        results[platform] = "published"
        
    return {
        "status": "success",
        "published_count": len(results),
        "details": results
    }

@activity.defn
async def optimize_ad_budgets(params: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze ROAS and adjust budgets across Meta, Google, and Marketplace ads."""
    tenant_id = params.get("tenant_id", "default")
    current_budgets = params.get("current_budgets", {})
    
    logger.info(f"Optimizing ad budgets for tenant: {tenant_id}")
    
    # Mock analysis: identify high performing channels
    # In production, this would fetch data from Facebook Ads / Google Ads connectors
    performance = {
        "meta": {"roas": 4.2, "spend": 1000},
        "google": {"roas": 2.1, "spend": 1500},
        "meesho": {"roas": 5.8, "spend": 500}
    }
    
    new_budgets = {}
    recommendations = []
    
    for channel, data in performance.items():
        if data["roas"] > 4.0:
            new_budgets[channel] = current_budgets.get(channel, 0) * 1.2
            recommendations.append(f"Increase {channel} budget by 20% due to ROAS {data['roas']}")
        elif data["roas"] < 2.5:
            new_budgets[channel] = current_budgets.get(channel, 0) * 0.8
            recommendations.append(f"Decrease {channel} budget by 20% due to low ROAS {data['roas']}")
        else:
            new_budgets[channel] = current_budgets.get(channel, 0)
            
    return {
        "status": "optimized",
        "new_budgets": new_budgets,
        "recommendations": recommendations,
        "optimized_at": datetime.now().isoformat()
    }
@activity.defn
async def execute_marketing_strategy_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the Marketing Strategist Agent via the AI Agents Service."""
    tenant_id = params.get("tenant_id", "default")
    company_info = params.get("company_info", {})
    goals = params.get("goals", {})
    
    logger.info(f"Executing Marketing Strategy for tenant: {tenant_id}")
    
    ai_agents_url = os.getenv("AI_AGENTS_SERVICE_URL", "http://brain-ai-agents:8000")
    
    async with httpx.AsyncClient() as client:
        # 1. Submit Task
        payload = {
            "agent_type": "marketing_strategist",
            "task_description": f"Develop marketing strategy for {company_info.get('name')}",
            "input_data": {
                "company_info": company_info,
                "goals": goals,
                "budget": params.get("budget", 5000),
                "timeline": params.get("timeline", "3 months")
            },
            "priority": "normal"
        }
        
        # We need a mock user context or token if auth is enabled.
        # Assuming system-to-system auth or skipped for internal network in this phase.
        # If headers needed: headers = {"X-Tenant-ID": tenant_id, "X-User-ID": "system"}
        
        try:
            response = await client.post(f"{ai_agents_url}/tasks", json=payload, timeout=10.0)
            response.raise_for_status()
            task_data = response.json()
            task_id = task_data["task_id"]
            logger.info(f"Submitted agent task {task_id}")
            
            # 2. Poll for Completion (Simple polling for now)
            # In production, use Signal or Webhook
            max_retries = 60 # 60 * 2s = 2 minutes timeout
            for _ in range(max_retries):
                await asyncio.sleep(2)
                status_resp = await client.get(f"{ai_agents_url}/tasks/{task_id}")
                if status_resp.status_code == 200:
                    status_data = status_resp.json()
                    status = status_data["status"]
                    
                    if status == "completed":
                        return status_data["result_data"]
                    elif status == "failed":
                        raise Exception(f"Agent task failed: {status_data.get('error_message')}")
                    elif status == "cancelled":
                        raise Exception("Agent task cancelled")
                        
            raise Exception("Timeout waiting for marketing agent")
            
        except httpx.RequestError as e:
            logger.error(f"Failed to communicate with AI Agents service: {e}")
            # Fallback for dev/test if service not reachable
            return {
                "strategy": "Fallback Strategy (Service Unreachable)",
                "note": str(e)
            }
        except Exception as e:
            logger.error(f"Error in marketing strategy activity: {e}")
            raise
