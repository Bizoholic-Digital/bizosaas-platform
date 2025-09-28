"""
Analytics Domain - Bounded Context for Performance Analytics and Reporting
Implements analytics aggregates with metric collection and reporting logic
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, text
from sqlalchemy.orm import selectinload

from shared.database.models import Metric, Report, Dashboard

logger = logging.getLogger(__name__)


class AnalyticsAggregate:
    """Analytics aggregate for metric collection and calculation"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.metrics_buffer = []
    
    def record_metric(self, entity_type: str, entity_id: str, 
                     metric_name: str, metric_value: float,
                     metric_unit: str = None, dimensions: Dict[str, Any] = None):
        """Record a single metric with validation"""
        if not metric_name or len(metric_name.strip()) == 0:
            raise ValueError("Metric name is required")
        
        if not isinstance(metric_value, (int, float)):
            raise ValueError("Metric value must be numeric")
        
        metric = {
            'entity_type': entity_type,
            'entity_id': entity_id,
            'metric_name': metric_name,
            'metric_value': float(metric_value),
            'metric_unit': metric_unit,
            'dimensions': dimensions or {},
            'timestamp': datetime.utcnow()
        }
        
        self.metrics_buffer.append(metric)
        logger.debug(f"Recorded metric: {metric_name} = {metric_value} for {entity_type}:{entity_id}")
    
    def calculate_performance_score(self, metrics: Dict[str, float]) -> float:
        """Calculate overall performance score based on multiple metrics"""
        if not metrics:
            return 0.0
        
        # Weight different metrics
        weights = {
            'conversion_rate': 0.3,
            'ctr': 0.2,
            'roi': 0.25,
            'quality_score': 0.15,
            'engagement_rate': 0.1
        }
        
        weighted_score = 0.0
        total_weight = 0.0
        
        for metric_name, value in metrics.items():
            weight = weights.get(metric_name, 0.1)
            
            # Normalize different metrics to 0-100 scale
            normalized_value = self._normalize_metric(metric_name, value)
            weighted_score += normalized_value * weight
            total_weight += weight
        
        return weighted_score / total_weight if total_weight > 0 else 0.0
    
    def _normalize_metric(self, metric_name: str, value: float) -> float:
        """Normalize different metrics to 0-100 scale"""
        normalizations = {
            'conversion_rate': lambda x: min(x * 5, 100),  # 20% = 100 score
            'ctr': lambda x: min(x * 10, 100),  # 10% = 100 score
            'roi': lambda x: min(x / 5, 100),  # 500% = 100 score
            'quality_score': lambda x: x,  # Already 0-100
            'engagement_rate': lambda x: min(x * 2, 100)  # 50% = 100 score
        }
        
        normalizer = normalizations.get(metric_name, lambda x: min(x, 100))
        return max(0, normalizer(value))
    
    def get_buffered_metrics(self):
        """Get buffered metrics for batch processing"""
        return self.metrics_buffer.copy()
    
    def clear_buffer(self):
        """Clear metrics buffer after processing"""
        self.metrics_buffer.clear()


