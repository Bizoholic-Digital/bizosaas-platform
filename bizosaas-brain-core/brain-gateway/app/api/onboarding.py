from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
import os
from enum import Enum
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_identity_port, get_current_user, get_secret_service
from app.domain.services.secret_service import SecretService
from domain.ports.identity_port import IdentityPort, AuthenticatedUser


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

class DiscoveryService(BaseModel):
    id: str
    name: str
    status: str
    cost: Optional[str] = None
    requiresEnablement: Optional[bool] = False

class DiscoveryResults(BaseModel):
    google: List[DiscoveryService] = []
    microsoft: List[DiscoveryService] = []
    lastUpdated: Optional[str] = None

class SocialLoginInfo(BaseModel):
    provider: str
    email: str
    name: Optional[str] = None
    profileImageUrl: Optional[str] = None

class AIAgentConfig(BaseModel):
    persona: str
    name: str = "Alex"
    tone: str = "professional"
    clientAdvocate: bool = True

class OnboardingState(BaseModel):
    currentStep: int
    socialLogin: Optional[SocialLoginInfo] = None
    profile: BusinessProfile
    digitalPresence: DigitalPresence
    discovery: DiscoveryResults = Field(default_factory=DiscoveryResults)
    analytics: AnalyticsConfig
    socialMedia: SocialMediaConfig
    goals: CampaignGoals
    tools: ToolIntegration
    agent: AIAgentConfig
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

@router.post("/discover")
async def discover_services(
    payload: Dict[str, Any],
    current_user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """
    Automated Discovery Endpoint:
    Triggers background checks for Google/Microsoft services based on SSO provider.
    """
    email = payload.get("email")
    provider = payload.get("provider", "none")
    
    tenant_id = current_user.tenant_id or current_user.id
    discovery_results = {"google": [], "microsoft": []}
    profile_updates = {}

    # Logic to fetch tokens from Clerk (simulated or real)
    # real_token = await identity_port.get_oauth_token(current_user.id, provider)
    
    if "google" in provider:
        # Mock Discovery for now - will integrate with real connectors in next step
        discovery_results["google"] = [
            {"id": "google-analytics", "name": "Google Analytics 4", "status": "detected", "requiresEnablement": False},
            {"id": "google-ads", "name": "Google Ads", "status": "detected", "cost": "$$$", "requiresEnablement": True},
            {"id": "google-business-profile", "name": "Google Business Profile", "status": "detected", "requiresEnablement": False}
        ]
        profile_updates = {
            "companyName": current_user.name or "My Business",
            "industry": "Marketing"
        }
    elif "microsoft" in provider:
        discovery_results["microsoft"] = [
            {"id": "microsoft-clarity", "name": "Microsoft Clarity", "status": "detected", "requiresEnablement": False},
            {"id": "bing-webmaster", "name": "Bing Webmaster Tools", "status": "not_detected", "requiresEnablement": True}
        ]

    return {
        "status": "success",
        "discovery": discovery_results,
        "profile": profile_updates
    }

@router.post("/goals")
async def save_goals(goals: CampaignGoals):
    """Save campaign goals"""
    return {"status": "success", "message": "Goals saved"}

@router.post("/google/discover")
async def discover_google_services(
    payload: Dict[str, Any], 
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    """
    Magic Discovery:
    1. Receive Google Access Token
    2. Attempt auto-linking for Analytics, Search Console, and Ads
    3. Save credentials and provision MCPs automatically
    """
    token = payload.get("access_token")
    if not token:
        raise HTTPException(status_code=400, detail="access_token is required")
    
    dry_run = payload.get("dry_run", False)
    selected_connectors = payload.get("selected_connectors", [])
    
    tenant_id = current_user.tenant_id or current_user.id
    results = {}
    
    all_connectors = [
        ("google-analytics", "app.connectors.google_analytics.GoogleAnalyticsConnector"),
        ("google-search-console", "app.connectors.google_search_console.GoogleSearchConsoleConnector"),
        ("google-ads", "app.connectors.google_ads.GoogleAdsConnector"),
        ("google-business-profile", "app.connectors.google_business_profile.GoogleBusinessProfileConnector")
    ]
    
    # Filter if selected_connectors is provided and not empty, and not a dry_run
    if selected_connectors and not dry_run:
        connectors_to_process = [c for c in all_connectors if c[0] in selected_connectors]
    else:
        connectors_to_process = all_connectors
    
    import importlib
    import asyncio
    
    async def process_connector(connector_id, class_path):
        try:
            # Dynamic import
            module_path, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            connector_cls = getattr(module, class_name)
            
            # Prepare credentials
            creds = {"access_token": token}
            if connector_id == "google-ads":
                creds["developer_token"] = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN", "DEVELOPER_TOKEN_HERE")
            
            connector = connector_cls(tenant_id=tenant_id, credentials=creds)
            
            # Perform discovery
            # For discovery, we check if the account is accessible/has properties
            discovery_result = await connector.perform_action("auto_link" if not dry_run else "discover", {})
            
            if not dry_run and discovery_result.get("status") == "success":
                # Save to Vault
                await secret_service.store_connector_credentials(
                    tenant_id=tenant_id,
                    connector_id=connector_id,
                    credentials=connector.credentials
                )
                
                # Provision MCP
                try:
                    from app.models.mcp import McpRegistry, UserMcpInstallation
                    from app.services.mcp_orchestrator import McpOrchestrator
                    
                    mcp = db.query(McpRegistry).filter(McpRegistry.slug == connector_id).first()
                    if mcp:
                        existing = db.query(UserMcpInstallation).filter(
                            UserMcpInstallation.user_id == current_user.id,
                            UserMcpInstallation.mcp_id == mcp.id
                        ).first()
                        
                        if not existing:
                            installation = UserMcpInstallation(
                                user_id=current_user.id,
                                mcp_id=mcp.id,
                                status="pending",
                                config={"connector_id": connector_id} 
                            )
                            db.add(installation)
                            db.commit()
                            db.refresh(installation)
                            background_tasks.add_task(McpOrchestrator.provision_mcp, installation.id)
                            discovery_result["mcp_provisioned"] = True
                except ImportError:
                    print("MCP models not available, skipping provisioning")
            return connector_id, discovery_result
        except Exception as e:
            print(f"Discovery failed for {connector_id}: {e}")
            return connector_id, {"status": "error", "message": str(e)}

    # Run discovery in parallel
    tasks = [process_connector(cid, path) for cid, path in connectors_to_process]
    discovery_results = await asyncio.gather(*tasks)
    
    for connector_id, result in discovery_results:
        results[connector_id] = result

    return {
        "status": "success",
        "discovered": results
    }

@router.post("/complete")
async def complete_onboarding(
    state: OnboardingState,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    identity: IdentityPort = Depends(get_identity_port),
    current_user: AuthenticatedUser = Depends(get_current_user)
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

