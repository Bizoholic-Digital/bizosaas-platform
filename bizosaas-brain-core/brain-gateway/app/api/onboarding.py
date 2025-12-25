from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict
from enum import Enum
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_identity_port
from domain.ports.identity_port import IdentityPort, User

router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])

# --- Enums & Models ---

class GoalEnum(str, Enum):
    lead_gen = "lead_gen"
    brand_awareness = "brand_awareness"
    ecommerce_sales = "ecommerce_sales"
    app_installs = "app_installs"

class BusinessProfile(BaseModel):
    companyName: str
    industry: str
    location: str
    gmbLink: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None

class DigitalPresence(BaseModel):
    websiteDetected: bool
    cmsType: Optional[str] = None
    crmType: Optional[str] = None
    hasTracking: Optional[bool] = False

class AnalyticsConfig(BaseModel):
    gaId: Optional[str] = None
    gscId: Optional[str] = None
    setupLater: bool = False

class SocialMediaConfig(BaseModel):
    platforms: List[str] = []
    facebookPageId: Optional[str] = None
    instagramHandle: Optional[str] = None
    linkedinCompanyId: Optional[str] = None
    twitterHandle: Optional[str] = None
    tiktokHandle: Optional[str] = None
    setupLater: bool = False

class TargetAudience(BaseModel):
    locations: List[str] = []
    ageRange: str
    interests: List[str] = []

class CampaignGoals(BaseModel):
    primaryGoal: GoalEnum
    secondaryGoals: List[str] = []
    monthlyBudget: float
    currency: str = "USD"
    targetAudience: TargetAudience

class WordPressConfig(BaseModel):
    connected: bool
    siteUrl: Optional[str] = None
    adminUrl: Optional[str] = None

class FluentCRMConfig(BaseModel):
    connected: bool

class WooCommerceConfig(BaseModel):
    connected: bool
    consumerKey: Optional[str] = None
    consumerSecret: Optional[str] = None

class ToolIntegration(BaseModel):
    selectedMcps: List[str] = []
    emailMarketing: Optional[str] = None
    adPlatforms: List[str] = []
    wordpress: Optional[WordPressConfig] = None
    fluentCrm: Optional[FluentCRMConfig] = None
    wooCommerce: Optional[WooCommerceConfig] = None

class AgentConfig(BaseModel):
    persona: str
    name: str = "Alex"
    tone: str = "professional"

class OnboardingState(BaseModel):
    currentStep: int
    profile: BusinessProfile
    digitalPresence: DigitalPresence
    analytics: AnalyticsConfig
    socialMedia: SocialMediaConfig
    goals: CampaignGoals
    tools: ToolIntegration
    agent: AgentConfig
    isComplete: bool

# --- Mock Data Store ---
# In production, this would be a database table linked to tenant_id
MOCK_STORE = {} 

# --- Endpoints ---

@router.get("/status")
async def get_onboarding_status():
    """Check if onboarding is complete for the current tenant"""
    # TODO: Fetch from actual DB using tenant context
    return {
        "isConnectionSuccess": True,
        "isComplete": False, 
        "currentStep": 0
    }

@router.post("/business-profile")
async def save_business_profile(profile: BusinessProfile):
    """Save business identity details"""
    # TODO: Save to DB
    return {"status": "success", "message": "Profile saved", "data": profile}

@router.get("/business-profile")
async def get_business_profile():
    # Helper to return mock success for check
    return {"success": True, "profile": {"onboarding_completed": False}}

@router.post("/digital-presence")
async def save_digital_presence(presence: DigitalPresence):
    """Save digital presence details"""
    return {"status": "success", "message": "Presence saved"}

@router.post("/integrations")
async def save_integrations(analytics: AnalyticsConfig, social: SocialMediaConfig):
    """Save integration preferences"""
    return {"status": "success", "message": "Integrations saved"}

@router.post("/goals")
async def save_goals(goals: CampaignGoals):
    """Save campaign goals"""
    return {"status": "success", "message": "Goals saved"}

@router.post("/complete")
async def complete_onboarding(
    state: OnboardingState,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    identity: IdentityPort = Depends(get_identity_port),
    current_user: User = Depends(get_identity_port().get_current_user)
):
    """
    Complete onboarding:
    1. Save profile/preferences (TODO side effect)
    2. Provision selected MCP tools
    """
    
    # Provision Selected MCPs
    from app.models.mcp import McpRegistry, UserMcpInstallation
    from app.services.mcp_orchestrator import McpOrchestrator
    
    provisioned_count = 0
    
    if state.tools.selectedMcps:
        for mcp_slug in state.tools.selectedMcps:
            try:
                # Resolve MCP
                mcp = db.query(McpRegistry).filter(McpRegistry.slug == mcp_slug).first()
                if not mcp:
                    print(f"Skipping unknown MCP: {mcp_slug}")
                    continue
                    
                # Check existence
                existing = db.query(UserMcpInstallation).filter(
                    UserMcpInstallation.user_id == current_user.id,
                    UserMcpInstallation.mcp_id == mcp.id
                ).first()
                
                if existing:
                    continue
                
                # Create Installation
                installation = UserMcpInstallation(
                    user_id=current_user.id,
                    mcp_id=mcp.id,
                    status="pending",
                    config={} 
                )
                db.add(installation)
                db.commit()
                db.refresh(installation)
                
                # Trigger Orchestrator
                background_tasks.add_task(McpOrchestrator.provision_mcp, installation.id)
                provisioned_count += 1
                
            except Exception as e:
                print(f"Failed to schedule provision for {mcp_slug}: {e}")
                
    return {
        "status": "success", 
        "message": f"Onboarding completed. {provisioned_count} tools provisioning.", 
        "redirect": "/dashboard",
        "strategyId": "strat_12345" 
    }