class AnalyticsDomain:
    """Domain service for analytics operations"""
    
    def __init__(self, db_session: AsyncSession, tenant_id: str):
        self.db = db_session
        self.tenant_id = tenant_id
        self.aggregate = AnalyticsAggregate(tenant_id)
    
    async def record_metrics(self, entity_type: str, entity_id: str, 
                           metrics: Dict[str, Any]):
        """Record multiple metrics for an entity"""
        try:
            # Use aggregate to validate and buffer metrics
            for metric_name, metric_data in metrics.items():
                if isinstance(metric_data, dict):
                    value = metric_data.get('value', 0)
                    unit = metric_data.get('unit')
                    dimensions = metric_data.get('dimensions', {})
                else:
                    value = metric_data
                    unit = None
                    dimensions = {}
                
                self.aggregate.record_metric(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    metric_name=metric_name,
                    metric_value=value,
                    metric_unit=unit,
                    dimensions=dimensions
                )
            
            # In real implementation, persist buffered metrics to database
            buffered_metrics = self.aggregate.get_buffered_metrics()
            for metric in buffered_metrics:
                # metric_record = Metric(
                #     tenant_id=self.tenant_id,
                #     entity_type=metric['entity_type'],
                #     entity_id=metric['entity_id'],
                #     metric_name=metric['metric_name'],
                #     metric_value=metric['metric_value'],
                #     metric_unit=metric['metric_unit'],
                #     dimensions=metric['dimensions'],
                #     timestamp=metric['timestamp']
                # )
                # self.db.add(metric_record)
                pass
            
            # await self.db.commit()
            self.aggregate.clear_buffer()
            
            logger.info(f"Recorded {len(buffered_metrics)} metrics for {entity_type}:{entity_id}")
            
        except Exception as e:
            logger.error(f"Failed to record metrics: {e}")
            raise
    
    async def get_campaign_metrics(self) -> List[Dict[str, Any]]:
        """Get aggregated campaign metrics"""
        try:
            # In real implementation, query actual metrics from database
            # For now, return mock data
            mock_campaigns = [
                {
                    "campaign_id": "camp_1",
                    "campaign_name": "Google Ads Q4",
                    "spend": 5420.50,
                    "impressions": 125430,
                    "clicks": 3210,
                    "conversions": 45,
                    "ctr": 2.56,
                    "cpc": 1.69,
                    "conversion_rate": 1.40,
                    "roi": 185.3,
                    "performance_score": 78.5
                },
                {
                    "campaign_id": "camp_2", 
                    "campaign_name": "LinkedIn B2B",
                    "spend": 3200.00,
                    "impressions": 45200,
                    "clicks": 1420,
                    "conversions": 28,
                    "ctr": 3.14,
                    "cpc": 2.25,
                    "conversion_rate": 1.97,
                    "roi": 156.8,
                    "performance_score": 82.1
                }
            ]
            
            # Calculate performance scores using aggregate
            for campaign in mock_campaigns:
                metrics = {
                    'conversion_rate': campaign['conversion_rate'],
                    'ctr': campaign['ctr'],
                    'roi': campaign['roi'] / 100
                }
                campaign['performance_score'] = round(
                    self.aggregate.calculate_performance_score(metrics), 1
                )
            
            return mock_campaigns
            
        except Exception as e:
            logger.error(f"Failed to get campaign metrics: {e}")
            raise
    
    async def get_lead_metrics(self) -> List[Dict[str, Any]]:
        """Get aggregated lead metrics"""
        try:
            # In real implementation, query lead pipeline data
            mock_lead_metrics = [
                {
                    "source": "google_ads",
                    "leads_captured": 145,
                    "leads_qualified": 78,
                    "leads_converted": 12,
                    "conversion_rate": 8.28,
                    "avg_score": 67.5,
                    "total_value": 48000
                },
                {
                    "source": "linkedin_ads",
                    "leads_captured": 89,
                    "leads_qualified": 62,
                    "leads_converted": 18,
                    "conversion_rate": 20.22,
                    "avg_score": 74.2,
                    "total_value": 72000
                },
                {
                    "source": "organic_search",
                    "leads_captured": 234,
                    "leads_qualified": 156,
                    "leads_converted": 28,
                    "conversion_rate": 11.97,
                    "avg_score": 58.9,
                    "total_value": 84000
                }
            ]
            
            return mock_lead_metrics
            
        except Exception as e:
            logger.error(f"Failed to get lead metrics: {e}")
            raise
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary"""
        try:
            # In real implementation, aggregate from multiple sources
            summary = {
                "total_campaigns": 12,
                "active_campaigns": 8,
                "total_spend": 45620.50,
                "total_revenue": 284000.00,
                "overall_roi": 522.3,
                "total_leads": 1247,
                "qualified_leads": 689,
                "converted_leads": 94,
                "avg_conversion_rate": 7.54,
                "top_performing_source": "linkedin_ads",
                "top_performing_campaign": "LinkedIn B2B",
                "monthly_trend": 15.8,  # % growth
                "quality_score": 78.5,
                "performance_rating": "Excellent"
            }
            
            # Calculate derived metrics
            summary["avg_deal_value"] = summary["total_revenue"] / summary["converted_leads"]
            summary["cost_per_lead"] = summary["total_spend"] / summary["total_leads"]
            summary["lead_to_customer_rate"] = (summary["converted_leads"] / summary["total_leads"]) * 100
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get performance summary: {e}")
            raise
    
    async def generate_report(self, report_type: str, date_range_start: datetime,
                            date_range_end: datetime, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        try:
            # In real implementation, generate detailed reports based on type
            report_data = {
                "report_id": str(uuid4()),
                "report_type": report_type,
                "generated_at": datetime.utcnow(),
                "date_range": {
                    "start": date_range_start.isoformat(),
                    "end": date_range_end.isoformat()
                },
                "filters": filters or {},
                "summary": await self.get_performance_summary()
            }
            
            if report_type == "campaign_performance":
                report_data["campaigns"] = await self.get_campaign_metrics()
            elif report_type == "lead_analysis":
                report_data["leads"] = await self.get_lead_metrics()
            elif report_type == "roi_analysis":
                report_data["roi_breakdown"] = await self._get_roi_breakdown()
            
            return report_data
            
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            raise
    
    async def _get_roi_breakdown(self) -> Dict[str, Any]:
        """Get detailed ROI breakdown"""
        return {
            "by_channel": {
                "google_ads": {"spend": 15420, "revenue": 89200, "roi": 478.2},
                "linkedin_ads": {"spend": 8900, "revenue": 72000, "roi": 709.0},
                "facebook_ads": {"spend": 12300, "revenue": 45600, "roi": 270.7}
            },
            "by_campaign_type": {
                "lead_generation": {"spend": 22500, "revenue": 128000, "roi": 468.9},
                "brand_awareness": {"spend": 8200, "revenue": 34800, "roi": 324.4},
                "retargeting": {"spend": 6920, "revenue": 43200, "roi": 524.3}
            },
            "monthly_trend": [
                {"month": "Jan", "roi": 345.6},
                {"month": "Feb", "roi": 412.3},
                {"month": "Mar", "roi": 389.7},
                {"month": "Apr", "roi": 456.8},
                {"month": "May", "roi": 522.3}
            ]
        }