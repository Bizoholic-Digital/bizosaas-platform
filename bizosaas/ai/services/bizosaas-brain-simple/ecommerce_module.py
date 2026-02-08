#!/usr/bin/env python3

"""
BizOSaaS Integrated E-commerce Module
Replaces separate Saleor backend with integrated e-commerce functionality
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
import uuid

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
import asyncpg
import redis

# ===========================================
# E-COMMERCE DATA MODELS
# ===========================================

class ProductStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class ProductType(str, Enum):
    PHYSICAL = "physical"
    DIGITAL = "digital"
    SERVICE = "service"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Product(BaseModel):
    id: Optional[str] = None
    tenant_id: str
    name: str
    description: Optional[str] = None
    sku: str
    price: Decimal
    compare_at_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    product_type: ProductType = ProductType.PHYSICAL
    status: ProductStatus = ProductStatus.DRAFT
    inventory_quantity: int = 0
    track_inventory: bool = True
    weight: Optional[Decimal] = None
    images: List[str] = []
    tags: List[str] = []
    categories: List[str] = []
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Customer(BaseModel):
    id: Optional[str] = None
    tenant_id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    total_spent: Decimal = Decimal("0.00")
    orders_count: int = 0
    created_at: Optional[datetime] = None

class Order(BaseModel):
    id: Optional[str] = None
    tenant_id: str
    customer_id: str
    order_number: str
    status: OrderStatus = OrderStatus.PENDING
    subtotal: Decimal
    tax_amount: Decimal = Decimal("0.00")
    shipping_amount: Decimal = Decimal("0.00")
    total_amount: Decimal
    items: List[Dict[str, Any]] = []
    shipping_address: Dict[str, str] = {}
    billing_address: Dict[str, str] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# ===========================================
# E-COMMERCE SERVICE CLASS
# ===========================================

class BizOSaaSEcommerce:
    """Integrated E-commerce functionality for BizOSaaS platform"""
    
    def __init__(self, db_pool: asyncpg.Pool, redis_client: redis.Redis):
        self.db_pool = db_pool
        self.redis_client = redis_client
        
    async def initialize_tables(self):
        """Initialize e-commerce database tables"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ecommerce_products (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    sku VARCHAR(100) UNIQUE NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    compare_at_price DECIMAL(10,2),
                    cost_price DECIMAL(10,2),
                    product_type VARCHAR(20) DEFAULT 'physical',
                    status VARCHAR(20) DEFAULT 'draft',
                    inventory_quantity INTEGER DEFAULT 0,
                    track_inventory BOOLEAN DEFAULT true,
                    weight DECIMAL(8,3),
                    images JSONB DEFAULT '[]',
                    tags JSONB DEFAULT '[]',
                    categories JSONB DEFAULT '[]',
                    seo_title VARCHAR(255),
                    seo_description TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ecommerce_customers (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20),
                    total_spent DECIMAL(10,2) DEFAULT 0.00,
                    orders_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ecommerce_orders (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
                    customer_id UUID REFERENCES ecommerce_customers(id),
                    order_number VARCHAR(50) UNIQUE NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    subtotal DECIMAL(10,2) NOT NULL,
                    tax_amount DECIMAL(10,2) DEFAULT 0.00,
                    shipping_amount DECIMAL(10,2) DEFAULT 0.00,
                    total_amount DECIMAL(10,2) NOT NULL,
                    items JSONB DEFAULT '[]',
                    shipping_address JSONB DEFAULT '{}',
                    billing_address JSONB DEFAULT '{}',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)

    async def create_product(self, tenant_id: str, product: Product) -> Product:
        """Create a new product"""
        async with self.db_pool.acquire() as conn:
            product_id = str(uuid.uuid4())
            
            await conn.execute("""
                INSERT INTO ecommerce_products 
                (id, tenant_id, name, description, sku, price, compare_at_price, cost_price, 
                 product_type, status, inventory_quantity, track_inventory, weight, 
                 images, tags, categories, seo_title, seo_description)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)
            """, 
            product_id, tenant_id, product.name, product.description, product.sku,
            product.price, product.compare_at_price, product.cost_price,
            product.product_type.value, product.status.value, 
            product.inventory_quantity, product.track_inventory, product.weight,
            product.images, product.tags, product.categories, 
            product.seo_title, product.seo_description)
            
            # Cache product data
            cache_key = f"product:{tenant_id}:{product_id}"
            self.redis_client.setex(cache_key, 3600, str(product.dict()))
            
            product.id = product_id
            product.tenant_id = tenant_id
            product.created_at = datetime.now(timezone.utc)
            return product

    async def get_products(self, tenant_id: str, status: Optional[ProductStatus] = None, 
                          limit: int = 50, offset: int = 0) -> List[Product]:
        """Get products for a tenant"""
        async with self.db_pool.acquire() as conn:
            query = """
                SELECT * FROM ecommerce_products 
                WHERE tenant_id = $1
            """
            params = [tenant_id]
            
            if status:
                query += " AND status = $2"
                params.append(status.value)
                
            query += " ORDER BY created_at DESC LIMIT $" + str(len(params)+1) + " OFFSET $" + str(len(params)+2)
            params.extend([limit, offset])
            
            rows = await conn.fetch(query, *params)
            
            products = []
            for row in rows:
                product = Product(
                    id=str(row['id']),
                    tenant_id=str(row['tenant_id']),
                    name=row['name'],
                    description=row['description'],
                    sku=row['sku'],
                    price=row['price'],
                    compare_at_price=row['compare_at_price'],
                    cost_price=row['cost_price'],
                    product_type=ProductType(row['product_type']),
                    status=ProductStatus(row['status']),
                    inventory_quantity=row['inventory_quantity'],
                    track_inventory=row['track_inventory'],
                    weight=row['weight'],
                    images=row['images'] or [],
                    tags=row['tags'] or [],
                    categories=row['categories'] or [],
                    seo_title=row['seo_title'],
                    seo_description=row['seo_description'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                products.append(product)
                
            return products

    async def create_customer(self, tenant_id: str, customer: Customer) -> Customer:
        """Create a new customer"""
        async with self.db_pool.acquire() as conn:
            customer_id = str(uuid.uuid4())
            
            await conn.execute("""
                INSERT INTO ecommerce_customers 
                (id, tenant_id, email, first_name, last_name, phone)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, customer_id, tenant_id, customer.email, customer.first_name, 
                customer.last_name, customer.phone)
            
            customer.id = customer_id
            customer.tenant_id = tenant_id
            customer.created_at = datetime.now(timezone.utc)
            return customer

    async def create_order(self, tenant_id: str, order: Order) -> Order:
        """Create a new order"""
        async with self.db_pool.acquire() as conn:
            order_id = str(uuid.uuid4())
            order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{order_id[:8].upper()}"
            
            await conn.execute("""
                INSERT INTO ecommerce_orders 
                (id, tenant_id, customer_id, order_number, status, subtotal, 
                 tax_amount, shipping_amount, total_amount, items, 
                 shipping_address, billing_address)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            """, order_id, tenant_id, order.customer_id, order_number,
                order.status.value, order.subtotal, order.tax_amount,
                order.shipping_amount, order.total_amount, order.items,
                order.shipping_address, order.billing_address)
            
            order.id = order_id
            order.tenant_id = tenant_id
            order.order_number = order_number
            order.created_at = datetime.now(timezone.utc)
            return order

    async def get_dashboard_stats(self, tenant_id: str) -> Dict[str, Any]:
        """Get e-commerce dashboard statistics"""
        async with self.db_pool.acquire() as conn:
            # Products stats
            products_total = await conn.fetchval(
                "SELECT COUNT(*) FROM ecommerce_products WHERE tenant_id = $1", tenant_id)
            products_published = await conn.fetchval(
                "SELECT COUNT(*) FROM ecommerce_products WHERE tenant_id = $1 AND status = 'published'", 
                tenant_id)
            
            # Orders stats
            orders_total = await conn.fetchval(
                "SELECT COUNT(*) FROM ecommerce_orders WHERE tenant_id = $1", tenant_id)
            revenue_total = await conn.fetchval(
                "SELECT COALESCE(SUM(total_amount), 0) FROM ecommerce_orders WHERE tenant_id = $1", 
                tenant_id)
            
            # Customers stats
            customers_total = await conn.fetchval(
                "SELECT COUNT(*) FROM ecommerce_customers WHERE tenant_id = $1", tenant_id)
            
            return {
                "products": {
                    "total": products_total or 0,
                    "published": products_published or 0,
                    "draft": (products_total or 0) - (products_published or 0)
                },
                "orders": {
                    "total": orders_total or 0,
                    "revenue": float(revenue_total or 0)
                },
                "customers": {
                    "total": customers_total or 0
                }
            }

# ===========================================
# FASTAPI ROUTER FOR E-COMMERCE ENDPOINTS
# ===========================================

def create_ecommerce_router(db_pool: asyncpg.Pool, redis_client: redis.Redis) -> APIRouter:
    """Create FastAPI router for e-commerce endpoints"""
    router = APIRouter(prefix="/ecommerce", tags=["E-commerce"])
    ecommerce = BizOSaaSEcommerce(db_pool, redis_client)
    
    @router.get("/dashboard/stats")
    async def get_ecommerce_stats(tenant_id: str):
        """Get e-commerce dashboard statistics"""
        return await ecommerce.get_dashboard_stats(tenant_id)
    
    @router.post("/products", response_model=Product)
    async def create_product(tenant_id: str, product: Product):
        """Create a new product"""
        return await ecommerce.create_product(tenant_id, product)
    
    @router.get("/products", response_model=List[Product])
    async def get_products(
        tenant_id: str,
        status: Optional[ProductStatus] = None,
        limit: int = Query(50, le=100),
        offset: int = Query(0, ge=0)
    ):
        """Get products for a tenant"""
        return await ecommerce.get_products(tenant_id, status, limit, offset)
    
    @router.post("/customers", response_model=Customer)
    async def create_customer(tenant_id: str, customer: Customer):
        """Create a new customer"""
        return await ecommerce.create_customer(tenant_id, customer)
    
    @router.post("/orders", response_model=Order)
    async def create_order(tenant_id: str, order: Order):
        """Create a new order"""
        return await ecommerce.create_order(tenant_id, order)
    
    return router