"""
Order Processing Data Models
Comprehensive data models for e-commerce order processing workflow
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator
from pydantic.types import EmailStr


class OrderStatus(str, Enum):
    """Order status enumeration"""
    PENDING = "pending"
    PAYMENT_PENDING = "payment_pending"
    PAYMENT_AUTHORIZED = "payment_authorized"
    PAYMENT_CAPTURED = "payment_captured"
    PROCESSING = "processing"
    INVENTORY_RESERVED = "inventory_reserved"
    READY_TO_SHIP = "ready_to_ship"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    RETURNED = "returned"
    EXCHANGE_REQUESTED = "exchange_requested"
    ON_HOLD = "on_hold"
    FAILED = "failed"


class PaymentStatus(str, Enum):
    """Payment status enumeration"""
    PENDING = "pending"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    DISPUTED = "disputed"
    CHARGEBACK = "chargeback"


class FulfillmentStatus(str, Enum):
    """Fulfillment status enumeration"""
    PENDING = "pending"
    ALLOCATED = "allocated"
    PICKING = "picking"
    PACKED = "packed"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    """Payment method enumeration"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    RAZORPAY = "razorpay"
    PAYU = "payu"
    BANK_TRANSFER = "bank_transfer"
    CASH_ON_DELIVERY = "cash_on_delivery"
    DIGITAL_WALLET = "digital_wallet"


class ShippingMethod(str, Enum):
    """Shipping method enumeration"""
    STANDARD = "standard"
    EXPRESS = "express"
    OVERNIGHT = "overnight"
    SAME_DAY = "same_day"
    PICKUP = "pickup"
    DIGITAL = "digital"


class FraudRiskLevel(str, Enum):
    """Fraud risk level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Address Models
class Address(BaseModel):
    """Address model"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    address_line_1: str = Field(..., min_length=1, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=2, max_length=2)  # ISO country code
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    is_commercial: bool = Field(default=False)
    
    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "address_line_1": "123 Main St",
                "city": "New York",
                "state": "NY",
                "postal_code": "10001",
                "country": "US",
                "phone": "+1-555-123-4567",
                "email": "john.doe@email.com"
            }
        }


# Product and Item Models
class OrderItem(BaseModel):
    """Order item model"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    product_id: str = Field(..., description="Product identifier")
    variant_id: Optional[str] = Field(None, description="Product variant identifier")
    sku: str = Field(..., description="Stock keeping unit")
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    quantity: int = Field(..., ge=1, description="Quantity ordered")
    unit_price: Decimal = Field(..., ge=0, description="Unit price")
    total_price: Decimal = Field(..., ge=0, description="Total price for all units")
    weight: Optional[Decimal] = Field(None, ge=0, description="Item weight in kg")
    dimensions: Optional[Dict[str, Decimal]] = Field(None, description="Length, width, height in cm")
    category: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    image_url: Optional[str] = Field(None, max_length=500)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    @validator('total_price')
    def validate_total_price(cls, v, values):
        """Validate total price matches quantity * unit_price"""
        if 'quantity' in values and 'unit_price' in values:
            expected = values['quantity'] * values['unit_price']
            if abs(v - expected) > Decimal('0.01'):
                raise ValueError('Total price must equal quantity * unit_price')
        return v


# Payment Models
class PaymentDetails(BaseModel):
    """Payment details model"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    method: PaymentMethod = Field(..., description="Payment method")
    gateway: str = Field(..., description="Payment gateway used")
    transaction_id: Optional[str] = Field(None, description="Gateway transaction ID")
    amount: Decimal = Field(..., ge=0, description="Payment amount")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO currency code")
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    authorized_at: Optional[datetime] = None
    captured_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    failure_reason: Optional[str] = Field(None, max_length=500)
    gateway_response: Optional[Dict[str, Any]] = Field(default_factory=dict)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


# Tax and Pricing Models
class TaxLine(BaseModel):
    """Tax line item model"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., max_length=100, description="Tax name")
    rate: Decimal = Field(..., ge=0, le=1, description="Tax rate as decimal")
    amount: Decimal = Field(..., ge=0, description="Tax amount")
    jurisdiction: str = Field(..., max_length=100, description="Tax jurisdiction")
    tax_type: str = Field(..., max_length=50, description="Type of tax")


class PricingSummary(BaseModel):
    """Order pricing summary model"""
    subtotal: Decimal = Field(..., ge=0, description="Subtotal before taxes and shipping")
    tax_total: Decimal = Field(..., ge=0, description="Total tax amount")
    shipping_total: Decimal = Field(..., ge=0, description="Total shipping cost")
    discount_total: Decimal = Field(default=Decimal('0'), ge=0, description="Total discount amount")
    total: Decimal = Field(..., ge=0, description="Final total amount")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO currency code")
    tax_lines: List[TaxLine] = Field(default_factory=list)


# Shipping and Fulfillment Models
class ShippingDetails(BaseModel):
    """Shipping details model"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    method: ShippingMethod = Field(..., description="Shipping method")
    carrier: str = Field(..., max_length=100, description="Shipping carrier")
    service_type: str = Field(..., max_length=100, description="Carrier service type")
    tracking_number: Optional[str] = Field(None, max_length=100)
    tracking_url: Optional[str] = Field(None, max_length=500)
    estimated_delivery: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    weight: Optional[Decimal] = Field(None, ge=0, description="Package weight in kg")
    dimensions: Optional[Dict[str, Decimal]] = Field(None, description="Package dimensions in cm")
    cost: Decimal = Field(..., ge=0, description="Shipping cost")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class FulfillmentItem(BaseModel):
    """Fulfillment item model"""
    order_item_id: str = Field(..., description="Reference to order item")
    quantity: int = Field(..., ge=1, description="Quantity being fulfilled")
    warehouse_id: Optional[str] = Field(None, description="Fulfilling warehouse")
    location: Optional[str] = Field(None, max_length=100, description="Warehouse location")


