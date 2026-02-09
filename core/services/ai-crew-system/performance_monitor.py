"""
Performance Monitor for BizOSaaS AI Crew System

This module provides comprehensive performance monitoring, metrics collection,
and optimization recommendations for the AI crew system.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import logging
import json
import statistics
from collections import defaultdict, deque

from .crew_orchestrator import TaskResponse, ExecutionStrategy, WorkflowStatus

logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of metrics tracked"""
    EXECUTION_TIME = "execution_time"
    SUCCESS_RATE = "success_rate"
    RESOURCE_USAGE = "resource_usage"
    COST_EFFICIENCY = "cost_efficiency"
    AGENT_UTILIZATION = "agent_utilization"
    STRATEGY_EFFECTIVENESS = "strategy_effectiveness"

class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class PerformanceMetric:
    """Individual performance metric"""
    metric_type: MetricType
    value: float
    timestamp: datetime
    strategy: str
    agent_id: Optional[str] = None
    tenant_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PerformanceAlert:
    """Performance alert"""
    level: AlertLevel
    message: str
    timestamp: datetime
    metric_type: MetricType
    current_value: float
    threshold: float
    affected_components: List[str] = field(default_factory=list)
    suggested_actions: List[str] = field(default_factory=list)

@dataclass
class PerformanceTrend:
    """Performance trend analysis"""
    metric_type: MetricType
    trend_direction: str  # "improving", "degrading", "stable"
    change_percentage: float
    time_period: timedelta
    data_points: int
    confidence: float

class PerformanceThresholds:
    """Performance thresholds for alerting"""
    
    def __init__(self):
        self.thresholds = {
            MetricType.EXECUTION_TIME: {
                AlertLevel.WARNING: 60.0,  # seconds
                AlertLevel.ERROR: 120.0,
                AlertLevel.CRITICAL: 300.0
            },
            MetricType.SUCCESS_RATE: {
                AlertLevel.WARNING: 0.9,  # 90%
                AlertLevel.ERROR: 0.8,    # 80%
                AlertLevel.CRITICAL: 0.7  # 70%
            },
            MetricType.RESOURCE_USAGE: {
                AlertLevel.WARNING: 0.7,  # 70%
                AlertLevel.ERROR: 0.85,   # 85%
                AlertLevel.CRITICAL: 0.95 # 95%
            },
            MetricType.COST_EFFICIENCY: {
                AlertLevel.WARNING: 2.0,  # Cost per successful operation
                AlertLevel.ERROR: 5.0,
                AlertLevel.CRITICAL: 10.0
            }
        }
    
    def get_alert_level(self, metric_type: MetricType, value: float) -> Optional[AlertLevel]:
        """Get alert level for a metric value"""
        thresholds = self.thresholds.get(metric_type, {})
        
        # For success rate, lower values are worse
        if metric_type == MetricType.SUCCESS_RATE:
            for level in [AlertLevel.CRITICAL, AlertLevel.ERROR, AlertLevel.WARNING]:
                if value <= thresholds.get(level, 0):
                    return level
        else:
            # For other metrics, higher values are worse
            for level in [AlertLevel.CRITICAL, AlertLevel.ERROR, AlertLevel.WARNING]:
                if value >= thresholds.get(level, float('inf')):
                    return level
        
        return None

