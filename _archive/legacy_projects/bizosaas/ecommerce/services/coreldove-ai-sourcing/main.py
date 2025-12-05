"""
CoreLDove AI-Powered Product Sourcing Service
Comprehensive dropshipping automation: Amazon sourcing → AI analysis → human approval → content generation → multi-platform publishing
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum

import httpx
import structlog
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
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
AI_AGENTS_URL = os.getenv("AI_AGENTS_URL", "http://host.docker.internal:8000")
SALEOR_BRIDGE_URL = os.getenv("SALEOR_BRIDGE_URL", "http://coreldove-bridge:8021")
MARKETING_SERVICE_URL = os.getenv("MARKETING_SERVICE_URL", "http://host.docker.internal:8020")
AMAZON_API_URL = os.getenv("AMAZON_API_URL", "http://coreldove-sourcing:8010")
REDIS_HOST = os.getenv("REDIS_HOST", "host.docker.internal")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# Database configuration
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER', 'admin')}:{os.getenv('POSTGRES_PASSWORD', 'securepassword')}@{os.getenv('POSTGRES_HOST', 'host.docker.internal')}:5432/{os.getenv('POSTGRES_DB', 'bizosaas')}"

# Initialize FastAPI app
app = FastAPI(
    title="CoreLDove AI Sourcing Service",
    description="AI-powered dropshipping automation with human-in-the-loop approval",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global clients
redis_client: Optional[redis.Redis] = None
http_client: Optional[httpx.AsyncClient] = None

# Enums and Models
class ProductCategory(str, Enum):
    SPORTS = "sports"
    FITNESS = "fitness"
    HEALTH = "health"
    WELLNESS = "wellness"
    NUTRITION = "nutrition"
    OUTDOOR = "outdoor"
    GYM_EQUIPMENT = "gym_equipment"
    YOGA = "yoga"
    RUNNING = "running"
    CYCLING = "cycling"

class ProductStatus(str, Enum):
    SOURCED = "sourced"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    CONTENT_GENERATION = "content_generation"
    READY_FOR_LISTING = "ready_for_listing"
    LISTED = "listed"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"

class SourcingRequest(BaseModel):
    categories: List[ProductCategory]
    max_products: int = Field(default=50, ge=1, le=500)
    min_rating: float = Field(default=4.0, ge=1.0, le=5.0)
    max_price_usd: Optional[float] = Field(default=None, ge=1.0)
    min_reviews: int = Field(default=100, ge=1)
    dropship_eligible_only: bool = True
    tenant_id: str
    user_id: str

class ProductInsight(BaseModel):
    product_id: str
    amazon_rating: float
    review_count: int
    seller_rating: float
    price_usd: float
    estimated_margin: float
    demand_score: float  # 0-100
    trending_score: float  # 0-100
    competition_level: str  # "low", "medium", "high"
    seasonal_factor: float
    key_features: List[str]
    pros: List[str]
    cons: List[str]
    target_audience: str
    market_potential: str

class SourcedProduct(BaseModel):
    id: str
    amazon_asin: str
    title: str
    description: str
    category: ProductCategory
    price_usd: float
    rating: float
    review_count: int
    images: List[str]
    features: List[str]
    seller_info: Dict[str, Any]
    dropship_eligible: bool
    insights: ProductInsight
    status: ProductStatus = ProductStatus.SOURCED
    tenant_id: str
    sourced_at: datetime = Field(default_factory=datetime.utcnow)

class ApprovalDecision(BaseModel):
    product_ids: List[str]
    action: str  # "approve" or "reject"
    notes: Optional[str] = None
    tenant_id: str
    user_id: str

class CategoryFilter(BaseModel):
    categories: List[ProductCategory]
    tenant_id: str

@app.on_event("startup")
async def startup_event():
    global redis_client, http_client
    
    try:
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        http_client = httpx.AsyncClient(timeout=60.0)
        logger.info("CoreLDove AI Sourcing Service started successfully")
    except Exception as e:
        logger.error("Failed to initialize services", error=str(e))
        raise

@app.on_event("shutdown")
async def shutdown_event():
    global redis_client, http_client
    
    try:
        if redis_client:
            await redis_client.close()
        if http_client:
            await http_client.aclose()
        logger.info("CoreLDove AI Sourcing Service shutdown completed")
    except Exception as e:
        logger.error("Error during shutdown", error=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "coreldove-ai-sourcing"
    }

@app.post("/api/sourcing/start")
async def start_product_sourcing(request: SourcingRequest, background_tasks: BackgroundTasks):
    """
    Start AI-powered product sourcing for specified categories
    Step 1 of the CoreLDove workflow
    """
    try:
        logger.info("Starting product sourcing", 
                   categories=request.categories, 
                   tenant_id=request.tenant_id)
        
        # Start background sourcing task
        background_tasks.add_task(
            perform_product_sourcing,
            request
        )
        
        # Store sourcing session in cache
        session_id = f"sourcing_session_{request.tenant_id}_{int(datetime.utcnow().timestamp())}"
        await redis_client.setex(
            session_id,
            3600,  # 1 hour TTL
            json.dumps({
                "status": "in_progress",
                "request": request.dict(),
                "started_at": datetime.utcnow().isoformat()
            })
        )
        
        return {
            "success": True,
            "session_id": session_id,
            "message": f"Product sourcing started for {len(request.categories)} categories",
            "estimated_completion": "10-15 minutes"
        }
        
    except Exception as e:
        logger.error("Failed to start product sourcing", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

async def perform_product_sourcing(request: SourcingRequest):
    """
    Background task: AI-powered product sourcing with insights generation
    """
    try:
        logger.info("Performing product sourcing", tenant_id=request.tenant_id)
        
        all_products = []
        
        # Source products for each category
        for category in request.categories:
            logger.info("Sourcing products for category", category=category)
            
            # Call Amazon sourcing service
            sourcing_response = await http_client.post(
                f"{AMAZON_API_URL}/api/source/category",
                json={
                    "category": category.value,
                    "max_products": request.max_products // len(request.categories),
                    "min_rating": request.min_rating,
                    "max_price": request.max_price_usd,
                    "min_reviews": request.min_reviews,
                    "dropship_only": request.dropship_eligible_only,
                    "tenant_id": request.tenant_id
                },
                timeout=120.0
            )
            
            if sourcing_response.status_code == 200:
                category_products = sourcing_response.json().get("products", [])
                
                # Generate AI insights for each product
                for product in category_products:
                    insights = await generate_product_insights(product)
                    
                    sourced_product = SourcedProduct(
                        id=product.get("id", ""),
                        amazon_asin=product.get("asin", ""),
                        title=product.get("title", ""),
                        description=product.get("description", ""),
                        category=category,
                        price_usd=product.get("price", 0.0),
                        rating=product.get("rating", 0.0),
                        review_count=product.get("review_count", 0),
                        images=product.get("images", []),
                        features=product.get("features", []),
                        seller_info=product.get("seller", {}),
                        dropship_eligible=product.get("dropship_eligible", False),
                        insights=insights,
                        tenant_id=request.tenant_id
                    )
                    
                    all_products.append(sourced_product)
        
        # Sort products by potential (combination of demand, trending, and margin)
        all_products.sort(
            key=lambda p: (p.insights.demand_score + p.insights.trending_score + p.insights.estimated_margin * 10) / 3,
            reverse=True
        )
        
        # Store sourced products for approval
        cache_key = f"sourced_products:{request.tenant_id}"
        await redis_client.setex(
            cache_key,
            86400,  # 24 hours TTL
            json.dumps([p.dict() for p in all_products])
        )
        
        # Notify completion
        await redis_client.publish(
            f"sourcing_complete:{request.tenant_id}",
            json.dumps({
                "products_found": len(all_products),
                "categories": [c.value for c in request.categories],
                "status": "ready_for_approval"
            })
        )
        
        logger.info("Product sourcing completed", 
                   tenant_id=request.tenant_id,
                   products_found=len(all_products))
        
    except Exception as e:
        logger.error("Product sourcing failed", error=str(e), tenant_id=request.tenant_id)

async def generate_product_insights(product_data: Dict[str, Any]) -> ProductInsight:
    """
    Generate AI-powered insights for a product using BizOSaaS AI agents
    """
    try:
        # Call AI agents service for product analysis
        analysis_response = await http_client.post(
            f"{AI_AGENTS_URL}/agents/product-market-analysis",
            json={
                "product_data": product_data,
                "analysis_type": "dropshipping_potential",
                "include_insights": ["demand", "competition", "trends", "margin", "audience"]
            },
            timeout=60.0
        )
        
        if analysis_response.status_code == 200:
            analysis = analysis_response.json()
            
            return ProductInsight(
                product_id=product_data.get("id", ""),
                amazon_rating=product_data.get("rating", 0.0),
                review_count=product_data.get("review_count", 0),
                seller_rating=product_data.get("seller", {}).get("rating", 0.0),
                price_usd=product_data.get("price", 0.0),
                estimated_margin=analysis.get("estimated_margin", 0.0),
                demand_score=analysis.get("demand_score", 50.0),
                trending_score=analysis.get("trending_score", 50.0),
                competition_level=analysis.get("competition_level", "medium"),
                seasonal_factor=analysis.get("seasonal_factor", 1.0),
                key_features=analysis.get("key_features", []),
                pros=analysis.get("pros", []),
                cons=analysis.get("cons", []),
                target_audience=analysis.get("target_audience", ""),
                market_potential=analysis.get("market_potential", "unknown")
            )
        else:
            # Fallback basic insights if AI service is unavailable
            return ProductInsight(
                product_id=product_data.get("id", ""),
                amazon_rating=product_data.get("rating", 0.0),
                review_count=product_data.get("review_count", 0),
                seller_rating=product_data.get("seller", {}).get("rating", 0.0),
                price_usd=product_data.get("price", 0.0),
                estimated_margin=25.0,  # Default assumption
                demand_score=50.0,
                trending_score=50.0,
                competition_level="medium",
                seasonal_factor=1.0,
                key_features=[],
                pros=[],
                cons=[],
                target_audience="General consumers",
                market_potential="moderate"
            )
            
    except Exception as e:
        logger.error("Failed to generate insights", error=str(e))
        # Return basic insights as fallback
        return ProductInsight(
            product_id=product_data.get("id", ""),
            amazon_rating=product_data.get("rating", 0.0),
            review_count=product_data.get("review_count", 0),
            seller_rating=0.0,
            price_usd=product_data.get("price", 0.0),
            estimated_margin=20.0,
            demand_score=40.0,
            trending_score=40.0,
            competition_level="unknown",
            seasonal_factor=1.0,
            key_features=[],
            pros=[],
            cons=[],
            target_audience="Unknown",
            market_potential="unknown"
        )

@app.get("/api/sourcing/products")
async def get_sourced_products(
    tenant_id: str,
    category: Optional[ProductCategory] = None,
    status: Optional[ProductStatus] = None,
    min_score: Optional[float] = Query(default=None, ge=0.0, le=100.0)
):
    """
    Get sourced products for human approval
    Step 2 of the CoreLDove workflow
    """
    try:
        cache_key = f"sourced_products:{tenant_id}"
        cached_products = await redis_client.get(cache_key)
        
        if not cached_products:
            return {
                "products": [],
                "total": 0,
                "message": "No sourced products found. Please start a sourcing session first."
            }
        
        products = json.loads(cached_products)
        
        # Apply filters
        if category:
            products = [p for p in products if p.get("category") == category.value]
        
        if status:
            products = [p for p in products if p.get("status") == status.value]
        
        if min_score:
            products = [
                p for p in products 
                if (p.get("insights", {}).get("demand_score", 0) + 
                    p.get("insights", {}).get("trending_score", 0)) / 2 >= min_score
            ]
        
        return {
            "products": products,
            "total": len(products),
            "filters": {
                "category": category.value if category else None,
                "status": status.value if status else None,
                "min_score": min_score
            }
        }
        
    except Exception as e:
        logger.error("Failed to get sourced products", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sourcing/approve")
async def approve_products(decision: ApprovalDecision, background_tasks: BackgroundTasks):
    """
    Human-in-the-loop approval for sourced products
    Step 3 of the CoreLDove workflow
    """
    try:
        logger.info("Processing approval decision", 
                   action=decision.action,
                   product_count=len(decision.product_ids),
                   tenant_id=decision.tenant_id)
        
        if decision.action == "approve":
            # Start content generation for approved products
            background_tasks.add_task(
                process_approved_products,
                decision.product_ids,
                decision.tenant_id,
                decision.user_id
            )
            
            message = f"Approved {len(decision.product_ids)} products for content generation"
        else:
            # Archive rejected products
            await archive_rejected_products(decision.product_ids, decision.tenant_id)
            message = f"Rejected {len(decision.product_ids)} products"
        
        return {
            "success": True,
            "action": decision.action,
            "products_processed": len(decision.product_ids),
            "message": message
        }
        
    except Exception as e:
        logger.error("Failed to process approval", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

async def process_approved_products(product_ids: List[str], tenant_id: str, user_id: str):
    """
    Background task: Process approved products through content generation pipeline
    Steps 4-6 of the CoreLDove workflow
    """
    try:
        logger.info("Processing approved products", 
                   product_count=len(product_ids),
                   tenant_id=tenant_id)
        
        for product_id in product_ids:
            # Step 4: Keyword research
            keywords_response = await http_client.post(
                f"{AI_AGENTS_URL}/agents/keyword-research",
                json={
                    "product_id": product_id,
                    "tenant_id": tenant_id,
                    "platforms": ["google", "amazon", "social"],
                    "intent_types": ["commercial", "informational"]
                },
                timeout=120.0
            )
            
            keywords_data = {}
            if keywords_response.status_code == 200:
                keywords_data = keywords_response.json()
            
            # Step 5: Content generation
            content_response = await http_client.post(
                f"{AI_AGENTS_URL}/agents/product-content-generation",
                json={
                    "product_id": product_id,
                    "tenant_id": tenant_id,
                    "keywords": keywords_data.get("keywords", []),
                    "content_types": ["title", "description", "bullet_points", "seo_content"]
                },
                timeout=120.0
            )
            
            content_data = {}
            if content_response.status_code == 200:
                content_data = content_response.json()
            
            # Step 6: Image enhancement
            image_response = await http_client.post(
                f"{AI_AGENTS_URL}/agents/image-enhancement",
                json={
                    "product_id": product_id,
                    "tenant_id": tenant_id,
                    "enhancement_types": ["background_removal", "quality_improvement", "branding"]
                },
                timeout=180.0
            )
            
            image_data = {}
            if image_response.status_code == 200:
                image_data = image_response.json()
            
            # Combine all generated data for preview
            processed_product = {
                "product_id": product_id,
                "keywords": keywords_data,
                "content": content_data,
                "images": image_data,
                "status": "ready_for_preview",
                "processed_at": datetime.utcnow().isoformat()
            }
            
            # Store processed product for preview approval
            preview_key = f"processed_product:{tenant_id}:{product_id}"
            await redis_client.setex(
                preview_key,
                86400,  # 24 hours TTL
                json.dumps(processed_product)
            )
        
        # Notify completion
        await redis_client.publish(
            f"content_generation_complete:{tenant_id}",
            json.dumps({
                "products_processed": len(product_ids),
                "status": "ready_for_preview"
            })
        )
        
        logger.info("Content generation completed", 
                   tenant_id=tenant_id,
                   products_processed=len(product_ids))
        
    except Exception as e:
        logger.error("Content generation failed", error=str(e), tenant_id=tenant_id)

async def archive_rejected_products(product_ids: List[str], tenant_id: str):
    """
    Archive rejected products
    """
    try:
        archive_key = f"rejected_products:{tenant_id}"
        existing_rejected = await redis_client.get(archive_key)
        
        rejected_list = json.loads(existing_rejected) if existing_rejected else []
        rejected_list.extend({
            "product_id": pid,
            "rejected_at": datetime.utcnow().isoformat()
        } for pid in product_ids)
        
        await redis_client.setex(
            archive_key,
            2592000,  # 30 days TTL
            json.dumps(rejected_list)
        )
        
        logger.info("Products archived", product_count=len(product_ids), tenant_id=tenant_id)
        
    except Exception as e:
        logger.error("Failed to archive rejected products", error=str(e))

@app.get("/api/sourcing/processed")
async def get_processed_products(tenant_id: str):
    """
    Get processed products ready for final approval and listing
    Step 7 of the CoreLDove workflow - Preview before publishing
    """
    try:
        # Get all processed products for tenant
        keys = await redis_client.keys(f"processed_product:{tenant_id}:*")
        processed_products = []
        
        for key in keys:
            product_data = await redis_client.get(key)
            if product_data:
                processed_products.append(json.loads(product_data))
        
        return {
            "processed_products": processed_products,
            "total": len(processed_products),
            "message": "Products ready for final approval and publishing"
        }
        
    except Exception as e:
        logger.error("Failed to get processed products", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sourcing/publish")
async def publish_products(
    product_ids: List[str],
    tenant_id: str,
    platforms: List[str],
    background_tasks: BackgroundTasks
):
    """
    Publish approved products to multiple platforms
    Step 8 of the CoreLDove workflow - Multi-platform publishing
    """
    try:
        logger.info("Publishing products to platforms",
                   product_count=len(product_ids),
                   platforms=platforms,
                   tenant_id=tenant_id)
        
        # Start background publishing task
        background_tasks.add_task(
            publish_to_platforms,
            product_ids,
            tenant_id,
            platforms
        )
        
        return {
            "success": True,
            "products_queued": len(product_ids),
            "platforms": platforms,
            "message": "Products queued for publishing to selected platforms"
        }
        
    except Exception as e:
        logger.error("Failed to queue products for publishing", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

async def publish_to_platforms(product_ids: List[str], tenant_id: str, platforms: List[str]):
    """
    Background task: Publish products to multiple platforms
    """
    try:
        for product_id in product_ids:
            # Get processed product data
            preview_key = f"processed_product:{tenant_id}:{product_id}"
            product_data = await redis_client.get(preview_key)
            
            if not product_data:
                logger.error("Processed product not found", product_id=product_id)
                continue
            
            processed_product = json.loads(product_data)
            
            # Publish to Saleor first (primary platform)
            if "saleor" in platforms:
                await publish_to_saleor(processed_product, tenant_id)
            
            # Publish to other platforms
            for platform in platforms:
                if platform != "saleor":
                    await publish_to_platform(processed_product, platform, tenant_id)
        
        # Start marketing automation
        await trigger_marketing_automation(product_ids, tenant_id)
        
        logger.info("Publishing completed", 
                   product_count=len(product_ids),
                   tenant_id=tenant_id)
        
    except Exception as e:
        logger.error("Publishing failed", error=str(e))

async def publish_to_saleor(product_data: Dict[str, Any], tenant_id: str):
    """Publish product to Saleor via bridge service"""
    try:
        response = await http_client.post(
            f"{SALEOR_BRIDGE_URL}/api/products/source-and-create",
            json={
                "source_url": f"internal://processed/{product_data['product_id']}",
                "source_type": "processed",
                "tenant_id": tenant_id,
                "user_id": "system",
                "ai_enhance": False,  # Already processed
                "processed_data": product_data
            },
            timeout=60.0
        )
        
        if response.status_code == 200:
            logger.info("Product published to Saleor", product_id=product_data['product_id'])
        else:
            logger.error("Failed to publish to Saleor", 
                        product_id=product_data['product_id'],
                        status_code=response.status_code)
            
    except Exception as e:
        logger.error("Saleor publishing error", error=str(e))

async def publish_to_platform(product_data: Dict[str, Any], platform: str, tenant_id: str):
    """Publish product to external platform"""
    try:
        # This will integrate with platform-specific APIs
        # For now, log the intent
        logger.info("Publishing to external platform",
                   platform=platform,
                   product_id=product_data['product_id'],
                   tenant_id=tenant_id)
        
        # TODO: Implement platform-specific publishing
        # - Amazon Seller Central API
        # - Facebook/Instagram Shopping API
        # - Google Shopping API
        # - eBay API
        # etc.
        
    except Exception as e:
        logger.error("External platform publishing error", 
                    platform=platform,
                    error=str(e))

async def trigger_marketing_automation(product_ids: List[str], tenant_id: str):
    """
    Trigger BizOSaaS marketing automation for published products
    Step 9 of the CoreLDove workflow - Automated marketing
    """
    try:
        response = await http_client.post(
            f"{MARKETING_SERVICE_URL}/api/campaigns/product-launch-campaign",
            json={
                "product_ids": product_ids,
                "tenant_id": tenant_id,
                "campaign_type": "product_launch",
                "automation_level": "full"
            },
            timeout=30.0
        )
        
        if response.status_code == 200:
            logger.info("Marketing automation triggered", 
                       product_count=len(product_ids),
                       tenant_id=tenant_id)
        else:
            logger.error("Failed to trigger marketing automation")
            
    except Exception as e:
        logger.error("Marketing automation error", error=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8022)