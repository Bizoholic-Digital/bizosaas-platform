import strawberry
from typing import Optional, List, Dict, Any
from datetime import datetime

@strawberry.type
class ProductVariantType:
    id: Optional[str]
    sku: Optional[str] = None
    price: float
    stock_quantity: int

@strawberry.type
class ProductType:
    id: Optional[str]
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    price: float
    currency: str
    stock_quantity: int
    sku: Optional[str] = None
    images: List[str]
    category_ids: List[str]
    variants: List[ProductVariantType]
    status: str

@strawberry.type
class OrderItemType:
    product_id: str
    variant_id: Optional[str] = None
    quantity: int
    price: float
    total: float

@strawberry.type
class OrderType:
    id: Optional[str]
    customer_id: Optional[str] = None
    email: Optional[str] = None
    items: List[OrderItemType]
    total_amount: float
    currency: str
    status: str
    created_at: Optional[datetime] = None

@strawberry.type
class EcommerceStatsType:
    products: int
    orders: int
    revenue: float
    last_sync: Optional[datetime] = None

@strawberry.input
class ProductInput:
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    price: float
    currency: str = "USD"
    stock_quantity: int = 0
    sku: Optional[str] = None
    images: Optional[List[str]] = None
    category_ids: Optional[List[str]] = None
    status: str = "active"