class PerformanceAnalyzer:
    """Analyzes performance data and generates insights"""
    
    def __init__(self):
        self.analysis_window = timedelta(hours=24)  # Default analysis window
    
    def analyze_execution_patterns(
        self, 
        metrics: List[PerformanceMetric]
    ) -> Dict[str, Any]:
        """Analyze execution patterns across strategies"""
        
        strategy_metrics = defaultdict(list)
        
        # Group metrics by strategy
        for metric in metrics:
            if metric.metric_type == MetricType.EXECUTION_TIME:
                strategy_metrics[metric.strategy].append(metric.value)
        
        analysis = {}
        
        for strategy, times in strategy_metrics.items():
            if times:
                analysis[strategy] = {
                    "average_time": statistics.mean(times),
                    "median_time": statistics.median(times),
                    "min_time": min(times),
                    "max_time": max(times),
                    "std_deviation": statistics.stdev(times) if len(times) > 1 else 0,
                    "execution_count": len(times)
                }
        
        return analysis
    
    def analyze_success_patterns(
        self, 
        executions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze success/failure patterns"""
        
        strategy_results = defaultdict(lambda: {"success": 0, "failure": 0})
        
        for execution in executions:
            strategy = execution.get("strategy_used", "unknown")
            status = execution.get("status", "unknown")
            
            if status == "completed":
                strategy_results[strategy]["success"] += 1
            else:
                strategy_results[strategy]["failure"] += 1
        
        analysis = {}
        
        for strategy, results in strategy_results.items():
            total = results["success"] + results["failure"]
            if total > 0:
                analysis[strategy] = {
                    "success_rate": results["success"] / total,
                    "total_executions": total,
                    "success_count": results["success"],
                    "failure_count": results["failure"]
                }
        
        return analysis
    
    def identify_bottlenecks(
        self, 
        metrics: List[PerformanceMetric]
    ) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks"""
        
        bottlenecks = []
        
        # Analyze execution time bottlenecks
        execution_times = [
            m for m in metrics 
            if m.metric_type == MetricType.EXECUTION_TIME
        ]
        
        if execution_times:
            avg_time = statistics.mean([m.value for m in execution_times])
            
            # Find strategies with significantly higher execution times
            strategy_times = defaultdict(list)
            for metric in execution_times:
                strategy_times[metric.strategy].append(metric.value)
            
            for strategy, times in strategy_times.items():
                strategy_avg = statistics.mean(times)
                if strategy_avg > avg_time * 1.5:  # 50% higher than average
                    bottlenecks.append({
                        "type": "execution_time",
                        "strategy": strategy,
                        "average_time": strategy_avg,
                        "global_average": avg_time,
                        "impact": "high",
                        "recommendation": f"Optimize {strategy} strategy execution"
                    })
        
        # Analyze agent utilization bottlenecks
        agent_metrics = [
            m for m in metrics 
            if m.metric_type == MetricType.AGENT_UTILIZATION and m.agent_id
        ]
        
        if agent_metrics:
            agent_usage = defaultdict(list)
            for metric in agent_metrics:
                agent_usage[metric.agent_id].append(metric.value)
            
            for agent_id, usage_values in agent_usage.items():
                avg_usage = statistics.mean(usage_values)
                if avg_usage > 0.8:  # 80% utilization
                    bottlenecks.append({
                        "type": "agent_utilization",
                        "agent_id": agent_id,
                        "utilization": avg_usage,
                        "impact": "medium",
                        "recommendation": f"Scale up agent {agent_id} or distribute load"
                    })
        
        return bottlenecks
    
    def generate_optimization_recommendations(
        self, 
        metrics: List[PerformanceMetric],
        executions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate optimization recommendations"""
        
        recommendations = []
        
        # Analyze execution patterns
        execution_analysis = self.analyze_execution_patterns(metrics)
        success_analysis = self.analyze_success_patterns(executions)
        bottlenecks = self.identify_bottlenecks(metrics)
        
        # Generate strategy-specific recommendations
        for strategy, stats in execution_analysis.items():
            if stats["average_time"] > 60:  # More than 1 minute
                recommendations.append({
                    "category": "performance",
                    "priority": "high",
                    "strategy": strategy,
                    "recommendation": "Consider breaking down complex tasks or optimizing agent selection",
                    "details": f"Average execution time: {stats['average_time']:.1f}s"
                })
        
        # Generate success rate recommendations
        for strategy, stats in success_analysis.items():
            if stats["success_rate"] < 0.9:  # Less than 90% success
                recommendations.append({
                    "category": "reliability",
                    "priority": "high",
                    "strategy": strategy,
                    "recommendation": "Improve error handling and add retry mechanisms",
                    "details": f"Success rate: {stats['success_rate']:.1%}"
                })
        
        # Add bottleneck recommendations
        for bottleneck in bottlenecks:
            recommendations.append({
                "category": "bottleneck",
                "priority": "medium",
                "recommendation": bottleneck["recommendation"],
                "details": f"{bottleneck['type']}: {bottleneck.get('strategy', bottleneck.get('agent_id', 'unknown'))}"
            })
        
        return recommendations

class CrewPerformanceMonitor:
    """Main performance monitoring system"""
    
    def __init__(self, max_metrics=10000):
        self.metrics: deque = deque(maxlen=max_metrics)
        self.alerts: deque = deque(maxlen=1000)
        self.executions: deque = deque(maxlen=5000)
        self.thresholds = PerformanceThresholds()
        self.analyzer = PerformanceAnalyzer()
        self.monitoring_active = True
        
        # Aggregated statistics
        self.hourly_stats = defaultdict(lambda: defaultdict(list))
        self.daily_stats = defaultdict(lambda: defaultdict(list))
    
    async def record_execution(self, response: TaskResponse):
        """Record execution metrics from task response"""
        
        if not self.monitoring_active:
            return
        
        timestamp = datetime.now()
        
        # Record execution details
        execution_record = {
            "task_id": response.task_id,
            "workflow_id": response.workflow_id,
            "strategy_used": response.strategy_used,
            "status": response.status,
            "execution_time": response.execution_time,
            "agents_used": response.agents_used,
            "error": response.error,
            "timestamp": timestamp.isoformat(),
            "metrics": response.metrics
        }
        
        self.executions.append(execution_record)
        
        # Record performance metrics
        await self._record_execution_time_metric(response, timestamp)
        await self._record_success_rate_metric(response, timestamp)
        await self._record_resource_usage_metric(response, timestamp)
        
        # Check for alerts
        await self._check_alerts(response, timestamp)
        
        # Update aggregated statistics
        await self._update_aggregated_stats(response, timestamp)
    
    async def _record_execution_time_metric(
        self, 
        response: TaskResponse, 
        timestamp: datetime
    ):
        """Record execution time metric"""
        
        metric = PerformanceMetric(
            metric_type=MetricType.EXECUTION_TIME,
            value=response.execution_time,
            timestamp=timestamp,
            strategy=response.strategy_used,
            tenant_id=response.metrics.get("tenant_id"),
            metadata={
                "task_id": response.task_id,
                "status": response.status,
                "agents_count": len(response.agents_used)
            }
        )
        
        self.metrics.append(metric)
    
    async def _record_success_rate_metric(
        self, 
        response: TaskResponse, 
        timestamp: datetime
    ):
        """Record success rate metric"""
        
        success_value = 1.0 if response.status == "completed" else 0.0
        
        metric = PerformanceMetric(
            metric_type=MetricType.SUCCESS_RATE,
            value=success_value,
            timestamp=timestamp,
            strategy=response.strategy_used,
            tenant_id=response.metrics.get("tenant_id"),
            metadata={
                "task_id": response.task_id,
                "error": response.error
            }
        )
        
        self.metrics.append(metric)
    
    async def _record_resource_usage_metric(
        self, 
        response: TaskResponse, 
        timestamp: datetime
    ):
        """Record resource usage metric"""
        
        # Calculate resource usage based on agents used and execution time
        base_usage = len(response.agents_used) * 0.1  # Base per agent
        time_factor = min(response.execution_time / 60, 1.0)  # Normalize to 1 minute
        resource_usage = min(base_usage + time_factor, 1.0)
        
        metric = PerformanceMetric(
            metric_type=MetricType.RESOURCE_USAGE,
            value=resource_usage,
            timestamp=timestamp,
            strategy=response.strategy_used,
            tenant_id=response.metrics.get("tenant_id"),
            metadata={
                "agents_used": len(response.agents_used),
                "execution_time": response.execution_time
            }
        )
        
        self.metrics.append(metric)
    
    async def _check_alerts(self, response: TaskResponse, timestamp: datetime):
        """Check for performance alerts"""
        
        # Check execution time alert
        exec_alert_level = self.thresholds.get_alert_level(
            MetricType.EXECUTION_TIME, 
            response.execution_time
        )
        
        if exec_alert_level:
            alert = PerformanceAlert(
                level=exec_alert_level,
                message=f"High execution time detected: {response.execution_time:.1f}s",
                timestamp=timestamp,
                metric_type=MetricType.EXECUTION_TIME,
                current_value=response.execution_time,
                threshold=self.thresholds.thresholds[MetricType.EXECUTION_TIME][exec_alert_level],
                affected_components=[response.strategy_used],
                suggested_actions=[
                    "Review task complexity",
                    "Consider optimizing agent selection",
                    "Check system resources"
                ]
            )
            
            self.alerts.append(alert)
            logger.warning(f"Performance alert: {alert.message}")
        
        # Check for failure alerts
        if response.status != "completed":
            alert = PerformanceAlert(
                level=AlertLevel.ERROR,
                message=f"Task execution failed: {response.error or 'Unknown error'}",
                timestamp=timestamp,
                metric_type=MetricType.SUCCESS_RATE,
                current_value=0.0,
                threshold=1.0,
                affected_components=[response.strategy_used] + response.agents_used,
                suggested_actions=[
                    "Review error logs",
                    "Check agent configuration",
                    "Validate input parameters"
                ]
            )
            
            self.alerts.append(alert)
            logger.error(f"Execution failure alert: {alert.message}")
    
    async def _update_aggregated_stats(
        self, 
        response: TaskResponse, 
        timestamp: datetime
    ):
        """Update hourly and daily aggregated statistics"""
        
        hour_key = timestamp.strftime("%Y-%m-%d-%H")
        day_key = timestamp.strftime("%Y-%m-%d")
        strategy = response.strategy_used
        
        # Hourly stats
        self.hourly_stats[hour_key]["execution_times"].append(response.execution_time)
        self.hourly_stats[hour_key]["strategies"].append(strategy)
        self.hourly_stats[hour_key]["success"].append(response.status == "completed")
        
        # Daily stats
        self.daily_stats[day_key]["execution_times"].append(response.execution_time)
        self.daily_stats[day_key]["strategies"].append(strategy)
        self.daily_stats[day_key]["success"].append(response.status == "completed")
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        
        recent_window = datetime.now() - timedelta(hours=24)
        recent_metrics = [
            m for m in self.metrics 
            if m.timestamp >= recent_window
        ]
        
        recent_executions = [
            e for e in self.executions
            if datetime.fromisoformat(e["timestamp"]) >= recent_window
        ]
        
        # Basic statistics
        total_executions = len(recent_executions)
        successful_executions = len([e for e in recent_executions if e["status"] == "completed"])
        success_rate = successful_executions / total_executions if total_executions > 0 else 0
        
        # Execution time statistics
        execution_times = [e["execution_time"] for e in recent_executions]
        avg_execution_time = statistics.mean(execution_times) if execution_times else 0
        
        # Strategy distribution
        strategy_counts = defaultdict(int)
        for execution in recent_executions:
            strategy_counts[execution["strategy_used"]] += 1
        
        # Agent utilization
        agent_usage = defaultdict(int)
        for execution in recent_executions:
            for agent in execution.get("agents_used", []):
                agent_usage[agent] += 1
        
        # Generate recommendations
        recommendations = self.analyzer.generate_optimization_recommendations(
            recent_metrics, 
            recent_executions
        )
        
        # Recent alerts
        recent_alerts = [
            {
                "level": alert.level.value,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat(),
                "metric_type": alert.metric_type.value
            }
            for alert in list(self.alerts)[-10:]  # Last 10 alerts
        ]
        
        return {
            "summary_period": "24_hours",
            "total_executions": total_executions,
            "success_rate": success_rate,
            "average_execution_time": avg_execution_time,
            "strategy_distribution": dict(strategy_counts),
            "agent_utilization": dict(agent_usage),
            "recent_alerts": recent_alerts,
            "recommendations": recommendations,
            "system_health": self._calculate_system_health(recent_metrics, recent_executions)
        }
    
    def _calculate_system_health(
        self, 
        metrics: List[PerformanceMetric], 
        executions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate overall system health score"""
        
        health_score = 100  # Start with perfect score
        health_factors = []
        
        # Success rate factor
        if executions:
            success_rate = len([e for e in executions if e["status"] == "completed"]) / len(executions)
            if success_rate < 0.95:
                penalty = (0.95 - success_rate) * 50  # Up to 50 point penalty
                health_score -= penalty
                health_factors.append(f"Success rate: {success_rate:.1%}")
        
        # Execution time factor
        execution_times = [e["execution_time"] for e in executions]
        if execution_times:
            avg_time = statistics.mean(execution_times)
            if avg_time > 30:  # More than 30 seconds
                penalty = min((avg_time - 30) / 60 * 20, 30)  # Up to 30 point penalty
                health_score -= penalty
                health_factors.append(f"Average execution time: {avg_time:.1f}s")
        
        # Alert factor
        recent_critical_alerts = len([
            a for a in self.alerts 
            if a.level == AlertLevel.CRITICAL and 
            a.timestamp >= datetime.now() - timedelta(hours=1)
        ])
        
        if recent_critical_alerts > 0:
            penalty = min(recent_critical_alerts * 10, 20)  # Up to 20 point penalty
            health_score -= penalty
            health_factors.append(f"Critical alerts: {recent_critical_alerts}")
        
        health_score = max(0, health_score)  # Don't go below 0
        
        # Determine health status
        if health_score >= 90:
            status = "excellent"
        elif health_score >= 80:
            status = "good"
        elif health_score >= 70:
            status = "fair"
        elif health_score >= 60:
            status = "poor"
        else:
            status = "critical"
        
        return {
            "score": health_score,
            "status": status,
            "factors": health_factors
        }
    
    async def get_detailed_metrics(
        self, 
        metric_type: Optional[MetricType] = None,
        strategy: Optional[str] = None,
        time_range: Optional[timedelta] = None
    ) -> List[Dict[str, Any]]:
        """Get detailed metrics with filtering"""
        
        if time_range is None:
            time_range = timedelta(hours=24)
        
        cutoff_time = datetime.now() - time_range
        
        filtered_metrics = []
        for metric in self.metrics:
            if metric.timestamp < cutoff_time:
                continue
            
            if metric_type and metric.metric_type != metric_type:
                continue
            
            if strategy and metric.strategy != strategy:
                continue
            
            filtered_metrics.append({
                "type": metric.metric_type.value,
                "value": metric.value,
                "timestamp": metric.timestamp.isoformat(),
                "strategy": metric.strategy,
                "agent_id": metric.agent_id,
                "tenant_id": metric.tenant_id,
                "metadata": metric.metadata
            })
        
        return filtered_metrics
    
    async def clear_old_data(self, retention_days: int = 7):
        """Clear old performance data"""
        
        cutoff_time = datetime.now() - timedelta(days=retention_days)
        
        # Clear old metrics
        self.metrics = deque([
            m for m in self.metrics if m.timestamp >= cutoff_time
        ], maxlen=self.metrics.maxlen)
        
        # Clear old executions
        self.executions = deque([
            e for e in self.executions 
            if datetime.fromisoformat(e["timestamp"]) >= cutoff_time
        ], maxlen=self.executions.maxlen)
        
        # Clear old alerts
        self.alerts = deque([
            a for a in self.alerts if a.timestamp >= cutoff_time
        ], maxlen=self.alerts.maxlen)
        
        logger.info(f"Cleared performance data older than {retention_days} days")
    
    def toggle_monitoring(self, active: bool):
        """Enable or disable performance monitoring"""
        self.monitoring_active = active
        logger.info(f"Performance monitoring {'enabled' if active else 'disabled'}")
    
    async def export_metrics(self, format: str = "json") -> str:
        """Export metrics in specified format"""
        
        if format.lower() == "json":
            data = {
                "export_timestamp": datetime.now().isoformat(),
                "metrics": [
                    {
                        "type": m.metric_type.value,
                        "value": m.value,
                        "timestamp": m.timestamp.isoformat(),
                        "strategy": m.strategy,
                        "agent_id": m.agent_id,
                        "tenant_id": m.tenant_id,
                        "metadata": m.metadata
                    }
                    for m in self.metrics
                ],
                "alerts": [
                    {
                        "level": a.level.value,
                        "message": a.message,
                        "timestamp": a.timestamp.isoformat(),
                        "metric_type": a.metric_type.value,
                        "current_value": a.current_value,
                        "threshold": a.threshold
                    }
                    for a in self.alerts
                ]
            }
            return json.dumps(data, indent=2)
        
        raise ValueError(f"Unsupported export format: {format}")

# Global instance
performance_monitor = CrewPerformanceMonitor()