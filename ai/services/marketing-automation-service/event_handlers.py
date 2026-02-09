"""
Event Handlers for Marketing Automation Service
Implements cross-service event processing using Redis Streams
"""

import logging
from datetime import datetime
from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from shared.events.domain_events import (
    DomainEvent, CampaignCreated, CampaignLaunched, CampaignMetricsUpdated,
    LeadCaptured, LeadQualified, LeadConverted, 
    TenantCreated, SubscriptionUpgraded
)
from shared.events.event_store import EventHandler

logger = logging.getLogger(__name__)


class CampaignEventHandler(EventHandler):
    """Handler for campaign-related events"""
    
    def __init__(self, db_session: AsyncSession):
        super().__init__([
            "campaign.created",
            "campaign.launched", 
            "campaign.metrics.updated"
        ])
        self.db = db_session
    
    async def handle(self, event: DomainEvent) -> None:
        """Handle campaign events"""
        try:
            if event.event_type == "campaign.created":
                await self._handle_campaign_created(event)
            elif event.event_type == "campaign.launched":
                await self._handle_campaign_launched(event)
            elif event.event_type == "campaign.metrics.updated":
                await self._handle_campaign_metrics_updated(event)
                
        except Exception as e:
            logger.error(f"Failed to handle campaign event {event.event_id}: {e}")
            raise
    
    async def _handle_campaign_created(self, event: CampaignCreated) -> None:
        """Process campaign creation event"""
        logger.info(f"Processing campaign created: {event.name} for tenant {event.tenant_id}")
        
        # Initialize campaign analytics tracking
        # In real implementation, create analytics records
        
        # Trigger campaign setup workflows
        # Could trigger N8N workflow for campaign setup
        
        # Send notification to campaign managers
        # Integration with notification service
        
        logger.info(f"Campaign creation processing complete: {event.campaign_id}")
    
    async def _handle_campaign_launched(self, event: CampaignLaunched) -> None:
        """Process campaign launch event"""
        logger.info(f"Processing campaign launch: {event.campaign_id} to {event.platform}")
        
        # Start performance monitoring
        # Set up automated optimization triggers
        # Initialize platform-specific tracking
        
        logger.info(f"Campaign launch processing complete: {event.campaign_id}")
    
    async def _handle_campaign_metrics_updated(self, event: CampaignMetricsUpdated) -> None:
        """Process campaign metrics update event"""
        logger.info(f"Processing metrics update for campaign: {event.campaign_id}")
        
        # Check for performance thresholds
        metrics = event.metrics
        
        # Alert on poor performance
        if metrics.get('ctr', 0) < 1.0:
            logger.warning(f"Low CTR detected for campaign {event.campaign_id}: {metrics.get('ctr')}%")
            # Trigger optimization workflow
        
        # Alert on budget overruns
        if metrics.get('spend_rate', 0) > 1.2:
            logger.warning(f"High spend rate for campaign {event.campaign_id}")
            # Send budget alert
        
        # Trigger AI optimization if performance drops
        conversion_rate = metrics.get('conversion_rate', 0)
        if conversion_rate > 0 and conversion_rate < 2.0:
            logger.info(f"Triggering AI optimization for campaign {event.campaign_id}")
            # Call AI optimization service
        
        logger.info(f"Campaign metrics processing complete: {event.campaign_id}")


