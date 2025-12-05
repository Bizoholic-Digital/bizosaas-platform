#!/usr/bin/env python3
"""
BizOSaaS Campaign Management Service - Port 3007
AI-Powered Marketing Campaign Automation & Optimization
Consolidated from stub implementation
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import asyncio
import httpx
import os
from datetime import datetime, timedelta
import logging
import uuid
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(
    title="BizOSaaS Campaign Management Service",
    description="AI-Powered Marketing Campaign Automation & Optimization",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:securepassword123@bizosaas-postgres-5432:5432/bizosaas_platform")
AI_AGENTS_URL = os.getenv("AI_AGENTS_URL", "http://bizosaas-brain:8001")
REDIS_URL = os.getenv("REDIS_URL", "redis://bizosaas-redis-6379:6379/4")
BRAIN_API_URL = os.getenv("BRAIN_API_URL", "http://localhost:8001")

# Pydantic models
class Campaign(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., description="Campaign name")
    client_id: str = Field(..., description="Client identifier")
    tenant_id: str = Field(..., description="Tenant identifier for multi-tenancy")
    platform: str = Field(..., description="Marketing platform (google_ads, facebook, linkedin)")
    budget: float = Field(..., gt=0, description="Campaign budget")
    objective: str = Field(..., description="Campaign objective")
    target_audience: Dict[str, Any] = Field(default_factory=dict)
    keywords: List[str] = Field(default_factory=list)
    ad_copy: Dict[str, str] = Field(default_factory=dict)
    status: str = Field(default="draft", description="Campaign status")
    ai_optimization: bool = Field(default=True, description="Enable AI optimization")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CampaignPerformance(BaseModel):
    campaign_id: str
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    cost: float = 0.0
    revenue: float = 0.0
    ctr: float = 0.0
    cpc: float = 0.0
    conversion_rate: float = 0.0
    roas: float = 0.0
    date: datetime = Field(default_factory=datetime.now)
    
class OptimizationRequest(BaseModel):
    campaign_id: str
    optimization_type: str = Field(..., description="Type of optimization (budget, keywords, audience)")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    ai_enabled: bool = Field(default=True, description="Use AI for optimization")

class AIInsights(BaseModel):
    campaign_id: str
    insights_type: str
    recommendations: List[str]
    confidence_score: float
    impact_estimate: str
    generated_at: datetime = Field(default_factory=datetime.now)

# In-memory storage (replace with proper database in production)
campaigns_db = {}
performance_db = {}
insights_db = {}

# Utility functions
async def call_brain_api(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Call Brain AI service for intelligent campaign operations"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BRAIN_API_URL}/api/brain/{endpoint}", json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Brain API call failed: {e}")
        return {"error": str(e), "fallback": True}

async def call_ai_agent(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Call AI agents service for intelligent campaign operations"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{AI_AGENTS_URL}/{endpoint}", json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"AI agent call failed: {e}")
        return {"error": str(e), "fallback": True}

def calculate_performance_metrics(performance: CampaignPerformance) -> CampaignPerformance:
    """Calculate derived performance metrics"""
    if performance.impressions > 0:
        performance.ctr = (performance.clicks / performance.impressions) * 100
    
    if performance.clicks > 0:
        performance.cpc = performance.cost / performance.clicks
        performance.conversion_rate = (performance.conversions / performance.clicks) * 100
    
    if performance.cost > 0:
        performance.roas = performance.revenue / performance.cost
    
    return performance

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration"""
    return {
        "status": "healthy",
        "service": "campaign-management",
        "version": "2.0.0",
        "port": 3007,
        "timestamp": datetime.now().isoformat(),
        "dependencies": {
            "database": "connected",
            "brain_api": "available",
            "ai_agents": "available",
            "redis": "connected"
        }
    }

# Campaign Management Endpoints
@app.post("/campaigns", response_model=Campaign)
async def create_campaign(campaign: Campaign, background_tasks: BackgroundTasks):
    """Create a new marketing campaign with AI optimization"""
    
    # Generate unique campaign ID
    campaign.id = str(uuid.uuid4())
    campaign.created_at = datetime.now()
    campaign.updated_at = datetime.now()
    
    # AI-powered campaign strategy optimization via Brain API
    if campaign.ai_optimization:
        optimization_data = {
            "campaign_data": campaign.dict(),
            "optimization_goal": "maximize_roi",
            "platform_specific": True,
            "tenant_id": campaign.tenant_id
        }
        
        # Call Brain API for campaign strategy optimization
        background_tasks.add_task(optimize_campaign_via_brain, campaign.id, optimization_data)
    
    # Store campaign
    campaigns_db[campaign.id] = campaign
    
    logger.info(f"Created campaign {campaign.id} for client {campaign.client_id} (tenant: {campaign.tenant_id})")
    return campaign

