"""
E-commerce Data Models for SQLAdmin Dashboard
Handles products, orders, customers, inventory, categories, and marketplace operations
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, UUID, Float, Enum, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class ProductStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"

class OrderStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"

class CustomerType(enum.Enum):
    GUEST = "guest"
    REGISTERED = "registered"
    VIP = "vip"
    WHOLESALE = "wholesale"

class ShippingStatus(enum.Enum):
    NOT_SHIPPED = "not_shipped"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"

# Product Catalog
class ProductAdmin(Base):
    __tablename__ = "ecommerce_products"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Basic product information
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    short_description = Column(Text)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    
    # Categorization
    category_id = Column(UUID(as_uuid=True), ForeignKey("ecommerce_categories.id"))
    brand = Column(String(100))
    tags = Column(JSON, default=[])
    
    # Pricing
    price = Column(DECIMAL(10, 2), nullable=False)
    compare_price = Column(DECIMAL(10, 2))  # Original price for discounts
    cost_price = Column(DECIMAL(10, 2))  # Cost to business
    currency = Column(String(3), default="USD")
    
    # Tax and shipping
    tax_class = Column(String(50))
    is_taxable = Column(Boolean, default=True)
    weight = Column(Float)
    weight_unit = Column(String(10), default="kg")
    requires_shipping = Column(Boolean, default=True)
    
    # Inventory management
    track_inventory = Column(Boolean, default=True)
    inventory_quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=10)
    allow_backorders = Column(Boolean, default=False)
    
    # Product variants
    has_variants = Column(Boolean, default=False)
    variant_options = Column(JSON, default=[])  # Color, Size, etc.
    
    # Digital products
    is_digital = Column(Boolean, default=False)
    digital_files = Column(JSON, default=[])
    download_limit = Column(Integer)
    download_expiry_days = Column(Integer)
    
    # SEO and marketing
    meta_title = Column(String(255))
    meta_description = Column(Text)
    featured_image = Column(String(500))
    gallery_images = Column(JSON, default=[])
    
    # Status and visibility
    status = Column(Enum(ProductStatus), default=ProductStatus.DRAFT)
    is_featured = Column(Boolean, default=False)
    is_visible = Column(Boolean, default=True)
    published_at = Column(DateTime(timezone=True))
    
    # Supplier and sourcing (for dropshipping)
    supplier_id = Column(UUID(as_uuid=True))
    supplier_sku = Column(String(100))
    supplier_price = Column(DECIMAL(10, 2))
    dropship_fee = Column(DECIMAL(10, 2))
    
    # Performance metrics
    view_count = Column(Integer, default=0)
    sales_count = Column(Integer, default=0)
    rating_average = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Custom fields and metadata
    custom_fields = Column(JSON, default={})
    metadata = Column(JSON, default={})
    
    # Relationships
    category = relationship("CategoryAdmin", back_populates="products")
    variants = relationship("ProductVariantAdmin", back_populates="product", cascade="all, delete-orphan")
    inventory_records = relationship("InventoryAdmin", back_populates="product")

# Product Categories
class CategoryAdmin(Base):
    __tablename__ = "ecommerce_categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Category details
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    
    # Hierarchy
    parent_id = Column(UUID(as_uuid=True), ForeignKey("ecommerce_categories.id"))
    level = Column(Integer, default=0)
    sort_order = Column(Integer, default=0)
    
    # Visual elements
    image_url = Column(String(500))
    icon = Column(String(100))
    color = Column(String(7))  # Hex color code
    
    # SEO
    meta_title = Column(String(255))
    meta_description = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Custom fields
    custom_fields = Column(JSON, default={})
    
    # Relationships
    products = relationship("ProductAdmin", back_populates="category")
    children = relationship("CategoryAdmin", remote_side=[id])

# Product Variants (sizes, colors, etc.)
class ProductVariantAdmin(Base):
    __tablename__ = "ecommerce_product_variants"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("ecommerce_products.id"), nullable=False)
    
    # Variant details
    name = Column(String(255), nullable=False)
    sku = Column(String(100), unique=True, nullable=False)
    
    # Variant options (color: red, size: large, etc.)
    option_values = Column(JSON, nullable=False)  # {"color": "red", "size": "large"}
    
    # Pricing (can override parent product)
    price = Column(DECIMAL(10, 2))
    compare_price = Column(DECIMAL(10, 2))
    cost_price = Column(DECIMAL(10, 2))
    
    # Inventory
    inventory_quantity = Column(Integer, default=0)
    weight = Column(Float)
    
    # Images
    image_url = Column(String(500))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("ProductAdmin", back_populates="variants")

# Customer management
class CustomerAdmin(Base):
    __tablename__ = "ecommerce_customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))  # Link to user account if registered
    
    # Personal details
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20))
    
    # Customer classification
    customer_type = Column(Enum(CustomerType), default=CustomerType.GUEST)
    customer_group = Column(String(50))  # VIP, Wholesale, etc.
    
    # Demographics
    date_of_birth = Column(DateTime)
    gender = Column(String(20))
    
    # Business details (for B2B)
    company_name = Column(String(200))
    tax_id = Column(String(50))
    
    # Preferences
    marketing_consent = Column(Boolean, default=False)
    preferred_language = Column(String(10), default="en")
    preferred_currency = Column(String(3), default="USD")
    
    # Customer metrics
    total_orders = Column(Integer, default=0)
    total_spent = Column(DECIMAL(12, 2), default=0.00)
    average_order_value = Column(DECIMAL(10, 2), default=0.00)
    lifetime_value = Column(DECIMAL(12, 2), default=0.00)
    
    # Status and activity
    is_active = Column(Boolean, default=True)
    last_order_at = Column(DateTime(timezone=True))
    last_login_at = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Custom fields
    custom_fields = Column(JSON, default={})
    notes = Column(Text)
    tags = Column(JSON, default=[])
    
    # Relationships
    orders = relationship("OrderAdmin", back_populates="customer", cascade="all, delete-orphan")
    addresses = relationship("CustomerAddressAdmin", back_populates="customer", cascade="all, delete-orphan")

# Customer Addresses
class CustomerAddressAdmin(Base):
    __tablename__ = "ecommerce_customer_addresses"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("ecommerce_customers.id"), nullable=False)
    
    # Address details
    first_name = Column(String(100))
    last_name = Column(String(100))
    company = Column(String(200))
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    phone = Column(String(20))
    
    # Address type and defaults
    is_default_shipping = Column(Boolean, default=False)
    is_default_billing = Column(Boolean, default=False)
    address_type = Column(String(20), default="both")  # shipping, billing, both
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("CustomerAdmin", back_populates="addresses")

# Orders management
class OrderAdmin(Base):
    __tablename__ = "ecommerce_orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("ecommerce_customers.id"))
    
    # Order identification
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    order_status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    shipping_status = Column(Enum(ShippingStatus), default=ShippingStatus.NOT_SHIPPED)
    
    # Financial details
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    tax_amount = Column(DECIMAL(10, 2), default=0.00)
    shipping_amount = Column(DECIMAL(10, 2), default=0.00)
    discount_amount = Column(DECIMAL(10, 2), default=0.00)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default="USD")
    
    # Customer information (snapshot at time of order)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(20))
    customer_notes = Column(Text)
    
    # Shipping address
    shipping_first_name = Column(String(100))
    shipping_last_name = Column(String(100))
    shipping_company = Column(String(200))
    shipping_address_line1 = Column(String(255))
    shipping_address_line2 = Column(String(255))
    shipping_city = Column(String(100))
    shipping_state = Column(String(100))
    shipping_postal_code = Column(String(20))
    shipping_country = Column(String(100))
    
    # Billing address
    billing_first_name = Column(String(100))
    billing_last_name = Column(String(100))
    billing_company = Column(String(200))
    billing_address_line1 = Column(String(255))
    billing_address_line2 = Column(String(255))
    billing_city = Column(String(100))
    billing_state = Column(String(100))
    billing_postal_code = Column(String(20))
    billing_country = Column(String(100))
    
    # Shipping details
    shipping_method = Column(String(100))
    shipping_carrier = Column(String(100))
    tracking_number = Column(String(100))
    shipped_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    
    # Payment details
    payment_method = Column(String(50))
    payment_gateway = Column(String(50))
    transaction_id = Column(String(100))
    payment_reference = Column(String(100))
    paid_at = Column(DateTime(timezone=True))
    
    # Order source and attribution
    source = Column(String(50), default="online")  # online, phone, in-person, etc.
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    
    # Fulfillment
    is_gift = Column(Boolean, default=False)
    gift_message = Column(Text)
    special_instructions = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed_at = Column(DateTime(timezone=True))
    cancelled_at = Column(DateTime(timezone=True))
    
    # Staff management
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    processed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    customer = relationship("CustomerAdmin", back_populates="orders")
    order_items = relationship("OrderItemAdmin", back_populates="order", cascade="all, delete-orphan")

# Order Items (individual products in an order)
class OrderItemAdmin(Base):
    __tablename__ = "ecommerce_order_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("ecommerce_orders.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("ecommerce_products.id"))
    variant_id = Column(UUID(as_uuid=True), ForeignKey("ecommerce_product_variants.id"))
    
    # Product details (snapshot at time of order)
    product_name = Column(String(255), nullable=False)
    product_sku = Column(String(100), nullable=False)
    variant_name = Column(String(255))
    
    # Quantity and pricing
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)  # Price per unit at time of order
    total_price = Column(DECIMAL(10, 2), nullable=False)  # quantity * price
    
    # Product specifications
    weight = Column(Float)
    product_options = Column(JSON, default={})  # Color, size, etc.
    
    # Fulfillment status
    fulfillment_status = Column(String(50), default="pending")
    shipped_quantity = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = relationship("OrderAdmin", back_populates="order_items")

# Inventory Management
class InventoryAdmin(Base):
    __tablename__ = "ecommerce_inventory"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("ecommerce_products.id"), nullable=False)
    variant_id = Column(UUID(as_uuid=True), ForeignKey("ecommerce_product_variants.id"))
    
    # Inventory tracking
    sku = Column(String(100), nullable=False, index=True)
    quantity_on_hand = Column(Integer, default=0)
    quantity_allocated = Column(Integer, default=0)  # Reserved for orders
    quantity_available = Column(Integer, default=0)  # on_hand - allocated
    
    # Warehouse and location
    warehouse_location = Column(String(100))
    bin_location = Column(String(50))
    
    # Reorder management
    reorder_level = Column(Integer, default=10)
    reorder_quantity = Column(Integer, default=100)
    supplier_id = Column(UUID(as_uuid=True))
    
    # Cost tracking
    unit_cost = Column(DECIMAL(10, 2))
    average_cost = Column(DECIMAL(10, 2))
    last_cost = Column(DECIMAL(10, 2))
    
    # Movement tracking
    last_movement_type = Column(String(50))  # received, sold, adjusted, etc.
    last_movement_date = Column(DateTime(timezone=True))
    last_movement_quantity = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("ProductAdmin", back_populates="inventory_records")

# Inventory Movements (stock adjustments, sales, receipts)
class InventoryMovementAdmin(Base):
    __tablename__ = "ecommerce_inventory_movements"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    inventory_id = Column(UUID(as_uuid=True), ForeignKey("ecommerce_inventory.id"), nullable=False)
    
    # Movement details
    movement_type = Column(String(50), nullable=False)  # sale, purchase, adjustment, transfer, etc.
    quantity_change = Column(Integer, nullable=False)  # Positive for increases, negative for decreases
    quantity_before = Column(Integer, nullable=False)
    quantity_after = Column(Integer, nullable=False)
    
    # Cost information
    unit_cost = Column(DECIMAL(10, 2))
    total_cost = Column(DECIMAL(10, 2))
    
    # Reference information
    reference_type = Column(String(50))  # order, purchase_order, adjustment, etc.
    reference_id = Column(UUID(as_uuid=True))
    reference_number = Column(String(100))
    
    # Notes and metadata
    notes = Column(Text)
    performed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    movement_date = Column(DateTime(timezone=True), default=datetime.utcnow)

# Shipping Methods
class ShippingMethodAdmin(Base):
    __tablename__ = "ecommerce_shipping_methods"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Method details
    name = Column(String(100), nullable=False)
    description = Column(Text)
    carrier = Column(String(100))  # UPS, FedEx, USPS, etc.
    
    # Pricing
    base_cost = Column(DECIMAL(10, 2), default=0.00)
    cost_per_weight = Column(DECIMAL(10, 2), default=0.00)
    cost_per_item = Column(DECIMAL(10, 2), default=0.00)
    free_shipping_threshold = Column(DECIMAL(10, 2))
    
    # Delivery estimates
    min_delivery_days = Column(Integer)
    max_delivery_days = Column(Integer)
    
    # Restrictions
    min_weight = Column(Float)
    max_weight = Column(Float)
    allowed_countries = Column(JSON, default=[])
    excluded_countries = Column(JSON, default=[])
    
    # Status
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)