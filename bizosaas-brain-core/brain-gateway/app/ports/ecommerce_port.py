from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class ProductVariant(BaseModel):
    id: Optional[str] = None
    sku: Optional[str] = None
    price: float
    stock_quantity: int = 0
    attributes: Dict[str, str] = {}

class Product(BaseModel):
    id: Optional[str] = None
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    price: float
    currency: str = "USD"
    stock_quantity: int = 0
    sku: Optional[str] = None
    images: List[str] = []
    category_ids: List[str] = []
    variants: List[ProductVariant] = []
    status: str = "active"

class OrderItem(BaseModel):
    product_id: str
    variant_id: Optional[str] = None
    quantity: int
    price: float
    total: float

class Order(BaseModel):
    id: Optional[str] = None
    customer_id: Optional[str] = None
    email: Optional[str] = None
    items: List[OrderItem] = []
    total_amount: float
    currency: str = "USD"
    status: str  # pending, processing, completed, cancelled
    shipping_address: Optional[Dict[str, Any]] = None
    billing_address: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None

class EcommerceStats(BaseModel):
    products: int
    orders: int
    revenue: float
    last_sync: Optional[datetime] = None

class ECommercePort(ABC):
    """
    Abstract Port for E-Commerce platforms (WooCommerce, Shopify, Saleor).
    """

    @abstractmethod
    async def get_stats(self) -> EcommerceStats:
        """Retrieve E-commerce statistics."""
        pass

    @abstractmethod
    async def get_products(self, limit: int = 100, category_id: Optional[str] = None) -> List[Product]:
        pass

    @abstractmethod
    async def get_product(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    async def create_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def update_product(self, product_id: str, updates: Dict[str, Any]) -> Product:
        pass

    @abstractmethod
    async def delete_product(self, product_id: str) -> bool:
        pass

    @abstractmethod
    async def update_inventory(self, product_id: str, quantity: int) -> bool:
        pass

    @abstractmethod
    async def get_orders(self, limit: int = 100, status: Optional[str] = None) -> List[Order]:
        pass
    
    @abstractmethod
    async def get_order(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    async def update_order_status(self, order_id: str, status: str) -> Order:
        pass
