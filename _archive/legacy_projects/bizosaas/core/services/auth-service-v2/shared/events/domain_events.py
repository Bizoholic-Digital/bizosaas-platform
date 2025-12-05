"""
Domain Events Framework
Implements event-driven architecture patterns for BizOSaas platform
Following DDD principles with proper event sourcing support
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
import uuid
import json
from enum import Enum


class EventVersion(Enum):
    """Event version for schema evolution"""
    V1 = 1
    V2 = 2


@dataclass
class EventMetadata:
    """Event metadata for tracing and correlation"""
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
    user_id: Optional[str] = None
    trace_id: Optional[str] = None


class DomainEvent(ABC):
    """Base class for all domain events following DDD patterns"""
    
    def __init__(self, tenant_id: str, metadata: Optional[EventMetadata] = None):
        self.event_id = str(uuid.uuid4())
        self.tenant_id = tenant_id
        self.occurred_at = datetime.utcnow()
        self.event_version = EventVersion.V1.value
        self.metadata = metadata or EventMetadata()
    
    @property
    @abstractmethod
    def event_type(self) -> str:
        """Event type identifier for routing and handlers"""
        pass
    
    @property
    @abstractmethod
    def aggregate_id(self) -> str:
        """ID of the aggregate that generated this event"""
        pass
    
    @property
    @abstractmethod
    def aggregate_type(self) -> str:
        """Type of aggregate that generated this event"""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serialize event to dictionary for storage"""
        pass
    
    def to_json(self) -> str:
        """Serialize event to JSON string"""
        return json.dumps(self.to_dict(), default=str)
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DomainEvent':
        """Deserialize event from dictionary"""
        pass


# ====================================================================
# CAMPAIGN DOMAIN EVENTS
# ====================================================================

class CampaignCreated(DomainEvent):
    """Event raised when a new campaign is created"""
    
    def __init__(self, tenant_id: str, campaign_id: str, name: str, 
                 budget: float, campaign_type: str, metadata: Optional[EventMetadata] = None):
        super().__init__(tenant_id, metadata)
        self.campaign_id = campaign_id
        self.name = name
        self.budget = budget
        self.campaign_type = campaign_type
    
    @property
    def event_type(self) -> str:
        return "campaign.created"
    
    @property
    def aggregate_id(self) -> str:
        return self.campaign_id
    
    @property
    def aggregate_type(self) -> str:
        return "Campaign"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "occurred_at": self.occurred_at.isoformat(),
            "tenant_id": self.tenant_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "campaign_id": self.campaign_id,
            "name": self.name,
            "budget": self.budget,
            "campaign_type": self.campaign_type,
            "metadata": asdict(self.metadata) if self.metadata else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CampaignCreated':
        metadata = EventMetadata(**data.get("metadata", {})) if data.get("metadata") else None
        return cls(
            tenant_id=data["tenant_id"],
            campaign_id=data["campaign_id"],
            name=data["name"],
            budget=data["budget"],
            campaign_type=data["campaign_type"],
            metadata=metadata
        )


class CampaignLaunched(DomainEvent):
    """Event raised when a campaign is launched to a platform"""
    
    def __init__(self, tenant_id: str, campaign_id: str, platform: str, 
                 platform_campaign_id: str, config: Dict[str, Any], 
                 metadata: Optional[EventMetadata] = None):
        super().__init__(tenant_id, metadata)
        self.campaign_id = campaign_id
        self.platform = platform
        self.platform_campaign_id = platform_campaign_id
        self.config = config
    
    @property
    def event_type(self) -> str:
        return "campaign.launched"
    
    @property
    def aggregate_id(self) -> str:
        return self.campaign_id
    
    @property
    def aggregate_type(self) -> str:
        return "Campaign"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "occurred_at": self.occurred_at.isoformat(),
            "tenant_id": self.tenant_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "campaign_id": self.campaign_id,
            "platform": self.platform,
            "platform_campaign_id": self.platform_campaign_id,
            "config": self.config,
            "metadata": asdict(self.metadata) if self.metadata else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CampaignLaunched':
        metadata = EventMetadata(**data.get("metadata", {})) if data.get("metadata") else None
        return cls(
            tenant_id=data["tenant_id"],
            campaign_id=data["campaign_id"],
            platform=data["platform"],
            platform_campaign_id=data["platform_campaign_id"],
            config=data["config"],
            metadata=metadata
        )


