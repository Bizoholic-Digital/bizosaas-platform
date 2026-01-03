"""
BillingEvent Model - Tracks billable usage events for metered billing.

Events are emitted by connectors and agents, then synced to Lago for invoicing.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum

# Import the declarative base from the existing models
from app.models import Base


class EventType(str, enum.Enum):
    """Billable event types aligned with Lago metrics."""
    # Connector Events
    CONNECTOR_SYNC = "connector_synced"
    CONNECTOR_ACTION = "connector_action"
    
    # AI Agent Events
    AI_TASK_COMPLETED = "ai_task_completed"
    AI_CHAT_MESSAGE = "ai_chat_message"
    
    # Content Events
    CONTENT_GENERATED = "content_generated"
    CONTENT_WORDS = "content_words"
    
    # Campaign Events
    CAMPAIGN_PUBLISHED = "campaign_published"
    CAMPAIGN_OPTIMIZED = "campaign_optimized"
    
    # API Events
    API_CALL = "api_call"


class BillingEvent(Base):
    """
    Stores billable usage events for metered billing.
    Events are accumulated and synced to Lago daily.
    """
    __tablename__ = "billing_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Ownership
    tenant_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=True)  # Can be None for system events
    
    # Event Details
    event_type = Column(String, nullable=False, index=True)  # Maps to Lago billable_metric_code
    event_code = Column(String, nullable=False)  # Sub-type (e.g., 'wordpress_post_sync')
    
    # Quantification
    quantity = Column(Float, default=1.0)  # Number of units (e.g., word count, sync count)
    
    # Context
    connector_id = Column(String, nullable=True)  # Which connector triggered this
    agent_id = Column(String, nullable=True)  # Which agent triggered this
    resource_type = Column(String, nullable=True)  # E.g., 'posts', 'contacts', 'ads'
    
    # Metadata for debugging and analytics
    event_metadata = Column(JSON, default=dict)
    
    # Billing Status
    synced_to_lago = Column(Integer, default=0)  # 0 = pending, 1 = synced, -1 = failed
    lago_event_id = Column(String, nullable=True)  # Lago's event ID after sync
    synced_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Compound index for efficient querying
    __table_args__ = (
        Index('ix_billing_events_tenant_pending', 'tenant_id', 'synced_to_lago', 'created_at'),
    )
    
    def to_lago_event(self) -> dict:
        """
        Convert to Lago event format for API submission.
        See: https://doc.getlago.com/api-reference/events/batch-events
        """
        return {
            "transaction_id": str(self.id),
            "external_customer_id": self.tenant_id,
            "code": self.event_type,  # Must match Lago billable_metric_code
            "timestamp": int(self.created_at.timestamp()),
            "properties": {
                "quantity": self.quantity,
                "connector_id": self.connector_id,
                "agent_id": self.agent_id,
                "event_code": self.event_code,
                "resource_type": self.resource_type,
                **(self.event_metadata or {})
            }
        }


class BillingEventService:
    """Helper methods for creating billing events."""
    
    def __init__(self, db):
        self.db = db
    
    def track_event(
        self,
        tenant_id: str,
        event_type: str,
        event_code: str,
        quantity: float = 1.0,
        connector_id: str = None,
        agent_id: str = None,
        user_id: str = None,
        resource_type: str = None,
        metadata: dict = None
    ) -> BillingEvent:
        """Create a new billing event."""
        event = BillingEvent(
            tenant_id=tenant_id,
            user_id=user_id,
            event_type=event_type,
            event_code=event_code,
            quantity=quantity,
            connector_id=connector_id,
            agent_id=agent_id,
            resource_type=resource_type,
            event_metadata=metadata or {}
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
    
    def get_pending_events(self, tenant_id: str = None, limit: int = 1000):
        """Get events pending sync to Lago."""
        query = self.db.query(BillingEvent).filter(
            BillingEvent.synced_to_lago == 0
        )
        if tenant_id:
            query = query.filter(BillingEvent.tenant_id == tenant_id)
        return query.order_by(BillingEvent.created_at).limit(limit).all()
    
    def mark_synced(self, event_ids: list, lago_event_id: str = None):
        """Mark events as successfully synced."""
        self.db.query(BillingEvent).filter(
            BillingEvent.id.in_(event_ids)
        ).update({
            'synced_to_lago': 1,
            'lago_event_id': lago_event_id,
            'synced_at': datetime.utcnow()
        }, synchronize_session=False)
        self.db.commit()
    
    def mark_failed(self, event_ids: list):
        """Mark events as failed to sync."""
        self.db.query(BillingEvent).filter(
            BillingEvent.id.in_(event_ids)
        ).update({
            'synced_to_lago': -1,
            'synced_at': datetime.utcnow()
        }, synchronize_session=False)
        self.db.commit()
