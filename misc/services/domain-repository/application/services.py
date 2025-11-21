"""
Application Services for Domain Repository

This module provides application services that coordinate domain aggregates
and implement use cases for the BizOSaaS platform.
"""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from uuid import UUID

import structlog

from .domain.base import BusinessRuleViolation, TenantIsolationViolation
from .domain.aggregates.lead import Lead, LeadSource, LeadStatus, ContactInfo, LeadScore, LeadQualificationCriteria
from .domain.aggregates.customer import Customer, CustomerProfile, CustomerType, CustomerTier, CustomerAddress, SubscriptionInfo
from .domain.aggregates.campaign import Campaign, CampaignType, CampaignObjective, CampaignBudget, CampaignSchedule, TargetingCriteria, OptimizationGoal
from .infrastructure.repositories import LeadRepository, CustomerRepository, CampaignRepository

logger = structlog.get_logger(__name__)


class LeadService:
    """Application service for Lead aggregate operations"""
    
    def __init__(self, lead_repository: LeadRepository, customer_repository: CustomerRepository):
        self.lead_repository = lead_repository
        self.customer_repository = customer_repository
        self.logger = logger.bind(component="lead_service")
    
    async def create_lead(
        self,
        tenant_id: UUID,
        contact_info: ContactInfo,
        source: LeadSource,
        utm_parameters: Optional[Dict[str, str]] = None,
        campaign_id: Optional[UUID] = None,
        referrer_url: Optional[str] = None,
        landing_page: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Lead:
        """Create a new lead"""
        
        try:
            # Check if lead with this email already exists
            if contact_info.email:
                existing_lead = await self.lead_repository.find_by_email(contact_info.email, tenant_id)
                if existing_lead:
                    raise BusinessRuleViolation(
                        f"Lead with email {contact_info.email} already exists",
                        details={"existing_lead_id": str(existing_lead.id)}
                    )
            
            # Create lead
            lead = Lead(
                tenant_id=tenant_id,
                contact_info=contact_info,
                source=source,
                utm_parameters=utm_parameters or {},
                campaign_id=campaign_id,
                referrer_url=referrer_url,
                landing_page=landing_page,
                custom_fields=custom_fields or {}
            )
            
            # Save lead
            saved_lead = await self.lead_repository.save(lead)
            
            self.logger.info(
                "Lead created successfully",
                lead_id=str(saved_lead.id),
                tenant_id=str(tenant_id),
                source=source.value,
                email=contact_info.email
            )
            
            return saved_lead
            
        except Exception as e:
            self.logger.error(
                "Failed to create lead",
                tenant_id=str(tenant_id),
                source=source.value,
                email=contact_info.email,
                error=str(e)
            )
            raise
    
    async def qualify_lead(
        self,
        lead_id: UUID,
        tenant_id: UUID,
        user_id: UUID,
        qualification_criteria: Optional[LeadQualificationCriteria] = None,
        score: Optional[LeadScore] = None
    ) -> Lead:
        """Qualify a lead"""
        
        try:
            # Get lead
            lead = await self.lead_repository.get_by_id(lead_id, tenant_id)
            if not lead:
                raise BusinessRuleViolation(f"Lead {lead_id} not found")
            
            # Update score if provided
            if score:
                lead.update_score(score, user_id)
            
            # Qualify lead
            lead.qualify_lead(user_id, qualification_criteria)
            
            # Save lead
            saved_lead = await self.lead_repository.save(lead)
            
            self.logger.info(
                "Lead qualified successfully",
                lead_id=str(lead_id),
                tenant_id=str(tenant_id),
                qualified_by=str(user_id)
            )
            
            return saved_lead
            
        except Exception as e:
            self.logger.error(
                "Failed to qualify lead",
                lead_id=str(lead_id),
                tenant_id=str(tenant_id),
                user_id=str(user_id),
                error=str(e)
            )
            raise
    
    async def convert_lead_to_customer(
        self,
        lead_id: UUID,
        tenant_id: UUID,
        user_id: UUID,
        conversion_value: Optional[Decimal] = None,
        customer_type: CustomerType = CustomerType.INDIVIDUAL,
        billing_address: Optional[CustomerAddress] = None
    ) -> Customer:
        """Convert a qualified lead to a customer"""
        
        try:
            # Get lead
            lead = await self.lead_repository.get_by_id(lead_id, tenant_id)
            if not lead:
                raise BusinessRuleViolation(f"Lead {lead_id} not found")
            
            if not lead.is_qualified:
                raise BusinessRuleViolation("Cannot convert unqualified lead to customer")
            
            # Check if customer with this email already exists
            if lead.contact_info.email:
                existing_customer = await self.customer_repository.find_by_email(lead.contact_info.email, tenant_id)
                if existing_customer:
                    raise BusinessRuleViolation(
                        f"Customer with email {lead.contact_info.email} already exists",
                        details={"existing_customer_id": str(existing_customer.id)}
                    )
            
            # Create customer profile from lead contact info
            customer_profile = CustomerProfile(
                first_name=lead.contact_info.first_name,
                last_name=lead.contact_info.last_name,
                email=lead.contact_info.email,
                phone=lead.contact_info.phone,
                company_name=lead.contact_info.company,
                job_title=lead.contact_info.job_title,
                website=lead.contact_info.website
            )
            
            # Create customer
            customer = Customer.create_from_lead(
                lead_id=lead.id,
                profile=customer_profile,
                tenant_id=tenant_id,
                acquisition_channel=lead.source.value
            )
            
            customer.customer_type = customer_type
            
            if billing_address:
                customer.billing_address = billing_address
            
            # Convert lead
            lead.convert_to_customer(customer.id, conversion_value, user_id)
            
            # Save both entities
            saved_customer = await self.customer_repository.save(customer)
            await self.lead_repository.save(lead)
            
            self.logger.info(
                "Lead converted to customer successfully",
                lead_id=str(lead_id),
                customer_id=str(customer.id),
                tenant_id=str(tenant_id),
                converted_by=str(user_id)
            )
            
            return saved_customer
            
        except Exception as e:
            self.logger.error(
                "Failed to convert lead to customer",
                lead_id=str(lead_id),
                tenant_id=str(tenant_id),
                user_id=str(user_id),
                error=str(e)
            )
            raise
    
    async def update_lead_score(
        self,
        lead_id: UUID,
        tenant_id: UUID,
        new_score: LeadScore,
        user_id: Optional[UUID] = None
    ) -> Lead:
        """Update lead score"""
        
        try:
            # Get lead
            lead = await self.lead_repository.get_by_id(lead_id, tenant_id)
            if not lead:
                raise BusinessRuleViolation(f"Lead {lead_id} not found")
            
            # Update score
            lead.update_score(new_score, user_id)
            
            # Save lead
            saved_lead = await self.lead_repository.save(lead)
            
            self.logger.info(
                "Lead score updated successfully",
                lead_id=str(lead_id),
                tenant_id=str(tenant_id),
                new_score=new_score.total_score
            )
            
            return saved_lead
            
        except Exception as e:
            self.logger.error(
                "Failed to update lead score",
                lead_id=str(lead_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def assign_lead(
        self,
        lead_id: UUID,
        tenant_id: UUID,
        assigned_to: UUID,
        assigned_by: UUID
    ) -> Lead:
        """Assign lead to a user"""
        
        try:
            # Get lead
            lead = await self.lead_repository.get_by_id(lead_id, tenant_id)
            if not lead:
                raise BusinessRuleViolation(f"Lead {lead_id} not found")
            
            # Assign lead
            lead.assign_to_user(assigned_to, assigned_by)
            
            # Save lead
            saved_lead = await self.lead_repository.save(lead)
            
            self.logger.info(
                "Lead assigned successfully",
                lead_id=str(lead_id),
                tenant_id=str(tenant_id),
                assigned_to=str(assigned_to),
                assigned_by=str(assigned_by)
            )
            
            return saved_lead
            
        except Exception as e:
            self.logger.error(
                "Failed to assign lead",
                lead_id=str(lead_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def get_qualified_leads(
        self,
        tenant_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[Lead]:
        """Get qualified leads for a tenant"""
        
        try:
            leads = await self.lead_repository.find_qualified_leads(tenant_id, limit, offset)
            
            self.logger.debug(
                "Retrieved qualified leads",
                tenant_id=str(tenant_id),
                count=len(leads)
            )
            
            return leads
            
        except Exception as e:
            self.logger.error(
                "Failed to get qualified leads",
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise


class CustomerService:
    """Application service for Customer aggregate operations"""
    
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository
        self.logger = logger.bind(component="customer_service")
    
    async def update_customer_profile(
        self,
        customer_id: UUID,
        tenant_id: UUID,
        new_profile: CustomerProfile,
        user_id: Optional[UUID] = None
    ) -> Customer:
        """Update customer profile"""
        
        try:
            # Get customer
            customer = await self.customer_repository.get_by_id(customer_id, tenant_id)
            if not customer:
                raise BusinessRuleViolation(f"Customer {customer_id} not found")
            
            # Update profile
            customer.update_profile(new_profile, user_id)
            
            # Save customer
            saved_customer = await self.customer_repository.save(customer)
            
            self.logger.info(
                "Customer profile updated successfully",
                customer_id=str(customer_id),
                tenant_id=str(tenant_id),
                updated_by=str(user_id) if user_id else None
            )
            
            return saved_customer
            
        except Exception as e:
            self.logger.error(
                "Failed to update customer profile",
                customer_id=str(customer_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def upgrade_customer_tier(
        self,
        customer_id: UUID,
        tenant_id: UUID,
        new_tier: CustomerTier,
        user_id: Optional[UUID] = None
    ) -> Customer:
        """Upgrade customer tier"""
        
        try:
            # Get customer
            customer = await self.customer_repository.get_by_id(customer_id, tenant_id)
            if not customer:
                raise BusinessRuleViolation(f"Customer {customer_id} not found")
            
            # Upgrade tier
            customer.upgrade_tier(new_tier, user_id)
            
            # Save customer
            saved_customer = await self.customer_repository.save(customer)
            
            self.logger.info(
                "Customer tier upgraded successfully",
                customer_id=str(customer_id),
                tenant_id=str(tenant_id),
                new_tier=new_tier.value,
                upgraded_by=str(user_id) if user_id else None
            )
            
            return saved_customer
            
        except Exception as e:
            self.logger.error(
                "Failed to upgrade customer tier",
                customer_id=str(customer_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def record_customer_purchase(
        self,
        customer_id: UUID,
        tenant_id: UUID,
        order_value: Decimal,
        order_date: Optional[datetime] = None
    ) -> Customer:
        """Record a customer purchase"""
        
        try:
            # Get customer
            customer = await self.customer_repository.get_by_id(customer_id, tenant_id)
            if not customer:
                raise BusinessRuleViolation(f"Customer {customer_id} not found")
            
            # Record purchase
            customer.record_purchase(order_value, order_date)
            
            # Save customer
            saved_customer = await self.customer_repository.save(customer)
            
            self.logger.info(
                "Customer purchase recorded successfully",
                customer_id=str(customer_id),
                tenant_id=str(tenant_id),
                order_value=float(order_value)
            )
            
            return saved_customer
            
        except Exception as e:
            self.logger.error(
                "Failed to record customer purchase",
                customer_id=str(customer_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def get_at_risk_customers(
        self,
        tenant_id: UUID,
        min_churn_risk: int = 60,
        limit: int = 100,
        offset: int = 0
    ) -> List[Customer]:
        """Get customers at churn risk"""
        
        try:
            customers = await self.customer_repository.find_at_risk_customers(
                tenant_id, min_churn_risk, limit, offset
            )
            
            self.logger.debug(
                "Retrieved at-risk customers",
                tenant_id=str(tenant_id),
                count=len(customers),
                min_churn_risk=min_churn_risk
            )
            
            return customers
            
        except Exception as e:
            self.logger.error(
                "Failed to get at-risk customers",
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise


class CampaignService:
    """Application service for Campaign aggregate operations"""
    
    def __init__(self, campaign_repository: CampaignRepository):
        self.campaign_repository = campaign_repository
        self.logger = logger.bind(component="campaign_service")
    
    async def create_campaign(
        self,
        tenant_id: UUID,
        name: str,
        campaign_type: CampaignType,
        objective: CampaignObjective,
        budget: CampaignBudget,
        schedule: CampaignSchedule,
        owner_id: Optional[UUID] = None,
        targeting: Optional[TargetingCriteria] = None,
        description: Optional[str] = None
    ) -> Campaign:
        """Create a new campaign"""
        
        try:
            # Create campaign
            campaign = Campaign(
                tenant_id=tenant_id,
                name=name,
                campaign_type=campaign_type,
                objective=objective,
                budget=budget,
                schedule=schedule,
                owner_id=owner_id,
                targeting=targeting or TargetingCriteria(),
                description=description
            )
            
            # Save campaign
            saved_campaign = await self.campaign_repository.save(campaign)
            
            self.logger.info(
                "Campaign created successfully",
                campaign_id=str(saved_campaign.id),
                tenant_id=str(tenant_id),
                name=name,
                campaign_type=campaign_type.value,
                budget=float(budget.total_budget)
            )
            
            return saved_campaign
            
        except Exception as e:
            self.logger.error(
                "Failed to create campaign",
                tenant_id=str(tenant_id),
                name=name,
                campaign_type=campaign_type.value,
                error=str(e)
            )
            raise
    
    async def launch_campaign(
        self,
        campaign_id: UUID,
        tenant_id: UUID,
        user_id: UUID
    ) -> Campaign:
        """Launch a campaign"""
        
        try:
            # Get campaign
            campaign = await self.campaign_repository.get_by_id(campaign_id, tenant_id)
            if not campaign:
                raise BusinessRuleViolation(f"Campaign {campaign_id} not found")
            
            # Launch campaign
            campaign.launch_campaign(user_id)
            
            # Save campaign
            saved_campaign = await self.campaign_repository.save(campaign)
            
            self.logger.info(
                "Campaign launched successfully",
                campaign_id=str(campaign_id),
                tenant_id=str(tenant_id),
                launched_by=str(user_id)
            )
            
            return saved_campaign
            
        except Exception as e:
            self.logger.error(
                "Failed to launch campaign",
                campaign_id=str(campaign_id),
                tenant_id=str(tenant_id),
                user_id=str(user_id),
                error=str(e)
            )
            raise
    
    async def enable_ai_optimization(
        self,
        campaign_id: UUID,
        tenant_id: UUID,
        optimization_goal: OptimizationGoal,
        user_id: UUID
    ) -> Campaign:
        """Enable AI optimization for a campaign"""
        
        try:
            # Get campaign
            campaign = await self.campaign_repository.get_by_id(campaign_id, tenant_id)
            if not campaign:
                raise BusinessRuleViolation(f"Campaign {campaign_id} not found")
            
            # Enable AI optimization
            campaign.enable_ai_optimization(optimization_goal, user_id)
            
            # Save campaign
            saved_campaign = await self.campaign_repository.save(campaign)
            
            self.logger.info(
                "AI optimization enabled for campaign",
                campaign_id=str(campaign_id),
                tenant_id=str(tenant_id),
                optimization_goal=optimization_goal.value,
                enabled_by=str(user_id)
            )
            
            return saved_campaign
            
        except Exception as e:
            self.logger.error(
                "Failed to enable AI optimization",
                campaign_id=str(campaign_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def get_active_campaigns(
        self,
        tenant_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[Campaign]:
        """Get active campaigns for a tenant"""
        
        try:
            campaigns = await self.campaign_repository.find_active_campaigns(tenant_id, limit, offset)
            
            self.logger.debug(
                "Retrieved active campaigns",
                tenant_id=str(tenant_id),
                count=len(campaigns)
            )
            
            return campaigns
            
        except Exception as e:
            self.logger.error(
                "Failed to get active campaigns",
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise


class DomainRepositoryService:
    """Main service that coordinates all domain operations"""
    
    def __init__(
        self,
        lead_repository: LeadRepository,
        customer_repository: CustomerRepository,
        campaign_repository: CampaignRepository
    ):
        self.lead_service = LeadService(lead_repository, customer_repository)
        self.customer_service = CustomerService(customer_repository)
        self.campaign_service = CampaignService(campaign_repository)
        self.logger = logger.bind(component="domain_repository_service")
    
    def get_lead_service(self) -> LeadService:
        """Get lead service"""
        return self.lead_service
    
    def get_customer_service(self) -> CustomerService:
        """Get customer service"""
        return self.customer_service
    
    def get_campaign_service(self) -> CampaignService:
        """Get campaign service"""
        return self.campaign_service
    
    async def health_check(self, tenant_id: UUID) -> Dict[str, Any]:
        """Perform health check on all services"""
        
        try:
            health_status = {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "tenant_id": str(tenant_id),
                "services": {
                    "lead_service": "healthy",
                    "customer_service": "healthy",
                    "campaign_service": "healthy"
                },
                "statistics": {
                    "total_leads": 0,
                    "qualified_leads": 0,
                    "total_customers": 0,
                    "at_risk_customers": 0,
                    "active_campaigns": 0
                }
            }
            
            # Get basic statistics
            try:
                qualified_leads = await self.lead_service.get_qualified_leads(tenant_id, limit=1)
                health_status["statistics"]["qualified_leads"] = len(qualified_leads)
            except Exception:
                health_status["services"]["lead_service"] = "degraded"
            
            try:
                at_risk_customers = await self.customer_service.get_at_risk_customers(tenant_id, limit=1)
                health_status["statistics"]["at_risk_customers"] = len(at_risk_customers)
            except Exception:
                health_status["services"]["customer_service"] = "degraded"
            
            try:
                active_campaigns = await self.campaign_service.get_active_campaigns(tenant_id, limit=1)
                health_status["statistics"]["active_campaigns"] = len(active_campaigns)
            except Exception:
                health_status["services"]["campaign_service"] = "degraded"
            
            # Determine overall status
            service_statuses = list(health_status["services"].values())
            if "unhealthy" in service_statuses:
                health_status["status"] = "unhealthy"
            elif "degraded" in service_statuses:
                health_status["status"] = "degraded"
            
            return health_status
            
        except Exception as e:
            self.logger.error(
                "Health check failed",
                tenant_id=str(tenant_id),
                error=str(e)
            )
            
            return {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "tenant_id": str(tenant_id),
                "error": str(e)
            }