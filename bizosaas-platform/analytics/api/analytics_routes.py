"""
Analytics API Routes for BizOSaaS Platform

FastAPI routes for unified cross-platform analytics and reporting.
Provides comprehensive analytics dashboards, AI-powered insights, and predictive analytics.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import get_db_session
from shared.enhanced_tenant_context import EnhancedTenantContext, PlatformType, TenantTier
from shared.rls_manager import RLSManager
from ai.services.bizosaas_brain.tenant_aware_ai_coordinator import TenantAwareAICoordinator
from analytics.services.unified_analytics_service import (
    UnifiedAnalyticsService,
    AnalyticsDashboard,
    AnalyticsQuery,
    MetricType,
    TimeRange,
    CrossPlatformInsight,
    PredictiveAnalytics
)
from security.compliance_framework import get_security_context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

# Global service instances (initialized on startup)
analytics_service: Optional[UnifiedAnalyticsService] = None
rls_manager: Optional[RLSManager] = None
ai_coordinator: Optional[TenantAwareAICoordinator] = None

class AnalyticsRequest(BaseModel):
    """Request model for analytics queries"""
    platforms: List[PlatformType] = Field(default_factory=list)
    metrics: List[MetricType] = Field(default_factory=list)
    time_range: TimeRange = TimeRange.LAST_30_DAYS
    custom_start: Optional[datetime] = None
    custom_end: Optional[datetime] = None
    filters: Dict[str, Any] = Field(default_factory=dict)
    aggregation: str = "daily"
    include_predictions: bool = False

class DashboardResponse(BaseModel):
    """Response model for analytics dashboard"""
    success: bool = True
    dashboard: AnalyticsDashboard
    generation_time_ms: int
    cached: bool = False

class InsightsResponse(BaseModel):
    """Response model for AI insights"""
    success: bool = True
    insights: List[CrossPlatformInsight]
    total_insights: int
    generation_time_ms: int

class PredictionsResponse(BaseModel):
    """Response model for predictive analytics"""
    success: bool = True
    predictions: List[PredictiveAnalytics]
    total_predictions: int
    generation_time_ms: int

class ExportRequest(BaseModel):
    """Request model for data export"""
    format: str = "csv"  # csv, json, excel
    platforms: List[PlatformType] = Field(default_factory=list)
    time_range: TimeRange = TimeRange.LAST_30_DAYS
    include_insights: bool = True
    include_predictions: bool = False

async def get_tenant_context(request: Request) -> EnhancedTenantContext:
    """Extract tenant context from request"""
    # In a real implementation, this would extract tenant info from JWT token
    # For now, using headers for development
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID required")

    # Mock tenant context for development
    # In production, this would be retrieved from database/cache
    from shared.enhanced_tenant_context import PlatformAccess, AIAgentContext

    return EnhancedTenantContext(
        tenant_id=tenant_id,
        platform_access={
            PlatformType.BIZOHOLIC: PlatformAccess(enabled=True, subscription_level="enterprise"),
            PlatformType.CORELDOVE: PlatformAccess(enabled=True, subscription_level="professional"),
            PlatformType.BUSINESS_DIRECTORY: PlatformAccess(enabled=True, subscription_level="starter"),
            PlatformType.THRILLRING: PlatformAccess(enabled=True, subscription_level="professional"),
            PlatformType.QUANTTRADE: PlatformAccess(enabled=True, subscription_level="enterprise")
        },
        ai_context=AIAgentContext(
            enabled_agents=["data_analyst", "business_intelligence", "growth_strategist"],
            max_concurrent_agents=10,
            ai_budget_limit=1000.0
        ),
        subscription_tier=TenantTier.ENTERPRISE
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "analytics", "timestamp": datetime.utcnow()}

@router.post("/dashboard", response_model=DashboardResponse)
async def get_analytics_dashboard(
    request: AnalyticsRequest,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get comprehensive analytics dashboard with cross-platform metrics
    """
    start_time = datetime.utcnow()

    try:
        # Validate subscription tier access
        if tenant_context.subscription_tier == TenantTier.FREE and len(request.platforms) > 1:
            raise HTTPException(
                status_code=403,
                detail="Multi-platform analytics requires paid subscription"
            )

        # Build analytics query
        query = AnalyticsQuery(
            tenant_id=tenant_context.tenant_id,
            platforms=request.platforms,
            metrics=request.metrics,
            time_range=request.time_range,
            custom_start=request.custom_start,
            custom_end=request.custom_end,
            filters=request.filters,
            aggregation=request.aggregation,
            include_predictions=request.include_predictions
        )

        # Generate dashboard
        dashboard = await analytics_service.build_unified_dashboard(
            session=session,
            tenant_context=tenant_context,
            query=query
        )

        generation_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        return DashboardResponse(
            dashboard=dashboard,
            generation_time_ms=generation_time
        )

    except Exception as e:
        logger.error(f"Error generating analytics dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate dashboard: {str(e)}")