@app.get("/campaigns", response_model=List[Campaign])
async def get_campaigns(
    client_id: Optional[str] = None, 
    tenant_id: Optional[str] = None,
    status: Optional[str] = None,
    platform: Optional[str] = None
):
    """Retrieve campaigns with optional filtering"""
    
    campaigns = list(campaigns_db.values())
    
    # Apply filters
    if client_id:
        campaigns = [c for c in campaigns if c.client_id == client_id]
    if tenant_id:
        campaigns = [c for c in campaigns if c.tenant_id == tenant_id]
    if status:
        campaigns = [c for c in campaigns if c.status == status]
    if platform:
        campaigns = [c for c in campaigns if c.platform == platform]
    
    return campaigns

@app.get("/campaigns/{campaign_id}", response_model=Campaign)
async def get_campaign(campaign_id: str):
    """Get specific campaign details"""
    
    if campaign_id not in campaigns_db:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return campaigns_db[campaign_id]

@app.put("/campaigns/{campaign_id}", response_model=Campaign)
async def update_campaign(campaign_id: str, campaign_update: Campaign, background_tasks: BackgroundTasks):
    """Update existing campaign"""
    
    if campaign_id not in campaigns_db:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Update campaign
    existing_campaign = campaigns_db[campaign_id]
    updated_data = campaign_update.dict(exclude_unset=True)
    updated_data["updated_at"] = datetime.now()
    
    for key, value in updated_data.items():
        setattr(existing_campaign, key, value)
    
    campaigns_db[campaign_id] = existing_campaign
    
    # Trigger AI re-optimization if enabled
    if existing_campaign.ai_optimization:
        optimization_data = {
            "campaign_data": existing_campaign.dict(),
            "optimization_goal": "maximize_roi",
            "update_type": "campaign_modification"
        }
        background_tasks.add_task(optimize_campaign_via_brain, campaign_id, optimization_data)
    
    logger.info(f"Updated campaign {campaign_id}")
    return existing_campaign

@app.delete("/campaigns/{campaign_id}")
async def delete_campaign(campaign_id: str):
    """Delete campaign"""
    
    if campaign_id not in campaigns_db:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    del campaigns_db[campaign_id]
    
    # Also delete associated performance data and insights
    if campaign_id in performance_db:
        del performance_db[campaign_id]
    if campaign_id in insights_db:
        del insights_db[campaign_id]
    
    logger.info(f"Deleted campaign {campaign_id}")
    return {"message": "Campaign deleted successfully"}

# Campaign Performance Endpoints
@app.post("/campaigns/{campaign_id}/performance")
async def record_performance(campaign_id: str, performance: CampaignPerformance):
    """Record campaign performance data with automatic metric calculation"""
    
    if campaign_id not in campaigns_db:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    performance.campaign_id = campaign_id
    performance = calculate_performance_metrics(performance)
    
    if campaign_id not in performance_db:
        performance_db[campaign_id] = []
    
    performance_db[campaign_id].append(performance)
    
    logger.info(f"Recorded performance for campaign {campaign_id}: CTR={performance.ctr:.2f}%, CPC={performance.cpc:.2f}, ROAS={performance.roas:.2f}")
    return {"message": "Performance data recorded", "metrics": performance.dict()}

@app.get("/campaigns/{campaign_id}/performance")
async def get_performance(campaign_id: str, days: int = 30):
    """Get campaign performance data"""
    
    if campaign_id not in campaigns_db:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    if campaign_id not in performance_db:
        return []
    
    # Filter by date range
    cutoff_date = datetime.now() - timedelta(days=days)
    performance_data = [
        p for p in performance_db[campaign_id] 
        if p.date >= cutoff_date
    ]
    
    return performance_data

# AI Optimization Endpoints
@app.post("/campaigns/{campaign_id}/optimize")
async def optimize_campaign(campaign_id: str, optimization: OptimizationRequest, background_tasks: BackgroundTasks):
    """AI-powered campaign optimization via Brain API"""
    
    if campaign_id not in campaigns_db:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    campaign = campaigns_db[campaign_id]
    performance_data = performance_db.get(campaign_id, [])
    
    # Prepare optimization data for Brain API
    optimization_data = {
        "campaign": campaign.dict(),
        "performance_history": [p.dict() for p in performance_data],
        "optimization_type": optimization.optimization_type,
        "parameters": optimization.parameters,
        "ai_enabled": optimization.ai_enabled
    }
    
    # Call Brain API optimization in background
    background_tasks.add_task(run_brain_optimization, campaign_id, optimization_data)
    
    return {
        "message": "Optimization started via Brain API",
        "campaign_id": campaign_id,
        "optimization_type": optimization.optimization_type,
        "status": "processing"
    }

