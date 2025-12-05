"""
FastAPI Routers for Domain Repository Service

This module defines the REST API endpoints for managing domain aggregates.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
import structlog

from dependencies import get_domain_service, get_tenant_context
from models import *
from .application.services import DomainRepositoryService
from .domain.base import BusinessRuleViolation, TenantIsolationViolation, ConcurrencyException
from .domain.aggregates.lead import ContactInfo, LeadScore, LeadQualificationCriteria
from .domain.aggregates.customer import CustomerProfile, CustomerAddress
from .domain.aggregates.campaign import CampaignBudget, CampaignSchedule, TargetingCriteria

logger = structlog.get_logger(__name__)


# Lead Router
lead_router = APIRouter(prefix="/leads", tags=["leads"])


@lead_router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    request: CreateLeadRequest,
    service: DomainRepositoryService = Depends(get_domain_service)
):
    """Create a new lead"""
    
    try:
        # Convert request to domain objects
        contact_info = ContactInfo(**request.contact_info.dict())
        
        # Create lead
        lead = await service.get_lead_service().create_lead(
            tenant_id=request.tenant_id,
            contact_info=contact_info,
            source=request.source,
            utm_parameters=request.utm_parameters,
            campaign_id=request.campaign_id,
            referrer_url=request.referrer_url,
            landing_page=request.landing_page,
            custom_fields=request.custom_fields
        )
        
        # Convert to response model
        return LeadResponse(
            id=lead.id,
            tenant_id=lead.tenant_id,
            source=lead.source,
            status=lead.status,
            priority=lead.priority,
            contact_info=ContactInfoRequest(**lead.contact_info.dict()),
            is_qualified=lead.is_qualified,
            qualification_date=lead.qualification_date,
            assigned_to=lead.assigned_to,
            assigned_at=lead.assigned_at,
            converted_to_customer_id=lead.converted_to_customer_id,
            conversion_date=lead.conversion_date,
            conversion_value=lead.conversion_value,
            utm_parameters=lead.utm_parameters,
            campaign_id=lead.campaign_id,
            custom_fields=lead.custom_fields,
            tags=lead.tags,
            created_at=lead.created_at,
            updated_at=lead.updated_at,
            version=lead.version
        )
        
    except BusinessRuleViolation as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Business rule violation: {e.message}"
        )
    except Exception as e:
        logger.error("Failed to create lead", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@lead_router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: UUID,
    tenant_id: UUID = Depends(get_tenant_context),
    service: DomainRepositoryService = Depends(get_domain_service)
):
    """Get a lead by ID"""
    
    try:
        lead = await service.get_lead_service().lead_repository.get_by_id(lead_id, tenant_id)
        
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead not found"
            )
        
        return LeadResponse(
            id=lead.id,
            tenant_id=lead.tenant_id,
            source=lead.source,
            status=lead.status,
            priority=lead.priority,
            contact_info=ContactInfoRequest(**lead.contact_info.dict()),
            is_qualified=lead.is_qualified,
            qualification_date=lead.qualification_date,
            assigned_to=lead.assigned_to,
            assigned_at=lead.assigned_at,
            converted_to_customer_id=lead.converted_to_customer_id,
            conversion_date=lead.conversion_date,
            conversion_value=lead.conversion_value,
            utm_parameters=lead.utm_parameters,
            campaign_id=lead.campaign_id,
            custom_fields=lead.custom_fields,
            tags=lead.tags,
            created_at=lead.created_at,
            updated_at=lead.updated_at,
            version=lead.version
        )
        
    except TenantIsolationViolation as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    except Exception as e:
        logger.error("Failed to get lead", lead_id=str(lead_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@lead_router.post("/{lead_id}/qualify", response_model=LeadResponse)
async def qualify_lead(
    lead_id: UUID,
    request: QualifyLeadRequest,
    service: DomainRepositoryService = Depends(get_domain_service)
):
    """Qualify a lead"""
    
    try:
        # Convert request to domain objects
        qualification_criteria = None
        if request.qualification_criteria:
            qualification_criteria = LeadQualificationCriteria(**request.qualification_criteria.dict())
        
        score = None
        if request.score:
            score = LeadScore(**request.score.dict())
        
        # Qualify lead
        lead = await service.get_lead_service().qualify_lead(
            lead_id=lead_id,
            tenant_id=request.tenant_id,
            user_id=request.user_id,
            qualification_criteria=qualification_criteria,
            score=score
        )
        
        return LeadResponse(
            id=lead.id,
            tenant_id=lead.tenant_id,
            source=lead.source,
            status=lead.status,
            priority=lead.priority,
            contact_info=ContactInfoRequest(**lead.contact_info.dict()),
            is_qualified=lead.is_qualified,
            qualification_date=lead.qualification_date,
            assigned_to=lead.assigned_to,
            assigned_at=lead.assigned_at,
            converted_to_customer_id=lead.converted_to_customer_id,
            conversion_date=lead.conversion_date,
            conversion_value=lead.conversion_value,
            utm_parameters=lead.utm_parameters,
            campaign_id=lead.campaign_id,
            custom_fields=lead.custom_fields,
            tags=lead.tags,
            created_at=lead.created_at,
            updated_at=lead.updated_at,
            version=lead.version
        )
        
    except BusinessRuleViolation as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Business rule violation: {e.message}"
        )
    except Exception as e:
        logger.error("Failed to qualify lead", lead_id=str(lead_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@lead_router.post("/{lead_id}/convert", response_model=CustomerResponse)
async def convert_lead_to_customer(
    lead_id: UUID,
    request: ConvertLeadRequest,
    service: DomainRepositoryService = Depends(get_domain_service)
):
    """Convert a lead to a customer"""
    
    try:
        customer = await service.get_lead_service().convert_lead_to_customer(
            lead_id=lead_id,
            tenant_id=request.tenant_id,
            user_id=request.user_id,
            conversion_value=request.conversion_value,
            customer_type=request.customer_type
        )
        
        return CustomerResponse(
            id=customer.id,
            tenant_id=customer.tenant_id,
            profile=CustomerProfileRequest(**customer.profile.dict()),
            status=customer.status,
            customer_type=customer.customer_type,
            tier=customer.tier,
            converted_from_lead_id=customer.converted_from_lead_id,
            conversion_date=customer.conversion_date,
            acquisition_channel=customer.acquisition_channel,
            billing_address=CustomerAddressRequest(**customer.billing_address.dict()) if customer.billing_address else None,
            shipping_address=CustomerAddressRequest(**customer.shipping_address.dict()) if customer.shipping_address else None,
            segments=customer.segments,
            tags=customer.tags,
            first_purchase_date=customer.first_purchase_date,
            last_activity_date=customer.last_activity_date,
            created_at=customer.created_at,
            updated_at=customer.updated_at,
            version=customer.version
        )
        
    except BusinessRuleViolation as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Business rule violation: {e.message}"
        )
    except Exception as e:
        logger.error("Failed to convert lead", lead_id=str(lead_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@lead_router.get("/", response_model=LeadListResponse)
async def list_qualified_leads(
    tenant_id: UUID = Depends(get_tenant_context),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    service: DomainRepositoryService = Depends(get_domain_service)
):
    """List qualified leads"""
    
    try:
        offset = (page - 1) * page_size
        leads = await service.get_lead_service().get_qualified_leads(
            tenant_id=tenant_id,
            limit=page_size,
            offset=offset
        )
        
        lead_responses = [
            LeadResponse(
                id=lead.id,
                tenant_id=lead.tenant_id,
                source=lead.source,
                status=lead.status,
                priority=lead.priority,
                contact_info=ContactInfoRequest(**lead.contact_info.dict()),
                is_qualified=lead.is_qualified,
                qualification_date=lead.qualification_date,
                assigned_to=lead.assigned_to,
                assigned_at=lead.assigned_at,
                converted_to_customer_id=lead.converted_to_customer_id,
                conversion_date=lead.conversion_date,
                conversion_value=lead.conversion_value,
                utm_parameters=lead.utm_parameters,
                campaign_id=lead.campaign_id,
                custom_fields=lead.custom_fields,
                tags=lead.tags,
                created_at=lead.created_at,
                updated_at=lead.updated_at,
                version=lead.version
            )
            for lead in leads
        ]
        
        return LeadListResponse(
            leads=lead_responses,
            total_count=len(lead_responses),  # In production, get actual count
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error("Failed to list qualified leads", tenant_id=str(tenant_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Customer Router
customer_router = APIRouter(prefix="/customers", tags=["customers"])


@customer_router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: UUID,
    tenant_id: UUID = Depends(get_tenant_context),
    service: DomainRepositoryService = Depends(get_domain_service)
):
    """Get a customer by ID"""
    
    try:
        customer = await service.get_customer_service().customer_repository.get_by_id(customer_id, tenant_id)
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        return CustomerResponse(
            id=customer.id,
            tenant_id=customer.tenant_id,
            profile=CustomerProfileRequest(**customer.profile.dict()),
            status=customer.status,
            customer_type=customer.customer_type,
            tier=customer.tier,
            converted_from_lead_id=customer.converted_from_lead_id,
            conversion_date=customer.conversion_date,
            acquisition_channel=customer.acquisition_channel,
            billing_address=CustomerAddressRequest(**customer.billing_address.dict()) if customer.billing_address else None,
            shipping_address=CustomerAddressRequest(**customer.shipping_address.dict()) if customer.shipping_address else None,
            segments=customer.segments,
            tags=customer.tags,
            first_purchase_date=customer.first_purchase_date,
            last_activity_date=customer.last_activity_date,
            created_at=customer.created_at,
            updated_at=customer.updated_at,
            version=customer.version
        )
        
    except TenantIsolationViolation as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    except Exception as e:
        logger.error("Failed to get customer", customer_id=str(customer_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@customer_router.put("/{customer_id}/profile", response_model=CustomerResponse)
async def update_customer_profile(
    customer_id: UUID,
    request: UpdateCustomerProfileRequest,
    service: DomainRepositoryService = Depends(get_domain_service)
):
    """Update customer profile"""
    
    try:
        profile = CustomerProfile(**request.profile.dict())
        
        customer = await service.get_customer_service().update_customer_profile(
            customer_id=customer_id,
            tenant_id=request.tenant_id,
            new_profile=profile,
            user_id=request.user_id
        )
        
        return CustomerResponse(
            id=customer.id,
            tenant_id=customer.tenant_id,
            profile=CustomerProfileRequest(**customer.profile.dict()),
            status=customer.status,
            customer_type=customer.customer_type,
            tier=customer.tier,
            converted_from_lead_id=customer.converted_from_lead_id,
            conversion_date=customer.conversion_date,
            acquisition_channel=customer.acquisition_channel,
            billing_address=CustomerAddressRequest(**customer.billing_address.dict()) if customer.billing_address else None,
            shipping_address=CustomerAddressRequest(**customer.shipping_address.dict()) if customer.shipping_address else None,
            segments=customer.segments,
            tags=customer.tags,
            first_purchase_date=customer.first_purchase_date,
            last_activity_date=customer.last_activity_date,
            created_at=customer.created_at,
            updated_at=customer.updated_at,
            version=customer.version
        )
        
    except BusinessRuleViolation as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Business rule violation: {e.message}"
        )
    except Exception as e:
        logger.error("Failed to update customer profile", customer_id=str(customer_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@customer_router.get("/at-risk", response_model=CustomerListResponse)
async def list_at_risk_customers(
    tenant_id: UUID = Depends(get_tenant_context),
    min_churn_risk: int = Query(60, ge=0, le=100),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    service: DomainRepositoryService = Depends(get_domain_service)
):
    """List customers at churn risk"""
    
    try:
        offset = (page - 1) * page_size
        customers = await service.get_customer_service().get_at_risk_customers(
            tenant_id=tenant_id,
            min_churn_risk=min_churn_risk,
            limit=page_size,
            offset=offset
        )
        
        customer_responses = [
            CustomerResponse(
                id=customer.id,
                tenant_id=customer.tenant_id,
                profile=CustomerProfileRequest(**customer.profile.dict()),
                status=customer.status,
                customer_type=customer.customer_type,
                tier=customer.tier,
                converted_from_lead_id=customer.converted_from_lead_id,
                conversion_date=customer.conversion_date,
                acquisition_channel=customer.acquisition_channel,
                billing_address=CustomerAddressRequest(**customer.billing_address.dict()) if customer.billing_address else None,
                shipping_address=CustomerAddressRequest(**customer.shipping_address.dict()) if customer.shipping_address else None,
                segments=customer.segments,
                tags=customer.tags,
                first_purchase_date=customer.first_purchase_date,
                last_activity_date=customer.last_activity_date,
                created_at=customer.created_at,
                updated_at=customer.updated_at,
                version=customer.version
            )
            for customer in customers
        ]
        
        return CustomerListResponse(
            customers=customer_responses,
            total_count=len(customer_responses),
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error("Failed to list at-risk customers", tenant_id=str(tenant_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Campaign Router
campaign_router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@campaign_router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    request: CreateCampaignRequest,
    service: DomainRepositoryService = Depends(get_domain_service)
):
    """Create a new campaign"""
    
    try:
        # Convert request to domain objects
        budget = CampaignBudget(**request.budget.dict())
        schedule = CampaignSchedule(**request.schedule.dict())
        targeting = TargetingCriteria(**request.targeting.dict()) if request.targeting else None
        
        # Create campaign
        campaign = await service.get_campaign_service().create_campaign(
            tenant_id=request.tenant_id,
            name=request.name,
            campaign_type=request.campaign_type,
            objective=request.objective,
            budget=budget,
            schedule=schedule,
            owner_id=request.owner_id,
            targeting=targeting,
            description=request.description
        )
        
        return CampaignResponse(
            id=campaign.id,
            tenant_id=campaign.tenant_id,
            name=campaign.name,
            description=campaign.description,
            campaign_type=campaign.campaign_type,
            objective=campaign.objective,
            status=campaign.status,
            budget=CampaignBudgetRequest(**campaign.budget.dict()),
            schedule=CampaignScheduleRequest(**campaign.schedule.dict()),
            targeting=TargetingCriteriaRequest(**campaign.targeting.dict()) if campaign.targeting else None,
            optimization_goal=campaign.optimization_goal,
            ai_optimization_enabled=campaign.ai_optimization_enabled,
            owner_id=campaign.owner_id,
            team_members=campaign.team_members,
            tags=campaign.tags,
            created_at=campaign.created_at,
            updated_at=campaign.updated_at,
            version=campaign.version
        )
        
    except BusinessRuleViolation as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Business rule violation: {e.message}"
        )
    except Exception as e:
        logger.error("Failed to create campaign", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@campaign_router.post("/{campaign_id}/launch", response_model=CampaignResponse)
async def launch_campaign(
    campaign_id: UUID,
    request: LaunchCampaignRequest,
    service: DomainRepositoryService = Depends(get_domain_service)
):
    """Launch a campaign"""
    
    try:
        campaign = await service.get_campaign_service().launch_campaign(
            campaign_id=campaign_id,
            tenant_id=request.tenant_id,
            user_id=request.user_id
        )
        
        return CampaignResponse(
            id=campaign.id,
            tenant_id=campaign.tenant_id,
            name=campaign.name,
            description=campaign.description,
            campaign_type=campaign.campaign_type,
            objective=campaign.objective,
            status=campaign.status,
            budget=CampaignBudgetRequest(**campaign.budget.dict()),
            schedule=CampaignScheduleRequest(**campaign.schedule.dict()),
            targeting=TargetingCriteriaRequest(**campaign.targeting.dict()) if campaign.targeting else None,
            optimization_goal=campaign.optimization_goal,
            ai_optimization_enabled=campaign.ai_optimization_enabled,
            owner_id=campaign.owner_id,
            team_members=campaign.team_members,
            tags=campaign.tags,
            created_at=campaign.created_at,
            updated_at=campaign.updated_at,
            version=campaign.version
        )
        
    except BusinessRuleViolation as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Business rule violation: {e.message}"
        )
    except Exception as e:
        logger.error("Failed to launch campaign", campaign_id=str(campaign_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@campaign_router.get("/active", response_model=CampaignListResponse)
async def list_active_campaigns(
    tenant_id: UUID = Depends(get_tenant_context),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    service: DomainRepositoryService = Depends(get_domain_service)
):
    """List active campaigns"""
    
    try:
        offset = (page - 1) * page_size
        campaigns = await service.get_campaign_service().get_active_campaigns(
            tenant_id=tenant_id,
            limit=page_size,
            offset=offset
        )
        
        campaign_responses = [
            CampaignResponse(
                id=campaign.id,
                tenant_id=campaign.tenant_id,
                name=campaign.name,
                description=campaign.description,
                campaign_type=campaign.campaign_type,
                objective=campaign.objective,
                status=campaign.status,
                budget=CampaignBudgetRequest(**campaign.budget.dict()),
                schedule=CampaignScheduleRequest(**campaign.schedule.dict()),
                targeting=TargetingCriteriaRequest(**campaign.targeting.dict()) if campaign.targeting else None,
                optimization_goal=campaign.optimization_goal,
                ai_optimization_enabled=campaign.ai_optimization_enabled,
                owner_id=campaign.owner_id,
                team_members=campaign.team_members,
                tags=campaign.tags,
                created_at=campaign.created_at,
                updated_at=campaign.updated_at,
                version=campaign.version
            )
            for campaign in campaigns
        ]
        
        return CampaignListResponse(
            campaigns=campaign_responses,
            total_count=len(campaign_responses),
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error("Failed to list active campaigns", tenant_id=str(tenant_id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Health Check Router
health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("/", response_model=HealthCheckResponse)
async def health_check(
    tenant_id: UUID = Depends(get_tenant_context),
    service: DomainRepositoryService = Depends(get_domain_service)
):
    """Health check endpoint"""
    
    try:
        health_status = await service.health_check(tenant_id)
        return HealthCheckResponse(**health_status)
        
    except Exception as e:
        logger.error("Health check failed", tenant_id=str(tenant_id), error=str(e))
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )