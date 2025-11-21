"""
CoreLDove Data Bridge Service
Synchronizes data between CoreLDove sourcing, MedusaJS, CRM, and BizOSaaS services
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
import httpx

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, text

# Import shared components
from shared.auth.jwt_auth import get_current_user, UserContext
from shared.database.models import Base

logger = logging.getLogger(__name__)

# Database Configuration
DATABASE_URL = "postgresql+asyncpg://admin:securepassword@host.docker.internal:5432/bizosaas"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Redis Clients
bizosaas_redis = None
coreldove_redis = None

# Service URLs
MEDUSA_URL = "http://coreldove-backend:9000"
SOURCING_URL = "http://coreldove-sourcing:8010"
CRM_URL = "http://coreldove-crm:8004"
AI_AGENTS_URL = "http://host.docker.internal:8000"
MARKETING_URL = "http://host.docker.internal:8020"

# Data Models
class ProductSyncRequest(BaseModel):
    source_id: str
    source_type: str  # 'amazon', 'manual', 'ai_generated'
    product_data: Dict[str, Any]
    tenant_id: Optional[str] = None

class OrderSyncRequest(BaseModel):
    order_id: str
    customer_data: Dict[str, Any]
    order_items: List[Dict[str, Any]]
    order_total: float
    tenant_id: Optional[str] = None

class DataSyncStatus(BaseModel):
    sync_id: str
    entity_type: str
    entity_id: str
    status: str  # 'pending', 'processing', 'completed', 'failed'
    source_service: str
    target_services: List[str]
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

# Background Sync Manager
class CoreLDoveSyncManager:
    """Manages data synchronization between CoreLDove services"""
    
    def __init__(self, db_session_factory, bizosaas_redis: redis.Redis, coreldove_redis: redis.Redis):
        self.db = db_session_factory
        self.bizosaas_redis = bizosaas_redis
        self.coreldove_redis = coreldove_redis
        self.sync_active = False
        self.sync_interval = 60  # 1 minute sync interval
        
    async def start_sync_manager(self):
        """Start background sync operations"""
        self.sync_active = True
        logger.info("Starting CoreLDove sync manager")
        
        while self.sync_active:
            try:
                await self._run_sync_cycle()
                await asyncio.sleep(self.sync_interval)
            except Exception as e:
                logger.error(f"Sync cycle error: {e}")
                await asyncio.sleep(30)  # Wait 30 seconds on error
    
    async def stop_sync_manager(self):
        """Stop background sync operations"""
        self.sync_active = False
        logger.info("Stopped CoreLDove sync manager")
    
    async def _run_sync_cycle(self):
        """Run one complete sync cycle"""
        # Sync products from sourcing to MedusaJS
        await self._sync_sourced_products()
        
        # Sync orders from MedusaJS to CRM
        await self._sync_orders_to_crm()
        
        # Sync customer data between services
        await self._sync_customer_data()
        
        # Update analytics and metrics
        await self._update_analytics()
        
        logger.debug("Sync cycle completed")
    
    async def _sync_sourced_products(self):
        """Sync new products from sourcing service to MedusaJS"""
        try:
            # Get pending products from sourcing service
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{SOURCING_URL}/products/pending-sync")
                
                if response.status_code == 200:
                    pending_products = response.json()
                    
                    for product_data in pending_products.get('products', []):
                        await self._sync_product_to_medusa(product_data)
                        
        except Exception as e:
            logger.error(f"Failed to sync sourced products: {e}")
    
    async def _sync_product_to_medusa(self, product_data: Dict[str, Any]):
        """Sync individual product to MedusaJS"""
        try:
            # Transform product data for MedusaJS format
            medusa_product = {
                "title": product_data.get("title", ""),
                "subtitle": product_data.get("subtitle", ""),
                "description": product_data.get("description", ""),
                "handle": product_data.get("handle", ""),
                "is_giftcard": False,
                "status": "draft",  # Start as draft for review
                "images": [{"url": url} for url in product_data.get("images", [])],
                "options": product_data.get("options", []),
                "variants": [{
                    "title": variant.get("title", "Default"),
                    "sku": variant.get("sku", ""),
                    "inventory_quantity": variant.get("inventory_quantity", 0),
                    "prices": [{
                        "currency_code": "usd",
                        "amount": int(variant.get("price", 0) * 100)  # Convert to cents
                    }]
                } for variant in product_data.get("variants", [])],
                "tags": product_data.get("tags", []),
                "type": {
                    "value": product_data.get("category", "general")
                }
            }
            
            # Create product in MedusaJS
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{MEDUSA_URL}/admin/products",
                    json=medusa_product,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    medusa_product_data = response.json()
                    
                    # Update sourcing service with MedusaJS product ID
                    await client.put(
                        f"{SOURCING_URL}/products/{product_data['id']}/medusa-sync",
                        json={
                            "medusa_product_id": medusa_product_data["product"]["id"],
                            "sync_status": "completed"
                        }
                    )
                    
                    # Trigger AI enhancement if needed
                    if product_data.get("needs_ai_enhancement", False):
                        await self._trigger_ai_product_enhancement(
                            product_data['id'], 
                            medusa_product_data["product"]["id"]
                        )
                    
                    logger.info(f"Successfully synced product {product_data['id']} to MedusaJS")
                else:
                    logger.error(f"Failed to create product in MedusaJS: {response.text}")
                    
        except Exception as e:
            logger.error(f"Failed to sync product to MedusaJS: {e}")
    
    async def _sync_orders_to_crm(self):
        """Sync new orders from MedusaJS to CRM service"""
        try:
            # Get recent orders from MedusaJS
            async with httpx.AsyncClient() as client:
                # Get orders from last 2 hours
                since_date = (datetime.utcnow() - timedelta(hours=2)).isoformat()
                
                response = await client.get(
                    f"{MEDUSA_URL}/admin/orders",
                    params={"created_at[gte]": since_date}
                )
                
                if response.status_code == 200:
                    orders_data = response.json()
                    
                    for order in orders_data.get('orders', []):
                        await self._sync_order_to_crm(order)
                        
        except Exception as e:
            logger.error(f"Failed to sync orders to CRM: {e}")
    
    async def _sync_order_to_crm(self, order_data: Dict[str, Any]):
        """Sync individual order to CRM service"""
        try:
            # Transform order data for CRM
            crm_order = {
                "order_id": order_data["id"],
                "customer_email": order_data.get("email", ""),
                "customer_name": f"{order_data.get('billing_address', {}).get('first_name', '')} {order_data.get('billing_address', {}).get('last_name', '')}".strip(),
                "order_total": order_data.get("total", 0) / 100,  # Convert from cents
                "order_status": order_data.get("status", "pending"),
                "order_date": order_data.get("created_at", ""),
                "shipping_address": order_data.get("shipping_address", {}),
                "billing_address": order_data.get("billing_address", {}),
                "items": [{
                    "product_id": item.get("variant", {}).get("product_id", ""),
                    "variant_id": item.get("variant_id", ""),
                    "title": item.get("title", ""),
                    "quantity": item.get("quantity", 0),
                    "price": item.get("unit_price", 0) / 100  # Convert from cents
                } for item in order_data.get("items", [])],
                "source": "coreldove_storefront"
            }
            
            # Create lead/customer in CRM
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{CRM_URL}/orders/import",
                    json=crm_order,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    # Trigger marketing automation for new customer
                    await self._trigger_customer_marketing(order_data)
                    logger.info(f"Successfully synced order {order_data['id']} to CRM")
                else:
                    logger.error(f"Failed to sync order to CRM: {response.text}")
                    
        except Exception as e:
            logger.error(f"Failed to sync order to CRM: {e}")
    
    async def _sync_customer_data(self):
        """Sync customer data between services"""
        try:
            # Get updated customer profiles from CRM
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{CRM_URL}/customers/updated")
                
                if response.status_code == 200:
                    customers = response.json().get('customers', [])
                    
                    for customer in customers:
                        # Update customer data in MedusaJS
                        await self._update_medusa_customer(customer)
                        
        except Exception as e:
            logger.error(f"Failed to sync customer data: {e}")
    
    async def _update_medusa_customer(self, customer_data: Dict[str, Any]):
        """Update customer information in MedusaJS"""
        try:
            async with httpx.AsyncClient() as client:
                # Find customer in MedusaJS by email
                response = await client.get(
                    f"{MEDUSA_URL}/admin/customers",
                    params={"email": customer_data.get("email", "")}
                )
                
                if response.status_code == 200:
                    customers = response.json().get('customers', [])
                    
                    if customers:
                        customer_id = customers[0]["id"]
                        
                        # Update customer data
                        update_data = {
                            "first_name": customer_data.get("first_name", ""),
                            "last_name": customer_data.get("last_name", ""),
                            "phone": customer_data.get("phone", ""),
                            "metadata": {
                                "crm_customer_id": customer_data.get("id"),
                                "lead_score": customer_data.get("lead_score", 0),
                                "customer_segment": customer_data.get("segment", "general")
                            }
                        }
                        
                        await client.post(
                            f"{MEDUSA_URL}/admin/customers/{customer_id}",
                            json=update_data
                        )
                        
                        logger.debug(f"Updated customer {customer_id} in MedusaJS")
                        
        except Exception as e:
            logger.error(f"Failed to update MedusaJS customer: {e}")
    
    async def _update_analytics(self):
        """Update analytics and performance metrics"""
        try:
            # Collect metrics from all services
            metrics = await self._collect_service_metrics()
            
            # Store aggregated metrics
            await self._store_analytics_data(metrics)
            
        except Exception as e:
            logger.error(f"Failed to update analytics: {e}")
    
    async def _collect_service_metrics(self) -> Dict[str, Any]:
        """Collect metrics from all CoreLDove services"""
        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "services": {}
        }
        
        services = [
            ("sourcing", SOURCING_URL),
            ("crm", CRM_URL),
            ("medusa", MEDUSA_URL)
        ]
        
        for service_name, service_url in services:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{service_url}/metrics", timeout=5.0)
                    
                    if response.status_code == 200:
                        metrics["services"][service_name] = response.json()
                    else:
                        metrics["services"][service_name] = {"status": "error", "code": response.status_code}
                        
            except Exception as e:
                metrics["services"][service_name] = {"status": "error", "message": str(e)}
        
        return metrics
    
    async def _store_analytics_data(self, metrics: Dict[str, Any]):
        """Store analytics data in Redis"""
        try:
            # Store latest metrics
            await self.bizosaas_redis.setex(
                "coreldove:metrics:latest",
                3600,  # 1 hour expiration
                json.dumps(metrics, default=str)
            )
            
            # Store in time series for trends
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M")
            await self.bizosaas_redis.setex(
                f"coreldove:metrics:timeseries:{timestamp}",
                86400,  # 24 hour expiration
                json.dumps(metrics, default=str)
            )
            
        except Exception as e:
            logger.error(f"Failed to store analytics data: {e}")
    
    async def _trigger_ai_product_enhancement(self, sourcing_id: str, medusa_id: str):
        """Trigger AI enhancement for product"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{AI_AGENTS_URL}/agents/enhance-product",
                    json={
                        "sourcing_product_id": sourcing_id,
                        "medusa_product_id": medusa_id,
                        "enhancement_type": "full"
                    }
                )
                
                if response.status_code == 200:
                    logger.info(f"Triggered AI enhancement for product {sourcing_id}")
                    
        except Exception as e:
            logger.error(f"Failed to trigger AI enhancement: {e}")
    
    async def _trigger_customer_marketing(self, order_data: Dict[str, Any]):
        """Trigger marketing automation for new customer"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{MARKETING_URL}/campaigns/trigger/new-customer",
                    json={
                        "customer_email": order_data.get("email", ""),
                        "order_value": order_data.get("total", 0) / 100,
                        "products_purchased": [item.get("title", "") for item in order_data.get("items", [])],
                        "source": "coreldove"
                    }
                )
                
                if response.status_code == 200:
                    logger.info(f"Triggered marketing automation for customer {order_data.get('email', '')}")
                    
        except Exception as e:
            logger.error(f"Failed to trigger marketing automation: {e}")

# Global sync manager
sync_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    global bizosaas_redis, coreldove_redis, sync_manager
    
    # Initialize Redis connections
    bizosaas_redis = redis.Redis(
        host="host.docker.internal",
        port=6379,
        decode_responses=False,
        health_check_interval=30
    )
    
    coreldove_redis = redis.Redis(
        host="coreldove-redis",
        port=6379,
        decode_responses=False,
        health_check_interval=30
    )
    
    # Initialize database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize sync manager
    sync_manager = CoreLDoveSyncManager(SessionLocal, bizosaas_redis, coreldove_redis)
    
    # Start background sync
    sync_task = asyncio.create_task(sync_manager.start_sync_manager())
    
    logger.info("CoreLDove Bridge Service started")
    yield
    
    # Cleanup
    await sync_manager.stop_sync_manager()
    sync_task.cancel()
    try:
        await sync_task
    except asyncio.CancelledError:
        pass
    
    if bizosaas_redis:
        await bizosaas_redis.aclose()
    if coreldove_redis:
        await coreldove_redis.aclose()
    
    logger.info("CoreLDove Bridge Service stopped")

app = FastAPI(
    title="CoreLDove Data Bridge Service",
    description="Synchronizes data between CoreLDove sourcing, MedusaJS, CRM, and BizOSaaS services",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:7001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencies
async def get_db_session():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# ============ API ENDPOINTS ============

@app.post("/sync/product")
async def sync_product_manual(
    request: ProductSyncRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(get_current_user)
):
    """Manually trigger product sync"""
    try:
        if sync_manager:
            background_tasks.add_task(
                sync_manager._sync_product_to_medusa,
                request.product_data
            )
        
        return {"status": "initiated", "message": "Product sync started"}
        
    except Exception as e:
        logger.error(f"Failed to trigger product sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync/order")
async def sync_order_manual(
    request: OrderSyncRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(get_current_user)
):
    """Manually trigger order sync"""
    try:
        if sync_manager:
            order_data = {
                "id": request.order_id,
                "email": request.customer_data.get("email", ""),
                "billing_address": request.customer_data,
                "total": int(request.order_total * 100),  # Convert to cents
                "items": request.order_items,
                "created_at": datetime.utcnow().isoformat()
            }
            
            background_tasks.add_task(
                sync_manager._sync_order_to_crm,
                order_data
            )
        
        return {"status": "initiated", "message": "Order sync started"}
        
    except Exception as e:
        logger.error(f"Failed to trigger order sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sync/status")
async def get_sync_status():
    """Get sync manager status"""
    try:
        if sync_manager:
            return {
                "status": "active" if sync_manager.sync_active else "inactive",
                "sync_interval": sync_manager.sync_interval,
                "last_sync": "unknown"  # Could track this
            }
        else:
            return {"status": "not_initialized"}
            
    except Exception as e:
        logger.error(f"Failed to get sync status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_bridge_metrics():
    """Get bridge service metrics"""
    try:
        if bizosaas_redis:
            metrics_data = await bizosaas_redis.get("coreldove:metrics:latest")
            if metrics_data:
                return json.loads(metrics_data)
        
        return {"status": "no_data"}
        
    except Exception as e:
        logger.error(f"Failed to get bridge metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Redis connections
        bizosaas_redis_status = "healthy"
        coreldove_redis_status = "healthy"
        
        try:
            await bizosaas_redis.ping()
        except:
            bizosaas_redis_status = "unhealthy"
        
        try:
            await coreldove_redis.ping()
        except:
            coreldove_redis_status = "unhealthy"
        
        return {
            "status": "healthy",
            "service": "coreldove-bridge",
            "sync_manager": "active" if sync_manager and sync_manager.sync_active else "inactive",
            "redis_connections": {
                "bizosaas": bizosaas_redis_status,
                "coreldove": coreldove_redis_status
            },
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8015)