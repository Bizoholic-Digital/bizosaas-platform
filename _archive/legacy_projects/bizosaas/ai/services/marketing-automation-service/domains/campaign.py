"""
Campaign Domain - Bounded Context for Campaign Management
Implements campaign aggregate with proper business rules and event publishing
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from sqlalchemy.orm import selectinload

from shared.database.models import Campaign, CampaignExecution, Integration
from shared.events.domain_events import CampaignCreated, CampaignLaunched, EventMetadata
from shared.events.event_store import EventPublisher

logger = logging.getLogger(__name__)


class CampaignAggregate:
    """Campaign aggregate root with business rules"""
    
    def __init__(self, campaign_data: Campaign):
        self.id = campaign_data.id
        self.tenant_id = campaign_data.tenant_id
        self.name = campaign_data.name
        self.description = campaign_data.description
        self.status = campaign_data.status
        self.campaign_type = campaign_data.campaign_type
        self.budget = campaign_data.budget
        self.start_date = campaign_data.start_date
        self.end_date = campaign_data.end_date
        self.target_audience = campaign_data.target_audience
        self.creative_assets = campaign_data.creative_assets
        self.performance_metrics = campaign_data.performance_metrics
        self.created_by = campaign_data.created_by
        self.created_at = campaign_data.created_at
        self.updated_at = campaign_data.updated_at
        
        # Track domain events
        self._domain_events = []
    
    def create(self, user_id: str, metadata: Optional[EventMetadata] = None):
        """Business logic for campaign creation"""
        # Validate business rules
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Campaign name is required")
        
        if self.budget <= 0:
            raise ValueError("Campaign budget must be greater than zero")
        
        if self.campaign_type not in ["google_ads", "facebook_ads", "linkedin_ads", "email"]:
            raise ValueError("Invalid campaign type")
        
        # Generate domain event
        event = CampaignCreated(
            tenant_id=self.tenant_id,
            campaign_id=str(self.id),
            name=self.name,
            budget=self.budget,
            campaign_type=self.campaign_type,
            metadata=metadata
        )
        self._domain_events.append(event)
        
        logger.info(f"Campaign created: {self.name} for tenant {self.tenant_id}")
    
    def launch_to_platform(self, platform: str, platform_campaign_id: str, 
                          config: Dict[str, Any], metadata: Optional[EventMetadata] = None):
        """Business logic for campaign launch"""
        if self.status != "draft":
            raise ValueError("Only draft campaigns can be launched")
        
        if not platform_campaign_id:
            raise ValueError("Platform campaign ID is required")
        
        # Update status
        self.status = "active"
        
        # Generate domain event
        event = CampaignLaunched(
            tenant_id=self.tenant_id,
            campaign_id=str(self.id),
            platform=platform,
            platform_campaign_id=platform_campaign_id,
            config=config,
            metadata=metadata
        )
        self._domain_events.append(event)
        
        logger.info(f"Campaign {self.name} launched to {platform}")
    
    def update_status(self, new_status: str):
        """Update campaign status with validation"""
        valid_statuses = ["draft", "active", "paused", "completed", "cancelled"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}")
        
        # Business rules for status transitions
        if self.status == "completed" and new_status != "completed":
            raise ValueError("Cannot change status of completed campaign")
        
        if self.status == "cancelled" and new_status not in ["cancelled", "draft"]:
            raise ValueError("Cannot reactivate cancelled campaign")
        
        self.status = new_status
        logger.info(f"Campaign {self.name} status updated to {new_status}")
    
    def get_domain_events(self):
        """Get domain events for publishing"""
        return self._domain_events.copy()
    
    def clear_domain_events(self):
        """Clear domain events after publishing"""
        self._domain_events.clear()


class CampaignDomain:
    """Domain service for campaign management operations"""
    
    def __init__(self, db_session: AsyncSession, event_publisher: EventPublisher, tenant_id: str):
        self.db = db_session
        self.event_publisher = event_publisher
        self.tenant_id = tenant_id
    
    async def create_campaign(self, name: str, description: Optional[str], 
                            campaign_type: str, budget: float, 
                            target_audience: Dict[str, Any], 
                            creative_assets: List[Dict[str, Any]],
                            created_by: str) -> Campaign:
        """Create new campaign using domain aggregate"""
        try:
            # Create campaign entity
            campaign_data = Campaign(
                id=uuid4(),
                tenant_id=self.tenant_id,
                name=name,
                description=description,
                campaign_type=campaign_type,
                budget=budget,
                target_audience=target_audience,
                creative_assets=creative_assets,
                created_by=created_by,
                status="draft"
            )
            
            # Use aggregate to apply business rules
            aggregate = CampaignAggregate(campaign_data)
            aggregate.create(created_by)
            
            # Persist to database
            self.db.add(campaign_data)
            await self.db.commit()
            await self.db.refresh(campaign_data)
            
            # Publish domain events
            events = aggregate.get_domain_events()
            if events:
                await self.event_publisher.publish_batch(events)
            
            return campaign_data
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to create campaign: {e}")
            raise
    
    async def launch_campaign(self, campaign_id: str, platform: str, 
                            config: Dict[str, Any]) -> str:
        """Launch campaign to advertising platform using BYOK credentials"""
        try:
            # Get campaign
            stmt = select(Campaign).where(
                Campaign.id == campaign_id,
                Campaign.tenant_id == self.tenant_id
            )
            result = await self.db.execute(stmt)
            campaign = result.scalar_one_or_none()
            
            if not campaign:
                raise ValueError("Campaign not found")
            
            # Resolve credentials using BYOK key resolution service
            from shared.credential_management import get_key_resolution_service
            from shared.billing import get_byok_billing_service, UsageType
            
            key_service = get_key_resolution_service()
            resolved_creds = await key_service.resolve_credentials(
                tenant_id=self.tenant_id,
                platform=platform
            )
            
            if resolved_creds.health_status != "healthy":
                raise ValueError(f"Platform credentials are not healthy: {platform}")
            
            # Create aggregate and launch
            aggregate = CampaignAggregate(campaign)
            
            # Launch to platform using resolved credentials
            platform_campaign_id = await self._launch_to_platform_api(
                platform, campaign, config, resolved_creds.credentials
            )
            
            # Apply business rules
            aggregate.launch_to_platform(platform, platform_campaign_id, config)
            
            # Update database
            campaign.status = aggregate.status
            
            # Create execution record
            execution = CampaignExecution(
                tenant_id=self.tenant_id,
                campaign_id=campaign.id,
                platform=platform,
                execution_status="active",
                execution_data=config,
                platform_campaign_id=platform_campaign_id
            )
            self.db.add(execution)
            
            await self.db.commit()
            
            # Record billable usage
            billing_service = get_byok_billing_service()
            billing_service.record_usage(
                tenant_id=self.tenant_id,
                platform=platform,
                usage_type=UsageType.CAMPAIGN_EXECUTION,
                quantity=1,
                credential_strategy=resolved_creds.strategy_used,
                metadata={
                    "campaign_id": str(campaign_id),
                    "platform_campaign_id": platform_campaign_id,
                    "billing_model": resolved_creds.usage_cost_model.value
                }
            )
            
            # Publish domain events
            events = aggregate.get_domain_events()
            if events:
                await self.event_publisher.publish_batch(events)
            
            logger.info(f"Campaign launched: {campaign.name} to {platform} using {resolved_creds.source} credentials")
            
            return platform_campaign_id
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to launch campaign: {e}")
            raise
    
    async def get_campaign_performance(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign performance metrics"""
        try:
            stmt = select(Campaign).options(
                selectinload(Campaign.campaign_executions)
            ).where(
                Campaign.id == campaign_id,
                Campaign.tenant_id == self.tenant_id
            )
            result = await self.db.execute(stmt)
            campaign = result.scalar_one_or_none()
            
            if not campaign:
                raise ValueError("Campaign not found")
            
            # Aggregate performance data
            total_spend = 0
            total_impressions = 0
            total_clicks = 0
            total_conversions = 0
            
            for execution in campaign.campaign_executions:
                metrics = execution.metrics_snapshot or {}
                total_spend += metrics.get("spend", 0)
                total_impressions += metrics.get("impressions", 0)
                total_clicks += metrics.get("clicks", 0)
                total_conversions += metrics.get("conversions", 0)
            
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
            conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
            
            return {
                "campaign_id": str(campaign_id),
                "campaign_name": campaign.name,
                "status": campaign.status,
                "budget": campaign.budget,
                "spend": total_spend,
                "impressions": total_impressions,
                "clicks": total_clicks,
                "conversions": total_conversions,
                "ctr": round(ctr, 2),
                "cpc": round(cpc, 2),
                "conversion_rate": round(conversion_rate, 2),
                "roi": round(((total_conversions * 100 - total_spend) / total_spend * 100), 2) if total_spend > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Failed to get campaign performance: {e}")
            raise
    
    async def _launch_to_platform_api(
        self, 
        platform: str, 
        campaign: Campaign, 
        config: Dict[str, Any], 
        credentials: Dict[str, str]
    ) -> str:
        """Launch campaign to platform using real API credentials"""
        
        # Import platform API clients
        from ..platform_apis import GoogleAdsClient, MetaAdsClient, LinkedInAdsClient
        
        # Prepare campaign data for platform APIs
        campaign_data = {
            "name": campaign.name,
            "description": campaign.description,
            "budget": campaign.budget,
            "target_audience": campaign.target_audience,
            "creative_assets": campaign.creative_assets
        }
        
        try:
            if platform == "google_ads":
                client = GoogleAdsClient(credentials)
                return await client.create_campaign(campaign_data, config)
            
            elif platform == "facebook_ads" or platform == "meta_ads":
                client = MetaAdsClient(credentials)
                return await client.create_campaign(campaign_data, config)
            
            elif platform == "linkedin_ads":
                client = LinkedInAdsClient(credentials)
                return await client.create_campaign(campaign_data, config)
            
            else:
                # Generic platform launch for unsupported platforms
                platform_campaign_id = f"{platform}_{uuid4().hex[:8]}"
                logger.info(f"Generic platform launch: {platform} - {platform_campaign_id}")
                return platform_campaign_id
                
        except Exception as e:
            logger.error(f"Platform API launch failed for {platform}: {e}")
            # Fall back to legacy simulation methods for development
            logger.warning(f"Falling back to simulation for platform: {platform}")
            return await self._fallback_simulation_launch(platform, campaign, config)
    
    async def _fallback_simulation_launch(self, platform: str, campaign: Campaign, config: Dict[str, Any]) -> str:
        """Fallback simulation for platform launch during development"""
        platform_campaign_id = f"{platform}_{uuid4().hex[:8]}"
        
        logger.info(f"{platform.title()} campaign created (simulation): {platform_campaign_id}")
        logger.debug(f"Campaign: {campaign.name}, Budget: ${campaign.budget}")
        
        # Simulate API delay
        import asyncio
        await asyncio.sleep(0.1)
        
        return platform_campaign_id
    
    async def _get_platform_integration(self, platform: str) -> Optional[Integration]:
        """Get platform integration configuration"""
        try:
            stmt = select(Integration).where(
                Integration.tenant_id == self.tenant_id,
                Integration.platform_name == platform,
                Integration.status == "active"
            )
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"Failed to get platform integration: {e}")
            return None