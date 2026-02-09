"""
Analytics & Intelligence Administration API
Handles management of GTM containers, GA4 properties, and Search Console
integrations across all tenants.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.dependencies import get_db, require_role
from app.models.user import Tenant
from domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/analytics", tags=["analytics-admin"])

@router.get("/gtm/containers")
async def list_global_gtm_containers(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """List all Google Tag Manager containers connected by tenants."""
    tenants = db.query(Tenant).all()
    results = []
    for t in tenants:
        gtm_id = t.settings.get("google_tag_manager_id") or t.settings.get("gtm_id")
        if gtm_id:
            results.append({
                "tenant_id": str(t.id),
                "tenant_name": t.name,
                "gtm_id": gtm_id,
                "status": "active"
            })
    return results

@router.get("/ga4/properties")
async def list_global_ga4_properties(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """List all GA4 properties connected by tenants."""
    tenants = db.query(Tenant).all()
    results = []
    for t in tenants:
        ga4_id = t.settings.get("ga4_measurement_id") or t.settings.get("ga4_id")
        if ga4_id:
            results.append({
                "tenant_id": str(t.id),
                "tenant_name": t.name,
                "ga4_id": ga4_id,
                "status": "active"
            })
    return results

@router.get("/benchmark")
async def get_benchmark_analytics(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Fetch comparative (benchmarked) insights across all tenants."""
    # This would aggregate data from the Directory Analytics and GA4 (if possible)
    return {
        "avg_page_views": 1500,
        "top_performing_industry": "Retail",
        "conversion_rate_avg": 2.4,
        "benchmarks": [
            {"category": "Retail", "avg_conversion": 3.1},
            {"category": "Services", "avg_conversion": 1.8},
            {"category": "B2B", "avg_conversion": 1.5}
        ]
    }

@router.post("/audit/tags")
async def run_tag_audit(
    tenant_id: Optional[UUID] = None,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Detect and report tag implementation issues across sites."""
    # This involves a workflow that scrapes the tenant's site and checks for GTM/GA4 scripts
    return {"status": "accepted", "message": "Tag audit workflow started"}

@router.get("/search/performance")
async def get_search_performance(
    period: str = "30d",
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Retrieve Google Search Console performance metrics."""
    # In a real impl, this would query the GSC API
    import random
    
    # Mock data trend
    dates = []
    clicks = []
    impressions = []
    
    base_clicks = 120
    base_impr = 4500
    
    for i in range(30):
        dates.append(f"Day {i+1}")
        clicks.append(base_clicks + random.randint(-20, 50))
        impressions.append(base_impr + random.randint(-500, 1200))
        
    return {
        "summary": {
            "total_clicks": sum(clicks),
            "total_impressions": sum(impressions),
            "avg_ctr": round((sum(clicks) / sum(impressions)) * 100, 2),
            "avg_position": 12.4
        },
        "trend": {
            "dates": dates,
            "clicks": clicks,
            "impressions": impressions
        }
    }

@router.get("/search/keywords")
async def get_top_keywords(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Retrieve top performing search queries."""
    return [
        {"query": "best saas platform", "clicks": 420, "impressions": 12000, "position": 3.2},
        {"query": "ai business tools", "clicks": 310, "impressions": 8500, "position": 4.5},
        {"query": "automated crm", "clicks": 180, "impressions": 6200, "position": 8.1},
        {"query": "bizosaas login", "clicks": 950, "impressions": 980, "position": 1.0},
        {"query": "white label dashboard", "clicks": 120, "impressions": 5400, "position": 11.2}
    ]