class CampaignMetricsUpdated(DomainEvent):
    """Event raised when campaign performance metrics are updated"""
    
    def __init__(self, tenant_id: str, campaign_id: str, platform: str,
                 metrics: Dict[str, Union[int, float]], metadata: Optional[EventMetadata] = None):
        super().__init__(tenant_id, metadata)
        self.campaign_id = campaign_id
        self.platform = platform
        self.metrics = metrics
    
    @property
    def event_type(self) -> str:
        return "campaign.metrics.updated"
    
    @property
    def aggregate_id(self) -> str:
        return self.campaign_id
    
    @property
    def aggregate_type(self) -> str:
        return "Campaign"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "occurred_at": self.occurred_at.isoformat(),
            "tenant_id": self.tenant_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "campaign_id": self.campaign_id,
            "platform": self.platform,
            "metrics": self.metrics,
            "metadata": asdict(self.metadata) if self.metadata else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CampaignMetricsUpdated':
        metadata = EventMetadata(**data.get("metadata", {})) if data.get("metadata") else None
        return cls(
            tenant_id=data["tenant_id"],
            campaign_id=data["campaign_id"],
            platform=data["platform"],
            metrics=data["metrics"],
            metadata=metadata
        )


# ====================================================================
# LEAD DOMAIN EVENTS
# ====================================================================

class LeadCaptured(DomainEvent):
    """Event raised when a new lead is captured"""
    
    def __init__(self, tenant_id: str, lead_id: str, source: str, 
                 contact_info: Dict[str, str], metadata: Optional[EventMetadata] = None):
        super().__init__(tenant_id, metadata)
        self.lead_id = lead_id
        self.source = source
        self.contact_info = contact_info
    
    @property
    def event_type(self) -> str:
        return "lead.captured"
    
    @property
    def aggregate_id(self) -> str:
        return self.lead_id
    
    @property
    def aggregate_type(self) -> str:
        return "Lead"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "occurred_at": self.occurred_at.isoformat(),
            "tenant_id": self.tenant_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "lead_id": self.lead_id,
            "source": self.source,
            "contact_info": self.contact_info,
            "metadata": asdict(self.metadata) if self.metadata else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LeadCaptured':
        metadata = EventMetadata(**data.get("metadata", {})) if data.get("metadata") else None
        return cls(
            tenant_id=data["tenant_id"],
            lead_id=data["lead_id"],
            source=data["source"],
            contact_info=data["contact_info"],
            metadata=metadata
        )


class LeadQualified(DomainEvent):
    """Event raised when a lead is qualified by AI or manual process"""
    
    def __init__(self, tenant_id: str, lead_id: str, score: float, 
                 qualification_reason: str, qualified_by: str,
                 metadata: Optional[EventMetadata] = None):
        super().__init__(tenant_id, metadata)
        self.lead_id = lead_id
        self.score = score
        self.qualification_reason = qualification_reason
        self.qualified_by = qualified_by  # 'ai' or user_id
    
    @property
    def event_type(self) -> str:
        return "lead.qualified"
    
    @property
    def aggregate_id(self) -> str:
        return self.lead_id
    
    @property
    def aggregate_type(self) -> str:
        return "Lead"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "occurred_at": self.occurred_at.isoformat(),
            "tenant_id": self.tenant_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "lead_id": self.lead_id,
            "score": self.score,
            "qualification_reason": self.qualification_reason,
            "qualified_by": self.qualified_by,
            "metadata": asdict(self.metadata) if self.metadata else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LeadQualified':
        metadata = EventMetadata(**data.get("metadata", {})) if data.get("metadata") else None
        return cls(
            tenant_id=data["tenant_id"],
            lead_id=data["lead_id"],
            score=data["score"],
            qualification_reason=data["qualification_reason"],
            qualified_by=data["qualified_by"],
            metadata=metadata
        )


