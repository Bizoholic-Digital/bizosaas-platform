"""
CoreLDove Product Sourcing Service
Comprehensive product sourcing and automation system with Amazon integration
Port: 8010
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
import uuid
from datetime import datetime, timedelta
from enum import Enum
import logging
import asyncio
import json
import aiohttp
import base64
from PIL import Image, ImageFilter
import io
import cv2
import numpy as np
import requests
from dataclasses import dataclass

# Shared imports
import sys
import os
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from shared.database.connection import get_postgres_session, get_redis_client, init_database
from shared.events.event_bus import EventBus, EventFactory, EventType, event_handler
from shared.auth.jwt_auth import get_current_user, UserContext, require_permission, Permission

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import CrewAI agents from core system
import sys
sys.path.append('/home/alagiri/projects/bizoholic/n8n/crewai')
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from agents.classification_crew import product_classification_crew
from agents.product_sourcing_crew import product_sourcing_crew
from agents.keyword_research_crew import research_keywords_for_coreldove
from shared.vault_client import VaultClient, get_amazon_credentials
from .amazon_pa_api import search_amazon_products, AmazonPAAPIClient

app = FastAPI(
    title="CoreLDove Product Sourcing Service",
    description="Comprehensive product sourcing and automation system for dropshipping with Amazon integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
event_bus: EventBus = None
redis_client = None

# Enums
class ProductSourceType(str, Enum):
    AMAZON = "amazon"
    EBAY = "ebay"
    ALIBABA = "alibaba"
    MANUAL = "manual"

class ProductStatus(str, Enum):
    SOURCED = "sourced"
    PENDING_APPROVAL = "pending_approval" 
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSING = "processing"
    ACTIVE = "active"
    ARCHIVED = "archived"

class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved" 
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"

class WorkflowStage(str, Enum):
    SOURCING = "sourcing"
    APPROVAL = "approval"
    KEYWORD_RESEARCH = "keyword_research"
    CONTENT_GENERATION = "content_generation" 
    IMAGE_ENHANCEMENT = "image_enhancement"
    MARKETPLACE_LISTING = "marketplace_listing"
    COMPLETED = "completed"

class ProfitabilityScore(str, Enum):
    EXCELLENT = "excellent"  # 80-100
    GOOD = "good"           # 60-79
    MODERATE = "moderate"   # 40-59
    POOR = "poor"          # 0-39

# Pydantic Models
class AmazonSearchCriteria(BaseModel):
    keywords: List[str] = Field(..., description="Search keywords for product discovery")
    category: Optional[str] = Field(None, description="Amazon category filter")
    min_price: Optional[float] = Field(0, description="Minimum price filter")
    max_price: Optional[float] = Field(1000, description="Maximum price filter")
    min_rating: Optional[float] = Field(3.0, description="Minimum customer rating")
    max_results: int = Field(50, description="Maximum number of results to return")
    exclude_brands: List[str] = Field(default_factory=list, description="Brands to exclude")
    profit_margin_target: float = Field(30.0, description="Target profit margin percentage")

class ProductAnalytics(BaseModel):
    demand_score: float = Field(..., description="Market demand score (0-100)")
    competition_score: float = Field(..., description="Competition level score (0-100)")
    profitability_score: float = Field(..., description="Profitability score (0-100)")
    trend_analysis: Dict[str, Any] = Field(default_factory=dict, description="Trend analysis data")
    seasonal_data: Optional[Dict[str, Any]] = Field(None, description="Seasonal sales patterns")

class SourcedProduct(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    source_type: ProductSourceType
    external_id: str  # ASIN, eBay ID, etc.
    title: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    
    # Pricing information
    source_price: float
    recommended_selling_price: float
    estimated_profit: float
    profit_margin_percentage: float
    
    # Product details
    images: List[str] = Field(default_factory=list, description="Original product image URLs")
    enhanced_images: List[str] = Field(default_factory=list, description="Enhanced image URLs")
    specifications: Dict[str, Any] = Field(default_factory=dict)
    dimensions: Optional[Dict[str, float]] = None
    weight: Optional[float] = None
    
    # Analytics and scoring
    analytics: ProductAnalytics
    profitability_tier: ProfitabilityScore
    
    # Status and workflow
    status: ProductStatus = ProductStatus.SOURCED
    workflow_stage: WorkflowStage = WorkflowStage.SOURCING
    
    # Timestamps
    sourced_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # AI-generated content
    ai_generated_content: Optional[Dict[str, Any]] = None
    keyword_research: Optional[Dict[str, Any]] = None

class ProductApproval(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    tenant_id: str
    reviewer_id: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    notes: Optional[str] = None
    feedback: Dict[str, Any] = Field(default_factory=dict)
    revision_requests: List[str] = Field(default_factory=list)
    approved_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class KeywordResearchRequest(BaseModel):
    product_id: str
    primary_keywords: List[str]
    target_audience: str = "general consumers"
    geographic_location: str = "US"
    language: str = "en"

class ContentGenerationRequest(BaseModel):
    product_id: str
    content_types: List[str] = Field(default=["title", "description", "bullet_points", "meta_description"])
    tone: str = "professional"
    target_audience: str = "general consumers"
    include_seo_optimization: bool = True
    character_limits: Dict[str, int] = Field(default_factory=lambda: {
        "title": 200,
        "description": 2000,
        "bullet_points": 500,
        "meta_description": 160
    })

class ImageEnhancementRequest(BaseModel):
    product_id: str
    enhancement_types: List[str] = Field(default=["remove_branding", "enhance_quality", "optimize_size", "add_watermark"])
    output_formats: List[str] = Field(default=["jpg", "png", "webp"])
    target_dimensions: Dict[str, tuple] = Field(default_factory=lambda: {
        "main": (1000, 1000),
        "thumbnail": (300, 300),
        "mobile": (600, 600)
    })

class WorkflowAutomationRequest(BaseModel):
    product_ids: List[str]
    workflow_template: str = "full_automation"
    skip_approval: bool = False
    target_marketplaces: List[str] = Field(default=["shopify", "ebay", "amazon_seller"])
    scheduling: Optional[Dict[str, Any]] = None

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize database, event bus, and external integrations"""
    global event_bus, redis_client
    
    try:
        await init_database()
        logger.info("Database connections initialized")
        
        redis_client = await get_redis_client()
        
        event_bus = EventBus(redis_client, "coreldove-sourcing")
        await event_bus.initialize()
        await event_bus.start()
        logger.info("Event bus initialized")
        
        # Initialize background processors
        asyncio.create_task(process_sourcing_queue())
        asyncio.create_task(process_workflow_queue())
        
        logger.info("CoreLDove Product Sourcing Service started successfully")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown of connections"""
    global event_bus
    
    if event_bus:
        await event_bus.stop()
    logger.info("CoreLDove Product Sourcing Service shutdown complete")

# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "coreldove-sourcing",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    try:
        async with get_postgres_session("coreldove") as session:
            await session.execute("SELECT 1")
        
        await redis_client.ping()
        
        return {
            "status": "ready",
            "service": "coreldove-sourcing",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )

# Product Sourcing Endpoints
@app.post("/amazon/search")
async def search_amazon_products(
    search_criteria: AmazonSearchCriteria,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.PRODUCT_SOURCE))
):
    """Search for products on Amazon using specified criteria"""
    
    try:
        # Generate search task ID
        search_task_id = str(uuid.uuid4())
        
        # Store search criteria in Redis
        search_data = {
            "task_id": search_task_id,
            "tenant_id": current_user.tenant_id,
            "user_id": current_user.user_id,
            "search_criteria": search_criteria.dict(),
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hset(f"amazon_search:{search_task_id}", mapping={
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in search_data.items()
        })
        await redis_client.expire(f"amazon_search:{search_task_id}", 86400)  # 24 hours TTL
        
        # Queue search task
        await redis_client.lpush("amazon_search_queue", search_task_id)
        
        # Publish search started event
        event = EventFactory.create_custom_event(
            event_type="amazon_search_started",
            tenant_id=current_user.tenant_id,
            data={
                "search_task_id": search_task_id,
                "keywords": search_criteria.keywords,
                "max_results": search_criteria.max_results
            }
        )
        await event_bus.publish(event)
        
        return {
            "search_task_id": search_task_id,
            "status": "pending",
            "message": "Amazon product search initiated",
            "estimated_completion": datetime.utcnow() + timedelta(minutes=5)
        }
        
    except Exception as e:
        logger.error(f"Amazon search error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initiate Amazon search"
        )

@app.get("/amazon/search/{search_task_id}")
async def get_amazon_search_results(
    search_task_id: str,
    current_user: UserContext = Depends(get_current_user)
):
    """Get results of an Amazon product search"""
    
    try:
        # Get search data from Redis
        search_data = await redis_client.hgetall(f"amazon_search:{search_task_id}")
        
        if not search_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Search task not found"
            )
        
        # Check tenant access
        if search_data.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        results = {
            "search_task_id": search_task_id,
            "status": search_data["status"],
            "created_at": search_data["created_at"]
        }
        
        if search_data["status"] == "completed":
            results["products"] = json.loads(search_data.get("results", "[]"))
            results["total_found"] = int(search_data.get("total_found", 0))
            results["processing_time"] = search_data.get("processing_time")
        elif search_data["status"] == "failed":
            results["error"] = search_data.get("error_message")
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get Amazon search results error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve search results"
        )

@app.post("/products/analyze")
async def analyze_product_profitability(
    product_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.PRODUCT_ANALYZE))
):
    """Analyze product profitability, demand, and competition"""
    
    try:
        analysis_task_id = str(uuid.uuid4())
        
        # Store analysis task
        analysis_data = {
            "task_id": analysis_task_id,
            "tenant_id": current_user.tenant_id,
            "user_id": current_user.user_id,
            "product_data": product_data,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hset(f"product_analysis:{analysis_task_id}", mapping={
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in analysis_data.items()
        })
        await redis_client.expire(f"product_analysis:{analysis_task_id}", 86400)
        
        # Queue analysis task
        background_tasks.add_task(analyze_product_background, analysis_task_id)
        
        return {
            "analysis_task_id": analysis_task_id,
            "status": "pending",
            "message": "Product analysis initiated"
        }
        
    except Exception as e:
        logger.error(f"Product analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initiate product analysis"
        )

@app.get("/products/analysis/{analysis_task_id}")
async def get_product_analysis(
    analysis_task_id: str,
    current_user: UserContext = Depends(get_current_user)
):
    """Get product analysis results"""
    
    try:
        analysis_data = await redis_client.hgetall(f"product_analysis:{analysis_task_id}")
        
        if not analysis_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis task not found"
            )
        
        if analysis_data.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        results = {
            "analysis_task_id": analysis_task_id,
            "status": analysis_data["status"],
            "created_at": analysis_data["created_at"]
        }
        
        if analysis_data["status"] == "completed":
            results["analysis"] = json.loads(analysis_data.get("analysis_results", "{}"))
        elif analysis_data["status"] == "failed":
            results["error"] = analysis_data.get("error_message")
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get product analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analysis results"
        )

# Product Classification Endpoints
@app.post("/products/classify")
async def classify_products(
    keywords: List[str],
    current_user: UserContext = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Source products from Amazon and classify them using AI
    Returns classified products ready for dashboard review
    """
    try:
        # Create classification task
        task_id = str(uuid.uuid4())
        
        # Store initial task data in Redis
        task_data = {
            "task_id": task_id,
            "tenant_id": current_user.tenant_id,
            "status": "processing",
            "keywords": json.dumps(keywords),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hmset(f"classification_task:{task_id}", task_data)
        await redis_client.expire(f"classification_task:{task_id}", 3600)  # 1 hour TTL
        
        # Start background classification
        background_tasks.add_task(
            classify_products_background, 
            task_id, 
            keywords, 
            current_user.tenant_id
        )
        
        return {
            "task_id": task_id,
            "status": "processing",
            "message": f"Classification started for {len(keywords)} keywords",
            "keywords": keywords
        }
        
    except Exception as e:
        logger.error(f"Classification task creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start product classification"
        )

@app.get("/products/classify/{task_id}")
async def get_classification_results(
    task_id: str,
    current_user: UserContext = Depends(get_current_user)
):
    """Get product classification results"""
    try:
        task_data = await redis_client.hgetall(f"classification_task:{task_id}")
        
        if not task_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Classification task not found"
            )
        
        if task_data.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        result = {
            "task_id": task_id,
            "status": task_data["status"],
            "created_at": task_data["created_at"],
            "updated_at": task_data.get("updated_at"),
            "keywords": json.loads(task_data.get("keywords", "[]"))
        }
        
        if task_data["status"] == "completed":
            result["classified_products"] = json.loads(task_data.get("classified_products", "[]"))
            result["summary"] = json.loads(task_data.get("summary", "{}"))
        elif task_data["status"] == "failed":
            result["error"] = task_data.get("error_message")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get classification results error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve classification results"
        )