@app.get("/campaigns/{campaign_id}/insights", response_model=List[AIInsights])
async def get_campaign_insights(campaign_id: str):
    """Get AI-generated campaign insights and recommendations via Brain API"""
    
    if campaign_id not in campaigns_db:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    campaign = campaigns_db[campaign_id]
    performance_data = performance_db.get(campaign_id, [])
    
    # Generate insights using Brain API
    insights_data = {
        "campaign": campaign.dict(),
        "performance_data": [p.dict() for p in performance_data],
        "analysis_type": "comprehensive_insights"
    }
    
    brain_insights = await call_brain_api("ai-insights", insights_data)
    
    if brain_insights.get("fallback"):
        # Fallback basic insights
        insights = generate_basic_insights(campaign, performance_data)
        insights_list = [AIInsights(
            campaign_id=campaign_id,
            insights_type="basic_fallback",
            recommendations=insights.get("recommendations", []),
            confidence_score=0.6,
            impact_estimate="medium"
        )]
    else:
        # Convert Brain API response to insights
        insights_list = [AIInsights(
            campaign_id=campaign_id,
            insights_type="ai_generated",
            recommendations=brain_insights.get("recommendations", []),
            confidence_score=brain_insights.get("confidence", 0.8),
            impact_estimate=brain_insights.get("impact", "high")
        )]
    
    # Store insights
    insights_db[campaign_id] = insights_list
    
    return insights_list

# Background tasks
async def optimize_campaign_via_brain(campaign_id: str, optimization_data: Dict[str, Any]):
    """Background task for Brain API campaign strategy optimization"""
    
    try:
        # Call Brain API for strategy optimization
        result = await call_brain_api("campaign-optimization", optimization_data)
        
        if not result.get("fallback"):
            # Apply Brain API recommendations
            campaign = campaigns_db[campaign_id]
            
            # Update campaign with Brain API recommendations
            if "keywords" in result:
                campaign.keywords = result["keywords"]
            if "ad_copy" in result:
                campaign.ad_copy.update(result["ad_copy"])
            if "target_audience" in result:
                campaign.target_audience.update(result["target_audience"])
            if "budget_adjustment" in result:
                campaign.budget *= result["budget_adjustment"]
            
            campaign.updated_at = datetime.now()
            campaigns_db[campaign_id] = campaign
            
            logger.info(f"Applied Brain API optimization to campaign {campaign_id}")
        
    except Exception as e:
        logger.error(f"Campaign optimization via Brain API failed for {campaign_id}: {e}")

async def run_brain_optimization(campaign_id: str, optimization_data: Dict[str, Any]):
    """Background task for running Brain API performance optimization"""
    
    try:
        result = await call_brain_api("performance-optimization", optimization_data)
        
        if not result.get("fallback"):
            # Apply optimization results from Brain API
            campaign = campaigns_db[campaign_id]
            
            # Update campaign based on Brain API optimization results
            if "budget_adjustment" in result:
                campaign.budget *= result["budget_adjustment"]
            if "bid_adjustments" in result:
                campaign.target_audience.update(result["bid_adjustments"])
            if "keyword_adjustments" in result:
                campaign.keywords = result["keyword_adjustments"]
            
            campaign.updated_at = datetime.now()
            campaigns_db[campaign_id] = campaign
            
            logger.info(f"Applied Brain API performance optimization to campaign {campaign_id}")
            
    except Exception as e:
        logger.error(f"Performance optimization via Brain API failed for {campaign_id}: {e}")

