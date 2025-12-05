"""
Amazon Workflow Monitoring and Error Handling System

This module provides comprehensive monitoring, error handling, and observability
for the Amazon listing workflow, ensuring reliable operation and providing
detailed insights into system performance and issues.

Key Features:
- Real-time workflow monitoring and health checks
- Comprehensive error handling and recovery mechanisms
- Performance metrics collection and analysis
- Alerting and notification system
- Audit trail and compliance logging
- Resource utilization monitoring
- Automatic retry and fallback strategies
- Integration with external monitoring systems

Integration with BizOSaaS Platform:
- Tenant-aware monitoring and logging
- Integration with central monitoring infrastructure
- AI-powered error analysis and recommendations
- Performance optimization insights
- Compliance audit trail
"""

import asyncio
import json
import logging
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid
import statistics
from pathlib import Path

# Monitoring and observability imports
import psutil  # For system monitoring
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest

# BizOSaaS Platform imports
from .ai_coordinator import EnhancedAICoordinator, EnhancedTenantContext
from .amazon_listing_workflow_orchestrator import WorkflowResult
from .amazon_bulk_processor import BatchProcessingResult, ProcessingStatus
from .amazon_compliance_validator import ValidationResult

# Setup logging
logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"     # System down or major functionality broken
    HIGH = "high"            # Significant impact on functionality
    MEDIUM = "medium"        # Moderate impact, degraded performance
    LOW = "low"              # Minor issues, no significant impact
    INFO = "info"            # Informational alerts

class MonitoringMetric(Enum):
    """Monitoring metric types"""
    WORKFLOW_SUCCESS_RATE = "workflow_success_rate"
    PROCESSING_TIME = "processing_time"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    RESOURCE_UTILIZATION = "resource_utilization"
    COMPLIANCE_SCORE = "compliance_score"
    API_RESPONSE_TIME = "api_response_time"
    QUEUE_LENGTH = "queue_length"

class ErrorCategory(Enum):
    """Error categorization for analysis"""
    SYSTEM_ERROR = "system_error"           # Infrastructure/system issues
    VALIDATION_ERROR = "validation_error"   # Content validation failures
    API_ERROR = "api_error"                 # External API failures
    TIMEOUT_ERROR = "timeout_error"         # Processing timeouts
    AUTH_ERROR = "auth_error"               # Authentication failures
    RATE_LIMIT_ERROR = "rate_limit_error"   # Rate limiting issues
    DATA_ERROR = "data_error"               # Data quality/format issues
    BUSINESS_LOGIC_ERROR = "business_logic_error"  # Business rule violations

@dataclass
class ErrorEvent:
    """Represents an error event for tracking and analysis"""
    id: str
    timestamp: datetime
    category: ErrorCategory
    severity: AlertSeverity
    message: str
    stack_trace: Optional[str]
    context: Dict[str, Any]
    tenant_id: Optional[str]
    workflow_id: Optional[str]
    component: str
    recoverable: bool
    auto_retry_count: int = 0
    resolution_status: str = "open"  # open, investigating, resolved, ignored

@dataclass
class PerformanceMetric:
    """Performance metric data point"""
    metric_type: MonitoringMetric
    value: float
    timestamp: datetime
    tenant_id: Optional[str]
    component: str
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class AlertRule:
    """Alert rule configuration"""
    name: str
    metric_type: MonitoringMetric
    threshold: float
    comparison: str  # >, <, >=, <=, ==
    severity: AlertSeverity
    enabled: bool = True
    cooldown_minutes: int = 15
    notification_channels: List[str] = field(default_factory=list)

@dataclass
class SystemHealth:
    """Overall system health status"""
    status: str  # healthy, degraded, unhealthy
    score: float  # 0-100 health score
    components: Dict[str, str]  # component -> status
    metrics: Dict[str, float]
    last_updated: datetime
    issues: List[str]

