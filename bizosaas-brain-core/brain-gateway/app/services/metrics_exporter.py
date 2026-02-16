"""
Prometheus metrics exporter for platform analytics.

Exports workflow, tenant, and campaign metrics in Prometheus format
for visualization in Grafana.
"""

import logging
from typing import Dict, Any
from datetime import datetime, timedelta

from prometheus_client import Gauge, Counter, Histogram, Info, CollectorRegistry
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.dependencies import get_db
from app.models.workflow_execution import WorkflowExecution
from app.models.user import Tenant
from app.models.campaign import Campaign, CampaignAnalytics
from app.models.platform_metrics import PlatformMetrics

logger = logging.getLogger(__name__)

# Create a custom registry for platform metrics
platform_registry = CollectorRegistry()

# Workflow metrics
workflow_executions_total = Counter(
    'platform_workflow_executions_total',
    'Total number of workflow executions',
    ['workflow_type', 'status'],
    registry=platform_registry
)

workflow_duration_seconds = Histogram(
    'platform_workflow_duration_seconds',
    'Workflow execution duration in seconds',
    ['workflow_type'],
    buckets=[1, 5, 10, 30, 60, 120, 300, 600, 1800, 3600],
    registry=platform_registry
)

workflow_cost_usd = Histogram(
    'platform_workflow_cost_usd',
    'Workflow execution cost in USD',
    ['workflow_type'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0],
    registry=platform_registry
)

workflow_success_rate = Gauge(
    'platform_workflow_success_rate',
    'Workflow success rate (0-1)',
    ['workflow_type'],
    registry=platform_registry
)

# Tenant metrics
tenant_total = Gauge(
    'platform_tenants_total',
    'Total number of tenants',
    registry=platform_registry
)

tenant_workflow_executions = Gauge(
    'platform_tenant_workflow_executions',
    'Number of workflow executions per tenant',
    ['tenant_id', 'tenant_name'],
    registry=platform_registry
)

tenant_cost_usd = Gauge(
    'platform_tenant_cost_usd',
    'Total cost per tenant in USD',
    ['tenant_id', 'tenant_name'],
    registry=platform_registry
)

tenant_active_campaigns = Gauge(
    'platform_tenant_active_campaigns',
    'Number of active campaigns per tenant',
    ['tenant_id', 'tenant_name'],
    registry=platform_registry
)

# Campaign metrics
campaign_total = Gauge(
    'platform_campaigns_total',
    'Total number of campaigns',
    ['status'],
    registry=platform_registry
)

campaign_impressions_total = Counter(
    'platform_campaign_impressions_total',
    'Total campaign impressions',
    registry=platform_registry
)

campaign_clicks_total = Counter(
    'platform_campaign_clicks_total',
    'Total campaign clicks',
    registry=platform_registry
)

campaign_conversions_total = Counter(
    'platform_campaign_conversions_total',
    'Total campaign conversions',
    registry=platform_registry
)

campaign_ctr = Gauge(
    'platform_campaign_ctr',
    'Platform-wide click-through rate',
    registry=platform_registry
)

campaign_conversion_rate = Gauge(
    'platform_campaign_conversion_rate',
    'Platform-wide conversion rate',
    registry=platform_registry
)

# Platform overview metrics
platform_info = Info(
    'platform_info',
    'Platform information',
    registry=platform_registry
)


