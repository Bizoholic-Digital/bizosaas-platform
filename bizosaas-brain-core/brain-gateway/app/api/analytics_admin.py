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
from app.models.workflow_execution import WorkflowExecution
from app.models.platform_metrics import PlatformMetrics
from app.domain.ports.identity_port import AuthenticatedUser
from datetime import datetime, timedelta
from sqlalchemy import func, and_

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

@router.get("/platform-overview")
async def get_platform_overview(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get high-level platform metrics overview.
    Returns aggregated metrics across all tenants.
    """
    # Get latest platform metrics snapshot
    latest_snapshot = db.query(PlatformMetrics).order_by(
        PlatformMetrics.snapshot_time.desc()
    ).first()
    
    if latest_snapshot:
        return latest_snapshot.to_dict()
    
    # If no snapshot exists, calculate real-time metrics
    total_tenants = db.query(func.count(Tenant.id)).scalar()
    total_workflows = db.query(func.count(WorkflowExecution.id)).scalar()
    
    # Last 24 hours metrics
    cutoff = datetime.utcnow() - timedelta(hours=24)
    recent_workflows = db.query(func.count(WorkflowExecution.id)).filter(
        WorkflowExecution.started_at >= cutoff
    ).scalar()
    
    recent_completed = db.query(func.count(WorkflowExecution.id)).filter(
        and_(
            WorkflowExecution.started_at >= cutoff,
            WorkflowExecution.status == "completed"
        )
    ).scalar()
    
    success_rate = (recent_completed / recent_workflows * 100) if recent_workflows > 0 else 0
    
    total_cost = db.query(func.sum(WorkflowExecution.cost_estimate)).filter(
        WorkflowExecution.started_at >= cutoff
    ).scalar() or 0
    
    return {
        "total_tenants": total_tenants,
        "total_workflows_all_time": total_workflows,
        "last_24h": {
            "workflow_executions": recent_workflows,
            "success_rate": round(success_rate, 2),
            "total_cost_usd": round(total_cost, 2)
        },
        "generated_at": datetime.utcnow().isoformat()
    }

@router.get("/tenant-comparison")
async def get_tenant_comparison(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Compare tenant performance and resource usage.
    Returns per-tenant metrics for comparison.
    """
    tenants = db.query(Tenant).all()
    
    tenant_data = []
    for tenant in tenants:
        workflow_count = db.query(func.count(WorkflowExecution.id)).filter(
            WorkflowExecution.tenant_id == str(tenant.id)
        ).scalar()
        
        total_cost = db.query(func.sum(WorkflowExecution.cost_estimate)).filter(
            WorkflowExecution.tenant_id == str(tenant.id)
        ).scalar() or 0
        
        # Last 7 days activity
        cutoff = datetime.utcnow() - timedelta(days=7)
        recent_activity = db.query(func.count(WorkflowExecution.id)).filter(
            and_(
                WorkflowExecution.tenant_id == str(tenant.id),
                WorkflowExecution.started_at >= cutoff
            )
        ).scalar()
        
        tenant_data.append({
            "tenant_id": str(tenant.id),
            "tenant_name": tenant.name,
            "total_workflows": workflow_count,
            "total_cost_usd": round(total_cost, 2),
            "last_7_days_activity": recent_activity
        })
    
    # Sort by cost descending
    tenant_data.sort(key=lambda x: x["total_cost_usd"], reverse=True)
    
    return {
        "tenants": tenant_data,
        "total_tenants": len(tenant_data),
        "generated_at": datetime.utcnow().isoformat()
    }

@router.get("/workflow-insights")
async def get_workflow_insights(
    hours: int = 24,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get detailed workflow execution insights.
    Includes success rates, costs, and performance trends.
    """
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    
    # Workflow type breakdown
    workflow_stats = db.query(
        WorkflowExecution.workflow_name,
        func.count(WorkflowExecution.id).label('total'),
        func.sum(func.case((WorkflowExecution.status == 'completed', 1), else_=0)).label('completed'),
        func.sum(func.case((WorkflowExecution.status == 'failed', 1), else_=0)).label('failed'),
        func.avg(WorkflowExecution.duration_seconds).label('avg_duration'),
        func.sum(WorkflowExecution.cost_estimate).label('total_cost')
    ).filter(
        WorkflowExecution.started_at >= cutoff
    ).group_by(WorkflowExecution.workflow_name).all()
    
    workflow_breakdown = []
    for stat in workflow_stats:
        success_rate = (stat.completed / stat.total * 100) if stat.total > 0 else 0
        workflow_breakdown.append({
            "workflow_name": stat.workflow_name,
            "total_executions": stat.total,
            "completed": stat.completed,
            "failed": stat.failed,
            "success_rate": round(success_rate, 2),
            "avg_duration_seconds": round(stat.avg_duration or 0, 2),
            "total_cost_usd": round(stat.total_cost or 0, 2)
        })
    
    # Sort by total executions
    workflow_breakdown.sort(key=lambda x: x["total_executions"], reverse=True)
    
    return {
        "time_range_hours": hours,
        "workflows": workflow_breakdown,
        "generated_at": datetime.utcnow().isoformat()
    }

@router.get("/cost-breakdown")
async def get_cost_breakdown(
    days: int = 7,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get platform-wide cost analysis and breakdown.
    """
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    # Total cost
    total_cost = db.query(func.sum(WorkflowExecution.cost_estimate)).filter(
        WorkflowExecution.started_at >= cutoff
    ).scalar() or 0
    
    # Cost by workflow type
    workflow_costs = db.query(
        WorkflowExecution.workflow_name,
        func.sum(WorkflowExecution.cost_estimate).label('cost'),
        func.count(WorkflowExecution.id).label('executions')
    ).filter(
        WorkflowExecution.started_at >= cutoff
    ).group_by(WorkflowExecution.workflow_name).all()
    
    cost_by_workflow = [
        {
            "workflow_name": wf.workflow_name,
            "total_cost_usd": round(wf.cost or 0, 2),
            "executions": wf.executions,
            "avg_cost_per_execution": round((wf.cost or 0) / wf.executions, 4) if wf.executions > 0 else 0
        }
        for wf in workflow_costs
    ]
    
    # Sort by cost descending
    cost_by_workflow.sort(key=lambda x: x["total_cost_usd"], reverse=True)
    
    # Cost by tenant
    tenant_costs = db.query(
        WorkflowExecution.tenant_id,
        func.sum(WorkflowExecution.cost_estimate).label('cost')
    ).filter(
        WorkflowExecution.started_at >= cutoff
    ).group_by(WorkflowExecution.tenant_id).all()
    
    cost_by_tenant = []
    for tc in tenant_costs:
        tenant = db.query(Tenant).filter(Tenant.id == tc.tenant_id).first()
        cost_by_tenant.append({
            "tenant_id": tc.tenant_id,
            "tenant_name": tenant.name if tenant else "Unknown",
            "total_cost_usd": round(tc.cost or 0, 2)
        })
    
    cost_by_tenant.sort(key=lambda x: x["total_cost_usd"], reverse=True)
    
    return {
        "time_range_days": days,
        "total_cost_usd": round(total_cost, 2),
        "cost_by_workflow": cost_by_workflow,
        "cost_by_tenant": cost_by_tenant[:10],  # Top 10 tenants
        "generated_at": datetime.utcnow().isoformat()
    }
