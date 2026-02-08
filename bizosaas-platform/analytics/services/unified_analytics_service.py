"""
Unified Analytics Service for BizOSaaS Platform

This service provides comprehensive cross-platform analytics and unified reporting
across all 5 platforms: Bizoholic, CoreLDove, Business Directory, ThrillRing, and QuantTrade.

Features:
- Real-time analytics aggregation across platforms
- AI-powered insights and predictive analytics
- Tenant-aware data isolation
- Subscription tier-based reporting capabilities
- Custom dashboard generation
- Automated reporting and alerts
- Performance optimization recommendations
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set, Union
from uuid import UUID, uuid4

import numpy as np
import pandas as pd
from fastapi import HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from shared.enhanced_tenant_context import EnhancedTenantContext, PlatformType, TenantTier
from shared.rls_manager import RLSManager
from ai.services.bizosaas_brain.tenant_aware_ai_coordinator import TenantAwareAICoordinator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricType(str, Enum):
    """Analytics metric types"""
    REVENUE = "revenue"
    USERS = "users"
    CONVERSIONS = "conversions"
    ENGAGEMENT = "engagement"
    PERFORMANCE = "performance"
    SATISFACTION = "satisfaction"
    RETENTION = "retention"
    ACQUISITION = "acquisition"

class TimeRange(str, Enum):
    """Time range options for analytics"""
    LAST_24_HOURS = "24h"
    LAST_7_DAYS = "7d"
    LAST_30_DAYS = "30d"
    LAST_90_DAYS = "90d"
    LAST_YEAR = "1y"
    CUSTOM = "custom"

class AnalyticsDataPoint(BaseModel):
    """Individual analytics data point"""
    timestamp: datetime
    platform: PlatformType
    metric_type: MetricType
    metric_name: str
    value: Union[float, int, str]
    dimensions: Dict[str, Any] = Field(default_factory=dict)
    tenant_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class PlatformMetrics(BaseModel):
    """Platform-specific metrics"""
    platform: PlatformType
    total_revenue: Decimal = Field(default=Decimal('0'))
    active_users: int = 0
    conversion_rate: float = 0.0
    engagement_score: float = 0.0
    performance_index: float = 0.0
    growth_rate: float = 0.0
    churn_rate: float = 0.0
    customer_satisfaction: float = 0.0
    key_metrics: Dict[str, Any] = Field(default_factory=dict)

class CrossPlatformInsight(BaseModel):
    """AI-generated cross-platform insights"""
    insight_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: str
    impact_score: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    affected_platforms: List[PlatformType]
    recommended_actions: List[str]
    priority: str = Field(default="medium")  # low, medium, high, critical
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AnalyticsDashboard(BaseModel):
    """Complete analytics dashboard data"""
    dashboard_id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    time_range: TimeRange
    platform_metrics: Dict[PlatformType, PlatformMetrics] = Field(default_factory=dict)
    cross_platform_insights: List[CrossPlatformInsight] = Field(default_factory=list)
    ai_recommendations: List[str] = Field(default_factory=list)
    kpi_summary: Dict[str, Any] = Field(default_factory=dict)
    subscription_tier: TenantTier
    custom_widgets: List[Dict[str, Any]] = Field(default_factory=list)

class PredictiveAnalytics(BaseModel):
    """Predictive analytics and forecasting"""
    prediction_id: str = Field(default_factory=lambda: str(uuid4()))
    metric_name: str
    platform: Optional[PlatformType] = None
    forecast_horizon: int  # days
    predicted_values: List[Dict[str, Any]]
    confidence_interval: Dict[str, float]
    model_accuracy: float
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    factors: List[str] = Field(default_factory=list)

class AnalyticsQuery(BaseModel):
    """Analytics query parameters"""
    tenant_id: str
    platforms: List[PlatformType] = Field(default_factory=list)
    metrics: List[MetricType] = Field(default_factory=list)
    time_range: TimeRange = TimeRange.LAST_30_DAYS
    custom_start: Optional[datetime] = None
    custom_end: Optional[datetime] = None
    filters: Dict[str, Any] = Field(default_factory=dict)
    aggregation: str = "daily"  # hourly, daily, weekly, monthly
    include_predictions: bool = False

class UnifiedAnalyticsService:
    """Unified Analytics Service for cross-platform reporting"""

    def __init__(self, rls_manager: RLSManager, ai_coordinator: TenantAwareAICoordinator):
        self.rls_manager = rls_manager
        self.ai_coordinator = ai_coordinator
        self.cache = {}
        self.insight_cache = {}

    async def collect_platform_data(
        self,
        session: AsyncSession,
        tenant_context: EnhancedTenantContext,
        query: AnalyticsQuery
    ) -> Dict[PlatformType, List[AnalyticsDataPoint]]:
        """Collect analytics data from all accessible platforms"""

        platform_data = {}

        # Set tenant context for RLS
        await self.rls_manager.set_tenant_context(session, tenant_context.tenant_id)

        # Determine accessible platforms based on subscription tier
        accessible_platforms = self._get_accessible_platforms(tenant_context, query.platforms)

        for platform in accessible_platforms:
            try:
                data_points = await self._collect_platform_specific_data(
                    session, platform, tenant_context, query
                )
                platform_data[platform] = data_points
                logger.info(f"Collected {len(data_points)} data points for {platform.value}")

            except Exception as e:
                logger.error(f"Error collecting data for {platform.value}: {str(e)}")
                platform_data[platform] = []

        return platform_data

    async def _collect_platform_specific_data(
        self,
        session: AsyncSession,
        platform: PlatformType,
        tenant_context: EnhancedTenantContext,
        query: AnalyticsQuery
    ) -> List[AnalyticsDataPoint]:
        """Collect data from specific platform"""

        data_points = []

        # Platform-specific data collection logic
        if platform == PlatformType.BIZOHOLIC:
            data_points.extend(await self._collect_bizoholic_data(session, tenant_context, query))
        elif platform == PlatformType.CORELDOVE:
            data_points.extend(await self._collect_coreldove_data(session, tenant_context, query))
        elif platform == PlatformType.BUSINESS_DIRECTORY:
            data_points.extend(await self._collect_business_directory_data(session, tenant_context, query))
        elif platform == PlatformType.THRILLRING:
            data_points.extend(await self._collect_thrillring_data(session, tenant_context, query))
        elif platform == PlatformType.QUANTTRADE:
            data_points.extend(await self._collect_quanttrade_data(session, tenant_context, query))

        return data_points

    async def _collect_bizoholic_data(
        self,
        session: AsyncSession,
        tenant_context: EnhancedTenantContext,
        query: AnalyticsQuery
    ) -> List[AnalyticsDataPoint]:
        """Collect Bizoholic marketing agency data"""

        data_points = []
        time_filter = self._get_time_filter(query)

        # Revenue data
        revenue_query = text("""
            SELECT
                DATE(created_at) as date,
                SUM(amount) as revenue,
                COUNT(*) as transactions
            FROM payments
            WHERE tenant_id = :tenant_id
                AND platform = 'bizoholic'
                AND created_at >= :start_date
                AND created_at <= :end_date
                AND status = 'completed'
            GROUP BY DATE(created_at)
            ORDER BY date
        """)

        result = await session.execute(
            revenue_query,
            {
                "tenant_id": tenant_context.tenant_id,
                "start_date": time_filter["start"],
                "end_date": time_filter["end"]
            }
        )

        for row in result:
            data_points.append(AnalyticsDataPoint(
                timestamp=row.date,
                platform=PlatformType.BIZOHOLIC,
                metric_type=MetricType.REVENUE,
                metric_name="daily_revenue",
                value=float(row.revenue or 0),
                tenant_id=tenant_context.tenant_id,
                dimensions={"transactions": row.transactions}
            ))

        # Campaign performance data
        campaign_query = text("""
            SELECT
                DATE(created_at) as date,
                COUNT(*) as campaigns,
                AVG(conversion_rate) as avg_conversion,
                SUM(leads_generated) as total_leads
            FROM marketing_campaigns
            WHERE tenant_id = :tenant_id
                AND created_at >= :start_date
                AND created_at <= :end_date
            GROUP BY DATE(created_at)
            ORDER BY date
        """)

        result = await session.execute(
            campaign_query,
            {
                "tenant_id": tenant_context.tenant_id,
                "start_date": time_filter["start"],
                "end_date": time_filter["end"]
            }
        )

        for row in result:
            data_points.append(AnalyticsDataPoint(
                timestamp=row.date,
                platform=PlatformType.BIZOHOLIC,
                metric_type=MetricType.CONVERSIONS,
                metric_name="campaign_performance",
                value=float(row.avg_conversion or 0),
                tenant_id=tenant_context.tenant_id,
                dimensions={
                    "campaigns": row.campaigns,
                    "total_leads": row.total_leads
                }
            ))

        return data_points

    async def _collect_coreldove_data(
        self,
        session: AsyncSession,
        tenant_context: EnhancedTenantContext,
        query: AnalyticsQuery
    ) -> List[AnalyticsDataPoint]:
        """Collect CoreLDove ecommerce data"""

        data_points = []
        time_filter = self._get_time_filter(query)

        # Sales data
        sales_query = text("""
            SELECT
                DATE(order_date) as date,
                SUM(total_amount) as revenue,
                COUNT(*) as orders,
                AVG(total_amount) as avg_order_value
            FROM orders
            WHERE tenant_id = :tenant_id
                AND platform = 'coreldove'
                AND order_date >= :start_date
                AND order_date <= :end_date
                AND status = 'completed'
            GROUP BY DATE(order_date)
            ORDER BY date
        """)

        result = await session.execute(
            sales_query,
            {
                "tenant_id": tenant_context.tenant_id,
                "start_date": time_filter["start"],
                "end_date": time_filter["end"]
            }
        )

        for row in result:
            data_points.append(AnalyticsDataPoint(
                timestamp=row.date,
                platform=PlatformType.CORELDOVE,
                metric_type=MetricType.REVENUE,
                metric_name="ecommerce_sales",
                value=float(row.revenue or 0),
                tenant_id=tenant_context.tenant_id,
                dimensions={
                    "orders": row.orders,
                    "avg_order_value": float(row.avg_order_value or 0)
                }
            ))

        # Product performance
        product_query = text("""
            SELECT
                DATE(created_at) as date,
                COUNT(*) as products_added,
                AVG(view_count) as avg_views,
                SUM(CASE WHEN stock_quantity = 0 THEN 1 ELSE 0 END) as out_of_stock
            FROM products
            WHERE tenant_id = :tenant_id
                AND created_at >= :start_date
                AND created_at <= :end_date
            GROUP BY DATE(created_at)
            ORDER BY date
        """)

        result = await session.execute(
            product_query,
            {
                "tenant_id": tenant_context.tenant_id,
                "start_date": time_filter["start"],
                "end_date": time_filter["end"]
            }
        )

        for row in result:
            data_points.append(AnalyticsDataPoint(
                timestamp=row.date,
                platform=PlatformType.CORELDOVE,
                metric_type=MetricType.PERFORMANCE,
                metric_name="product_metrics",
                value=float(row.avg_views or 0),
                tenant_id=tenant_context.tenant_id,
                dimensions={
                    "products_added": row.products_added,
                    "out_of_stock": row.out_of_stock
                }
            ))

        return data_points

    async def _collect_business_directory_data(
        self,
        session: AsyncSession,
        tenant_context: EnhancedTenantContext,
        query: AnalyticsQuery
    ) -> List[AnalyticsDataPoint]:
        """Collect Business Directory data"""

        data_points = []
        time_filter = self._get_time_filter(query)

        # Directory listings data
        listings_query = text("""
            SELECT
                DATE(created_at) as date,
                COUNT(*) as new_listings,
                SUM(view_count) as total_views,
                AVG(rating) as avg_rating
            FROM business_listings
            WHERE tenant_id = :tenant_id
                AND created_at >= :start_date
                AND created_at <= :end_date
                AND status = 'active'
            GROUP BY DATE(created_at)
            ORDER BY date
        """)

        result = await session.execute(
            listings_query,
            {
                "tenant_id": tenant_context.tenant_id,
                "start_date": time_filter["start"],
                "end_date": time_filter["end"]
            }
        )

        for row in result:
            data_points.append(AnalyticsDataPoint(
                timestamp=row.date,
                platform=PlatformType.BUSINESS_DIRECTORY,
                metric_type=MetricType.ENGAGEMENT,
                metric_name="directory_activity",
                value=float(row.total_views or 0),
                tenant_id=tenant_context.tenant_id,
                dimensions={
                    "new_listings": row.new_listings,
                    "avg_rating": float(row.avg_rating or 0)
                }
            ))

        return data_points

    async def _collect_thrillring_data(
        self,
        session: AsyncSession,
        tenant_context: EnhancedTenantContext,
        query: AnalyticsQuery
    ) -> List[AnalyticsDataPoint]:
        """Collect ThrillRing gaming data"""

        data_points = []
        time_filter = self._get_time_filter(query)

        # Gaming activity data
        gaming_query = text("""
            SELECT
                DATE(created_at) as date,
                COUNT(DISTINCT user_id) as active_players,
                SUM(score) as total_score,
                COUNT(*) as games_played
            FROM game_sessions
            WHERE tenant_id = :tenant_id
                AND created_at >= :start_date
                AND created_at <= :end_date
            GROUP BY DATE(created_at)
            ORDER BY date
        """)

        result = await session.execute(
            gaming_query,
            {
                "tenant_id": tenant_context.tenant_id,
                "start_date": time_filter["start"],
                "end_date": time_filter["end"]
            }
        )

        for row in result:
            data_points.append(AnalyticsDataPoint(
                timestamp=row.date,
                platform=PlatformType.THRILLRING,
                metric_type=MetricType.ENGAGEMENT,
                metric_name="gaming_activity",
                value=row.active_players,
                tenant_id=tenant_context.tenant_id,
                dimensions={
                    "total_score": row.total_score,
                    "games_played": row.games_played
                }
            ))

        return data_points

    async def _collect_quanttrade_data(
        self,
        session: AsyncSession,
        tenant_context: EnhancedTenantContext,
        query: AnalyticsQuery
    ) -> List[AnalyticsDataPoint]:
        """Collect QuantTrade financial data"""

        data_points = []
        time_filter = self._get_time_filter(query)

        # Trading activity data
        trading_query = text("""
            SELECT
                DATE(executed_at) as date,
                COUNT(*) as trades,
                SUM(CASE WHEN profit_loss > 0 THEN profit_loss ELSE 0 END) as profits,
                SUM(CASE WHEN profit_loss < 0 THEN ABS(profit_loss) ELSE 0 END) as losses,
                AVG(profit_loss) as avg_pnl
            FROM trades
            WHERE tenant_id = :tenant_id
                AND executed_at >= :start_date
                AND executed_at <= :end_date
                AND status = 'executed'
            GROUP BY DATE(executed_at)
            ORDER BY date
        """)

        result = await session.execute(
            trading_query,
            {
                "tenant_id": tenant_context.tenant_id,
                "start_date": time_filter["start"],
                "end_date": time_filter["end"]
            }
        )

        for row in result:
            data_points.append(AnalyticsDataPoint(
                timestamp=row.date,
                platform=PlatformType.QUANTTRADE,
                metric_type=MetricType.PERFORMANCE,
                metric_name="trading_performance",
                value=float(row.avg_pnl or 0),
                tenant_id=tenant_context.tenant_id,
                dimensions={
                    "trades": row.trades,
                    "profits": float(row.profits or 0),
                    "losses": float(row.losses or 0)
                }
            ))

        return data_points

    async def generate_platform_metrics(
        self,
        platform_data: Dict[PlatformType, List[AnalyticsDataPoint]]
    ) -> Dict[PlatformType, PlatformMetrics]:
        """Generate aggregated metrics for each platform"""

        platform_metrics = {}

        for platform, data_points in platform_data.items():
            if not data_points:
                platform_metrics[platform] = PlatformMetrics(platform=platform)
                continue

            metrics = PlatformMetrics(platform=platform)

            # Calculate revenue metrics
            revenue_points = [dp for dp in data_points if dp.metric_type == MetricType.REVENUE]
            if revenue_points:
                metrics.total_revenue = Decimal(str(sum(dp.value for dp in revenue_points)))

            # Calculate engagement metrics
            engagement_points = [dp for dp in data_points if dp.metric_type == MetricType.ENGAGEMENT]
            if engagement_points:
                metrics.engagement_score = sum(dp.value for dp in engagement_points) / len(engagement_points)

            # Calculate performance metrics
            performance_points = [dp for dp in data_points if dp.metric_type == MetricType.PERFORMANCE]
            if performance_points:
                metrics.performance_index = sum(dp.value for dp in performance_points) / len(performance_points)

            # Calculate conversion metrics
            conversion_points = [dp for dp in data_points if dp.metric_type == MetricType.CONVERSIONS]
            if conversion_points:
                metrics.conversion_rate = sum(dp.value for dp in conversion_points) / len(conversion_points)

            # Platform-specific calculations
            metrics.key_metrics = await self._calculate_platform_specific_metrics(platform, data_points)

            platform_metrics[platform] = metrics

        return platform_metrics

    async def _calculate_platform_specific_metrics(
        self,
        platform: PlatformType,
        data_points: List[AnalyticsDataPoint]
    ) -> Dict[str, Any]:
        """Calculate platform-specific key metrics"""

        key_metrics = {}

        if platform == PlatformType.BIZOHOLIC:
            # Marketing-specific metrics
            campaign_points = [dp for dp in data_points if "campaign" in dp.metric_name]
            if campaign_points:
                key_metrics["total_campaigns"] = len(campaign_points)
                key_metrics["avg_leads_per_campaign"] = sum(
                    dp.dimensions.get("total_leads", 0) for dp in campaign_points
                ) / len(campaign_points) if campaign_points else 0

        elif platform == PlatformType.CORELDOVE:
            # Ecommerce-specific metrics
            sales_points = [dp for dp in data_points if "sales" in dp.metric_name]
            if sales_points:
                key_metrics["total_orders"] = sum(
                    dp.dimensions.get("orders", 0) for dp in sales_points
                )
                key_metrics["avg_order_value"] = sum(
                    dp.dimensions.get("avg_order_value", 0) for dp in sales_points
                ) / len(sales_points) if sales_points else 0

        elif platform == PlatformType.BUSINESS_DIRECTORY:
            # Directory-specific metrics
            directory_points = [dp for dp in data_points if "directory" in dp.metric_name]
            if directory_points:
                key_metrics["total_listings"] = sum(
                    dp.dimensions.get("new_listings", 0) for dp in directory_points
                )
                key_metrics["avg_rating"] = sum(
                    dp.dimensions.get("avg_rating", 0) for dp in directory_points
                ) / len(directory_points) if directory_points else 0

        elif platform == PlatformType.THRILLRING:
            # Gaming-specific metrics
            gaming_points = [dp for dp in data_points if "gaming" in dp.metric_name]
            if gaming_points:
                key_metrics["total_players"] = max(
                    dp.value for dp in gaming_points
                ) if gaming_points else 0
                key_metrics["total_games"] = sum(
                    dp.dimensions.get("games_played", 0) for dp in gaming_points
                )

        elif platform == PlatformType.QUANTTRADE:
            # Trading-specific metrics
            trading_points = [dp for dp in data_points if "trading" in dp.metric_name]
            if trading_points:
                key_metrics["total_trades"] = sum(
                    dp.dimensions.get("trades", 0) for dp in trading_points
                )
                key_metrics["win_rate"] = self._calculate_win_rate(trading_points)

        return key_metrics

    def _calculate_win_rate(self, trading_points: List[AnalyticsDataPoint]) -> float:
        """Calculate trading win rate"""
        profitable_trades = 0
        total_trades = 0

        for point in trading_points:
            if point.value > 0:  # Positive PnL
                profitable_trades += point.dimensions.get("trades", 0)
            total_trades += point.dimensions.get("trades", 0)

        return (profitable_trades / total_trades * 100) if total_trades > 0 else 0

    async def generate_ai_insights(
        self,
        platform_data: Dict[PlatformType, List[AnalyticsDataPoint]],
        platform_metrics: Dict[PlatformType, PlatformMetrics],
        tenant_context: EnhancedTenantContext
    ) -> List[CrossPlatformInsight]:
        """Generate AI-powered cross-platform insights"""

        insights = []

        # Use AI coordinator to analyze data and generate insights
        analysis_prompt = self._build_analysis_prompt(platform_data, platform_metrics)

        try:
            ai_response = await self.ai_coordinator.coordinate_analysis(
                tenant_context=tenant_context,
                analysis_type="cross_platform_insights",
                data=analysis_prompt,
                agent_specializations=["data_analyst", "business_intelligence", "growth_strategist"]
            )

            # Parse AI response into structured insights
            insights = self._parse_ai_insights(ai_response, platform_metrics)

        except Exception as e:
            logger.error(f"Error generating AI insights: {str(e)}")
            # Fallback to rule-based insights
            insights = await self._generate_rule_based_insights(platform_metrics)

        return insights

    def _build_analysis_prompt(
        self,
        platform_data: Dict[PlatformType, List[AnalyticsDataPoint]],
        platform_metrics: Dict[PlatformType, PlatformMetrics]
    ) -> str:
        """Build analysis prompt for AI insights"""

        prompt = """
        Analyze the following cross-platform analytics data and provide strategic insights:

        Platform Metrics Summary:
        """

        for platform, metrics in platform_metrics.items():
            prompt += f"""
        {platform.value.title()}:
        - Revenue: ${metrics.total_revenue}
        - Engagement Score: {metrics.engagement_score:.2f}
        - Performance Index: {metrics.performance_index:.2f}
        - Conversion Rate: {metrics.conversion_rate:.2f}%
        - Key Metrics: {metrics.key_metrics}
        """

        prompt += """

        Please provide:
        1. Cross-platform performance insights
        2. Optimization opportunities
        3. Growth recommendations
        4. Risk assessments
        5. Strategic priorities

        Focus on actionable insights that can drive business growth across all platforms.
        """

        return prompt

    def _parse_ai_insights(
        self,
        ai_response: Dict[str, Any],
        platform_metrics: Dict[PlatformType, PlatformMetrics]
    ) -> List[CrossPlatformInsight]:
        """Parse AI response into structured insights"""

        insights = []

        try:
            # Extract insights from AI response
            ai_insights = ai_response.get("insights", [])

            for insight_data in ai_insights:
                insight = CrossPlatformInsight(
                    title=insight_data.get("title", "AI Insight"),
                    description=insight_data.get("description", ""),
                    impact_score=float(insight_data.get("impact_score", 0.5)),
                    confidence=float(insight_data.get("confidence", 0.8)),
                    affected_platforms=[
                        PlatformType(p) for p in insight_data.get("platforms", [])
                    ],
                    recommended_actions=insight_data.get("actions", []),
                    priority=insight_data.get("priority", "medium")
                )
                insights.append(insight)

        except Exception as e:
            logger.error(f"Error parsing AI insights: {str(e)}")

        return insights

    async def _generate_rule_based_insights(
        self,
        platform_metrics: Dict[PlatformType, PlatformMetrics]
    ) -> List[CrossPlatformInsight]:
        """Generate rule-based insights as fallback"""

        insights = []

        # Revenue performance insight
        revenue_platforms = {p: m.total_revenue for p, m in platform_metrics.items()}
        top_revenue_platform = max(revenue_platforms.items(), key=lambda x: x[1])

        if top_revenue_platform[1] > 0:
            insights.append(CrossPlatformInsight(
                title="Revenue Performance Leader",
                description=f"{top_revenue_platform[0].value.title()} is your top revenue-generating platform with ${top_revenue_platform[1]}",
                impact_score=0.8,
                confidence=0.9,
                affected_platforms=[top_revenue_platform[0]],
                recommended_actions=[
                    "Scale successful strategies from this platform to others",
                    "Increase marketing investment in this platform",
                    "Analyze what makes this platform successful"
                ],
                priority="high"
            ))

        # Engagement opportunities
        engagement_scores = {p: m.engagement_score for p, m in platform_metrics.items()}
        low_engagement_platforms = [p for p, score in engagement_scores.items() if score < 50]

        if low_engagement_platforms:
            insights.append(CrossPlatformInsight(
                title="Engagement Improvement Opportunity",
                description=f"Platforms {', '.join(p.value for p in low_engagement_platforms)} show low engagement scores",
                impact_score=0.7,
                confidence=0.8,
                affected_platforms=low_engagement_platforms,
                recommended_actions=[
                    "Implement user engagement campaigns",
                    "Analyze successful engagement strategies from other platforms",
                    "A/B test new features to improve user interaction"
                ],
                priority="medium"
            ))

        return insights

    async def generate_predictive_analytics(
        self,
        platform_data: Dict[PlatformType, List[AnalyticsDataPoint]],
        tenant_context: EnhancedTenantContext
    ) -> List[PredictiveAnalytics]:
        """Generate predictive analytics and forecasting"""

        predictions = []

        for platform, data_points in platform_data.items():
            if len(data_points) < 7:  # Need at least 7 days of data
                continue

            # Group data by metric type
            metric_groups = {}
            for point in data_points:
                metric_key = f"{point.metric_type}_{point.metric_name}"
                if metric_key not in metric_groups:
                    metric_groups[metric_key] = []
                metric_groups[metric_key].append(point)

            for metric_key, points in metric_groups.items():
                if len(points) >= 7:
                    prediction = await self._create_prediction(platform, metric_key, points)
                    if prediction:
                        predictions.append(prediction)

        return predictions

    async def _create_prediction(
        self,
        platform: PlatformType,
        metric_key: str,
        data_points: List[AnalyticsDataPoint]
    ) -> Optional[PredictiveAnalytics]:
        """Create prediction for specific metric"""

        try:
            # Sort by timestamp
            sorted_points = sorted(data_points, key=lambda x: x.timestamp)

            # Extract values and timestamps
            values = [float(point.value) for point in sorted_points]
            timestamps = [point.timestamp for point in sorted_points]

            # Simple linear regression for trend prediction
            X = np.array(range(len(values))).reshape(-1, 1)
            y = np.array(values)

            # Calculate trend
            slope = np.polyfit(range(len(values)), values, 1)[0]

            # Generate 30-day forecast
            forecast_days = 30
            predicted_values = []

            for i in range(forecast_days):
                future_index = len(values) + i
                predicted_value = values[-1] + (slope * (i + 1))
                future_date = timestamps[-1] + timedelta(days=i+1)

                predicted_values.append({
                    "date": future_date.isoformat(),
                    "value": max(0, predicted_value),  # Ensure non-negative
                    "confidence": max(0.3, 0.9 - (i * 0.02))  # Decreasing confidence
                })

            # Calculate model accuracy (simplified)
            model_accuracy = min(0.95, max(0.3, 1.0 - abs(slope / np.mean(values)) if np.mean(values) > 0 else 0.5))

            return PredictiveAnalytics(
                metric_name=metric_key,
                platform=platform,
                forecast_horizon=forecast_days,
                predicted_values=predicted_values,
                confidence_interval={"lower": 0.8, "upper": 0.95},
                model_accuracy=model_accuracy,
                factors=["historical_trend", "seasonal_patterns", "market_conditions"]
            )

        except Exception as e:
            logger.error(f"Error creating prediction for {metric_key}: {str(e)}")
            return None

    async def build_unified_dashboard(
        self,
        session: AsyncSession,
        tenant_context: EnhancedTenantContext,
        query: AnalyticsQuery
    ) -> AnalyticsDashboard:
        """Build complete unified analytics dashboard"""

        # Collect platform data
        platform_data = await self.collect_platform_data(session, tenant_context, query)

        # Generate platform metrics
        platform_metrics = await self.generate_platform_metrics(platform_data)

        # Generate AI insights
        insights = await self.generate_ai_insights(platform_data, platform_metrics, tenant_context)

        # Generate predictions if requested
        predictions = []
        if query.include_predictions:
            predictions = await self.generate_predictive_analytics(platform_data, tenant_context)

        # Calculate KPI summary
        kpi_summary = self._calculate_kpi_summary(platform_metrics)

        # Generate AI recommendations
        ai_recommendations = await self._generate_ai_recommendations(insights, platform_metrics)

        # Build custom widgets based on subscription tier
        custom_widgets = self._build_custom_widgets(tenant_context.subscription_tier, platform_metrics)

        dashboard = AnalyticsDashboard(
            tenant_id=tenant_context.tenant_id,
            time_range=query.time_range,
            platform_metrics=platform_metrics,
            cross_platform_insights=insights,
            ai_recommendations=ai_recommendations,
            kpi_summary=kpi_summary,
            subscription_tier=tenant_context.subscription_tier,
            custom_widgets=custom_widgets
        )

        return dashboard

    def _calculate_kpi_summary(
        self,
        platform_metrics: Dict[PlatformType, PlatformMetrics]
    ) -> Dict[str, Any]:
        """Calculate overall KPI summary across platforms"""

        total_revenue = sum(m.total_revenue for m in platform_metrics.values())
        avg_engagement = sum(m.engagement_score for m in platform_metrics.values()) / len(platform_metrics) if platform_metrics else 0
        avg_performance = sum(m.performance_index for m in platform_metrics.values()) / len(platform_metrics) if platform_metrics else 0
        avg_conversion = sum(m.conversion_rate for m in platform_metrics.values()) / len(platform_metrics) if platform_metrics else 0

        return {
            "total_revenue": float(total_revenue),
            "avg_engagement_score": avg_engagement,
            "avg_performance_index": avg_performance,
            "avg_conversion_rate": avg_conversion,
            "active_platforms": len(platform_metrics),
            "top_performing_platform": max(
                platform_metrics.items(),
                key=lambda x: x[1].performance_index
            )[0].value if platform_metrics else None
        }

    async def _generate_ai_recommendations(
        self,
        insights: List[CrossPlatformInsight],
        platform_metrics: Dict[PlatformType, PlatformMetrics]
    ) -> List[str]:
        """Generate AI-powered recommendations"""

        recommendations = []

        # High-priority insights recommendations
        high_priority_insights = [i for i in insights if i.priority == "high"]
        for insight in high_priority_insights[:3]:  # Top 3 high-priority
            recommendations.extend(insight.recommended_actions[:2])  # Top 2 actions each

        # Performance-based recommendations
        performance_scores = {p: m.performance_index for p, m in platform_metrics.items()}

        if performance_scores:
            best_platform = max(performance_scores.items(), key=lambda x: x[1])
            worst_platform = min(performance_scores.items(), key=lambda x: x[1])

            if best_platform[1] > worst_platform[1] + 20:  # Significant difference
                recommendations.append(
                    f"Apply successful strategies from {best_platform[0].value} to improve {worst_platform[0].value} performance"
                )

        # Revenue optimization recommendations
        revenue_totals = {p: m.total_revenue for p, m in platform_metrics.items()}
        if revenue_totals:
            top_revenue = max(revenue_totals.items(), key=lambda x: x[1])
            recommendations.append(
                f"Scale marketing investments in {top_revenue[0].value} as it generates the highest revenue"
            )

        return recommendations[:5]  # Limit to top 5 recommendations

    def _build_custom_widgets(
        self,
        subscription_tier: TenantTier,
        platform_metrics: Dict[PlatformType, PlatformMetrics]
    ) -> List[Dict[str, Any]]:
        """Build custom dashboard widgets based on subscription tier"""

        widgets = []

        # Basic widgets for all tiers
        widgets.append({
            "type": "revenue_chart",
            "title": "Revenue Overview",
            "data": {p.value: float(m.total_revenue) for p, m in platform_metrics.items()},
            "chart_type": "bar"
        })

        widgets.append({
            "type": "engagement_metrics",
            "title": "Engagement Scores",
            "data": {p.value: m.engagement_score for p, m in platform_metrics.items()},
            "chart_type": "radar"
        })

        # Advanced widgets for higher tiers
        if subscription_tier in [TenantTier.PROFESSIONAL, TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]:
            widgets.append({
                "type": "performance_heatmap",
                "title": "Platform Performance Matrix",
                "data": {
                    p.value: {
                        "performance": m.performance_index,
                        "engagement": m.engagement_score,
                        "conversion": m.conversion_rate
                    } for p, m in platform_metrics.items()
                },
                "chart_type": "heatmap"
            })

        # Enterprise-only widgets
        if subscription_tier in [TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]:
            widgets.append({
                "type": "predictive_analytics",
                "title": "Revenue Forecast",
                "data": "predictive_chart_data",
                "chart_type": "line_with_forecast"
            })

            widgets.append({
                "type": "ai_insights_panel",
                "title": "AI-Powered Insights",
                "data": "insights_summary",
                "chart_type": "insight_cards"
            })

        return widgets

    def _get_accessible_platforms(
        self,
        tenant_context: EnhancedTenantContext,
        requested_platforms: List[PlatformType]
    ) -> List[PlatformType]:
        """Get platforms accessible based on subscription and platform access"""

        accessible = []

        # Check platform access permissions
        for platform in requested_platforms or list(PlatformType):
            platform_access = tenant_context.platform_access.get(platform)
            if platform_access and platform_access.enabled:
                accessible.append(platform)

        # If no platforms requested, return all accessible platforms
        if not requested_platforms:
            accessible = [
                platform for platform, access in tenant_context.platform_access.items()
                if access.enabled
            ]

        return accessible

    def _get_time_filter(self, query: AnalyticsQuery) -> Dict[str, datetime]:
        """Get time filter based on query parameters"""

        end_date = datetime.utcnow()

        if query.time_range == TimeRange.CUSTOM:
            start_date = query.custom_start or (end_date - timedelta(days=30))
            end_date = query.custom_end or end_date
        elif query.time_range == TimeRange.LAST_24_HOURS:
            start_date = end_date - timedelta(hours=24)
        elif query.time_range == TimeRange.LAST_7_DAYS:
            start_date = end_date - timedelta(days=7)
        elif query.time_range == TimeRange.LAST_30_DAYS:
            start_date = end_date - timedelta(days=30)
        elif query.time_range == TimeRange.LAST_90_DAYS:
            start_date = end_date - timedelta(days=90)
        elif query.time_range == TimeRange.LAST_YEAR:
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=30)

        return {"start": start_date, "end": end_date}

# Export the service class
__all__ = ["UnifiedAnalyticsService", "AnalyticsDashboard", "AnalyticsQuery", "CrossPlatformInsight"]