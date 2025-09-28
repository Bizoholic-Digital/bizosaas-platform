"""
Repository Implementations for Domain Aggregates

This module provides concrete implementations of repository interfaces
using SQLAlchemy for data persistence and Event Bus for event publishing.
"""

from abc import ABC
from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy import and_, desc, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import structlog

from .domain.base import Repository, AggregateRoot, EventPublisher, ConcurrencyException, TenantIsolationViolation
from .domain.aggregates.lead import Lead, LeadEntity, LeadStatus, LeadSource
from .domain.aggregates.customer import Customer, CustomerEntity, CustomerStatus, CustomerTier
from .domain.aggregates.campaign import Campaign, CampaignEntity, CampaignStatus, CampaignType

logger = structlog.get_logger(__name__)


class BaseRepository(ABC):
    """Base repository with common functionality"""
    
    def __init__(self, session: AsyncSession, event_publisher: EventPublisher):
        self.session = session
        self.event_publisher = event_publisher
        self.logger = logger.bind(component=f"{self.__class__.__name__}")
    
    async def _ensure_tenant_isolation(self, entity_id: UUID, tenant_id: UUID, entity_class) -> None:
        """Ensure entity belongs to the specified tenant"""
        
        query = select(entity_class).where(
            and_(
                entity_class.id == entity_id,
                entity_class.tenant_id == tenant_id
            )
        )
        
        result = await self.session.execute(query)
        entity = result.scalar_one_or_none()
        
        if entity is None:
            raise TenantIsolationViolation(
                f"Entity {entity_id} not found or does not belong to tenant {tenant_id}"
            )
    
    async def _check_optimistic_concurrency(self, entity, expected_version: int) -> None:
        """Check optimistic concurrency control"""
        
        if entity.version != expected_version:
            raise ConcurrencyException(
                f"Concurrency conflict: expected version {expected_version}, got {entity.version}",
                details={
                    "expected_version": expected_version,
                    "actual_version": entity.version,
                    "entity_id": str(entity.id)
                }
            )


