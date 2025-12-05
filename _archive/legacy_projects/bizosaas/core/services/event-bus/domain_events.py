"""
Domain Event Definitions for BizOSaaS Platform

This module defines all domain events that can occur across the platform,
enabling event-driven architecture and AI agent coordination.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EventStatus(str, Enum):
    """Event processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class EventPriority(str, Enum):
    """Event priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class EventCategory(str, Enum):
    """Event categories for organization"""
    USER = "user"
    TENANT = "tenant"
    CAMPAIGN = "campaign"
    LEAD = "lead"
    AI_ANALYSIS = "ai_analysis"
    SYSTEM = "system"
    INTEGRATION = "integration"
    BILLING = "billing"
    SECURITY = "security"


class BaseEvent(BaseModel):
    """Base domain event with common fields"""
    
    # Event identification
    event_id: UUID = Field(default_factory=uuid4, description="Unique event identifier")
    event_type: str = Field(..., description="Type of event (e.g., 'lead.created')")
    event_version: str = Field(default="1.0", description="Event schema version")
    
    # Event metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the event occurred")
    tenant_id: UUID = Field(..., description="Tenant context for multi-tenancy")
    source_service: str = Field(..., description="Service that emitted the event")
    correlation_id: Optional[UUID] = Field(None, description="Request correlation ID")
    causation_id: Optional[UUID] = Field(None, description="ID of the event that caused this event")
    
    # Event properties
    category: EventCategory = Field(..., description="Event category")
    priority: EventPriority = Field(default=EventPriority.NORMAL, description="Event priority")
    aggregate_id: Optional[UUID] = Field(None, description="ID of the aggregate root")
    aggregate_type: Optional[str] = Field(None, description="Type of aggregate root")
    
    # Event data
    data: Dict[str, Any] = Field(default_factory=dict, description="Event payload")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Processing info
    status: EventStatus = Field(default=EventStatus.PENDING, description="Processing status")
    retry_count: int = Field(default=0, description="Number of processing retries")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    
    # Routing and targeting
    target_services: List[str] = Field(default_factory=list, description="Services that should receive this event")
    routing_key: Optional[str] = Field(None, description="Message broker routing key")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


# User & Tenant Events

class UserCreated(BaseEvent):
    """User account created"""
    event_type: str = "user.created"
    category: EventCategory = EventCategory.USER
    
    @classmethod
    def create(cls, tenant_id: UUID, user_id: UUID, email: str, role: str, **kwargs):
        return cls(
            tenant_id=tenant_id,
            source_service="identity-service",
            aggregate_id=user_id,
            aggregate_type="User",
            data={
                "user_id": str(user_id),
                "email": email,
                "role": role,
                **kwargs
            }
        )


class UserUpdated(BaseEvent):
    """User account updated"""
    event_type: str = "user.updated"
    category: EventCategory = EventCategory.USER


class UserDeactivated(BaseEvent):
    """User account deactivated"""
    event_type: str = "user.deactivated"
    category: EventCategory = EventCategory.USER


class TenantCreated(BaseEvent):
    """New tenant organization created"""
    event_type: str = "tenant.created"
    category: EventCategory = EventCategory.TENANT
    priority: EventPriority = EventPriority.HIGH
    
    @classmethod
    def create(cls, tenant_id: UUID, name: str, subscription_plan: str, **kwargs):
        return cls(
            tenant_id=tenant_id,
            source_service="identity-service",
            aggregate_id=tenant_id,
            aggregate_type="Tenant",
            data={
                "tenant_id": str(tenant_id),
                "name": name,
                "subscription_plan": subscription_plan,
                **kwargs
            }
        )


class TenantSubscriptionChanged(BaseEvent):
    """Tenant subscription plan changed"""
    event_type: str = "tenant.subscription_changed"
    category: EventCategory = EventCategory.TENANT
    priority: EventPriority = EventPriority.HIGH


# Lead & Campaign Events

class LeadCreated(BaseEvent):
    """New lead captured"""
    event_type: str = "lead.created"
    category: EventCategory = EventCategory.LEAD
    priority: EventPriority = EventPriority.HIGH
    
    @classmethod
    def create(cls, tenant_id: UUID, lead_id: UUID, source: str, contact_info: Dict[str, Any], **kwargs):
        return cls(
            tenant_id=tenant_id,
            source_service="crm-service",
            aggregate_id=lead_id,
            aggregate_type="Lead",
            data={
                "lead_id": str(lead_id),
                "source": source,
                "contact_info": contact_info,
                **kwargs
            },
            target_services=["ai-agents", "marketing-automation", "analytics-service"]
        )


class LeadQualified(BaseEvent):
    """Lead qualified by AI or human"""
    event_type: str = "lead.qualified"
    category: EventCategory = EventCategory.LEAD
    priority: EventPriority = EventPriority.HIGH


class LeadConverted(BaseEvent):
    """Lead converted to customer"""
    event_type: str = "lead.converted"
    category: EventCategory = EventCategory.LEAD
    priority: EventPriority = EventPriority.CRITICAL


class CampaignCreated(BaseEvent):
    """Marketing campaign created"""
    event_type: str = "campaign.created"
    category: EventCategory = EventCategory.CAMPAIGN
    
    @classmethod
    def create(cls, tenant_id: UUID, campaign_id: UUID, campaign_type: str, budget: float, **kwargs):
        return cls(
            tenant_id=tenant_id,
            source_service="campaign-service",
            aggregate_id=campaign_id,
            aggregate_type="Campaign",
            data={
                "campaign_id": str(campaign_id),
                "campaign_type": campaign_type,
                "budget": budget,
                **kwargs
            },
            target_services=["ai-agents", "analytics-service"]
        )


class CampaignLaunched(BaseEvent):
    """Campaign launched and active"""
    event_type: str = "campaign.launched"
    category: EventCategory = EventCategory.CAMPAIGN
    priority: EventPriority = EventPriority.HIGH


class CampaignPaused(BaseEvent):
    """Campaign paused"""
    event_type: str = "campaign.paused"
    category: EventCategory = EventCategory.CAMPAIGN


class CampaignCompleted(BaseEvent):
    """Campaign completed"""
    event_type: str = "campaign.completed"
    category: EventCategory = EventCategory.CAMPAIGN


class CampaignOptimized(BaseEvent):
    """Campaign optimized by AI"""
    event_type: str = "campaign.optimized"
    category: EventCategory = EventCategory.CAMPAIGN
    priority: EventPriority = EventPriority.HIGH


# AI Agent Events

class AIAnalysisRequested(BaseEvent):
    """AI analysis requested"""
    event_type: str = "ai.analysis_requested"
    category: EventCategory = EventCategory.AI_ANALYSIS
    
    @classmethod
    def create(cls, tenant_id: UUID, analysis_type: str, target_id: UUID, parameters: Dict[str, Any], **kwargs):
        return cls(
            tenant_id=tenant_id,
            source_service=kwargs.get("source_service", "unknown"),
            aggregate_id=target_id,
            data={
                "analysis_type": analysis_type,
                "target_id": str(target_id),
                "parameters": parameters,
                **kwargs
            },
            target_services=["ai-agents"]
        )


class AIAnalysisStarted(BaseEvent):
    """AI analysis started processing"""
    event_type: str = "ai.analysis_started"
    category: EventCategory = EventCategory.AI_ANALYSIS


class AIAnalysisCompleted(BaseEvent):
    """AI analysis completed"""
    event_type: str = "ai.analysis_completed"
    category: EventCategory = EventCategory.AI_ANALYSIS
    priority: EventPriority = EventPriority.HIGH
    
    @classmethod
    def create(cls, tenant_id: UUID, analysis_id: UUID, analysis_type: str, results: Dict[str, Any], **kwargs):
        return cls(
            tenant_id=tenant_id,
            source_service="ai-agents",
            aggregate_id=analysis_id,
            data={
                "analysis_id": str(analysis_id),
                "analysis_type": analysis_type,
                "results": results,
                **kwargs
            }
        )


class AIAnalysisFailed(BaseEvent):
    """AI analysis failed"""
    event_type: str = "ai.analysis_failed"
    category: EventCategory = EventCategory.AI_ANALYSIS
    priority: EventPriority = EventPriority.HIGH


class AgentTaskAssigned(BaseEvent):
    """Task assigned to AI agent"""
    event_type: str = "agent.task_assigned"
    category: EventCategory = EventCategory.AI_ANALYSIS
    
    @classmethod
    def create(cls, tenant_id: UUID, agent_id: str, task_type: str, task_data: Dict[str, Any], **kwargs):
        return cls(
            tenant_id=tenant_id,
            source_service="ai-agents",
            data={
                "agent_id": agent_id,
                "task_type": task_type,
                "task_data": task_data,
                **kwargs
            }
        )


class AgentTaskCompleted(BaseEvent):
    """Task completed by AI agent"""
    event_type: str = "agent.task_completed"
    category: EventCategory = EventCategory.AI_ANALYSIS
    priority: EventPriority = EventPriority.HIGH


class AgentTaskFailed(BaseEvent):
    """Task failed by AI agent"""
    event_type: str = "agent.task_failed"
    category: EventCategory = EventCategory.AI_ANALYSIS
    priority: EventPriority = EventPriority.HIGH


# System Events

class SystemHealthCheck(BaseEvent):
    """System health check event"""
    event_type: str = "system.health_check"
    category: EventCategory = EventCategory.SYSTEM
    priority: EventPriority = EventPriority.LOW


class SystemAlert(BaseEvent):
    """System alert or warning"""
    event_type: str = "system.alert"
    category: EventCategory = EventCategory.SYSTEM
    priority: EventPriority = EventPriority.CRITICAL


class IntegrationConnected(BaseEvent):
    """External integration connected"""
    event_type: str = "integration.connected"
    category: EventCategory = EventCategory.INTEGRATION


class IntegrationDisconnected(BaseEvent):
    """External integration disconnected"""
    event_type: str = "integration.disconnected"
    category: EventCategory = EventCategory.INTEGRATION
    priority: EventPriority = EventPriority.HIGH


class IntegrationError(BaseEvent):
    """Integration error occurred"""
    event_type: str = "integration.error"
    category: EventCategory = EventCategory.INTEGRATION
    priority: EventPriority = EventPriority.HIGH


# Billing Events

class BillingUsageUpdated(BaseEvent):
    """Billing usage metrics updated"""
    event_type: str = "billing.usage_updated"
    category: EventCategory = EventCategory.BILLING


class BillingLimitExceeded(BaseEvent):
    """Billing limit exceeded"""
    event_type: str = "billing.limit_exceeded"
    category: EventCategory = EventCategory.BILLING
    priority: EventPriority = EventPriority.CRITICAL


class PaymentProcessed(BaseEvent):
    """Payment processed successfully"""
    event_type: str = "billing.payment_processed"
    category: EventCategory = EventCategory.BILLING
    priority: EventPriority = EventPriority.HIGH


class PaymentFailed(BaseEvent):
    """Payment processing failed"""
    event_type: str = "billing.payment_failed"
    category: EventCategory = EventCategory.BILLING
    priority: EventPriority = EventPriority.CRITICAL


# Security Events

class SecurityBreach(BaseEvent):
    """Security breach detected"""
    event_type: str = "security.breach"
    category: EventCategory = EventCategory.SECURITY
    priority: EventPriority = EventPriority.CRITICAL


class SuspiciousActivity(BaseEvent):
    """Suspicious activity detected"""
    event_type: str = "security.suspicious_activity"
    category: EventCategory = EventCategory.SECURITY
    priority: EventPriority = EventPriority.HIGH


class AuthenticationFailed(BaseEvent):
    """Authentication attempt failed"""
    event_type: str = "security.auth_failed"
    category: EventCategory = EventCategory.SECURITY
    priority: EventPriority = EventPriority.HIGH


# Event type registry for dynamic instantiation
EVENT_TYPES = {
    "user.created": UserCreated,
    "user.updated": UserUpdated,
    "user.deactivated": UserDeactivated,
    "tenant.created": TenantCreated,
    "tenant.subscription_changed": TenantSubscriptionChanged,
    "lead.created": LeadCreated,
    "lead.qualified": LeadQualified,
    "lead.converted": LeadConverted,
    "campaign.created": CampaignCreated,
    "campaign.launched": CampaignLaunched,
    "campaign.paused": CampaignPaused,
    "campaign.completed": CampaignCompleted,
    "campaign.optimized": CampaignOptimized,
    "ai.analysis_requested": AIAnalysisRequested,
    "ai.analysis_started": AIAnalysisStarted,
    "ai.analysis_completed": AIAnalysisCompleted,
    "ai.analysis_failed": AIAnalysisFailed,
    "agent.task_assigned": AgentTaskAssigned,
    "agent.task_completed": AgentTaskCompleted,
    "agent.task_failed": AgentTaskFailed,
    "system.health_check": SystemHealthCheck,
    "system.alert": SystemAlert,
    "integration.connected": IntegrationConnected,
    "integration.disconnected": IntegrationDisconnected,
    "integration.error": IntegrationError,
    "billing.usage_updated": BillingUsageUpdated,
    "billing.limit_exceeded": BillingLimitExceeded,
    "billing.payment_processed": PaymentProcessed,
    "billing.payment_failed": PaymentFailed,
    "security.breach": SecurityBreach,
    "security.suspicious_activity": SuspiciousActivity,
    "security.auth_failed": AuthenticationFailed,
}


def create_event(event_type: str, **kwargs) -> BaseEvent:
    """Factory function to create events dynamically"""
    event_class = EVENT_TYPES.get(event_type, BaseEvent)
    return event_class(event_type=event_type, **kwargs)


def get_event_class(event_type: str) -> type[BaseEvent]:
    """Get event class by type name"""
    return EVENT_TYPES.get(event_type, BaseEvent)