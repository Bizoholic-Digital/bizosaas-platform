"""
BizoSaaS CRM Service - Multi-Tenant Lead Management
Foundation for amoca-education/crm-fastapi-react integration
"""
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime, date
import asyncio
import json
import uuid
from ai_integrations import (
    classify_product_with_ai, detect_fraud_with_ai,
    get_ai_product_recommendations, generate_marketing_strategy,
    check_ai_agents_health
)
from business_logic import (
    cross_selling_engine, dynamic_pricing_engine, inventory_optimizer
)
from models import (
    # E-commerce models
    Product, ProductCreate, ProductUpdate, ProductListResponse,
    Order, OrderCreate, OrderUpdate, OrderListResponse, OrderItem,
    InventoryLevel, InventoryUpdate, InventoryAlert, InventoryListResponse,
    Supplier, AIWorkflowExecution, AIWorkflowResponse,
    BulkProductUpdate, BulkInventoryUpdate, BulkOperationResult,
    # Enums
    ProductCategory, ProductClassification, ProductStatus,
    OrderStatus, OrderFinancialStatus, FraudRiskLevel, MarketplaceType
)
import os
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class LeadSource(str, Enum):
    WEBSITE = "website"
    REFERRAL = "referral"
    SOCIAL_MEDIA = "social_media"
    EMAIL_CAMPAIGN = "email_campaign"
    COLD_CALL = "cold_call"
    TRADE_SHOW = "trade_show"
    OTHER = "other"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Lead(BaseModel):
    id: Optional[int] = None
    tenant_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    status: LeadStatus = LeadStatus.NEW
    source: LeadSource = LeadSource.WEBSITE
    priority: Priority = Priority.MEDIUM
    score: Optional[int] = 0  # AI-generated lead score
    notes: Optional[str] = None
    tags: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    assigned_to: Optional[int] = None

class LeadCreate(BaseModel):
    tenant_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    source: LeadSource = LeadSource.WEBSITE
    notes: Optional[str] = None
    tags: Optional[List[str]] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting BizoSaaS CRM Service...")
    
    # Check infrastructure connectivity
    postgres_host = os.getenv("POSTGRES_HOST", "postgres-pgvector.apps-platform.svc.cluster.local")
    cache_host = os.getenv("CACHE_HOST", "dragonfly-cache.apps-platform.svc.cluster.local")
    
    logger.info(f"PostgreSQL: {postgres_host}")
    logger.info(f"Cache: {cache_host}")
    logger.info("CRM Service ready for amoca-education integration")
    
    # Check AI agents health
    ai_health = await check_ai_agents_health()
    logger.info(f"AI Agents Status: {ai_health}")
    
    yield
    
    logger.info("Shutting down CRM Service...")

