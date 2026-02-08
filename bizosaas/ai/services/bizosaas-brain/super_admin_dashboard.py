"""
Super Admin Dashboard for BizOSaaS Platform
Provides comprehensive platform-wide control and monitoring capabilities
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field
import structlog

# Import existing components
from ai_agents_management import get_ai_agents_manager, AIAgentConfig, AgentCategory
from enhanced_tenant_management import get_enhanced_tenant_manager
from personal_ai_assistant import get_personal_ai_assistant
from event_bus_integration import publish_brain_event, BrainEventTypes

# Import unified tenant system
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from unified_tenant_middleware import UnifiedTenant

logger = structlog.get_logger(__name__)


class UserRole(str, Enum):
    """User roles for platform access control"""
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin"
    CLIENT = "client"
    DEVELOPER = "developer"
    SUPPORT = "support"


class DashboardWidget(str, Enum):
    """Available dashboard widgets"""
    TENANT_OVERVIEW = "tenant_overview"
    GLOBAL_ANALYTICS = "global_analytics"
    SYSTEM_HEALTH = "system_health"
    AI_AGENTS_STATUS = "ai_agents_status"
    PLATFORM_METRICS = "platform_metrics"
    SECURITY_MONITORING = "security_monitoring"
    REVENUE_ANALYTICS = "revenue_analytics"
    TENANT_PERFORMANCE = "tenant_performance"
    INFRASTRUCTURE_STATUS = "infrastructure_status"
    USER_ACTIVITY = "user_activity"


class PlatformMetrics(BaseModel):
    """Platform-wide metrics model"""
    total_tenants: int = 0
    active_tenants: int = 0
    total_users: int = 0
    total_ai_executions: int = 0
    success_rate: float = 0.0
    total_revenue: float = 0.0
    monthly_revenue: float = 0.0
    server_uptime: float = 0.0
    avg_response_time: float = 0.0
    storage_usage_gb: float = 0.0
    bandwidth_usage_gb: float = 0.0
    last_updated: datetime = Field(default_factory=datetime.now)


class TenantSummary(BaseModel):
    """Tenant summary for dashboard display"""
    tenant_id: str
    tenant_name: str
    slug: str
    status: str
    subscription_tier: str
    monthly_revenue: float
    user_count: int
    ai_executions_24h: int
    last_activity: Optional[datetime]
    health_score: float
    created_at: datetime


class SystemHealthStatus(BaseModel):
    """System health monitoring"""
    overall_status: str = "healthy"
    brain_api_status: str = "healthy"
    vault_status: str = "healthy"
    database_status: str = "healthy"
    redis_status: str = "healthy"
    event_bus_status: str = "healthy"
    ai_agents_status: str = "healthy"
    cms_status: str = "healthy"
    ecommerce_status: str = "healthy"
    uptime_percentage: float = 99.9
    response_time_ms: float = 150.0
    last_check: datetime = Field(default_factory=datetime.now)


class DashboardConfig(BaseModel):
    """User-specific dashboard configuration"""
    user_id: str
    user_role: UserRole
    enabled_widgets: List[DashboardWidget]
    layout_preferences: Dict[str, Any] = Field(default_factory=dict)
    refresh_intervals: Dict[str, int] = Field(default_factory=dict)
    notification_settings: Dict[str, bool] = Field(default_factory=dict)
    tenant_filters: List[str] = Field(default_factory=list)


class SuperAdminDashboard:
    """
    Comprehensive Super Admin Dashboard for BizOSaaS Platform
    
    Provides platform-wide control, monitoring, and management capabilities
    with role-based access control and real-time insights.
    """
    
    def __init__(self, vault_client=None, redis_client=None):
        self.vault_client = vault_client
        self.redis_client = redis_client
        self.logger = logger.bind(component="super_admin_dashboard")
        
        # Initialize managers
        self.ai_agents_manager = get_ai_agents_manager(vault_client, redis_client)
        self.tenant_manager = get_enhanced_tenant_manager(vault_client)
        self.ai_assistant = get_personal_ai_assistant(vault_client, None)
        
        # Dashboard configurations by role
        self.role_permissions = {
            UserRole.SUPER_ADMIN: {
                "widgets": list(DashboardWidget),
                "can_modify_tenants": True,
                "can_access_all_data": True,
                "can_manage_users": True,
                "can_configure_system": True
            },
            UserRole.TENANT_ADMIN: {
                "widgets": [
                    DashboardWidget.TENANT_PERFORMANCE,
                    DashboardWidget.AI_AGENTS_STATUS,
                    DashboardWidget.USER_ACTIVITY,
                    DashboardWidget.REVENUE_ANALYTICS
                ],
                "can_modify_tenants": False,
                "can_access_all_data": False,
                "can_manage_users": True,
                "can_configure_system": False
            },
            UserRole.CLIENT: {
                "widgets": [
                    DashboardWidget.TENANT_PERFORMANCE,
                    DashboardWidget.AI_AGENTS_STATUS
                ],
                "can_modify_tenants": False,
                "can_access_all_data": False,
                "can_manage_users": False,
                "can_configure_system": False
            }
        }
    
    async def get_dashboard_data(
        self, 
        user_role: UserRole, 
        tenant: Optional[UnifiedTenant] = None,
        widgets: Optional[List[DashboardWidget]] = None
    ) -> Dict[str, Any]:
        """Get dashboard data based on user role and permissions"""
        try:
            # Check permissions
            permissions = self.role_permissions.get(user_role, {})
            allowed_widgets = permissions.get("widgets", [])
            
            if widgets:
                # Filter requested widgets by permissions
                widgets = [w for w in widgets if w in allowed_widgets]
            else:
                widgets = allowed_widgets
            
            dashboard_data = {
                "user_role": user_role,
                "permissions": permissions,
                "widgets": {},
                "last_updated": datetime.now().isoformat()
            }
            
            # Load widget data based on permissions
            for widget in widgets:
                widget_data = await self._get_widget_data(widget, user_role, tenant)
                dashboard_data["widgets"][widget.value] = widget_data
            
            return dashboard_data
            
        except Exception as e:
            self.logger.error(f"Failed to get dashboard data: {e}")
            return {"error": str(e)}
    
    async def _get_widget_data(
        self, 
        widget: DashboardWidget, 
        user_role: UserRole, 
        tenant: Optional[UnifiedTenant]
    ) -> Dict[str, Any]:
        """Get data for a specific dashboard widget"""
        try:
            if widget == DashboardWidget.TENANT_OVERVIEW:
                return await self._get_tenant_overview(user_role, tenant)
            
            elif widget == DashboardWidget.GLOBAL_ANALYTICS:
                return await self._get_global_analytics(user_role)
            
            elif widget == DashboardWidget.SYSTEM_HEALTH:
                return await self._get_system_health()
            
            elif widget == DashboardWidget.AI_AGENTS_STATUS:
                return await self._get_ai_agents_status(tenant)
            
            elif widget == DashboardWidget.PLATFORM_METRICS:
                return await self._get_platform_metrics()
            
            elif widget == DashboardWidget.SECURITY_MONITORING:
                return await self._get_security_monitoring()
            
            elif widget == DashboardWidget.REVENUE_ANALYTICS:
                return await self._get_revenue_analytics(tenant)
            
            elif widget == DashboardWidget.TENANT_PERFORMANCE:
                return await self._get_tenant_performance(tenant)
            
            elif widget == DashboardWidget.INFRASTRUCTURE_STATUS:
                return await self._get_infrastructure_status()
            
            elif widget == DashboardWidget.USER_ACTIVITY:
                return await self._get_user_activity(tenant)
            
            else:
                return {"error": f"Unknown widget: {widget}"}
                
        except Exception as e:
            self.logger.error(f"Failed to get widget data for {widget}: {e}")
            return {"error": str(e)}
    
    async def _get_tenant_overview(
        self, 
        user_role: UserRole, 
        tenant: Optional[UnifiedTenant]
    ) -> Dict[str, Any]:
        """Get tenant overview data"""
        if user_role == UserRole.SUPER_ADMIN:
            # Super admin sees all tenants
            tenants = await self.tenant_manager.list_tenants()
            tenant_summaries = []
            
            for t in tenants:
                summary = TenantSummary(
                    tenant_id=t.tenant_id,
                    tenant_name=t.name,
                    slug=t.slug,
                    status=t.status,
                    subscription_tier=t.subscription_tier,
                    monthly_revenue=float(t.monthly_revenue or 0),
                    user_count=await self._get_tenant_user_count(t),
                    ai_executions_24h=await self._get_tenant_ai_executions(t),
                    last_activity=await self._get_tenant_last_activity(t),
                    health_score=await self._calculate_tenant_health(t),
                    created_at=t.created_at
                )
                tenant_summaries.append(summary.model_dump())
            
            return {
                "total_tenants": len(tenants),
                "active_tenants": len([t for t in tenants if t.status == "active"]),
                "tenant_summaries": tenant_summaries
            }
        
        elif tenant:
            # Tenant admin sees only their tenant
            summary = TenantSummary(
                tenant_id=tenant.tenant_id,
                tenant_name=tenant.name,
                slug=tenant.slug,
                status=tenant.status,
                subscription_tier=tenant.subscription_tier,
                monthly_revenue=float(tenant.monthly_revenue or 0),
                user_count=await self._get_tenant_user_count(tenant),
                ai_executions_24h=await self._get_tenant_ai_executions(tenant),
                last_activity=await self._get_tenant_last_activity(tenant),
                health_score=await self._calculate_tenant_health(tenant),
                created_at=tenant.created_at
            )
            
            return {
                "tenant_summary": summary.model_dump()
            }
        
        return {"error": "No tenant access"}
    
    async def _get_global_analytics(self, user_role: UserRole) -> Dict[str, Any]:
        """Get global platform analytics"""
        if user_role != UserRole.SUPER_ADMIN:
            return {"error": "Insufficient permissions"}
        
        # Get global metrics from AI agents manager
        total_agents = len(self.ai_agents_manager.agent_registry)
        
        # Mock analytics data (would come from real analytics service)
        return {
            "total_ai_agents": total_agents,
            "agents_by_category": await self._get_agents_by_category(),
            "execution_trends": await self._get_execution_trends(),
            "performance_metrics": await self._get_performance_metrics(),
            "user_engagement": await self._get_user_engagement_metrics()
        }
    
    async def _get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health status"""
        health_status = SystemHealthStatus()
        
        # Check Brain API health
        try:
            # Brain API is running if we can execute this
            health_status.brain_api_status = "healthy"
        except:
            health_status.brain_api_status = "unhealthy"
        
        # Check Vault status
        if self.vault_client:
            try:
                self.vault_client.read_secret("system/health")
                health_status.vault_status = "healthy"
            except:
                health_status.vault_status = "unhealthy"
        
        # Check Redis status
        if self.redis_client:
            try:
                await self.redis_client.ping()
                health_status.redis_status = "healthy"
            except:
                health_status.redis_status = "unhealthy"
        
        # Overall status
        unhealthy_services = [
            service for service, status in health_status.model_dump().items()
            if status == "unhealthy" and service.endswith("_status")
        ]
        
        if unhealthy_services:
            health_status.overall_status = "degraded" if len(unhealthy_services) < 3 else "unhealthy"
        
        return health_status.model_dump()
    
    async def _get_ai_agents_status(self, tenant: Optional[UnifiedTenant]) -> Dict[str, Any]:
        """Get AI agents status and performance"""
        agents = await self.ai_agents_manager.get_all_agents(tenant)
        
        agents_by_category = {}
        for agent in agents:
            category = agent.category.value
            if category not in agents_by_category:
                agents_by_category[category] = []
            agents_by_category[category].append({
                "agent_id": agent.agent_id,
                "name": agent.name,
                "status": "idle",  # Would get from execution status
                "last_execution": None,
                "success_rate": 95.0  # Mock data
            })
        
        return {
            "total_agents": len(agents),
            "agents_by_category": agents_by_category,
            "recent_executions": await self._get_recent_agent_executions(tenant)
        }
    
    async def _get_platform_metrics(self) -> Dict[str, Any]:
        """Get comprehensive platform metrics"""
        metrics = PlatformMetrics()
        
        # Get tenant count
        tenants = await self.tenant_manager.list_tenants()
        metrics.total_tenants = len(tenants)
        metrics.active_tenants = len([t for t in tenants if t.status == "active"])
        
        # Mock additional metrics (would come from real monitoring)
        metrics.total_users = sum([await self._get_tenant_user_count(t) for t in tenants])
        metrics.success_rate = 95.8
        metrics.server_uptime = 99.9
        metrics.avg_response_time = 150.0
        
        return metrics.model_dump()
    
    async def _get_security_monitoring(self) -> Dict[str, Any]:
        """Get security monitoring data"""
        return {
            "security_events_24h": 0,
            "failed_login_attempts": 0,
            "blocked_ips": [],
            "vulnerability_scans": {
                "last_scan": datetime.now().isoformat(),
                "issues_found": 0,
                "status": "clean"
            },
            "ssl_certificates": {
                "status": "valid",
                "expires_in_days": 90
            }
        }
    
    async def _get_revenue_analytics(self, tenant: Optional[UnifiedTenant]) -> Dict[str, Any]:
        """Get revenue analytics"""
        if tenant:
            # Tenant-specific revenue
            return {
                "monthly_revenue": float(tenant.monthly_revenue or 0),
                "subscription_tier": tenant.subscription_tier,
                "billing_status": "active",
                "usage_metrics": await self._get_tenant_usage_metrics(tenant)
            }
        else:
            # Global revenue analytics
            tenants = await self.tenant_manager.list_tenants()
            total_revenue = sum([float(t.monthly_revenue or 0) for t in tenants])
            
            return {
                "total_monthly_revenue": total_revenue,
                "revenue_by_tier": await self._get_revenue_by_tier(),
                "growth_metrics": await self._get_revenue_growth()
            }
    
    async def _get_tenant_performance(self, tenant: Optional[UnifiedTenant]) -> Dict[str, Any]:
        """Get tenant performance metrics"""
        if not tenant:
            return {"error": "No tenant specified"}
        
        return {
            "tenant_id": tenant.tenant_id,
            "performance_score": await self._calculate_tenant_health(tenant),
            "ai_usage": await self._get_tenant_ai_executions(tenant),
            "user_engagement": await self._get_tenant_user_engagement(tenant),
            "resource_usage": await self._get_tenant_usage_metrics(tenant)
        }
    
    async def _get_infrastructure_status(self) -> Dict[str, Any]:
        """Get infrastructure status"""
        return {
            "servers": {
                "brain_api": {"status": "running", "cpu": 45.0, "memory": 62.0},
                "database": {"status": "running", "cpu": 30.0, "memory": 58.0},
                "redis": {"status": "running", "cpu": 15.0, "memory": 25.0}
            },
            "network": {
                "latency_ms": 45.0,
                "bandwidth_utilization": 35.0,
                "requests_per_second": 150
            },
            "storage": {
                "database_size_gb": 12.5,
                "backup_status": "up_to_date",
                "free_space_gb": 450.0
            }
        }
    
    async def _get_user_activity(self, tenant: Optional[UnifiedTenant]) -> Dict[str, Any]:
        """Get user activity data"""
        if tenant:
            return {
                "active_users_24h": await self._get_tenant_active_users(tenant),
                "total_users": await self._get_tenant_user_count(tenant),
                "user_sessions": await self._get_tenant_user_sessions(tenant)
            }
        else:
            # Global user activity
            return {
                "total_active_users": 0,
                "new_registrations_24h": 0,
                "user_retention_rate": 85.0
            }
    
    # Helper methods for data retrieval
    async def _get_tenant_user_count(self, tenant: UnifiedTenant) -> int:
        """Get user count for tenant"""
        # Mock implementation
        return 5
    
    async def _get_tenant_ai_executions(self, tenant: UnifiedTenant) -> int:
        """Get AI executions for tenant in last 24h"""
        # Mock implementation
        return 150
    
    async def _get_tenant_last_activity(self, tenant: UnifiedTenant) -> Optional[datetime]:
        """Get last activity timestamp for tenant"""
        # Mock implementation
        return datetime.now() - timedelta(hours=2)
    
    async def _calculate_tenant_health(self, tenant: UnifiedTenant) -> float:
        """Calculate tenant health score"""
        # Mock implementation
        return 85.5
    
    async def _get_agents_by_category(self) -> Dict[str, int]:
        """Get agent count by category"""
        agents = await self.ai_agents_manager.get_all_agents()
        category_counts = {}
        
        for agent in agents:
            category = agent.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return category_counts
    
    async def _get_execution_trends(self) -> Dict[str, Any]:
        """Get execution trend data"""
        return {
            "daily_executions": [120, 150, 180, 200, 175, 190, 210],
            "success_rates": [95.2, 96.1, 94.8, 97.3, 95.9, 96.7, 98.1]
        }
    
    async def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return {
            "avg_execution_time": 2.5,
            "throughput_per_hour": 500,
            "resource_utilization": 65.0
        }
    
    async def _get_user_engagement_metrics(self) -> Dict[str, Any]:
        """Get user engagement metrics"""
        return {
            "daily_active_users": 125,
            "avg_session_duration": 25.5,
            "feature_usage": {
                "ai_agents": 85.0,
                "analytics": 70.0,
                "campaigns": 60.0
            }
        }
    
    async def _get_recent_agent_executions(self, tenant: Optional[UnifiedTenant]) -> List[Dict[str, Any]]:
        """Get recent agent executions"""
        # Mock data
        return [
            {
                "agent_name": "Marketing Strategy Planner",
                "execution_time": "2 minutes ago",
                "status": "completed",
                "duration": 45.2
            },
            {
                "agent_name": "SEO Content Optimizer",
                "execution_time": "5 minutes ago", 
                "status": "completed",
                "duration": 32.1
            }
        ]
    
    async def _get_tenant_usage_metrics(self, tenant: UnifiedTenant) -> Dict[str, Any]:
        """Get tenant usage metrics"""
        return {
            "api_requests": 1250,
            "storage_usage_mb": 450.0,
            "bandwidth_usage_mb": 1200.0
        }
    
    async def _get_revenue_by_tier(self) -> Dict[str, float]:
        """Get revenue breakdown by subscription tier"""
        return {
            "basic": 2500.0,
            "professional": 8900.0,
            "enterprise": 15600.0
        }
    
    async def _get_revenue_growth(self) -> Dict[str, Any]:
        """Get revenue growth metrics"""
        return {
            "monthly_growth_rate": 15.5,
            "yearly_projection": 125000.0,
            "churn_rate": 5.2
        }
    
    async def _get_tenant_user_engagement(self, tenant: UnifiedTenant) -> Dict[str, Any]:
        """Get tenant user engagement"""
        return {
            "avg_session_duration": 22.5,
            "pages_per_session": 4.2,
            "bounce_rate": 35.0
        }
    
    async def _get_tenant_active_users(self, tenant: UnifiedTenant) -> int:
        """Get active users for tenant"""
        return 3
    
    async def _get_tenant_user_sessions(self, tenant: UnifiedTenant) -> int:
        """Get user sessions for tenant"""
        return 15


