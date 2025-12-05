"""
Shared Pydantic models for BizoSaaS platform
"""
from .base import BaseModel, TenantModel
from .user import User, UserCreate, UserUpdate, UserInDB
from .tenant import Tenant, TenantCreate, TenantUpdate
from .campaign import Campaign, CampaignCreate, CampaignUpdate
from .lead import Lead, LeadCreate, LeadUpdate
from .analytics import AnalyticsReport, CampaignMetrics

__all__ = [
    "BaseModel",
    "TenantModel", 
    "User",
    "UserCreate",
    "UserUpdate", 
    "UserInDB",
    "Tenant",
    "TenantCreate",
    "TenantUpdate",
    "Campaign",
    "CampaignCreate", 
    "CampaignUpdate",
    "Lead",
    "LeadCreate",
    "LeadUpdate",
    "AnalyticsReport",
    "CampaignMetrics"
]