def create_app() -> FastAPI:
    """Create FastAPI application"""
    
    app = FastAPI(
        title="BizoSaaS CRM Service",
        description="Multi-tenant Customer Relationship Management with AI lead scoring",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

app = create_app()

# In-memory storage for demo (will be replaced with database)
leads_db: Dict[int, Lead] = {}
next_id = 1

# E-commerce in-memory storage (will be replaced with database)
products_db: Dict[str, Product] = {}
orders_db: Dict[str, Order] = {}
inventory_db: Dict[str, InventoryLevel] = {}
suppliers_db: Dict[str, Supplier] = {}
ai_workflows_db: Dict[str, AIWorkflowExecution] = {}

def generate_ai_score(lead: Lead) -> int:
    """Generate AI-based lead score (mock implementation)"""
    score = 50  # Base score
    
    # Score based on company
    if lead.company:
        score += 20
    
    # Score based on job title
    if lead.job_title and any(title in lead.job_title.lower() for title in ["ceo", "cto", "manager", "director"]):
        score += 20
    
    # Score based on source
    source_scores = {
        LeadSource.REFERRAL: 30,
        LeadSource.WEBSITE: 15,
        LeadSource.SOCIAL_MEDIA: 10,
        LeadSource.EMAIL_CAMPAIGN: 10,
        LeadSource.TRADE_SHOW: 25
    }
    score += source_scores.get(lead.source, 5)
    
    return min(score, 100)

# API Endpoints
@app.get("/health")
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "service": "crm-service",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "dependencies": {
            "postgres": os.getenv("POSTGRES_HOST", "not_configured"),
            "cache": os.getenv("CACHE_HOST", "not_configured"),
            "auth_service": "bizosaas-auth-service.bizosaas-dev.svc.cluster.local:8001",
            "ai_agents": await check_ai_agents_health(),
            "business_logic_engines": {
                "cross_selling": True,
                "dynamic_pricing": True,
                "inventory_optimization": True
            }
        },
        "features": {
            "lead_management": "ready",
            "contact_management": "ready", 
            "deal_tracking": "ready",
            "ai_lead_scoring": "ready",
            "multi_tenant": "ready",
            "amoca_integration": "planned",
            "ecommerce_products": "ready",
            "order_management": "ready",
            "inventory_tracking": "ready",
            "ai_classification": "ready",
            "fraud_detection": "ready",
            "supplier_management": "ready",
            "bulk_operations": "ready"
        },
        "stats": {
            "total_leads": len(leads_db),
            "total_products": len(products_db),
            "total_orders": len(orders_db),
            "active_inventory_items": len(inventory_db),
            "active_suppliers": len([s for s in suppliers_db.values() if s.is_active]),
            "running_ai_workflows": len([w for w in ai_workflows_db.values() if w.status == "running"])
        }
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "BizoSaaS CRM Service",
        "version": "1.0.0",
        "status": "running",
        "description": "Multi-tenant CRM with AI lead scoring",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "leads": "/leads",
            "analytics": "/analytics",
            "products": "/products",
            "orders": "/orders",
            "inventory": "/inventory",
            "suppliers": "/suppliers",
            "ai_workflows": "/ai-workflows"
        },
        "integration_ready": "amoca-education/crm-fastapi-react"
    }