class MetricsExporter:
    """Exports platform metrics to Prometheus."""
    
    def __init__(self):
        """Initialize metrics exporter."""
        self.registry = platform_registry
    
    async def update_workflow_metrics(self, time_range_hours: int = 24) -> None:
        """
        Update workflow execution metrics.
        
        Args:
            time_range_hours: Hours to look back for metrics
        """
        try:
            db: Session = next(get_db())
            cutoff_time = datetime.utcnow() - timedelta(hours=time_range_hours)
            
            # Get workflow executions by type and status
            executions = db.query(
                WorkflowExecution.workflow_name,
                WorkflowExecution.status,
                func.count(WorkflowExecution.id).label('count'),
                func.avg(WorkflowExecution.duration_seconds).label('avg_duration'),
                func.sum(WorkflowExecution.cost_usd).label('total_cost')
            ).filter(
                WorkflowExecution.started_at >= cutoff_time
            ).group_by(
                WorkflowExecution.workflow_name,
                WorkflowExecution.status
            ).all()
            
            # Update counters and gauges
            for exec_data in executions:
                workflow_type = exec_data.workflow_name or "unknown"
                status = exec_data.status or "unknown"
                
                # Update execution counter
                workflow_executions_total.labels(
                    workflow_type=workflow_type,
                    status=status
                ).inc(exec_data.count)
                
                # Update duration histogram
                if exec_data.avg_duration:
                    workflow_duration_seconds.labels(
                        workflow_type=workflow_type
                    ).observe(exec_data.avg_duration)
                
                # Update cost histogram
                if exec_data.total_cost:
                    workflow_cost_usd.labels(
                        workflow_type=workflow_type
                    ).observe(exec_data.total_cost)
            
            # Calculate success rates per workflow type
            workflow_stats = db.query(
                WorkflowExecution.workflow_name,
                func.count(WorkflowExecution.id).label('total'),
                func.sum(func.case((WorkflowExecution.status == 'completed', 1), else_=0)).label('completed')
            ).filter(
                WorkflowExecution.started_at >= cutoff_time
            ).group_by(
                WorkflowExecution.workflow_name
            ).all()
            
            for stat in workflow_stats:
                if stat.total > 0:
                    success_rate = stat.completed / stat.total
                    workflow_success_rate.labels(
                        workflow_type=stat.workflow_name or "unknown"
                    ).set(success_rate)
            
            db.close()
            logger.info(f"Updated workflow metrics for last {time_range_hours} hours")
            
        except Exception as e:
            logger.error(f"Failed to update workflow metrics: {e}")
    
    async def update_tenant_metrics(self) -> None:
        """Update tenant usage metrics."""
        try:
            db: Session = next(get_db())
            
            # Get total tenants
            total_tenants = db.query(func.count(Tenant.id)).scalar()
            tenant_total.set(total_tenants)
            
            # Get per-tenant metrics
            tenants = db.query(Tenant).all()
            
            for tenant in tenants:
                # Workflow executions
                workflow_count = db.query(func.count(WorkflowExecution.id)).filter(
                    WorkflowExecution.tenant_id == tenant.id
                ).scalar() or 0
                
                tenant_workflow_executions.labels(
                    tenant_id=str(tenant.id),
                    tenant_name=tenant.name
                ).set(workflow_count)
                
                # Total cost
                total_cost = db.query(func.sum(WorkflowExecution.cost_usd)).filter(
                    WorkflowExecution.tenant_id == tenant.id
                ).scalar() or 0.0
                
                tenant_cost_usd.labels(
                    tenant_id=str(tenant.id),
                    tenant_name=tenant.name
                ).set(total_cost)
                
                # Active campaigns
                active_campaigns = db.query(func.count(Campaign.id)).filter(
                    Campaign.tenant_id == tenant.id,
                    Campaign.status == 'active'
                ).scalar() or 0
                
                tenant_active_campaigns.labels(
                    tenant_id=str(tenant.id),
                    tenant_name=tenant.name
                ).set(active_campaigns)
            
            db.close()
            logger.info("Updated tenant metrics")
            
        except Exception as e:
            logger.error(f"Failed to update tenant metrics: {e}")
    
    async def update_campaign_metrics(self) -> None:
        """Update campaign performance metrics."""
        try:
            db: Session = next(get_db())
            
            # Campaign counts by status
            campaign_statuses = db.query(
                Campaign.status,
                func.count(Campaign.id).label('count')
            ).group_by(Campaign.status).all()
            
            for status_data in campaign_statuses:
                campaign_total.labels(
                    status=status_data.status or "unknown"
                ).set(status_data.count)
            
            # Aggregate campaign analytics
            analytics = db.query(
                func.sum(CampaignAnalytics.impressions).label('total_impressions'),
                func.sum(CampaignAnalytics.clicks).label('total_clicks'),
                func.sum(CampaignAnalytics.conversions).label('total_conversions')
            ).first()
            
            if analytics:
                total_impressions = analytics.total_impressions or 0
                total_clicks = analytics.total_clicks or 0
                total_conversions = analytics.total_conversions or 0
                
                # Update counters
                campaign_impressions_total.inc(total_impressions)
                campaign_clicks_total.inc(total_clicks)
                campaign_conversions_total.inc(total_conversions)
                
                # Calculate rates
                ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
                conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
                
                campaign_ctr.set(ctr)
                campaign_conversion_rate.set(conversion_rate)
            
            db.close()
            logger.info("Updated campaign metrics")
            
        except Exception as e:
            logger.error(f"Failed to update campaign metrics: {e}")
    
    async def update_platform_info(self) -> None:
        """Update platform information metric."""
        try:
            db: Session = next(get_db())
            
            # Get latest platform metrics snapshot
            latest_snapshot = db.query(PlatformMetrics).order_by(
                PlatformMetrics.snapshot_time.desc()
            ).first()
            
            info_data = {
                'version': '1.0.0',
                'environment': 'production',
                'last_snapshot': latest_snapshot.snapshot_time.isoformat() if latest_snapshot else 'never'
            }
            
            platform_info.info(info_data)
            
            db.close()
            logger.info("Updated platform info")
            
        except Exception as e:
            logger.error(f"Failed to update platform info: {e}")
    
    async def update_all_metrics(self, time_range_hours: int = 24) -> None:
        """
        Update all platform metrics.
        
        Args:
            time_range_hours: Hours to look back for workflow metrics
        """
        await self.update_workflow_metrics(time_range_hours)
        await self.update_tenant_metrics()
        await self.update_campaign_metrics()
        await self.update_platform_info()
        logger.info("All platform metrics updated")


# Global metrics exporter instance
metrics_exporter = MetricsExporter()


async def get_metrics_exporter() -> MetricsExporter:
    """
    Get the global metrics exporter instance.
    
    Returns:
        MetricsExporter instance
    """
    return metrics_exporter