@router.post("/insights", response_model=InsightsResponse)
async def get_ai_insights(
    request: AnalyticsRequest,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get AI-powered cross-platform insights and recommendations
    """
    start_time = datetime.utcnow()

    try:
        # Validate AI access
        if not tenant_context.ai_context.enabled_agents:
            raise HTTPException(
                status_code=403,
                detail="AI insights require AI agent access"
            )

        # Build analytics query
        query = AnalyticsQuery(
            tenant_id=tenant_context.tenant_id,
            platforms=request.platforms,
            metrics=request.metrics,
            time_range=request.time_range,
            custom_start=request.custom_start,
            custom_end=request.custom_end,
            filters=request.filters,
            aggregation=request.aggregation
        )

        # Collect platform data
        platform_data = await analytics_service.collect_platform_data(
            session=session,
            tenant_context=tenant_context,
            query=query
        )

        # Generate platform metrics
        platform_metrics = await analytics_service.generate_platform_metrics(platform_data)

        # Generate AI insights
        insights = await analytics_service.generate_ai_insights(
            platform_data=platform_data,
            platform_metrics=platform_metrics,
            tenant_context=tenant_context
        )

        generation_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        return InsightsResponse(
            insights=insights,
            total_insights=len(insights),
            generation_time_ms=generation_time
        )

    except Exception as e:
        logger.error(f"Error generating AI insights: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")

@router.post("/predictions", response_model=PredictionsResponse)
async def get_predictive_analytics(
    request: AnalyticsRequest,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get predictive analytics and forecasting
    """
    start_time = datetime.utcnow()

    try:
        # Validate subscription tier for predictions
        if tenant_context.subscription_tier in [TenantTier.FREE, TenantTier.STARTER]:
            raise HTTPException(
                status_code=403,
                detail="Predictive analytics requires Professional or higher subscription"
            )

        # Build analytics query
        query = AnalyticsQuery(
            tenant_id=tenant_context.tenant_id,
            platforms=request.platforms,
            metrics=request.metrics,
            time_range=request.time_range,
            custom_start=request.custom_start,
            custom_end=request.custom_end,
            filters=request.filters,
            aggregation=request.aggregation,
            include_predictions=True
        )

        # Collect platform data
        platform_data = await analytics_service.collect_platform_data(
            session=session,
            tenant_context=tenant_context,
            query=query
        )

        # Generate predictions
        predictions = await analytics_service.generate_predictive_analytics(
            platform_data=platform_data,
            tenant_context=tenant_context
        )

        generation_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        return PredictionsResponse(
            predictions=predictions,
            total_predictions=len(predictions),
            generation_time_ms=generation_time
        )

    except Exception as e:
        logger.error(f"Error generating predictions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate predictions: {str(e)}")

@router.get("/platforms")
async def get_available_platforms(
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
):
    """
    Get available platforms for tenant
    """
    accessible_platforms = []

    for platform, access in tenant_context.platform_access.items():
        if access.enabled:
            accessible_platforms.append({
                "platform": platform.value,
                "enabled": access.enabled,
                "subscription_level": access.subscription_level,
                "features": access.features
            })

    return {
        "success": True,
        "platforms": accessible_platforms,
        "total_platforms": len(accessible_platforms)
    }

@router.get("/metrics")
async def get_available_metrics():
    """
    Get available metric types
    """
    return {
        "success": True,
        "metrics": [
            {"type": metric.value, "description": metric.value.replace("_", " ").title()}
            for metric in MetricType
        ]
    }

@router.post("/export")
async def export_analytics_data(
    request: ExportRequest,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Export analytics data in various formats
    """
    try:
        # Build analytics query
        query = AnalyticsQuery(
            tenant_id=tenant_context.tenant_id,
            platforms=request.platforms,
            time_range=request.time_range,
            include_predictions=request.include_predictions
        )

        # Collect platform data
        platform_data = await analytics_service.collect_platform_data(
            session=session,
            tenant_context=tenant_context,
            query=query
        )

        # Generate export data based on format
        if request.format == "csv":
            export_data = await _generate_csv_export(platform_data, request)
            media_type = "text/csv"
            filename = f"analytics_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"

        elif request.format == "json":
            export_data = await _generate_json_export(platform_data, request)
            media_type = "application/json"
            filename = f"analytics_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

        elif request.format == "excel":
            export_data = await _generate_excel_export(platform_data, request)
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            filename = f"analytics_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.xlsx"

        else:
            raise HTTPException(status_code=400, detail="Unsupported export format")

        return StreamingResponse(
            export_data,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        logger.error(f"Error exporting analytics data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to export data: {str(e)}")

@router.get("/realtime/{platform}")
async def get_realtime_metrics(
    platform: PlatformType,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get real-time metrics for specific platform
    """
    try:
        # Validate platform access
        platform_access = tenant_context.platform_access.get(platform)
        if not platform_access or not platform_access.enabled:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied to {platform.value} platform"
            )

        # Get last 24 hours of data
        query = AnalyticsQuery(
            tenant_id=tenant_context.tenant_id,
            platforms=[platform],
            time_range=TimeRange.LAST_24_HOURS,
            aggregation="hourly"
        )

        platform_data = await analytics_service.collect_platform_data(
            session=session,
            tenant_context=tenant_context,
            query=query
        )

        # Format for real-time display
        realtime_data = []
        if platform in platform_data:
            for point in platform_data[platform][-10:]:  # Last 10 data points
                realtime_data.append({
                    "timestamp": point.timestamp.isoformat(),
                    "metric": point.metric_name,
                    "value": point.value,
                    "dimensions": point.dimensions
                })

        return {
            "success": True,
            "platform": platform.value,
            "data": realtime_data,
            "last_updated": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error getting real-time metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get real-time metrics: {str(e)}")

# Helper functions for data export

async def _generate_csv_export(platform_data, request: ExportRequest):
    """Generate CSV export"""
    import io
    import csv

    output = io.StringIO()
    writer = csv.writer(output)

    # Write headers
    writer.writerow(["Platform", "Timestamp", "Metric Type", "Metric Name", "Value", "Dimensions"])

    # Write data
    for platform, data_points in platform_data.items():
        for point in data_points:
            writer.writerow([
                platform.value,
                point.timestamp.isoformat(),
                point.metric_type.value,
                point.metric_name,
                point.value,
                str(point.dimensions)
            ])

    output.seek(0)
    return io.BytesIO(output.getvalue().encode('utf-8'))

async def _generate_json_export(platform_data, request: ExportRequest):
    """Generate JSON export"""
    import io

    export_data = {
        "export_timestamp": datetime.utcnow().isoformat(),
        "platforms": {}
    }

    for platform, data_points in platform_data.items():
        export_data["platforms"][platform.value] = [
            {
                "timestamp": point.timestamp.isoformat(),
                "metric_type": point.metric_type.value,
                "metric_name": point.metric_name,
                "value": point.value,
                "dimensions": point.dimensions
            }
            for point in data_points
        ]

    json_str = json.dumps(export_data, indent=2, default=str)
    return io.BytesIO(json_str.encode('utf-8'))

async def _generate_excel_export(platform_data, request: ExportRequest):
    """Generate Excel export"""
    import io
    import pandas as pd

    # Create Excel writer
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Create summary sheet
        summary_data = []
        for platform, data_points in platform_data.items():
            summary_data.append({
                "Platform": platform.value,
                "Total Data Points": len(data_points),
                "Date Range": f"{min(p.timestamp for p in data_points)} to {max(p.timestamp for p in data_points)}" if data_points else "No data"
            })

        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name="Summary", index=False)

        # Create individual platform sheets
        for platform, data_points in platform_data.items():
            if data_points:
                platform_data_list = []
                for point in data_points:
                    platform_data_list.append({
                        "Timestamp": point.timestamp,
                        "Metric Type": point.metric_type.value,
                        "Metric Name": point.metric_name,
                        "Value": point.value,
                        "Dimensions": str(point.dimensions)
                    })

                platform_df = pd.DataFrame(platform_data_list)
                platform_df.to_excel(writer, sheet_name=platform.value[:31], index=False)  # Excel sheet name limit

    output.seek(0)
    return output

# Initialize analytics service
async def initialize_analytics_service(app):
    """Initialize analytics service on startup"""
    global analytics_service, rls_manager, ai_coordinator

    # Initialize services
    rls_manager = RLSManager()
    ai_coordinator = TenantAwareAICoordinator(rls_manager)
    analytics_service = UnifiedAnalyticsService(rls_manager, ai_coordinator)

    logger.info("Analytics service initialized successfully")

# Export router and initialization function
__all__ = ["router", "initialize_analytics_service"]