"""
Analytics Activities for Multi-tenant Dashboard
Aggregates platform-wide metrics across all tenants.
"""

from temporalio import activity
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging

from app.dependencies import get_db
from app.models.workflow_execution import WorkflowExecution
from app.models.campaign import Campaign, CampaignAnalytics
from app.models.user import Tenant
from app.models.agent import Agent, AgentOptimization

logger = logging.getLogger(__name__)


@activity.defn
async def aggregate_workflow_metrics_activity(time_range_hours: int = 24) -> Dict[str, Any]:
    """
    Aggregate workflow execution metrics across all tenants.
    
    Args:
        time_range_hours: Number of hours to look back for metrics
        
    Returns:
        Dictionary containing aggregated workflow metrics
    """
    db: Session = next(get_db())
    try:
        cutoff_time = datetime.utcnow() - timedelta(hours=time_range_hours)
        
        # Total workflow executions
        total_executions = db.query(func.count(WorkflowExecution.id)).filter(
            WorkflowExecution.started_at >= cutoff_time
        ).scalar()
        
        # Success rate
        completed = db.query(func.count(WorkflowExecution.id)).filter(
            and_(
                WorkflowExecution.started_at >= cutoff_time,
                WorkflowExecution.status == "completed"
            )
        ).scalar()
        
        failed = db.query(func.count(WorkflowExecution.id)).filter(
            and_(
                WorkflowExecution.started_at >= cutoff_time,
                WorkflowExecution.status == "failed"
            )
        ).scalar()
        
        success_rate = (completed / total_executions * 100) if total_executions > 0 else 0
        
        # Average duration
        avg_duration = db.query(func.avg(WorkflowExecution.duration_seconds)).filter(
            and_(
                WorkflowExecution.started_at >= cutoff_time,
                WorkflowExecution.status == "completed"
            )
        ).scalar() or 0
        
        # Total cost
        total_cost = db.query(func.sum(WorkflowExecution.cost_estimate)).filter(
            WorkflowExecution.started_at >= cutoff_time
        ).scalar() or 0
        
        # Workflow type breakdown
        workflow_breakdown = db.query(
            WorkflowExecution.workflow_name,
            func.count(WorkflowExecution.id).label('count')
        ).filter(
            WorkflowExecution.started_at >= cutoff_time
        ).group_by(WorkflowExecution.workflow_name).all()
        
        return {
            "total_executions": total_executions,
            "completed": completed,
            "failed": failed,
            "success_rate": round(success_rate, 2),
            "avg_duration_seconds": round(avg_duration, 2),
            "total_cost_usd": round(total_cost, 2),
            "workflow_breakdown": [
                {"workflow_name": name, "count": count}
                for name, count in workflow_breakdown
            ],
            "time_range_hours": time_range_hours,
            "generated_at": datetime.utcnow().isoformat()
        }
    finally:
        db.close()


@activity.defn
async def aggregate_tenant_usage_activity() -> Dict[str, Any]:
    """
    Calculate per-tenant resource usage and costs.
    
    Returns:
        Dictionary containing tenant usage metrics
    """
    db: Session = next(get_db())
    try:
        tenants = db.query(Tenant).all()
        
        tenant_metrics = []
        for tenant in tenants:
            # Workflow executions for this tenant
            workflow_count = db.query(func.count(WorkflowExecution.id)).filter(
                WorkflowExecution.tenant_id == str(tenant.id)
            ).scalar()
            
            # Total cost for this tenant
            tenant_cost = db.query(func.sum(WorkflowExecution.cost_estimate)).filter(
                WorkflowExecution.tenant_id == str(tenant.id)
            ).scalar() or 0
            
            # Active campaigns
            active_campaigns = db.query(func.count(Campaign.id)).filter(
                and_(
                    Campaign.tenant_id == tenant.id,
                    Campaign.status == "active"
                )
            ).scalar()
            
            # Custom agents
            custom_agents = db.query(func.count(Agent.id)).filter(
                Agent.tenant_id == str(tenant.id)
            ).scalar()
            
            tenant_metrics.append({
                "tenant_id": str(tenant.id),
                "tenant_name": tenant.name,
                "workflow_executions": workflow_count,
                "total_cost_usd": round(tenant_cost, 2),
                "active_campaigns": active_campaigns,
                "custom_agents": custom_agents
            })
        
        # Sort by cost descending
        tenant_metrics.sort(key=lambda x: x["total_cost_usd"], reverse=True)
        
        return {
            "total_tenants": len(tenants),
            "tenant_metrics": tenant_metrics,
            "generated_at": datetime.utcnow().isoformat()
        }
    finally:
        db.close()


