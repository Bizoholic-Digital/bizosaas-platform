from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_identity_port, get_current_user, get_secret_service
from app.domain.services.secret_service import SecretService
from domain.ports.identity_port import IdentityPort, AuthenticatedUser


import httpx

router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])

# Google Maps API Key
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyBZxfvuglTrcCIZZfSVDTltjBWTgEuRLto")

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
    type: Optional[str] = "service"
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
    
    if "google" in provider.lower():
        # Mock Discovery - Returning detailed properties for GTM, GA4, GSC
        discovery_results["google"] = [
            # GTM Containers
            {"id": "GTM-PRH6T87", "name": "Bizoholic Main Container", "status": "detected", "type": "gtm_container"},
            {"id": "GTM-WLZK2N9", "name": "Staging/Dev Container", "status": "detected", "type": "gtm_container"},
            
            # GA4 Properties
            {"id": "315422891", "name": "Marketing GA4 (Primary)", "status": "detected", "type": "ga4_property"},
            {"id": "284771203", "name": "E-commerce Analytics", "status": "detected", "type": "ga4_property"},
            
            # GSC Sites
            {"id": "https://bizoholic.net/", "name": "bizoholic.net", "status": "detected", "type": "gsc_site"},
            {"id": "sc-domain:bizoholic.net", "name": "bizoholic.net (Domain)", "status": "detected", "type": "gsc_site"},

            # Facebook Analytics (Integrated here for convenience in discovery results)
            {"id": "fb-pixel-12345", "name": "Meta Pixel (Primary)", "status": "detected", "type": "fb_analytics"},
            
            # Core Services
            {"id": "google-ads", "name": "Google Ads", "status": "detected", "type": "service", "cost": "$$$", "requiresEnablement": True},
            {"id": "google-business-profile", "name": "Google Business Profile", "status": "detected", "type": "service", "requiresEnablement": False},
            {"id": "linkedin-ads", "name": "LinkedIn Ads", "status": "detected", "type": "service", "requiresEnablement": True},
            {"id": "tiktok-ads", "name": "TikTok Ads", "status": "detected", "type": "service", "requiresEnablement": True}
        ]
        profile_updates = {}
        if current_user.name:
             profile_updates["companyName"] = current_user.name
    elif "microsoft" in provider.lower():
        discovery_results["microsoft"] = [
            {"id": "clarity-proj-abc", "name": "Bizoholic Clarity", "status": "detected", "type": "clarity_project"},
            {"id": "bing-site-123", "name": "bizoholic.net (Bing)", "status": "detected", "type": "bing_profile"},
            {"id": "ms-365", "name": "Microsoft 365", "status": "detected", "type": "service", "requiresEnablement": False},
            {"id": "ms-teams", "name": "Microsoft Teams", "status": "detected", "type": "service", "requiresEnablement": True}
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
        ("google-business-profile", "app.connectors.google_business_profile.GoogleBusinessProfileConnector"),
        ("google-tag-manager", "app.connectors.google_tag_manager.GoogleTagManagerConnector")
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
        
    return results

@router.post("/gtm/analyze")
async def analyze_gtm_onboarding(
    payload: Dict[str, Any],
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Priority GTM-First Onboarding:
    Triggers the Temporal workflow to analyze the website and Google assets.
    """
    website_url = payload.get("website_url")
    access_token = payload.get("access_token")
    
    if not website_url:
        raise HTTPException(status_code=400, detail="website_url is required")

    try:
        from app.models.workflow import Workflow
        
        # Ensure Workflow Record Exists
        wf_name = f"GTM Onboarding: {website_url}"
        tenant_id = str(current_user.tenant_id or current_user.id)
        
        existing_wf = db.query(Workflow).filter(
            Workflow.tenant_id == tenant_id,
            Workflow.name == wf_name
        ).first()
        
        if not existing_wf:
            existing_wf = Workflow(
                tenant_id=tenant_id,
                name=wf_name,
                type="Integration",
                status="running",
                description=f"Automated GTM/GA4 setup for {website_url}",
                config={"retries": 3, "priority": "high"},
                created_at=datetime.utcnow()
            )
            db.add(existing_wf)
            db.commit()
            db.refresh(existing_wf)
            
        # Update run stats
        existing_wf.status = "running"
        existing_wf.runs_today = (existing_wf.runs_today or 0) + 1
        existing_wf.last_run = datetime.utcnow()
        db.commit()

        from temporalio.client import Client
        client = await Client.connect(os.getenv("TEMPORAL_HOST", "localhost:7233"))
        
        handle = await client.start_workflow(
            "GTMOnboardingWorkflow",
            {
                "website_url": website_url,
                "google_access_token": access_token,
                "tenant_id": str(current_user.tenant_id or current_user.id),
                "workflow_db_id": str(existing_wf.id)
            },
            id=f"gtm-onboarding-{current_user.id}",
            task_queue="connector-tasks"
        )
        
        return {
            "status": "started",
            "workflow_id": handle.id,
            "message": "GTM analysis and integration workflow started."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start GTM workflow: {e}")

    return {
        "status": "success",
        "discovered": results
    }

@router.post("/scan")
async def scan_website_tags(payload: Dict[str, Any]):
    """
    Synchronous Website Scan:
    Quickly checks the homepage for installed tags (GTM, GA4, Meta) and Plugins.
    Used to auto-select the correct container/property from the authenticated user's list.
    """
    website_url = payload.get("website_url")
    if not website_url:
         return {"status": "error", "message": "No URL provided"}

    if not website_url.startswith("http"):
        website_url = "https://" + website_url

    detected = {
        "gtm": [],
        "ga4": [],
        "ua": [],
        "meta": [],
        "clarity": [],
        "site_kit": False,
        "cms": "none",
        "plugins": []
    }

    try:
        import re
        import httpx
        
        async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
            resp = await client.get(website_url, timeout=10.0)
            html = resp.text

            # 1. Platform Detection (Infrastructure)
            if "/wp-content/" in html or "/wp-includes/" in html or 'name="generator" content="WordPress' in html:
                detected["cms"] = "wordpress"
            elif ".myshopify.com" in website_url or 'cdn.shopify.com' in html:
                detected["cms"] = "shopify"
            elif "wix.com" in html:
                detected["cms"] = "wix"

            # 2. Tracking & Analytics
            gtm_matches = re.findall(r'GTM-[A-Z0-9]{4,10}', html)
            detected["gtm"] = list(set(gtm_matches))

            ga4_matches = re.findall(r'G-[A-Z0-9]{6,12}', html)
            detected["ga4"] = list(set(ga4_matches))

            ua_matches = re.findall(r'UA-\d{4,10}-\d{1,2}', html)
            detected["ua"] = list(set(ua_matches))
            
            if "clarity.ms" in html or "clarity/tag" in html:
                clarity_matches = re.findall(r'clarity/tag/([a-zA-Z0-9]+)', html)
                detected["clarity"] = list(set(clarity_matches))
            
            if "fbq('init'" in html or "fbevents.js" in html:
                 fb_matches = re.findall(r"fbq\(['\"]init['\"],\s*['\"](\d+)['\"]", html)
                 detected["meta"] = list(set(fb_matches))
            
            if 'Check for Google Site Kit' in html or 'name="generator" content="Site Kit' in html:
                detected["site_kit"] = True

            # 3. Plugin Detection via Multi-Marker Scan
            common_plugins = {
                "woocommerce": {"name": "WooCommerce", "markers": ["/plugins/woocommerce/", "woocommerce-no-js", 'content="WooCommerce']},
                "elementor": {"name": "Elementor", "markers": ["/plugins/elementor/", "elementor-default", 'content="Elementor']},
                "wordpress-seo": {"name": "Yoast SEO", "markers": ["/plugins/wordpress-seo/", "Yoast SEO plugin", "yoast-schema-graph"]},
                "fluent-crm": {"name": "FluentCRM", "markers": ["/plugins/fluent-crm/", "fluentcrm-"]},
                "hubspot": {"name": "HubSpot", "markers": ["/plugins/hubspot/", "hubspot.js", "hs-script-loader"]},
                "mailchimp": {"name": "Mailchimp", "markers": ["/plugins/mailchimp-for-wp/", "mc4wp-", "chimpstatic.com"]},
                "calendly": {"name": "Calendly", "markers": ["calendly.com/assets/external/widget.js", "calendly-inline-widget"]},
                "gohighlevel": {"name": "GoHighLevel", "markers": ["/plugins/leadconnector/", "msgsndr.com"]},
                "zoho": {"name": "Zoho CRM", "markers": ["/plugins/zoho-crm-forms/", "zoho.com/crm/"]},
                "contact-form-7": {"name": "Contact Form 7", "markers": ["/plugins/contact-form-7/", "wpcf7-"]},
                "wpforms": {"name": "WPForms", "markers": ["/plugins/wpforms-lite/", "/plugins/wpforms/", "wpforms-"]},
                "rank-math": {"name": "RankMath", "markers": ["/plugins/rank-math/", "rank-math-"]},
                "bizosaas-connect": {"name": "BizoSaaS Bridge", "markers": ["/wp-json/bizosaas/v1/"]}
            }

            matched_plugins = []
            is_bridge = False
            for slug, info in common_plugins.items():
                is_detected = False
                for marker in info["markers"]:
                    if marker in html:
                        is_detected = True
                        break
                
                if is_detected:
                    matched_plugins.append({"slug": slug, "name": info["name"], "status": "active"})
                    if slug == "bizosaas-connect":
                        is_bridge = True

            # 4. Proactive Bridge Verification
            if not is_bridge and detected["cms"] == "wordpress":
                try:
                    status_url = f"{website_url.rstrip('/')}/wp-json/bizosaas/v1/status"
                    async with httpx.AsyncClient(verify=False, timeout=2.0) as bridge_client:
                        b_resp = await bridge_client.get(status_url)
                        if b_resp.status_code == 200 and b_resp.json().get("status") == "active":
                            is_bridge = True
                            if not any(p["slug"] == "bizosaas-connect" for p in matched_plugins):
                                matched_plugins.append({"slug": "bizosaas-connect", "name": "BizoSaaS Bridge", "status": "active"})
                except:
                    pass

            detected["plugins"] = matched_plugins
            detected["is_bridge_active"] = is_bridge

    except Exception as e:
        print(f"Quick scan failed for {website_url}: {e}")
        return {"status": "error", "message": str(e)}

    return {
        "status": "success",
        "website_url": website_url,
        "scanned_tags": detected
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
    from app.services.billing_service import BillingService
    from app.models.user import Tenant
    
    # 0. Save Onboarding Data to Tenant Profile (for Business Directory/Manta-style use)
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    
    # ... rest of complete logic
    return {"status": "success"}

@router.get("/tools/download-plugin")
async def download_plugin():
    """
    Generates and downloads the BizoSaaS Connect WordPress plugin zip.
    """
    import io
    import zipfile
    from starlette.responses import StreamingResponse
    
    # Path to the single plugin file
    plugin_path = "app/templates/plugins/bizosaas-connect/bizosaas-connect.php"
    
    if not os.path.exists(plugin_path):
         raise HTTPException(status_code=404, detail="Plugin template not found")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Add the file to the zip, placing it inside a folder 'bizosaas-connect'
        zip_file.write(plugin_path, arcname="bizosaas-connect/bizosaas-connect.php")
    
    zip_buffer.seek(0)
    
    return StreamingResponse(
        zip_buffer, 
        media_type="application/zip", 
        headers={"Content-Disposition": "attachment; filename=bizosaas-connect.zip"}
    )

@router.post("/tools/verify-plugin")
async def verify_plugin_connection(payload: Dict[str, str]):
    """
    Verifies if the BizoSaaS Connect plugin is active on the target site.
    """
    website_url = payload.get("website_url")
    if not website_url:
        raise HTTPException(status_code=400, detail="Website URL is required")

    if not website_url.startswith("http"):
        website_url = "https://" + website_url

    # Normalize URL - remove trailing slash
    website_url = website_url.rstrip("/")
    api_url = f"{website_url}/wp-json/bizosaas/v1/status"
    
    try:
        import httpx
        async with httpx.AsyncClient(verify=False, timeout=5.0) as client:
            resp = await client.get(api_url)
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "active":
                    return {
                        "status": "connected",
                        "plugin_version": data.get("version"),
                        "wp_version": data.get("wp_version")
                    }
    except Exception as e:
        print(f"Plugin verification failed for {api_url}: {e}")
        pass
        
@router.post("/tools/connect-wordpress")
async def connect_wordpress_credentials(payload: Dict[str, str]):
    """
    Validates WordPress Application Password credentials.
    This enables 'Agentic' access even before the custom plugin is installed,
    allowing for basic management (Posts, Pages, Media) via standard APIs.
    """
    website_url = payload.get("website_url")
    username = payload.get("username")
    app_password = payload.get("application_password")

    if not website_url or not username or not app_password:
        raise HTTPException(status_code=400, detail="Missing credentials")

    if not website_url.startswith("http"):
        website_url = "https://" + website_url

    website_url = website_url.rstrip("/")
    # Standard WP REST API User Endpoint
    api_url = f"{website_url}/wp-json/wp/v2/users/me"

    try:
        import httpx
        async with httpx.AsyncClient(verify=False, timeout=10.0) as client:
            # WP Application Passwords use Basic Auth
            resp = await client.get(
                api_url, 
                auth=(username, app_password)
            )

            if resp.status_code == 200:
                user_data = resp.json()
                return {
                    "status": "connected",
                    "message": "Credentials verified successfully",
                    "wp_user_id": user_data.get("id"),
                    "wp_user_name": user_data.get("name"),
                    "capabilities": "standard_rest_api" 
                }
            elif resp.status_code == 401:
                 return {"status": "error", "message": "Invalid credentials (401 Unauthorized)"}
            else:
                 return {"status": "error", "message": f"Connection failed: {resp.status_code}"}

    except Exception as e:
        print(f"WP Connection failed: {e}")
        return {"status": "error", "message": str(e)}
        tenant.settings = {
            **(tenant.settings or {}),
            "business_profile": onboarding_data.get("profile"),
            "digital_presence": onboarding_data.get("digital_presence"),
            "social_media": onboarding_data.get("social_media"),
            "marketing_goals": onboarding_data.get("goals"),
            "ai_agent_config": onboarding_data.get("agent"),
            "onboarding_completed_at": str(datetime.utcnow())
        }
        tenant.name = state.profile.companyName
        db.add(tenant)
        db.commit()
        print(f"Stored comprehensive profile data for tenant: {tenant.name}")

    # 1. Create Subscription in Lago
    billing_service = BillingService(db)
    try:
        # Default to 'standard' plan for now. Future: connection to pricing selection step.
        subscription = await billing_service.create_subscription(
            current_user.tenant_id, 
            "standard",
            email=current_user.email,
            name=state.profile.companyName or current_user.name
        )
        print(f"Subscription created: {subscription.id if hasattr(subscription, 'id') else 'OK'}")
    except Exception as e:
        print(f"Subscription creation failed: {e}")

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
                
    # Sync to CRM
    try:
        from app.api.crm import get_active_crm_connector
        from app.dependencies import get_secret_service
        
        secret_service = get_secret_service()
        # Default to FluentCRM or first available CRM
        crm_connector = await get_active_crm_connector(current_user.tenant_id, secret_service)
        
        if crm_connector:
            await crm_connector.create_contact({
                "first_name": current_user.name.split(' ')[0] if current_user.name else "",
                "last_name": ' '.join(current_user.name.split(' ')[1:]) if current_user.name and ' ' in current_user.name else "",
                "email": current_user.email,
                "company": state.profile.companyName,
                "status": "lead",
                "tags": ["onboarded", "new_tenant"]
            })
            print(f"CRM Sync successful for {current_user.email}")
    except Exception as e:
        print(f"CRM Sync failed: {e}")

    # Mark user as onboarded in Clerk
    try:
        await identity.update_user_metadata(current_user.id, {"onboarded": True})
    except Exception as e:
        print(f"Failed to update user metadata: {e}")

    return {
        "status": "success", 
        "message": f"Onboarding completed. {provisioned_count} tools provisioning.", 
        "redirect": "/dashboard",
        "strategyId": "strat_12345" 
    }


# --- Google Places API Integration ---

@router.get("/places/autocomplete")
async def places_autocomplete(input: str, types: str = "establishment"):
    """
    Proxy to Google Places Autocomplete API.
    Returns a list of business predictions.
    types: 'establishment' for businesses, 'geocode' for addresses
    """
    if not input:
        return {"predictions": []}
        
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://maps.googleapis.com/maps/api/place/autocomplete/json",
            params={
                "input": input,
                "key": GOOGLE_MAPS_API_KEY,
                "types": types, 
            }
        )
        
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch from Google Places API")
        
    data = response.json()
    return {"predictions": data.get("predictions", [])}

@router.get("/places/details")
async def place_details(place_id: str):
    """
    Proxy to Google Places Details API.
    Returns detailed information about a selected place.
    """
    if not place_id:
        raise HTTPException(status_code=400, detail="Place ID is required")
        
    # Fields to request from Places API
    fields = "name,formatted_address,formatted_phone_number,website,url,geometry"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://maps.googleapis.com/maps/api/place/details/json",
            params={
                "place_id": place_id,
                "fields": fields,
                "key": GOOGLE_MAPS_API_KEY,
            }
        )
        
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch from Google Places API")
        
    data = response.json()
    result = data.get("result", {})
    
    return {
        "companyName": result.get("name"),
        "location": result.get("formatted_address"),
        "phone": result.get("formatted_phone_number"),
        "website": result.get("website"),
        "gmbLink": result.get("url"), # Google Maps URL
        "placeId": place_id
    }