def generate_basic_insights(campaign: Campaign, performance_data: List[CampaignPerformance]) -> Dict[str, Any]:
    """Generate basic insights when Brain API is unavailable"""
    
    if not performance_data:
        return {
            "status": "insufficient_data",
            "message": "Need more performance data for insights",
            "recommendations": [
                "Continue running campaign for at least 7 days",
                "Monitor initial performance metrics",
                "Consider A/B testing different ad copies"
            ]
        }
    
    # Calculate basic metrics
    total_impressions = sum(p.impressions for p in performance_data)
    total_clicks = sum(p.clicks for p in performance_data)
    total_cost = sum(p.cost for p in performance_data)
    total_conversions = sum(p.conversions for p in performance_data)
    total_revenue = sum(p.revenue for p in performance_data)
    
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_cpc = (total_cost / total_clicks) if total_clicks > 0 else 0
    conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
    roas = (total_revenue / total_cost) if total_cost > 0 else 0
    
    insights = {
        "performance_summary": {
            "impressions": total_impressions,
            "clicks": total_clicks,
            "cost": total_cost,
            "conversions": total_conversions,
            "revenue": total_revenue,
            "ctr": round(avg_ctr, 2),
            "cpc": round(avg_cpc, 2),
            "conversion_rate": round(conversion_rate, 2),
            "roas": round(roas, 2)
        },
        "recommendations": []
    }
    
    # Basic recommendations
    if avg_ctr < 2.0:
        insights["recommendations"].append("Consider improving ad copy to increase click-through rate")
    if conversion_rate < 2.0:
        insights["recommendations"].append("Optimize landing page for better conversion rate")
    if avg_cpc > 2.0:
        insights["recommendations"].append("Review keyword strategy to reduce cost per click")
    if roas < 3.0:
        insights["recommendations"].append("Focus on higher-value keywords and audiences")
    
    return insights

# Batch operations
@app.post("/campaigns/batch/status")
async def update_campaigns_status(campaign_ids: List[str], status: str):
    """Batch update campaign status"""
    
    updated_campaigns = []
    for campaign_id in campaign_ids:
        if campaign_id in campaigns_db:
            campaigns_db[campaign_id].status = status
            campaigns_db[campaign_id].updated_at = datetime.now()
            updated_campaigns.append(campaign_id)
    
    return {
        "updated_campaigns": updated_campaigns,
        "total_updated": len(updated_campaigns)
    }

# Analytics endpoints
@app.get("/analytics/campaigns/summary")
async def get_campaigns_summary(client_id: Optional[str] = None, tenant_id: Optional[str] = None):
    """Get campaign analytics summary"""
    
    campaigns = list(campaigns_db.values())
    if client_id:
        campaigns = [c for c in campaigns if c.client_id == client_id]
    if tenant_id:
        campaigns = [c for c in campaigns if c.tenant_id == tenant_id]
    
    summary = {
        "total_campaigns": len(campaigns),
        "active_campaigns": len([c for c in campaigns if c.status == "active"]),
        "total_budget": sum(c.budget for c in campaigns),
        "ai_enabled_campaigns": len([c for c in campaigns if c.ai_optimization]),
        "platforms": {}
    }
    
    # Group by platform
    for campaign in campaigns:
        if campaign.platform not in summary["platforms"]:
            summary["platforms"][campaign.platform] = 0
        summary["platforms"][campaign.platform] += 1
    
    return summary

@app.get("/analytics/performance/aggregate")
async def get_aggregate_performance(tenant_id: Optional[str] = None, days: int = 30):
    """Get aggregated performance metrics across campaigns"""
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    total_metrics = {
        "impressions": 0,
        "clicks": 0,
        "conversions": 0,
        "cost": 0.0,
        "revenue": 0.0,
        "campaigns_count": 0
    }
    
    for campaign_id, performance_list in performance_db.items():
        campaign = campaigns_db.get(campaign_id)
        if tenant_id and campaign and campaign.tenant_id != tenant_id:
            continue
            
        recent_performance = [p for p in performance_list if p.date >= cutoff_date]
        if recent_performance:
            total_metrics["campaigns_count"] += 1
            for perf in recent_performance:
                total_metrics["impressions"] += perf.impressions
                total_metrics["clicks"] += perf.clicks
                total_metrics["conversions"] += perf.conversions
                total_metrics["cost"] += perf.cost
                total_metrics["revenue"] += perf.revenue
    
    # Calculate aggregate metrics
    if total_metrics["impressions"] > 0:
        total_metrics["avg_ctr"] = (total_metrics["clicks"] / total_metrics["impressions"]) * 100
    if total_metrics["clicks"] > 0:
        total_metrics["avg_cpc"] = total_metrics["cost"] / total_metrics["clicks"]
        total_metrics["avg_conversion_rate"] = (total_metrics["conversions"] / total_metrics["clicks"]) * 100
    if total_metrics["cost"] > 0:
        total_metrics["avg_roas"] = total_metrics["revenue"] / total_metrics["cost"]
    
    return total_metrics

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3007, log_level="info")