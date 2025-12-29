from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from app.models.campaign import Campaign, CampaignChannel, CampaignStatus
from app.connectors.registry import ConnectorRegistry
from app.store import active_connectors
from app.connectors.base import ConnectorType
from app.ports.marketing_port import MarketingPort, Campaign as PortCampaign

class CampaignService:
    def __init__(self, db: Session):
        self.db = db

    def create_campaign(self, tenant_id: UUID, name: str, goal: Optional[str] = None, user_id: Optional[UUID] = None) -> Campaign:
        campaign = Campaign(
            tenant_id=tenant_id,
            name=name,
            goal=goal,
            created_by=user_id,
            status=CampaignStatus.DRAFT
        )
        self.db.add(campaign)
        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def list_campaigns(self, tenant_id: UUID) -> List[Campaign]:
        return self.db.query(Campaign).filter(Campaign.tenant_id == tenant_id).order_by(Campaign.created_at.desc()).all()

    def get_campaign(self, campaign_id: UUID, tenant_id: UUID) -> Optional[Campaign]:
        return self.db.query(Campaign).filter(
            Campaign.id == campaign_id, 
            Campaign.tenant_id == tenant_id
        ).first()

    def add_channel(self, campaign_id: UUID, channel_type: str, connector_id: str, config: Dict[str, Any]) -> CampaignChannel:
        channel = CampaignChannel(
            campaign_id=campaign_id,
            channel_type=channel_type,
            connector_id=connector_id,
            config=config,
            status="pending"
        )
        self.db.add(channel)
        self.db.commit()
        self.db.refresh(channel)
        return channel

    async def publish_campaign(self, campaign_id: UUID, tenant_id: UUID):
        campaign = self.get_campaign(campaign_id, tenant_id)
        if not campaign:
            raise ValueError("Campaign not found")

        # In a real system, this would be a background task (Temporal or Celery)
        # For now, we do it inline for simplicity
        
        results = []
        
        for channel in campaign.channels:
            if channel.channel_type == "email":
                try:
                    # 1. Resolve Connector
                    connector = await self._get_connector(str(tenant_id), channel.connector_id, ConnectorType.MARKETING)
                    
                    if not connector:
                         channel.status = "error"
                         channel.stats = {"error": "Connector not found"}
                         results.append({"channel_id": str(channel.id), "status": "error", "error": "Connector not found"})
                         continue

                    # 2. Create/Send in External System
                    # Create Port Campaign model
                    port_campaign = PortCampaign(
                        name=campaign.name,
                        subject=channel.config.get("subject", campaign.name),
                        list_ids=[channel.config.get("list_id")] if channel.config.get("list_id") else [],
                        status="draft"
                    )
                    
                    external_campaign = await connector.create_campaign(port_campaign)
                    
                    channel.remote_id = external_campaign.id
                    channel.status = "synced"
                    
                    # If we want to send immediately
                    if channel.config.get("send_immediately", False):
                        await connector.send_campaign(external_campaign.id)
                        channel.status = "sent"

                    results.append({"channel_id": str(channel.id), "status": channel.status, "remote_id": channel.remote_id})
                    
                except Exception as e:
                    channel.status = "error"
                    channel.stats = {"error": str(e)}
                    results.append({"channel_id": str(channel.id), "status": "error", "error": str(e)})

        campaign.status = CampaignStatus.ACTIVE
        self.db.commit()
        return results

    async def _get_connector(self, tenant_id: str, connector_id: str, type: ConnectorType):
        # Helper to get initialized connector
        # This assumes connector_id matches the config.id (e.g. "mailchimp")
        
        # Valid configs for this type
        configs = [c for c in ConnectorRegistry.get_all_configs() if c.type == type]
        target_config = next((c for c in configs if c.id == connector_id), None)
        
        if not target_config:
            return None

        key = f"{tenant_id}:{target_config.id}"
        if key in active_connectors:
            data = active_connectors[key]
            return ConnectorRegistry.create_connector(target_config.id, tenant_id, data["credentials"])
        return None
