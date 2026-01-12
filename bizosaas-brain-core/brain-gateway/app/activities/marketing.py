from temporalio import activity
from typing import Dict, Any, List, Optional
import logging
import httpx
import os
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