# Global dashboard instance
_super_admin_dashboard: Optional[SuperAdminDashboard] = None


def get_super_admin_dashboard(vault_client=None, redis_client=None) -> SuperAdminDashboard:
    """Get or create the global Super Admin Dashboard"""
    global _super_admin_dashboard
    
    if _super_admin_dashboard is None:
        _super_admin_dashboard = SuperAdminDashboard(vault_client, redis_client)
    
    return _super_admin_dashboard


# Convenience functions
async def get_dashboard_for_user(
    user_role: UserRole,
    tenant: Optional[UnifiedTenant] = None,
    widgets: Optional[List[DashboardWidget]] = None
) -> Dict[str, Any]:
    """Get dashboard data for specific user"""
    dashboard = get_super_admin_dashboard()
    return await dashboard.get_dashboard_data(user_role, tenant, widgets)


async def get_super_admin_overview() -> Dict[str, Any]:
    """Get complete super admin overview"""
    dashboard = get_super_admin_dashboard()
    return await dashboard.get_dashboard_data(UserRole.SUPER_ADMIN)


async def get_tenant_admin_dashboard(tenant: UnifiedTenant) -> Dict[str, Any]:
    """Get tenant admin dashboard"""
    dashboard = get_super_admin_dashboard()
    return await dashboard.get_dashboard_data(UserRole.TENANT_ADMIN, tenant)