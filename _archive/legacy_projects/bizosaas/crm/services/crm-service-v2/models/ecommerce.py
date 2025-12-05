"""
E-commerce Pydantic Models for CRM Service v2
============================================

Comprehensive e-commerce models for CoreLDove integration with CRM system.
Includes product management, order processing, inventory tracking, and AI-enhanced features.

Features:
- Product catalog management with AI classification
- Order management with fraud detection
- Inventory tracking with automated reorder
- AI workflow tracking for agent integration
- Multi-tenant support with proper validation
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date
from enum import Enum
from decimal import Decimal

# Enums for e-commerce entities
class ProductCategory(str, Enum):
    """Product categories for CoreLDove"""
    SPORTS = "sports"
    FITNESS = "fitness" 
    HEALTH = "health"
    WELLNESS = "wellness"

class ProductClassification(str, Enum):
    """AI-based product classification for dropshipping suitability"""
    HERO = "hero"           # 80+ score, high profit potential
    GOOD = "good"           # 65-79 score, solid performer
    MODERATE = "moderate"   # 40-64 score, test candidate
    POOR = "poor"          # <40 score, not recommended

class ProductStatus(str, Enum):
    """Product status in catalog"""
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    ACTIVE = "active"
    PAUSED = "paused"
    DISCONTINUED = "discontinued"
    OUT_OF_STOCK = "out_of_stock"

class OrderStatus(str, Enum):
    """Order processing status"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class OrderFinancialStatus(str, Enum):
    """Order payment status"""
    PENDING = "pending"
    PAID = "paid"
    PARTIALLY_PAID = "partially_paid"
    REFUNDED = "refunded"
    VOIDED = "voided"

class FraudRiskLevel(str, Enum):
    """AI fraud detection risk levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class MarketplaceType(str, Enum):
    """Supported marketplaces"""
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    INDIAMART = "indiamart"
    ETSY = "etsy"
    OVERSTOCK = "overstock"

# Base models for reusability
class TimestampMixin(BaseModel):
    """Mixin for timestamp fields"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TenantMixin(BaseModel):
    """Mixin for multi-tenant support"""
    tenant_id: int

# Product Models
class ProductDimensions(BaseModel):
    """Product physical dimensions"""
    length: Optional[float] = Field(None, description="Length in inches")
    width: Optional[float] = Field(None, description="Width in inches")
    height: Optional[float] = Field(None, description="Height in inches")
    weight: Optional[float] = Field(None, description="Weight in pounds")

class ProductImages(BaseModel):
    """Product image URLs"""
    primary_image: Optional[str] = Field(None, description="Primary product image URL")
    additional_images: List[str] = Field(default_factory=list, description="Additional image URLs")
    product_videos: List[str] = Field(default_factory=list, description="Product video URLs")

class ProductPricing(BaseModel):
    """Product pricing information"""
    source_price: float = Field(..., description="Original marketplace price")
    recommended_price: Optional[float] = Field(None, description="AI-recommended selling price")
    current_selling_price: Optional[float] = Field(None, description="Current selling price")
    cost_basis: Optional[float] = Field(None, description="Our cost including fees")
    currency: str = Field(default="USD", description="Currency code")

class ProductMarketData(BaseModel):
    """AI-generated market insights"""
    market_opportunity: Optional[str] = Field(None, description="Market opportunity level")
    trending_score: float = Field(default=0.0, description="Trending score 0-1")
    seasonal_factors: List[str] = Field(default_factory=list, description="Seasonal considerations")
    competitive_analysis: Dict[str, Any] = Field(default_factory=dict, description="Competitive analysis data")
    estimated_monthly_sales: int = Field(default=0, description="Estimated monthly sales volume")

class ProductAIMetrics(BaseModel):
    """AI-enhanced product metrics"""
    dropship_score: float = Field(default=0.0, ge=0.0, le=100.0, description="AI dropship eligibility score")
    classification: Optional[ProductClassification] = Field(None, description="AI product classification")
    eligibility_factors: List[str] = Field(default_factory=list, description="Factors affecting eligibility")
    profit_margin_estimate: float = Field(default=0.0, description="Estimated profit margin")
    ai_workflow_id: Optional[str] = Field(None, description="AI workflow tracking ID")

