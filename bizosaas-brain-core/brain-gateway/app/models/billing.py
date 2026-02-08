from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, JSON, Numeric, Date, Boolean
from sqlalchemy.orm import relationship
from .base import Base
from .utils import GUID
import uuid
from datetime import datetime

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    price = Column(Numeric(10, 2), nullable=False, default=0.00)
    currency = Column(String(3), nullable=False, default="USD")
    interval = Column(String(20), nullable=False, default="monthly") # monthly, yearly
    features = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    subscriptions = relationship("Subscription", back_populates="plan")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(GUID, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(GUID, ForeignKey("subscription_plans.id", ondelete="RESTRICT"), nullable=False)
    status = Column(String(20), default="active", nullable=False) # active, cancelled, past_due, trialing
    current_period_start = Column(DateTime(timezone=True), nullable=False)
    current_period_end = Column(DateTime(timezone=True), nullable=False)
    cancel_at_period_end = Column(Boolean, default=False, nullable=False)
    
    gateway = Column(String(20), nullable=True) # razorpay, stripe, paypal
    gateway_subscription_id = Column(String(255), nullable=True)
    gateway_customer_id = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    tenant = relationship("Tenant")
    plan = relationship("SubscriptionPlan", back_populates="subscriptions")
    invoices = relationship("Invoice", back_populates="subscription")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(GUID, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    subscription_id = Column(GUID, ForeignKey("subscriptions.id", ondelete="SET NULL"), nullable=True)
    
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    status = Column(String(20), default="open", nullable=False) # draft, open, paid, void, uncollectible
    
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    due_date = Column(Date, nullable=False)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    
    gateway_invoice_id = Column(String(255), nullable=True)
    pdf_url = Column(String(512), nullable=True)
    
    billing_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    subscription = relationship("Subscription", back_populates="invoices")

class UsageEvent(Base):
    __tablename__ = "usage_events"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(GUID, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False, index=True) # ai_query, connector_sync, email_send
    quantity = Column(Integer, default=1, nullable=False)
    properties = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
