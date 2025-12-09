from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict
from enum import Enum

router = APIRouter(prefix="/api/brain/onboarding", tags=["onboarding"])

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

class ToolIntegration(BaseModel):
    emailMarketing: Optional[str] = None
    adPlatforms: List[str] = []

class OnboardingState(BaseModel):
    currentStep: int
    profile: BusinessProfile
    digitalPresence: DigitalPresence
    analytics: AnalyticsConfig
    socialMedia: SocialMediaConfig
    goals: CampaignGoals
    tools: ToolIntegration
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
async def complete_onboarding(state: OnboardingState):
    """Complete onboarding and trigger initial strategy generation"""
    # Here we would trigger the Temporal workflow to start the "OnboardingCrew"
    # and "CampaignStrategyCrew" agents.
    
    return {
        "status": "success", 
        "message": "Onboarding completed", 
        "redirect": "/dashboard",
        "strategyId": "strat_12345" # Mock ID
    }

