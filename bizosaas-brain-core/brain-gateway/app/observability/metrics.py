"""
Custom metrics for BizOSaaS Platform
Provides standardized metrics for monitoring connector operations, workflows, and system health.
"""

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
try:
    from opentelemetry.exporter.prometheus import PrometheusMetricReader
    PROMETHEUS_AVAILABLE = True
except ImportError:
    logging.warning("OpenTelemetry Prometheus exporter not found. Prometheus metrics disabled.")
    PROMETHEUS_AVAILABLE = False
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import os
import logging

logger = logging.getLogger(__name__)

# Initialize metrics
resource = Resource(attributes={
    SERVICE_NAME: "brain-gateway"
})

# Use Prometheus exporter for metrics
if PROMETHEUS_AVAILABLE:
    prometheus_reader = PrometheusMetricReader()
    meter_provider = MeterProvider(resource=resource, metric_readers=[prometheus_reader])
else:
    # Use fallback or no-op provider
    meter_provider = MeterProvider(resource=resource)

metrics.set_meter_provider(meter_provider)

# Get meter
meter = metrics.get_meter(__name__)

# ============================================================================
# Connector Metrics
# ============================================================================

connector_operations_counter = meter.create_counter(
    name="connector.operations.total",
    description="Total number of connector operations",
    unit="1"
)

connector_operation_duration = meter.create_histogram(
    name="connector.operation.duration",
    description="Duration of connector operations in milliseconds",
    unit="ms"
)

connector_errors_counter = meter.create_counter(
    name="connector.errors.total",
    description="Total number of connector errors",
    unit="1"
)

connector_sync_operations = meter.create_counter(
    name="connector.sync.operations",
    description="Total number of sync operations per connector",
    unit="1"
)

connector_sync_records = meter.create_counter(
    name="connector.sync.records",
    description="Total number of records synced",
    unit="1"
)

# ============================================================================
# Workflow Metrics
# ============================================================================

workflow_executions_counter = meter.create_counter(
    name="workflow.executions.total",
    description="Total number of workflow executions",
    unit="1"
)

workflow_execution_duration = meter.create_histogram(
    name="workflow.execution.duration",
    description="Duration of workflow executions in milliseconds",
    unit="ms"
)

workflow_step_duration = meter.create_histogram(
    name="workflow.step.duration",
    description="Duration of individual workflow steps in milliseconds",
    unit="ms"
)

workflow_failures_counter = meter.create_counter(
    name="workflow.failures.total",
    description="Total number of workflow failures",
    unit="1"
)

# ============================================================================
# AI Agent Metrics
# ============================================================================

agent_invocations_counter = meter.create_counter(
    name="agent.invocations.total",
    description="Total number of agent invocations",
    unit="1"
)

agent_response_duration = meter.create_histogram(
    name="agent.response.duration",
    description="Duration of agent responses in milliseconds",
    unit="ms"
)

agent_token_usage = meter.create_counter(
    name="agent.tokens.used",
    description="Total number of tokens used by agents",
    unit="1"
)

agent_errors_counter = meter.create_counter(
    name="agent.errors.total",
    description="Total number of agent errors",
    unit="1"
)

# ============================================================================
# API Metrics
# ============================================================================

api_requests_counter = meter.create_counter(
    name="api.requests.total",
    description="Total number of API requests",
    unit="1"
)

api_request_duration = meter.create_histogram(
    name="api.request.duration",
    description="Duration of API requests in milliseconds",
    unit="ms"
)

api_errors_counter = meter.create_counter(
    name="api.errors.total",
    description="Total number of API errors",
    unit="1"
)

# ============================================================================
# Database Metrics
# ============================================================================

db_query_duration = meter.create_histogram(
    name="db.query.duration",
    description="Duration of database queries in milliseconds",
    unit="ms"
)

db_connection_pool_size = meter.create_up_down_counter(
    name="db.connection.pool.size",
    description="Current database connection pool size",
    unit="1"
)

# ============================================================================
# Cache Metrics
# ============================================================================

cache_hits_counter = meter.create_counter(
    name="cache.hits.total",
    description="Total number of cache hits",
    unit="1"
)

cache_misses_counter = meter.create_counter(
    name="cache.misses.total",
    description="Total number of cache misses",
    unit="1"
)

# ============================================================================
# Helper Functions
# ============================================================================

def record_connector_operation(
    connector_type: str,
    operation: str,
    duration_ms: float,
    success: bool = True,
    tenant_id: str = "unknown"
):
    """Record a connector operation with metrics"""
    attributes = {
        "connector_type": connector_type,
        "operation": operation,
        "tenant_id": tenant_id,
        "status": "success" if success else "error"
    }
    
    connector_operations_counter.add(1, attributes)
    connector_operation_duration.record(duration_ms, attributes)
    
    if not success:
        connector_errors_counter.add(1, attributes)

def record_connector_sync(
    connector_type: str,
    resource_type: str,
    record_count: int,
    tenant_id: str = "unknown"
):
    """Record a connector sync operation"""
    attributes = {
        "connector_type": connector_type,
        "resource_type": resource_type,
        "tenant_id": tenant_id
    }
    
    connector_sync_operations.add(1, attributes)
    connector_sync_records.add(record_count, attributes)

def record_workflow_execution(
    workflow_id: str,
    duration_ms: float,
    success: bool = True,
    tenant_id: str = "unknown"
):
    """Record a workflow execution"""
    attributes = {
        "workflow_id": workflow_id,
        "tenant_id": tenant_id,
        "status": "success" if success else "failed"
    }
    
    workflow_executions_counter.add(1, attributes)
    workflow_execution_duration.record(duration_ms, attributes)
    
    if not success:
        workflow_failures_counter.add(1, attributes)

def record_agent_invocation(
    agent_id: str,
    duration_ms: float,
    tokens_used: int = 0,
    success: bool = True,
    tenant_id: str = "unknown"
):
    """Record an AI agent invocation"""
    attributes = {
        "agent_id": agent_id,
        "tenant_id": tenant_id,
        "status": "success" if success else "error"
    }
    
    agent_invocations_counter.add(1, attributes)
    agent_response_duration.record(duration_ms, attributes)
    
    if tokens_used > 0:
        agent_token_usage.add(tokens_used, attributes)
    
    if not success:
        agent_errors_counter.add(1, attributes)

logger.info("Custom metrics initialized successfully")