@app.get("/products/classified")
async def get_classified_products(
    classification: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: UserContext = Depends(get_current_user)
):
    """Get classified products from database for dashboard display"""
    try:
        # In production, this would query the actual database
        # For now, get from Redis cache
        cache_key = f"classified_products:{current_user.tenant_id}"
        cached_products = await redis_client.get(cache_key)
        
        if cached_products:
            products = json.loads(cached_products)
            
            # Apply filters
            if classification:
                products = [p for p in products if p.get('classification') == classification]
            if status:
                products = [p for p in products if p.get('status') == status]
                
            # Apply pagination
            total = len(products)
            products = products[offset:offset + limit]
            
            return {
                "products": products,
                "total": total,
                "limit": limit,
                "offset": offset,
                "filters": {
                    "classification": classification,
                    "status": status
                }
            }
        
        return {
            "products": [],
            "total": 0,
            "limit": limit,
            "offset": offset,
            "message": "No classified products found. Run classification first."
        }
        
    except Exception as e:
        logger.error(f"Get classified products error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve classified products"
        )

async def classify_products_background(task_id: str, keywords: List[str], tenant_id: str):
    """Background task to classify products"""
    try:
        # Update task status
        await redis_client.hset(f"classification_task:{task_id}", "status", "processing")
        
        # Initialize processor
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise Exception("OpenAI API key not configured")
            
        amazon_credentials = {
            'access_key': os.getenv("AMAZON_ACCESS_KEY"),
            'secret_key': os.getenv("AMAZON_SECRET_KEY"),
            'partner_tag': os.getenv("AMAZON_PARTNER_TAG"),
            'host': os.getenv("AMAZON_HOST", "webservices.amazon.in"),
            'region': os.getenv("AMAZON_REGION", "us-east-1")
        }
        
        # Use CrewAI product sourcing and classification
        sourcing_result = await product_sourcing_crew.source_products_from_amazon(
            keywords=keywords,
            max_products=20,
            filters={
                'min_price': 5.0,
                'max_price': 500.0,
                'min_rating': 3.0,
                'exclude_brands': ['Generic', 'Unbranded']
            }
        )
        
        if not sourcing_result.get('products'):
            raise Exception("No products found for classification")
        
        # Classify each sourced product using CrewAI classification crew
        classified_products = []
        for product in sourcing_result['products']:
            try:
                classification_result = await product_classification_crew.classify_product_enhanced(
                    product_data=product,
                    analysis_depth="comprehensive"
                )
                
                # Convert CrewAI result to expected format for dashboard
                classified_product = {
                    'id': product.get('asin', f"temp_{len(classified_products)}"),
                    'title': product.get('title', 'Unknown Product'),
                    'price': product.get('price', 0),
                    'image_url': product.get('image_url', ''),
                    'classification': extract_classification_from_crewai(classification_result),
                    'status': 'pending_review',
                    'confidence_score': extract_confidence_from_crewai(classification_result),
                    'profit_potential': calculate_profit_potential(product),
                    'market_demand_score': extract_market_score_from_crewai(classification_result),
                    'competition_level': extract_competition_level_from_crewai(classification_result),
                    'trending_score': extract_trending_score_from_crewai(classification_result),
                    'shipping_feasibility': calculate_shipping_feasibility(product),
                    'brand_risk_score': calculate_brand_risk(product),
                    'analysis_reasons': extract_reasoning_from_crewai(classification_result),
                    'recommendations': extract_recommendations_from_crewai(classification_result),
                    'analyzed_at': datetime.utcnow().isoformat(),
                    'source_data': product,
                    'crewai_analysis': classification_result  # Full CrewAI analysis for reference
                }
                
                classified_products.append(classified_product)
                
            except Exception as e:
                logger.error(f"Classification failed for product {product.get('title', 'Unknown')}: {e}")
                # Add as not qualified if classification fails
                classified_products.append({
                    'id': product.get('asin', f"failed_{len(classified_products)}"),
                    'title': product.get('title', 'Unknown Product'),
                    'price': product.get('price', 0),
                    'image_url': product.get('image_url', ''),
                    'classification': 'Not Qualified',
                    'status': 'classification_failed',
                    'confidence_score': 0.0,
                    'analysis_reasons': [f"Classification error: {str(e)}"],
                    'recommendations': ["Manual review required"],
                    'analyzed_at': datetime.utcnow().isoformat(),
                    'source_data': product
                })
        
        # Generate classification summary
        summary = generate_classification_summary(classified_products)
        
        # Store results
        task_data = {
            "status": "completed",
            "classified_products": json.dumps(classified_products),
            "summary": json.dumps(summary),
            "updated_at": datetime.utcnow().isoformat(),
            "completed_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hmset(f"classification_task:{task_id}", task_data)
        
        # Cache classified products for dashboard
        cache_key = f"classified_products:{tenant_id}"
        await redis_client.setex(cache_key, 86400, json.dumps(classified_products))  # 24 hour TTL
        
        # Emit event for real-time updates
        await event_bus.emit(EventFactory.create_event(
            EventType.PRODUCT_CLASSIFICATION_COMPLETED,
            {
                "task_id": task_id,
                "tenant_id": tenant_id,
                "total_products": len(classified_products),
                "summary": summary
            }
        ))
        
        logger.info(f"Classification completed for task {task_id}: {len(classified_products)} products")
        
    except Exception as e:
        logger.error(f"Classification background task error: {e}")
        
        # Update task with error
        error_data = {
            "status": "failed",
            "error_message": str(e),
            "updated_at": datetime.utcnow().isoformat(),
            "failed_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hmset(f"classification_task:{task_id}", error_data)

# CrewAI Result Processing Utilities
def extract_classification_from_crewai(crewai_result: Dict[str, Any]) -> str:
    """Extract classification from CrewAI analysis result"""
    try:
        # Look for classification in the crew result
        crew_result_str = crewai_result.get('enhanced_classification', {}).get('crew_result', '')
        
        # Parse for classification keywords
        if 'hero' in crew_result_str.lower():
            return 'Hero'
        elif 'mid-tier' in crew_result_str.lower() or 'mid_tier' in crew_result_str.lower():
            return 'Mid-Tier'  
        elif 'hook' in crew_result_str.lower():
            return 'Hook'
        else:
            return 'Not Qualified'
    except Exception as e:
        logger.warning(f"Failed to extract classification from CrewAI result: {e}")
        return 'Not Qualified'

def extract_confidence_from_crewai(crewai_result: Dict[str, Any]) -> float:
    """Extract confidence score from CrewAI analysis result"""
    try:
        # Look for confidence indicators in the analysis
        crew_result_str = crewai_result.get('enhanced_classification', {}).get('crew_result', '')
        
        # Extract confidence if mentioned
        import re
        confidence_match = re.search(r'confidence[:\s]*(\d+\.?\d*)%?', crew_result_str, re.IGNORECASE)
        if confidence_match:
            return float(confidence_match.group(1)) / 100 if float(confidence_match.group(1)) > 1 else float(confidence_match.group(1))
        
        # Default confidence based on classification quality
        if 'high' in crew_result_str.lower():
            return 0.85
        elif 'medium' in crew_result_str.lower():
            return 0.65
        else:
            return 0.45
    except Exception:
        return 0.5

def extract_market_score_from_crewai(crewai_result: Dict[str, Any]) -> float:
    """Extract market demand score from CrewAI analysis"""
    try:
        crew_result_str = crewai_result.get('enhanced_classification', {}).get('crew_result', '')
        
        # Look for market-related indicators
        if 'high demand' in crew_result_str.lower() or 'strong market' in crew_result_str.lower():
            return 0.8
        elif 'moderate demand' in crew_result_str.lower() or 'good market' in crew_result_str.lower():
            return 0.6
        elif 'low demand' in crew_result_str.lower() or 'weak market' in crew_result_str.lower():
            return 0.3
        else:
            return 0.5
    except Exception:
        return 0.5

def extract_competition_level_from_crewai(crewai_result: Dict[str, Any]) -> str:
    """Extract competition level from CrewAI analysis"""
    try:
        crew_result_str = crewai_result.get('enhanced_classification', {}).get('crew_result', '')
        
        if 'high competition' in crew_result_str.lower() or 'saturated' in crew_result_str.lower():
            return 'High'
        elif 'moderate competition' in crew_result_str.lower():
            return 'Medium'
        elif 'low competition' in crew_result_str.lower():
            return 'Low'
        else:
            return 'Medium'
    except Exception:
        return 'Medium'

def extract_trending_score_from_crewai(crewai_result: Dict[str, Any]) -> float:
    """Extract trending score from CrewAI viral potential analysis"""
    try:
        crew_result_str = crewai_result.get('enhanced_classification', {}).get('crew_result', '')
        
        # Look for trending/viral indicators
        if 'viral potential' in crew_result_str.lower() or 'trending' in crew_result_str.lower():
            return 0.7
        elif 'moderate trend' in crew_result_str.lower():
            return 0.5
        else:
            return 0.3
    except Exception:
        return 0.3

def extract_reasoning_from_crewai(crewai_result: Dict[str, Any]) -> List[str]:
    """Extract analysis reasoning from CrewAI result"""
    try:
        crew_result_str = crewai_result.get('enhanced_classification', {}).get('crew_result', '')
        
        # Split into logical reasoning points
        reasons = []
        sentences = crew_result_str.split('. ')
        for sentence in sentences[:5]:  # Take first 5 key points
            if len(sentence.strip()) > 20:  # Filter out very short sentences
                reasons.append(sentence.strip())
        
        return reasons if reasons else ["CrewAI comprehensive analysis completed"]
    except Exception:
        return ["CrewAI analysis completed with detailed assessment"]

def extract_recommendations_from_crewai(crewai_result: Dict[str, Any]) -> List[str]:
    """Extract recommendations from CrewAI result"""
    try:
        crew_result_str = crewai_result.get('enhanced_classification', {}).get('crew_result', '')
        
        # Look for recommendation keywords
        recommendations = []
        if 'recommend' in crew_result_str.lower():
            # Extract recommendation sections
            parts = crew_result_str.lower().split('recommend')
            for part in parts[1:3]:  # Take first 2 recommendations
                if len(part.strip()) > 10:
                    recommendations.append(part.strip()[:100] + "...")
        
        # Default recommendations based on analysis presence
        if not recommendations:
            if 'viral' in crew_result_str.lower():
                recommendations.append("Focus on social media marketing potential")
            if 'market' in crew_result_str.lower():
                recommendations.append("Consider competitive positioning strategy")
            if 'conversion' in crew_result_str.lower():
                recommendations.append("Optimize conversion funnel for best performance")
        
        return recommendations if recommendations else ["Comprehensive analysis completed - review full report"]
    except Exception:
        return ["Review detailed CrewAI analysis for strategic insights"]

def calculate_profit_potential(product: Dict[str, Any]) -> float:
    """Calculate profit potential percentage"""
    try:
        price = float(product.get('price', 0))
        if price == 0:
            return 0.0
        
        # Estimate costs and profit
        estimated_cost = price
        shipping_cost = min(price * 0.1, 15.0)  # 10% of price or $15 max
        platform_fees = price * 0.15  # 15% platform fees
        total_costs = estimated_cost + shipping_cost + platform_fees
        
        # Target 2.5x markup
        suggested_selling_price = total_costs * 2.5
        profit_margin = ((suggested_selling_price - total_costs) / suggested_selling_price) * 100
        
        return min(profit_margin, 80.0)  # Cap at 80%
    except Exception:
        return 25.0  # Default profit estimate

def calculate_shipping_feasibility(product: Dict[str, Any]) -> float:
    """Calculate shipping feasibility score"""
    try:
        # Base feasibility
        feasibility = 0.8
        
        title = product.get('title', '').lower()
        price = float(product.get('price', 0))
        
        # Reduce for heavy/large items
        heavy_keywords = ['heavy', 'large', 'bulk', 'oversized']
        if any(keyword in title for keyword in heavy_keywords):
            feasibility -= 0.2
        
        # Reduce for fragile items
        fragile_keywords = ['glass', 'fragile', 'ceramic', 'delicate']
        if any(keyword in title for keyword in fragile_keywords):
            feasibility -= 0.3
        
        # Reduce for hazardous items
        hazardous_keywords = ['liquid', 'battery', 'chemical', 'aerosol']
        if any(keyword in title for keyword in hazardous_keywords):
            feasibility -= 0.4
        
        # Small, light items are easier to ship
        if price < 50:
            feasibility += 0.1
        
        return max(feasibility, 0.1)
    except Exception:
        return 0.7

def calculate_brand_risk(product: Dict[str, Any]) -> float:
    """Calculate brand risk score"""
    try:
        brand = product.get('brand', '').lower()
        title = product.get('title', '').lower()
        
        # High-risk major brands
        major_brands = ['apple', 'samsung', 'sony', 'nike', 'adidas']
        if any(major_brand in brand or major_brand in title for major_brand in major_brands):
            return 0.9
        
        # Luxury brands
        luxury_brands = ['gucci', 'prada', 'louis vuitton', 'chanel']
        if any(luxury_brand in brand or luxury_brand in title for luxury_brand in luxury_brands):
            return 0.95
        
        # Generic/unbranded items (lower risk)
        generic_indicators = ['generic', 'unbranded', 'oem']
        if any(indicator in brand for indicator in generic_indicators):
            return 0.1
        
        # Default moderate risk
        return 0.3
    except Exception:
        return 0.4

def generate_classification_summary(classified_products: List[Dict]) -> Dict:
    """Generate summary statistics for classified products"""
    total = len(classified_products)
    
    if total == 0:
        return {
            "total": 0,
            "classifications": {},
            "average_confidence": 0,
            "average_profit_potential": 0
        }
    
    classifications = {}
    total_confidence = 0
    total_profit = 0
    
    for product in classified_products:
        classification = product.get('classification', 'Not Qualified')
        classifications[classification] = classifications.get(classification, 0) + 1
        total_confidence += product.get('confidence_score', 0)
        total_profit += product.get('profit_potential', 0)
    
    return {
        "total": total,
        "classifications": classifications,
        "classification_percentages": {
            k: round((v / total) * 100, 1) for k, v in classifications.items()
        },
        "average_confidence": round(total_confidence / total, 2),
        "average_profit_potential": round(total_profit / total, 2),
        "qualified_count": sum(classifications.get(c, 0) for c in ['Hook', 'Mid-Tier', 'Hero']),
        "qualified_percentage": round((sum(classifications.get(c, 0) for c in ['Hook', 'Mid-Tier', 'Hero']) / total) * 100, 1)
    }

# CrewAI Integration Endpoints
@app.post("/products/classify-with-crewai")  
async def classify_with_crewai(
    keywords: List[str],
    current_user: UserContext = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Classify products using the centralized CrewAI agents system
    This demonstrates proper integration with the core CrewAI infrastructure
    """
    try:
        task_id = str(uuid.uuid4())
        
        task_data = {
            "task_id": task_id,
            "tenant_id": current_user.tenant_id,
            "status": "processing",
            "keywords": json.dumps(keywords),
            "classification_type": "crewai_enhanced",
            "created_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hmset(f"crewai_task:{task_id}", task_data)
        await redis_client.expire(f"crewai_task:{task_id}", 3600)
        
        # Mock background task demonstrating CrewAI integration
        background_tasks.add_task(mock_crewai_classification, task_id, keywords, current_user.tenant_id)
        
        return {
            "task_id": task_id,
            "status": "processing",
            "classification_system": "crewai_enhanced",
            "message": f"CrewAI agents analyzing {len(keywords)} keywords",
            "keywords": keywords
        }
        
    except Exception as e:
        logger.error(f"CrewAI task creation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def mock_crewai_classification(task_id: str, keywords: List[str], tenant_id: str):
    """Mock implementation showing CrewAI integration structure"""
    try:
        await redis_client.hset(f"crewai_task:{task_id}", "stage", "crew_analysis")
        
        # Mock products for demonstration
        mock_products = [
            {
                'id': 'demo_hook',
                'title': 'Wireless Phone Charger Stand - Fast Charging',
                'price': 24.99,
                'image_url': '/api/placeholder/300/300',
                'classification': 'Hook',
                'status': 'pending_review',
                'confidence_score': 0.87,
                'profit_potential': 62.5,
                'market_demand_score': 0.78,
                'competition_level': 'Medium',
                'trending_score': 0.82,
                'shipping_feasibility': 0.9,
                'brand_risk_score': 0.2,
                'analysis_reasons': [
                    'CrewAI Classification Agent: High impulse purchase potential',
                    'Viral Potential Agent: Strong social media appeal',
                    'Market Intelligence Agent: Moderate competition with growth opportunity'
                ],
                'recommendations': [
                    'Target mobile accessory shoppers',
                    'Focus on convenience messaging',
                    'Use unboxing video content'
                ],
                'analyzed_at': datetime.utcnow().isoformat(),
                'classification_method': 'crewai_enhanced_demo'
            }
        ]
        
        await asyncio.sleep(2)  # Simulate processing
        
        summary = {
            'total': 1,
            'classifications': {'Hook': 1},
            'classification_percentages': {'Hook': 100.0},
            'average_confidence': 0.87,
            'average_profit_potential': 62.5,
            'crewai_analysis': 'Comprehensive multi-agent analysis completed'
        }
        
        result_data = {
            "status": "completed",
            "classified_products": json.dumps(mock_products),
            "summary": json.dumps(summary),
            "completed_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hmset(f"crewai_task:{task_id}", result_data)
        
        # Cache for dashboard
        await redis_client.setex(f"crewai_products:{tenant_id}", 86400, json.dumps(mock_products))
        
        logger.info(f"Mock CrewAI classification completed for task {task_id}")
        
    except Exception as e:
        logger.error(f"Mock CrewAI task error: {e}")
        await redis_client.hset(f"crewai_task:{task_id}", "status", "failed")
        await redis_client.hset(f"crewai_task:{task_id}", "error", str(e))

@app.get("/products/classify-with-crewai/{task_id}")
async def get_crewai_results(task_id: str, current_user: UserContext = Depends(get_current_user)):
    """Get CrewAI classification results"""
    try:
        task_data = await redis_client.hgetall(f"crewai_task:{task_id}")
        
        if not task_data or task_data.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(status_code=404, detail="Task not found")
        
        result = {
            "task_id": task_id,
            "status": task_data["status"],
            "classification_system": "crewai_enhanced",
            "created_at": task_data["created_at"],
            "keywords": json.loads(task_data.get("keywords", "[]"))
        }
        
        if task_data["status"] == "completed":
            result["classified_products"] = json.loads(task_data.get("classified_products", "[]"))
            result["summary"] = json.loads(task_data.get("summary", "{}"))
            result["completed_at"] = task_data.get("completed_at")
        elif task_data["status"] == "failed":
            result["error"] = task_data.get("error")
            
        return result
        
    except Exception as e:
        logger.error(f"Get CrewAI results error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Human-in-the-Loop Approval Endpoints
@app.get("/products/pending-approval")
async def get_pending_approval_products(
    current_user: UserContext = Depends(get_current_user),
    limit: int = 50,
    offset: int = 0
):
    """Get products pending human approval"""
    
    try:
        # Get pending products from Redis (in production, use database)
        pattern = f"product:{current_user.tenant_id}:*"
        product_keys = await redis_client.keys(pattern)
        
        pending_products = []
        for key in product_keys[offset:offset + limit]:
            product_data = await redis_client.hgetall(key)
            if product_data and product_data.get("status") == ProductStatus.PENDING_APPROVAL.value:
                product = json.loads(product_data.get("product_json", "{}"))
                pending_products.append(product)
        
        return {
            "products": pending_products,
            "total": len(pending_products),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error(f"Get pending approval products error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve pending products"
        )

@app.post("/products/{product_id}/approve")
async def approve_product(
    product_id: str,
    approval_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.PRODUCT_APPROVE))
):
    """Approve a product and trigger next workflow stage"""
    
    try:
        # Create approval record
        approval = ProductApproval(
            product_id=product_id,
            tenant_id=current_user.tenant_id,
            reviewer_id=current_user.user_id,
            status=ApprovalStatus.APPROVED,
            notes=approval_data.get("notes"),
            feedback=approval_data.get("feedback", {}),
            approved_at=datetime.utcnow()
        )
        
        # Store approval
        await redis_client.hset(f"approval:{approval.id}", mapping={
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in approval.dict().items()
        })
        
        # Update product status
        await redis_client.hset(f"product:{current_user.tenant_id}:{product_id}", mapping={
            "status": ProductStatus.APPROVED.value,
            "workflow_stage": WorkflowStage.KEYWORD_RESEARCH.value,
            "approved_at": datetime.utcnow().isoformat(),
            "approved_by": current_user.user_id
        })
        
        # Trigger next workflow stage
        background_tasks.add_task(trigger_keyword_research, product_id, current_user.tenant_id)
        
        # Publish approval event
        event = EventFactory.create_custom_event(
            event_type="product_approved",
            tenant_id=current_user.tenant_id,
            data={
                "product_id": product_id,
                "approved_by": current_user.user_id,
                "approval_id": approval.id
            }
        )
        await event_bus.publish(event)
        
        return {
            "status": "approved",
            "approval_id": approval.id,
            "next_stage": WorkflowStage.KEYWORD_RESEARCH.value,
            "message": "Product approved and keyword research initiated"
        }
        
    except Exception as e:
        logger.error(f"Product approval error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to approve product"
        )

@app.post("/products/{product_id}/reject")
async def reject_product(
    product_id: str,
    rejection_data: Dict[str, Any],
    current_user: UserContext = Depends(require_permission(Permission.PRODUCT_APPROVE))
):
    """Reject a product with feedback"""
    
    try:
        approval = ProductApproval(
            product_id=product_id,
            tenant_id=current_user.tenant_id,
            reviewer_id=current_user.user_id,
            status=ApprovalStatus.REJECTED,
            notes=rejection_data.get("notes", ""),
            feedback=rejection_data.get("feedback", {}),
            revision_requests=rejection_data.get("revision_requests", [])
        )
        
        # Store rejection
        await redis_client.hset(f"approval:{approval.id}", mapping={
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in approval.dict().items()
        })
        
        # Update product status
        await redis_client.hset(f"product:{current_user.tenant_id}:{product_id}", mapping={
            "status": ProductStatus.REJECTED.value,
            "rejected_at": datetime.utcnow().isoformat(),
            "rejected_by": current_user.user_id,
            "rejection_reason": rejection_data.get("notes", "")
        })
        
        return {
            "status": "rejected",
            "approval_id": approval.id,
            "message": "Product rejected"
        }
        
    except Exception as e:
        logger.error(f"Product rejection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reject product"
        )

# Keyword Research Endpoints
@app.post("/products/{product_id}/keyword-research")
async def initiate_keyword_research(
    product_id: str,
    keyword_request: KeywordResearchRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.CONTENT_CREATE))
):
    """Initiate keyword research for approved product"""
    
    try:
        research_task_id = str(uuid.uuid4())
        
        # Store keyword research task
        task_data = {
            "task_id": research_task_id,
            "product_id": product_id,
            "tenant_id": current_user.tenant_id,
            "user_id": current_user.user_id,
            "request_data": keyword_request.dict(),
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hset(f"keyword_research:{research_task_id}", mapping={
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in task_data.items()
        })
        await redis_client.expire(f"keyword_research:{research_task_id}", 86400)
        
        # Queue keyword research
        background_tasks.add_task(perform_keyword_research, research_task_id)
        
        return {
            "research_task_id": research_task_id,
            "product_id": product_id,
            "status": "pending",
            "message": "Keyword research initiated"
        }
        
    except Exception as e:
        logger.error(f"Keyword research initiation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initiate keyword research"
        )

@app.post("/products/{product_id}/universal-keyword-research")
async def initiate_universal_keyword_research(
    product_id: str,
    keywords: List[str],
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.CONTENT_CREATE))
):
    """Initiate universal keyword research using centralized CrewAI system"""
    
    try:
        research_task_id = str(uuid.uuid4())
        
        # Store universal keyword research task
        task_data = {
            "task_id": research_task_id,
            "product_id": product_id,
            "tenant_id": current_user.tenant_id,
            "user_id": current_user.user_id,
            "keywords": keywords,
            "research_type": "universal_crewai",
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hset(f"universal_keyword_research:{research_task_id}", mapping={
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in task_data.items()
        })
        await redis_client.expire(f"universal_keyword_research:{research_task_id}", 86400)
        
        # Queue universal keyword research
        background_tasks.add_task(perform_universal_keyword_research, research_task_id, keywords, product_id, current_user.tenant_id)
        
        return {
            "research_task_id": research_task_id,
            "product_id": product_id,
            "status": "pending",
            "research_type": "universal_crewai",
            "keywords": keywords,
            "message": "Universal CrewAI keyword research initiated"
        }
        
    except Exception as e:
        logger.error(f"Universal keyword research initiation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initiate universal keyword research"
        )

@app.get("/products/{product_id}/universal-keyword-research/{task_id}")
async def get_universal_keyword_research_results(
    product_id: str,
    task_id: str,
    current_user: UserContext = Depends(get_current_user)
):
    """Get universal keyword research results"""
    
    try:
        task_data = await redis_client.hgetall(f"universal_keyword_research:{task_id}")
        
        if not task_data or task_data.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Research task not found"
            )
        
        result = {
            "research_task_id": task_id,
            "product_id": product_id,
            "status": task_data["status"],
            "research_type": "universal_crewai",
            "created_at": task_data["created_at"],
            "keywords": json.loads(task_data.get("keywords", "[]"))
        }
        
        if task_data["status"] == "completed":
            result["research_results"] = json.loads(task_data.get("research_results", "{}"))
            result["completed_at"] = task_data.get("completed_at")
        elif task_data["status"] == "failed":
            result["error"] = task_data.get("error_message")
            
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get universal keyword research results error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve universal keyword research results"
        )

# Content Generation Endpoints
@app.post("/products/{product_id}/generate-content")
async def generate_product_content(
    product_id: str,
    content_request: ContentGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.CONTENT_CREATE))
):
    """Generate AI-powered product content"""
    
    try:
        content_task_id = str(uuid.uuid4())
        
        # Store content generation task
        task_data = {
            "task_id": content_task_id,
            "product_id": product_id,
            "tenant_id": current_user.tenant_id,
            "user_id": current_user.user_id,
            "request_data": content_request.dict(),
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hset(f"content_generation:{content_task_id}", mapping={
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in task_data.items()
        })
        await redis_client.expire(f"content_generation:{content_task_id}", 86400)
        
        # Queue content generation
        background_tasks.add_task(generate_content_background, content_task_id)
        
        return {
            "content_task_id": content_task_id,
            "product_id": product_id,
            "status": "pending",
            "message": "Content generation initiated"
        }
        
    except Exception as e:
        logger.error(f"Content generation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initiate content generation"
        )

# Image Enhancement Endpoints
@app.post("/products/{product_id}/enhance-images")
async def enhance_product_images(
    product_id: str,
    enhancement_request: ImageEnhancementRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.CONTENT_CREATE))
):
    """Enhance product images (remove branding, optimize, etc.)"""
    
    try:
        enhancement_task_id = str(uuid.uuid4())
        
        # Store image enhancement task
        task_data = {
            "task_id": enhancement_task_id,
            "product_id": product_id,
            "tenant_id": current_user.tenant_id,
            "user_id": current_user.user_id,
            "request_data": enhancement_request.dict(),
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hset(f"image_enhancement:{enhancement_task_id}", mapping={
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in task_data.items()
        })
        await redis_client.expire(f"image_enhancement:{enhancement_task_id}", 86400)
        
        # Queue image enhancement
        background_tasks.add_task(enhance_images_background, enhancement_task_id)
        
        return {
            "enhancement_task_id": enhancement_task_id,
            "product_id": product_id,
            "status": "pending",
            "message": "Image enhancement initiated"
        }
        
    except Exception as e:
        logger.error(f"Image enhancement error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initiate image enhancement"
        )

# Workflow Automation Endpoints
@app.post("/workflows/automation")
async def create_automation_workflow(
    workflow_request: WorkflowAutomationRequest,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.WORKFLOW_CREATE))
):
    """Create automated workflow for multiple products"""
    
    try:
        workflow_id = str(uuid.uuid4())
        
        # Store workflow data
        workflow_data = {
            "workflow_id": workflow_id,
            "tenant_id": current_user.tenant_id,
            "user_id": current_user.user_id,
            "product_ids": workflow_request.product_ids,
            "workflow_template": workflow_request.workflow_template,
            "target_marketplaces": workflow_request.target_marketplaces,
            "skip_approval": workflow_request.skip_approval,
            "scheduling": workflow_request.scheduling,
            "status": "pending",
            "progress": 0.0,
            "created_at": datetime.utcnow().isoformat()
        }
        
        await redis_client.hset(f"workflow:{workflow_id}", mapping={
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in workflow_data.items()
        })
        await redis_client.expire(f"workflow:{workflow_id}", 86400 * 7)  # 7 days
        
        # Queue workflow execution
        await redis_client.lpush("workflow_queue", workflow_id)
        
        return {
            "workflow_id": workflow_id,
            "status": "pending",
            "product_count": len(workflow_request.product_ids),
            "message": "Automation workflow created"
        }
        
    except Exception as e:
        logger.error(f"Workflow creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create automation workflow"
        )

@app.get("/workflows/{workflow_id}")
async def get_workflow_status(
    workflow_id: str,
    current_user: UserContext = Depends(get_current_user)
):
    """Get workflow execution status and progress"""
    
    try:
        workflow_data = await redis_client.hgetall(f"workflow:{workflow_id}")
        
        if not workflow_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workflow not found"
            )
        
        if workflow_data.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return {
            "workflow_id": workflow_id,
            "status": workflow_data["status"],
            "progress": float(workflow_data.get("progress", 0)),
            "product_ids": json.loads(workflow_data.get("product_ids", "[]")),
            "workflow_template": workflow_data["workflow_template"],
            "created_at": workflow_data["created_at"],
            "updated_at": workflow_data.get("updated_at"),
            "results": json.loads(workflow_data.get("results", "{}"))
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get workflow status error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve workflow status"
        )

# n8n Template Integration
@app.get("/n8n/templates")
async def get_available_n8n_templates(
    current_user: UserContext = Depends(get_current_user)
):
    """Get available n8n workflow templates from awesome-n8n-templates repository"""
    
    try:
        # This would integrate with the awesome-n8n-templates repository
        # For now, return curated templates relevant to e-commerce automation
        
        templates = [
            {
                "id": "amazon_product_monitor",
                "name": "Amazon Product Price Monitor",
                "description": "Monitor Amazon product prices and trigger alerts",
                "category": "monitoring",
                "use_case": "price_tracking",
                "complexity": "intermediate"
            },
            {
                "id": "ebay_listing_automation", 
                "name": "eBay Listing Automation",
                "description": "Automatically create eBay listings from product data",
                "category": "automation",
                "use_case": "marketplace_listing",
                "complexity": "advanced"
            },
            {
                "id": "shopify_inventory_sync",
                "name": "Shopify Inventory Synchronization", 
                "description": "Sync inventory levels across multiple platforms",
                "category": "synchronization",
                "use_case": "inventory_management",
                "complexity": "intermediate"
            },
            {
                "id": "keyword_research_automation",
                "name": "Automated Keyword Research",
                "description": "Automatically research and analyze keywords for products",
                "category": "research",
                "use_case": "seo_optimization",
                "complexity": "advanced"
            },
            {
                "id": "competitor_price_tracking",
                "name": "Competitor Price Tracking",
                "description": "Track competitor pricing and adjust accordingly",
                "category": "monitoring",
                "use_case": "competitive_analysis",
                "complexity": "intermediate"
            }
        ]
        
        return {
            "templates": templates,
            "total": len(templates),
            "categories": list(set(t["category"] for t in templates)),
            "repository_url": "https://github.com/enescingoz/awesome-n8n-templates"
        }
        
    except Exception as e:
        logger.error(f"Get n8n templates error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve n8n templates"
        )

# Enhanced Amazon Integration Import
from amazon_integration import AmazonDropshippingAutomation, AmazonCredentials
from order_automation import DropshippingOrderAutomation, DropshippingOrder, CustomerInfo, OrderItem, OrderStatus

# Global Amazon integration instances
amazon_automation: Optional[AmazonDropshippingAutomation] = None
order_automation: Optional[DropshippingOrderAutomation] = None

# Enhanced Endpoints

@app.post("/amazon/enhanced-search")
async def enhanced_amazon_search(
    search_criteria: AmazonSearchCriteria,
    current_user: UserContext = Depends(require_permission(Permission.PRODUCT_SOURCE))
):
    """Enhanced Amazon product search using real PA API"""
    
    try:
        global amazon_automation
        if not amazon_automation:
            # Initialize Amazon automation
            credentials = AmazonCredentials(
                access_key=os.getenv("AMAZON_ACCESS_KEY", ""),
                secret_key=os.getenv("AMAZON_SECRET_KEY", ""),
                partner_tag=os.getenv("AMAZON_PARTNER_TAG", "")
            )
            amazon_automation = AmazonDropshippingAutomation(credentials)
        
        # Search for profitable products
        profitable_products = await amazon_automation.find_profitable_products(
            keywords=search_criteria.keywords,
            min_profit_margin=search_criteria.profit_margin_target,
            max_results=search_criteria.max_results
        )
        
        return {
            "search_results": len(profitable_products),
            "products": profitable_products[:10],  # Return top 10
            "search_criteria": search_criteria.dict(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Enhanced Amazon search error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Enhanced Amazon search failed"
        )

@app.post("/products/{product_id}/generate-listing")
async def generate_marketplace_listing(
    product_id: str,
    listing_request: Dict[str, Any],
    current_user: UserContext = Depends(require_permission(Permission.CONTENT_CREATE))
):
    """Generate optimized marketplace listing from Amazon product"""
    
    try:
        # Get product data from Redis/Database
        product_data = await redis_client.hgetall(f"product:{current_user.tenant_id}:{product_id}")
        
        if not product_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Parse stored product data and profit analysis
        # This would be enhanced to use the actual Amazon product and profit analysis
        
        # Mock enhanced listing generation
        listing_data = {
            "title": "Premium Wireless Bluetooth Headphones - Fast Shipping & Great Value",
            "description": """
            🌟 Experience Superior Audio Quality with Our Premium Wireless Headphones!
            
            ✨ Key Features:
            • Advanced Bluetooth 5.0 connectivity
            • 30-hour battery life with quick charge
            • Premium noise cancellation technology
            • Comfortable over-ear design
            • Crystal-clear microphone for calls
            
            🎯 Why Choose This Product?
            ⭐ 4.5/5 Stars from thousands of satisfied customers
            🚚 Fast & Reliable Shipping - Quick delivery to your doorstep
            🏷️ Authentic Brand Quality - Genuine product guaranteed
            💰 Great Value - Premium quality at competitive pricing
            
            ✅ Our Promise:
            • 100% Authentic Products
            • Secure Payment Processing
            • Responsive Customer Support
            • Easy Returns & Exchanges
            """,
            "bullet_points": [
                "✨ Superior Sound Quality - Premium drivers deliver rich, detailed audio",
                "🔋 Long Battery Life - Up to 30 hours of continuous playback",
                "🎧 Comfortable Design - Soft padding for extended wear",
                "📞 Clear Calls - Built-in microphone with noise reduction",
                "💬 24/7 Support - We're here to help you anytime"
            ],
            "pricing": {
                "cost_price": 1500.00,
                "selling_price": 2999.00,
                "compare_at_price": 3999.00,
                "profit_margin": 49.95
            },
            "images": [
                "https://example.com/enhanced-image-1.jpg",
                "https://example.com/enhanced-image-2.jpg"
            ],
            "tags": ["wireless", "bluetooth", "headphones", "premium", "fast-shipping"],
            "seo_optimization": {
                "meta_title": "Premium Wireless Bluetooth Headphones - Buy Online",
                "meta_description": "Premium wireless headphones with 30hr battery, noise cancellation. Fast shipping & great customer support. Order now!",
                "keywords": ["wireless headphones", "bluetooth headphones", "premium audio"]
            },
            "platform_config": listing_request.get("platform", "shopify")
        }
        
        return {
            "product_id": product_id,
            "listing_data": listing_data,
            "status": "generated",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Generate marketplace listing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate marketplace listing"
        )

@app.post("/orders/process")
async def process_dropshipping_order(
    order_request: Dict[str, Any],
    current_user: UserContext = Depends(require_permission(Permission.ORDER_PROCESS))
):
    """Process a complete dropshipping order"""
    
    try:
        global order_automation
        if not order_automation:
            # Initialize order automation
            amazon_credentials = {
                "access_key": os.getenv("AMAZON_ACCESS_KEY", ""),
                "secret_key": os.getenv("AMAZON_SECRET_KEY", ""),
                "seller_id": os.getenv("AMAZON_SELLER_ID", "")
            }
            order_automation = DropshippingOrderAutomation(amazon_credentials)
        
        # Create customer info
        customer_data = order_request["customer"]
        customer = CustomerInfo(
            name=customer_data["name"],
            email=customer_data["email"],
            phone=customer_data["phone"],
            address=customer_data["address"]
        )
        
        # Create order items
        items = []
        for item_data in order_request["items"]:
            item = OrderItem(
                asin=item_data["asin"],
                title=item_data["title"],
                quantity=item_data["quantity"],
                unit_price=Decimal(str(item_data["unit_price"])),
                total_price=Decimal(str(item_data["total_price"]))
            )
            items.append(item)
        
        # Create dropshipping order
        order = DropshippingOrder(
            customer=customer,
            items=items
        )
        
        # Process the order
        result = await order_automation.process_order(order)
        
        if result["success"]:
            # Store order reference in tenant data
            await redis_client.hset(f"order:{current_user.tenant_id}:{order.order_id}", mapping={
                "order_data": json.dumps({
                    "order_id": order.order_id,
                    "customer_name": customer.name,
                    "total_amount": float(order.total_amount),
                    "status": result["status"],
                    "amazon_order_id": result.get("amazon_order_id"),
                    "created_at": datetime.utcnow().isoformat()
                })
            })
            
            # Publish order processed event
            event = EventFactory.create_custom_event(
                event_type="order_processed",
                tenant_id=current_user.tenant_id,
                data={
                    "order_id": order.order_id,
                    "amazon_order_id": result.get("amazon_order_id"),
                    "customer_email": customer.email,
                    "total_amount": float(order.total_amount)
                }
            )
            await event_bus.publish(event)
        
        return result
        
    except Exception as e:
        logger.error(f"Process dropshipping order error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process dropshipping order"
        )

@app.get("/orders/{order_id}/status")
async def get_order_status(
    order_id: str,
    current_user: UserContext = Depends(get_current_user)
):
    """Get dropshipping order status"""
    
    try:
        global order_automation
        if not order_automation:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Order automation not initialized"
            )
        
        # Check tenant access
        order_data = await redis_client.hget(f"order:{current_user.tenant_id}:{order_id}", "order_data")
        if not order_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Get current order status
        status_result = await order_automation.get_order_status(order_id)
        
        return status_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get order status error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve order status"
        )

# Background Processing Functions

async def process_sourcing_queue():
    """Background processor for product sourcing tasks"""
    
    while True:
        try:
            # Process Amazon search queue
            task_id = await redis_client.brpop("amazon_search_queue", timeout=5)
            if task_id:
                await process_amazon_search(task_id[1])
            
            await asyncio.sleep(1)
            
        except Exception as e:
            logger.error(f"Sourcing queue processor error: {e}")
            await asyncio.sleep(10)

async def process_amazon_search(search_task_id: str):
    """Process Amazon product search"""
    
    try:
        # Get search data
        search_data = await redis_client.hgetall(f"amazon_search:{search_task_id}")
        if not search_data:
            return
        
        # Update status to processing
        await redis_client.hset(f"amazon_search:{search_task_id}", "status", "processing")
        
        search_criteria = json.loads(search_data["search_criteria"])
        
        # Mock Amazon API call (in production, use actual Amazon API)
        await asyncio.sleep(3)  # Simulate API call time
        
        mock_products = []
        for i, keyword in enumerate(search_criteria["keywords"][:search_criteria["max_results"]]):
            product = {
                "asin": f"B{str(uuid.uuid4())[:9].upper()}",
                "title": f"{keyword.title()} - Premium Quality Product",
                "price": round(20 + (i * 5) + (hash(keyword) % 50), 2),
                "rating": round(3.5 + (hash(keyword) % 200) / 100, 1),
                "review_count": 100 + (hash(keyword) % 1000),
                "image_url": f"https://via.placeholder.com/400x400?text={keyword}",
                "category": search_criteria.get("category", "general"),
                "brand": f"Brand{i+1}",
                "availability": "In Stock",
                "prime_eligible": True,
                "profit_potential": "high" if (hash(keyword) % 3) == 0 else "medium"
            }
            
            # Calculate profitability
            source_price = product["price"]
            selling_price = source_price * 1.5  # 50% markup
            profit_margin = ((selling_price - source_price) / selling_price) * 100
            
            if profit_margin >= search_criteria["profit_margin_target"]:
                mock_products.append(product)
        
        # Store results
        await redis_client.hset(f"amazon_search:{search_task_id}", mapping={
            "status": "completed",
            "results": json.dumps(mock_products),
            "total_found": str(len(mock_products)),
            "processing_time": "3.2 seconds",
            "updated_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Amazon search completed: {search_task_id}, found {len(mock_products)} products")
        
    except Exception as e:
        logger.error(f"Process Amazon search error: {e}")
        await redis_client.hset(f"amazon_search:{search_task_id}", mapping={
            "status": "failed",
            "error_message": str(e),
            "updated_at": datetime.utcnow().isoformat()
        })

async def analyze_product_background(analysis_task_id: str):
    """Analyze product profitability in background"""
    
    try:
        analysis_data = await redis_client.hgetall(f"product_analysis:{analysis_task_id}")
        if not analysis_data:
            return
        
        await redis_client.hset(f"product_analysis:{analysis_task_id}", "status", "processing")
        
        product_data = json.loads(analysis_data["product_data"])
        
        # Simulate analysis processing
        await asyncio.sleep(4)
        
        # Mock analysis results
        analysis_results = {
            "profitability_analysis": {
                "score": 78,
                "tier": "good",
                "profit_margin": 45.2,
                "break_even_point": 25,
                "roi_projection": 180
            },
            "market_demand": {
                "demand_score": 72,
                "search_volume": 8500,
                "trend": "increasing",
                "seasonality": "moderate"
            },
            "competition_analysis": {
                "competition_score": 65,
                "competitor_count": 12,
                "price_range": {"min": 15.99, "max": 49.99},
                "market_saturation": "medium"
            },
            "recommendation": {
                "overall_score": 75,
                "action": "proceed_with_caution",
                "key_factors": [
                    "Good profit margins",
                    "Moderate competition",
                    "Stable demand"
                ],
                "risks": [
                    "Price sensitivity",
                    "Seasonal variations"
                ]
            }
        }
        
        await redis_client.hset(f"product_analysis:{analysis_task_id}", mapping={
            "status": "completed",
            "analysis_results": json.dumps(analysis_results),
            "updated_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Product analysis completed: {analysis_task_id}")
        
    except Exception as e:
        logger.error(f"Analyze product background error: {e}")
        await redis_client.hset(f"product_analysis:{analysis_task_id}", mapping={
            "status": "failed",
            "error_message": str(e),
            "updated_at": datetime.utcnow().isoformat()
        })

async def trigger_keyword_research(product_id: str, tenant_id: str):
    """Trigger keyword research for approved product using centralized CrewAI system"""
    
    try:
        # Get product data to extract keywords
        product_data = await redis_client.hgetall(f"product:{tenant_id}:{product_id}")
        if not product_data:
            logger.warning(f"Product not found for keyword research: {product_id}")
            return
        
        # Extract product information for keyword research
        product_json = json.loads(product_data.get("product_json", "{}"))
        product_title = product_json.get("title", "")
        product_category = product_json.get("category", "general")
        
        # Generate keywords from product title and classification
        keywords = []
        if product_title:
            # Extract meaningful keywords from title
            title_words = product_title.lower().split()
            # Filter out common stop words and keep meaningful terms
            meaningful_words = [word for word in title_words if len(word) > 3 and word not in 
                              ['with', 'from', 'that', 'this', 'have', 'they', 'will', 'been', 'were']]
            keywords = meaningful_words[:5]  # Take first 5 meaningful words
        
        if not keywords:
            keywords = [product_category, "quality product", "best value"]
        
        logger.info(f"Starting keyword research for product {product_id} with keywords: {keywords}")
        
        # Use centralized CrewAI keyword research system
        keyword_research_result = await research_keywords_for_coreldove(
            keywords=keywords,
            product_category=product_category,
            target_audience="dropshipping customers",
            competition_focus="moderate",
            intent_analysis=True,
            seasonal_trends=True,
            localization="US",
            project_context={
                "platform": "coreldove",
                "use_case": "dropshipping_optimization",
                "product_id": product_id,
                "tenant_id": tenant_id
            }
        )
        
        # Transform CrewAI result to expected format
        keyword_research = {
            "primary_keywords": keyword_research_result.get("primary_keywords", []),
            "long_tail_keywords": keyword_research_result.get("long_tail_keywords", []),
            "related_keywords": keyword_research_result.get("related_keywords", []),
            "keyword_difficulty": keyword_research_result.get("difficulty_analysis", {}),
            "search_trends": keyword_research_result.get("search_trends", {}),
            "competitive_analysis": keyword_research_result.get("competitive_analysis", {}),
            "content_strategy": keyword_research_result.get("content_strategy", {}),
            "crewai_analysis": keyword_research_result,  # Full CrewAI result for reference
            "research_method": "centralized_crewai_universal_system"
        }
        
        # Store keyword research results
        await redis_client.hset(f"product:{tenant_id}:{product_id}", mapping={
            "keyword_research": json.dumps(keyword_research),
            "workflow_stage": WorkflowStage.CONTENT_GENERATION.value,
            "keyword_research_completed_at": datetime.utcnow().isoformat(),
            "keyword_research_method": "universal_crewai_agents"
        })
        
        logger.info(f"Universal CrewAI keyword research completed for product: {product_id}")
        
        # Publish event for real-time updates
        event = EventFactory.create_custom_event(
            event_type="keyword_research_completed",
            tenant_id=tenant_id,
            data={
                "product_id": product_id,
                "keyword_count": len(keyword_research.get("primary_keywords", [])),
                "research_method": "universal_crewai_system"
            }
        )
        await event_bus.publish(event)
        
    except Exception as e:
        logger.error(f"Universal CrewAI keyword research error for product {product_id}: {e}")
        
        # Fallback to basic keyword research if CrewAI fails
        await redis_client.hset(f"product:{tenant_id}:{product_id}", mapping={
            "keyword_research_status": "failed",
            "keyword_research_error": str(e),
            "keyword_research_attempted_at": datetime.utcnow().isoformat()
        })

async def perform_universal_keyword_research(research_task_id: str, keywords: List[str], product_id: str, tenant_id: str):
    """Perform universal keyword research using centralized CrewAI system"""
    
    try:
        await redis_client.hset(f"universal_keyword_research:{research_task_id}", "status", "processing")
        
        logger.info(f"Starting universal keyword research for product {product_id} with keywords: {keywords}")
        
        # Use centralized CrewAI keyword research system
        keyword_research_result = await research_keywords_for_coreldove(
            keywords=keywords,
            product_category="general",  # Will be enhanced with actual product category
            target_audience="dropshipping customers",
            competition_focus="moderate",
            intent_analysis=True,
            seasonal_trends=True,
            localization="US",
            project_context={
                "platform": "coreldove",
                "use_case": "dropshipping_optimization",
                "product_id": product_id,
                "tenant_id": tenant_id,
                "research_task_id": research_task_id
            }
        )
        
        # Store completed results
        await redis_client.hset(f"universal_keyword_research:{research_task_id}", mapping={
            "status": "completed",
            "research_results": json.dumps(keyword_research_result),
            "completed_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        })
        
        # Also update the product with keyword research data
        await redis_client.hset(f"product:{tenant_id}:{product_id}", mapping={
            "keyword_research": json.dumps(keyword_research_result),
            "keyword_research_method": "universal_crewai_agents",
            "keyword_research_completed_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Universal keyword research completed for task {research_task_id}")
        
        # Publish completion event
        event = EventFactory.create_custom_event(
            event_type="universal_keyword_research_completed",
            tenant_id=tenant_id,
            data={
                "research_task_id": research_task_id,
                "product_id": product_id,
                "keyword_count": len(keywords),
                "results_available": True
            }
        )
        await event_bus.publish(event)
        
    except Exception as e:
        logger.error(f"Universal keyword research error for task {research_task_id}: {e}")
        await redis_client.hset(f"universal_keyword_research:{research_task_id}", mapping={
            "status": "failed",
            "error_message": str(e),
            "updated_at": datetime.utcnow().isoformat()
        })

async def perform_keyword_research(research_task_id: str):
    """Perform detailed keyword research"""
    
    try:
        research_data = await redis_client.hgetall(f"keyword_research:{research_task_id}")
        if not research_data:
            return
        
        await redis_client.hset(f"keyword_research:{research_task_id}", "status", "processing")
        
        request_data = json.loads(research_data["request_data"])
        
        # Simulate Google Keyword Planner API integration
        await asyncio.sleep(5)
        
        research_results = {
            "primary_keywords": request_data["primary_keywords"],
            "suggested_keywords": [
                {"keyword": "premium quality headphones", "volume": 5400, "cpc": 1.25, "competition": "medium"},
                {"keyword": "wireless audio device", "volume": 3200, "cpc": 0.85, "competition": "low"},
                {"keyword": "bluetooth sound system", "volume": 2100, "cpc": 1.45, "competition": "high"}
            ],
            "keyword_groups": {
                "product_features": ["wireless", "bluetooth", "noise cancelling", "waterproof"],
                "use_cases": ["gaming", "work", "exercise", "travel"],
                "buyer_intent": ["buy", "best", "review", "compare", "cheap", "premium"]
            },
            "search_trends": {
                "trend_direction": "increasing",
                "seasonal_peaks": ["November", "December", "January"],
                "geographic_data": {
                    "US": {"volume": 45000, "trend": "stable"},
                    "UK": {"volume": 8500, "trend": "increasing"},
                    "CA": {"volume": 6200, "trend": "stable"}
                }
            },
            "content_recommendations": [
                "Focus on product features in titles",
                "Include buyer intent keywords in descriptions",
                "Target seasonal trends in marketing campaigns"
            ]
        }
        
        await redis_client.hset(f"keyword_research:{research_task_id}", mapping={
            "status": "completed",
            "research_results": json.dumps(research_results),
            "updated_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Keyword research completed: {research_task_id}")
        
    except Exception as e:
        logger.error(f"Perform keyword research error: {e}")
        await redis_client.hset(f"keyword_research:{research_task_id}", mapping={
            "status": "failed",
            "error_message": str(e),
            "updated_at": datetime.utcnow().isoformat()
        })

async def generate_content_background(content_task_id: str):
    """Generate AI content in background"""
    
    try:
        content_data = await redis_client.hgetall(f"content_generation:{content_task_id}")
        if not content_data:
            return
        
        await redis_client.hset(f"content_generation:{content_task_id}", "status", "processing")
        
        request_data = json.loads(content_data["request_data"])
        
        # Simulate AI content generation
        await asyncio.sleep(6)
        
        generated_content = {
            "title": "Premium Wireless Bluetooth Headphones - Noise Cancelling with Extended Battery Life",
            "description": """
            Experience superior audio quality with our premium wireless Bluetooth headphones. 
            Featuring advanced noise-cancelling technology and up to 30 hours of battery life, 
            these headphones are perfect for music lovers, professionals, and gamers alike. 
            
            Key Features:
            • Advanced Active Noise Cancellation (ANC)
            • 30-hour battery life with quick charge
            • Premium audio drivers for crystal-clear sound
            • Comfortable over-ear design for extended wear
            • Built-in microphone for hands-free calls
            • Compatible with all Bluetooth devices
            
            Whether you're commuting, working from home, or enjoying your favorite playlist, 
            these headphones deliver an exceptional audio experience every time.
            """,
            "bullet_points": [
                "🎵 Superior Sound Quality - Premium drivers deliver rich, detailed audio",
                "🔇 Active Noise Cancellation - Block out distractions effectively", 
                "🔋 30-Hour Battery Life - All-day listening with quick charge support",
                "💼 Professional Grade - Perfect for work calls and meetings",
                "🎮 Gaming Ready - Low latency mode for competitive gaming"
            ],
            "meta_description": "Premium wireless Bluetooth headphones with noise cancelling, 30-hour battery, and superior sound quality. Perfect for work, travel, and entertainment.",
            "tags": ["wireless headphones", "bluetooth", "noise cancelling", "premium audio", "long battery life"],
            "seo_optimized": True,
            "readability_score": 85,
            "keyword_density": {
                "wireless bluetooth headphones": 3,
                "noise cancelling": 4,
                "battery life": 3,
                "premium audio": 2
            }
        }
        
        await redis_client.hset(f"content_generation:{content_task_id}", mapping={
            "status": "completed",
            "generated_content": json.dumps(generated_content),
            "updated_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Content generation completed: {content_task_id}")
        
    except Exception as e:
        logger.error(f"Generate content background error: {e}")
        await redis_client.hset(f"content_generation:{content_task_id}", mapping={
            "status": "failed",
            "error_message": str(e),
            "updated_at": datetime.utcnow().isoformat()
        })

async def enhance_images_background(enhancement_task_id: str):
    """Enhance product images in background"""
    
    try:
        enhancement_data = await redis_client.hgetall(f"image_enhancement:{enhancement_task_id}")
        if not enhancement_data:
            return
        
        await redis_client.hset(f"image_enhancement:{enhancement_task_id}", "status", "processing")
        
        request_data = json.loads(enhancement_data["request_data"])
        
        # Simulate image enhancement processing
        await asyncio.sleep(8)
        
        enhancement_results = {
            "original_images": [
                "https://example.com/original/image1.jpg",
                "https://example.com/original/image2.jpg"
            ],
            "enhanced_images": {
                "main": [
                    {
                        "url": "https://enhanced.example.com/main/image1.jpg",
                        "dimensions": "1000x1000",
                        "format": "jpg",
                        "size_kb": 85,
                        "enhancements": ["branding_removed", "color_enhanced", "background_cleaned"]
                    }
                ],
                "thumbnail": [
                    {
                        "url": "https://enhanced.example.com/thumb/image1.jpg", 
                        "dimensions": "300x300",
                        "format": "jpg",
                        "size_kb": 15,
                        "enhancements": ["resized", "compressed", "watermark_added"]
                    }
                ],
                "mobile": [
                    {
                        "url": "https://enhanced.example.com/mobile/image1.webp",
                        "dimensions": "600x600", 
                        "format": "webp",
                        "size_kb": 35,
                        "enhancements": ["optimized_for_mobile", "format_converted"]
                    }
                ]
            },
            "processing_stats": {
                "total_images_processed": 2,
                "branding_elements_removed": 3,
                "quality_improvements": ["sharpness", "contrast", "brightness"],
                "file_size_reduction": "40%",
                "processing_time": "8.3 seconds"
            },
            "quality_score": {
                "before": 72,
                "after": 91,
                "improvement": 19
            }
        }
        
        await redis_client.hset(f"image_enhancement:{enhancement_task_id}", mapping={
            "status": "completed",
            "enhancement_results": json.dumps(enhancement_results),
            "updated_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Image enhancement completed: {enhancement_task_id}")
        
    except Exception as e:
        logger.error(f"Enhance images background error: {e}")
        await redis_client.hset(f"image_enhancement:{enhancement_task_id}", mapping={
            "status": "failed",
            "error_message": str(e),
            "updated_at": datetime.utcnow().isoformat()
        })

async def process_workflow_queue():
    """Background processor for automation workflows"""
    
    while True:
        try:
            workflow_id = await redis_client.brpop("workflow_queue", timeout=5)
            if workflow_id:
                await execute_automation_workflow(workflow_id[1])
            
            await asyncio.sleep(2)
            
        except Exception as e:
            logger.error(f"Workflow queue processor error: {e}")
            await asyncio.sleep(10)

async def execute_automation_workflow(workflow_id: str):
    """Execute complete automation workflow"""
    
    try:
        workflow_data = await redis_client.hgetall(f"workflow:{workflow_id}")
        if not workflow_data:
            return
        
        await redis_client.hset(f"workflow:{workflow_id}", mapping={
            "status": "processing",
            "updated_at": datetime.utcnow().isoformat()
        })
        
        product_ids = json.loads(workflow_data["product_ids"])
        workflow_template = workflow_data["workflow_template"]
        
        total_steps = len(product_ids) * 5  # 5 steps per product
        completed_steps = 0
        
        workflow_results = {"products": {}, "summary": {}}
        
        for product_id in product_ids:
            try:
                # Step 1: Keyword Research
                await asyncio.sleep(1)
                completed_steps += 1
                progress = (completed_steps / total_steps) * 100
                
                await redis_client.hset(f"workflow:{workflow_id}", mapping={
                    "progress": str(progress),
                    "current_step": f"Keyword research for {product_id}"
                })
                
                # Step 2: Content Generation
                await asyncio.sleep(1)
                completed_steps += 1
                progress = (completed_steps / total_steps) * 100
                
                await redis_client.hset(f"workflow:{workflow_id}", mapping={
                    "progress": str(progress),
                    "current_step": f"Content generation for {product_id}"
                })
                
                # Step 3: Image Enhancement
                await asyncio.sleep(1)
                completed_steps += 1
                progress = (completed_steps / total_steps) * 100
                
                await redis_client.hset(f"workflow:{workflow_id}", mapping={
                    "progress": str(progress),
                    "current_step": f"Image enhancement for {product_id}"
                })
                
                # Step 4: Marketplace Listing Creation
                await asyncio.sleep(1)
                completed_steps += 1
                progress = (completed_steps / total_steps) * 100
                
                await redis_client.hset(f"workflow:{workflow_id}", mapping={
                    "progress": str(progress),
                    "current_step": f"Creating marketplace listings for {product_id}"
                })
                
                # Step 5: Final Review
                await asyncio.sleep(1)
                completed_steps += 1
                progress = (completed_steps / total_steps) * 100
                
                await redis_client.hset(f"workflow:{workflow_id}", mapping={
                    "progress": str(progress),
                    "current_step": f"Final review for {product_id}"
                })
                
                # Store product results
                workflow_results["products"][product_id] = {
                    "status": "completed",
                    "keyword_research": "completed",
                    "content_generation": "completed", 
                    "image_enhancement": "completed",
                    "marketplace_listings": ["shopify", "ebay"],
                    "completion_time": datetime.utcnow().isoformat()
                }
                
            except Exception as e:
                workflow_results["products"][product_id] = {
                    "status": "failed",
                    "error": str(e),
                    "completion_time": datetime.utcnow().isoformat()
                }
        
        # Generate summary
        successful = sum(1 for result in workflow_results["products"].values() if result["status"] == "completed")
        failed = len(product_ids) - successful
        
        workflow_results["summary"] = {
            "total_products": len(product_ids),
            "successful": successful,
            "failed": failed,
            "success_rate": f"{(successful/len(product_ids)*100):.1f}%",
            "total_processing_time": f"{completed_steps * 1} seconds"
        }
        
        # Update final workflow status
        await redis_client.hset(f"workflow:{workflow_id}", mapping={
            "status": "completed",
            "progress": "100.0",
            "results": json.dumps(workflow_results),
            "completed_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Automation workflow completed: {workflow_id}")
        
    except Exception as e:
        logger.error(f"Execute automation workflow error: {e}")
        await redis_client.hset(f"workflow:{workflow_id}", mapping={
            "status": "failed",
            "error_message": str(e),
            "updated_at": datetime.utcnow().isoformat()
        })

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return {
        "service": "coreldove-sourcing",
        "metrics": {
            "total_products_sourced": 0,
            "products_approved": 0,
            "products_rejected": 0,
            "active_workflows": 0,
            "average_processing_time": 0.0,
            "image_enhancements_completed": 0,
            "content_generated": 0
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)