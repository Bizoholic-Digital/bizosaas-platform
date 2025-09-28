"""
AI Agent Execution Monitoring and Performance Analytics

This module provides comprehensive real-time monitoring and analytics for AI agent executions
across the BizOSaaS platform. It integrates with PostHog for user analytics, MLflow for 
agent performance tracking, and Prometheus for system metrics.

Features:
- Real-time agent execution monitoring
- Performance analytics and trend analysis
- Multi-tenant metrics isolation
- Integration with PostHog, MLflow, and Prometheus
- Custom dashboards and alerting
- Success rate tracking and optimization insights
"""

from typing import Dict, List, Optional, Any, Union
from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
import asyncio
import json
import uuid
import time
import statistics
from collections import defaultdict, deque

# Analytics integrations
try:
    import posthog
except ImportError:
    posthog = None

try:
    import mlflow
    import mlflow.tracking
except ImportError:
    mlflow = None

try:
    from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry
except ImportError:
    Counter = Histogram = Gauge = CollectorRegistry = None

# Import AI agents and tenant management
from ai_agents_management import (
    AgentCategory, AgentPriority, AgentStatus,
    get_agent_by_id, get_available_agents_by_category
)
from tenant_middleware import get_current_tenant, TenantContext


class ExecutionStatus(str, Enum):
    """AI Agent execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class PerformanceMetricType(str, Enum):
    """Types of performance metrics"""
    EXECUTION_TIME = "execution_time"
    TOKENS_USED = "tokens_used"
    COST = "cost"
    SUCCESS_RATE = "success_rate"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    LATENCY = "latency"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    QUALITY_SCORE = "quality_score"


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AgentExecutionMetrics:
    """Metrics for a single agent execution"""
    execution_id: str
    tenant_id: str
    agent_id: str
    agent_name: str
    agent_category: AgentCategory
    status: ExecutionStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    tokens_used: Optional[int] = None
    cost_usd: Optional[float] = None
    success: bool = False
    error_message: Optional[str] = None
    quality_score: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    model_used: Optional[str] = None
    temperature: Optional[float] = None
    memory_usage_mb: Optional[float] = None
    cpu_usage_percent: Optional[float] = None
    user_id: Optional[str] = None
    task_type: Optional[str] = None
    fine_tuning_config_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceAnalytics:
    """Performance analytics for agents"""
    tenant_id: str
    agent_id: Optional[str] = None
    agent_category: Optional[AgentCategory] = None
    time_period: str = "24h"
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    success_rate_percent: float = 0.0
    avg_execution_time_seconds: float = 0.0
    avg_tokens_used: float = 0.0
    total_cost_usd: float = 0.0
    avg_quality_score: float = 0.0
    executions_per_hour: float = 0.0
    error_breakdown: Dict[str, int] = field(default_factory=dict)
    performance_trends: List[Dict[str, Any]] = field(default_factory=list)
    top_performing_agents: List[Dict[str, Any]] = field(default_factory=list)
    alerts: List[Dict[str, Any]] = field(default_factory=list)


class AIAgentMonitor:
    """
    Comprehensive AI Agent Monitoring and Analytics System
    
    Provides real-time monitoring, performance analytics, and alerting
    for AI agent executions across the multi-tenant platform.
    """
    
    def __init__(self, vault_client=None, redis_client=None, event_bus_client=None):
        self.vault_client = vault_client
        self.redis_client = redis_client
        self.event_bus_client = event_bus_client
        
        # In-memory storage for real-time metrics (would use Redis/database in production)
        self.active_executions: Dict[str, AgentExecutionMetrics] = {}
        self.execution_history: deque = deque(maxlen=10000)  # Keep last 10k executions
        self.tenant_metrics: Dict[str, Dict[str, Any]] = defaultdict(dict)
        
        # Analytics clients
        self.posthog_client = self._init_posthog()
        self.mlflow_client = self._init_mlflow()
        self.prometheus_metrics = self._init_prometheus()
        
        # Performance thresholds for alerting
        self.performance_thresholds = {
            "max_execution_time": 300.0,  # 5 minutes
            "min_success_rate": 85.0,  # 85%
            "max_error_rate": 15.0,  # 15%
            "max_cost_per_execution": 5.0,  # $5
            "min_quality_score": 0.7  # 70%
        }
    
    def _init_posthog(self):
        """Initialize PostHog client"""
        if posthog:
            # Configure PostHog with environment variables
            posthog.project_api_key = "your-posthog-api-key"
            posthog.host = "http://localhost:8000"  # Self-hosted PostHog
            return posthog
        return None
    
    def _init_mlflow(self):
        """Initialize MLflow client"""
        if mlflow:
            mlflow.set_tracking_uri("http://localhost:5000")  # Self-hosted MLflow
            return mlflow.tracking.MlflowClient()
        return None
    
    def _init_prometheus(self):
        """Initialize Prometheus metrics"""
        if Counter and Histogram and Gauge:
            registry = CollectorRegistry()
            
            metrics = {
                "agent_executions_total": Counter(
                    "ai_agent_executions_total",
                    "Total number of AI agent executions",
                    ["tenant_id", "agent_id", "status"],
                    registry=registry
                ),
                "agent_execution_duration": Histogram(
                    "ai_agent_execution_duration_seconds",
                    "AI agent execution duration",
                    ["tenant_id", "agent_id"],
                    registry=registry
                ),
                "agent_tokens_used": Histogram(
                    "ai_agent_tokens_used_total",
                    "Tokens used by AI agents",
                    ["tenant_id", "agent_id"],
                    registry=registry
                ),
                "agent_cost": Histogram(
                    "ai_agent_cost_usd",
                    "Cost of AI agent executions in USD",
                    ["tenant_id", "agent_id"],
                    registry=registry
                ),
                "agent_success_rate": Gauge(
                    "ai_agent_success_rate_percent",
                    "AI agent success rate percentage",
                    ["tenant_id", "agent_id"],
                    registry=registry
                ),
                "active_executions": Gauge(
                    "ai_agent_active_executions",
                    "Number of currently active AI agent executions",
                    ["tenant_id"],
                    registry=registry
                )
            }
            
            return metrics
        return {}
    
    async def start_execution_monitoring(
        self, 
        tenant_id: str, 
        agent_id: str, 
        task_data: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> str:
        """Start monitoring an AI agent execution"""
        try:
            execution_id = str(uuid.uuid4())
            
            # Get agent details
            agent_details = await get_agent_by_id(agent_id)
            if not agent_details:
                raise ValueError(f"Agent {agent_id} not found")
            
            # Create execution metrics
            metrics = AgentExecutionMetrics(
                execution_id=execution_id,
                tenant_id=tenant_id,
                agent_id=agent_id,
                agent_name=agent_details["name"],
                agent_category=AgentCategory(agent_details["category"]),
                status=ExecutionStatus.PENDING,
                start_time=datetime.now(),
                user_id=user_id,
                task_type=task_data.get("task_type"),
                fine_tuning_config_id=task_data.get("fine_tuning_config_id"),
                metadata={
                    "task_data": task_data,
                    "agent_priority": agent_details.get("priority"),
                    "agent_version": agent_details.get("version", "1.0.0")
                }
            )
            
            # Store active execution
            self.active_executions[execution_id] = metrics
            
            # Update Prometheus metrics
            if self.prometheus_metrics:
                self.prometheus_metrics["agent_executions_total"].labels(
                    tenant_id=tenant_id,
                    agent_id=agent_id,
                    status="started"
                ).inc()
                
                self.prometheus_metrics["active_executions"].labels(
                    tenant_id=tenant_id
                ).inc()
            
            # Track in PostHog
            if self.posthog_client and user_id:
                self.posthog_client.capture(
                    user_id,
                    "ai_agent_execution_started",
                    {
                        "tenant_id": tenant_id,
                        "agent_id": agent_id,
                        "agent_name": agent_details["name"],
                        "agent_category": agent_details["category"],
                        "execution_id": execution_id,
                        "task_type": task_data.get("task_type")
                    }
                )
            
            # Start MLflow run
            if self.mlflow_client:
                try:
                    experiment_name = f"ai_agents_{tenant_id}"
                    
                    # Create experiment if it doesn't exist
                    try:
                        experiment = mlflow.get_experiment_by_name(experiment_name)
                        if experiment is None:
                            experiment_id = mlflow.create_experiment(experiment_name)
                        else:
                            experiment_id = experiment.experiment_id
                    except Exception:
                        experiment_id = mlflow.create_experiment(experiment_name)
                    
                    # Start MLflow run
                    run = mlflow.start_run(
                        experiment_id=experiment_id,
                        run_name=f"{agent_id}_{execution_id[:8]}"
                    )
                    
                    # Log parameters
                    mlflow.log_params({
                        "agent_id": agent_id,
                        "agent_name": agent_details["name"],
                        "agent_category": agent_details["category"],
                        "tenant_id": tenant_id,
                        "task_type": task_data.get("task_type", "unknown")
                    })
                    
                    metrics.metadata["mlflow_run_id"] = run.info.run_id
                    
                except Exception as e:
                    print(f"MLflow logging failed: {e}")
            
            return execution_id
            
        except Exception as e:
            raise Exception(f"Failed to start execution monitoring: {str(e)}")
    
    async def update_execution_status(
        self, 
        execution_id: str, 
        status: ExecutionStatus,
        additional_metrics: Optional[Dict[str, Any]] = None
    ):
        """Update execution status and metrics"""
        try:
            if execution_id not in self.active_executions:
                raise ValueError(f"Execution {execution_id} not found")
            
            metrics = self.active_executions[execution_id]
            metrics.status = status
            
            # Update additional metrics if provided
            if additional_metrics:
                for key, value in additional_metrics.items():
                    if hasattr(metrics, key):
                        setattr(metrics, key, value)
            
            # If execution is running, record start time
            if status == ExecutionStatus.RUNNING:
                metrics.start_time = datetime.now()
            
            # Update Prometheus metrics
            if self.prometheus_metrics:
                self.prometheus_metrics["agent_executions_total"].labels(
                    tenant_id=metrics.tenant_id,
                    agent_id=metrics.agent_id,
                    status=status.value
                ).inc()
            
        except Exception as e:
            raise Exception(f"Failed to update execution status: {str(e)}")
    
    async def complete_execution_monitoring(
        self, 
        execution_id: str, 
        success: bool,
        result_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ) -> AgentExecutionMetrics:
        """Complete execution monitoring and calculate final metrics"""
        try:
            if execution_id not in self.active_executions:
                raise ValueError(f"Execution {execution_id} not found")
            
            metrics = self.active_executions[execution_id]
            metrics.end_time = datetime.now()
            metrics.success = success
            metrics.error_message = error_message
            
            # Calculate duration
            if metrics.start_time:
                metrics.duration_seconds = (metrics.end_time - metrics.start_time).total_seconds()
            
            # Set final status
            metrics.status = ExecutionStatus.COMPLETED if success else ExecutionStatus.FAILED
            
            # Update metrics from result data
            if result_data:
                metrics.tokens_used = result_data.get("tokens_used")
                metrics.input_tokens = result_data.get("input_tokens")
                metrics.output_tokens = result_data.get("output_tokens")
                metrics.cost_usd = result_data.get("cost_usd")
                metrics.quality_score = result_data.get("quality_score")
                metrics.model_used = result_data.get("model_used")
                metrics.memory_usage_mb = result_data.get("memory_usage_mb")
                metrics.cpu_usage_percent = result_data.get("cpu_usage_percent")
            
            # Update Prometheus metrics
            if self.prometheus_metrics:
                # Record final metrics
                if metrics.duration_seconds:
                    self.prometheus_metrics["agent_execution_duration"].labels(
                        tenant_id=metrics.tenant_id,
                        agent_id=metrics.agent_id
                    ).observe(metrics.duration_seconds)
                
                if metrics.tokens_used:
                    self.prometheus_metrics["agent_tokens_used"].labels(
                        tenant_id=metrics.tenant_id,
                        agent_id=metrics.agent_id
                    ).observe(metrics.tokens_used)
                
                if metrics.cost_usd:
                    self.prometheus_metrics["agent_cost"].labels(
                        tenant_id=metrics.tenant_id,
                        agent_id=metrics.agent_id
                    ).observe(metrics.cost_usd)
                
                # Decrease active executions count
                self.prometheus_metrics["active_executions"].labels(
                    tenant_id=metrics.tenant_id
                ).dec()
            
            # Complete MLflow run
            if self.mlflow_client and "mlflow_run_id" in metrics.metadata:
                try:
                    with mlflow.start_run(run_id=metrics.metadata["mlflow_run_id"]):
                        # Log final metrics
                        if metrics.duration_seconds:
                            mlflow.log_metric("execution_time", metrics.duration_seconds)
                        if metrics.tokens_used:
                            mlflow.log_metric("tokens_used", metrics.tokens_used)
                        if metrics.cost_usd:
                            mlflow.log_metric("cost_usd", metrics.cost_usd)
                        if metrics.quality_score:
                            mlflow.log_metric("quality_score", metrics.quality_score)
                        
                        mlflow.log_metric("success", 1 if success else 0)
                        
                        # Log artifacts if available
                        if result_data and "output" in result_data:
                            mlflow.log_text(str(result_data["output"]), "agent_output.txt")
                        
                        if error_message:
                            mlflow.log_text(error_message, "error.txt")
                
                except Exception as e:
                    print(f"MLflow completion failed: {e}")
            
            # Track completion in PostHog
            if self.posthog_client and metrics.user_id:
                self.posthog_client.capture(
                    metrics.user_id,
                    "ai_agent_execution_completed",
                    {
                        "tenant_id": metrics.tenant_id,
                        "agent_id": metrics.agent_id,
                        "agent_name": metrics.agent_name,
                        "execution_id": execution_id,
                        "success": success,
                        "duration_seconds": metrics.duration_seconds,
                        "tokens_used": metrics.tokens_used,
                        "cost_usd": metrics.cost_usd,
                        "quality_score": metrics.quality_score
                    }
                )
            
            # Move to history and remove from active
            self.execution_history.append(metrics)
            del self.active_executions[execution_id]
            
            # Update tenant metrics
            await self._update_tenant_metrics(metrics)
            
            # Check for alerts
            await self._check_performance_alerts(metrics)
            
            return metrics
            
        except Exception as e:
            raise Exception(f"Failed to complete execution monitoring: {str(e)}")
    
    async def get_real_time_metrics(self, tenant_id: str) -> Dict[str, Any]:
        """Get real-time metrics for a tenant"""
        try:
            # Get active executions for tenant
            active_tenant_executions = [
                metrics for metrics in self.active_executions.values()
                if metrics.tenant_id == tenant_id
            ]
            
            # Get recent history (last 24 hours)
            recent_history = [
                metrics for metrics in self.execution_history
                if metrics.tenant_id == tenant_id and 
                metrics.end_time and 
                metrics.end_time > datetime.now() - timedelta(hours=24)
            ]
            
            # Calculate metrics
            total_executions = len(recent_history)
            successful_executions = len([m for m in recent_history if m.success])
            failed_executions = total_executions - successful_executions
            success_rate = (successful_executions / max(total_executions, 1)) * 100
            
            # Average metrics
            avg_duration = statistics.mean([
                m.duration_seconds for m in recent_history 
                if m.duration_seconds
            ]) if recent_history else 0
            
            avg_tokens = statistics.mean([
                m.tokens_used for m in recent_history 
                if m.tokens_used
            ]) if recent_history else 0
            
            total_cost = sum([
                m.cost_usd for m in recent_history 
                if m.cost_usd
            ])
            
            # Agent breakdown
            agent_stats = defaultdict(lambda: {"executions": 0, "success": 0, "avg_duration": 0})
            for metrics in recent_history:
                agent_stats[metrics.agent_id]["executions"] += 1
                if metrics.success:
                    agent_stats[metrics.agent_id]["success"] += 1
                if metrics.duration_seconds:
                    agent_stats[metrics.agent_id]["avg_duration"] = (
                        agent_stats[metrics.agent_id].get("avg_duration", 0) + metrics.duration_seconds
                    ) / agent_stats[metrics.agent_id]["executions"]
            
            return {
                "tenant_id": tenant_id,
                "timestamp": datetime.now().isoformat(),
                "active_executions": len(active_tenant_executions),
                "recent_24h": {
                    "total_executions": total_executions,
                    "successful_executions": successful_executions,
                    "failed_executions": failed_executions,
                    "success_rate_percent": round(success_rate, 2),
                    "avg_execution_time_seconds": round(avg_duration, 2),
                    "avg_tokens_used": round(avg_tokens, 2),
                    "total_cost_usd": round(total_cost, 4),
                    "executions_per_hour": round(total_executions / 24, 2)
                },
                "agent_breakdown": dict(agent_stats),
                "active_executions_details": [
                    {
                        "execution_id": m.execution_id,
                        "agent_id": m.agent_id,
                        "agent_name": m.agent_name,
                        "status": m.status.value,
                        "start_time": m.start_time.isoformat(),
                        "duration_so_far": (datetime.now() - m.start_time).total_seconds()
                    }
                    for m in active_tenant_executions
                ]
            }
            
        except Exception as e:
            raise Exception(f"Failed to get real-time metrics: {str(e)}")
    
    async def get_performance_analytics(
        self, 
        tenant_id: str,
        time_period: str = "24h",
        agent_id: Optional[str] = None
    ) -> PerformanceAnalytics:
        """Get comprehensive performance analytics"""
        try:
            # Parse time period
            if time_period == "1h":
                start_time = datetime.now() - timedelta(hours=1)
            elif time_period == "24h":
                start_time = datetime.now() - timedelta(hours=24)
            elif time_period == "7d":
                start_time = datetime.now() - timedelta(days=7)
            elif time_period == "30d":
                start_time = datetime.now() - timedelta(days=30)
            else:
                start_time = datetime.now() - timedelta(hours=24)
            
            # Filter executions
            filtered_executions = [
                metrics for metrics in self.execution_history
                if metrics.tenant_id == tenant_id and 
                metrics.end_time and 
                metrics.end_time > start_time and
                (not agent_id or metrics.agent_id == agent_id)
            ]
            
            if not filtered_executions:
                return PerformanceAnalytics(
                    tenant_id=tenant_id,
                    agent_id=agent_id,
                    time_period=time_period
                )
            
            # Calculate analytics
            total_executions = len(filtered_executions)
            successful_executions = len([m for m in filtered_executions if m.success])
            failed_executions = total_executions - successful_executions
            success_rate = (successful_executions / total_executions) * 100
            
            # Average metrics
            durations = [m.duration_seconds for m in filtered_executions if m.duration_seconds]
            avg_execution_time = statistics.mean(durations) if durations else 0
            
            tokens = [m.tokens_used for m in filtered_executions if m.tokens_used]
            avg_tokens_used = statistics.mean(tokens) if tokens else 0
            
            costs = [m.cost_usd for m in filtered_executions if m.cost_usd]
            total_cost = sum(costs) if costs else 0
            
            quality_scores = [m.quality_score for m in filtered_executions if m.quality_score]
            avg_quality_score = statistics.mean(quality_scores) if quality_scores else 0
            
            # Calculate executions per hour
            time_diff = (datetime.now() - start_time).total_seconds() / 3600
            executions_per_hour = total_executions / time_diff if time_diff > 0 else 0
            
            # Error breakdown
            error_breakdown = defaultdict(int)
            for metrics in filtered_executions:
                if not metrics.success and metrics.error_message:
                    error_type = metrics.error_message.split(":")[0] if ":" in metrics.error_message else "Unknown"
                    error_breakdown[error_type] += 1
            
            # Performance trends (hourly buckets)
            performance_trends = self._calculate_performance_trends(filtered_executions, start_time)
            
            # Top performing agents
            top_performing_agents = self._calculate_top_performing_agents(filtered_executions)
            
            # Generate alerts
            alerts = self._generate_performance_alerts(
                success_rate, avg_execution_time, total_cost / max(total_executions, 1), avg_quality_score
            )
            
            return PerformanceAnalytics(
                tenant_id=tenant_id,
                agent_id=agent_id,
                time_period=time_period,
                total_executions=total_executions,
                successful_executions=successful_executions,
                failed_executions=failed_executions,
                success_rate_percent=round(success_rate, 2),
                avg_execution_time_seconds=round(avg_execution_time, 2),
                avg_tokens_used=round(avg_tokens_used, 2),
                total_cost_usd=round(total_cost, 4),
                avg_quality_score=round(avg_quality_score, 2),
                executions_per_hour=round(executions_per_hour, 2),
                error_breakdown=dict(error_breakdown),
                performance_trends=performance_trends,
                top_performing_agents=top_performing_agents,
                alerts=alerts
            )
            
        except Exception as e:
            raise Exception(f"Failed to get performance analytics: {str(e)}")
    
    def _calculate_performance_trends(self, executions: List[AgentExecutionMetrics], start_time: datetime) -> List[Dict[str, Any]]:
        """Calculate hourly performance trends"""
        trends = []
        current_time = start_time
        
        while current_time < datetime.now():
            hour_end = current_time + timedelta(hours=1)
            hour_executions = [
                m for m in executions 
                if m.end_time and current_time <= m.end_time < hour_end
            ]
            
            if hour_executions:
                successful = len([m for m in hour_executions if m.success])
                total = len(hour_executions)
                success_rate = (successful / total) * 100
                avg_duration = statistics.mean([
                    m.duration_seconds for m in hour_executions 
                    if m.duration_seconds
                ]) if hour_executions else 0
            else:
                success_rate = 0
                avg_duration = 0
                total = 0
            
            trends.append({
                "timestamp": current_time.isoformat(),
                "executions": total,
                "success_rate": round(success_rate, 2),
                "avg_duration": round(avg_duration, 2)
            })
            
            current_time = hour_end
        
        return trends
    
    def _calculate_top_performing_agents(self, executions: List[AgentExecutionMetrics]) -> List[Dict[str, Any]]:
        """Calculate top performing agents"""
        agent_stats = defaultdict(lambda: {
            "executions": 0, "success": 0, "total_duration": 0, 
            "total_tokens": 0, "total_cost": 0, "quality_scores": []
        })
        
        for metrics in executions:
            stats = agent_stats[metrics.agent_id]
            stats["executions"] += 1
            stats["agent_name"] = metrics.agent_name
            stats["agent_category"] = metrics.agent_category.value
            
            if metrics.success:
                stats["success"] += 1
            if metrics.duration_seconds:
                stats["total_duration"] += metrics.duration_seconds
            if metrics.tokens_used:
                stats["total_tokens"] += metrics.tokens_used
            if metrics.cost_usd:
                stats["total_cost"] += metrics.cost_usd
            if metrics.quality_score:
                stats["quality_scores"].append(metrics.quality_score)
        
        # Calculate averages and rankings
        ranked_agents = []
        for agent_id, stats in agent_stats.items():
            success_rate = (stats["success"] / stats["executions"]) * 100
            avg_duration = stats["total_duration"] / stats["executions"]
            avg_quality = statistics.mean(stats["quality_scores"]) if stats["quality_scores"] else 0
            
            ranked_agents.append({
                "agent_id": agent_id,
                "agent_name": stats["agent_name"],
                "agent_category": stats["agent_category"],
                "executions": stats["executions"],
                "success_rate": round(success_rate, 2),
                "avg_duration": round(avg_duration, 2),
                "avg_quality_score": round(avg_quality, 2),
                "total_cost": round(stats["total_cost"], 4),
                "performance_score": round((success_rate + avg_quality * 100) / 2, 2)
            })
        
        # Sort by performance score
        return sorted(ranked_agents, key=lambda x: x["performance_score"], reverse=True)[:10]
    
    def _generate_performance_alerts(
        self, success_rate: float, avg_duration: float, avg_cost: float, avg_quality: float
    ) -> List[Dict[str, Any]]:
        """Generate performance alerts based on thresholds"""
        alerts = []
        
        if success_rate < self.performance_thresholds["min_success_rate"]:
            alerts.append({
                "type": "success_rate_low",
                "severity": AlertSeverity.HIGH.value,
                "message": f"Success rate ({success_rate:.1f}%) is below threshold ({self.performance_thresholds['min_success_rate']}%)",
                "value": success_rate,
                "threshold": self.performance_thresholds["min_success_rate"]
            })
        
        if avg_duration > self.performance_thresholds["max_execution_time"]:
            alerts.append({
                "type": "execution_time_high",
                "severity": AlertSeverity.MEDIUM.value,
                "message": f"Average execution time ({avg_duration:.1f}s) is above threshold ({self.performance_thresholds['max_execution_time']}s)",
                "value": avg_duration,
                "threshold": self.performance_thresholds["max_execution_time"]
            })
        
        if avg_cost > self.performance_thresholds["max_cost_per_execution"]:
            alerts.append({
                "type": "cost_high",
                "severity": AlertSeverity.MEDIUM.value,
                "message": f"Average cost per execution (${avg_cost:.2f}) is above threshold (${self.performance_thresholds['max_cost_per_execution']})",
                "value": avg_cost,
                "threshold": self.performance_thresholds["max_cost_per_execution"]
            })
        
        if avg_quality < self.performance_thresholds["min_quality_score"]:
            alerts.append({
                "type": "quality_score_low",
                "severity": AlertSeverity.HIGH.value,
                "message": f"Average quality score ({avg_quality:.2f}) is below threshold ({self.performance_thresholds['min_quality_score']})",
                "value": avg_quality,
                "threshold": self.performance_thresholds["min_quality_score"]
            })
        
        return alerts
    
    async def _update_tenant_metrics(self, metrics: AgentExecutionMetrics):
        """Update aggregated tenant metrics"""
        tenant_id = metrics.tenant_id
        
        if tenant_id not in self.tenant_metrics:
            self.tenant_metrics[tenant_id] = {
                "total_executions": 0,
                "successful_executions": 0,
                "total_duration": 0,
                "total_tokens": 0,
                "total_cost": 0,
                "agent_usage": defaultdict(int)
            }
        
        tenant_stats = self.tenant_metrics[tenant_id]
        tenant_stats["total_executions"] += 1
        
        if metrics.success:
            tenant_stats["successful_executions"] += 1
        
        if metrics.duration_seconds:
            tenant_stats["total_duration"] += metrics.duration_seconds
        
        if metrics.tokens_used:
            tenant_stats["total_tokens"] += metrics.tokens_used
        
        if metrics.cost_usd:
            tenant_stats["total_cost"] += metrics.cost_usd
        
        tenant_stats["agent_usage"][metrics.agent_id] += 1
        
        # Update Prometheus success rate gauge
        if self.prometheus_metrics:
            success_rate = (tenant_stats["successful_executions"] / tenant_stats["total_executions"]) * 100
            self.prometheus_metrics["agent_success_rate"].labels(
                tenant_id=tenant_id,
                agent_id=metrics.agent_id
            ).set(success_rate)
    
    async def _check_performance_alerts(self, metrics: AgentExecutionMetrics):
        """Check if execution triggers any performance alerts"""
        alerts = []
        
        # Check execution time
        if metrics.duration_seconds and metrics.duration_seconds > self.performance_thresholds["max_execution_time"]:
            alerts.append({
                "type": "execution_timeout",
                "severity": AlertSeverity.HIGH.value,
                "execution_id": metrics.execution_id,
                "agent_id": metrics.agent_id,
                "value": metrics.duration_seconds
            })
        
        # Check cost
        if metrics.cost_usd and metrics.cost_usd > self.performance_thresholds["max_cost_per_execution"]:
            alerts.append({
                "type": "high_cost",
                "severity": AlertSeverity.MEDIUM.value,
                "execution_id": metrics.execution_id,
                "agent_id": metrics.agent_id,
                "value": metrics.cost_usd
            })
        
        # Check quality score
        if metrics.quality_score and metrics.quality_score < self.performance_thresholds["min_quality_score"]:
            alerts.append({
                "type": "low_quality",
                "severity": AlertSeverity.HIGH.value,
                "execution_id": metrics.execution_id,
                "agent_id": metrics.agent_id,
                "value": metrics.quality_score
            })
        
        # Store alerts (in production, would send to alerting system)
        for alert in alerts:
            print(f"ALERT: {alert}")


# Global monitor instance
ai_agent_monitor = AIAgentMonitor()

# API helper functions
async def start_agent_execution_monitoring(
    tenant_id: str, agent_id: str, task_data: Dict[str, Any], user_id: Optional[str] = None
) -> str:
    """Start monitoring an AI agent execution"""
    return await ai_agent_monitor.start_execution_monitoring(tenant_id, agent_id, task_data, user_id)

async def update_agent_execution_status(
    execution_id: str, status: ExecutionStatus, additional_metrics: Optional[Dict[str, Any]] = None
):
    """Update execution status and metrics"""
    return await ai_agent_monitor.update_execution_status(execution_id, status, additional_metrics)

async def complete_agent_execution_monitoring(
    execution_id: str, success: bool, result_data: Optional[Dict[str, Any]] = None, error_message: Optional[str] = None
) -> AgentExecutionMetrics:
    """Complete execution monitoring"""
    return await ai_agent_monitor.complete_execution_monitoring(execution_id, success, result_data, error_message)

async def get_tenant_real_time_metrics(tenant_id: str) -> Dict[str, Any]:
    """Get real-time metrics for tenant"""
    return await ai_agent_monitor.get_real_time_metrics(tenant_id)

async def get_tenant_performance_analytics(
    tenant_id: str, time_period: str = "24h", agent_id: Optional[str] = None
) -> PerformanceAnalytics:
    """Get performance analytics for tenant"""
    return await ai_agent_monitor.get_performance_analytics(tenant_id, time_period, agent_id)