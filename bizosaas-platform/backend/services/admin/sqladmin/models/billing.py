"""
Billing Data Models for SQLAdmin Dashboard
Handles subscriptions, invoices, payments, plans, and financial operations
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, UUID, DECIMAL, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class SubscriptionStatus(enum.Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PAUSED = "paused"

class InvoiceStatus(enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PlanInterval(enum.Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    LIFETIME = "lifetime"

class PaymentMethod(enum.Enum):
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    CRYPTO = "crypto"

# Subscription Plans
class PlanAdmin(Base):
    __tablename__ = "billing_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))  # Nullable for global plans
    
    # Plan details
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    
    # Pricing
    price = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default="USD")
    interval = Column(Enum(PlanInterval), default=PlanInterval.MONTHLY)
    trial_days = Column(Integer, default=0)
    
    # Features and limits
    features = Column(JSON, default=[])
    limits = Column(JSON, default={})  # user_limit, storage_gb, api_calls, etc.
    
    # Plan metadata
    is_popular = Column(Boolean, default=False)
    is_custom = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    
    # Integration IDs
    stripe_price_id = Column(String(255))
    paypal_plan_id = Column(String(255))
    external_ids = Column(JSON, default={})
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subscriptions = relationship("SubscriptionAdmin", back_populates="plan")

# Customer Subscriptions
class SubscriptionAdmin(Base):
    __tablename__ = "billing_subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("billing_plans.id"), nullable=False)
    
    # Subscription details
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.TRIAL)
    
    # Billing cycle
    current_period_start = Column(DateTime(timezone=True), nullable=False)
    current_period_end = Column(DateTime(timezone=True), nullable=False)
    trial_start = Column(DateTime(timezone=True))
    trial_end = Column(DateTime(timezone=True))
    
    # Pricing (can override plan pricing)
    amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default="USD")
    discount_amount = Column(DECIMAL(10, 2), default=0.00)
    
    # Payment method
    default_payment_method_id = Column(UUID(as_uuid=True), ForeignKey("billing_payment_methods.id"))
    
    # Subscription modifications
    quantity = Column(Integer, default=1)  # For per-seat pricing
    custom_pricing = Column(JSON, default={})
    addons = Column(JSON, default=[])
    
    # Cancellation
    cancel_at_period_end = Column(Boolean, default=False)
    cancelled_at = Column(DateTime(timezone=True))
    cancellation_reason = Column(String(255))
    
    # Integration
    stripe_subscription_id = Column(String(255))
    paypal_subscription_id = Column(String(255))
    external_ids = Column(JSON, default={})
    
    # Metadata
    metadata = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    plan = relationship("PlanAdmin", back_populates="subscriptions")
    invoices = relationship("InvoiceAdmin", back_populates="subscription")

# Customer Payment Methods
class PaymentMethodAdmin(Base):
    __tablename__ = "billing_payment_methods"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Payment method details
    type = Column(Enum(PaymentMethod), nullable=False)
    is_default = Column(Boolean, default=False)
    
    # Card details (for card payments)
    card_brand = Column(String(50))
    card_last4 = Column(String(4))
    card_exp_month = Column(Integer)
    card_exp_year = Column(Integer)
    card_country = Column(String(2))
    
    # Bank details (for bank transfers)
    bank_name = Column(String(255))
    account_last4 = Column(String(4))
    routing_number = Column(String(20))
    
    # Billing address
    billing_name = Column(String(255))
    billing_email = Column(String(255))
    billing_phone = Column(String(20))
    billing_address_line1 = Column(String(255))
    billing_address_line2 = Column(String(255))
    billing_city = Column(String(100))
    billing_state = Column(String(100))
    billing_postal_code = Column(String(20))
    billing_country = Column(String(100))
    
    # Integration IDs
    stripe_payment_method_id = Column(String(255))
    paypal_payment_method_id = Column(String(255))
    external_ids = Column(JSON, default={})
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

# Invoices
class InvoiceAdmin(Base):
    __tablename__ = "billing_invoices"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("billing_subscriptions.id"))
    
    # Invoice identification
    invoice_number = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT)
    
    # Financial details
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    tax_amount = Column(DECIMAL(10, 2), default=0.00)
    discount_amount = Column(DECIMAL(10, 2), default=0.00)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    amount_paid = Column(DECIMAL(10, 2), default=0.00)
    amount_due = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default="USD")
    
    # Dates
    issue_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    due_date = Column(DateTime(timezone=True), nullable=False)
    paid_date = Column(DateTime(timezone=True))
    
    # Billing details
    bill_to_name = Column(String(255), nullable=False)
    bill_to_email = Column(String(255), nullable=False)
    bill_to_address = Column(JSON)
    
    # Invoice content
    line_items = Column(JSON, nullable=False)  # Invoice line items
    notes = Column(Text)
    terms = Column(Text)
    
    # PDF and delivery
    pdf_url = Column(String(500))
    sent_at = Column(DateTime(timezone=True))
    viewed_at = Column(DateTime(timezone=True))
    
    # Integration
    stripe_invoice_id = Column(String(255))
    external_ids = Column(JSON, default={})
    
    # Metadata
    metadata = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subscription = relationship("SubscriptionAdmin", back_populates="invoices")
    payments = relationship("PaymentAdmin", back_populates="invoice")

# Payments and Transactions
class PaymentAdmin(Base):
    __tablename__ = "billing_payments"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("billing_invoices.id"))
    payment_method_id = Column(UUID(as_uuid=True), ForeignKey("billing_payment_methods.id"))
    
    # Payment details
    amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default="USD")
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    # Payment method used
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    
    # Transaction details
    transaction_id = Column(String(255), unique=True, index=True)
    gateway_transaction_id = Column(String(255))
    gateway_reference = Column(String(255))
    
    # Processing
    processed_at = Column(DateTime(timezone=True))
    failure_reason = Column(String(500))
    gateway_response = Column(JSON)
    
    # Refunds
    refunded_amount = Column(DECIMAL(10, 2), default=0.00)
    refunded_at = Column(DateTime(timezone=True))
    refund_reason = Column(String(500))
    
    # Fees
    gateway_fee = Column(DECIMAL(10, 2), default=0.00)
    platform_fee = Column(DECIMAL(10, 2), default=0.00)
    net_amount = Column(DECIMAL(10, 2))
    
    # Integration
    stripe_payment_id = Column(String(255))
    paypal_payment_id = Column(String(255))
    external_ids = Column(JSON, default={})
    
    # Risk and fraud
    risk_score = Column(Float)
    is_disputed = Column(Boolean, default=False)
    dispute_reason = Column(String(255))
    
    # Metadata
    metadata = Column(JSON, default={})
    description = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    invoice = relationship("InvoiceAdmin", back_populates="payments")

# Billing Addresses
class BillingAddressAdmin(Base):
    __tablename__ = "billing_addresses"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Address details
    company_name = Column(String(255))
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    
    # Address
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    
    # Tax information
    tax_id = Column(String(100))
    vat_number = Column(String(100))
    
    # Status
    is_default = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

# Coupons and Discounts
class CouponAdmin(Base):
    __tablename__ = "billing_coupons"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))  # Nullable for global coupons
    
    # Coupon details
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Discount configuration
    discount_type = Column(String(20), nullable=False)  # percentage, fixed_amount
    discount_value = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default="USD")
    
    # Usage limits
    max_uses = Column(Integer)  # Total times coupon can be used
    max_uses_per_customer = Column(Integer, default=1)
    current_uses = Column(Integer, default=0)
    
    # Validity period
    valid_from = Column(DateTime(timezone=True), default=datetime.utcnow)
    valid_until = Column(DateTime(timezone=True))
    
    # Restrictions
    minimum_amount = Column(DECIMAL(10, 2))
    applicable_plans = Column(JSON, default=[])  # Specific plans this applies to
    first_time_customers_only = Column(Boolean, default=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# Coupon Usage Tracking
class CouponUsageAdmin(Base):
    __tablename__ = "billing_coupon_usage"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    coupon_id = Column(UUID(as_uuid=True), ForeignKey("billing_coupons.id"), nullable=False)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("billing_invoices.id"))
    
    # Usage details
    discount_amount = Column(DECIMAL(10, 2), nullable=False)
    
    # Timestamps
    used_at = Column(DateTime(timezone=True), default=datetime.utcnow)

# Tax Rates and Configuration
class TaxRateAdmin(Base):
    __tablename__ = "billing_tax_rates"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))  # Nullable for global rates
    
    # Tax details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    rate = Column(DECIMAL(5, 4), nullable=False)  # Tax rate as decimal (0.0825 for 8.25%)
    
    # Geographic scope
    country = Column(String(100))
    state = Column(String(100))
    postal_codes = Column(JSON, default=[])
    
    # Tax type
    tax_type = Column(String(50), default="sales_tax")  # sales_tax, vat, gst, etc.
    
    # Status
    is_active = Column(Boolean, default=True)
    is_inclusive = Column(Boolean, default=False)  # Tax included in price vs added
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

# Revenue and Financial Reporting
class RevenueReportAdmin(Base):
    __tablename__ = "billing_revenue_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Report period
    report_date = Column(DateTime(timezone=True), nullable=False)
    period_type = Column(String(20), nullable=False)  # daily, weekly, monthly, yearly
    
    # Revenue metrics
    gross_revenue = Column(DECIMAL(12, 2), default=0.00)
    net_revenue = Column(DECIMAL(12, 2), default=0.00)
    refunded_amount = Column(DECIMAL(12, 2), default=0.00)
    
    # Subscription metrics
    new_subscriptions = Column(Integer, default=0)
    cancelled_subscriptions = Column(Integer, default=0)
    active_subscriptions = Column(Integer, default=0)
    
    # Customer metrics
    new_customers = Column(Integer, default=0)
    churned_customers = Column(Integer, default=0)
    total_customers = Column(Integer, default=0)
    
    # Financial ratios
    monthly_recurring_revenue = Column(DECIMAL(12, 2), default=0.00)
    annual_recurring_revenue = Column(DECIMAL(12, 2), default=0.00)
    average_revenue_per_user = Column(DECIMAL(10, 2), default=0.00)
    customer_lifetime_value = Column(DECIMAL(10, 2), default=0.00)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    calculated_at = Column(DateTime(timezone=True), default=datetime.utcnow)