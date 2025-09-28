"""
API Models for Domain Repository Service

This module defines the Pydantic models for API requests and responses.
"""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field, validator

from .domain.aggregates.lead import LeadSource, LeadStatus, LeadPriority
from .domain.aggregates.customer import CustomerStatus, CustomerTier, CustomerType, SubscriptionStatus
from .domain.aggregates.campaign import CampaignType, CampaignObjective, CampaignStatus, OptimizationGoal


# Base Models
class TenantContextModel(BaseModel):
    """Base model that includes tenant context"""
    tenant_id: UUID = Field(..., description="Tenant UUID for multi-tenancy")


# Lead API Models
class ContactInfoRequest(BaseModel):
    """Contact information for lead creation"""
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None


class LeadScoreRequest(BaseModel):
    """Lead score update request"""
    total_score: int = Field(..., ge=0, le=100)
    demographic_score: int = Field(default=0, ge=0, le=100)
    behavioral_score: int = Field(default=0, ge=0, le=100)
    firmographic_score: int = Field(default=0, ge=0, le=100)
    engagement_score: int = Field(default=0, ge=0, le=100)


class LeadQualificationRequest(BaseModel):
    """Lead qualification request"""
    budget_range: Optional[str] = None
    timeline: Optional[str] = None
    decision_maker: bool = False
    pain_points: List[str] = Field(default_factory=list)
    use_case: Optional[str] = None
    company_size: Optional[str] = None
    industry: Optional[str] = None


class CreateLeadRequest(TenantContextModel):
    """Request to create a new lead"""
    contact_info: ContactInfoRequest
    source: LeadSource
    utm_parameters: Optional[Dict[str, str]] = None
    campaign_id: Optional[UUID] = None
    referrer_url: Optional[str] = None
    landing_page: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None


class QualifyLeadRequest(TenantContextModel):
    """Request to qualify a lead"""
    user_id: UUID
    qualification_criteria: Optional[LeadQualificationRequest] = None
    score: Optional[LeadScoreRequest] = None


class UpdateLeadScoreRequest(TenantContextModel):
    """Request to update lead score"""
    score: LeadScoreRequest
    user_id: Optional[UUID] = None


class AssignLeadRequest(TenantContextModel):
    """Request to assign a lead"""
    assigned_to: UUID
    assigned_by: UUID


class ConvertLeadRequest(TenantContextModel):
    """Request to convert lead to customer"""
    user_id: UUID
    conversion_value: Optional[Decimal] = None
    customer_type: CustomerType = CustomerType.INDIVIDUAL


class LeadResponse(BaseModel):
    """Lead response model"""
    id: UUID
    tenant_id: UUID
    source: LeadSource
    status: LeadStatus
    priority: LeadPriority
    contact_info: ContactInfoRequest
    is_qualified: bool
    qualification_date: Optional[datetime] = None
    assigned_to: Optional[UUID] = None
    assigned_at: Optional[datetime] = None
    converted_to_customer_id: Optional[UUID] = None
    conversion_date: Optional[datetime] = None
    conversion_value: Optional[Decimal] = None
    utm_parameters: Dict[str, str]
    campaign_id: Optional[UUID] = None
    custom_fields: Dict[str, Any]
    tags: Set[str]
    created_at: datetime
    updated_at: datetime
    version: int


# Customer API Models
class CustomerAddressRequest(BaseModel):
    """Customer address request"""
    street_address: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    address_type: str = "billing"


class CustomerProfileRequest(BaseModel):
    """Customer profile request"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    annual_revenue: Optional[Decimal] = None
    timezone: Optional[str] = None
    preferred_language: str = "en"


class UpdateCustomerProfileRequest(TenantContextModel):
    """Request to update customer profile"""
    profile: CustomerProfileRequest
    user_id: Optional[UUID] = None


class UpgradeCustomerTierRequest(TenantContextModel):
    """Request to upgrade customer tier"""
    new_tier: CustomerTier
    user_id: Optional[UUID] = None


class RecordPurchaseRequest(TenantContextModel):
    """Request to record customer purchase"""
    order_value: Decimal = Field(..., gt=0)
    order_date: Optional[datetime] = None


class CustomerResponse(BaseModel):
    """Customer response model"""
    id: UUID
    tenant_id: UUID
    profile: CustomerProfileRequest
    status: CustomerStatus
    customer_type: CustomerType
    tier: CustomerTier
    converted_from_lead_id: Optional[UUID] = None
    conversion_date: Optional[datetime] = None
    acquisition_channel: Optional[str] = None
    billing_address: Optional[CustomerAddressRequest] = None
    shipping_address: Optional[CustomerAddressRequest] = None
    segments: Set[str]
    tags: Set[str]
    first_purchase_date: Optional[datetime] = None
    last_activity_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    version: int


# Campaign API Models
class CampaignBudgetRequest(BaseModel):
    """Campaign budget request"""
    total_budget: Decimal = Field(..., gt=0)
    daily_budget: Optional[Decimal] = None
    currency: str = "USD"
    budget_type: str = "total"
    auto_optimization: bool = False


class CampaignScheduleRequest(BaseModel):
    """Campaign schedule request"""
    start_date: datetime
    end_date: Optional[datetime] = None
    timezone: str = "UTC"
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None


class TargetingCriteriaRequest(BaseModel):
    """Targeting criteria request"""
    age_range: Optional[Dict[str, int]] = None
    gender: Optional[List[str]] = None
    location: Optional[Dict[str, Any]] = None
    languages: Optional[List[str]] = None
    interests: List[str] = Field(default_factory=list)
    behaviors: List[str] = Field(default_factory=list)
    job_titles: List[str] = Field(default_factory=list)
    industries: List[str] = Field(default_factory=list)
    company_sizes: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)


class CreateCampaignRequest(TenantContextModel):
    """Request to create a new campaign"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    campaign_type: CampaignType
    objective: CampaignObjective
    budget: CampaignBudgetRequest
    schedule: CampaignScheduleRequest
    targeting: Optional[TargetingCriteriaRequest] = None
    owner_id: Optional[UUID] = None


class LaunchCampaignRequest(TenantContextModel):
    """Request to launch a campaign"""
    user_id: UUID


class EnableAIOptimizationRequest(TenantContextModel):
    """Request to enable AI optimization"""
    optimization_goal: OptimizationGoal
    user_id: UUID


class CampaignResponse(BaseModel):
    """Campaign response model"""
    id: UUID
    tenant_id: UUID
    name: str
    description: Optional[str] = None
    campaign_type: CampaignType
    objective: CampaignObjective
    status: CampaignStatus
    budget: CampaignBudgetRequest
    schedule: CampaignScheduleRequest
    targeting: Optional[TargetingCriteriaRequest] = None
    optimization_goal: Optional[OptimizationGoal] = None
    ai_optimization_enabled: bool
    owner_id: Optional[UUID] = None
    team_members: List[UUID]
    tags: Set[str]
    created_at: datetime
    updated_at: datetime
    version: int


# Common Response Models
class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    tenant_id: str
    services: Dict[str, str]
    statistics: Dict[str, int]


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# List Response Models
class LeadListResponse(BaseModel):
    """Lead list response"""
    leads: List[LeadResponse]
    total_count: int
    page: int
    page_size: int


class CustomerListResponse(BaseModel):
    """Customer list response"""
    customers: List[CustomerResponse]
    total_count: int
    page: int
    page_size: int


class CampaignListResponse(BaseModel):
    """Campaign list response"""
    campaigns: List[CampaignResponse]
    total_count: int
    page: int
    page_size: int