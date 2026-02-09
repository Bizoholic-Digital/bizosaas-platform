"""
CoreLDove Bridge Service for Saleor Integration
Handles data synchronization between Saleor GraphQL API and BizOSaaS ecosystem
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

import httpx
import structlog
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from pydantic import BaseModel, Field
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Configuration
SALEOR_API_URL = os.getenv("SALEOR_API_URL", "http://saleor-api:8000/graphql/")
SALEOR_API_TOKEN = os.getenv("SALEOR_API_TOKEN", "")
BIZOSAAS_API_URL = os.getenv("BIZOSAAS_API_URL", "http://host.docker.internal:8000")
AI_AGENTS_URL = os.getenv("AI_AGENTS_URL", "http://host.docker.internal:8000")
REDIS_HOST = os.getenv("REDIS_HOST", "host.docker.internal")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CORELDOVE_REDIS_HOST = os.getenv("CORELDOVE_REDIS_HOST", "coreldove-redis")
CORELDOVE_REDIS_PORT = int(os.getenv("CORELDOVE_REDIS_PORT", "6379"))

# Database configuration
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER', 'admin')}:{os.getenv('POSTGRES_PASSWORD', 'securepassword')}@{os.getenv('POSTGRES_HOST', 'host.docker.internal')}:5432/{os.getenv('POSTGRES_DB', 'bizosaas')}"

# Initialize FastAPI app
app = FastAPI(
    title="CoreLDove Bridge Service",
    description="Integration layer between Saleor GraphQL API and BizOSaaS ecosystem",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global clients
saleor_client: Optional[Client] = None
redis_client: Optional[redis.Redis] = None
coreldove_redis_client: Optional[redis.Redis] = None
http_client: Optional[httpx.AsyncClient] = None
db_engine = None
async_session = None

# Pydantic models
class ProductSourceRequest(BaseModel):
    """Request model for product sourcing from external APIs"""
    source_url: str
    source_type: str = "amazon"
    tenant_id: str
    user_id: str
    ai_enhance: bool = True

class SaleorProductCreate(BaseModel):
    """Model for creating products in Saleor"""
    name: str
    description: str
    category_id: Optional[str] = None
    product_type_id: Optional[str] = None
    weight: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = {}
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None

class BizOSaaSProduct(BaseModel):
    """Model for BizOSaaS product data"""
    tenant_id: str
    external_id: str
    source_data: Dict[str, Any]
    ai_analysis: Optional[Dict[str, Any]] = {}
    saleor_product_id: Optional[str] = None
    sync_status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)

# GraphQL Queries and Mutations
SALEOR_PRODUCT_CREATE_MUTATION = gql("""
    mutation ProductCreate($input: ProductCreateInput!) {
        productCreate(input: $input) {
            product {
                id
                name
                slug
                description
                seoTitle
                seoDescription
                category {
                    id
                    name
                }
                productType {
                    id
                    name
                }
                metadata {
                    key
                    value
                }
            }
            errors {
                field
                message
                code
            }
        }
    }
