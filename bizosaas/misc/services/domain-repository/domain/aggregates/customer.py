"""
Customer Aggregate - Central domain model for customer management

This aggregate handles customer lifecycle including:
- Customer creation from lead conversion
- Customer profile management
- Relationship and interaction tracking
- Customer segmentation and scoring
- Subscription and billing management
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, String, DateTime, Numeric, Text, Enum as SQLEnum, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from .base import AggregateRoot, DomainEvent, ValueObject, BaseEntity, BusinessRuleViolation


class CustomerStatus(str, Enum):
    """Customer status throughout the lifecycle"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CHURNED = "churned"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


class CustomerTier(str, Enum):
    """Customer tier/segment levels"""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    ENTERPRISE = "enterprise"


class CustomerType(str, Enum):
    """Type of customer"""
    INDIVIDUAL = "individual"
    SMALL_BUSINESS = "small_business"
    MEDIUM_BUSINESS = "medium_business"
    ENTERPRISE = "enterprise"
    NON_PROFIT = "non_profit"
    GOVERNMENT = "government"


class SubscriptionStatus(str, Enum):
    """Subscription status"""
    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    PAUSED = "paused"


class CustomerAddress(ValueObject):
    """Value object for customer address"""
    
    street_address: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    address_type: str = "billing"  # billing, shipping, headquarters
    
    @property
    def formatted_address(self) -> str:
        """Get formatted address string"""
        parts = [
            self.street_address,
            self.city,
            self.state_province,
            self.postal_code,
            self.country
        ]
        return ', '.join(filter(None, parts))


class CustomerProfile(ValueObject):
    """Value object for customer profile information"""
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    annual_revenue: Optional[Decimal] = None
    timezone: Optional[str] = None
    preferred_language: str = "en"
    
    @property
    def full_name(self) -> str:
        """Get full name"""
        parts = [self.first_name, self.last_name]
        return ' '.join(filter(None, parts))
    
    @property
    def display_name(self) -> str:
        """Get the best display name available"""
        if self.full_name.strip():
            return self.full_name
        if self.company_name:
            return self.company_name
        return self.email