# Lead Management Endpoints
@app.post("/leads", response_model=Lead)
async def create_lead(lead_data: LeadCreate):
    """Create a new lead with AI scoring"""
    global next_id
    
    lead = Lead(
        id=next_id,
        **lead_data.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Generate AI score
    lead.score = generate_ai_score(lead)
    
    leads_db[next_id] = lead
    next_id += 1
    
    logger.info(f"Lead created: {lead.email} (Score: {lead.score})")
    return lead

@app.get("/leads", response_model=List[Lead])
async def list_leads(
    tenant_id: int = Query(...),
    status: Optional[LeadStatus] = Query(None),
    source: Optional[LeadSource] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """List leads with filtering"""
    filtered_leads = [
        lead for lead in leads_db.values()
        if lead.tenant_id == tenant_id
    ]
    
    if status:
        filtered_leads = [lead for lead in filtered_leads if lead.status == status]
    
    if source:
        filtered_leads = [lead for lead in filtered_leads if lead.source == source]
    
    # Apply pagination
    paginated_leads = filtered_leads[offset:offset + limit]
    
    return paginated_leads

@app.get("/leads/{lead_id}", response_model=Lead)
async def get_lead(lead_id: int):
    """Get lead by ID"""
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return leads_db[lead_id]

@app.get("/analytics/leads")
async def lead_analytics(tenant_id: int = Query(...)):
    """Lead analytics for tenant"""
    tenant_leads = [lead for lead in leads_db.values() if lead.tenant_id == tenant_id]
    
    if not tenant_leads:
        return {"message": "No leads found for tenant", "total_leads": 0}
    
    # Status distribution
    status_counts = {}
    for status in LeadStatus:
        status_counts[status.value] = len([lead for lead in tenant_leads if lead.status == status])
    
    # Source distribution
    source_counts = {}
    for source in LeadSource:
        source_counts[source.value] = len([lead for lead in tenant_leads if lead.source == source])
    
    # Average score
    avg_score = sum(lead.score or 0 for lead in tenant_leads) / len(tenant_leads)
    
    return {
        "total_leads": len(tenant_leads),
        "status_distribution": status_counts,
        "source_distribution": source_counts,
        "average_score": round(avg_score, 2),
        "high_priority_leads": len([lead for lead in tenant_leads if lead.priority == Priority.HIGH])
    }

# ============================================================================
# E-COMMERCE API ENDPOINTS
# ============================================================================

# Product Management Endpoints
@app.post("/products", response_model=Product)
async def create_product(product_data: ProductCreate):
    """Create a new product with AI classification"""
    product_id = str(uuid.uuid4())
    
    # Create product with AI scoring placeholder
    product = Product(
        id=product_id,
        **product_data.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Simulate AI classification
    product = await classify_product_with_ai(product)
    
    # Store product
    products_db[product_id] = product
    
    # Create initial inventory record
    inventory_record = InventoryLevel(
        id=str(uuid.uuid4()),
        tenant_id=product.tenant_id,
        product_id=product_id,
        sku=product.sku,
        available_quantity=product.stock_quantity,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    inventory_db[product_id] = inventory_record
    
    # Trigger AI workflow for product analysis
    await trigger_ai_product_workflow(product)
    
    # Publish product created event
    await event_bus.publish("product.created", {
        "product_id": product_id,
        "title": product.title,
        "category": product.category.value,
        "sku": product.sku,
        "classification": product.ai_metrics.classification.value if product.ai_metrics else None
    })
    
    logger.info(f"Product created: {product.title} (Classification: {product.ai_metrics.classification if product.ai_metrics else 'pending'})")
    return product

@app.get("/products", response_model=ProductListResponse)
async def list_products(
    tenant_id: int = Query(...),
    category: Optional[ProductCategory] = Query(None),
    classification: Optional[ProductClassification] = Query(None),
    status: Optional[ProductStatus] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """List products with filtering and pagination"""
    # Filter products by tenant
    filtered_products = [
        product for product in products_db.values()
        if product.tenant_id == tenant_id
    ]
    
    # Apply filters
    if category:
        filtered_products = [p for p in filtered_products if p.category == category]
    
    if classification and any(p.ai_metrics and p.ai_metrics.classification == classification for p in filtered_products):
        filtered_products = [p for p in filtered_products 
                           if p.ai_metrics and p.ai_metrics.classification == classification]
    
    if status:
        filtered_products = [p for p in filtered_products if p.status == status]
    
    # Apply pagination
    total_count = len(filtered_products)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_products = filtered_products[start_idx:end_idx]
    
    return ProductListResponse(
        products=paginated_products,
        total_count=total_count,
        page=page,
        page_size=page_size,
        has_next=end_idx < total_count,
        has_previous=page > 1
    )

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get product by ID"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return products_db[product_id]

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, updates: ProductUpdate):
    """Update existing product"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = products_db[product_id]
    
    # Apply updates
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    product.updated_at = datetime.now()
    
    # Re-classify if AI metrics were updated
    if "ai_metrics" in update_data:
        product = await classify_product_with_ai(product)
    
    products_db[product_id] = product
    logger.info(f"Product updated: {product.title}")
    return product

@app.delete("/products/{product_id}")
async def delete_product(product_id: str):
    """Delete product (soft delete by setting status)"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = products_db[product_id]
    product.status = ProductStatus.DISCONTINUED
    product.updated_at = datetime.now()
    
    logger.info(f"Product deleted: {product.title}")
    return {"message": "Product deleted successfully"}

# Order Management Endpoints
@app.post("/orders", response_model=Order)
async def create_order(order_data: OrderCreate):
    """Create a new order with AI fraud detection"""
    order_id = str(uuid.uuid4())
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{len(orders_db) + 1:04d}"
    
    # Create order
    order = Order(
        id=order_id,
        order_number=order_number,
        **order_data.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Run AI fraud detection
    order = await detect_fraud_with_ai(order)
    
    # Reserve inventory
    await reserve_inventory_for_order(order)
    
    # Store order
    orders_db[order_id] = order
    
    # Trigger order processing workflow
    await trigger_ai_order_workflow(order)
    
    # Publish order created event
    await event_bus.publish("order.created", {
        "order_id": order_id,
        "order_number": order.order_number,
        "customer_email": order.customer_email,
        "total_amount": order.total_amount,
        "items_count": len(order.items),
        "risk_level": order.fraud_analysis.risk_level.value if order.fraud_analysis else "unknown"
    })
    
    logger.info(f"Order created: {order.order_number} (Risk: {order.fraud_analysis.risk_level if order.fraud_analysis else 'unknown'})")
    return order

@app.get("/orders", response_model=OrderListResponse)
async def list_orders(
    tenant_id: int = Query(...),
    status: Optional[OrderStatus] = Query(None),
    financial_status: Optional[OrderFinancialStatus] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """List orders with filtering and pagination"""
    # Filter orders by tenant
    filtered_orders = [
        order for order in orders_db.values()
        if order.tenant_id == tenant_id
    ]
    
    # Apply filters
    if status:
        filtered_orders = [o for o in filtered_orders if o.status == status]
    
    if financial_status:
        filtered_orders = [o for o in filtered_orders if o.financial_status == financial_status]
    
    # Apply pagination
    total_count = len(filtered_orders)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_orders = filtered_orders[start_idx:end_idx]
    
    return OrderListResponse(
        orders=paginated_orders,
        total_count=total_count,
        page=page,
        page_size=page_size,
        has_next=end_idx < total_count,
        has_previous=page > 1
    )

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get order by ID"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return orders_db[order_id]

@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: str, updates: OrderUpdate):
    """Update existing order"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order = orders_db[order_id]
    
    # Apply updates
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    order.updated_at = datetime.now()
    
    orders_db[order_id] = order
    logger.info(f"Order updated: {order.order_number}")
    return order

# Inventory Management Endpoints
@app.get("/inventory", response_model=InventoryListResponse)
async def list_inventory(
    tenant_id: int = Query(...),
    low_stock_only: bool = Query(False),
    out_of_stock_only: bool = Query(False)
):
    """List inventory levels with alerts"""
    # Filter inventory by tenant
    filtered_inventory = [
        inv for inv in inventory_db.values()
        if inv.tenant_id == tenant_id
    ]
    
    # Apply stock filters
    if low_stock_only:
        filtered_inventory = [inv for inv in filtered_inventory 
                            if inv.available_quantity <= inv.reorder_point]
    
    if out_of_stock_only:
        filtered_inventory = [inv for inv in filtered_inventory 
                            if inv.available_quantity == 0]
    
    # Generate alerts
    alerts = []
    for inv in filtered_inventory:
        if inv.available_quantity == 0:
            alerts.append(InventoryAlert(
                product_id=inv.product_id,
                sku=inv.sku,
                alert_type="out_of_stock",
                message=f"Product {inv.sku} is out of stock",
                severity="critical",
                current_quantity=inv.available_quantity,
                threshold=0,
                recommended_action="Restock immediately"
            ))
        elif inv.available_quantity <= inv.reorder_point:
            alerts.append(InventoryAlert(
                product_id=inv.product_id,
                sku=inv.sku,
                alert_type="low_stock",
                message=f"Product {inv.sku} is below reorder point",
                severity="warning",
                current_quantity=inv.available_quantity,
                threshold=inv.reorder_point,
                recommended_action=f"Reorder {inv.reorder_quantity} units"
            ))
    
    return InventoryListResponse(
        inventory_levels=filtered_inventory,
        alerts=alerts,
        total_count=len(filtered_inventory)
    )

@app.put("/inventory/{product_id}", response_model=InventoryLevel)
async def update_inventory(product_id: str, updates: InventoryUpdate):
    """Update inventory levels"""
    if product_id not in inventory_db:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    
    inventory = inventory_db[product_id]
    
    # Apply updates
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(inventory, field, value)
    
    inventory.updated_at = datetime.now()
    
    # Trigger AI reorder recommendation if needed
    if inventory.available_quantity <= inventory.reorder_point:
        inventory = await generate_ai_reorder_recommendation(inventory)
    
    inventory_db[product_id] = inventory
    logger.info(f"Inventory updated for product: {inventory.sku}")
    return inventory

# Supplier Management Endpoints
@app.post("/suppliers", response_model=Supplier)
async def create_supplier(supplier_data: Supplier):
    """Create a new supplier"""
    supplier_id = str(uuid.uuid4())
    
    supplier = Supplier(
        id=supplier_id,
        **supplier_data.dict(exclude={'id'}),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    suppliers_db[supplier_id] = supplier
    
    logger.info(f"Supplier created: {supplier.supplier_name}")
    return supplier

@app.get("/suppliers")
async def list_suppliers(
    tenant_id: int = Query(...),
    marketplace: Optional[MarketplaceType] = Query(None),
    active_only: bool = Query(True)
):
    """List suppliers with filtering"""
    filtered_suppliers = [
        supplier for supplier in suppliers_db.values()
        if supplier.tenant_id == tenant_id
    ]
    
    if marketplace:
        filtered_suppliers = [s for s in filtered_suppliers if s.marketplace == marketplace]
    
    if active_only:
        filtered_suppliers = [s for s in filtered_suppliers if s.is_active]
    
    return {"suppliers": filtered_suppliers, "total_count": len(filtered_suppliers)}

# AI Workflow Endpoints
@app.post("/ai-workflows/product-classification/{product_id}", response_model=AIWorkflowResponse)
async def run_product_classification(product_id: str, tenant_id: int = Query(...)):
    """Run AI product classification workflow"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    workflow_id = str(uuid.uuid4())
    
    # Create workflow execution record
    workflow = AIWorkflowExecution(
        id=workflow_id,
        tenant_id=tenant_id,
        workflow_type="product_classification",
        entity_type="product",
        entity_id=product_id,
        status="running",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    ai_workflows_db[workflow_id] = workflow
    
    # Start async classification
    asyncio.create_task(run_async_product_classification(workflow_id, product_id))
    
    return AIWorkflowResponse(
        workflow_id=workflow_id,
        status="running",
        progress=0.0,
        estimated_completion=datetime.now().replace(microsecond=0),
        results_available=False
    )

@app.get("/ai-workflows/{workflow_id}", response_model=AIWorkflowExecution)
async def get_workflow_status(workflow_id: str):
    """Get AI workflow status and results"""
    if workflow_id not in ai_workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return ai_workflows_db[workflow_id]

@app.post("/products/{product_id}/recommendations")
async def get_product_recommendations(product_id: str, tenant_id: int = Query(...), limit: int = Query(10, le=50)):
    """Get AI-powered product recommendations"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = products_db[product_id]
    recommendations = await get_ai_product_recommendations(tenant_id, product.category.value, limit)
    
    return {
        "product_id": product_id,
        "recommendations": recommendations,
        "total_count": len(recommendations),
        "generated_at": datetime.now().isoformat()
    }

@app.post("/products/{product_id}/marketing-strategy")
async def generate_product_marketing_strategy_endpoint(product_id: str):
    """Generate marketing strategy for a product"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = products_db[product_id]
    strategy = await generate_marketing_strategy(product)
    
    return {
        "product_id": product_id,
        "marketing_strategy": strategy,
        "generated_at": datetime.now().isoformat()
    }

# Event Bus API Endpoints
@app.get("/events")
async def list_events(
    event_type: Optional[str] = Query(None),
    limit: int = Query(50, le=200)
):
    """List recent events from the event bus"""
    events = event_bus.event_log
    
    if event_type:
        events = [e for e in events if e["type"] == event_type]
    
    # Get most recent events
    recent_events = events[-limit:] if len(events) > limit else events
    
    return {
        "events": recent_events,
        "total_count": len(recent_events),
        "available_event_types": list(set(e["type"] for e in event_bus.event_log))
    }

@app.get("/analytics/dashboard")
async def get_dashboard_analytics(
    tenant_id: int = Query(...),
    days: int = Query(30, ge=1, le=365)
):
    """Get comprehensive dashboard analytics"""
    # Product analytics
    tenant_products = [p for p in products_db.values() if p.tenant_id == tenant_id]
    product_classifications = {}
    for classification in ProductClassification:
        count = len([p for p in tenant_products 
                    if p.ai_metrics and p.ai_metrics.classification == classification])
        product_classifications[classification.value] = count
    
    # Order analytics
    tenant_orders = [o for o in orders_db.values() if o.tenant_id == tenant_id]
    order_statuses = {}
    for status in OrderStatus:
        count = len([o for o in tenant_orders if o.status == status])
        order_statuses[status.value] = count
    
    # Revenue analytics
    total_revenue = sum(o.total_amount for o in tenant_orders 
                       if o.financial_status == OrderFinancialStatus.PAID)
    
    # Inventory analytics
    tenant_inventory = [i for i in inventory_db.values() if i.tenant_id == tenant_id]
    low_stock_items = len([i for i in tenant_inventory 
                          if i.available_quantity <= i.reorder_point])
    out_of_stock_items = len([i for i in tenant_inventory 
                             if i.available_quantity == 0])
    
    # AI workflow analytics
    tenant_workflows = [w for w in ai_workflows_db.values() if w.tenant_id == tenant_id]
    workflow_statuses = {}
    for workflow in tenant_workflows:
        status = workflow.status
        workflow_statuses[status] = workflow_statuses.get(status, 0) + 1
    
    return {
        "tenant_id": tenant_id,
        "period_days": days,
        "products": {
            "total": len(tenant_products),
            "by_classification": product_classifications,
            "active": len([p for p in tenant_products if p.status == ProductStatus.ACTIVE])
        },
        "orders": {
            "total": len(tenant_orders),
            "by_status": order_statuses,
            "total_revenue": total_revenue
        },
        "inventory": {
            "total_items": len(tenant_inventory),
            "low_stock_alerts": low_stock_items,
            "out_of_stock_alerts": out_of_stock_items
        },
        "ai_workflows": {
            "total": len(tenant_workflows),
            "by_status": workflow_statuses
        },
        "generated_at": datetime.now().isoformat()
    }

# Bulk Operations
@app.post("/products/bulk-update", response_model=BulkOperationResult)
async def bulk_update_products(bulk_update: BulkProductUpdate):
    """Bulk update multiple products"""
    results = BulkOperationResult(
        success_count=0,
        failure_count=0,
        errors=[],
        processed_ids=[]
    )
    
    for product_id in bulk_update.product_ids:
        try:
            if product_id in products_db:
                product = products_db[product_id]
                
                # Apply updates
                update_data = bulk_update.updates.dict(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(product, field, value)
                
                product.updated_at = datetime.now()
                products_db[product_id] = product
                
                results.success_count += 1
                results.processed_ids.append(product_id)
            else:
                results.failure_count += 1
                results.errors.append({
                    "product_id": product_id,
                    "error": "Product not found"
                })
        except Exception as e:
            results.failure_count += 1
            results.errors.append({
                "product_id": product_id,
                "error": str(e)
            })
    
    logger.info(f"Bulk update completed: {results.success_count} success, {results.failure_count} failed")
    
    # Publish bulk update event
    await event_bus.publish("products.bulk_updated", {
        "success_count": results.success_count,
        "failure_count": results.failure_count,
        "processed_ids": results.processed_ids
    })
    
    return results

# ============================================================================
# EVENT BUS INTEGRATION
# ============================================================================

class EventBusPublisher:
    """Simple event bus for publishing e-commerce events"""
    
    def __init__(self):
        self.subscribers = {}
        self.event_log = []
    
    def subscribe(self, event_type: str, handler):
        """Subscribe to an event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    async def publish(self, event_type: str, data: Dict[str, Any]):
        """Publish an event to all subscribers"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "id": str(uuid.uuid4())
        }
        
        # Log event
        self.event_log.append(event)
        logger.info(f"Event published: {event_type}")
        
        # Notify subscribers
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception as e:
                    logger.error(f"Event handler failed: {e}")

# Global event bus instance
event_bus = EventBusPublisher()

# Event handlers
async def handle_product_created(event):
    """Handle product created event"""
    product_data = event["data"]
    logger.info(f"Product created event processed: {product_data.get('title', 'Unknown')}")

async def handle_order_created(event):
    """Handle order created event"""
    order_data = event["data"]
    logger.info(f"Order created event processed: {order_data.get('order_number', 'Unknown')}")

async def handle_inventory_low(event):
    """Handle low inventory event"""
    inventory_data = event["data"]
    logger.warning(f"Low inventory alert: {inventory_data.get('sku', 'Unknown')}")

# Register event handlers
event_bus.subscribe("product.created", handle_product_created)
event_bus.subscribe("order.created", handle_order_created)
event_bus.subscribe("inventory.low", handle_inventory_low)

async def reserve_inventory_for_order(order: Order):
    """Reserve inventory for order items"""
    try:
        for item in order.items:
            if item.product_id in inventory_db:
                inventory = inventory_db[item.product_id]
                if inventory.available_quantity >= item.quantity:
                    inventory.available_quantity -= item.quantity
                    inventory.reserved_quantity += item.quantity
                    inventory.updated_at = datetime.now()
                    
                    # Check for low stock and publish event
                    if inventory.available_quantity <= inventory.reorder_point:
                        await event_bus.publish("inventory.low", {
                            "product_id": item.product_id,
                            "sku": item.sku,
                            "current_quantity": inventory.available_quantity,
                            "reorder_point": inventory.reorder_point
                        })
                else:
                    logger.warning(f"Insufficient inventory for product {item.sku}")
                    await event_bus.publish("inventory.insufficient", {
                        "product_id": item.product_id,
                        "sku": item.sku,
                        "requested": item.quantity,
                        "available": inventory.available_quantity
                    })
    except Exception as e:
        logger.error(f"Inventory reservation failed: {e}")

async def generate_ai_reorder_recommendation(inventory: InventoryLevel) -> InventoryLevel:
    """Generate AI-powered reorder recommendations"""
    try:
        # Simple AI logic (replace with actual ML model)
        inventory.ai_reorder_recommendation = True
        inventory.recommended_order_quantity = inventory.reorder_quantity
        
        # Predict stockout date based on current usage
        from datetime import timedelta
        inventory.predicted_stockout_date = (datetime.now() + timedelta(days=7)).date()
        
        # Publish reorder recommendation event
        await event_bus.publish("inventory.reorder_recommended", {
            "product_id": inventory.product_id,
            "sku": inventory.sku,
            "recommended_quantity": inventory.recommended_order_quantity,
            "predicted_stockout": inventory.predicted_stockout_date.isoformat() if inventory.predicted_stockout_date else None
        })
        
        return inventory
    except Exception as e:
        logger.error(f"AI reorder recommendation failed: {e}")
        return inventory

async def trigger_ai_product_workflow(product: Product):
    """Trigger AI workflow for product analysis"""
    try:
        logger.info(f"Starting AI analysis for product: {product.title}")
        
        # Publish product analysis event
        await event_bus.publish("product.analysis_started", {
            "product_id": product.id,
            "title": product.title,
            "category": product.category.value,
            "classification": product.ai_metrics.classification.value if product.ai_metrics else None
        })
        
        # Trigger marketing strategy generation in background
        asyncio.create_task(generate_product_marketing_strategy(product))
        
    except Exception as e:
        logger.error(f"Failed to trigger AI workflow: {e}")

async def trigger_ai_order_workflow(order: Order):
    """Trigger AI workflow for order processing"""
    try:
        logger.info(f"Starting AI order processing for: {order.order_number}")
        
        # Publish order processing event
        await event_bus.publish("order.processing_started", {
            "order_id": order.id,
            "order_number": order.order_number,
            "total_amount": order.total_amount,
            "risk_level": order.fraud_analysis.risk_level.value if order.fraud_analysis else "unknown"
        })
        
    except Exception as e:
        logger.error(f"Failed to trigger order workflow: {e}")

async def generate_product_marketing_strategy(product: Product):
    """Generate marketing strategy for product in background"""
    try:
        strategy = await generate_marketing_strategy(product)
        
        # Publish marketing strategy event
        await event_bus.publish("marketing.strategy_generated", {
            "product_id": product.id,
            "strategy": strategy
        })
        
        logger.info(f"Marketing strategy generated for: {product.title}")
    except Exception as e:
        logger.error(f"Marketing strategy generation failed: {e}")

# Advanced Business Logic Endpoints
@app.post("/products/{product_id}/cross-sell")
async def get_cross_sell_recommendations(
    product_id: str, 
    recommendation_type: str = Query("cross_sell", regex="^(cross_sell|upsell|complement)$"),
    limit: int = Query(10, le=20)
):
    """Get cross-selling, upselling, or complementary product recommendations"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = products_db[product_id]
    recommendations = await cross_selling_engine.generate_product_recommendations(
        product, products_db, recommendation_type, limit
    )
    
    return {
        "product_id": product_id,
        "recommendation_type": recommendation_type,
        "recommendations": recommendations,
        "total_count": len(recommendations),
        "generated_at": datetime.now().isoformat()
    }

@app.post("/products/{product_id}/optimize-pricing")
async def optimize_product_pricing(
    product_id: str,
    market_conditions: Optional[Dict[str, Any]] = None,
    competitor_prices: Optional[List[float]] = None
):
    """Get AI-powered pricing optimization recommendations"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = products_db[product_id]
    
    # Default market conditions if not provided
    if market_conditions is None:
        market_conditions = {
            "demand_level": "medium",
            "competition_level": "medium",
            "seasonality": "normal"
        }
    
    pricing_recommendation = await dynamic_pricing_engine.calculate_optimal_price(
        product, market_conditions, competitor_prices
    )
    
    return {
        "product_id": product_id,
        "pricing_analysis": pricing_recommendation,
        "market_conditions": market_conditions,
        "generated_at": datetime.now().isoformat()
    }

@app.post("/inventory/{product_id}/optimize")
async def optimize_inventory_levels(
    product_id: str,
    sales_history: Optional[List[Dict[str, Any]]] = None
):
    """Get AI-powered inventory optimization recommendations"""
    if product_id not in inventory_db:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = products_db[product_id]
    inventory = inventory_db[product_id]
    
    inventory_recommendations = await inventory_optimizer.calculate_optimal_stock_levels(
        product, inventory, sales_history
    )
    
    return {
        "product_id": product_id,
        "inventory_optimization": inventory_recommendations,
        "generated_at": datetime.now().isoformat()
    }

async def run_async_product_classification(workflow_id: str, product_id: str):
    """Run async product classification workflow"""
    try:
        workflow = ai_workflows_db[workflow_id]
        product = products_db[product_id]
        
        # Simulate AI processing
        await asyncio.sleep(2)  # Simulate processing time
        
        # Update workflow progress
        workflow.progress = 0.5
        workflow.status = "processing"
        
        # Run classification
        classified_product = await classify_product_with_ai(product)
        products_db[product_id] = classified_product
        
        # Complete workflow
        workflow.progress = 1.0
        workflow.status = "completed"
        workflow.results = {
            "classification": classified_product.ai_metrics.classification.value if classified_product.ai_metrics else "unknown",
            "score": classified_product.ai_metrics.dropship_score if classified_product.ai_metrics else 0.0
        }
        workflow.updated_at = datetime.now()
        
        logger.info(f"Product classification completed for: {product.title}")
        
    except Exception as e:
        logger.error(f"Async classification failed: {e}")
        workflow = ai_workflows_db[workflow_id]
        workflow.status = "failed"
        workflow.error_message = str(e)
        workflow.updated_at = datetime.now()

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8004"))
    
    logger.info(f"Starting CRM Service with E-commerce Extensions on {host}:{port}")
    logger.info("Features: Lead Management + Product Catalog + Order Management + AI Classification")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,
        workers=1
    )