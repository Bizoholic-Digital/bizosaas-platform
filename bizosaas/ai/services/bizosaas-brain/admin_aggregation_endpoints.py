"""
Admin Aggregation API Endpoints
Provides cross-platform data aggregation for BizOSaaS Admin Dashboard
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/brain/admin", tags=["Admin Aggregation"])


# Pydantic Models
class PlatformStats(BaseModel):
    platform: str
    total_users: int
    active_users_24h: int
    total_revenue: float
    total_orders: int
    total_leads: int
    active_campaigns: int


class SystemHealth(BaseModel):
    service: str
    status: str
    uptime_hours: float
    last_check: datetime
    response_time_ms: float


class CrossPlatformMetrics(BaseModel):
    total_platforms: int
    platforms_online: int
    total_users: int
    total_revenue: float
    total_orders: int
    total_leads: int
    active_campaigns: int
    system_health: List[SystemHealth]


class UserActivity(BaseModel):
    user_id: str
    email: str
    last_login: datetime
    platforms_accessed: List[str]
    total_sessions: int
    current_platform: Optional[str]


class RevenueBreakdown(BaseModel):
    platform: str
    daily_revenue: float
    weekly_revenue: float
    monthly_revenue: float
    top_products: List[Dict[str, Any]]


# Mock data (replace with real database queries)
MOCK_PLATFORM_STATS = {
    "coreldove": PlatformStats(
        platform="coreldove",
        total_users=150,
        active_users_24h=45,
        total_revenue=145820.50,
        total_orders=1834,
        total_leads=0,
        active_campaigns=3
    ),
    "bizoholic": PlatformStats(
        platform="bizoholic",
        total_users=45,
        active_users_24h=12,
        total_revenue=0.0,
        total_orders=0,
        total_leads=328,
        active_campaigns=12
    ),
    "thrillring": PlatformStats(
        platform="thrillring",
        total_users=2341,
        active_users_24h=456,
        total_revenue=0.0,
        total_orders=0,
        total_leads=0,
        active_campaigns=5
    ),
    "business_directory": PlatformStats(
        platform="business_directory",
        total_users=89,
        active_users_24h=23,
        total_revenue=0.0,
        total_orders=0,
        total_leads=0,
        active_campaigns=0
    )
}

MOCK_SYSTEM_HEALTH = [
    SystemHealth(
        service="AI Central Hub",
        status="healthy",
        uptime_hours=168.5,
        last_check=datetime.now(),
        response_time_ms=45.2
    ),
    SystemHealth(
        service="Saleor E-commerce",
        status="healthy",
        uptime_hours=168.5,
        last_check=datetime.now(),
        response_time_ms=125.8
    ),
    SystemHealth(
        service="Django CRM",
        status="healthy",
        uptime_hours=168.5,
        last_check=datetime.now(),
        response_time_ms=89.3
    ),
    SystemHealth(
        service="Wagtail CMS",
        status="healthy",
        uptime_hours=168.5,
        last_check=datetime.now(),
        response_time_ms=67.1
    ),
    SystemHealth(
        service="PostgreSQL",
        status="healthy",
        uptime_hours=720.0,
        last_check=datetime.now(),
        response_time_ms=12.5
    ),
    SystemHealth(
        service="Redis Cache",
        status="healthy",
        uptime_hours=720.0,
        last_check=datetime.now(),
        response_time_ms=3.2
    )
]


@router.get("/metrics/cross-platform", response_model=CrossPlatformMetrics)
async def get_cross_platform_metrics():
    """
    Get aggregated metrics across all platforms

    Returns comprehensive metrics for admin dashboard
    """
    try:
        total_users = sum(stats.total_users for stats in MOCK_PLATFORM_STATS.values())
        total_revenue = sum(stats.total_revenue for stats in MOCK_PLATFORM_STATS.values())
        total_orders = sum(stats.total_orders for stats in MOCK_PLATFORM_STATS.values())
        total_leads = sum(stats.total_leads for stats in MOCK_PLATFORM_STATS.values())
        active_campaigns = sum(stats.active_campaigns for stats in MOCK_PLATFORM_STATS.values())

        return CrossPlatformMetrics(
            total_platforms=4,
            platforms_online=4,
            total_users=total_users,
            total_revenue=total_revenue,
            total_orders=total_orders,
            total_leads=total_leads,
            active_campaigns=active_campaigns,
            system_health=MOCK_SYSTEM_HEALTH
        )

    except Exception as e:
        logger.error(f"Error getting cross-platform metrics: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving metrics")


@router.get("/platforms/{platform}/stats", response_model=PlatformStats)
async def get_platform_stats(platform: str):
    """
    Get detailed statistics for a specific platform

    Returns user counts, revenue, orders, leads, and campaigns
    """
    try:
        if platform not in MOCK_PLATFORM_STATS:
            raise HTTPException(status_code=404, detail=f"Platform {platform} not found")

        return MOCK_PLATFORM_STATS[platform]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting platform stats for {platform}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving platform stats")


@router.get("/platforms/all/stats")
async def get_all_platform_stats():
    """
    Get statistics for all platforms

    Returns array of platform statistics
    """
    try:
        return {
            "success": True,
            "platforms": list(MOCK_PLATFORM_STATS.values()),
            "total_platforms": len(MOCK_PLATFORM_STATS)
        }
    except Exception as e:
        logger.error(f"Error getting all platform stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving platform stats")


@router.get("/system/health")
async def get_system_health():
    """
    Get health status of all backend services

    Returns service health, uptime, and response times
    """
    try:
        healthy_count = sum(1 for service in MOCK_SYSTEM_HEALTH if service.status == "healthy")

        return {
            "success": True,
            "overall_health": "healthy" if healthy_count == len(MOCK_SYSTEM_HEALTH) else "degraded",
            "services": MOCK_SYSTEM_HEALTH,
            "healthy_services": healthy_count,
            "total_services": len(MOCK_SYSTEM_HEALTH),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting system health: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving system health")


@router.get("/users/activity")
async def get_user_activity(
    limit: int = 50,
    platform: Optional[str] = None
):
    """
    Get recent user activity across all platforms

    Returns user login activity and platform usage
    """
    try:
        # Mock user activity data
        activities = [
            UserActivity(
                user_id="user_001",
                email="john@example.com",
                last_login=datetime.now() - timedelta(minutes=15),
                platforms_accessed=["coreldove", "client_portal"],
                total_sessions=45,
                current_platform="coreldove"
            ),
            UserActivity(
                user_id="user_002",
                email="sarah@example.com",
                last_login=datetime.now() - timedelta(hours=2),
                platforms_accessed=["bizoholic", "client_portal"],
                total_sessions=23,
                current_platform="bizoholic"
            ),
            UserActivity(
                user_id="user_003",
                email="mike@example.com",
                last_login=datetime.now() - timedelta(hours=5),
                platforms_accessed=["thrillring"],
                total_sessions=156,
                current_platform="thrillring"
            )
        ]

        if platform:
            activities = [a for a in activities if platform in a.platforms_accessed]

        return {
            "success": True,
            "activities": activities[:limit],
            "total": len(activities),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error getting user activity: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving user activity")


@router.get("/revenue/breakdown")
async def get_revenue_breakdown():
    """
    Get revenue breakdown by platform

    Returns daily, weekly, and monthly revenue for each platform
    """
    try:
        breakdown = [
            RevenueBreakdown(
                platform="coreldove",
                daily_revenue=12450.00,
                weekly_revenue=78920.50,
                monthly_revenue=342150.75,
                top_products=[
                    {"name": "Premium Yoga Mat", "sales": 234, "revenue": 23400.00},
                    {"name": "Resistance Bands Set", "sales": 189, "revenue": 9450.00},
                    {"name": "Foam Roller", "sales": 156, "revenue": 6240.00}
                ]
            )
        ]

        return {
            "success": True,
            "breakdown": breakdown,
            "total_daily": sum(b.daily_revenue for b in breakdown),
            "total_weekly": sum(b.weekly_revenue for b in breakdown),
            "total_monthly": sum(b.monthly_revenue for b in breakdown),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error getting revenue breakdown: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving revenue breakdown")


@router.get("/analytics/summary")
async def get_analytics_summary(
    period: str = "24h"  # Options: 24h, 7d, 30d
):
    """
    Get analytics summary for specified time period

    Returns aggregated analytics across all platforms
    """
    try:
        return {
            "success": True,
            "period": period,
            "summary": {
                "total_sessions": 2341,
                "unique_users": 456,
                "avg_session_duration_mins": 12.5,
                "bounce_rate": 0.32,
                "conversion_rate": 0.045,
                "total_page_views": 12456,
                "top_pages": [
                    {"path": "/", "views": 2341, "platform": "bizoholic"},
                    {"path": "/products", "views": 1834, "platform": "coreldove"},
                    {"path": "/games", "views": 1567, "platform": "thrillring"}
                ]
            },
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving analytics summary")


@router.get("/health")
async def admin_api_health():
    """Health check for admin aggregation API"""
    return {
        "status": "healthy",
        "service": "admin-aggregation-api",
        "endpoints_available": 8
    }