class LeadRepository(BaseRepository):
    """Repository for Lead aggregate"""
    
    async def get_by_id(self, lead_id: UUID, tenant_id: UUID) -> Optional[Lead]:
        """Get lead by ID within tenant context"""
        
        try:
            query = select(LeadEntity).where(
                and_(
                    LeadEntity.id == lead_id,
                    LeadEntity.tenant_id == tenant_id,
                    LeadEntity.is_active == True
                )
            )
            
            result = await self.session.execute(query)
            lead_entity = result.scalar_one_or_none()
            
            if lead_entity is None:
                return None
            
            domain_lead = lead_entity.to_domain()
            
            self.logger.debug(
                "Lead retrieved successfully",
                lead_id=str(lead_id),
                tenant_id=str(tenant_id)
            )
            
            return domain_lead
            
        except Exception as e:
            self.logger.error(
                "Failed to retrieve lead",
                lead_id=str(lead_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def save(self, lead: Lead) -> Lead:
        """Save lead and publish domain events"""
        
        try:
            # Check if this is a new lead or an update
            query = select(LeadEntity).where(
                and_(
                    LeadEntity.id == lead.id,
                    LeadEntity.tenant_id == lead.tenant_id
                )
            )
            
            result = await self.session.execute(query)
            existing_entity = result.scalar_one_or_none()
            
            if existing_entity is not None:
                # Update existing lead
                await self._check_optimistic_concurrency(existing_entity, lead.version - 1)
                
                # Update the entity with new data
                updated_entity = LeadEntity.from_domain(lead)
                
                # Copy the new values to the existing entity
                for key, value in updated_entity.__dict__.items():
                    if not key.startswith('_') and key != 'id':
                        setattr(existing_entity, key, value)
                
                lead_entity = existing_entity
            else:
                # Create new lead
                lead_entity = LeadEntity.from_domain(lead)
                self.session.add(lead_entity)
            
            # Flush to get any database-generated values
            await self.session.flush()
            
            # Publish domain events
            domain_events = lead.domain_events
            if domain_events:
                await self.event_publisher.publish_many(domain_events)
                lead.mark_events_as_committed()
            
            self.logger.info(
                "Lead saved successfully",
                lead_id=str(lead.id),
                tenant_id=str(lead.tenant_id),
                version=lead.version,
                events_published=len(domain_events)
            )
            
            return lead
            
        except Exception as e:
            self.logger.error(
                "Failed to save lead",
                lead_id=str(lead.id),
                tenant_id=str(lead.tenant_id),
                error=str(e)
            )
            raise
    
    async def delete(self, lead_id: UUID, tenant_id: UUID) -> bool:
        """Soft delete lead by ID within tenant context"""
        
        try:
            await self._ensure_tenant_isolation(lead_id, tenant_id, LeadEntity)
            
            query = select(LeadEntity).where(
                and_(
                    LeadEntity.id == lead_id,
                    LeadEntity.tenant_id == tenant_id
                )
            )
            
            result = await self.session.execute(query)
            lead_entity = result.scalar_one_or_none()
            
            if lead_entity is not None:
                lead_entity.is_active = False
                await self.session.flush()
                
                self.logger.info(
                    "Lead deleted successfully",
                    lead_id=str(lead_id),
                    tenant_id=str(tenant_id)
                )
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(
                "Failed to delete lead",
                lead_id=str(lead_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def exists(self, lead_id: UUID, tenant_id: UUID) -> bool:
        """Check if lead exists within tenant context"""
        
        try:
            query = select(func.count(LeadEntity.id)).where(
                and_(
                    LeadEntity.id == lead_id,
                    LeadEntity.tenant_id == tenant_id,
                    LeadEntity.is_active == True
                )
            )
            
            result = await self.session.execute(query)
            count = result.scalar()
            
            return count > 0
            
        except Exception as e:
            self.logger.error(
                "Failed to check lead existence",
                lead_id=str(lead_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def find_by_email(self, email: str, tenant_id: UUID) -> Optional[Lead]:
        """Find lead by email within tenant context"""
        
        try:
            # Search in contact_info JSON field
            query = select(LeadEntity).where(
                and_(
                    LeadEntity.tenant_id == tenant_id,
                    LeadEntity.is_active == True,
                    LeadEntity.contact_info['email'].astext == email
                )
            )
            
            result = await self.session.execute(query)
            lead_entity = result.scalar_one_or_none()
            
            if lead_entity is None:
                return None
            
            return lead_entity.to_domain()
            
        except Exception as e:
            self.logger.error(
                "Failed to find lead by email",
                email=email,
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def find_by_status(self, status: LeadStatus, tenant_id: UUID, limit: int = 100, offset: int = 0) -> List[Lead]:
        """Find leads by status within tenant context"""
        
        try:
            query = select(LeadEntity).where(
                and_(
                    LeadEntity.tenant_id == tenant_id,
                    LeadEntity.status == status,
                    LeadEntity.is_active == True
                )
            ).order_by(desc(LeadEntity.created_at)).limit(limit).offset(offset)
            
            result = await self.session.execute(query)
            lead_entities = result.scalars().all()
            
            return [entity.to_domain() for entity in lead_entities]
            
        except Exception as e:
            self.logger.error(
                "Failed to find leads by status",
                status=status.value,
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def find_qualified_leads(self, tenant_id: UUID, limit: int = 100, offset: int = 0) -> List[Lead]:
        """Find qualified leads within tenant context"""
        
        try:
            query = select(LeadEntity).where(
                and_(
                    LeadEntity.tenant_id == tenant_id,
                    LeadEntity.is_qualified == True,
                    LeadEntity.is_active == True
                )
            ).order_by(desc(LeadEntity.qualification_date)).limit(limit).offset(offset)
            
            result = await self.session.execute(query)
            lead_entities = result.scalars().all()
            
            return [entity.to_domain() for entity in lead_entities]
            
        except Exception as e:
            self.logger.error(
                "Failed to find qualified leads",
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise


class CustomerRepository(BaseRepository):
    """Repository for Customer aggregate"""
    
    async def get_by_id(self, customer_id: UUID, tenant_id: UUID) -> Optional[Customer]:
        """Get customer by ID within tenant context"""
        
        try:
            query = select(CustomerEntity).where(
                and_(
                    CustomerEntity.id == customer_id,
                    CustomerEntity.tenant_id == tenant_id,
                    CustomerEntity.is_active == True
                )
            )
            
            result = await self.session.execute(query)
            customer_entity = result.scalar_one_or_none()
            
            if customer_entity is None:
                return None
            
            domain_customer = customer_entity.to_domain()
            
            self.logger.debug(
                "Customer retrieved successfully",
                customer_id=str(customer_id),
                tenant_id=str(tenant_id)
            )
            
            return domain_customer
            
        except Exception as e:
            self.logger.error(
                "Failed to retrieve customer",
                customer_id=str(customer_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def save(self, customer: Customer) -> Customer:
        """Save customer and publish domain events"""
        
        try:
            # Check if this is a new customer or an update
            query = select(CustomerEntity).where(
                and_(
                    CustomerEntity.id == customer.id,
                    CustomerEntity.tenant_id == customer.tenant_id
                )
            )
            
            result = await self.session.execute(query)
            existing_entity = result.scalar_one_or_none()
            
            if existing_entity is not None:
                # Update existing customer
                await self._check_optimistic_concurrency(existing_entity, customer.version - 1)
                
                # Update the entity with new data
                updated_entity = CustomerEntity.from_domain(customer)
                
                # Copy the new values to the existing entity
                for key, value in updated_entity.__dict__.items():
                    if not key.startswith('_') and key != 'id':
                        setattr(existing_entity, key, value)
                
                customer_entity = existing_entity
            else:
                # Create new customer
                customer_entity = CustomerEntity.from_domain(customer)
                self.session.add(customer_entity)
            
            # Flush to get any database-generated values
            await self.session.flush()
            
            # Publish domain events
            domain_events = customer.domain_events
            if domain_events:
                await self.event_publisher.publish_many(domain_events)
                customer.mark_events_as_committed()
            
            self.logger.info(
                "Customer saved successfully",
                customer_id=str(customer.id),
                tenant_id=str(customer.tenant_id),
                version=customer.version,
                events_published=len(domain_events)
            )
            
            return customer
            
        except Exception as e:
            self.logger.error(
                "Failed to save customer",
                customer_id=str(customer.id),
                tenant_id=str(customer.tenant_id),
                error=str(e)
            )
            raise
    
    async def delete(self, customer_id: UUID, tenant_id: UUID) -> bool:
        """Soft delete customer by ID within tenant context"""
        
        try:
            await self._ensure_tenant_isolation(customer_id, tenant_id, CustomerEntity)
            
            query = select(CustomerEntity).where(
                and_(
                    CustomerEntity.id == customer_id,
                    CustomerEntity.tenant_id == tenant_id
                )
            )
            
            result = await self.session.execute(query)
            customer_entity = result.scalar_one_or_none()
            
            if customer_entity is not None:
                customer_entity.is_active = False
                await self.session.flush()
                
                self.logger.info(
                    "Customer deleted successfully",
                    customer_id=str(customer_id),
                    tenant_id=str(tenant_id)
                )
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(
                "Failed to delete customer",
                customer_id=str(customer_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def exists(self, customer_id: UUID, tenant_id: UUID) -> bool:
        """Check if customer exists within tenant context"""
        
        try:
            query = select(func.count(CustomerEntity.id)).where(
                and_(
                    CustomerEntity.id == customer_id,
                    CustomerEntity.tenant_id == tenant_id,
                    CustomerEntity.is_active == True
                )
            )
            
            result = await self.session.execute(query)
            count = result.scalar()
            
            return count > 0
            
        except Exception as e:
            self.logger.error(
                "Failed to check customer existence",
                customer_id=str(customer_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def find_by_email(self, email: str, tenant_id: UUID) -> Optional[Customer]:
        """Find customer by email within tenant context"""
        
        try:
            # Search in profile_data JSON field
            query = select(CustomerEntity).where(
                and_(
                    CustomerEntity.tenant_id == tenant_id,
                    CustomerEntity.is_active == True,
                    CustomerEntity.profile_data['email'].astext == email
                )
            )
            
            result = await self.session.execute(query)
            customer_entity = result.scalar_one_or_none()
            
            if customer_entity is None:
                return None
            
            return customer_entity.to_domain()
            
        except Exception as e:
            self.logger.error(
                "Failed to find customer by email",
                email=email,
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def find_by_tier(self, tier: CustomerTier, tenant_id: UUID, limit: int = 100, offset: int = 0) -> List[Customer]:
        """Find customers by tier within tenant context"""
        
        try:
            query = select(CustomerEntity).where(
                and_(
                    CustomerEntity.tenant_id == tenant_id,
                    CustomerEntity.tier == tier,
                    CustomerEntity.is_active == True
                )
            ).order_by(desc(CustomerEntity.created_at)).limit(limit).offset(offset)
            
            result = await self.session.execute(query)
            customer_entities = result.scalars().all()
            
            return [entity.to_domain() for entity in customer_entities]
            
        except Exception as e:
            self.logger.error(
                "Failed to find customers by tier",
                tier=tier.value,
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def find_at_risk_customers(self, tenant_id: UUID, min_churn_risk: int = 60, limit: int = 100, offset: int = 0) -> List[Customer]:
        """Find customers at churn risk within tenant context"""
        
        try:
            # Search in metrics_data JSON field for churn_risk_score
            query = select(CustomerEntity).where(
                and_(
                    CustomerEntity.tenant_id == tenant_id,
                    CustomerEntity.is_active == True,
                    CustomerEntity.metrics_data['churn_risk_score'].astext.cast(func.numeric) >= min_churn_risk
                )
            ).order_by(desc(CustomerEntity.metrics_data['churn_risk_score'].astext.cast(func.numeric))).limit(limit).offset(offset)
            
            result = await self.session.execute(query)
            customer_entities = result.scalars().all()
            
            return [entity.to_domain() for entity in customer_entities]
            
        except Exception as e:
            self.logger.error(
                "Failed to find at-risk customers",
                tenant_id=str(tenant_id),
                min_churn_risk=min_churn_risk,
                error=str(e)
            )
            raise


class CampaignRepository(BaseRepository):
    """Repository for Campaign aggregate"""
    
    async def get_by_id(self, campaign_id: UUID, tenant_id: UUID) -> Optional[Campaign]:
        """Get campaign by ID within tenant context"""
        
        try:
            query = select(CampaignEntity).where(
                and_(
                    CampaignEntity.id == campaign_id,
                    CampaignEntity.tenant_id == tenant_id,
                    CampaignEntity.is_active == True
                )
            )
            
            result = await self.session.execute(query)
            campaign_entity = result.scalar_one_or_none()
            
            if campaign_entity is None:
                return None
            
            domain_campaign = campaign_entity.to_domain()
            
            self.logger.debug(
                "Campaign retrieved successfully",
                campaign_id=str(campaign_id),
                tenant_id=str(tenant_id)
            )
            
            return domain_campaign
            
        except Exception as e:
            self.logger.error(
                "Failed to retrieve campaign",
                campaign_id=str(campaign_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def save(self, campaign: Campaign) -> Campaign:
        """Save campaign and publish domain events"""
        
        try:
            # Check if this is a new campaign or an update
            query = select(CampaignEntity).where(
                and_(
                    CampaignEntity.id == campaign.id,
                    CampaignEntity.tenant_id == campaign.tenant_id
                )
            )
            
            result = await self.session.execute(query)
            existing_entity = result.scalar_one_or_none()
            
            if existing_entity is not None:
                # Update existing campaign
                await self._check_optimistic_concurrency(existing_entity, campaign.version - 1)
                
                # Update the entity with new data
                updated_entity = CampaignEntity.from_domain(campaign)
                
                # Copy the new values to the existing entity
                for key, value in updated_entity.__dict__.items():
                    if not key.startswith('_') and key != 'id':
                        setattr(existing_entity, key, value)
                
                campaign_entity = existing_entity
            else:
                # Create new campaign
                campaign_entity = CampaignEntity.from_domain(campaign)
                self.session.add(campaign_entity)
            
            # Flush to get any database-generated values
            await self.session.flush()
            
            # Publish domain events
            domain_events = campaign.domain_events
            if domain_events:
                await self.event_publisher.publish_many(domain_events)
                campaign.mark_events_as_committed()
            
            self.logger.info(
                "Campaign saved successfully",
                campaign_id=str(campaign.id),
                tenant_id=str(campaign.tenant_id),
                version=campaign.version,
                events_published=len(domain_events)
            )
            
            return campaign
            
        except Exception as e:
            self.logger.error(
                "Failed to save campaign",
                campaign_id=str(campaign.id),
                tenant_id=str(campaign.tenant_id),
                error=str(e)
            )
            raise
    
    async def delete(self, campaign_id: UUID, tenant_id: UUID) -> bool:
        """Soft delete campaign by ID within tenant context"""
        
        try:
            await self._ensure_tenant_isolation(campaign_id, tenant_id, CampaignEntity)
            
            query = select(CampaignEntity).where(
                and_(
                    CampaignEntity.id == campaign_id,
                    CampaignEntity.tenant_id == tenant_id
                )
            )
            
            result = await self.session.execute(query)
            campaign_entity = result.scalar_one_or_none()
            
            if campaign_entity is not None:
                campaign_entity.is_active = False
                await self.session.flush()
                
                self.logger.info(
                    "Campaign deleted successfully",
                    campaign_id=str(campaign_id),
                    tenant_id=str(tenant_id)
                )
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(
                "Failed to delete campaign",
                campaign_id=str(campaign_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def exists(self, campaign_id: UUID, tenant_id: UUID) -> bool:
        """Check if campaign exists within tenant context"""
        
        try:
            query = select(func.count(CampaignEntity.id)).where(
                and_(
                    CampaignEntity.id == campaign_id,
                    CampaignEntity.tenant_id == tenant_id,
                    CampaignEntity.is_active == True
                )
            )
            
            result = await self.session.execute(query)
            count = result.scalar()
            
            return count > 0
            
        except Exception as e:
            self.logger.error(
                "Failed to check campaign existence",
                campaign_id=str(campaign_id),
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def find_by_status(self, status: CampaignStatus, tenant_id: UUID, limit: int = 100, offset: int = 0) -> List[Campaign]:
        """Find campaigns by status within tenant context"""
        
        try:
            query = select(CampaignEntity).where(
                and_(
                    CampaignEntity.tenant_id == tenant_id,
                    CampaignEntity.status == status,
                    CampaignEntity.is_active == True
                )
            ).order_by(desc(CampaignEntity.created_at)).limit(limit).offset(offset)
            
            result = await self.session.execute(query)
            campaign_entities = result.scalars().all()
            
            return [entity.to_domain() for entity in campaign_entities]
            
        except Exception as e:
            self.logger.error(
                "Failed to find campaigns by status",
                status=status.value,
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise
    
    async def find_active_campaigns(self, tenant_id: UUID, limit: int = 100, offset: int = 0) -> List[Campaign]:
        """Find active campaigns within tenant context"""
        
        try:
            query = select(CampaignEntity).where(
                and_(
                    CampaignEntity.tenant_id == tenant_id,
                    CampaignEntity.status == CampaignStatus.ACTIVE,
                    CampaignEntity.is_active == True
                )
            ).order_by(desc(CampaignEntity.created_at)).limit(limit).offset(offset)
            
            result = await self.session.execute(query)
            campaign_entities = result.scalars().all()
            
            return [entity.to_domain() for entity in campaign_entities]
            
        except Exception as e:
            self.logger.error(
                "Failed to find active campaigns",
                tenant_id=str(tenant_id),
                error=str(e)
            )
            raise