@activity.defn
async def aggregate_campaign_performance_activity() -> Dict[str, Any]:
    """
    Aggregate campaign performance metrics across all tenants.
    
    Returns:
        Dictionary containing campaign performance data
    """
    db: Session = next(get_db())
    try:
        # Total campaigns
        total_campaigns = db.query(func.count(Campaign.id)).scalar()
        
        # Active campaigns
        active_campaigns = db.query(func.count(Campaign.id)).filter(
            Campaign.status == "active"
        ).scalar()
        
        # Campaign analytics aggregation
        total_impressions = db.query(func.sum(CampaignAnalytics.metric_value)).filter(
            CampaignAnalytics.metric_name == "impressions"
        ).scalar() or 0
        
        total_clicks = db.query(func.sum(CampaignAnalytics.metric_value)).filter(
            CampaignAnalytics.metric_name == "clicks"
        ).scalar() or 0
        
        total_conversions = db.query(func.sum(CampaignAnalytics.metric_value)).filter(
            CampaignAnalytics.metric_name == "conversions"
        ).scalar() or 0
        
        # Calculate platform-wide CTR
        ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        
        # Conversion rate
        conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        
        return {
            "total_campaigns": total_campaigns,
            "active_campaigns": active_campaigns,
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "platform_ctr": round(ctr, 2),
            "platform_conversion_rate": round(conversion_rate, 2),
            "generated_at": datetime.utcnow().isoformat()
        }
    finally:
        db.close()


@activity.defn
async def generate_platform_insights_activity(
    workflow_metrics: Dict[str, Any],
    tenant_usage: Dict[str, Any],
    campaign_performance: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate actionable insights from aggregated platform metrics.
    
    Args:
        workflow_metrics: Aggregated workflow data
        tenant_usage: Tenant usage data
        campaign_performance: Campaign performance data
        
    Returns:
        Dictionary containing platform insights and recommendations
    """
    insights = []
    
    # Workflow insights
    if workflow_metrics["success_rate"] < 90:
        insights.append({
            "type": "warning",
            "category": "workflow_health",
            "message": f"Workflow success rate is {workflow_metrics['success_rate']}%, below the 90% target",
            "recommendation": "Review failed workflows and implement error handling improvements"
        })
    
    if workflow_metrics["avg_duration_seconds"] > 300:
        insights.append({
            "type": "optimization",
            "category": "performance",
            "message": f"Average workflow duration is {workflow_metrics['avg_duration_seconds']}s",
            "recommendation": "Consider optimizing long-running workflows or implementing caching"
        })
    
    # Cost insights
    if workflow_metrics["total_cost_usd"] > 1000:
        insights.append({
            "type": "info",
            "category": "cost",
            "message": f"Platform costs are ${workflow_metrics['total_cost_usd']} for the last {workflow_metrics['time_range_hours']} hours",
            "recommendation": "Review high-cost workflows and consider model optimization"
        })
    
    # Tenant insights
    if tenant_usage["total_tenants"] > 0:
        top_tenant = tenant_usage["tenant_metrics"][0]
        insights.append({
            "type": "info",
            "category": "tenant_usage",
            "message": f"Top tenant '{top_tenant['tenant_name']}' accounts for ${top_tenant['total_cost_usd']} in costs",
            "recommendation": "Monitor high-usage tenants for optimization opportunities"
        })
    
    # Campaign insights
    if campaign_performance["platform_ctr"] < 2.0:
        insights.append({
            "type": "optimization",
            "category": "campaign_performance",
            "message": f"Platform-wide CTR is {campaign_performance['platform_ctr']}%, below industry average",
            "recommendation": "Review campaign targeting and creative strategies"
        })
    
    return {
        "insights": insights,
        "summary": {
            "total_insights": len(insights),
            "warnings": len([i for i in insights if i["type"] == "warning"]),
            "optimizations": len([i for i in insights if i["type"] == "optimization"])
        },
        "generated_at": datetime.utcnow().isoformat()
    }
