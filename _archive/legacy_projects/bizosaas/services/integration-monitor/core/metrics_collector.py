"""
Metrics Collector
Collects and aggregates monitoring metrics for analysis and reporting
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict, deque
import statistics

logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Collects and aggregates metrics from health checks and system monitoring
    Provides historical data analysis and trend calculation
    """
    
    def __init__(self, max_data_points: int = 10000):
        # Raw metrics storage
        self.health_metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_data_points))
        self.system_metrics: deque = deque(maxlen=max_data_points)
        self.error_metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_data_points))
        self.cost_metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_data_points))
        
        # Aggregated metrics cache
        self.aggregated_cache: Dict[str, Any] = {}
        self.cache_ttl: int = 60  # Cache for 1 minute
        self.last_cache_update: float = 0
        
        # Performance tracking
        self.collection_stats = {
            'total_collections': 0,
            'failed_collections': 0,
            'average_collection_time': 0.0,
            'last_collection_time': 0.0
        }
        
        logger.info("Metrics Collector initialized")
    
    async def record_health_check(self, health_data: Any):
        """Record health check result"""
        try:
            start_time = time.time()
            
            integration_name = health_data.name
            timestamp = time.time()
            
            # Create health metric record
            health_record = {
                'timestamp': timestamp,
                'integration': integration_name,
                'status': health_data.status.value if hasattr(health_data.status, 'value') else str(health_data.status),
                'response_time': health_data.response_time,
                'error_rate': health_data.error_rate,
                'uptime': health_data.uptime,
                'health_score': health_data.health_score,
                'cost_today': health_data.cost_today,
                'rate_limit_usage': health_data.rate_limit_usage,
                'consecutive_failures': health_data.consecutive_failures
            }
            
            # Store in health metrics
            self.health_metrics[integration_name].append(health_record)
            
            # Record error if unhealthy
            if health_data.status.value != 'healthy':
                error_record = {
                    'timestamp': timestamp,
                    'integration': integration_name,
                    'error_type': health_data.status.value,
                    'response_time': health_data.response_time,
                    'metadata': health_data.metadata
                }
                self.error_metrics[integration_name].append(error_record)
            
            # Record cost data
            cost_record = {
                'timestamp': timestamp,
                'integration': integration_name,
                'cost': health_data.cost_today,
                'requests': getattr(health_data, 'request_count', 0)
            }
            self.cost_metrics[integration_name].append(cost_record)
            
            # Update collection stats
            collection_time = time.time() - start_time
            self._update_collection_stats(collection_time, success=True)
            
            # Invalidate cache
            self.last_cache_update = 0
            
            logger.debug(f"Recorded health metrics for {integration_name}")
            
        except Exception as e:
            logger.error(f"Failed to record health check metrics: {e}")
            self._update_collection_stats(0, success=False)
    
    async def record_system_metrics(self, metrics_data: Any):
        """Record system-level metrics"""
        try:
            timestamp = time.time()
            
            system_record = {
                'timestamp': timestamp,
                'total_integrations': metrics_data.total_integrations,
                'healthy_count': metrics_data.healthy_count,
                'degraded_count': metrics_data.degraded_count,
                'unhealthy_count': metrics_data.unhealthy_count,
                'average_response_time': metrics_data.average_response_time,
                'total_error_rate': metrics_data.total_error_rate,
                'average_uptime': metrics_data.average_uptime,
                'active_alerts': metrics_data.active_alerts,
                'failovers_today': metrics_data.failovers_today,
                'cost_today': metrics_data.cost_today
            }
            
            self.system_metrics.append(system_record)
            
            # Invalidate cache
            self.last_cache_update = 0
            
            logger.debug("Recorded system metrics")
            
        except Exception as e:
            logger.error(f"Failed to record system metrics: {e}")
    
    async def update_system_metrics(self, metrics_data: Any):
        """Update system metrics (alias for record_system_metrics)"""
        await self.record_system_metrics(metrics_data)
    
    def get_integration_metrics(self, integration_name: str, period_hours: int = 24) -> Dict[str, Any]:
        """Get metrics for specific integration over a time period"""
        
        if integration_name not in self.health_metrics:
            return {
                'integration': integration_name,
                'period_hours': period_hours,
                'data_points': 0,
                'metrics': {}
            }
        
        # Filter data by time period
        cutoff_time = time.time() - (period_hours * 3600)
        health_data = [
            record for record in self.health_metrics[integration_name]
            if record['timestamp'] >= cutoff_time
        ]
        
        if not health_data:
            return {
                'integration': integration_name,
                'period_hours': period_hours,
                'data_points': 0,
                'metrics': {}
            }
        
        # Calculate metrics
        response_times = [r['response_time'] for r in health_data]
        error_rates = [r['error_rate'] for r in health_data]
        uptimes = [r['uptime'] for r in health_data]
        health_scores = [r['health_score'] for r in health_data]
        costs = [r['cost_today'] for r in health_data]
        
        # Status distribution
        status_counts = defaultdict(int)
        for record in health_data:
            status_counts[record['status']] += 1
        
        metrics = {
            'integration': integration_name,
            'period_hours': period_hours,
            'data_points': len(health_data),
            'response_time': {
                'average': statistics.mean(response_times),
                'median': statistics.median(response_times),
                'min': min(response_times),
                'max': max(response_times),
                'p95': self._percentile(response_times, 95),
                'p99': self._percentile(response_times, 99)
            },
            'error_rate': {
                'average': statistics.mean(error_rates),
                'max': max(error_rates),
                'trend': self._calculate_trend([r['error_rate'] for r in health_data[-10:]])
            },
            'uptime': {
                'average': statistics.mean(uptimes),
                'min': min(uptimes),
                'current': health_data[-1]['uptime'] if health_data else 0
            },
            'health_score': {
                'average': statistics.mean(health_scores),
                'current': health_data[-1]['health_score'] if health_data else 0,
                'trend': self._calculate_trend([r['health_score'] for r in health_data[-10:]])
            },
            'cost': {
                'total': sum(costs),
                'average_daily': statistics.mean(costs),
                'trend': self._calculate_trend([r['cost_today'] for r in health_data[-10:]])
            },
            'status_distribution': dict(status_counts),
            'availability': self._calculate_availability(health_data),
            'reliability_score': self._calculate_reliability_score(health_data)
        }
        
        return metrics
    
    def get_system_overview(self, period_hours: int = 24) -> Dict[str, Any]:
        """Get system-wide metrics overview"""
        
        # Use cached data if available and fresh
        cache_key = f"system_overview_{period_hours}"
        if (cache_key in self.aggregated_cache and 
            time.time() - self.last_cache_update < self.cache_ttl):
            return self.aggregated_cache[cache_key]
        
        # Filter system data by time period
        cutoff_time = time.time() - (period_hours * 3600)
        system_data = [
            record for record in self.system_metrics
            if record['timestamp'] >= cutoff_time
        ]
        
        if not system_data:
            return {
                'period_hours': period_hours,
                'data_points': 0,
                'overview': {}
            }
        
        # Calculate system metrics
        latest_record = system_data[-1]
        
        # Trends
        response_time_trend = self._calculate_trend([r['average_response_time'] for r in system_data[-10:]])
        error_rate_trend = self._calculate_trend([r['total_error_rate'] for r in system_data[-10:]])
        uptime_trend = self._calculate_trend([r['average_uptime'] for r in system_data[-10:]])
        cost_trend = self._calculate_trend([r['cost_today'] for r in system_data[-10:]])
        
        overview = {
            'period_hours': period_hours,
            'data_points': len(system_data),
            'current_status': {
                'total_integrations': latest_record['total_integrations'],
                'healthy_integrations': latest_record['healthy_count'],
                'degraded_integrations': latest_record['degraded_count'],
                'unhealthy_integrations': latest_record['unhealthy_count'],
                'health_percentage': (latest_record['healthy_count'] / latest_record['total_integrations'] * 100) if latest_record['total_integrations'] > 0 else 0
            },
            'performance': {
                'average_response_time': latest_record['average_response_time'],
                'response_time_trend': response_time_trend,
                'total_error_rate': latest_record['total_error_rate'],
                'error_rate_trend': error_rate_trend,
                'average_uptime': latest_record['average_uptime'],
                'uptime_trend': uptime_trend
            },
            'alerts': {
                'active_alerts': latest_record['active_alerts'],
                'failovers_today': latest_record['failovers_today']
            },
            'costs': {
                'total_cost_today': latest_record['cost_today'],
                'cost_trend': cost_trend
            },
            'trends': {
                'response_time': f"{response_time_trend:+.1f}%",
                'error_rate': f"{error_rate_trend:+.1f}%",
                'uptime': f"{uptime_trend:+.1f}%",
                'cost': f"{cost_trend:+.1f}%"
            }
        }
        
        # Cache the result
        self.aggregated_cache[cache_key] = overview
        self.last_cache_update = time.time()
        
        return overview
    
    def get_integration_comparison(self, integration_names: List[str], period_hours: int = 24) -> Dict[str, Any]:
        """Compare metrics across multiple integrations"""
        
        comparison_data = {}
        
        for integration_name in integration_names:
            metrics = self.get_integration_metrics(integration_name, period_hours)
            comparison_data[integration_name] = {
                'response_time': metrics.get('response_time', {}).get('average', 0),
                'error_rate': metrics.get('error_rate', {}).get('average', 0),
                'uptime': metrics.get('uptime', {}).get('average', 0),
                'health_score': metrics.get('health_score', {}).get('current', 0),
                'cost': metrics.get('cost', {}).get('total', 0),
                'availability': metrics.get('availability', 0)
            }
        
        # Calculate rankings
        rankings = {
            'best_response_time': sorted(comparison_data.items(), key=lambda x: x[1]['response_time'])[:3],
            'worst_response_time': sorted(comparison_data.items(), key=lambda x: x[1]['response_time'], reverse=True)[:3],
            'best_uptime': sorted(comparison_data.items(), key=lambda x: x[1]['uptime'], reverse=True)[:3],
            'highest_cost': sorted(comparison_data.items(), key=lambda x: x[1]['cost'], reverse=True)[:3],
            'best_health_score': sorted(comparison_data.items(), key=lambda x: x[1]['health_score'], reverse=True)[:3]
        }
        
        return {
            'period_hours': period_hours,
            'integrations': comparison_data,
            'rankings': rankings,
            'summary': {
                'total_integrations': len(integration_names),
                'average_response_time': statistics.mean([data['response_time'] for data in comparison_data.values()]),
                'average_uptime': statistics.mean([data['uptime'] for data in comparison_data.values()]),
                'total_cost': sum([data['cost'] for data in comparison_data.values()])
            }
        }
    
    def get_error_analysis(self, period_hours: int = 24) -> Dict[str, Any]:
        """Analyze error patterns and trends"""
        
        cutoff_time = time.time() - (period_hours * 3600)
        all_errors = []
        
        # Collect all errors within time period
        for integration_name, error_deque in self.error_metrics.items():
            for error in error_deque:
                if error['timestamp'] >= cutoff_time:
                    all_errors.append(error)
        
        if not all_errors:
            return {
                'period_hours': period_hours,
                'total_errors': 0,
                'analysis': {}
            }
        
        # Analyze error patterns
        error_by_type = defaultdict(int)
        error_by_integration = defaultdict(int)
        error_by_hour = defaultdict(int)
        
        for error in all_errors:
            error_by_type[error['error_type']] += 1
            error_by_integration[error['integration']] += 1
            
            # Group by hour
            hour_key = datetime.fromtimestamp(error['timestamp']).strftime('%Y-%m-%d %H:00')
            error_by_hour[hour_key] += 1
        
        # Find patterns
        most_common_error = max(error_by_type.items(), key=lambda x: x[1]) if error_by_type else ('none', 0)
        most_problematic_integration = max(error_by_integration.items(), key=lambda x: x[1]) if error_by_integration else ('none', 0)
        
        return {
            'period_hours': period_hours,
            'total_errors': len(all_errors),
            'error_rate': len(all_errors) / (period_hours * 60),  # errors per minute
            'by_type': dict(error_by_type),
            'by_integration': dict(error_by_integration),
            'by_hour': dict(error_by_hour),
            'patterns': {
                'most_common_error_type': most_common_error[0],
                'most_common_error_count': most_common_error[1],
                'most_problematic_integration': most_problematic_integration[0],
                'most_problematic_integration_errors': most_problematic_integration[1]
            },
            'trend': self._calculate_error_trend(all_errors)
        }
    
    def get_cost_analysis(self, period_hours: int = 24) -> Dict[str, Any]:
        """Analyze cost patterns and optimization opportunities"""
        
        cutoff_time = time.time() - (period_hours * 3600)
        
        cost_by_integration = {}
        total_cost = 0
        
        for integration_name, cost_deque in self.cost_metrics.items():
            integration_costs = [
                cost['cost'] for cost in cost_deque
                if cost['timestamp'] >= cutoff_time
            ]
            
            if integration_costs:
                integration_total = sum(integration_costs)
                cost_by_integration[integration_name] = {
                    'total_cost': integration_total,
                    'average_cost': statistics.mean(integration_costs),
                    'cost_trend': self._calculate_trend(integration_costs[-10:]) if len(integration_costs) >= 10 else 0,
                    'data_points': len(integration_costs)
                }
                total_cost += integration_total
        
        # Find cost optimization opportunities
        high_cost_integrations = sorted(
            cost_by_integration.items(),
            key=lambda x: x[1]['total_cost'],
            reverse=True
        )[:5]
        
        return {
            'period_hours': period_hours,
            'total_cost': total_cost,
            'by_integration': cost_by_integration,
            'optimization': {
                'highest_cost_integrations': high_cost_integrations,
                'cost_per_hour': total_cost / period_hours if period_hours > 0 else 0,
                'projected_monthly_cost': (total_cost / period_hours) * 24 * 30 if period_hours > 0 else 0
            }
        }
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of data"""
        if not data:
            return 0.0
        
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower_index = int(index)
            upper_index = lower_index + 1
            weight = index - lower_index
            return sorted_data[lower_index] * (1 - weight) + sorted_data[upper_index] * weight
    
    def _calculate_trend(self, data: List[float]) -> float:
        """Calculate trend as percentage change"""
        if len(data) < 2:
            return 0.0
        
        # Compare first half with second half
        mid_point = len(data) // 2
        first_half_avg = statistics.mean(data[:mid_point]) if mid_point > 0 else 0
        second_half_avg = statistics.mean(data[mid_point:])
        
        if first_half_avg == 0:
            return 0.0
        
        return ((second_half_avg - first_half_avg) / first_half_avg) * 100
    
    def _calculate_availability(self, health_data: List[Dict]) -> float:
        """Calculate availability percentage"""
        if not health_data:
            return 0.0
        
        healthy_count = sum(1 for record in health_data if record['status'] == 'healthy')
        return (healthy_count / len(health_data)) * 100
    
    def _calculate_reliability_score(self, health_data: List[Dict]) -> float:
        """Calculate reliability score based on multiple factors"""
        if not health_data:
            return 0.0
        
        # Factors: availability, response time consistency, error rate
        availability = self._calculate_availability(health_data)
        
        response_times = [r['response_time'] for r in health_data]
        response_time_consistency = 100 - (statistics.stdev(response_times) / statistics.mean(response_times) * 100) if len(response_times) > 1 else 100
        
        error_rates = [r['error_rate'] for r in health_data]
        avg_error_rate = statistics.mean(error_rates)
        error_score = max(0, 100 - (avg_error_rate * 1000))  # Convert to percentage and invert
        
        # Weighted average
        reliability_score = (availability * 0.5 + response_time_consistency * 0.3 + error_score * 0.2)
        
        return min(100, max(0, reliability_score))
    
    def _calculate_error_trend(self, errors: List[Dict]) -> str:
        """Calculate error trend description"""
        if len(errors) < 10:
            return "insufficient_data"
        
        # Group errors by hour and compare recent vs previous
        hours = {}
        for error in errors:
            hour = int(error['timestamp'] // 3600)
            hours[hour] = hours.get(hour, 0) + 1
        
        if len(hours) < 2:
            return "stable"
        
        sorted_hours = sorted(hours.items())
        mid_point = len(sorted_hours) // 2
        
        recent_avg = statistics.mean([count for _, count in sorted_hours[mid_point:]])
        previous_avg = statistics.mean([count for _, count in sorted_hours[:mid_point]])
        
        if recent_avg > previous_avg * 1.2:
            return "increasing"
        elif recent_avg < previous_avg * 0.8:
            return "decreasing"
        else:
            return "stable"
    
    def _update_collection_stats(self, collection_time: float, success: bool):
        """Update collection statistics"""
        self.collection_stats['total_collections'] += 1
        
        if success:
            # Update average collection time
            total = self.collection_stats['total_collections']
            current_avg = self.collection_stats['average_collection_time']
            self.collection_stats['average_collection_time'] = (current_avg * (total - 1) + collection_time) / total
            self.collection_stats['last_collection_time'] = collection_time
        else:
            self.collection_stats['failed_collections'] += 1
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get metrics collection statistics"""
        total_data_points = sum(len(deque_obj) for deque_obj in self.health_metrics.values())
        total_data_points += len(self.system_metrics)
        
        return {
            **self.collection_stats,
            'total_data_points': total_data_points,
            'integrations_tracked': len(self.health_metrics),
            'cache_hit_rate': 0.0,  # Would calculate from actual cache hits
            'memory_usage': {
                'health_metrics': sum(len(deque_obj) for deque_obj in self.health_metrics.values()),
                'system_metrics': len(self.system_metrics),
                'error_metrics': sum(len(deque_obj) for deque_obj in self.error_metrics.values()),
                'cost_metrics': sum(len(deque_obj) for deque_obj in self.cost_metrics.values())
            }
        }
    
    def clear_old_data(self, hours_to_keep: int = 168):  # 7 days default
        """Clear old data to manage memory usage"""
        cutoff_time = time.time() - (hours_to_keep * 3600)
        removed_count = 0
        
        # Clear old health metrics
        for integration_name in list(self.health_metrics.keys()):
            original_len = len(self.health_metrics[integration_name])
            self.health_metrics[integration_name] = deque(
                [record for record in self.health_metrics[integration_name] if record['timestamp'] >= cutoff_time],
                maxlen=self.health_metrics[integration_name].maxlen
            )
            removed_count += original_len - len(self.health_metrics[integration_name])
        
        # Clear old system metrics
        original_len = len(self.system_metrics)
        self.system_metrics = deque(
            [record for record in self.system_metrics if record['timestamp'] >= cutoff_time],
            maxlen=self.system_metrics.maxlen
        )
        removed_count += original_len - len(self.system_metrics)
        
        # Clear cache
        self.aggregated_cache.clear()
        self.last_cache_update = 0
        
        logger.info(f"Cleared {removed_count} old data points (keeping {hours_to_keep} hours)")
        
        return removed_count