class Product(TenantMixin, TimestampMixin):
    """Complete product model"""
    id: Optional[str] = None
    
    # External identifiers
    asin: str = Field(..., description="Amazon ASIN or external ID")
    sku: str = Field(..., description="Unique SKU")
    external_id: Optional[str] = Field(None, description="Other marketplace ID")
    
    # Basic information
    title: str = Field(..., min_length=1, max_length=500, description="Product title")
    brand: Optional[str] = Field(None, max_length=200, description="Brand name")
    manufacturer: Optional[str] = Field(None, max_length=200, description="Manufacturer")
    model_number: Optional[str] = Field(None, max_length=100, description="Model number")
    
    # Categorization
    category: ProductCategory = Field(..., description="Primary product category")
    subcategory: Optional[str] = Field(None, max_length=100, description="Subcategory")
    product_type: Optional[str] = Field(None, max_length=100, description="Product type")
    tags: List[str] = Field(default_factory=list, description="Product tags")
    
    # Product details
    description: Optional[str] = Field(None, description="Product description")
    key_features: List[str] = Field(default_factory=list, description="Key product features")
    specifications: Dict[str, Any] = Field(default_factory=dict, description="Technical specifications")
    
    # Physical properties
    dimensions: Optional[ProductDimensions] = None
    
    # Media
    images: Optional[ProductImages] = None
    
    # Pricing
    pricing: ProductPricing
    
    # Quality metrics
    rating: Optional[float] = Field(None, ge=0.0, le=5.0, description="Average rating")
    review_count: int = Field(default=0, ge=0, description="Number of reviews")
    sales_rank: Optional[int] = Field(None, description="Marketplace sales rank")
    
    # AI insights
    ai_metrics: Optional[ProductAIMetrics] = None
    market_data: Optional[ProductMarketData] = None
    
    # Status and inventory
    status: ProductStatus = Field(default=ProductStatus.PENDING_REVIEW)
    is_available: bool = Field(default=True, description="Product availability")
    stock_quantity: int = Field(default=0, ge=0, description="Current stock quantity")
    min_order_quantity: int = Field(default=1, ge=1, description="Minimum order quantity")
    max_order_quantity: Optional[int] = Field(None, description="Maximum order quantity")
    
    # Marketplace information
    source_marketplace: MarketplaceType = Field(default=MarketplaceType.AMAZON)
    marketplace_url: Optional[str] = Field(None, description="Direct link to source product")
    marketplace_data: Dict[str, Any] = Field(default_factory=dict, description="Raw marketplace data")
    
    # Business intelligence
    target_audience: List[str] = Field(default_factory=list, description="Target audience segments")
    marketing_keywords: List[str] = Field(default_factory=list, description="SEO keywords")

class ProductCreate(BaseModel):
    """Create new product payload"""
    tenant_id: int
    asin: str = Field(..., description="Amazon ASIN or external ID")
    sku: str = Field(..., description="Unique SKU")
    title: str = Field(..., min_length=1, max_length=500)
    category: ProductCategory
    source_price: float = Field(..., gt=0.0, description="Source marketplace price")
    description: Optional[str] = None
    brand: Optional[str] = None
    currency: str = Field(default="USD")
    
    @validator('sku')
    def validate_sku(cls, v):
        """Ensure SKU meets requirements"""
        if not v or len(v.strip()) == 0:
            raise ValueError('SKU cannot be empty')
        return v.strip().upper()

