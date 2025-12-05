"""
Tenant-Specific Admin Dashboards for BizOSaaS Platform

This module provides project-specific dashboard implementations that extend the unified
BizOSaaS dashboard framework. Each tenant gets a customized dashboard view with
project-scoped controls and functionality.

Project Dashboards:
- Bizoholic: AI Marketing Agency dashboard
- Coreldove: E-commerce sourcing and automation dashboard  
- ThrillRing: Entertainment platform dashboard
- QuantTrade: Personal trading platform dashboard
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass
import asyncio
import json

# Import unified dashboard base classes
from super_admin_dashboard import (
    UserRole, DashboardWidget, SuperAdminDashboard,
    get_dashboard_for_user, get_tenant_admin_dashboard
)

# Import AI agents and tenant management
from ai_agents_management import AgentCategory, get_available_agents_by_category
from tenant_middleware import get_current_tenant, TenantContext


class ProjectType(str, Enum):
    """Supported project types in BizOSaaS ecosystem"""
    BIZOHOLIC = "bizoholic"
    CORELDOVE = "coreldove"
    THRILLRING = "thrillring"
    QUANTTRADE = "quanttrade"
    CLIENT_PORTAL = "client_portal"


@dataclass
class ProjectDashboardConfig:
    """Configuration for project-specific dashboards"""
    project_type: ProjectType
    display_name: str
    primary_color: str
    available_widgets: List[DashboardWidget]
    ai_agent_categories: List[AgentCategory]
    default_metrics: List[str]
    custom_endpoints: List[str]
    permissions: Dict[str, bool]


class TenantAdminDashboard:
    """
    Tenant-specific admin dashboard that provides project-scoped controls
    while maintaining unified architecture.
    """
    
    def __init__(self, vault_client=None, redis_client=None, event_bus_client=None):
        self.vault_client = vault_client
        self.redis_client = redis_client
        self.event_bus_client = event_bus_client
        
        # Project-specific dashboard configurations
        self.project_configs = {
            ProjectType.BIZOHOLIC: ProjectDashboardConfig(
                project_type=ProjectType.BIZOHOLIC,
                display_name="Bizoholic AI Marketing Agency",
                primary_color="#FF6B35",
                available_widgets=[
                    DashboardWidget.CLIENT_OVERVIEW,
                    DashboardWidget.CAMPAIGN_PERFORMANCE,
                    DashboardWidget.AI_AGENT_STATUS,
                    DashboardWidget.LEAD_GENERATION,
                    DashboardWidget.CONTENT_ANALYTICS,
                    DashboardWidget.SEO_METRICS,
                    DashboardWidget.REVENUE_DASHBOARD,
                    DashboardWidget.CLIENT_SATISFACTION
                ],
                ai_agent_categories=[
                    AgentCategory.MARKETING,
                    AgentCategory.SEO_CONTENT,
                    AgentCategory.ANALYTICS,
                    AgentCategory.LEAD_GENERATION
                ],
                default_metrics=[
                    "active_campaigns", "conversion_rate", "client_retention",
                    "content_performance", "seo_rankings", "lead_quality_score"
                ],
                custom_endpoints=[
                    "/api/bizoholic/campaigns", "/api/bizoholic/clients",
                    "/api/bizoholic/content", "/api/bizoholic/leads"
                ],
                permissions={
                    "manage_campaigns": True,
                    "manage_clients": True,
                    "access_analytics": True,
                    "manage_content": True,
                    "configure_ai_agents": True
                }
            ),
            
            ProjectType.CORELDOVE: ProjectDashboardConfig(
                project_type=ProjectType.CORELDOVE,
                display_name="Coreldove E-commerce Automation",
                primary_color="#4ECDC4",
                available_widgets=[
                    DashboardWidget.PRODUCT_CATALOG,
                    DashboardWidget.INVENTORY_STATUS,
                    DashboardWidget.ORDER_MANAGEMENT,
                    DashboardWidget.AI_AGENT_STATUS,
                    DashboardWidget.SUPPLIER_ANALYTICS,
                    DashboardWidget.REVENUE_DASHBOARD,
                    DashboardWidget.AUTOMATION_METRICS,
                    DashboardWidget.SOURCING_PERFORMANCE
                ],
                ai_agent_categories=[
                    AgentCategory.ECOMMERCE,
                    AgentCategory.ANALYTICS,
                    AgentCategory.INFRASTRUCTURE
                ],
                default_metrics=[
                    "product_listings", "order_volume", "inventory_turnover",
                    "sourcing_efficiency", "automation_success_rate", "profit_margins"
                ],
                custom_endpoints=[
                    "/api/coreldove/products", "/api/coreldove/orders",
                    "/api/coreldove/suppliers", "/api/coreldove/automation"
                ],
                permissions={
                    "manage_products": True,
                    "manage_orders": True,
                    "access_analytics": True,
                    "manage_suppliers": True,
                    "configure_automation": True
                }
            ),
            
            ProjectType.THRILLRING: ProjectDashboardConfig(
                project_type=ProjectType.THRILLRING,
                display_name="ThrillRing Entertainment Platform",
                primary_color="#9B59B6",
                available_widgets=[
                    DashboardWidget.CONTENT_ANALYTICS,
                    DashboardWidget.USER_ENGAGEMENT,
                    DashboardWidget.AI_AGENT_STATUS,
                    DashboardWidget.MONETIZATION_METRICS,
                    DashboardWidget.CONTENT_MODERATION,
                    DashboardWidget.CREATOR_ANALYTICS,
                    DashboardWidget.PLATFORM_HEALTH
                ],
                ai_agent_categories=[
                    AgentCategory.ANALYTICS,
                    AgentCategory.SEO_CONTENT,
                    AgentCategory.INFRASTRUCTURE
                ],
                default_metrics=[
                    "active_users", "content_uploads", "engagement_rate",
                    "creator_earnings", "platform_revenue", "content_quality_score"
                ],
                custom_endpoints=[
                    "/api/thrillring/content", "/api/thrillring/users",
                    "/api/thrillring/creators", "/api/thrillring/monetization"
                ],
                permissions={
                    "manage_content": True,
                    "manage_users": True,
                    "access_analytics": True,
                    "manage_creators": True,
                    "configure_monetization": True
                }
            ),
            
            ProjectType.QUANTTRADE: ProjectDashboardConfig(
                project_type=ProjectType.QUANTTRADE,
                display_name="QuantTrade Personal Trading",
                primary_color="#E74C3C",
                available_widgets=[
                    DashboardWidget.TRADING_PERFORMANCE,
                    DashboardWidget.PORTFOLIO_ANALYTICS,
                    DashboardWidget.AI_AGENT_STATUS,
                    DashboardWidget.RISK_MANAGEMENT,
                    DashboardWidget.MARKET_ANALYTICS,
                    DashboardWidget.ALGORITHM_METRICS,
                    DashboardWidget.STRATEGY_PERFORMANCE
                ],
                ai_agent_categories=[
                    AgentCategory.ANALYTICS,
                    AgentCategory.INFRASTRUCTURE
                ],
                default_metrics=[
                    "portfolio_value", "daily_pnl", "sharpe_ratio",
                    "max_drawdown", "win_rate", "algorithm_performance"
                ],
                custom_endpoints=[
                    "/api/quanttrade/portfolio", "/api/quanttrade/trades",
                    "/api/quanttrade/strategies", "/api/quanttrade/analytics"
                ],
                permissions={
                    "manage_portfolio": True,
                    "access_analytics": True,
                    "configure_strategies": True,
                    "manage_risk_settings": True,
                    "personal_use_only": True
                }
            )
        }
    
    async def get_tenant_dashboard(self, tenant_id: str, user_role: UserRole, project_type: ProjectType) -> Dict[str, Any]:
        """
        Get project-specific dashboard data for tenant admin
        """
        try:
            # Get project configuration
            config = self.project_configs.get(project_type)
            if not config:
                raise ValueError(f"Unsupported project type: {project_type}")
            
            # Get base tenant dashboard data
            base_dashboard = await get_tenant_admin_dashboard(tenant_id)
            
            # Get project-specific metrics
            project_metrics = await self._get_project_metrics(tenant_id, project_type)
            
            # Get AI agents for this project
            project_agents = await self._get_project_ai_agents(tenant_id, config.ai_agent_categories)
            
            # Get project-specific analytics
            project_analytics = await self._get_project_analytics(tenant_id, project_type)
            
            return {
                "tenant_id": tenant_id,
                "project_type": project_type.value,
                "project_name": config.display_name,
                "primary_color": config.primary_color,
                "user_role": user_role.value,
                "permissions": config.permissions,
                "widgets": {
                    "available": [widget.value for widget in config.available_widgets],
                    "data": await self._get_widget_data(tenant_id, project_type, config.available_widgets)
                },
                "metrics": {
                    "default": config.default_metrics,
                    "current": project_metrics
                },
                "ai_agents": project_agents,
                "analytics": project_analytics,
                "endpoints": config.custom_endpoints,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get tenant dashboard: {str(e)}",
                "tenant_id": tenant_id,
                "project_type": project_type.value if project_type else None
            }
    
    async def _get_project_metrics(self, tenant_id: str, project_type: ProjectType) -> Dict[str, Any]:
        """Get project-specific metrics"""
        try:
            if project_type == ProjectType.BIZOHOLIC:
                return {
                    "active_campaigns": await self._get_bizoholic_campaigns(tenant_id),
                    "conversion_rate": await self._get_conversion_metrics(tenant_id),
                    "client_retention": await self._get_retention_metrics(tenant_id),
                    "content_performance": await self._get_content_metrics(tenant_id),
                    "seo_rankings": await self._get_seo_metrics(tenant_id),
                    "lead_quality_score": await self._get_lead_quality(tenant_id)
                }
            elif project_type == ProjectType.CORELDOVE:
                return {
                    "product_listings": await self._get_product_count(tenant_id),
                    "order_volume": await self._get_order_metrics(tenant_id),
                    "inventory_turnover": await self._get_inventory_metrics(tenant_id),
                    "sourcing_efficiency": await self._get_sourcing_metrics(tenant_id),
                    "automation_success_rate": await self._get_automation_metrics(tenant_id),
                    "profit_margins": await self._get_profitability(tenant_id)
                }
            elif project_type == ProjectType.THRILLRING:
                return {
                    "active_users": await self._get_user_metrics(tenant_id),
                    "content_uploads": await self._get_content_volume(tenant_id),
                    "engagement_rate": await self._get_engagement_metrics(tenant_id),
                    "creator_earnings": await self._get_creator_metrics(tenant_id),
                    "platform_revenue": await self._get_revenue_metrics(tenant_id),
                    "content_quality_score": await self._get_quality_metrics(tenant_id)
                }
            elif project_type == ProjectType.QUANTTRADE:
                return {
                    "portfolio_value": await self._get_portfolio_value(tenant_id),
                    "daily_pnl": await self._get_pnl_metrics(tenant_id),
                    "sharpe_ratio": await self._get_performance_ratios(tenant_id),
                    "max_drawdown": await self._get_risk_metrics(tenant_id),
                    "win_rate": await self._get_trading_success(tenant_id),
                    "algorithm_performance": await self._get_algo_metrics(tenant_id)
                }
            else:
                return {}
                
        except Exception as e:
            return {"error": f"Failed to get project metrics: {str(e)}"}
    
    async def _get_project_ai_agents(self, tenant_id: str, categories: List[AgentCategory]) -> Dict[str, Any]:
        """Get AI agents available for this project"""
        try:
            project_agents = {}
            
            for category in categories:
                agents = await get_available_agents_by_category(category)
                project_agents[category.value] = [
                    {
                        "agent_id": agent["agent_id"],
                        "name": agent["name"],
                        "description": agent["description"],
                        "status": await self._get_agent_status(tenant_id, agent["agent_id"]),
                        "last_execution": await self._get_agent_last_execution(tenant_id, agent["agent_id"]),
                        "success_rate": await self._get_agent_success_rate(tenant_id, agent["agent_id"])
                    }
                    for agent in agents
                ]
            
            return project_agents
            
        except Exception as e:
            return {"error": f"Failed to get project AI agents: {str(e)}"}
    
    async def _get_project_analytics(self, tenant_id: str, project_type: ProjectType) -> Dict[str, Any]:
        """Get project-specific analytics and insights"""
        try:
            # Time-based analytics for the last 30 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            if project_type == ProjectType.BIZOHOLIC:
                return {
                    "campaign_trends": await self._get_campaign_trends(tenant_id, start_date, end_date),
                    "client_acquisition": await self._get_acquisition_trends(tenant_id, start_date, end_date),
                    "content_performance": await self._get_content_trends(tenant_id, start_date, end_date),
                    "revenue_growth": await self._get_revenue_trends(tenant_id, start_date, end_date)
                }
            elif project_type == ProjectType.CORELDOVE:
                return {
                    "sales_trends": await self._get_sales_trends(tenant_id, start_date, end_date),
                    "inventory_analytics": await self._get_inventory_analytics(tenant_id, start_date, end_date),
                    "supplier_performance": await self._get_supplier_analytics(tenant_id, start_date, end_date),
                    "automation_efficiency": await self._get_automation_analytics(tenant_id, start_date, end_date)
                }
            elif project_type == ProjectType.THRILLRING:
                return {
                    "user_growth": await self._get_user_growth_trends(tenant_id, start_date, end_date),
                    "content_analytics": await self._get_content_analytics(tenant_id, start_date, end_date),
                    "monetization_trends": await self._get_monetization_trends(tenant_id, start_date, end_date),
                    "engagement_analytics": await self._get_engagement_analytics(tenant_id, start_date, end_date)
                }
            elif project_type == ProjectType.QUANTTRADE:
                return {
                    "performance_analytics": await self._get_performance_analytics(tenant_id, start_date, end_date),
                    "risk_analytics": await self._get_risk_analytics(tenant_id, start_date, end_date),
                    "strategy_comparison": await self._get_strategy_analytics(tenant_id, start_date, end_date),
                    "market_correlation": await self._get_market_analytics(tenant_id, start_date, end_date)
                }
            else:
                return {}
                
        except Exception as e:
            return {"error": f"Failed to get project analytics: {str(e)}"}
    
    async def _get_widget_data(self, tenant_id: str, project_type: ProjectType, widgets: List[DashboardWidget]) -> Dict[str, Any]:
        """Get data for specific dashboard widgets"""
        widget_data = {}
        
        for widget in widgets:
            try:
                if widget == DashboardWidget.CLIENT_OVERVIEW:
                    widget_data[widget.value] = await self._get_client_overview_data(tenant_id)
                elif widget == DashboardWidget.CAMPAIGN_PERFORMANCE:
                    widget_data[widget.value] = await self._get_campaign_performance_data(tenant_id)
                elif widget == DashboardWidget.AI_AGENT_STATUS:
                    widget_data[widget.value] = await self._get_ai_agent_status_data(tenant_id, project_type)
                elif widget == DashboardWidget.PRODUCT_CATALOG:
                    widget_data[widget.value] = await self._get_product_catalog_data(tenant_id)
                elif widget == DashboardWidget.TRADING_PERFORMANCE:
                    widget_data[widget.value] = await self._get_trading_performance_data(tenant_id)
                # Add more widget data methods as needed
                
            except Exception as e:
                widget_data[widget.value] = {"error": f"Failed to load widget data: {str(e)}"}
        
        return widget_data
    
    # Placeholder methods for project-specific data retrieval
    # These would connect to actual project databases and APIs
    
    async def _get_bizoholic_campaigns(self, tenant_id: str) -> int:
        """Get active campaign count for Bizoholic"""
        # Mock data - replace with actual database query
        return 12
    
    async def _get_conversion_metrics(self, tenant_id: str) -> float:
        """Get conversion rate metrics"""
        return 15.7
    
    async def _get_retention_metrics(self, tenant_id: str) -> float:
        """Get client retention metrics"""
        return 89.3
    
    async def _get_content_metrics(self, tenant_id: str) -> Dict[str, Any]:
        """Get content performance metrics"""
        return {
            "total_content": 156,
            "engagement_rate": 12.4,
            "viral_content": 8
        }
    
    async def _get_seo_metrics(self, tenant_id: str) -> Dict[str, Any]:
        """Get SEO performance metrics"""
        return {
            "avg_ranking": 15.2,
            "keyword_improvements": 45,
            "organic_traffic_growth": 23.1
        }
    
    async def _get_lead_quality(self, tenant_id: str) -> float:
        """Get lead quality score"""
        return 78.5
    
    async def _get_product_count(self, tenant_id: str) -> int:
        """Get product listing count for Coreldove"""
        return 1247
    
    async def _get_order_metrics(self, tenant_id: str) -> Dict[str, Any]:
        """Get order volume metrics"""
        return {
            "daily_orders": 45,
            "weekly_orders": 312,
            "monthly_orders": 1280
        }
    
    async def _get_inventory_metrics(self, tenant_id: str) -> float:
        """Get inventory turnover rate"""
        return 4.2
    
    async def _get_sourcing_metrics(self, tenant_id: str) -> float:
        """Get sourcing efficiency percentage"""
        return 91.3
    
    async def _get_automation_metrics(self, tenant_id: str) -> float:
        """Get automation success rate"""
        return 96.7
    
    async def _get_profitability(self, tenant_id: str) -> float:
        """Get profit margin percentage"""
        return 24.8
    
    async def _get_user_metrics(self, tenant_id: str) -> int:
        """Get active user count for ThrillRing"""
        return 15647
    
    async def _get_content_volume(self, tenant_id: str) -> int:
        """Get daily content upload count"""
        return 234
    
    async def _get_engagement_metrics(self, tenant_id: str) -> float:
        """Get user engagement rate"""
        return 18.6
    
    async def _get_creator_metrics(self, tenant_id: str) -> float:
        """Get creator earnings"""
        return 47623.45
    
    async def _get_revenue_metrics(self, tenant_id: str) -> float:
        """Get platform revenue"""
        return 156789.23
    
    async def _get_quality_metrics(self, tenant_id: str) -> float:
        """Get content quality score"""
        return 82.4
    
    async def _get_portfolio_value(self, tenant_id: str) -> float:
        """Get portfolio value for QuantTrade"""
        return 847526.78
    
    async def _get_pnl_metrics(self, tenant_id: str) -> float:
        """Get daily P&L"""
        return 2847.32
    
    async def _get_performance_ratios(self, tenant_id: str) -> float:
        """Get Sharpe ratio"""
        return 1.84
    
    async def _get_risk_metrics(self, tenant_id: str) -> float:
        """Get maximum drawdown"""
        return -8.7
    
    async def _get_trading_success(self, tenant_id: str) -> float:
        """Get win rate percentage"""
        return 67.3
    
    async def _get_algo_metrics(self, tenant_id: str) -> Dict[str, Any]:
        """Get algorithm performance metrics"""
        return {
            "algorithms_running": 12,
            "avg_performance": 15.7,
            "best_performer": "momentum_strategy_v3"
        }
    
    async def _get_agent_status(self, tenant_id: str, agent_id: str) -> str:
        """Get AI agent status"""
        return "active"
    
    async def _get_agent_last_execution(self, tenant_id: str, agent_id: str) -> str:
        """Get agent last execution time"""
        return (datetime.now() - timedelta(minutes=15)).isoformat()
    
    async def _get_agent_success_rate(self, tenant_id: str, agent_id: str) -> float:
        """Get agent success rate"""
        return 94.2
    
    # Analytics methods would return time-series data
    async def _get_campaign_trends(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get campaign performance trends"""
        return [{"date": "2025-09-01", "campaigns": 8, "performance": 12.4}]
    
    async def _get_acquisition_trends(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get client acquisition trends"""
        return [{"date": "2025-09-01", "new_clients": 3, "conversion_rate": 15.2}]
    
    async def _get_content_trends(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get content performance trends"""
        return [{"date": "2025-09-01", "content_pieces": 12, "engagement": 14.7}]
    
    async def _get_revenue_trends(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get revenue growth trends"""
        return [{"date": "2025-09-01", "revenue": 15647.32, "growth_rate": 8.4}]
    
    async def _get_sales_trends(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get sales trends for Coreldove"""
        return [{"date": "2025-09-01", "sales": 12847.56, "orders": 67}]
    
    async def _get_inventory_analytics(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get inventory analytics"""
        return [{"date": "2025-09-01", "stock_level": 1247, "turnover": 4.2}]
    
    async def _get_supplier_analytics(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get supplier performance analytics"""
        return [{"date": "2025-09-01", "orders_fulfilled": 45, "quality_score": 92.3}]
    
    async def _get_automation_analytics(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get automation efficiency analytics"""
        return [{"date": "2025-09-01", "tasks_automated": 156, "success_rate": 96.7}]
    
    async def _get_user_growth_trends(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get user growth trends for ThrillRing"""
        return [{"date": "2025-09-01", "new_users": 234, "retention": 78.4}]
    
    async def _get_content_analytics(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get content analytics"""
        return [{"date": "2025-09-01", "uploads": 156, "views": 45623, "engagement": 18.7}]
    
    async def _get_monetization_trends(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get monetization trends"""
        return [{"date": "2025-09-01", "revenue": 8745.23, "creator_earnings": 6234.56}]
    
    async def _get_engagement_analytics(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get engagement analytics"""
        return [{"date": "2025-09-01", "likes": 12847, "shares": 3456, "comments": 1234}]
    
    async def _get_performance_analytics(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get trading performance analytics"""
        return [{"date": "2025-09-01", "pnl": 1247.56, "trades": 23, "win_rate": 67.3}]
    
    async def _get_risk_analytics(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get risk analytics"""
        return [{"date": "2025-09-01", "var": -2347.89, "sharpe": 1.84, "drawdown": -5.2}]
    
    async def _get_strategy_analytics(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get strategy comparison analytics"""
        return [{"strategy": "momentum_v3", "performance": 15.7, "risk": 12.3}]
    
    async def _get_market_analytics(self, tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get market correlation analytics"""
        return [{"market": "SPY", "correlation": 0.73, "beta": 1.15}]
    
    # Widget data methods
    async def _get_client_overview_data(self, tenant_id: str) -> Dict[str, Any]:
        """Get client overview widget data"""
        return {
            "total_clients": 23,
            "active_campaigns": 12,
            "monthly_revenue": 47623.45,
            "client_satisfaction": 94.2
        }
    
    async def _get_campaign_performance_data(self, tenant_id: str) -> Dict[str, Any]:
        """Get campaign performance widget data"""
        return {
            "active_campaigns": 12,
            "avg_conversion_rate": 15.7,
            "total_impressions": 456789,
            "cost_per_acquisition": 23.45
        }
    
    async def _get_ai_agent_status_data(self, tenant_id: str, project_type: ProjectType) -> Dict[str, Any]:
        """Get AI agent status widget data"""
        return {
            "agents_active": 18,
            "agents_idle": 3,
            "avg_success_rate": 94.2,
            "tasks_completed_today": 156
        }
    
    async def _get_product_catalog_data(self, tenant_id: str) -> Dict[str, Any]:
        """Get product catalog widget data"""
        return {
            "total_products": 1247,
            "active_listings": 1189,
            "out_of_stock": 23,
            "pending_approval": 35
        }
    
    async def _get_trading_performance_data(self, tenant_id: str) -> Dict[str, Any]:
        """Get trading performance widget data"""
        return {
            "portfolio_value": 847526.78,
            "daily_pnl": 2847.32,
            "ytd_return": 23.7,
            "active_positions": 12
        }


# Global tenant dashboard instance
tenant_dashboard = TenantAdminDashboard()

# API helper functions
async def get_bizoholic_dashboard(tenant_id: str, user_role: UserRole = UserRole.ADMINISTRATOR) -> Dict[str, Any]:
    """Get Bizoholic project dashboard"""
    return await tenant_dashboard.get_tenant_dashboard(tenant_id, user_role, ProjectType.BIZOHOLIC)

async def get_coreldove_dashboard(tenant_id: str, user_role: UserRole = UserRole.ADMINISTRATOR) -> Dict[str, Any]:
    """Get Coreldove project dashboard"""
    return await tenant_dashboard.get_tenant_dashboard(tenant_id, user_role, ProjectType.CORELDOVE)

async def get_thrillring_dashboard(tenant_id: str, user_role: UserRole = UserRole.ADMINISTRATOR) -> Dict[str, Any]:
    """Get ThrillRing project dashboard"""
    return await tenant_dashboard.get_tenant_dashboard(tenant_id, user_role, ProjectType.THRILLRING)

async def get_quanttrade_dashboard(tenant_id: str, user_role: UserRole = UserRole.ADMINISTRATOR) -> Dict[str, Any]:
    """Get QuantTrade project dashboard"""
    return await tenant_dashboard.get_tenant_dashboard(tenant_id, user_role, ProjectType.QUANTTRADE)

async def get_project_dashboard_by_type(tenant_id: str, project_type: str, user_role: UserRole = UserRole.ADMINISTRATOR) -> Dict[str, Any]:
    """Get dashboard for any project type"""
    try:
        project_enum = ProjectType(project_type.lower())
        return await tenant_dashboard.get_tenant_dashboard(tenant_id, user_role, project_enum)
    except ValueError:
        return {
            "success": False,
            "error": f"Unsupported project type: {project_type}",
            "supported_types": [pt.value for pt in ProjectType]
        }