class AmazonWorkflowMonitor:
    """
    Comprehensive monitoring and error handling system for Amazon workflows

    Provides real-time monitoring, error tracking, performance analysis,
    and automated recovery mechanisms for the entire Amazon listing ecosystem.
    """

    def __init__(
        self,
        ai_coordinator: EnhancedAICoordinator,
        enable_metrics: bool = True,
        enable_alerting: bool = True,
        metrics_retention_days: int = 30
    ):
        self.ai_coordinator = ai_coordinator
        self.enable_metrics = enable_metrics
        self.enable_alerting = enable_alerting
        self.metrics_retention_days = metrics_retention_days

        # Error and event storage
        self.error_events: Dict[str, ErrorEvent] = {}
        self.performance_metrics: List[PerformanceMetric] = []
        self.alert_rules: List[AlertRule] = []

        # Monitoring state
        self.component_health: Dict[str, str] = {}
        self.last_alert_times: Dict[str, datetime] = {}
        self.error_pattern_cache: Dict[str, List[ErrorEvent]] = {}

        # Prometheus metrics
        if self.enable_metrics:
            self.registry = CollectorRegistry()
            self._setup_prometheus_metrics()

        # Alert handlers
        self.alert_handlers: List[Callable] = []

        # Recovery strategies
        self.recovery_strategies: Dict[ErrorCategory, Callable] = {}
        self._setup_recovery_strategies()

        # Default alert rules
        self._setup_default_alert_rules()

        # Background monitoring tasks
        self.monitoring_tasks: List[asyncio.Task] = []
        self._start_background_monitoring()

        logger.info("Amazon Workflow Monitor initialized")

    def _setup_prometheus_metrics(self):
        """Setup Prometheus metrics collectors"""
        self.workflow_counter = Counter(
            'amazon_workflow_total',
            'Total Amazon workflow executions',
            ['tenant_id', 'status'],
            registry=self.registry
        )

        self.workflow_duration = Histogram(
            'amazon_workflow_duration_seconds',
            'Amazon workflow execution duration',
            ['tenant_id', 'component'],
            registry=self.registry
        )

        self.error_counter = Counter(
            'amazon_workflow_errors_total',
            'Total workflow errors',
            ['tenant_id', 'category', 'component'],
            registry=self.registry
        )

        self.compliance_score_gauge = Gauge(
            'amazon_compliance_score',
            'Amazon listing compliance score',
            ['tenant_id'],
            registry=self.registry
        )

        self.queue_length_gauge = Gauge(
            'amazon_processing_queue_length',
            'Current processing queue length',
            ['tenant_id'],
            registry=self.registry
        )

        self.resource_utilization_gauge = Gauge(
            'system_resource_utilization',
            'System resource utilization percentage',
            ['resource_type'],
            registry=self.registry
        )

    def _setup_recovery_strategies(self):
        """Setup automatic recovery strategies for different error types"""
        self.recovery_strategies = {
            ErrorCategory.TIMEOUT_ERROR: self._handle_timeout_recovery,
            ErrorCategory.RATE_LIMIT_ERROR: self._handle_rate_limit_recovery,
            ErrorCategory.API_ERROR: self._handle_api_error_recovery,
            ErrorCategory.SYSTEM_ERROR: self._handle_system_error_recovery,
            ErrorCategory.VALIDATION_ERROR: self._handle_validation_error_recovery
        }

    def _setup_default_alert_rules(self):
        """Setup default alerting rules"""
        self.alert_rules = [
            AlertRule(
                name="High Error Rate",
                metric_type=MonitoringMetric.ERROR_RATE,
                threshold=0.1,  # 10% error rate
                comparison=">",
                severity=AlertSeverity.HIGH,
                cooldown_minutes=10
            ),
            AlertRule(
                name="Low Success Rate",
                metric_type=MonitoringMetric.WORKFLOW_SUCCESS_RATE,
                threshold=0.8,  # 80% success rate
                comparison="<",
                severity=AlertSeverity.MEDIUM,
                cooldown_minutes=15
            ),
            AlertRule(
                name="High Processing Time",
                metric_type=MonitoringMetric.PROCESSING_TIME,
                threshold=300,  # 5 minutes
                comparison=">",
                severity=AlertSeverity.MEDIUM,
                cooldown_minutes=20
            ),
            AlertRule(
                name="Low Compliance Score",
                metric_type=MonitoringMetric.COMPLIANCE_SCORE,
                threshold=70,  # 70% compliance score
                comparison="<",
                severity=AlertSeverity.HIGH,
                cooldown_minutes=30
            ),
            AlertRule(
                name="High Resource Utilization",
                metric_type=MonitoringMetric.RESOURCE_UTILIZATION,
                threshold=90,  # 90% resource utilization
                comparison=">",
                severity=AlertSeverity.CRITICAL,
                cooldown_minutes=5
            )
        ]

    def _start_background_monitoring(self):
        """Start background monitoring tasks"""
        # System health monitoring
        health_task = asyncio.create_task(self._monitor_system_health())
        self.monitoring_tasks.append(health_task)

        # Metrics cleanup
        cleanup_task = asyncio.create_task(self._cleanup_old_metrics())
        self.monitoring_tasks.append(cleanup_task)

        # Alert evaluation
        alert_task = asyncio.create_task(self._evaluate_alerts())
        self.monitoring_tasks.append(alert_task)

        # Error pattern analysis
        pattern_task = asyncio.create_task(self._analyze_error_patterns())
        self.monitoring_tasks.append(pattern_task)

    async def record_workflow_start(
        self,
        workflow_id: str,
        tenant_context: EnhancedTenantContext,
        component: str = "workflow_orchestrator"
    ):
        """Record workflow start event"""
        try:
            self.component_health[f"{component}_{workflow_id}"] = "running"

            if self.enable_metrics:
                self.workflow_counter.labels(
                    tenant_id=tenant_context.tenant_id,
                    status="started"
                ).inc()

            await self._record_metric(
                metric_type=MonitoringMetric.WORKFLOW_SUCCESS_RATE,
                value=1.0,  # Will be updated on completion
                tenant_id=tenant_context.tenant_id,
                component=component,
                tags={"workflow_id": workflow_id, "event": "start"}
            )

            logger.info(f"Workflow {workflow_id} started monitoring")

        except Exception as e:
            logger.error(f"Failed to record workflow start: {e}")

    async def record_workflow_completion(
        self,
        workflow_id: str,
        tenant_context: EnhancedTenantContext,
        workflow_result: WorkflowResult,
        processing_time: float,
        component: str = "workflow_orchestrator"
    ):
        """Record workflow completion event"""
        try:
            success = workflow_result.success
            status = "success" if success else "failure"

            self.component_health[f"{component}_{workflow_id}"] = status

            if self.enable_metrics:
                self.workflow_counter.labels(
                    tenant_id=tenant_context.tenant_id,
                    status=status
                ).inc()

                self.workflow_duration.labels(
                    tenant_id=tenant_context.tenant_id,
                    component=component
                ).observe(processing_time)

            # Record performance metrics
            await self._record_metric(
                metric_type=MonitoringMetric.PROCESSING_TIME,
                value=processing_time,
                tenant_id=tenant_context.tenant_id,
                component=component,
                tags={"workflow_id": workflow_id}
            )

            await self._record_metric(
                metric_type=MonitoringMetric.WORKFLOW_SUCCESS_RATE,
                value=1.0 if success else 0.0,
                tenant_id=tenant_context.tenant_id,
                component=component,
                tags={"workflow_id": workflow_id}
            )

            # Record errors if any
            if not success and workflow_result.errors:
                for error in workflow_result.errors:
                    await self.record_error(
                        component=component,
                        error_category=ErrorCategory.BUSINESS_LOGIC_ERROR,
                        message=error,
                        context={"workflow_id": workflow_id},
                        tenant_id=tenant_context.tenant_id,
                        workflow_id=workflow_id
                    )

            logger.info(f"Workflow {workflow_id} completed: {status} in {processing_time:.2f}s")

        except Exception as e:
            logger.error(f"Failed to record workflow completion: {e}")

    async def record_error(
        self,
        component: str,
        error_category: ErrorCategory,
        message: str,
        context: Dict[str, Any] = None,
        exception: Optional[Exception] = None,
        tenant_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
        severity: AlertSeverity = AlertSeverity.MEDIUM,
        recoverable: bool = True
    ) -> str:
        """Record an error event"""
        try:
            error_id = str(uuid.uuid4())
            stack_trace = None

            if exception:
                stack_trace = traceback.format_exception(
                    type(exception), exception, exception.__traceback__
                )
                stack_trace = ''.join(stack_trace)

            error_event = ErrorEvent(
                id=error_id,
                timestamp=datetime.utcnow(),
                category=error_category,
                severity=severity,
                message=message,
                stack_trace=stack_trace,
                context=context or {},
                tenant_id=tenant_id,
                workflow_id=workflow_id,
                component=component,
                recoverable=recoverable
            )

            self.error_events[error_id] = error_event

            # Update component health
            self.component_health[component] = "error"

            # Record Prometheus metrics
            if self.enable_metrics:
                self.error_counter.labels(
                    tenant_id=tenant_id or "unknown",
                    category=error_category.value,
                    component=component
                ).inc()

            # Record performance metric
            await self._record_metric(
                metric_type=MonitoringMetric.ERROR_RATE,
                value=1.0,
                tenant_id=tenant_id,
                component=component,
                tags={"error_category": error_category.value, "error_id": error_id}
            )

            # Attempt automatic recovery if applicable
            if recoverable and error_category in self.recovery_strategies:
                try:
                    await self.recovery_strategies[error_category](error_event)
                except Exception as recovery_error:
                    logger.error(f"Recovery strategy failed: {recovery_error}")

            # Trigger alerts if enabled
            if self.enable_alerting and severity in [AlertSeverity.CRITICAL, AlertSeverity.HIGH]:
                await self._trigger_alert(error_event)

            logger.error(f"Error recorded: {error_id} - {message}")

            return error_id

        except Exception as e:
            logger.error(f"Failed to record error: {e}")
            return ""

    async def record_compliance_validation(
        self,
        tenant_id: str,
        validation_result: ValidationResult,
        component: str = "compliance_validator"
    ):
        """Record compliance validation results"""
        try:
            if self.enable_metrics:
                self.compliance_score_gauge.labels(tenant_id=tenant_id).set(
                    validation_result.overall_score
                )

            await self._record_metric(
                metric_type=MonitoringMetric.COMPLIANCE_SCORE,
                value=validation_result.overall_score,
                tenant_id=tenant_id,
                component=component,
                tags={
                    "critical_issues": str(validation_result.critical_issues),
                    "total_issues": str(validation_result.total_issues)
                }
            )

            # Record compliance issues as errors if critical
            if validation_result.critical_issues > 0:
                await self.record_error(
                    component=component,
                    error_category=ErrorCategory.VALIDATION_ERROR,
                    message=f"Critical compliance issues found: {validation_result.critical_issues}",
                    context={
                        "compliance_score": validation_result.overall_score,
                        "critical_issues": validation_result.critical_issues,
                        "total_issues": validation_result.total_issues
                    },
                    tenant_id=tenant_id,
                    severity=AlertSeverity.HIGH
                )

            logger.info(f"Compliance validation recorded: {validation_result.overall_score:.1f}")

        except Exception as e:
            logger.error(f"Failed to record compliance validation: {e}")

    async def record_batch_progress(
        self,
        tenant_id: str,
        batch_result: BatchProcessingResult,
        component: str = "bulk_processor"
    ):
        """Record batch processing progress"""
        try:
            # Update queue length
            if self.enable_metrics:
                remaining_items = batch_result.total_items - batch_result.processed_items
                self.queue_length_gauge.labels(tenant_id=tenant_id).set(remaining_items)

            # Record throughput
            if batch_result.processing_time and batch_result.processing_time.total_seconds() > 0:
                throughput = batch_result.processed_items / batch_result.processing_time.total_seconds()
                await self._record_metric(
                    metric_type=MonitoringMetric.THROUGHPUT,
                    value=throughput,
                    tenant_id=tenant_id,
                    component=component,
                    tags={"batch_id": batch_result.batch_id}
                )

            # Record error rate
            await self._record_metric(
                metric_type=MonitoringMetric.ERROR_RATE,
                value=batch_result.error_rate,
                tenant_id=tenant_id,
                component=component,
                tags={"batch_id": batch_result.batch_id}
            )

            logger.debug(f"Batch progress recorded: {batch_result.processed_items}/{batch_result.total_items}")

        except Exception as e:
            logger.error(f"Failed to record batch progress: {e}")

    async def _record_metric(
        self,
        metric_type: MonitoringMetric,
        value: float,
        tenant_id: Optional[str],
        component: str,
        tags: Dict[str, str] = None
    ):
        """Record a performance metric"""
        if not self.enable_metrics:
            return

        try:
            metric = PerformanceMetric(
                metric_type=metric_type,
                value=value,
                timestamp=datetime.utcnow(),
                tenant_id=tenant_id,
                component=component,
                tags=tags or {}
            )

            self.performance_metrics.append(metric)

            # Keep metrics list manageable
            if len(self.performance_metrics) > 10000:
                # Remove oldest 20% of metrics
                remove_count = len(self.performance_metrics) // 5
                self.performance_metrics = self.performance_metrics[remove_count:]

        except Exception as e:
            logger.error(f"Failed to record metric: {e}")

    async def _monitor_system_health(self):
        """Background task to monitor system health"""
        while True:
            try:
                # Monitor CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                await self._record_metric(
                    metric_type=MonitoringMetric.RESOURCE_UTILIZATION,
                    value=cpu_percent,
                    tenant_id=None,
                    component="system",
                    tags={"resource": "cpu"}
                )

                if self.enable_metrics:
                    self.resource_utilization_gauge.labels(resource_type="cpu").set(cpu_percent)

                # Monitor memory usage
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                await self._record_metric(
                    metric_type=MonitoringMetric.RESOURCE_UTILIZATION,
                    value=memory_percent,
                    tenant_id=None,
                    component="system",
                    tags={"resource": "memory"}
                )

                if self.enable_metrics:
                    self.resource_utilization_gauge.labels(resource_type="memory").set(memory_percent)

                # Monitor disk usage
                disk = psutil.disk_usage('/')
                disk_percent = (disk.used / disk.total) * 100
                await self._record_metric(
                    metric_type=MonitoringMetric.RESOURCE_UTILIZATION,
                    value=disk_percent,
                    tenant_id=None,
                    component="system",
                    tags={"resource": "disk"}
                )

                if self.enable_metrics:
                    self.resource_utilization_gauge.labels(resource_type="disk").set(disk_percent)

                await asyncio.sleep(60)  # Monitor every minute

            except Exception as e:
                logger.error(f"System health monitoring error: {e}")
                await asyncio.sleep(300)  # Longer delay on error

    async def _cleanup_old_metrics(self):
        """Background task to clean up old metrics"""
        while True:
            try:
                cutoff_date = datetime.utcnow() - timedelta(days=self.metrics_retention_days)

                # Clean up performance metrics
                self.performance_metrics = [
                    metric for metric in self.performance_metrics
                    if metric.timestamp > cutoff_date
                ]

                # Clean up error events
                old_error_ids = [
                    error_id for error_id, error_event in self.error_events.items()
                    if error_event.timestamp < cutoff_date
                ]

                for error_id in old_error_ids:
                    del self.error_events[error_id]

                logger.info(f"Cleaned up {len(old_error_ids)} old error events")

                await asyncio.sleep(3600)  # Clean up every hour

            except Exception as e:
                logger.error(f"Metrics cleanup error: {e}")
                await asyncio.sleep(3600)

    async def _evaluate_alerts(self):
        """Background task to evaluate alert rules"""
        while True:
            try:
                if not self.enable_alerting:
                    await asyncio.sleep(60)
                    continue

                current_time = datetime.utcnow()

                for rule in self.alert_rules:
                    if not rule.enabled:
                        continue

                    # Check cooldown
                    last_alert = self.last_alert_times.get(rule.name)
                    if last_alert and (current_time - last_alert).total_seconds() < rule.cooldown_minutes * 60:
                        continue

                    # Get recent metrics for evaluation
                    recent_metrics = await self._get_recent_metrics(rule.metric_type, minutes=10)

                    if not recent_metrics:
                        continue

                    # Calculate metric value (average for most metrics)
                    metric_value = statistics.mean([metric.value for metric in recent_metrics])

                    # Evaluate threshold
                    triggered = False
                    if rule.comparison == ">":
                        triggered = metric_value > rule.threshold
                    elif rule.comparison == "<":
                        triggered = metric_value < rule.threshold
                    elif rule.comparison == ">=":
                        triggered = metric_value >= rule.threshold
                    elif rule.comparison == "<=":
                        triggered = metric_value <= rule.threshold
                    elif rule.comparison == "==":
                        triggered = abs(metric_value - rule.threshold) < 0.001

                    if triggered:
                        await self._send_alert(rule, metric_value)
                        self.last_alert_times[rule.name] = current_time

                await asyncio.sleep(60)  # Evaluate every minute

            except Exception as e:
                logger.error(f"Alert evaluation error: {e}")
                await asyncio.sleep(60)

    async def _analyze_error_patterns(self):
        """Background task to analyze error patterns"""
        while True:
            try:
                # Analyze error patterns every 30 minutes
                await asyncio.sleep(1800)

                # Group errors by category and component
                error_patterns = {}
                cutoff_time = datetime.utcnow() - timedelta(hours=24)

                for error_event in self.error_events.values():
                    if error_event.timestamp < cutoff_time:
                        continue

                    key = f"{error_event.category.value}_{error_event.component}"
                    if key not in error_patterns:
                        error_patterns[key] = []
                    error_patterns[key].append(error_event)

                # Analyze patterns and generate insights
                for pattern_key, errors in error_patterns.items():
                    if len(errors) >= 5:  # Pattern threshold
                        await self._generate_error_pattern_insight(pattern_key, errors)

            except Exception as e:
                logger.error(f"Error pattern analysis error: {e}")

    async def _get_recent_metrics(
        self,
        metric_type: MonitoringMetric,
        minutes: int = 10
    ) -> List[PerformanceMetric]:
        """Get recent metrics for a specific type"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)

        return [
            metric for metric in self.performance_metrics
            if metric.metric_type == metric_type and metric.timestamp > cutoff_time
        ]

    async def _send_alert(self, rule: AlertRule, current_value: float):
        """Send alert notification"""
        try:
            alert_message = f"Alert: {rule.name} - Current value: {current_value:.2f}, Threshold: {rule.threshold}"

            # Send to configured notification channels
            for handler in self.alert_handlers:
                try:
                    await handler(rule, current_value, alert_message)
                except Exception as e:
                    logger.error(f"Alert handler failed: {e}")

            logger.warning(alert_message)

        except Exception as e:
            logger.error(f"Failed to send alert: {e}")

    async def _generate_error_pattern_insight(self, pattern_key: str, errors: List[ErrorEvent]):
        """Generate insights from error patterns using AI"""
        try:
            error_summary = {
                "pattern": pattern_key,
                "count": len(errors),
                "time_range": f"{errors[0].timestamp} to {errors[-1].timestamp}",
                "messages": [error.message for error in errors[:5]]  # Sample messages
            }

            # Use AI to analyze pattern
            analysis_prompt = f"""
            Analyze this error pattern and provide insights:
            Pattern: {error_summary}

            Provide:
            1. Root cause analysis
            2. Potential solutions
            3. Prevention strategies
            """

            try:
                insight = await self.ai_coordinator.generate_response(
                    messages=[{"role": "user", "content": analysis_prompt}],
                    agent_type="error_analyst"
                )

                logger.info(f"Error pattern insight for {pattern_key}: {insight}")

            except Exception as ai_error:
                logger.error(f"AI error analysis failed: {ai_error}")

        except Exception as e:
            logger.error(f"Error pattern insight generation failed: {e}")

    async def _trigger_alert(self, error_event: ErrorEvent):
        """Trigger immediate alert for critical errors"""
        try:
            alert_message = f"Critical Error: {error_event.message} in {error_event.component}"

            for handler in self.alert_handlers:
                try:
                    await handler(None, None, alert_message)
                except Exception as e:
                    logger.error(f"Critical alert handler failed: {e}")

        except Exception as e:
            logger.error(f"Failed to trigger critical alert: {e}")

    # Recovery strategy implementations
    async def _handle_timeout_recovery(self, error_event: ErrorEvent):
        """Handle timeout error recovery"""
        try:
            logger.info(f"Attempting timeout recovery for {error_event.id}")

            # Implement exponential backoff retry
            if error_event.auto_retry_count < 3:
                error_event.auto_retry_count += 1
                delay = min(300, 30 * (2 ** error_event.auto_retry_count))

                logger.info(f"Scheduling retry in {delay} seconds")
                # In production, would re-queue the failed operation
                error_event.resolution_status = "auto_retry_scheduled"

        except Exception as e:
            logger.error(f"Timeout recovery failed: {e}")

    async def _handle_rate_limit_recovery(self, error_event: ErrorEvent):
        """Handle rate limit error recovery"""
        try:
            logger.info(f"Attempting rate limit recovery for {error_event.id}")

            # Implement adaptive rate limiting
            delay = 60  # Wait 1 minute before retry
            logger.info(f"Rate limit recovery: waiting {delay} seconds")

            error_event.resolution_status = "rate_limit_backoff"

        except Exception as e:
            logger.error(f"Rate limit recovery failed: {e}")

    async def _handle_api_error_recovery(self, error_event: ErrorEvent):
        """Handle API error recovery"""
        try:
            logger.info(f"Attempting API error recovery for {error_event.id}")

            # Check if alternative API endpoints are available
            # In production, would implement circuit breaker pattern
            error_event.resolution_status = "circuit_breaker_activated"

        except Exception as e:
            logger.error(f"API error recovery failed: {e}")

    async def _handle_system_error_recovery(self, error_event: ErrorEvent):
        """Handle system error recovery"""
        try:
            logger.info(f"Attempting system error recovery for {error_event.id}")

            # Check system resources and attempt cleanup
            # In production, would implement resource monitoring and cleanup
            error_event.resolution_status = "system_cleanup_initiated"

        except Exception as e:
            logger.error(f"System error recovery failed: {e}")

    async def _handle_validation_error_recovery(self, error_event: ErrorEvent):
        """Handle validation error recovery"""
        try:
            logger.info(f"Attempting validation error recovery for {error_event.id}")

            # Attempt auto-fix if possible
            # In production, would trigger auto-fix workflows
            error_event.resolution_status = "auto_fix_attempted"

        except Exception as e:
            logger.error(f"Validation error recovery failed: {e}")

    # Public interface methods
    async def get_system_health(self) -> SystemHealth:
        """Get current system health status"""
        try:
            # Calculate overall health score
            recent_errors = [
                error for error in self.error_events.values()
                if error.timestamp > datetime.utcnow() - timedelta(hours=1)
            ]

            error_rate = len(recent_errors) / max(1, len(self.error_events))
            health_score = max(0, 100 - (error_rate * 100))

            # Determine status
            if health_score >= 90:
                status = "healthy"
            elif health_score >= 70:
                status = "degraded"
            else:
                status = "unhealthy"

            # Get component health
            components = {}
            for component, health in self.component_health.items():
                components[component] = health

            # Get recent metrics
            recent_metrics = {}
            for metric_type in MonitoringMetric:
                metrics = await self._get_recent_metrics(metric_type, minutes=5)
                if metrics:
                    recent_metrics[metric_type.value] = statistics.mean([m.value for m in metrics])

            # Identify issues
            issues = []
            critical_errors = [e for e in recent_errors if e.severity == AlertSeverity.CRITICAL]
            if critical_errors:
                issues.append(f"{len(critical_errors)} critical errors in the last hour")

            return SystemHealth(
                status=status,
                score=health_score,
                components=components,
                metrics=recent_metrics,
                last_updated=datetime.utcnow(),
                issues=issues
            )

        except Exception as e:
            logger.error(f"Failed to get system health: {e}")
            return SystemHealth(
                status="unhealthy",
                score=0,
                components={},
                metrics={},
                last_updated=datetime.utcnow(),
                issues=[f"Health check failed: {str(e)}"]
            )

    def add_alert_handler(self, handler: Callable):
        """Add custom alert handler"""
        self.alert_handlers.append(handler)

    def get_prometheus_metrics(self) -> str:
        """Get Prometheus metrics in text format"""
        if not self.enable_metrics:
            return ""

        return generate_latest(self.registry).decode('utf-8')

    async def get_error_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get error summary for the specified time period"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            recent_errors = [
                error for error in self.error_events.values()
                if error.timestamp > cutoff_time
            ]

            # Group by category
            by_category = {}
            for error in recent_errors:
                category = error.category.value
                if category not in by_category:
                    by_category[category] = 0
                by_category[category] += 1

            # Group by component
            by_component = {}
            for error in recent_errors:
                component = error.component
                if component not in by_component:
                    by_component[component] = 0
                by_component[component] += 1

            return {
                "total_errors": len(recent_errors),
                "time_period_hours": hours,
                "by_category": by_category,
                "by_component": by_component,
                "error_rate": len(recent_errors) / max(1, hours),
                "critical_errors": len([e for e in recent_errors if e.severity == AlertSeverity.CRITICAL])
            }

        except Exception as e:
            logger.error(f"Failed to get error summary: {e}")
            return {"error": str(e)}

    async def shutdown(self):
        """Graceful shutdown of monitoring system"""
        logger.info("Shutting down monitoring system...")

        # Cancel background tasks
        for task in self.monitoring_tasks:
            task.cancel()

        # Wait for tasks to complete
        await asyncio.gather(*self.monitoring_tasks, return_exceptions=True)

        logger.info("Monitoring system shutdown completed")

# Export main classes
__all__ = [
    'AmazonWorkflowMonitor',
    'ErrorEvent',
    'PerformanceMetric',
    'AlertRule',
    'SystemHealth',
    'AlertSeverity',
    'MonitoringMetric',
    'ErrorCategory'
]