class ProductUpdate(BaseModel):
    """Update existing product payload"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    current_selling_price: Optional[float] = Field(None, gt=0.0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    status: Optional[ProductStatus] = None
    tags: Optional[List[str]] = None
    ai_metrics: Optional[ProductAIMetrics] = None

# Order Models
class OrderAddress(BaseModel):
    """Shipping/billing address"""
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    company: Optional[str] = Field(None, max_length=200)
    address1: str = Field(..., max_length=200)
    address2: Optional[str] = Field(None, max_length=200)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    zip_code: str = Field(..., max_length=20)
    country: str = Field(..., max_length=100)
    phone: Optional[str] = Field(None, max_length=50)

class OrderItem(BaseModel):
    """Individual order line item"""
    product_id: str = Field(..., description="Product ID")
    sku: str = Field(..., description="Product SKU")
    title: str = Field(..., description="Product title at time of order")
    quantity: int = Field(..., gt=0, description="Ordered quantity")
    unit_price: float = Field(..., gt=0.0, description="Unit price")
    total_price: float = Field(..., gt=0.0, description="Line total")
    
    @validator('total_price', always=True)
    def validate_total_price(cls, v, values):
        """Validate total price calculation"""
        if 'quantity' in values and 'unit_price' in values:
            expected_total = values['quantity'] * values['unit_price']
            if abs(v - expected_total) > 0.01:  # Allow small floating point differences
                raise ValueError('Total price does not match quantity × unit price')
        return v

class FraudDetectionMetrics(BaseModel):
    """AI fraud detection analysis"""
    risk_level: FraudRiskLevel = Field(..., description="Fraud risk assessment")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk score 0-1")
    risk_factors: List[str] = Field(default_factory=list, description="Identified risk factors")
    verification_required: bool = Field(default=False, description="Manual verification needed")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="AI confidence in assessment")

class Order(TenantMixin, TimestampMixin):
    """Complete order model"""
    id: Optional[str] = None
    order_number: str = Field(..., description="Unique order number")
    
    # Customer information
    customer_email: EmailStr = Field(..., description="Customer email")
    customer_phone: Optional[str] = Field(None, description="Customer phone")
    
    # Order items
    items: List[OrderItem] = Field(..., min_items=1, description="Order items")
    
    # Addresses
    shipping_address: OrderAddress = Field(..., description="Shipping address")
    billing_address: Optional[OrderAddress] = Field(None, description="Billing address")
    
    # Financial information
    subtotal: float = Field(..., ge=0.0, description="Subtotal amount")
    tax_amount: float = Field(default=0.0, ge=0.0, description="Tax amount")
    shipping_amount: float = Field(default=0.0, ge=0.0, description="Shipping cost")
    discount_amount: float = Field(default=0.0, ge=0.0, description="Discount applied")
    total_amount: float = Field(..., gt=0.0, description="Total order amount")
    currency: str = Field(default="USD", description="Currency code")
    
    # Status tracking
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    financial_status: OrderFinancialStatus = Field(default=OrderFinancialStatus.PENDING)
    fulfillment_status: str = Field(default="unfulfilled", description="Fulfillment status")
    
    # AI fraud detection
    fraud_analysis: Optional[FraudDetectionMetrics] = None
    
    # Processing information
    processing_notes: Optional[str] = Field(None, description="Internal processing notes")
    tracking_number: Optional[str] = Field(None, description="Shipping tracking number")
    estimated_delivery: Optional[date] = Field(None, description="Estimated delivery date")
    
    @validator('total_amount', always=True)
    def validate_total_amount(cls, v, values):
        """Validate total amount calculation"""
        subtotal = values.get('subtotal', 0.0)
        tax = values.get('tax_amount', 0.0)
        shipping = values.get('shipping_amount', 0.0)
        discount = values.get('discount_amount', 0.0)
        
        expected_total = subtotal + tax + shipping - discount
        if abs(v - expected_total) > 0.01:
            raise ValueError('Total amount does not match calculated sum')
        return v

class OrderCreate(BaseModel):
    """Create new order payload"""
    tenant_id: int
    customer_email: EmailStr
    items: List[OrderItem] = Field(..., min_items=1)
    shipping_address: OrderAddress
    billing_address: Optional[OrderAddress] = None
    subtotal: float = Field(..., ge=0.0)
    tax_amount: float = Field(default=0.0, ge=0.0)
    shipping_amount: float = Field(default=0.0, ge=0.0)
    discount_amount: float = Field(default=0.0, ge=0.0)
    total_amount: float = Field(..., gt=0.0)
    currency: str = Field(default="USD")

class OrderUpdate(BaseModel):
    """Update existing order payload"""
    status: Optional[OrderStatus] = None
    financial_status: Optional[OrderFinancialStatus] = None
    fulfillment_status: Optional[str] = None
    tracking_number: Optional[str] = None
    processing_notes: Optional[str] = None

# Inventory Models
class InventoryLevel(TenantMixin, TimestampMixin):
    """Product inventory tracking"""
    id: Optional[str] = None
    product_id: str = Field(..., description="Product ID")
    sku: str = Field(..., description="Product SKU")
    
    # Stock levels
    available_quantity: int = Field(..., ge=0, description="Available stock")
    reserved_quantity: int = Field(default=0, ge=0, description="Reserved for orders")
    incoming_quantity: int = Field(default=0, ge=0, description="Incoming stock")
    
    # Thresholds
    reorder_point: int = Field(default=10, ge=0, description="Reorder threshold")
    reorder_quantity: int = Field(default=50, ge=1, description="Standard reorder quantity")
    max_stock_level: Optional[int] = Field(None, description="Maximum stock level")
    
    # AI recommendations
    ai_reorder_recommendation: Optional[bool] = Field(None, description="AI reorder recommendation")
    predicted_stockout_date: Optional[date] = Field(None, description="AI predicted stockout")
    recommended_order_quantity: Optional[int] = Field(None, description="AI recommended order qty")

class InventoryUpdate(BaseModel):
    """Update inventory levels"""
    available_quantity: Optional[int] = Field(None, ge=0)
    reorder_point: Optional[int] = Field(None, ge=0)
    reorder_quantity: Optional[int] = Field(None, ge=1)
    max_stock_level: Optional[int] = None

class InventoryAlert(BaseModel):
    """Inventory alerts and notifications"""
    product_id: str
    sku: str
    alert_type: str = Field(..., description="Alert type (low_stock, out_of_stock, reorder)")
    message: str = Field(..., description="Alert message")
    severity: str = Field(..., description="Alert severity (info, warning, critical)")
    current_quantity: int = Field(..., ge=0)
    threshold: int = Field(..., ge=0)
    recommended_action: Optional[str] = None

# Supplier Models
class Supplier(TenantMixin, TimestampMixin):
    """Supplier information"""
    id: Optional[str] = None
    supplier_name: str = Field(..., max_length=200)
    supplier_id: Optional[str] = Field(None, description="External supplier ID")
    marketplace: MarketplaceType = Field(..., description="Source marketplace")
    
    # Contact information
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = Field(None, max_length=50)
    business_address: Dict[str, str] = Field(default_factory=dict)
    
    # Performance metrics
    fulfillment_rate: float = Field(default=1.0, ge=0.0, le=1.0, description="Order fulfillment rate")
    on_time_delivery_rate: float = Field(default=0.9, ge=0.0, le=1.0, description="On-time delivery rate")
    quality_score: float = Field(default=0.8, ge=0.0, le=1.0, description="Quality rating")
    
    # Status
    is_approved: bool = Field(default=False, description="Supplier approval status")
    is_active: bool = Field(default=True, description="Supplier active status")
    risk_level: str = Field(default="medium", description="Risk assessment")

# AI Workflow Models
class AIWorkflowExecution(TenantMixin, TimestampMixin):
    """Track AI workflow executions"""
    id: Optional[str] = None
    workflow_type: str = Field(..., description="Type of AI workflow")
    entity_type: str = Field(..., description="Entity type (product, order, etc)")
    entity_id: str = Field(..., description="Entity ID")
    
    # Execution details
    status: str = Field(default="running", description="Execution status")
    progress: float = Field(default=0.0, ge=0.0, le=1.0, description="Progress percentage")
    
    # Results
    results: Dict[str, Any] = Field(default_factory=dict, description="Workflow results")
    metrics: Dict[str, float] = Field(default_factory=dict, description="Performance metrics")
    recommendations: List[str] = Field(default_factory=list, description="AI recommendations")
    
    # Error handling
    error_message: Optional[str] = None
    retry_count: int = Field(default=0, ge=0)

# Response Models
class ProductListResponse(BaseModel):
    """Product list API response"""
    products: List[Product]
    total_count: int
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    has_next: bool
    has_previous: bool

class OrderListResponse(BaseModel):
    """Order list API response"""
    orders: List[Order]
    total_count: int
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    has_next: bool
    has_previous: bool

class InventoryListResponse(BaseModel):
    """Inventory list API response"""
    inventory_levels: List[InventoryLevel]
    alerts: List[InventoryAlert]
    total_count: int

class AIWorkflowResponse(BaseModel):
    """AI workflow execution response"""
    workflow_id: str
    status: str
    progress: float
    estimated_completion: Optional[datetime] = None
    results_available: bool = False

# Bulk operation models
class BulkProductUpdate(BaseModel):
    """Bulk product updates"""
    product_ids: List[str] = Field(..., min_items=1, max_items=100)
    updates: ProductUpdate

class BulkInventoryUpdate(BaseModel):
    """Bulk inventory updates"""
    updates: List[Dict[str, Any]] = Field(..., min_items=1, max_items=100, description="Array of {product_id, quantity} objects")

class BulkOperationResult(BaseModel):
    """Result of bulk operations"""
    success_count: int = Field(..., ge=0)
    failure_count: int = Field(..., ge=0)
    errors: List[Dict[str, str]] = Field(default_factory=list)
    processed_ids: List[str] = Field(default_factory=list)