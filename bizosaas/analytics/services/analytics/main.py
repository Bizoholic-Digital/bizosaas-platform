"""
Analytics Service - BizoholicSaaS
Handles metrics collection, reporting, and dashboard generation
Port: 8003
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union
import uuid
from datetime import datetime, timedelta
import logging
from enum import Enum
import json
import asyncio

# Shared imports
import sys
import os
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from shared.database.connection import get_postgres_session, get_redis_client, init_database
from shared.database.models import Metric, Report, Dashboard
from shared.events.event_bus import EventBus, EventFactory, EventType, event_handler
from shared.auth.jwt_auth import get_current_user, UserContext, require_permission, Permission

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Analytics Service",
    description="Real-time metrics, reporting, and dashboard generation for BizoholicSaaS",
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
class MetricType(str, Enum):
    CAMPAIGN_PERFORMANCE = "campaign_performance"
    USER_ENGAGEMENT = "user_engagement" 
    SYSTEM_PERFORMANCE = "system_performance"
    FINANCIAL = "financial"
    CONVERSION = "conversion"

class ReportType(str, Enum):
    CAMPAIGN_PERFORMANCE = "campaign_performance"
    ROI_ANALYSIS = "roi_analysis"
    USER_BEHAVIOR = "user_behavior"
    SYSTEM_HEALTH = "system_health"
    CUSTOM = "custom"

class TimeRange(str, Enum):
    LAST_HOUR = "last_hour"
    LAST_24_HOURS = "last_24_hours"
    LAST_7_DAYS = "last_7_days"
    LAST_30_DAYS = "last_30_days"
    LAST_90_DAYS = "last_90_days"
    CUSTOM = "custom"

# Pydantic models
class MetricCreate(BaseModel):
    entity_type: str  # campaign, user, system, etc.
    entity_id: str
    metric_name: str
    metric_value: float
    metric_unit: Optional[str] = None
    dimensions: Dict[str, Any] = {}
    timestamp: Optional[datetime] = None

class MetricResponse(BaseModel):
    id: str
    entity_type: str
    entity_id: str
    metric_name: str
    metric_value: float
    metric_unit: Optional[str]
    dimensions: Dict[str, Any]
    timestamp: datetime
    tenant_id: str
    created_at: datetime

class MetricQuery(BaseModel):
    entity_type: Optional[str] = None
    entity_ids: Optional[List[str]] = None
    metric_names: Optional[List[str]] = None
    time_range: TimeRange = TimeRange.LAST_24_HOURS
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    aggregation: Optional[str] = "avg"  # avg, sum, count, min, max
    group_by: Optional[List[str]] = None

class ReportCreate(BaseModel):
    name: str
    report_type: ReportType
    data_source: str
    date_range_start: datetime
    date_range_end: datetime
    config: Dict[str, Any] = {}
    is_scheduled: bool = False
    schedule_config: Dict[str, Any] = {}

class ReportResponse(BaseModel):
    id: str
    name: str
    report_type: ReportType
    data_source: str
    date_range_start: datetime
    date_range_end: datetime
    report_data: Dict[str, Any]
    generated_by: str
    is_scheduled: bool
    schedule_config: Dict[str, Any]
    tenant_id: str
    created_at: datetime
    updated_at: datetime

class DashboardCreate(BaseModel):
    name: str
    description: Optional[str] = None
    widgets: List[Dict[str, Any]] = []
    layout: Dict[str, Any] = {}
    filters: Dict[str, Any] = {}
    is_shared: bool = False

class DashboardResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    widgets: List[Dict[str, Any]]
    layout: Dict[str, Any]
    filters: Dict[str, Any]
    owner_id: str
    is_shared: bool
    tenant_id: str
    created_at: datetime
    updated_at: datetime

class DashboardWidget(BaseModel):
    widget_id: str
    widget_type: str  # chart, table, metric, kpi
    title: str
    config: Dict[str, Any]
    data_source: Dict[str, Any]
    position: Dict[str, int] = {"x": 0, "y": 0, "w": 4, "h": 4}

class KPIResponse(BaseModel):
    name: str
    value: Union[int, float, str]
    unit: Optional[str]
    trend: Optional[float]  # Percentage change
    comparison_period: Optional[str]
    status: Optional[str]  # good, warning, critical

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and event bus connections"""
    global event_bus, redis_client
    
    try:
        await init_database()
        logger.info("Database connections initialized")
        
        redis_client = await get_redis_client()
        
        event_bus = EventBus(redis_client, "analytics")
        await event_bus.initialize()
        await event_bus.start()
        logger.info("Event bus initialized")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown of connections"""
    global event_bus
    
    if event_bus:
        await event_bus.stop()
    logger.info("Analytics Service shutdown complete")

# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "analytics",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    try:
        async with get_postgres_session("analytics") as session:
            await session.execute("SELECT 1")
        
        await redis_client.ping()
        
        return {
            "status": "ready",
            "service": "analytics",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )

# Metrics endpoints
@app.post("/metrics", response_model=MetricResponse)
async def record_metric(
    metric_data: MetricCreate,
    current_user: UserContext = Depends(require_permission(Permission.ANALYTICS_CREATE))
):
    """Record a new metric"""
    
    try:
        async with get_postgres_session("analytics") as session:
            new_metric = Metric(
                id=uuid.uuid4(),
                entity_type=metric_data.entity_type,
                entity_id=uuid.UUID(metric_data.entity_id),
                metric_name=metric_data.metric_name,
                metric_value=metric_data.metric_value,
                metric_unit=metric_data.metric_unit,
                dimensions=metric_data.dimensions,
                timestamp=metric_data.timestamp or datetime.utcnow(),
                tenant_id=uuid.UUID(current_user.tenant_id)
            )
            
            session.add(new_metric)
            await session.commit()
            await session.refresh(new_metric)
            
            # Cache metric in Redis for real-time access
            metric_key = f"metric:{current_user.tenant_id}:{metric_data.entity_type}:{metric_data.metric_name}:{metric_data.entity_id}"
            await redis_client.zadd(
                metric_key,
                {str(new_metric.metric_value): new_metric.timestamp.timestamp()}
            )
            await redis_client.expire(metric_key, 86400 * 7)  # 7 days TTL
            
            # Publish metric recorded event
            event = EventFactory.metric_recorded(
                tenant_id=current_user.tenant_id,
                entity_id=metric_data.entity_id,
                metric_name=metric_data.metric_name,
                value=metric_data.metric_value
            )
            await event_bus.publish(event)
            
            return MetricResponse(
                id=str(new_metric.id),
                entity_type=new_metric.entity_type,
                entity_id=str(new_metric.entity_id),
                metric_name=new_metric.metric_name,
                metric_value=new_metric.metric_value,
                metric_unit=new_metric.metric_unit,
                dimensions=new_metric.dimensions,
                timestamp=new_metric.timestamp,
                tenant_id=str(new_metric.tenant_id),
                created_at=new_metric.created_at
            )
            
    except Exception as e:
        logger.error(f"Record metric error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record metric"
        )

@app.post("/metrics/query")
async def query_metrics(
    query: MetricQuery,
    current_user: UserContext = Depends(require_permission(Permission.ANALYTICS_READ))
):
    """Query metrics with aggregation and filtering"""
    
    try:
        async with get_postgres_session("analytics") as session:
            from sqlalchemy import select, func
            
            # Build base query
            stmt = select(Metric).where(
                Metric.tenant_id == uuid.UUID(current_user.tenant_id)
            )
            
            # Apply filters
            if query.entity_type:
                stmt = stmt.where(Metric.entity_type == query.entity_type)
            
            if query.entity_ids:
                entity_uuids = [uuid.UUID(eid) for eid in query.entity_ids]
                stmt = stmt.where(Metric.entity_id.in_(entity_uuids))
            
            if query.metric_names:
                stmt = stmt.where(Metric.metric_name.in_(query.metric_names))
            
            # Apply time range
            if query.time_range != TimeRange.CUSTOM:
                end_date = datetime.utcnow()
                if query.time_range == TimeRange.LAST_HOUR:
                    start_date = end_date - timedelta(hours=1)
                elif query.time_range == TimeRange.LAST_24_HOURS:
                    start_date = end_date - timedelta(days=1)
                elif query.time_range == TimeRange.LAST_7_DAYS:
                    start_date = end_date - timedelta(days=7)
                elif query.time_range == TimeRange.LAST_30_DAYS:
                    start_date = end_date - timedelta(days=30)
                elif query.time_range == TimeRange.LAST_90_DAYS:
                    start_date = end_date - timedelta(days=90)
            else:
                start_date = query.start_date
                end_date = query.end_date
            
            if start_date and end_date:
                stmt = stmt.where(
                    Metric.timestamp >= start_date,
                    Metric.timestamp <= end_date
                )
            
            # Execute query
            result = await session.execute(stmt.order_by(Metric.timestamp.desc()).limit(1000))
            metrics = result.scalars().all()
            
            # Apply aggregation if specified
            if query.aggregation and len(metrics) > 0:
                aggregated_data = await apply_aggregation(metrics, query.aggregation, query.group_by)
                return {
                    "aggregated_data": aggregated_data,
                    "total_records": len(metrics),
                    "query_params": query.dict()
                }
            
            return {
                "metrics": [
                    MetricResponse(
                        id=str(metric.id),
                        entity_type=metric.entity_type,
                        entity_id=str(metric.entity_id),
                        metric_name=metric.metric_name,
                        metric_value=metric.metric_value,
                        metric_unit=metric.metric_unit,
                        dimensions=metric.dimensions,
                        timestamp=metric.timestamp,
                        tenant_id=str(metric.tenant_id),
                        created_at=metric.created_at
                    ) for metric in metrics
                ],
                "total_records": len(metrics),
                "query_params": query.dict()
            }
            
    except Exception as e:
        logger.error(f"Query metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to query metrics"
        )

async def apply_aggregation(metrics: List[Metric], aggregation: str, group_by: Optional[List[str]]) -> Dict[str, Any]:
    """Apply aggregation to metrics data"""
    
    if not group_by:
        # Simple aggregation across all metrics
        values = [m.metric_value for m in metrics]
        
        if aggregation == "sum":
            result = sum(values)
        elif aggregation == "avg":
            result = sum(values) / len(values) if values else 0
        elif aggregation == "count":
            result = len(values)
        elif aggregation == "min":
            result = min(values) if values else 0
        elif aggregation == "max":
            result = max(values) if values else 0
        else:
            result = 0
        
        return {"aggregated_value": result, "count": len(values)}
    
    # Group by specified fields and aggregate
    groups = {}
    for metric in metrics:
        group_key_parts = []
        
        for group_field in group_by:
            if group_field == "entity_type":
                group_key_parts.append(metric.entity_type)
            elif group_field == "metric_name":
                group_key_parts.append(metric.metric_name)
            elif group_field in metric.dimensions:
                group_key_parts.append(str(metric.dimensions[group_field]))
            else:
                group_key_parts.append("unknown")
        
        group_key = "|".join(group_key_parts)
        
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(metric.metric_value)
    
    # Apply aggregation to each group
    aggregated_groups = {}
    for group_key, values in groups.items():
        if aggregation == "sum":
            aggregated_groups[group_key] = sum(values)
        elif aggregation == "avg":
            aggregated_groups[group_key] = sum(values) / len(values)
        elif aggregation == "count":
            aggregated_groups[group_key] = len(values)
        elif aggregation == "min":
            aggregated_groups[group_key] = min(values)
        elif aggregation == "max":
            aggregated_groups[group_key] = max(values)
    
    return {
        "groups": aggregated_groups,
        "group_by": group_by,
        "total_groups": len(aggregated_groups)
    }

# KPI endpoints
@app.get("/kpis")
async def get_kpis(
    current_user: UserContext = Depends(require_permission(Permission.ANALYTICS_READ)),
    time_range: TimeRange = TimeRange.LAST_30_DAYS
):
    """Get key performance indicators for tenant"""
    
    try:
        # Calculate time range
        end_date = datetime.utcnow()
        if time_range == TimeRange.LAST_24_HOURS:
            start_date = end_date - timedelta(days=1)
            comparison_start = start_date - timedelta(days=1)
        elif time_range == TimeRange.LAST_7_DAYS:
            start_date = end_date - timedelta(days=7)
            comparison_start = start_date - timedelta(days=7)
        elif time_range == TimeRange.LAST_30_DAYS:
            start_date = end_date - timedelta(days=30)
            comparison_start = start_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=30)
            comparison_start = start_date - timedelta(days=30)
        
        kpis = []
        
        # Get campaign performance KPIs
        campaign_kpis = await calculate_campaign_kpis(
            current_user.tenant_id, start_date, end_date, comparison_start
        )
        kpis.extend(campaign_kpis)
        
        # Get user engagement KPIs
        engagement_kpis = await calculate_engagement_kpis(
            current_user.tenant_id, start_date, end_date, comparison_start
        )
        kpis.extend(engagement_kpis)
        
        # Get financial KPIs
        financial_kpis = await calculate_financial_kpis(
            current_user.tenant_id, start_date, end_date, comparison_start
        )
        kpis.extend(financial_kpis)
        
        return {
            "kpis": kpis,
            "time_range": time_range.value,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Get KPIs error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate KPIs"
        )

async def calculate_campaign_kpis(tenant_id: str, start_date: datetime, end_date: datetime, comparison_start: datetime) -> List[KPIResponse]:
    """Calculate campaign performance KPIs"""
    
    kpis = []
    
    try:
        async with get_postgres_session("analytics") as session:
            from sqlalchemy import select, func
            
            # Active campaigns count
            campaign_stmt = select(func.count()).select_from(
                select(Metric).where(
                    Metric.tenant_id == uuid.UUID(tenant_id),
                    Metric.metric_name == "campaign_active",
                    Metric.timestamp >= start_date,
                    Metric.timestamp <= end_date
                ).subquery()
            )
            
            result = await session.execute(campaign_stmt)
            active_campaigns = result.scalar() or 0
            
            kpis.append(KPIResponse(
                name="Active Campaigns",
                value=active_campaigns,
                unit="campaigns",
                trend=None,  # Would calculate from comparison period
                comparison_period=None,
                status="good" if active_campaigns > 0 else "warning"
            ))
            
            # Total impressions
            impressions_stmt = select(func.sum(Metric.metric_value)).where(
                Metric.tenant_id == uuid.UUID(tenant_id),
                Metric.metric_name == "impressions",
                Metric.timestamp >= start_date,
                Metric.timestamp <= end_date
            )
            
            result = await session.execute(impressions_stmt)
            total_impressions = result.scalar() or 0
            
            kpis.append(KPIResponse(
                name="Total Impressions",
                value=int(total_impressions),
                unit="impressions",
                trend=None,
                comparison_period=None,
                status="good" if total_impressions > 1000 else "warning"
            ))
            
            # Click-through rate
            clicks_stmt = select(func.sum(Metric.metric_value)).where(
                Metric.tenant_id == uuid.UUID(tenant_id),
                Metric.metric_name == "clicks",
                Metric.timestamp >= start_date,
                Metric.timestamp <= end_date
            )
            
            result = await session.execute(clicks_stmt)
            total_clicks = result.scalar() or 0
            
            ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            
            kpis.append(KPIResponse(
                name="Click-Through Rate",
                value=round(ctr, 2),
                unit="%",
                trend=None,
                comparison_period=None,
                status="good" if ctr > 2.0 else "warning" if ctr > 1.0 else "critical"
            ))
            
    except Exception as e:
        logger.error(f"Calculate campaign KPIs error: {e}")
    
    return kpis

async def calculate_engagement_kpis(tenant_id: str, start_date: datetime, end_date: datetime, comparison_start: datetime) -> List[KPIResponse]:
    """Calculate user engagement KPIs"""
    
    kpis = []
    
    try:
        # Simulate engagement metrics
        kpis.extend([
            KPIResponse(
                name="Daily Active Users",
                value=125,
                unit="users",
                trend=12.5,
                comparison_period="previous_period",
                status="good"
            ),
            KPIResponse(
                name="Session Duration",
                value=8.5,
                unit="minutes",
                trend=-5.2,
                comparison_period="previous_period",
                status="warning"
            ),
            KPIResponse(
                name="Feature Adoption Rate",
                value=67.8,
                unit="%",
                trend=23.1,
                comparison_period="previous_period",
                status="good"
            )
        ])
        
    except Exception as e:
        logger.error(f"Calculate engagement KPIs error: {e}")
    
    return kpis

async def calculate_financial_kpis(tenant_id: str, start_date: datetime, end_date: datetime, comparison_start: datetime) -> List[KPIResponse]:
    """Calculate financial KPIs"""
    
    kpis = []
    
    try:
        # Simulate financial metrics
        kpis.extend([
            KPIResponse(
                name="Total Revenue",
                value=15420.50,
                unit="USD",
                trend=18.7,
                comparison_period="previous_period",
                status="good"
            ),
            KPIResponse(
                name="Cost Per Acquisition",
                value=45.20,
                unit="USD",
                trend=-8.3,
                comparison_period="previous_period",
                status="good"
            ),
            KPIResponse(
                name="Return on Ad Spend",
                value=3.8,
                unit="x",
                trend=15.4,
                comparison_period="previous_period",
                status="good"
            )
        ])
        
    except Exception as e:
        logger.error(f"Calculate financial KPIs error: {e}")
    
    return kpis

# Report endpoints
@app.post("/reports", response_model=ReportResponse)
async def generate_report(
    report_data: ReportCreate,
    background_tasks: BackgroundTasks,
    current_user: UserContext = Depends(require_permission(Permission.REPORT_GENERATE))
):
    """Generate a new report"""
    
    try:
        async with get_postgres_session("analytics") as session:
            new_report = Report(
                id=uuid.uuid4(),
                name=report_data.name,
                report_type=report_data.report_type.value,
                data_source=report_data.data_source,
                date_range_start=report_data.date_range_start,
                date_range_end=report_data.date_range_end,
                report_data={},  # Will be populated by background task
                generated_by=uuid.UUID(current_user.user_id),
                is_scheduled=report_data.is_scheduled,
                schedule_config=report_data.schedule_config,
                tenant_id=uuid.UUID(current_user.tenant_id)
            )
            
            session.add(new_report)
            await session.commit()
            await session.refresh(new_report)
            
            # Schedule report generation as background task
            background_tasks.add_task(
                generate_report_data,
                str(new_report.id),
                report_data.report_type,
                report_data.config
            )
            
            # Publish report generation event
            event = EventFactory.report_generated(
                tenant_id=current_user.tenant_id,
                report_id=str(new_report.id),
                report_data={
                    "name": new_report.name,
                    "type": new_report.report_type,
                    "generated_by": current_user.user_id
                }
            )
            await event_bus.publish(event)
            
            return ReportResponse(
                id=str(new_report.id),
                name=new_report.name,
                report_type=ReportType(new_report.report_type),
                data_source=new_report.data_source,
                date_range_start=new_report.date_range_start,
                date_range_end=new_report.date_range_end,
                report_data=new_report.report_data,
                generated_by=str(new_report.generated_by),
                is_scheduled=new_report.is_scheduled,
                schedule_config=new_report.schedule_config,
                tenant_id=str(new_report.tenant_id),
                created_at=new_report.created_at,
                updated_at=new_report.updated_at
            )
            
    except Exception as e:
        logger.error(f"Generate report error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate report"
        )

async def generate_report_data(report_id: str, report_type: ReportType, config: Dict[str, Any]):
    """Background task to generate report data"""
    
    try:
        # Simulate report generation
        await asyncio.sleep(3)
        
        if report_type == ReportType.CAMPAIGN_PERFORMANCE:
            report_data = {
                "summary": {
                    "total_campaigns": 12,
                    "active_campaigns": 8,
                    "total_impressions": 125430,
                    "total_clicks": 3210,
                    "total_conversions": 87,
                    "total_spend": 5420.50,
                    "average_ctr": 2.56,
                    "average_cpc": 1.69,
                    "conversion_rate": 2.71
                },
                "campaigns": [
                    {
                        "id": "campaign_1",
                        "name": "Summer Sale 2024",
                        "impressions": 45230,
                        "clicks": 1150,
                        "conversions": 32,
                        "spend": 1950.00,
                        "ctr": 2.54,
                        "conversion_rate": 2.78,
                        "roas": 4.2
                    },
                    {
                        "id": "campaign_2",
                        "name": "Product Launch Campaign",
                        "impressions": 32100,
                        "clicks": 890,
                        "conversions": 25,
                        "spend": 1420.30,
                        "ctr": 2.77,
                        "conversion_rate": 2.81,
                        "roas": 3.8
                    }
                ],
                "trends": {
                    "daily_performance": [
                        {"date": "2024-01-01", "impressions": 4500, "clicks": 115, "conversions": 3},
                        {"date": "2024-01-02", "impressions": 4800, "clicks": 125, "conversions": 4},
                        {"date": "2024-01-03", "impressions": 5200, "clicks": 140, "conversions": 5}
                    ]
                }
            }
        elif report_type == ReportType.ROI_ANALYSIS:
            report_data = {
                "summary": {
                    "total_revenue": 18750.00,
                    "total_spend": 5420.50,
                    "net_profit": 13329.50,
                    "roi_percentage": 245.8,
                    "average_order_value": 215.52,
                    "customer_acquisition_cost": 62.30
                },
                "channel_performance": [
                    {"channel": "Google Ads", "spend": 2500.00, "revenue": 9500.00, "roi": 280.0},
                    {"channel": "Facebook Ads", "spend": 1800.00, "revenue": 6200.00, "roi": 244.4},
                    {"channel": "LinkedIn Ads", "spend": 1120.50, "revenue": 3050.00, "roi": 172.2}
                ]
            }
        else:
            report_data = {"status": "generated", "message": "Custom report data would be generated here"}
        
        # Update report with generated data
        async with get_postgres_session("analytics") as session:
            from sqlalchemy import select
            stmt = select(Report).where(Report.id == uuid.UUID(report_id))
            result = await session.execute(stmt)
            report = result.scalar_one_or_none()
            
            if report:
                report.report_data = report_data
                report.updated_at = datetime.utcnow()
                await session.commit()
        
    except Exception as e:
        logger.error(f"Generate report data error: {e}")

# Dashboard endpoints
@app.post("/dashboards", response_model=DashboardResponse)
async def create_dashboard(
    dashboard_data: DashboardCreate,
    current_user: UserContext = Depends(require_permission(Permission.DASHBOARD_MANAGE))
):
    """Create a new dashboard"""
    
    try:
        async with get_postgres_session("analytics") as session:
            new_dashboard = Dashboard(
                id=uuid.uuid4(),
                name=dashboard_data.name,
                description=dashboard_data.description,
                widgets=dashboard_data.widgets,
                layout=dashboard_data.layout,
                filters=dashboard_data.filters,
                owner_id=uuid.UUID(current_user.user_id),
                is_shared=dashboard_data.is_shared,
                tenant_id=uuid.UUID(current_user.tenant_id)
            )
            
            session.add(new_dashboard)
            await session.commit()
            await session.refresh(new_dashboard)
            
            return DashboardResponse(
                id=str(new_dashboard.id),
                name=new_dashboard.name,
                description=new_dashboard.description,
                widgets=new_dashboard.widgets,
                layout=new_dashboard.layout,
                filters=new_dashboard.filters,
                owner_id=str(new_dashboard.owner_id),
                is_shared=new_dashboard.is_shared,
                tenant_id=str(new_dashboard.tenant_id),
                created_at=new_dashboard.created_at,
                updated_at=new_dashboard.updated_at
            )
            
    except Exception as e:
        logger.error(f"Create dashboard error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create dashboard"
        )

@app.get("/dashboards", response_model=List[DashboardResponse])
async def list_dashboards(
    current_user: UserContext = Depends(require_permission(Permission.ANALYTICS_READ))
):
    """List dashboards for current user/tenant"""
    
    try:
        async with get_postgres_session("analytics") as session:
            from sqlalchemy import select, or_
            
            stmt = select(Dashboard).where(
                Dashboard.tenant_id == uuid.UUID(current_user.tenant_id),
                Dashboard.is_active == True,
                or_(
                    Dashboard.owner_id == uuid.UUID(current_user.user_id),
                    Dashboard.is_shared == True
                )
            ).order_by(Dashboard.created_at.desc())
            
            result = await session.execute(stmt)
            dashboards = result.scalars().all()
            
            return [
                DashboardResponse(
                    id=str(dashboard.id),
                    name=dashboard.name,
                    description=dashboard.description,
                    widgets=dashboard.widgets,
                    layout=dashboard.layout,
                    filters=dashboard.filters,
                    owner_id=str(dashboard.owner_id),
                    is_shared=dashboard.is_shared,
                    tenant_id=str(dashboard.tenant_id),
                    created_at=dashboard.created_at,
                    updated_at=dashboard.updated_at
                ) for dashboard in dashboards
            ]
            
    except Exception as e:
        logger.error(f"List dashboards error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list dashboards"
        )

# Event handlers
@event_handler(EventType.CAMPAIGN_STARTED)
async def handle_campaign_started(event):
    """Handle campaign started - record metrics"""
    try:
        # Record campaign start metric
        await record_metric(
            MetricCreate(
                entity_type="campaign",
                entity_id=event.data.get("campaign_id"),
                metric_name="campaign_started",
                metric_value=1,
                dimensions={"campaign_name": event.data.get("name", "Unknown")}
            ),
            None  # This is from event handler, skip auth
        )
    except Exception as e:
        logger.error(f"Error handling campaign started event: {e}")

@event_handler(EventType.USER_LOGIN)
async def handle_user_login(event):
    """Handle user login - record engagement metrics"""
    try:
        # Record user login metric
        metric_data = MetricCreate(
            entity_type="user",
            entity_id=event.user_id,
            metric_name="user_login",
            metric_value=1,
            dimensions={"login_method": "password"}  # Could be extracted from event
        )
        
        # Would need to bypass auth for event handlers in real implementation
        logger.info(f"User login metric recorded for user {event.user_id}")
        
    except Exception as e:
        logger.error(f"Error handling user login event: {e}")

# Real-time metrics endpoint
@app.get("/metrics/realtime")
async def get_realtime_metrics(
    current_user: UserContext = Depends(require_permission(Permission.ANALYTICS_READ)),
    metric_names: Optional[str] = None
):
    """Get real-time metrics from Redis cache"""
    
    try:
        if metric_names:
            requested_metrics = metric_names.split(",")
        else:
            requested_metrics = ["impressions", "clicks", "conversions", "active_users"]
        
        realtime_data = {}
        
        for metric_name in requested_metrics:
            # Get latest values from Redis sorted sets
            metric_pattern = f"metric:{current_user.tenant_id}:*:{metric_name}:*"
            keys = await redis_client.keys(metric_pattern)
            
            total_value = 0
            latest_values = []
            
            for key in keys:
                # Get latest values (last hour)
                latest = await redis_client.zrangebyscore(
                    key,
                    min=(datetime.utcnow() - timedelta(hours=1)).timestamp(),
                    max=datetime.utcnow().timestamp(),
                    withscores=True
                )
                
                if latest:
                    for value, timestamp in latest:
                        latest_values.append({
                            "value": float(value),
                            "timestamp": datetime.fromtimestamp(timestamp).isoformat()
                        })
                        total_value += float(value)
            
            realtime_data[metric_name] = {
                "current_total": total_value,
                "latest_values": sorted(latest_values, key=lambda x: x["timestamp"])[-10:],  # Last 10 values
                "last_updated": datetime.utcnow().isoformat()
            }
        
        return {
            "realtime_metrics": realtime_data,
            "generated_at": datetime.utcnow().isoformat(),
            "tenant_id": current_user.tenant_id
        }
        
    except Exception as e:
        logger.error(f"Get realtime metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get realtime metrics"
        )

# Metrics endpoint for Prometheus
@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return {
        "service": "analytics",
        "metrics": {
            "total_metrics_recorded": 0,
            "reports_generated": 0,
            "dashboards_created": 0,
            "active_realtime_streams": 0
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)