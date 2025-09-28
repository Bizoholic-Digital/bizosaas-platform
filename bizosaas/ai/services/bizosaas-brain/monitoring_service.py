#!/usr/bin/env python3
"""
BizOSaaS Monitoring Service
Prometheus FastAPI Instrumentator for comprehensive observability
"""

from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
from fastapi.responses import Response as FastAPIResponse
from typing import Dict, Any, Optional, List
import time
import psutil
import asyncio
import logging
import json
from datetime import datetime, timedelta
import os

# Set up logging
logger = logging.getLogger(__name__)

class BizOSaaSMonitoringService:
    """Comprehensive monitoring service for BizOSaaS platform"""
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.instrumentator = None
        
        # Custom metrics
        self.setup_custom_metrics()
        
        # System metrics
        self.system_metrics = {}
        
        # Business metrics
        self.business_metrics = {
            "total_tenants": 0,
            "active_tenants": 0,
            "total_users": 0,
            "active_users": 0,
            "leads_generated": 0,
            "emails_sent": 0,
            "ai_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0
        }
        
        # Performance tracking
        self.performance_metrics = {
            "avg_response_time": 0,
            "p95_response_time": 0,
            "p99_response_time": 0,
            "error_rate": 0,
            "throughput": 0
        }
    
    def setup_custom_metrics(self):
        """Setup custom Prometheus metrics"""
        # Business metrics
        self.tenant_counter = Counter(
            'bizosaas_tenants_total',
            'Total number of tenants',
            ['status']
        )
        
        self.user_counter = Counter(
            'bizosaas_users_total',
            'Total number of users',
            ['tenant_id', 'status']
        )
        
        self.lead_counter = Counter(
            'bizosaas_leads_total',
            'Total number of leads generated',
            ['tenant_id', 'source']
        )
        
        self.email_counter = Counter(
            'bizosaas_emails_sent_total',
            'Total number of emails sent',
            ['tenant_id', 'template', 'status']
        )
        
        self.ai_request_counter = Counter(
            'bizosaas_ai_requests_total',
            'Total number of AI requests',
            ['tenant_id', 'model', 'status']
        )
        
        self.ai_request_duration = Histogram(
            'bizosaas_ai_request_duration_seconds',
            'AI request processing time',
            ['tenant_id', 'model'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
        )
        
        # Cache metrics
        self.cache_counter = Counter(
            'bizosaas_cache_operations_total',
            'Total cache operations',
            ['operation', 'status']
        )
        
        # System metrics
        self.memory_usage = Gauge(
            'bizosaas_memory_usage_bytes',
            'Memory usage in bytes'
        )
        
        self.cpu_usage = Gauge(
            'bizosaas_cpu_usage_percent',
            'CPU usage percentage'
        )
        
        self.disk_usage = Gauge(
            'bizosaas_disk_usage_percent',
            'Disk usage percentage'
        )
        
        # Active connections
        self.active_connections = Gauge(
            'bizosaas_active_connections',
            'Number of active connections'
        )
        
        # Database metrics
        self.db_pool_size = Gauge(
            'bizosaas_db_pool_size',
            'Database connection pool size'
        )
        
        self.db_active_connections = Gauge(
            'bizosaas_db_active_connections',
            'Active database connections'
        )
        
        # API endpoint metrics
        self.endpoint_requests = Counter(
            'bizosaas_endpoint_requests_total',
            'Total requests per endpoint',
            ['method', 'endpoint', 'tenant_id', 'status_code']
        )
        
        self.endpoint_duration = Histogram(
            'bizosaas_endpoint_duration_seconds',
            'Request processing time per endpoint',
            ['method', 'endpoint', 'tenant_id'],
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
        )
    
    def setup_instrumentator(self):
        """Setup FastAPI instrumentator with custom configuration"""
        self.instrumentator = Instrumentator(
            should_group_status_codes=False,
            should_ignore_untemplated=True,
            should_respect_env_var=True,
            should_instrument_requests_inprogress=True,
            excluded_handlers=["/metrics", "/health", "/docs", "/openapi.json"],
            env_var_name="ENABLE_METRICS",
            inprogress_name="bizosaas_inprogress",
            inprogress_labels=True,
        )
        
        # Add default metrics
        self.instrumentator.add(
            metrics.request_size(
                should_include_handler=True,
                should_include_method=True,
                should_include_status=True,
                metric_namespace="bizosaas",
                metric_subsystem="http",
            )
        ).add(
            metrics.response_size(
                should_include_handler=True,
                should_include_method=True,
                should_include_status=True,
                metric_namespace="bizosaas",
                metric_subsystem="http",
            )
        ).add(
            metrics.latency(
                should_include_handler=True,
                should_include_method=True,
                should_include_status=True,
                metric_namespace="bizosaas",
                metric_subsystem="http",
            )
        ).add(
            metrics.requests(
                should_include_handler=True,
                should_include_method=True,
                should_include_status=True,
                metric_namespace="bizosaas",
                metric_subsystem="http",
            )
        )
        
        # Add custom info metric
        self.instrumentator.add(
            self._custom_tenant_info()
        )
        
        # Initialize instrumentator
        self.instrumentator.instrument(self.app)
        
        # Expose metrics endpoint
        self.instrumentator.expose(self.app, endpoint="/metrics")
        
        logger.info("Prometheus instrumentator initialized successfully")
    
    def _custom_tenant_info(self):
        """Custom metric function to track tenant information"""
        def instrumentation(info: metrics.Info) -> None:
            if hasattr(info.request, "state") and hasattr(info.request.state, "tenant_id"):
                tenant_id = info.request.state.tenant_id
                
                # Track endpoint requests by tenant
                self.endpoint_requests.labels(
                    method=info.method,
                    endpoint=info.modified_handler,
                    tenant_id=tenant_id,
                    status_code=info.response.status_code
                ).inc()
                
                # Track endpoint duration by tenant
                if hasattr(info, "modified_duration"):
                    self.endpoint_duration.labels(
                        method=info.method,
                        endpoint=info.modified_handler,
                        tenant_id=tenant_id
                    ).observe(info.modified_duration)
        
        return instrumentation
    
    async def update_system_metrics(self):
        """Update system metrics"""
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            self.memory_usage.set(memory.used)
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_usage.set(cpu_percent)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.disk_usage.set(disk_percent)
            
            # Update system metrics dict
            self.system_metrics = {
                "memory_usage_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "cpu_usage_percent": cpu_percent,
                "disk_usage_percent": round(disk_percent, 2),
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "load_average": os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to update system metrics: {e}")
    
    def record_tenant_metric(self, tenant_id: str, status: str = "active"):
        """Record tenant metric"""
        self.tenant_counter.labels(status=status).inc()
        if status == "active":
            self.business_metrics["active_tenants"] += 1
        self.business_metrics["total_tenants"] += 1
    
    def record_user_metric(self, tenant_id: str, status: str = "active"):
        """Record user metric"""
        self.user_counter.labels(tenant_id=tenant_id, status=status).inc()
        if status == "active":
            self.business_metrics["active_users"] += 1
        self.business_metrics["total_users"] += 1
    
    def record_lead_metric(self, tenant_id: str, source: str = "website"):
        """Record lead generation metric"""
        self.lead_counter.labels(tenant_id=tenant_id, source=source).inc()
        self.business_metrics["leads_generated"] += 1
    
    def record_email_metric(self, tenant_id: str, template: str, status: str = "sent"):
        """Record email sending metric"""
        self.email_counter.labels(tenant_id=tenant_id, template=template, status=status).inc()
        if status == "sent":
            self.business_metrics["emails_sent"] += 1
    
    def record_ai_request(self, tenant_id: str, model: str, duration: float, status: str = "success"):
        """Record AI request metrics"""
        self.ai_request_counter.labels(tenant_id=tenant_id, model=model, status=status).inc()
        self.ai_request_duration.labels(tenant_id=tenant_id, model=model).observe(duration)
        self.business_metrics["ai_requests"] += 1
    
    def record_cache_operation(self, operation: str, status: str):
        """Record cache operation metrics"""
        self.cache_counter.labels(operation=operation, status=status).inc()
        if status == "hit":
            self.business_metrics["cache_hits"] += 1
        elif status == "miss":
            self.business_metrics["cache_misses"] += 1
    
    async def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary"""
        await self.update_system_metrics()
        
        # Calculate cache hit ratio
        total_cache_ops = self.business_metrics["cache_hits"] + self.business_metrics["cache_misses"]
        cache_hit_ratio = (self.business_metrics["cache_hits"] / total_cache_ops * 100) if total_cache_ops > 0 else 0
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "system_metrics": self.system_metrics,
            "business_metrics": {
                **self.business_metrics,
                "cache_hit_ratio": round(cache_hit_ratio, 2)
            },
            "performance_metrics": self.performance_metrics,
            "service_status": {
                "uptime_seconds": time.time() - getattr(self, 'start_time', time.time()),
                "version": os.getenv("SERVICE_VERSION", "1.0.0"),
                "environment": os.getenv("ENVIRONMENT", "development")
            }
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        health_status = {
            "status": "healthy",
            "service": "monitoring",
            "timestamp": datetime.utcnow().isoformat(),
            "version": os.getenv("SERVICE_VERSION", "1.0.0")
        }
        
        try:
            # Check system resources
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Health thresholds
            memory_threshold = 90  # 90%
            cpu_threshold = 90     # 90%
            
            if memory.percent > memory_threshold:
                health_status["status"] = "degraded"
                health_status["warnings"] = health_status.get("warnings", [])
                health_status["warnings"].append(f"High memory usage: {memory.percent}%")
            
            if cpu_percent > cpu_threshold:
                health_status["status"] = "degraded"
                health_status["warnings"] = health_status.get("warnings", [])
                health_status["warnings"].append(f"High CPU usage: {cpu_percent}%")
            
            # Add system info
            health_status["system"] = {
                "memory_percent": memory.percent,
                "cpu_percent": cpu_percent,
                "available_memory_gb": round(memory.available / (1024**3), 2)
            }
            
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["error"] = str(e)
        
        return health_status
    
    async def start_background_tasks(self):
        """Start background monitoring tasks"""
        self.start_time = time.time()
        
        async def system_metrics_updater():
            """Background task to update system metrics"""
            while True:
                try:
                    await self.update_system_metrics()
                    await asyncio.sleep(30)  # Update every 30 seconds
                except Exception as e:
                    logger.error(f"System metrics update error: {e}")
                    await asyncio.sleep(60)  # Wait longer on error
        
        # Start background task
        asyncio.create_task(system_metrics_updater())
        logger.info("Background monitoring tasks started")
    
    def create_middleware(self):
        """Create monitoring middleware"""
        async def monitoring_middleware(request: Request, call_next):
            # Start timing
            start_time = time.time()
            
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Extract tenant info if available
            tenant_id = getattr(request.state, 'tenant_id', 'unknown')
            
            # Record metrics would happen in instrumentator
            # This middleware can be used for custom business logic
            
            return response
        
        return monitoring_middleware

def setup_monitoring(app: FastAPI) -> BizOSaaSMonitoringService:
    """Setup monitoring for FastAPI app"""
    monitoring = BizOSaaSMonitoringService(app)
    monitoring.setup_instrumentator()
    
    # Add middleware
    app.middleware("http")(monitoring.create_middleware())
    
    # Add monitoring endpoints
    @app.get("/health/monitoring")
    async def monitoring_health():
        return await monitoring.health_check()
    
    @app.get("/metrics/summary")
    async def metrics_summary():
        return await monitoring.get_metrics_summary()
    
    return monitoring