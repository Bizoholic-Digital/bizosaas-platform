"""
AI Command Processor for Natural Language Analytics Queries
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class AICommandProcessor:
    """Process natural language queries and convert to Superset API calls"""
    
    def __init__(self):
        self.intent_patterns = {
            "get_chart_data": [
                r"show.*(?:chart|graph|data)",
                r"display.*(?:analytics|metrics)",
                r"get.*(?:sales|revenue|users)",
                r"(?:sales|revenue|metrics|analytics).*(?:last|this|past)"
            ],
            "create_dashboard": [
                r"create.*dashboard",
                r"build.*dashboard",
                r"make.*dashboard",
                r"new dashboard"
            ],
            "get_insights": [
                r"what.*(?:trends|patterns|insights)",
                r"analyze.*(?:data|performance)",
                r"insights?.*(?:from|about)",
                r"tell me about"
            ],
            "compare_metrics": [
                r"compare.*(?:to|with|vs)",
                r"(?:difference|delta).*between",
                r"vs\.|versus"
            ]
        }
        
        self.time_patterns = {
            "last_week": [r"last week", r"past week"],
            "last_month": [r"last month", r"past month", r"previous month"],
            "last_quarter": [r"last quarter", r"past quarter", r"q[1-4]"],
            "today": [r"today", r"this day"],
            "yesterday": [r"yesterday"],
            "this_week": [r"this week", r"current week"],
            "this_month": [r"this month", r"current month"],
            "this_year": [r"this year", r"current year"]
        }
        
        self.metric_patterns = {
            "sales": [r"sales", r"revenue", r"income"],
            "users": [r"users?", r"customers?", r"visitors?"],
            "sessions": [r"sessions?", r"visits?"],
            "conversions": [r"conversions?", r"conversion rate"],
            "engagement": [r"engagement", r"time on site", r"bounce rate"]
        }

    async def parse_analytics_query(self, query: str, tenant_id: str) -> Dict[str, Any]:
        """Parse natural language query into structured analytics request"""
        
        query_lower = query.lower()
        
        # Detect intent
        intent = self._detect_intent(query_lower)
        
        # Extract time period
        time_period = self._extract_time_period(query_lower)
        
        # Extract metrics
        metrics = self._extract_metrics(query_lower)
        
        # Extract filters
        filters = self._extract_filters(query_lower, tenant_id)
        
        result = {
            "intent": intent,
            "query": query,
            "time_period": time_period,
            "metrics": metrics,
            "filters": filters,
            "tenant_id": tenant_id
        }
        
        # Add specific parameters based on intent
        if intent == "get_chart_data":
            result["chart_id"] = self._suggest_chart_id(metrics, time_period)
            
        elif intent == "create_dashboard":
            result["dashboard_spec"] = self._generate_dashboard_spec(metrics, time_period)
            
        elif intent == "get_insights":
            result["analysis_type"] = "trend_analysis"
            
        return result

    def _detect_intent(self, query: str) -> str:
        """Detect the intent of the natural language query"""
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return intent
        
        # Default to data query if no specific intent found
        return "get_chart_data"

    def _extract_time_period(self, query: str) -> Dict[str, Any]:
        """Extract time period from query"""
        
        for period, patterns in self.time_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return {
                        "type": period,
                        "start_date": self._get_period_start_date(period),
                        "end_date": datetime.now().date()
                    }
        
        # Default to last 30 days
        return {
            "type": "last_month",
            "start_date": (datetime.now() - timedelta(days=30)).date(),
            "end_date": datetime.now().date()
        }

    def _extract_metrics(self, query: str) -> List[str]:
        """Extract metrics from query"""
        
        detected_metrics = []
        
        for metric, patterns in self.metric_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    detected_metrics.append(metric)
        
        # If no specific metrics found, default to basic metrics
        if not detected_metrics:
            detected_metrics = ["sales", "users", "sessions"]
        
        return detected_metrics

    def _extract_filters(self, query: str, tenant_id: str) -> Dict[str, Any]:
        """Extract filters from query"""
        
        filters = [
            {
                "col": "tenant_id",
                "op": "==",
                "val": tenant_id
            }
        ]
        
        # Extract region filters
        region_patterns = [r"in ([\w\s]+)", r"from ([\w\s]+)", r"by region"]
        for pattern in region_patterns:
            match = re.search(pattern, query)
            if match and len(match.groups()) > 0:
                region = match.group(1).strip()
                filters.append({
                    "col": "region",
                    "op": "==",
                    "val": region
                })
        
        return {"filters": filters}

    def _suggest_chart_id(self, metrics: List[str], time_period: Dict) -> Optional[int]:
        """Suggest appropriate chart ID based on metrics and time period"""
        
        # Simple mapping - in production this would query available charts
        chart_mapping = {
            ("sales",): 1,
            ("users",): 2,
            ("sessions",): 3,
            ("sales", "users"): 4,
            ("conversions",): 5
        }
        
        # Try exact match first
        metrics_tuple = tuple(sorted(metrics))
        if metrics_tuple in chart_mapping:
            return chart_mapping[metrics_tuple]
        
        # Try single metric matches
        for metric in metrics:
            if (metric,) in chart_mapping:
                return chart_mapping[(metric,)]
        
        # Default chart
        return 1

    def _generate_dashboard_spec(self, metrics: List[str], time_period: Dict) -> Dict[str, Any]:
        """Generate dashboard specification from metrics and time period"""
        
        return {
            "dashboard_title": f"Analytics Dashboard - {time_period['type'].replace('_', ' ').title()}",
            "description": f"Dashboard showing {', '.join(metrics)} metrics",
            "charts": [
                {
                    "chart_type": "line_chart",
                    "metrics": metrics,
                    "time_period": time_period
                },
                {
                    "chart_type": "bar_chart", 
                    "metrics": metrics[:2],  # Limit to 2 metrics for bar chart
                    "time_period": time_period
                }
            ]
        }

    def _get_period_start_date(self, period: str) -> datetime.date:
        """Get start date for a given period"""
        
        now = datetime.now()
        
        if period == "last_week":
            return (now - timedelta(weeks=1)).date()
        elif period == "last_month":
            return (now - timedelta(days=30)).date()
        elif period == "last_quarter":
            return (now - timedelta(days=90)).date()
        elif period == "yesterday":
            return (now - timedelta(days=1)).date()
        elif period == "this_week":
            days_since_monday = now.weekday()
            return (now - timedelta(days=days_since_monday)).date()
        elif period == "this_month":
            return now.replace(day=1).date()
        elif period == "this_year":
            return now.replace(month=1, day=1).date()
        else:
            return (now - timedelta(days=7)).date()  # Default to last week