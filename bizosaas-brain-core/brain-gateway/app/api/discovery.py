from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.dependencies import get_db, get_current_user
from app.domain.ports.identity_port import AuthenticatedUser
import random

router = APIRouter()

@router.get("/recommendations")
async def get_recommendations(
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # This would eventually use AI to analyze the business graph
    # For now, we return intelligent placeholders based on common high-value integrations
    
    from app.models.mcp import UserMcpInstallation, McpRegistry
    
    # Check if Google Tag Manager is connected
    gtm = db.query(UserMcpInstallation).join(McpRegistry).filter(
        UserMcpInstallation.user_id == current_user.id,
        McpRegistry.slug == 'google-tag-manager',
        UserMcpInstallation.status.in_(['connected', 'installed', 'configured'])
    ).first()

    if gtm:
        # Simulate detection from GTM tags
        return [
            {
                "id": "intercom",
                "name": "Intercom",
                "description": "Customer messaging platform detected via GTM.",
                "category": "Communication",
                "reason": "Found 'Intercom' tag in your Google Tag Manager container.",
                "impactScore": 95,
                "potentialGrowth": "Improved Support",
                "connected": False,
                "color": "blue",
                "icon_type": "message",
                "is_detected": True
            },
            {
                "id": "hotjar",
                "name": "Hotjar",
                "description": "Heatmaps and recording tool detected via GTM.",
                "category": "Analytics",
                "reason": "Found 'Hotjar Tracking Code' in your GTM container.",
                "impactScore": 88,
                "potentialGrowth": "UX Insights",
                "connected": False,
                "color": "red",
                "icon_type": "activity",
                "is_detected": True
            },
            {
                "id": "facebook-pixel",
                "name": "Meta Pixel",
                "description": "Ad tracking detected via GTM.",
                "category": "Marketing",
                "reason": "Found 'Facebook Pixel' tag in your GTM container.",
                "impactScore": 90,
                "potentialGrowth": "Ad Retargeting",
                "connected": False,
                "color": "indigo",
                "icon_type": "facebook",
                "is_detected": True
            }
        ]

    # Default static recommendations
    recommendations = [
        {
            "id": "mailchimp",
            "name": "Mailchimp Marketing",
            "description": "Automate your customer outreach based on Shopify orders.",
            "category": "Marketing",
            "reason": "Integrates with your active store to drive 12% higher retention.",
            "impactScore": 85,
            "potentialGrowth": "+12% Revenue",
            "connected": False,
            "color": "amber",
            "icon_type": "mail"
        },
        {
            "id": "slack",
            "name": "Slack Notifications",
            "description": "Get real-time alerts for high-value task completions.",
            "category": "Operations",
            "reason": "Reduces response time by 45% for critical business events.",
            "impactScore": 92,
            "potentialGrowth": "-45% Latency",
            "connected": False,
            "color": "purple",
            "icon_type": "message"
        },
        {
            "id": "hubspot",
            "name": "HubSpot CRM",
            "description": "Centralize your customer data from 5 different sources.",
            "category": "Sales",
            "reason": "Consolidates 450+ orphaned leads found in your workspaces.",
            "impactScore": 78,
            "potentialGrowth": "Unified View",
            "connected": False,
            "color": "orange",
            "icon_type": "users"
        }
    ]
    
    return recommendations