class LeadConverted(DomainEvent):
    """Event raised when a lead converts to customer"""
    
    def __init__(self, tenant_id: str, lead_id: str, conversion_value: float,
                 conversion_source: str, customer_id: str, 
                 metadata: Optional[EventMetadata] = None):
        super().__init__(tenant_id, metadata)
        self.lead_id = lead_id
        self.conversion_value = conversion_value
        self.conversion_source = conversion_source
        self.customer_id = customer_id
    
    @property
    def event_type(self) -> str:
        return "lead.converted"
    
    @property
    def aggregate_id(self) -> str:
        return self.lead_id
    
    @property
    def aggregate_type(self) -> str:
        return "Lead"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "occurred_at": self.occurred_at.isoformat(),
            "tenant_id": self.tenant_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "lead_id": self.lead_id,
            "conversion_value": self.conversion_value,
            "conversion_source": self.conversion_source,
            "customer_id": self.customer_id,
            "metadata": asdict(self.metadata) if self.metadata else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LeadConverted':
        metadata = EventMetadata(**data.get("metadata", {})) if data.get("metadata") else None
        return cls(
            tenant_id=data["tenant_id"],
            lead_id=data["lead_id"],
            conversion_value=data["conversion_value"],
            conversion_source=data["conversion_source"],
            customer_id=data["customer_id"],
            metadata=metadata
        )


# ====================================================================
# TENANT/SUBSCRIPTION DOMAIN EVENTS
# ====================================================================

class TenantCreated(DomainEvent):
    """Event raised when a new tenant is created"""
    
    def __init__(self, tenant_id: str, name: str, plan: str, owner_user_id: str,
                 metadata: Optional[EventMetadata] = None):
        super().__init__(tenant_id, metadata)
        self.name = name
        self.plan = plan
        self.owner_user_id = owner_user_id
    
    @property
    def event_type(self) -> str:
        return "tenant.created"
    
    @property
    def aggregate_id(self) -> str:
        return self.tenant_id
    
    @property
    def aggregate_type(self) -> str:
        return "Tenant"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "occurred_at": self.occurred_at.isoformat(),
            "tenant_id": self.tenant_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "name": self.name,
            "plan": self.plan,
            "owner_user_id": self.owner_user_id,
            "metadata": asdict(self.metadata) if self.metadata else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TenantCreated':
        metadata = EventMetadata(**data.get("metadata", {})) if data.get("metadata") else None
        return cls(
            tenant_id=data["tenant_id"],
            name=data["name"],
            plan=data["plan"],
            owner_user_id=data["owner_user_id"],
            metadata=metadata
        )


class SubscriptionUpgraded(DomainEvent):
    """Event raised when subscription plan is upgraded"""
    
    def __init__(self, tenant_id: str, old_plan: str, new_plan: str, 
                 effective_date: datetime, metadata: Optional[EventMetadata] = None):
        super().__init__(tenant_id, metadata)
        self.old_plan = old_plan
        self.new_plan = new_plan
        self.effective_date = effective_date
    
    @property
    def event_type(self) -> str:
        return "subscription.upgraded"
    
    @property
    def aggregate_id(self) -> str:
        return self.tenant_id
    
    @property
    def aggregate_type(self) -> str:
        return "Subscription"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "occurred_at": self.occurred_at.isoformat(),
            "tenant_id": self.tenant_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "old_plan": self.old_plan,
            "new_plan": self.new_plan,
            "effective_date": self.effective_date.isoformat(),
            "metadata": asdict(self.metadata) if self.metadata else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SubscriptionUpgraded':
        metadata = EventMetadata(**data.get("metadata", {})) if data.get("metadata") else None
        return cls(
            tenant_id=data["tenant_id"],
            old_plan=data["old_plan"],
            new_plan=data["new_plan"],
            effective_date=datetime.fromisoformat(data["effective_date"]),
            metadata=metadata
        )


# ====================================================================
# EVENT REGISTRY FOR DESERIALIZATION
# ====================================================================

EVENT_REGISTRY = {
    "campaign.created": CampaignCreated,
    "campaign.launched": CampaignLaunched,
    "campaign.metrics.updated": CampaignMetricsUpdated,
    "lead.captured": LeadCaptured,
    "lead.qualified": LeadQualified,
    "lead.converted": LeadConverted,
    "tenant.created": TenantCreated,
    "subscription.upgraded": SubscriptionUpgraded,
}


def deserialize_event(event_data: Dict[str, Any]) -> DomainEvent:
    """Deserialize event from dictionary using event registry"""
    event_type = event_data.get("event_type")
    if event_type not in EVENT_REGISTRY:
        raise ValueError(f"Unknown event type: {event_type}")
    
    event_class = EVENT_REGISTRY[event_type]
    return event_class.from_dict(event_data)


def deserialize_events(events_data: List[Dict[str, Any]]) -> List[DomainEvent]:
    """Deserialize multiple events from list of dictionaries"""
    return [deserialize_event(event_data) for event_data in events_data]