class Fulfillment(BaseModel):
    """Fulfillment model"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    status: FulfillmentStatus = Field(default=FulfillmentStatus.PENDING)
    items: List[FulfillmentItem] = Field(..., min_items=1)
    shipping_details: Optional[ShippingDetails] = None
    warehouse_id: Optional[str] = Field(None, description="Fulfilling warehouse")
    notes: Optional[str] = Field(None, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None


# Fraud Detection Models
class FraudAssessment(BaseModel):
    """Fraud risk assessment model"""
    risk_level: FraudRiskLevel = Field(..., description="Overall risk level")
    risk_score: float = Field(..., ge=0, le=100, description="Risk score 0-100")
    factors: List[str] = Field(default_factory=list, description="Risk factors identified")
    recommendations: List[str] = Field(default_factory=list, description="Recommended actions")
    requires_review: bool = Field(default=False, description="Requires manual review")
    assessed_at: datetime = Field(default_factory=datetime.utcnow)
    assessed_by: str = Field(default="automated", description="Assessment method")


# Main Order Models
class OrderCreateRequest(BaseModel):
    """Order creation request model"""
    customer_id: str = Field(..., description="Customer identifier")
    items: List[OrderItem] = Field(..., min_items=1, description="Order items")
    billing_address: Address = Field(..., description="Billing address")
    shipping_address: Address = Field(..., description="Shipping address")
    payment_method: PaymentMethod = Field(..., description="Payment method")
    shipping_method: ShippingMethod = Field(..., description="Shipping method")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO currency code")
    notes: Optional[str] = Field(None, max_length=1000, description="Order notes")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "customer_id": "cust_12345",
                "items": [
                    {
                        "product_id": "prod_123",
                        "sku": "SKU-123",
                        "name": "Premium Widget",
                        "quantity": 2,
                        "unit_price": "29.99",
                        "total_price": "59.98"
                    }
                ],
                "billing_address": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "address_line_1": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10001",
                    "country": "US"
                },
                "payment_method": "credit_card",
                "shipping_method": "standard",
                "currency": "USD"
            }
        }


class OrderUpdateRequest(BaseModel):
    """Order update request model"""
    status: Optional[OrderStatus] = None
    notes: Optional[str] = Field(None, max_length=1000)
    metadata: Optional[Dict[str, Any]] = None
    shipping_address: Optional[Address] = None
    
    class Config:
        schema_extra = {
            "example": {
                "status": "processing",
                "notes": "Customer requested expedited shipping"
            }
        }


class FulfillmentRequest(BaseModel):
    """Fulfillment request model"""
    items: List[FulfillmentItem] = Field(..., min_items=1)
    warehouse_id: Optional[str] = None
    shipping_method: Optional[ShippingMethod] = None
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=1000)
    notify_customer: bool = Field(default=True)
    
    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {
                        "order_item_id": "item_123",
                        "quantity": 2,
                        "warehouse_id": "warehouse_1"
                    }
                ],
                "shipping_method": "express",
                "carrier": "FedEx",
                "notify_customer": True
            }
        }


class RefundRequest(BaseModel):
    """Refund request model"""
    amount: Optional[Decimal] = Field(None, ge=0, description="Refund amount (if partial)")
    reason: str = Field(..., max_length=500, description="Refund reason")
    items: Optional[List[str]] = Field(None, description="Item IDs for partial refund")
    restock_items: bool = Field(default=True, description="Whether to restock items")
    notify_customer: bool = Field(default=True)
    notes: Optional[str] = Field(None, max_length=1000)
    
    class Config:
        schema_extra = {
            "example": {
                "reason": "Customer requested refund - product not as described",
                "restock_items": True,
                "notify_customer": True
            }
        }


class OrderResponse(BaseModel):
    """Complete order response model"""
    id: str = Field(..., description="Order ID")
    order_number: str = Field(..., description="Human-readable order number")
    customer_id: str = Field(..., description="Customer identifier")
    status: OrderStatus = Field(..., description="Current order status")
    items: List[OrderItem] = Field(..., description="Order items")
    billing_address: Address = Field(..., description="Billing address")
    shipping_address: Address = Field(..., description="Shipping address")
    pricing: PricingSummary = Field(..., description="Pricing breakdown")
    payment_details: Optional[PaymentDetails] = None
    fulfillments: List[Fulfillment] = Field(default_factory=list)
    fraud_assessment: Optional[FraudAssessment] = None
    notes: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(..., description="Order creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "order_123456789",
                "order_number": "ORD-2024-001234",
                "customer_id": "cust_12345",
                "status": "processing",
                "items": [],
                "billing_address": {},
                "shipping_address": {},
                "pricing": {
                    "subtotal": "59.98",
                    "tax_total": "4.80",
                    "shipping_total": "9.99",
                    "total": "74.77",
                    "currency": "USD"
                },
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z"
            }
        }


# Tracking Models
class TrackingEvent(BaseModel):
    """Tracking event model"""
    timestamp: datetime = Field(..., description="Event timestamp")
    status: str = Field(..., max_length=100, description="Tracking status")
    location: Optional[str] = Field(None, max_length=200, description="Event location")
    description: str = Field(..., max_length=500, description="Event description")
    details: Optional[Dict[str, Any]] = Field(default_factory=dict)


class TrackingResponse(BaseModel):
    """Order tracking response model"""
    order_id: str = Field(..., description="Order ID")
    tracking_number: Optional[str] = Field(None, description="Tracking number")
    carrier: Optional[str] = Field(None, description="Shipping carrier")
    status: FulfillmentStatus = Field(..., description="Current fulfillment status")
    estimated_delivery: Optional[datetime] = None
    events: List[TrackingEvent] = Field(default_factory=list)
    last_updated: datetime = Field(..., description="Last tracking update")
    
    class Config:
        schema_extra = {
            "example": {
                "order_id": "order_123456789",
                "tracking_number": "1234567890",
                "carrier": "FedEx",
                "status": "in_transit",
                "estimated_delivery": "2024-01-05T18:00:00Z",
                "events": [
                    {
                        "timestamp": "2024-01-01T12:00:00Z",
                        "status": "shipped",
                        "location": "New York, NY",
                        "description": "Package shipped from fulfillment center"
                    }
                ],
                "last_updated": "2024-01-03T10:30:00Z"
            }
        }


# Inventory Models
class InventoryUpdate(BaseModel):
    """Inventory update model"""
    product_id: str = Field(..., description="Product ID")
    variant_id: Optional[str] = None
    quantity_change: int = Field(..., description="Quantity change (positive or negative)")
    reason: str = Field(..., max_length=200, description="Reason for inventory change")
    warehouse_id: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "product_id": "prod_123",
                "quantity_change": -2,
                "reason": "Order fulfillment",
                "warehouse_id": "warehouse_1"
            }
        }


# Analytics Models
class OrderMetrics(BaseModel):
    """Order processing metrics model"""
    total_orders: int = Field(..., description="Total number of orders")
    successful_orders: int = Field(..., description="Successfully processed orders")
    failed_orders: int = Field(..., description="Failed orders")
    average_processing_time: float = Field(..., description="Average processing time in seconds")
    success_rate: float = Field(..., description="Order success rate as percentage")
    revenue: Decimal = Field(..., description="Total revenue")
    period_start: datetime = Field(..., description="Metrics period start")
    period_end: datetime = Field(..., description="Metrics period end")


# HITL (Human-in-the-Loop) Models
class HITLReviewRequest(BaseModel):
    """Human review request model"""
    order_id: str = Field(..., description="Order requiring review")
    review_type: str = Field(..., description="Type of review required")
    priority: str = Field(..., description="Review priority level")
    reason: str = Field(..., description="Reason for review")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    assigned_to: Optional[str] = Field(None, description="Assigned reviewer")
    due_date: Optional[datetime] = Field(None, description="Review due date")


class HITLReviewResponse(BaseModel):
    """Human review response model"""
    review_id: str = Field(..., description="Review ID")
    decision: str = Field(..., description="Review decision")
    comments: Optional[str] = Field(None, description="Reviewer comments")
    approved: bool = Field(..., description="Whether approved")
    reviewed_by: str = Field(..., description="Reviewer ID")
    reviewed_at: datetime = Field(default_factory=datetime.utcnow)


# Error Models
class ProcessingError(BaseModel):
    """Order processing error model"""
    error_code: str = Field(..., description="Error code")
    error_message: str = Field(..., description="Error message")
    error_type: str = Field(..., description="Type of error")
    recoverable: bool = Field(..., description="Whether error is recoverable")
    retry_after: Optional[int] = Field(None, description="Seconds to wait before retry")
    context: Dict[str, Any] = Field(default_factory=dict, description="Error context")