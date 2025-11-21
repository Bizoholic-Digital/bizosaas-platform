"""
Lead Management Domain - Bounded Context for CRM and Lead Processing
Implements lead aggregate with qualification, scoring, and conversion logic
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, and_
from sqlalchemy.orm import selectinload

from shared.database.models import BaseModel, TenantAwareModel
from shared.events.domain_events import LeadCaptured, LeadQualified, LeadConverted, EventMetadata
from shared.events.event_store import EventPublisher

logger = logging.getLogger(__name__)


# Lead Models (would be in shared/database/models.py in full implementation)
class Lead(TenantAwareModel):
    """Lead entity for CRM system"""
    __tablename__ = "leads"
    __table_args__ = {'schema': 'campaign_management'}
    
    source = None  # String column - traffic source
    contact_info = None  # JSONB column - contact details
    campaign_id = None  # UUID column - optional campaign reference
    score = None  # Float column - lead qualification score
    status = None  # String column - lead status
    qualification_notes = None  # Text column - qualification details
    assigned_to = None  # UUID column - assigned user
    last_contact = None  # DateTime column - last contact attempt
    conversion_data = None  # JSONB column - conversion tracking


class LeadActivity(TenantAwareModel):
    """Lead activity tracking"""
    __tablename__ = "lead_activities"
    __table_args__ = {'schema': 'campaign_management'}
    
    lead_id = None  # UUID foreign key
    activity_type = None  # String - email_open, website_visit, form_fill, etc.
    activity_data = None  # JSONB - activity details
    occurred_at = None  # DateTime - when activity occurred


class LeadAggregate:
    """Lead aggregate root with business rules for CRM operations"""
    
    def __init__(self, lead_data: Lead):
        self.id = lead_data.id if hasattr(lead_data, 'id') else uuid4()
        self.tenant_id = lead_data.tenant_id if hasattr(lead_data, 'tenant_id') else None
        self.source = lead_data.source if hasattr(lead_data, 'source') else None
        self.contact_info = lead_data.contact_info if hasattr(lead_data, 'contact_info') else {}
        self.campaign_id = lead_data.campaign_id if hasattr(lead_data, 'campaign_id') else None
        self.score = lead_data.score if hasattr(lead_data, 'score') else 0.0
        self.status = lead_data.status if hasattr(lead_data, 'status') else "new"
        self.qualification_notes = lead_data.qualification_notes if hasattr(lead_data, 'qualification_notes') else ""
        self.assigned_to = lead_data.assigned_to if hasattr(lead_data, 'assigned_to') else None
        
        # Track domain events
        self._domain_events = []
    
    def capture(self, metadata: Optional[EventMetadata] = None):
        """Business logic for lead capture"""
        # Validate contact info
        if not self.contact_info:
            raise ValueError("Contact information is required")
        
        email = self.contact_info.get('email')
        if not email or '@' not in email:
            raise ValueError("Valid email address is required")
        
        # Set initial status and score
        self.status = "new"
        self.score = self._calculate_initial_score()
        
        # Generate domain event
        event = LeadCaptured(
            tenant_id=self.tenant_id,
            lead_id=str(self.id),
            source=self.source,
            contact_info=self.contact_info,
            metadata=metadata
        )
        self._domain_events.append(event)
        
        logger.info(f"Lead captured: {email} from {self.source}")
    
    def qualify(self, score: float, qualification_reason: str, qualified_by: str,
               metadata: Optional[EventMetadata] = None):
        """Business logic for lead qualification"""
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100")
        
        if not qualification_reason:
            raise ValueError("Qualification reason is required")
        
        old_score = self.score
        self.score = score
        self.qualification_notes = qualification_reason
        
        # Update status based on score
        if score >= 80:
            self.status = "hot"
        elif score >= 60:
            self.status = "warm"
        elif score >= 40:
            self.status = "qualified"
        else:
            self.status = "cold"
        
        # Generate domain event
        event = LeadQualified(
            tenant_id=self.tenant_id,
            lead_id=str(self.id),
            score=score,
            qualification_reason=qualification_reason,
            qualified_by=qualified_by,
            metadata=metadata
        )
        self._domain_events.append(event)
        
        logger.info(f"Lead qualified: {self.contact_info.get('email')} - Score: {old_score} → {score}")
    
    def convert(self, conversion_value: float, conversion_source: str, customer_id: str,
               metadata: Optional[EventMetadata] = None):
        """Business logic for lead conversion"""
        if self.status in ["converted", "closed_lost"]:
            raise ValueError("Cannot convert lead that is already converted or closed")
        
        if conversion_value <= 0:
            raise ValueError("Conversion value must be greater than zero")
        
        # Update status and conversion data
        self.status = "converted"
        
        # Generate domain event
        event = LeadConverted(
            tenant_id=self.tenant_id,
            lead_id=str(self.id),
            conversion_value=conversion_value,
            conversion_source=conversion_source,
            customer_id=customer_id,
            metadata=metadata
        )
        self._domain_events.append(event)
        
        logger.info(f"Lead converted: {self.contact_info.get('email')} - Value: ${conversion_value}")
    
    def _calculate_initial_score(self) -> float:
        """Calculate initial lead score based on available information"""
        score = 30.0  # Base score
        
        # Score based on contact info completeness
        if self.contact_info.get('phone'):
            score += 10
        if self.contact_info.get('company'):
            score += 15
        if self.contact_info.get('job_title'):
            score += 10
        
        # Score based on source quality
        high_quality_sources = ['google_ads', 'linkedin_ads', 'referral']
        medium_quality_sources = ['organic_search', 'social_media']
        
        if self.source in high_quality_sources:
            score += 20
        elif self.source in medium_quality_sources:
            score += 10
        else:
            score += 5
        
        return min(score, 100.0)
    
    def get_domain_events(self):
        """Get domain events for publishing"""
        return self._domain_events.copy()
    
    def clear_domain_events(self):
        """Clear domain events after publishing"""
        self._domain_events.clear()


class LeadDomain:
    """Domain service for lead management operations"""
    
    def __init__(self, db_session: AsyncSession, event_publisher: EventPublisher, tenant_id: str):
        self.db = db_session
        self.event_publisher = event_publisher
        self.tenant_id = tenant_id
    
    async def capture_lead(self, source: str, contact_info: Dict[str, Any], 
                          campaign_id: Optional[str] = None) -> Dict[str, Any]:
        """Capture new lead using domain aggregate"""
        try:
            # Create lead mock object (in real implementation, use actual Lead model)
            lead_data = type('Lead', (), {
                'id': uuid4(),
                'tenant_id': self.tenant_id,
                'source': source,
                'contact_info': contact_info,
                'campaign_id': campaign_id,
                'score': 0.0,
                'status': 'new'
            })()
            
            # Use aggregate to apply business rules
            aggregate = LeadAggregate(lead_data)
            aggregate.capture()
            
            # In real implementation, persist to database
            # self.db.add(lead_data)
            # await self.db.commit()
            
            # Publish domain events
            events = aggregate.get_domain_events()
            if events:
                await self.event_publisher.publish_batch(events)
            
            # Return lead info
            return {
                'id': str(aggregate.id),
                'source': aggregate.source,
                'contact_info': aggregate.contact_info,
                'score': aggregate.score,
                'status': aggregate.status,
                'created_at': datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Failed to capture lead: {e}")
            raise
    
    async def qualify_lead(self, lead_id: str, score: float, 
                          qualification_reason: str, qualified_by: str):
        """Qualify lead with scoring"""
        try:
            # In real implementation, fetch from database
            # For now, create mock lead data
            lead_data = type('Lead', (), {
                'id': lead_id,
                'tenant_id': self.tenant_id,
                'score': 30.0,
                'status': 'new',
                'contact_info': {'email': 'test@example.com'}
            })()
            
            # Use aggregate to apply business rules
            aggregate = LeadAggregate(lead_data)
            aggregate.qualify(score, qualification_reason, qualified_by)
            
            # In real implementation, update database
            # lead.score = aggregate.score
            # lead.status = aggregate.status
            # await self.db.commit()
            
            # Publish domain events
            events = aggregate.get_domain_events()
            if events:
                await self.event_publisher.publish_batch(events)
            
            logger.info(f"Lead {lead_id} qualified with score {score}")
            
        except Exception as e:
            logger.error(f"Failed to qualify lead: {e}")
            raise
    
    async def convert_lead(self, lead_id: str, conversion_value: float, 
                          conversion_source: str, customer_id: str):
        """Convert lead to customer"""
        try:
            # In real implementation, fetch from database
            lead_data = type('Lead', (), {
                'id': lead_id,
                'tenant_id': self.tenant_id,
                'status': 'qualified',
                'contact_info': {'email': 'test@example.com'}
            })()
            
            # Use aggregate to apply business rules
            aggregate = LeadAggregate(lead_data)
            aggregate.convert(conversion_value, conversion_source, customer_id)
            
            # In real implementation, update database
            # lead.status = aggregate.status
            # await self.db.commit()
            
            # Publish domain events
            events = aggregate.get_domain_events()
            if events:
                await self.event_publisher.publish_batch(events)
            
            logger.info(f"Lead {lead_id} converted with value ${conversion_value}")
            
        except Exception as e:
            logger.error(f"Failed to convert lead: {e}")
            raise
    
    async def get_lead_pipeline(self) -> List[Dict[str, Any]]:
        """Get lead pipeline metrics"""
        try:
            # In real implementation, query database for actual metrics
            # For now, return mock data
            pipeline_data = [
                {"stage": "new", "count": 45, "value": 22500},
                {"stage": "qualified", "count": 32, "value": 48000},
                {"stage": "warm", "count": 18, "value": 54000},
                {"stage": "hot", "count": 12, "value": 72000},
                {"stage": "converted", "count": 8, "value": 120000}
            ]
            
            return pipeline_data
            
        except Exception as e:
            logger.error(f"Failed to get lead pipeline: {e}")
            raise
    
    async def get_lead_sources(self) -> Dict[str, Any]:
        """Get lead source breakdown"""
        try:
            # In real implementation, query database
            sources_data = {
                "google_ads": {"count": 45, "conversion_rate": 12.5, "avg_score": 68},
                "facebook_ads": {"count": 38, "conversion_rate": 8.7, "avg_score": 55},
                "linkedin_ads": {"count": 22, "conversion_rate": 18.2, "avg_score": 75},
                "organic_search": {"count": 28, "conversion_rate": 14.3, "avg_score": 62},
                "referral": {"count": 15, "conversion_rate": 26.7, "avg_score": 82}
            }
            
            return sources_data
            
        except Exception as e:
            logger.error(f"Failed to get lead sources: {e}")
            raise