""")

SALEOR_PRODUCTS_QUERY = gql("""
    query GetProducts($first: Int, $after: String, $filter: ProductFilterInput) {
        products(first: $first, after: $after, filter: $filter) {
            edges {
                node {
                    id
                    name
                    slug
                    description
                    seoTitle
                    seoDescription
                    created
                    updatedAt
                    category {
                        id
                        name
                    }
                    productType {
                        id
                        name
                    }
                    variants {
                        id
                        name
                        sku
                        pricing {
                            priceUndiscounted {
                                gross {
                                    amount
                                    currency
                                }
                            }
                        }
                    }
                    metadata {
                        key
                        value
                    }
                }
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
""")

SALEOR_CATEGORIES_QUERY = gql("""
    query GetCategories {
        categories(first: 100) {
            edges {
                node {
                    id
                    name
                    slug
                    description
                    parent {
                        id
                        name
                    }
                }
            }
        }
    }
""")

@app.on_event("startup")
async def startup_event():
    """Initialize connections and services"""
    global saleor_client, redis_client, coreldove_redis_client, http_client, db_engine, async_session
    
    try:
        # Initialize Saleor GraphQL client
        headers = {}
        if SALEOR_API_TOKEN:
            headers["Authorization"] = f"Bearer {SALEOR_API_TOKEN}"
        
        transport = AIOHTTPTransport(url=SALEOR_API_URL, headers=headers)
        saleor_client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Initialize Redis clients
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        coreldove_redis_client = redis.Redis(host=CORELDOVE_REDIS_HOST, port=CORELDOVE_REDIS_PORT, decode_responses=True)
        
        # Initialize HTTP client
        http_client = httpx.AsyncClient(timeout=30.0)
        
        # Initialize database
        db_engine = create_async_engine(DATABASE_URL, echo=False)
        async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
        
        logger.info("CoreLDove Bridge Service started successfully")
        
    except Exception as e:
        logger.error("Failed to initialize services", error=str(e))
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup connections"""
    global saleor_client, redis_client, coreldove_redis_client, http_client, db_engine
    
    try:
        if saleor_client:
            await saleor_client.close_async()
        if redis_client:
            await redis_client.close()
        if coreldove_redis_client:
            await coreldove_redis_client.close()
        if http_client:
            await http_client.aclose()
        if db_engine:
            await db_engine.dispose()
            
        logger.info("CoreLDove Bridge Service shutdown completed")
        
    except Exception as e:
        logger.error("Error during shutdown", error=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Saleor connection
        saleor_healthy = False
        if saleor_client:
            try:
                # Simple query to test connection
                result = await saleor_client.execute_async(SALEOR_CATEGORIES_QUERY)
                saleor_healthy = bool(result.get("categories"))
            except Exception:
                pass
        
        # Test Redis connections
        redis_healthy = False
        coreldove_redis_healthy = False
        
        if redis_client:
            try:
                await redis_client.ping()
                redis_healthy = True
            except Exception:
                pass
        
        if coreldove_redis_client:
            try:
                await coreldove_redis_client.ping()
                coreldove_redis_healthy = True
            except Exception:
                pass
        
        return {
            "status": "healthy" if all([saleor_healthy, redis_healthy, coreldove_redis_healthy]) else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "saleor": "healthy" if saleor_healthy else "unhealthy",
                "redis": "healthy" if redis_healthy else "unhealthy",
                "coreldove_redis": "healthy" if coreldove_redis_healthy else "unhealthy"
            }
        }
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=500, detail="Health check failed")

# Product sourcing and creation workflow
@app.post("/api/products/source-and-create")
async def source_and_create_product(request: ProductSourceRequest, background_tasks: BackgroundTasks):
    """
    Source product data from external APIs, enhance with AI, and create in Saleor
    """
    try:
        logger.info("Starting product sourcing and creation", 
                   source_url=request.source_url, 
                   tenant_id=request.tenant_id)
        
        # Step 1: Call sourcing service
        sourcing_response = await http_client.post(
            f"{os.getenv('SOURCING_URL', 'http://coreldove-sourcing:8010')}/api/source/product",
            json={
                "url": request.source_url,
                "source_type": request.source_type,
                "tenant_id": request.tenant_id,
                "user_id": request.user_id
            }
        )
        
        if sourcing_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to source product data")
        
        sourced_data = sourcing_response.json()
        
        # Step 2: AI enhancement (if requested)
        ai_analysis = {}
        if request.ai_enhance:
            ai_response = await http_client.post(
                f"{AI_AGENTS_URL}/agents/product-optimization",
                json={
                    "product_data": sourced_data,
                    "tenant_id": request.tenant_id,
                    "optimization_type": "seo_content_pricing"
                }
            )
            
            if ai_response.status_code == 200:
                ai_analysis = ai_response.json()
        
        # Step 3: Create product in Saleor
        saleor_input = {
            "name": ai_analysis.get("optimized_title", sourced_data.get("title", "")),
            "description": ai_analysis.get("optimized_description", sourced_data.get("description", "")),
            "seo": {
                "title": ai_analysis.get("seo_title"),
                "description": ai_analysis.get("seo_description")
            },
            "metadata": [
                {"key": "source_url", "value": request.source_url},
                {"key": "source_type", "value": request.source_type},
                {"key": "tenant_id", "value": request.tenant_id},
                {"key": "ai_enhanced", "value": str(request.ai_enhance)},
                {"key": "external_id", "value": sourced_data.get("id", "")},
            ]
        }
        
        # Add category if AI suggested one
        if ai_analysis.get("suggested_category_id"):
            saleor_input["category"] = ai_analysis["suggested_category_id"]
        
        # Create product in Saleor
        result = await saleor_client.execute_async(SALEOR_PRODUCT_CREATE_MUTATION, 
                                                  variable_values={"input": saleor_input})
        
        if result["productCreate"]["errors"]:
            raise HTTPException(status_code=400, 
                              detail=f"Saleor product creation failed: {result['productCreate']['errors']}")
        
        saleor_product = result["productCreate"]["product"]
        
        # Step 4: Store in BizOSaaS database and cache
        product_record = BizOSaaSProduct(
            tenant_id=request.tenant_id,
            external_id=sourced_data.get("id", ""),
            source_data=sourced_data,
            ai_analysis=ai_analysis,
            saleor_product_id=saleor_product["id"],
            sync_status="completed"
        )
        
        # Cache the product data
        cache_key = f"coreldove:product:{request.tenant_id}:{saleor_product['id']}"
        await coreldove_redis_client.setex(
            cache_key, 
            3600,  # 1 hour TTL
            json.dumps({
                "saleor_product": saleor_product,
                "bizosaas_data": product_record.dict(),
                "sourced_data": sourced_data,
                "ai_analysis": ai_analysis
            })
        )
        
        # Step 5: Trigger marketing automation (background task)
        background_tasks.add_task(
            trigger_marketing_automation,
            saleor_product["id"],
            request.tenant_id,
            ai_analysis
        )
        
        logger.info("Product created successfully", 
                   saleor_id=saleor_product["id"],
                   tenant_id=request.tenant_id)
        
        return {
            "success": True,
            "saleor_product": saleor_product,
            "source_data": sourced_data,
            "ai_analysis": ai_analysis,
            "message": "Product sourced, enhanced, and created successfully"
        }
        
    except Exception as e:
        logger.error("Product creation workflow failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

async def trigger_marketing_automation(saleor_product_id: str, tenant_id: str, ai_analysis: Dict[str, Any]):
    """
    Background task to trigger marketing automation for new products
    """
    try:
        # Notify marketing service about new product
        await http_client.post(
            f"{os.getenv('MARKETING_URL', 'http://host.docker.internal:8020')}/api/campaigns/product-launch",
            json={
                "product_id": saleor_product_id,
                "tenant_id": tenant_id,
                "ai_insights": ai_analysis,
                "automation_type": "product_launch"
            }
        )
        
        logger.info("Marketing automation triggered", 
                   product_id=saleor_product_id,
                   tenant_id=tenant_id)
        
    except Exception as e:
        logger.error("Failed to trigger marketing automation", 
                    error=str(e),
                    product_id=saleor_product_id)

# Saleor GraphQL proxy endpoints
@app.get("/api/saleor/products")
async def get_saleor_products(
    first: int = 20,
    after: Optional[str] = None,
    tenant_id: Optional[str] = None
):
    """
    Get products from Saleor with optional tenant filtering
    """
    try:
        variables = {"first": first}
        if after:
            variables["after"] = after
        
        # Add tenant filter if provided
        if tenant_id:
            variables["filter"] = {
                "metadata": [{"key": "tenant_id", "value": tenant_id}]
            }
        
        result = await saleor_client.execute_async(SALEOR_PRODUCTS_QUERY, 
                                                  variable_values=variables)
        
        return result["products"]
        
    except Exception as e:
        logger.error("Failed to fetch Saleor products", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/saleor/categories")
async def get_saleor_categories():
    """
    Get all product categories from Saleor
    """
    try:
        result = await saleor_client.execute_async(SALEOR_CATEGORIES_QUERY)
        return result["categories"]
        
    except Exception as e:
        logger.error("Failed to fetch Saleor categories", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Synchronization endpoints
@app.post("/api/sync/full")
async def trigger_full_sync(tenant_id: str, background_tasks: BackgroundTasks):
    """
    Trigger a full synchronization between Saleor and BizOSaaS
    """
    background_tasks.add_task(perform_full_sync, tenant_id)
    
    return {
        "message": "Full synchronization started",
        "tenant_id": tenant_id,
        "status": "initiated"
    }

async def perform_full_sync(tenant_id: str):
    """
    Background task to perform full data synchronization
    """
    try:
        logger.info("Starting full synchronization", tenant_id=tenant_id)
        
        # Sync products from Saleor to BizOSaaS cache
        products = await get_saleor_products(first=1000, tenant_id=tenant_id)
        
        for edge in products["edges"]:
            product = edge["node"]
            cache_key = f"coreldove:product:{tenant_id}:{product['id']}"
            
            await coreldove_redis_client.setex(
                cache_key,
                3600,  # 1 hour TTL
                json.dumps({
                    "saleor_product": product,
                    "last_sync": datetime.utcnow().isoformat()
                })
            )
        
        logger.info("Full synchronization completed", 
                   tenant_id=tenant_id,
                   products_synced=len(products["edges"]))
        
    except Exception as e:
        logger.error("Full synchronization failed", 
                    error=str(e),
                    tenant_id=tenant_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8021)