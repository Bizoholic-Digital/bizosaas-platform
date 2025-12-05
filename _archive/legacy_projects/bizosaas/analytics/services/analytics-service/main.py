"""
Analytics & Reporting Service - Domain Service for Marketing Analytics and Business Intelligence
FastAPI application handling campaign performance, ROI analysis, and automated reporting
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import io
import pandas as pd

# Import shared models and configurations
import sys
import os
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas/shared')

from configs.settings import settings


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting Analytics & Reporting Service...")
    
    # Initialize connections to data sources
    # await init_analytics_db()
    
    logger.info("Analytics service initialized successfully")
    
    yield
    
    logger.info("Analytics & Reporting Service shutdown complete")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="BizoSaaS Analytics & Reporting Service",
        description="Domain service for marketing analytics, business intelligence, and automated reporting",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app


app = create_app()


# Pydantic models for Analytics
from pydantic import BaseModel, Field
from enum import Enum


class ReportType(str, Enum):
    CAMPAIGN_PERFORMANCE = "campaign_performance"
    ROI_ANALYSIS = "roi_analysis"
    LEAD_ATTRIBUTION = "lead_attribution"
    CONVERSION_FUNNEL = "conversion_funnel"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    CUSTOM_DASHBOARD = "custom_dashboard"


class TimeRange(str, Enum):
    LAST_7_DAYS = "7d"
    LAST_30_DAYS = "30d"
    LAST_90_DAYS = "90d"
    LAST_YEAR = "1y"
    CUSTOM = "custom"


class ReportRequest(BaseModel):
    """Request for generating analytics report"""
    report_type: ReportType
    time_range: TimeRange
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    filters: Dict[str, Any] = Field(default_factory=dict)
    tenant_id: int
    format: str = "json"  # json, pdf, csv, xlsx


class CampaignMetrics(BaseModel):
    """Campaign performance metrics"""
    campaign_id: str
    campaign_name: str
    platform: str  # google_ads, meta_ads, linkedin_ads
    impressions: int
    clicks: int
    conversions: int
    spend: float
    revenue: float
    ctr: float  # Click-through rate
    cpa: float  # Cost per acquisition
    roas: float  # Return on ad spend
    quality_score: Optional[float] = None
    date_range: dict


class AnalyticsDashboard(BaseModel):
    """Analytics dashboard data"""
    overview_metrics: dict
    campaign_performance: List[CampaignMetrics]
    conversion_funnel: dict
    roi_trends: List[dict]
    top_performing_keywords: List[dict]
    geographic_performance: List[dict]
    device_performance: dict
    attribution_analysis: dict


class ROIAnalysis(BaseModel):
    """ROI analysis report"""
    total_spend: float
    total_revenue: float
    overall_roas: float
    campaigns_analyzed: int
    top_performing_campaigns: List[dict]
    underperforming_campaigns: List[dict]
    optimization_recommendations: List[str]
    projected_improvements: dict


# Health check
@app.get("/health")
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "service": "analytics-reporting",
        "version": "1.0.0",
        "features": ["campaign_analytics", "roi_analysis", "automated_reporting", "custom_dashboards"]
    }


@app.get("/dashboard", response_model=AnalyticsDashboard)
async def get_analytics_dashboard(
    tenant_id: int,
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """Get comprehensive analytics dashboard data"""
    try:
        # Calculate date range
        if time_range == TimeRange.CUSTOM and start_date and end_date:
            date_start, date_end = start_date, end_date
        else:
            days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}[time_range]
            date_end = datetime.utcnow()
            date_start = date_end - timedelta(days=days)
        
        # Mock analytics data (replace with actual data queries)
        dashboard_data = AnalyticsDashboard(
            overview_metrics={
                "total_campaigns": 12,
                "total_spend": 45670.50,
                "total_revenue": 128450.25,
                "overall_roas": 2.81,
                "total_leads": 1247,
                "conversion_rate": 3.2,
                "average_cpa": 36.63,
                "active_keywords": 1834
            },
            campaign_performance=[
                CampaignMetrics(
                    campaign_id="gads_001",
                    campaign_name="Google Ads - Tech Startup Keywords",
                    platform="google_ads",
                    impressions=125000,
                    clicks=3750,
                    conversions=120,
                    spend=4500.00,
                    revenue=15600.00,
                    ctr=3.0,
                    cpa=37.50,
                    roas=3.47,
                    quality_score=8.2,
                    date_range={"start": date_start.isoformat(), "end": date_end.isoformat()}
                ),
                CampaignMetrics(
                    campaign_id="meta_002", 
                    campaign_name="Meta Ads - E-commerce Products",
                    platform="meta_ads",
                    impressions=98000,
                    clicks=2940,
                    conversions=89,
                    spend=3200.00,
                    revenue=11250.00,
                    ctr=3.0,
                    cpa=35.96,
                    roas=3.52,
                    date_range={"start": date_start.isoformat(), "end": date_end.isoformat()}
                )
            ],
            conversion_funnel={
                "impressions": 450000,
                "clicks": 13500,
                "landing_page_views": 12150,
                "leads": 1247,
                "opportunities": 342,
                "customers": 89,
                "conversion_rates": {
                    "impression_to_click": 3.0,
                    "click_to_lead": 9.2,
                    "lead_to_opportunity": 27.4,
                    "opportunity_to_customer": 26.0
                }
            },
            roi_trends=[
                {"date": "2024-01-01", "spend": 1200, "revenue": 3600, "roas": 3.0},
                {"date": "2024-01-08", "spend": 1350, "revenue": 4050, "roas": 3.0},
                {"date": "2024-01-15", "spend": 1180, "revenue": 3894, "roas": 3.3},
                {"date": "2024-01-22", "spend": 1420, "revenue": 4260, "roas": 3.0}
            ],
            top_performing_keywords=[
                {"keyword": "AI marketing software", "clicks": 1250, "conversions": 45, "cpa": 28.50},
                {"keyword": "marketing automation", "clicks": 980, "conversions": 38, "cpa": 31.20},
                {"keyword": "digital marketing platform", "clicks": 890, "conversions": 29, "cpa": 41.50}
            ],
            geographic_performance=[
                {"location": "California", "impressions": 45000, "clicks": 1350, "conversions": 42},
                {"location": "New York", "impressions": 38000, "clicks": 1140, "conversions": 35},
                {"location": "Texas", "impressions": 29000, "clicks": 870, "conversions": 28}
            ],
            device_performance={
                "desktop": {"impressions": 200000, "clicks": 6000, "conversions": 180, "cpa": 35.00},
                "mobile": {"impressions": 180000, "clicks": 5400, "conversions": 135, "cpa": 38.50},
                "tablet": {"impressions": 70000, "clicks": 2100, "conversions": 52, "cpa": 42.30}
            },
            attribution_analysis={
                "first_touch": {"google_ads": 45, "meta_ads": 32, "linkedin_ads": 18, "organic": 25},
                "last_touch": {"google_ads": 52, "meta_ads": 28, "linkedin_ads": 15, "organic": 15},
                "multi_touch": {"assisted_conversions": 156, "direct_conversions": 89}
            }
        )
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Failed to get analytics dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics dashboard")


@app.get("/roi-analysis", response_model=ROIAnalysis)
async def get_roi_analysis(
    tenant_id: int,
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    campaign_ids: Optional[List[str]] = None
):
    """Get detailed ROI analysis"""
    try:
        # Mock ROI analysis (replace with actual calculations)
        roi_analysis = ROIAnalysis(
            total_spend=45670.50,
            total_revenue=128450.25,
            overall_roas=2.81,
            campaigns_analyzed=12,
            top_performing_campaigns=[
                {
                    "campaign_id": "gads_001",
                    "name": "Google Ads - Tech Keywords",
                    "spend": 4500.00,
                    "revenue": 15600.00,
                    "roas": 3.47,
                    "roi_percentage": 247
                },
                {
                    "campaign_id": "meta_002",
                    "name": "Meta Ads - E-commerce",
                    "spend": 3200.00,
                    "revenue": 11250.00, 
                    "roas": 3.52,
                    "roi_percentage": 252
                }
            ],
            underperforming_campaigns=[
                {
                    "campaign_id": "linkedin_003",
                    "name": "LinkedIn - B2B Services",
                    "spend": 2800.00,
                    "revenue": 3920.00,
                    "roas": 1.40,
                    "roi_percentage": 40
                }
            ],
            optimization_recommendations=[
                "Increase budget allocation to Google Ads campaigns (ROAS: 3.47)",
                "Optimize Meta Ads targeting to improve conversion rate",
                "Review LinkedIn campaign keywords and audiences",
                "Implement dayparting to reduce costs during low-conversion hours",
                "Test new ad creative formats for underperforming campaigns"
            ],
            projected_improvements={
                "budget_reallocation_impact": {"additional_revenue": 8500, "improved_roas": 3.15},
                "creative_optimization_impact": {"conversion_lift": "15-25%", "cpa_reduction": "8-12%"},
                "audience_refinement_impact": {"quality_score_improvement": 1.2, "ctr_increase": "18%"}
            }
        )
        
        return roi_analysis
        
    except Exception as e:
        logger.error(f"Failed to get ROI analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve ROI analysis")


@app.post("/reports/generate")
async def generate_report(
    report_request: ReportRequest,
    background_tasks: BackgroundTasks
):
    """Generate custom analytics report"""
    try:
        report_id = f"report_{report_request.tenant_id}_{report_request.report_type}_{int(datetime.utcnow().timestamp())}"
        
        # Start report generation in background
        background_tasks.add_task(
            generate_report_task,
            report_id,
            report_request
        )
        
        return {
            "success": True,
            "report_id": report_id,
            "status": "generating",
            "estimated_completion": "2-5 minutes",
            "message": f"{report_request.report_type.replace('_', ' ').title()} report generation started"
        }
        
    except Exception as e:
        logger.error(f"Failed to start report generation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start report generation")


@app.get("/reports/{report_id}/status")
async def get_report_status(report_id: str, tenant_id: int):
    """Get report generation status"""
    # Mock status (replace with actual status tracking)
    return {
        "report_id": report_id,
        "status": "completed",
        "progress": 100,
        "download_url": f"/reports/{report_id}/download",
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat()
    }


@app.get("/reports/{report_id}/download")
async def download_report(report_id: str, tenant_id: int, format: str = "pdf"):
    """Download generated report"""
    try:
        if format == "csv":
            # Generate CSV report
            data = {
                "Campaign Name": ["Google Ads - Tech", "Meta Ads - Ecommerce"],
                "Spend": [4500.00, 3200.00],
                "Revenue": [15600.00, 11250.00],
                "ROAS": [3.47, 3.52]
            }
            df = pd.DataFrame(data)
            
            # Create CSV content
            csv_content = df.to_csv(index=False)
            
            return StreamingResponse(
                io.StringIO(csv_content),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={report_id}.csv"}
            )
            
        elif format == "json":
            # Generate JSON report
            report_data = {
                "report_id": report_id,
                "generated_at": datetime.utcnow().isoformat(),
                "data": {
                    "campaigns": [
                        {"name": "Google Ads - Tech", "spend": 4500.00, "revenue": 15600.00, "roas": 3.47},
                        {"name": "Meta Ads - Ecommerce", "spend": 3200.00, "revenue": 11250.00, "roas": 3.52}
                    ]
                }
            }
            
            return JSONResponse(content=report_data)
            
        else:
            raise HTTPException(status_code=400, detail="Unsupported format. Use 'csv' or 'json'")
            
    except Exception as e:
        logger.error(f"Failed to download report {report_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to download report")


@app.get("/campaigns/{campaign_id}/performance")
async def get_campaign_performance(
    campaign_id: str,
    tenant_id: int,
    time_range: TimeRange = TimeRange.LAST_30_DAYS
):
    """Get detailed performance metrics for a specific campaign"""
    # Mock campaign performance data
    return {
        "campaign_id": campaign_id,
        "campaign_name": "Google Ads - Tech Startup Keywords",
        "platform": "google_ads",
        "status": "active",
        "performance_summary": {
            "impressions": 125000,
            "clicks": 3750,
            "conversions": 120,
            "spend": 4500.00,
            "revenue": 15600.00,
            "ctr": 3.0,
            "cpa": 37.50,
            "roas": 3.47
        },
        "daily_performance": [
            {"date": "2024-01-01", "impressions": 4200, "clicks": 126, "spend": 150.00, "conversions": 4},
            {"date": "2024-01-02", "impressions": 4100, "clicks": 123, "spend": 147.00, "conversions": 3},
        ],
        "keyword_performance": [
            {"keyword": "AI marketing software", "impressions": 12500, "clicks": 375, "conversions": 15, "cpa": 30.00},
            {"keyword": "marketing automation", "impressions": 9800, "clicks": 294, "conversions": 12, "cpa": 35.50}
        ],
        "audience_insights": {
            "top_demographics": [
                {"age_range": "25-34", "percentage": 35, "conversions": 42},
                {"age_range": "35-44", "percentage": 28, "conversions": 34}
            ],
            "geographic_performance": [
                {"location": "California", "impressions": 35000, "conversions": 35},
                {"location": "New York", "impressions": 28000, "conversions": 28}
            ]
        }
    }


# Background task functions
async def generate_report_task(report_id: str, report_request: ReportRequest):
    """Background task to generate analytics report"""
    try:
        logger.info(f"Starting report generation: {report_id}")
        
        # Simulate report generation time
        await asyncio.sleep(10)  # Replace with actual report generation
        
        # Generate report data based on type
        if report_request.report_type == ReportType.CAMPAIGN_PERFORMANCE:
            await generate_campaign_performance_report(report_id, report_request)
        elif report_request.report_type == ReportType.ROI_ANALYSIS:
            await generate_roi_analysis_report(report_id, report_request)
        # Add other report types...
        
        logger.info(f"Completed report generation: {report_id}")
        
    except Exception as e:
        logger.error(f"Failed to generate report {report_id}: {str(e)}")


async def generate_campaign_performance_report(report_id: str, request: ReportRequest):
    """Generate campaign performance report"""
    # Implementation for campaign performance report
    pass


async def generate_roi_analysis_report(report_id: str, request: ReportRequest):
    """Generate ROI analysis report"""
    # Implementation for ROI analysis report  
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)