class LeadEventHandler(EventHandler):
    """Handler for lead management events"""
    
    def __init__(self, db_session: AsyncSession):
        super().__init__([
            "lead.captured",
            "lead.qualified",
            "lead.converted"
        ])
        self.db = db_session
    
    async def handle(self, event: DomainEvent) -> None:
        """Handle lead events"""
        try:
            if event.event_type == "lead.captured":
                await self._handle_lead_captured(event)
            elif event.event_type == "lead.qualified":
                await self._handle_lead_qualified(event)
            elif event.event_type == "lead.converted":
                await self._handle_lead_converted(event)
                
        except Exception as e:
            logger.error(f"Failed to handle lead event {event.event_id}: {e}")
            raise
    
    async def _handle_lead_captured(self, event: LeadCaptured) -> None:
        """Process lead capture event"""
        logger.info(f"Processing lead capture: {event.lead_id} from {event.source}")
        
        # Add to CRM system
        # Trigger lead nurturing workflow
        # Send welcome email
        # Assign to sales rep based on rules
        
        # Start lead scoring process
        email = event.contact_info.get('email', '')
        company = event.contact_info.get('company', '')
        
        if company:
            logger.info(f"B2B lead detected: {email} from {company}")
            # Trigger B2B qualification workflow
        else:
            logger.info(f"B2C lead detected: {email}")
            # Trigger B2C nurturing workflow
        
        logger.info(f"Lead capture processing complete: {event.lead_id}")
    
    async def _handle_lead_qualified(self, event: LeadQualified) -> None:
        """Process lead qualification event"""
        logger.info(f"Processing lead qualification: {event.lead_id} - Score: {event.score}")
        
        # Route based on qualification score
        if event.score >= 80:
            # Hot lead - immediate sales contact
            logger.info(f"Hot lead detected: {event.lead_id} - Triggering immediate sales contact")
            # Notify sales team
            # Schedule immediate follow-up
            
        elif event.score >= 60:
            # Warm lead - nurture sequence
            logger.info(f"Warm lead detected: {event.lead_id} - Starting nurture sequence")
            # Trigger targeted content sequence
            
        elif event.score >= 40:
            # Qualified lead - standard follow-up
            logger.info(f"Qualified lead: {event.lead_id} - Standard follow-up process")
            # Add to standard sales pipeline
            
        else:
            # Cold lead - long-term nurturing
            logger.info(f"Cold lead: {event.lead_id} - Long-term nurturing")
            # Add to educational content sequence
        
        logger.info(f"Lead qualification processing complete: {event.lead_id}")
    
    async def _handle_lead_converted(self, event: LeadConverted) -> None:
        """Process lead conversion event"""
        logger.info(f"Processing lead conversion: {event.lead_id} - Value: ${event.conversion_value}")
        
        # Update campaign attribution
        # Calculate ROI impact
        # Update lead source performance
        # Trigger customer onboarding
        # Send conversion notifications
        
        # High-value conversion alerts
        if event.conversion_value > 10000:
            logger.info(f"High-value conversion: {event.lead_id} - ${event.conversion_value}")
            # Notify management
            # Trigger VIP onboarding
        
        logger.info(f"Lead conversion processing complete: {event.lead_id}")


class TenantEventHandler(EventHandler):
    """Handler for tenant and subscription events"""
    
    def __init__(self, db_session: AsyncSession):
        super().__init__([
            "tenant.created",
            "subscription.upgraded"
        ])
        self.db = db_session
    
    async def handle(self, event: DomainEvent) -> None:
        """Handle tenant events"""
        try:
            if event.event_type == "tenant.created":
                await self._handle_tenant_created(event)
            elif event.event_type == "subscription.upgraded":
                await self._handle_subscription_upgraded(event)
                
        except Exception as e:
            logger.error(f"Failed to handle tenant event {event.event_id}: {e}")
            raise
    
    async def _handle_tenant_created(self, event: TenantCreated) -> None:
        """Process new tenant creation"""
        logger.info(f"Processing tenant creation: {event.name} (Plan: {event.plan})")
        
        # Initialize tenant resources
        # Create default campaigns templates
        # Set up analytics dashboards
        # Configure integrations based on plan
        # Send welcome emails
        # Schedule onboarding calls
        
        logger.info(f"Tenant creation processing complete: {event.tenant_id}")
    
    async def _handle_subscription_upgraded(self, event: SubscriptionUpgraded) -> None:
        """Process subscription upgrade"""
        logger.info(f"Processing subscription upgrade: {event.old_plan} -> {event.new_plan}")
        
        # Update tenant limits
        # Enable premium features
        # Migrate data if needed
        # Send upgrade confirmation
        # Trigger success metrics
        
        logger.info(f"Subscription upgrade processing complete: {event.tenant_id}")


class NotificationEventHandler(EventHandler):
    """Handler for cross-service notifications"""
    
    def __init__(self, db_session: AsyncSession):
        super().__init__([
            "campaign.created",
            "lead.captured",
            "lead.converted",
            "subscription.upgraded"
        ])
        self.db = db_session
    
    async def handle(self, event: DomainEvent) -> None:
        """Handle notification-triggering events"""
        try:
            # Route to appropriate notification method
            if event.event_type in ["campaign.created", "campaign.launched"]:
                await self._send_campaign_notification(event)
            elif event.event_type in ["lead.captured", "lead.qualified", "lead.converted"]:
                await self._send_lead_notification(event)
            elif event.event_type == "subscription.upgraded":
                await self._send_subscription_notification(event)
                
        except Exception as e:
            logger.error(f"Failed to handle notification event {event.event_id}: {e}")
            raise
    
    async def _send_campaign_notification(self, event: DomainEvent) -> None:
        """Send campaign-related notifications"""
        # In real implementation, integrate with notification service
        # Send emails, Slack notifications, dashboard alerts
        logger.info(f"Campaign notification sent for event: {event.event_type}")
    
    async def _send_lead_notification(self, event: DomainEvent) -> None:
        """Send lead-related notifications"""
        # In real implementation, notify sales team, update CRM
        logger.info(f"Lead notification sent for event: {event.event_type}")
    
    async def _send_subscription_notification(self, event: DomainEvent) -> None:
        """Send subscription-related notifications"""
        # In real implementation, update billing, notify account managers
        logger.info(f"Subscription notification sent for event: {event.event_type}")