class CustomerMetrics(ValueObject):
    """Value object for customer metrics and KPIs"""
    
    lifetime_value: Decimal = Decimal('0.00')
    total_revenue: Decimal = Decimal('0.00')
    total_orders: int = 0
    average_order_value: Decimal = Decimal('0.00')
    last_order_date: Optional[datetime] = None
    acquisition_cost: Optional[Decimal] = None
    churn_risk_score: int = 0  # 0-100
    satisfaction_score: Optional[int] = None  # 1-10
    nps_score: Optional[int] = None  # -100 to 100
    support_tickets_count: int = 0
    
    @validator('churn_risk_score')
    def validate_churn_risk_score(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Churn risk score must be between 0 and 100')
        return v
    
    @validator('satisfaction_score')
    def validate_satisfaction_score(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError('Satisfaction score must be between 1 and 10')
        return v
    
    @validator('nps_score')
    def validate_nps_score(cls, v):
        if v is not None and (v < -100 or v > 100):
            raise ValueError('NPS score must be between -100 and 100')
        return v


class SubscriptionInfo(ValueObject):
    """Value object for subscription information"""
    
    subscription_id: Optional[UUID] = None
    plan_id: Optional[str] = None
    plan_name: Optional[str] = None
    status: SubscriptionStatus = SubscriptionStatus.TRIAL
    started_at: Optional[datetime] = None
    trial_ends_at: Optional[datetime] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    canceled_at: Optional[datetime] = None
    monthly_value: Optional[Decimal] = None
    yearly_value: Optional[Decimal] = None
    billing_cycle: str = "monthly"  # monthly, yearly, one-time
    
    @property
    def is_trial(self) -> bool:
        """Check if customer is in trial"""
        return self.status == SubscriptionStatus.TRIAL
    
    @property
    def is_active(self) -> bool:
        """Check if subscription is active"""
        return self.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIAL]
    
    @property
    def days_until_renewal(self) -> Optional[int]:
        """Get days until next renewal"""
        if not self.current_period_end:
            return None
        delta = self.current_period_end - datetime.utcnow()
        return max(0, delta.days)


class CustomerInteraction(ValueObject):
    """Value object for customer interactions"""
    
    interaction_id: UUID = Field(default_factory=uuid4)
    interaction_type: str  # support, sales, marketing, onboarding, etc.
    channel: str  # email, phone, chat, in-person, etc.
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[UUID] = None  # Staff member who handled interaction
    subject: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    outcome: Optional[str] = None
    sentiment: Optional[str] = None  # positive, neutral, negative
    duration_minutes: Optional[int] = None


# Domain Events
class CustomerCreated(DomainEvent):
    """Event raised when a new customer is created"""
    event_type: str = "customer.created"


class CustomerProfileUpdated(DomainEvent):
    """Event raised when customer profile is updated"""
    event_type: str = "customer.profile_updated"


class CustomerStatusChanged(DomainEvent):
    """Event raised when customer status changes"""
    event_type: str = "customer.status_changed"


class CustomerTierChanged(DomainEvent):
    """Event raised when customer tier changes"""
    event_type: str = "customer.tier_changed"


class CustomerSubscriptionUpdated(DomainEvent):
    """Event raised when subscription info is updated"""
    event_type: str = "customer.subscription_updated"


class CustomerInteractionAdded(DomainEvent):
    """Event raised when an interaction is recorded"""
    event_type: str = "customer.interaction_added"


class CustomerChurnRiskUpdated(DomainEvent):
    """Event raised when churn risk score changes significantly"""
    event_type: str = "customer.churn_risk_updated"


# Customer Aggregate Root
class Customer(AggregateRoot):
    """
    Customer aggregate root - manages customer lifecycle and business rules
    """
    
    # Basic Information
    profile: CustomerProfile
    status: CustomerStatus = CustomerStatus.ACTIVE
    customer_type: CustomerType = CustomerType.INDIVIDUAL
    tier: CustomerTier = CustomerTier.BRONZE
    
    # Lead Conversion Tracking
    converted_from_lead_id: Optional[UUID] = None
    conversion_date: Optional[datetime] = None
    acquisition_channel: Optional[str] = None
    
    # Addresses
    billing_address: Optional[CustomerAddress] = None
    shipping_address: Optional[CustomerAddress] = None
    
    # Subscription and Billing
    subscription: Optional[SubscriptionInfo] = None
    payment_method_id: Optional[str] = None
    billing_email: Optional[str] = None
    
    # Metrics and Analytics
    metrics: CustomerMetrics = Field(default_factory=CustomerMetrics)
    
    # Interactions and Support
    interactions: List[CustomerInteraction] = Field(default_factory=list)
    
    # Segmentation and Targeting
    segments: Set[str] = Field(default_factory=set)
    tags: Set[str] = Field(default_factory=set)
    
    # Preferences and Settings
    communication_preferences: Dict[str, bool] = Field(default_factory=dict)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    
    # Important Dates
    first_purchase_date: Optional[datetime] = None
    last_activity_date: Optional[datetime] = None
    
    # Notes and Comments
    notes: List[str] = Field(default_factory=list)
    
    def __init__(self, **data):
        super().__init__(**data)
        
        # Set default communication preferences
        if not self.communication_preferences:
            self.communication_preferences = {
                "email_marketing": True,
                "email_notifications": True,
                "sms_notifications": False,
                "phone_calls": True
            }
        
        # Raise creation event
        self.add_domain_event(CustomerCreated(
            aggregate_id=self.id,
            aggregate_type="Customer",
            tenant_id=self.tenant_id,
            data={
                "customer_id": str(self.id),
                "email": self.profile.email,
                "company_name": self.profile.company_name,
                "customer_type": self.customer_type.value,
                "tier": self.tier.value,
                "converted_from_lead_id": str(self.converted_from_lead_id) if self.converted_from_lead_id else None,
                "acquisition_channel": self.acquisition_channel
            }
        ))
    
    @classmethod
    def create_from_lead(cls, lead_id: UUID, profile: CustomerProfile, tenant_id: UUID, acquisition_channel: Optional[str] = None) -> 'Customer':
        """Create a customer from a converted lead"""
        
        customer = cls(
            tenant_id=tenant_id,
            profile=profile,
            converted_from_lead_id=lead_id,
            conversion_date=datetime.utcnow(),
            acquisition_channel=acquisition_channel,
            last_activity_date=datetime.utcnow()
        )
        
        # Set billing email to profile email if not specified
        if not customer.billing_email:
            customer.billing_email = profile.email
        
        return customer
    
    def update_profile(self, new_profile: CustomerProfile, user_id: Optional[UUID] = None) -> None:
        """Update customer profile"""
        
        old_email = self.profile.email
        self.profile = new_profile
        self.increment_version()
        
        # Update billing email if profile email changed
        if old_email != new_profile.email and self.billing_email == old_email:
            self.billing_email = new_profile.email
        
        # Record interaction
        self.add_interaction(
            interaction_type="profile_update",
            channel="system",
            user_id=user_id,
            details={
                "old_email": old_email,
                "new_email": new_profile.email
            }
        )
        
        # Raise profile update event
        self.add_domain_event(CustomerProfileUpdated(
            aggregate_id=self.id,
            aggregate_type="Customer",
            tenant_id=self.tenant_id,
            data={
                "customer_id": str(self.id),
                "old_email": old_email,
                "new_email": new_profile.email,
                "updated_by": str(user_id) if user_id else None
            }
        ))
    
    def change_status(self, new_status: CustomerStatus, user_id: Optional[UUID] = None, reason: Optional[str] = None) -> None:
        """Change customer status"""
        
        if new_status == self.status:
            return  # No change needed
        
        old_status = self.status
        self.status = new_status
        self.increment_version()
        
        # Handle status-specific logic
        if new_status == CustomerStatus.CHURNED:
            self.metrics = self.metrics.copy(update={"churn_risk_score": 100})
        elif new_status == CustomerStatus.ACTIVE and old_status == CustomerStatus.CHURNED:
            self.metrics = self.metrics.copy(update={"churn_risk_score": 0})
        
        # Record interaction
        self.add_interaction(
            interaction_type="status_change",
            channel="system",
            user_id=user_id,
            details={
                "old_status": old_status.value,
                "new_status": new_status.value,
                "reason": reason
            }
        )
        
        # Raise status change event
        self.add_domain_event(CustomerStatusChanged(
            aggregate_id=self.id,
            aggregate_type="Customer",
            tenant_id=self.tenant_id,
            data={
                "customer_id": str(self.id),
                "old_status": old_status.value,
                "new_status": new_status.value,
                "changed_by": str(user_id) if user_id else None,
                "reason": reason
            }
        ))
    
    def upgrade_tier(self, new_tier: CustomerTier, user_id: Optional[UUID] = None) -> None:
        """Upgrade customer tier"""
        
        if new_tier == self.tier:
            return  # No change needed
        
        # Validate tier upgrade (can only go up)
        tier_order = [CustomerTier.BRONZE, CustomerTier.SILVER, CustomerTier.GOLD, CustomerTier.PLATINUM, CustomerTier.ENTERPRISE]
        current_index = tier_order.index(self.tier)
        new_index = tier_order.index(new_tier)
        
        if new_index < current_index:
            raise BusinessRuleViolation(f"Cannot downgrade tier from {self.tier.value} to {new_tier.value}")
        
        old_tier = self.tier
        self.tier = new_tier
        self.increment_version()
        
        # Record interaction
        self.add_interaction(
            interaction_type="tier_upgrade",
            channel="system",
            user_id=user_id,
            details={
                "old_tier": old_tier.value,
                "new_tier": new_tier.value
            }
        )
        
        # Raise tier change event
        self.add_domain_event(CustomerTierChanged(
            aggregate_id=self.id,
            aggregate_type="Customer",
            tenant_id=self.tenant_id,
            data={
                "customer_id": str(self.id),
                "old_tier": old_tier.value,
                "new_tier": new_tier.value,
                "upgraded_by": str(user_id) if user_id else None
            }
        ))
    
    def update_subscription(self, subscription_info: SubscriptionInfo, user_id: Optional[UUID] = None) -> None:
        """Update subscription information"""
        
        old_subscription = self.subscription
        self.subscription = subscription_info
        self.increment_version()
        
        # Auto-upgrade tier based on subscription value
        if subscription_info.monthly_value:
            monthly_value = subscription_info.monthly_value
            if monthly_value >= 1000 and self.tier != CustomerTier.ENTERPRISE:
                self.tier = CustomerTier.ENTERPRISE
            elif monthly_value >= 500 and self.tier not in [CustomerTier.PLATINUM, CustomerTier.ENTERPRISE]:
                self.tier = CustomerTier.PLATINUM
            elif monthly_value >= 100 and self.tier not in [CustomerTier.GOLD, CustomerTier.PLATINUM, CustomerTier.ENTERPRISE]:
                self.tier = CustomerTier.GOLD
            elif monthly_value >= 25 and self.tier == CustomerTier.BRONZE:
                self.tier = CustomerTier.SILVER
        
        # Raise subscription update event
        self.add_domain_event(CustomerSubscriptionUpdated(
            aggregate_id=self.id,
            aggregate_type="Customer",
            tenant_id=self.tenant_id,
            data={
                "customer_id": str(self.id),
                "subscription_id": str(subscription_info.subscription_id) if subscription_info.subscription_id else None,
                "plan_name": subscription_info.plan_name,
                "status": subscription_info.status.value,
                "monthly_value": float(subscription_info.monthly_value) if subscription_info.monthly_value else None,
                "updated_by": str(user_id) if user_id else None
            }
        ))
    
    def add_interaction(self, interaction_type: str, channel: str, user_id: Optional[UUID] = None, subject: Optional[str] = None, details: Optional[Dict[str, Any]] = None, outcome: Optional[str] = None, sentiment: Optional[str] = None, duration_minutes: Optional[int] = None) -> None:
        """Add an interaction record"""
        
        interaction = CustomerInteraction(
            interaction_type=interaction_type,
            channel=channel,
            user_id=user_id,
            subject=subject,
            details=details or {},
            outcome=outcome,
            sentiment=sentiment,
            duration_minutes=duration_minutes
        )
        
        self.interactions.append(interaction)
        self.last_activity_date = datetime.utcnow()
        self.increment_version()
        
        # Update churn risk based on interaction sentiment
        if sentiment == "negative":
            new_churn_risk = min(100, self.metrics.churn_risk_score + 10)
            self.update_churn_risk_score(new_churn_risk)
        elif sentiment == "positive":
            new_churn_risk = max(0, self.metrics.churn_risk_score - 5)
            self.update_churn_risk_score(new_churn_risk)
        
        # Raise interaction event
        self.add_domain_event(CustomerInteractionAdded(
            aggregate_id=self.id,
            aggregate_type="Customer",
            tenant_id=self.tenant_id,
            data={
                "customer_id": str(self.id),
                "interaction": interaction.dict(),
                "interaction_count": len(self.interactions)
            }
        ))
    
    def update_metrics(self, new_metrics: CustomerMetrics) -> None:
        """Update customer metrics"""
        
        old_churn_risk = self.metrics.churn_risk_score
        self.metrics = new_metrics
        self.increment_version()
        
        # Check for significant churn risk changes
        churn_risk_change = abs(new_metrics.churn_risk_score - old_churn_risk)
        if churn_risk_change >= 20:  # Significant change threshold
            self.add_domain_event(CustomerChurnRiskUpdated(
                aggregate_id=self.id,
                aggregate_type="Customer",
                tenant_id=self.tenant_id,
                data={
                    "customer_id": str(self.id),
                    "old_churn_risk": old_churn_risk,
                    "new_churn_risk": new_metrics.churn_risk_score,
                    "risk_level": self._get_churn_risk_level(new_metrics.churn_risk_score)
                }
            ))
    
    def update_churn_risk_score(self, new_score: int) -> None:
        """Update churn risk score"""
        
        if new_score < 0 or new_score > 100:
            raise BusinessRuleViolation("Churn risk score must be between 0 and 100")
        
        old_score = self.metrics.churn_risk_score
        self.metrics = self.metrics.copy(update={"churn_risk_score": new_score})
        self.increment_version()
        
        # Check for significant changes
        score_change = abs(new_score - old_score)
        if score_change >= 20:  # Significant change threshold
            self.add_domain_event(CustomerChurnRiskUpdated(
                aggregate_id=self.id,
                aggregate_type="Customer",
                tenant_id=self.tenant_id,
                data={
                    "customer_id": str(self.id),
                    "old_churn_risk": old_score,
                    "new_churn_risk": new_score,
                    "risk_level": self._get_churn_risk_level(new_score)
                }
            ))
    
    def add_segment(self, segment: str) -> None:
        """Add customer to a segment"""
        self.segments.add(segment.lower().strip())
        self.increment_version()
    
    def remove_segment(self, segment: str) -> None:
        """Remove customer from a segment"""
        self.segments.discard(segment.lower().strip())
        self.increment_version()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the customer"""
        self.tags.add(tag.lower().strip())
        self.increment_version()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the customer"""
        self.tags.discard(tag.lower().strip())
        self.increment_version()
    
    def update_communication_preferences(self, preferences: Dict[str, bool]) -> None:
        """Update communication preferences"""
        self.communication_preferences.update(preferences)
        self.increment_version()
    
    def add_note(self, note: str, user_id: Optional[UUID] = None) -> None:
        """Add a note to the customer"""
        timestamp = datetime.utcnow().isoformat()
        formatted_note = f"[{timestamp}] {note}"
        if user_id:
            formatted_note = f"[{timestamp}] [{user_id}] {note}"
        
        self.notes.append(formatted_note)
        self.increment_version()
    
    def record_purchase(self, order_value: Decimal, order_date: Optional[datetime] = None) -> None:
        """Record a purchase and update metrics"""
        
        if order_date is None:
            order_date = datetime.utcnow()
        
        # Update first purchase date
        if self.first_purchase_date is None:
            self.first_purchase_date = order_date
        
        # Update metrics
        new_total_orders = self.metrics.total_orders + 1
        new_total_revenue = self.metrics.total_revenue + order_value
        new_average_order_value = new_total_revenue / new_total_orders
        
        self.metrics = self.metrics.copy(update={
            "total_orders": new_total_orders,
            "total_revenue": new_total_revenue,
            "average_order_value": new_average_order_value,
            "last_order_date": order_date
        })
        
        self.last_activity_date = order_date
        self.increment_version()
        
        # Reduce churn risk after purchase
        new_churn_risk = max(0, self.metrics.churn_risk_score - 15)
        self.update_churn_risk_score(new_churn_risk)
    
    def _get_churn_risk_level(self, score: int) -> str:
        """Get churn risk level description"""
        if score >= 80:
            return "critical"
        elif score >= 60:
            return "high"
        elif score >= 40:
            return "medium"
        elif score >= 20:
            return "low"
        else:
            return "minimal"
    
    @property
    def age_in_days(self) -> int:
        """Get customer age in days"""
        return (datetime.utcnow() - self.created_at).days
    
    @property
    def days_since_last_activity(self) -> Optional[int]:
        """Get days since last activity"""
        if not self.last_activity_date:
            return None
        return (datetime.utcnow() - self.last_activity_date).days
    
    @property
    def days_since_last_purchase(self) -> Optional[int]:
        """Get days since last purchase"""
        if not self.metrics.last_order_date:
            return None
        return (datetime.utcnow() - self.metrics.last_order_date).days
    
    @property
    def is_at_risk(self) -> bool:
        """Check if customer is at churn risk"""
        return self.metrics.churn_risk_score >= 60


# SQLAlchemy Model for Persistence
class CustomerEntity(BaseEntity):
    """SQLAlchemy model for Customer persistence"""
    
    __tablename__ = "customers"
    
    # Basic Information
    profile_data = Column(JSON, nullable=False)  # CustomerProfile as JSON
    status = Column(SQLEnum(CustomerStatus), nullable=False, default=CustomerStatus.ACTIVE)
    customer_type = Column(SQLEnum(CustomerType), nullable=False, default=CustomerType.INDIVIDUAL)
    tier = Column(SQLEnum(CustomerTier), nullable=False, default=CustomerTier.BRONZE)
    
    # Lead Conversion Tracking
    converted_from_lead_id = Column(PGUUID(as_uuid=True))
    conversion_date = Column(DateTime)
    acquisition_channel = Column(String(100))
    
    # Addresses (stored as JSON)
    billing_address = Column(JSON)
    shipping_address = Column(JSON)
    
    # Subscription and Billing
    subscription_data = Column(JSON)  # SubscriptionInfo as JSON
    payment_method_id = Column(String(100))
    billing_email = Column(String(255))
    
    # Metrics and Analytics
    metrics_data = Column(JSON)  # CustomerMetrics as JSON
    
    # Interactions (stored as JSON array)
    interactions = Column(JSON, default=list)
    
    # Segmentation and Targeting
    segments = Column(JSON, default=list)  # Convert set to list for JSON storage
    tags = Column(JSON, default=list)  # Convert set to list for JSON storage
    
    # Preferences and Settings
    communication_preferences = Column(JSON, default=dict)
    custom_fields = Column(JSON, default=dict)
    
    # Important Dates
    first_purchase_date = Column(DateTime)
    last_activity_date = Column(DateTime)
    
    # Notes
    notes = Column(JSON, default=list)
    
    def to_domain(self) -> Customer:
        """Convert SQLAlchemy model to domain aggregate"""
        
        # Convert JSON data back to value objects
        profile = CustomerProfile(**self.profile_data)
        metrics = CustomerMetrics(**self.metrics_data) if self.metrics_data else CustomerMetrics()
        
        billing_address = CustomerAddress(**self.billing_address) if self.billing_address else None
        shipping_address = CustomerAddress(**self.shipping_address) if self.shipping_address else None
        subscription = SubscriptionInfo(**self.subscription_data) if self.subscription_data else None
        
        # Convert interactions
        interactions = [CustomerInteraction(**interaction) for interaction in (self.interactions or [])]
        
        return Customer(
            id=self.id,
            tenant_id=self.tenant_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            version=self.version,
            profile=profile,
            status=self.status,
            customer_type=self.customer_type,
            tier=self.tier,
            converted_from_lead_id=self.converted_from_lead_id,
            conversion_date=self.conversion_date,
            acquisition_channel=self.acquisition_channel,
            billing_address=billing_address,
            shipping_address=shipping_address,
            subscription=subscription,
            payment_method_id=self.payment_method_id,
            billing_email=self.billing_email,
            metrics=metrics,
            interactions=interactions,
            segments=set(self.segments or []),
            tags=set(self.tags or []),
            communication_preferences=self.communication_preferences or {},
            custom_fields=self.custom_fields or {},
            first_purchase_date=self.first_purchase_date,
            last_activity_date=self.last_activity_date,
            notes=self.notes or []
        )
    
    @classmethod
    def from_domain(cls, domain_customer: Customer) -> 'CustomerEntity':
        """Create SQLAlchemy model from domain aggregate"""
        
        return cls(
            id=domain_customer.id,
            tenant_id=domain_customer.tenant_id,
            created_at=domain_customer.created_at,
            updated_at=domain_customer.updated_at,
            version=domain_customer.version,
            profile_data=domain_customer.profile.dict(),
            status=domain_customer.status,
            customer_type=domain_customer.customer_type,
            tier=domain_customer.tier,
            converted_from_lead_id=domain_customer.converted_from_lead_id,
            conversion_date=domain_customer.conversion_date,
            acquisition_channel=domain_customer.acquisition_channel,
            billing_address=domain_customer.billing_address.dict() if domain_customer.billing_address else None,
            shipping_address=domain_customer.shipping_address.dict() if domain_customer.shipping_address else None,
            subscription_data=domain_customer.subscription.dict() if domain_customer.subscription else None,
            payment_method_id=domain_customer.payment_method_id,
            billing_email=domain_customer.billing_email,
            metrics_data=domain_customer.metrics.dict(),
            interactions=[interaction.dict() for interaction in domain_customer.interactions],
            segments=list(domain_customer.segments),
            tags=list(domain_customer.tags),
            communication_preferences=domain_customer.communication_preferences,
            custom_fields=domain_customer.custom_fields,
            first_purchase_date=domain_customer.first_purchase_date,
            last_activity_date=domain_customer.last_activity_date,
            notes=domain_customer.notes
        )