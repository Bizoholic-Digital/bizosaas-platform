"""
Performance Monitoring and Metrics Collection
Comprehensive monitoring for order processing workflow
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from collections import defaultdict, deque
import psutil
import threading

logger = logging.getLogger(__name__)


@dataclass
class MetricPoint:
    """Single metric data point"""
    timestamp: datetime
    value: float
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceMetrics:
    """Performance metrics container"""
    response_time_ms: float = 0.0
    throughput_per_second: float = 0.0
    error_rate_percent: float = 0.0
    cpu_usage_percent: float = 0.0
    memory_usage_mb: float = 0.0
    active_connections: int = 0
    queue_size: int = 0


class PerformanceMonitor:
    """
    Performance monitoring system for order processing
    Tracks response times, throughput, errors, and system resources
    """
    
    def __init__(self, max_history_size: int = 10000):
        self.max_history_size = max_history_size
        
        # Metrics storage
        self.metrics_history = defaultdict(lambda: deque(maxlen=max_history_size))
        self.active_requests = {}
        self.system_metrics = {}
        
        # Performance counters
        self.counters = defaultdict(int)
        self.timers = defaultdict(list)
        self.gauges = defaultdict(float)
        
        # Alerting thresholds
        self.thresholds = {
            "response_time_ms": 5000,      # 5 seconds
            "error_rate_percent": 5.0,      # 5%
            "cpu_usage_percent": 80.0,      # 80%
            "memory_usage_mb": 2048,        # 2GB
            "queue_size": 1000              # 1000 items
        }
        
        # Alert callbacks
        self.alert_callbacks = []
        
        # Background monitoring
        self._monitoring_active = True
        self._start_background_monitoring()
    
    def start_order_processing(self, order_id: str) -> str:
        """Start tracking order processing time"""
        
        request_id = f"order_{order_id}_{int(time.time() * 1000)}"
        
        self.active_requests[request_id] = {
            "order_id": order_id,
            "start_time": time.time(),
            "start_datetime": datetime.utcnow(),
            "stage": "started",
            "checkpoints": []
        }
        
        # Increment active requests counter
        self.gauges["active_requests"] += 1
        
        logger.debug(f"Started monitoring order processing: {order_id}")
        
        return request_id
    
    def add_checkpoint(self, request_id: str, checkpoint_name: str, metadata: Optional[Dict[str, Any]] = None):
        """Add performance checkpoint"""
        
        if request_id in self.active_requests:
            current_time = time.time()
            start_time = self.active_requests[request_id]["start_time"]
            
            checkpoint = {
                "name": checkpoint_name,
                "timestamp": datetime.utcnow(),
                "elapsed_ms": (current_time - start_time) * 1000,
                "metadata": metadata or {}
            }
            
            self.active_requests[request_id]["checkpoints"].append(checkpoint)
            self.active_requests[request_id]["stage"] = checkpoint_name
            
            logger.debug(f"Checkpoint {checkpoint_name}: {checkpoint['elapsed_ms']:.2f}ms")
    
    def complete_order_processing(self, request_id: str, processing_time: float, success: bool):
        """Complete order processing tracking"""
        
        if request_id not in self.active_requests:
            logger.warning(f"Request ID {request_id} not found in active requests")
            return
        
        request_data = self.active_requests.pop(request_id)
        order_id = request_data["order_id"]
        
        # Record metrics
        self._record_metric("order_processing_time_ms", processing_time * 1000, {
            "order_id": order_id,
            "success": str(success)
        })
        
        # Update counters
        self.counters["total_orders"] += 1
        if success:
            self.counters["successful_orders"] += 1
        else:
            self.counters["failed_orders"] += 1
        
        # Update gauges
        self.gauges["active_requests"] -= 1
        
        # Calculate throughput
        self._update_throughput()
        
        # Calculate error rate
        self._update_error_rate()
        
        logger.info(f"Completed monitoring order {order_id}: {processing_time:.2f}s, success: {success}")
    
    def record_payment_processing(self, order_id: str, gateway: str, amount: float, processing_time: float, success: bool):
        """Record payment processing metrics"""
        
        tags = {
            "order_id": order_id,
            "gateway": gateway,
            "success": str(success)
        }
        
        self._record_metric("payment_processing_time_ms", processing_time * 1000, tags)
        self._record_metric("payment_amount", amount, tags)
        
        # Gateway-specific counters
        self.counters[f"payments_{gateway}_total"] += 1
        if success:
            self.counters[f"payments_{gateway}_success"] += 1
        else:
            self.counters[f"payments_{gateway}_failed"] += 1
    
    def record_inventory_operation(self, operation: str, product_count: int, processing_time: float, success: bool):
        """Record inventory operation metrics"""
        
        tags = {
            "operation": operation,
            "success": str(success)
        }
        
        self._record_metric("inventory_operation_time_ms", processing_time * 1000, tags)
        self._record_metric("inventory_product_count", product_count, tags)
        
        self.counters[f"inventory_{operation}_total"] += 1
        if success:
            self.counters[f"inventory_{operation}_success"] += 1
        else:
            self.counters[f"inventory_{operation}_failed"] += 1
    
    def record_fulfillment_operation(self, operation: str, item_count: int, processing_time: float, success: bool):
        """Record fulfillment operation metrics"""
        
        tags = {
            "operation": operation,
            "success": str(success)
        }
        
        self._record_metric("fulfillment_operation_time_ms", processing_time * 1000, tags)
        self._record_metric("fulfillment_item_count", item_count, tags)
        
        self.counters[f"fulfillment_{operation}_total"] += 1
        if success:
            self.counters[f"fulfillment_{operation}_success"] += 1
        else:
            self.counters[f"fulfillment_{operation}_failed"] += 1
    
    def record_notification_sent(self, notification_type: str, channel: str, success: bool):
        """Record notification metrics"""
        
        tags = {
            "type": notification_type,
            "channel": channel,
            "success": str(success)
        }
        
        self._record_metric("notification_sent", 1, tags)
        
        self.counters[f"notifications_{channel}_total"] += 1
        if success:
            self.counters[f"notifications_{channel}_success"] += 1
        else:
            self.counters[f"notifications_{channel}_failed"] += 1
    
    def record_api_request(self, endpoint: str, method: str, response_time: float, status_code: int):
        """Record API request metrics"""
        
        tags = {
            "endpoint": endpoint,
            "method": method,
            "status_code": str(status_code),
            "success": str(200 <= status_code < 400)
        }
        
        self._record_metric("api_response_time_ms", response_time * 1000, tags)
        
        self.counters[f"api_requests_total"] += 1
        self.counters[f"api_requests_{status_code}"] += 1
    
    def get_metrics(self, time_range_minutes: int = 60) -> Dict[str, Any]:
        """Get comprehensive metrics for specified time range"""
        
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_range_minutes)
        
        # Calculate metrics
        current_metrics = self._calculate_current_metrics(cutoff_time)
        
        # Get system metrics
        system_metrics = self._get_system_metrics()
        
        # Get performance summary
        performance_summary = self._get_performance_summary(cutoff_time)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "time_range_minutes": time_range_minutes,
            "current_metrics": current_metrics,
            "system_metrics": system_metrics,
            "performance_summary": performance_summary,
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "active_requests": len(self.active_requests),
            "alerts": self._check_alerts()
        }
    
    def get_order_processing_stats(self) -> Dict[str, Any]:
        """Get order processing specific statistics"""
        
        # Calculate processing time statistics
        processing_times = [
            point.value for point in self.metrics_history["order_processing_time_ms"]
            if point.timestamp > datetime.utcnow() - timedelta(hours=24)
        ]
        
        if processing_times:
            avg_processing_time = sum(processing_times) / len(processing_times)
            min_processing_time = min(processing_times)
            max_processing_time = max(processing_times)
            
            # Calculate percentiles
            sorted_times = sorted(processing_times)
            p50 = sorted_times[int(len(sorted_times) * 0.5)]
            p95 = sorted_times[int(len(sorted_times) * 0.95)]
            p99 = sorted_times[int(len(sorted_times) * 0.99)]
        else:
            avg_processing_time = min_processing_time = max_processing_time = 0
            p50 = p95 = p99 = 0
        
        return {
            "total_orders_processed": self.counters.get("total_orders", 0),
            "successful_orders": self.counters.get("successful_orders", 0),
            "failed_orders": self.counters.get("failed_orders", 0),
            "success_rate_percent": self._calculate_success_rate(),
            "average_processing_time_ms": avg_processing_time,
            "min_processing_time_ms": min_processing_time,
            "max_processing_time_ms": max_processing_time,
            "p50_processing_time_ms": p50,
            "p95_processing_time_ms": p95,
            "p99_processing_time_ms": p99,
            "current_throughput_per_minute": self.gauges.get("throughput_per_minute", 0),
            "active_processing_requests": self.gauges.get("active_requests", 0)
        }
    
    def add_alert_callback(self, callback: Callable[[str, Dict[str, Any]], None]):
        """Add callback for alerts"""
        self.alert_callbacks.append(callback)
    
    def set_threshold(self, metric_name: str, threshold_value: float):
        """Set alert threshold for metric"""
        self.thresholds[metric_name] = threshold_value
    
    def shutdown(self):
        """Shutdown monitoring"""
        self._monitoring_active = False
        logger.info("Performance monitoring shutdown")
    
    # Private methods
    
    def _record_metric(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Record metric point"""
        
        metric_point = MetricPoint(
            timestamp=datetime.utcnow(),
            value=value,
            tags=tags or {}
        )
        
        self.metrics_history[metric_name].append(metric_point)
    
    def _calculate_current_metrics(self, cutoff_time: datetime) -> PerformanceMetrics:
        """Calculate current performance metrics"""
        
        # Filter recent metrics
        recent_processing_times = [
            point.value for point in self.metrics_history["order_processing_time_ms"]
            if point.timestamp > cutoff_time
        ]
        
        # Calculate averages
        avg_response_time = sum(recent_processing_times) / len(recent_processing_times) if recent_processing_times else 0
        
        return PerformanceMetrics(
            response_time_ms=avg_response_time,
            throughput_per_second=self.gauges.get("throughput_per_second", 0),
            error_rate_percent=self.gauges.get("error_rate_percent", 0),
            cpu_usage_percent=self.gauges.get("cpu_usage_percent", 0),
            memory_usage_mb=self.gauges.get("memory_usage_mb", 0),
            active_connections=self.gauges.get("active_requests", 0),
            queue_size=self.gauges.get("queue_size", 0)
        )
    
    def _get_system_metrics(self) -> Dict[str, Any]:
        """Get system resource metrics"""
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            self.gauges["cpu_usage_percent"] = cpu_percent
            self.gauges["memory_usage_mb"] = memory.used / (1024 * 1024)
            self.gauges["memory_usage_percent"] = memory.percent
            
            return {
                "cpu_usage_percent": cpu_percent,
                "memory_usage_mb": memory.used / (1024 * 1024),
                "memory_usage_percent": memory.percent,
                "memory_available_mb": memory.available / (1024 * 1024),
                "disk_usage_percent": (disk.used / disk.total) * 100,
                "disk_free_gb": disk.free / (1024 * 1024 * 1024)
            }
            
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            return {}
    
    def _get_performance_summary(self, cutoff_time: datetime) -> Dict[str, Any]:
        """Get performance summary"""
        
        # Recent orders
        recent_orders = self.counters.get("total_orders", 0)
        recent_successful = self.counters.get("successful_orders", 0)
        recent_failed = self.counters.get("failed_orders", 0)
        
        return {
            "orders_processed": recent_orders,
            "successful_orders": recent_successful,
            "failed_orders": recent_failed,
            "success_rate_percent": (recent_successful / recent_orders * 100) if recent_orders > 0 else 0,
            "average_throughput": self.gauges.get("throughput_per_minute", 0),
            "peak_concurrent_requests": max(self.gauges.get("peak_active_requests", 0), self.gauges.get("active_requests", 0))
        }
    
    def _update_throughput(self):
        """Update throughput metrics"""
        
        current_time = datetime.utcnow()
        one_minute_ago = current_time - timedelta(minutes=1)
        
        # Count orders in last minute
        recent_orders = len([
            point for point in self.metrics_history["order_processing_time_ms"]
            if point.timestamp > one_minute_ago
        ])
        
        self.gauges["throughput_per_minute"] = recent_orders
        self.gauges["throughput_per_second"] = recent_orders / 60.0
    
    def _update_error_rate(self):
        """Update error rate metrics"""
        
        total_orders = self.counters.get("total_orders", 0)
        failed_orders = self.counters.get("failed_orders", 0)
        
        if total_orders > 0:
            self.gauges["error_rate_percent"] = (failed_orders / total_orders) * 100
        else:
            self.gauges["error_rate_percent"] = 0
    
    def _calculate_success_rate(self) -> float:
        """Calculate overall success rate"""
        
        total_orders = self.counters.get("total_orders", 0)
        successful_orders = self.counters.get("successful_orders", 0)
        
        if total_orders > 0:
            return (successful_orders / total_orders) * 100
        return 0.0
    
    def _check_alerts(self) -> List[Dict[str, Any]]:
        """Check for alert conditions"""
        
        alerts = []
        
        # Check thresholds
        for metric_name, threshold in self.thresholds.items():
            current_value = self.gauges.get(metric_name, 0)
            
            if current_value > threshold:
                alert = {
                    "metric": metric_name,
                    "current_value": current_value,
                    "threshold": threshold,
                    "severity": "warning" if current_value < threshold * 1.2 else "critical",
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                alerts.append(alert)
                
                # Call alert callbacks
                for callback in self.alert_callbacks:
                    try:
                        callback(metric_name, alert)
                    except Exception as e:
                        logger.error(f"Alert callback failed: {e}")
        
        return alerts
    
    def _start_background_monitoring(self):
        """Start background monitoring thread"""
        
        def monitor_loop():
            while self._monitoring_active:
                try:
                    # Update system metrics
                    self._get_system_metrics()
                    
                    # Update throughput
                    self._update_throughput()
                    
                    # Update error rate
                    self._update_error_rate()
                    
                    # Check alerts
                    self._check_alerts()
                    
                    # Update peak active requests
                    current_active = self.gauges.get("active_requests", 0)
                    peak_active = self.gauges.get("peak_active_requests", 0)
                    if current_active > peak_active:
                        self.gauges["peak_active_requests"] = current_active
                    
                    time.sleep(30)  # Update every 30 seconds
                    
                except Exception as e:
                    logger.error(f"Background monitoring error: {e}")
                    time.sleep(10)  # Wait before retry
        
        monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitoring_thread.start()


class MetricsCollector:
    """
    Metrics collection and aggregation system
    Collects and stores metrics for analytics and reporting
    """
    
    def __init__(self):
        self.metrics_store = defaultdict(list)
        self.aggregated_metrics = {}
        self.collection_interval = 60  # seconds
        self._start_collection()
    
    async def record_order_metric(self, order_id: str, metric_type: str, value: float, metadata: Optional[Dict[str, Any]] = None):
        """Record order-specific metric"""
        
        metric_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "order_id": order_id,
            "metric_type": metric_type,
            "value": value,
            "metadata": metadata or {}
        }
        
        self.metrics_store[metric_type].append(metric_entry)
        
        logger.debug(f"Recorded metric {metric_type}: {value} for order {order_id}")
    
    async def record_business_metric(self, metric_type: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Record business-level metric"""
        
        metric_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "metric_type": metric_type,
            "value": value,
            "tags": tags or {}
        }
        
        self.metrics_store["business_metrics"].append(metric_entry)
    
    def get_aggregated_metrics(self, metric_type: str, aggregation_period: str = "hour") -> Dict[str, Any]:
        """Get aggregated metrics for specified period"""
        
        if metric_type not in self.metrics_store:
            return {"error": f"Metric type {metric_type} not found"}
        
        # Simple aggregation (in production, use proper time-series database)
        metrics = self.metrics_store[metric_type]
        
        if not metrics:
            return {"count": 0, "average": 0, "sum": 0, "min": 0, "max": 0}
        
        values = [m["value"] for m in metrics]
        
        return {
            "count": len(values),
            "average": sum(values) / len(values),
            "sum": sum(values),
            "min": min(values),
            "max": max(values),
            "latest": values[-1] if values else 0
        }
    
    def get_business_kpis(self) -> Dict[str, Any]:
        """Get key business KPIs"""
        
        # Calculate KPIs from collected metrics
        order_metrics = self.get_aggregated_metrics("processing_time")
        revenue_metrics = self.get_aggregated_metrics("order_value")
        
        return {
            "total_orders_processed": order_metrics.get("count", 0),
            "average_processing_time_seconds": order_metrics.get("average", 0) / 1000,
            "total_revenue": revenue_metrics.get("sum", 0),
            "average_order_value": revenue_metrics.get("average", 0),
            "orders_per_minute": self._calculate_orders_per_minute(),
            "revenue_per_hour": self._calculate_revenue_per_hour(),
            "customer_satisfaction_score": self._calculate_satisfaction_score()
        }
    
    def export_metrics(self, format_type: str = "json") -> str:
        """Export metrics in specified format"""
        
        if format_type == "json":
            import json
            return json.dumps(dict(self.metrics_store), indent=2, default=str)
        elif format_type == "csv":
            return self._export_as_csv()
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _start_collection(self):
        """Start background metrics collection"""
        
        def collection_loop():
            while True:
                try:
                    # Aggregate metrics periodically
                    self._aggregate_metrics()
                    
                    # Cleanup old metrics
                    self._cleanup_old_metrics()
                    
                    time.sleep(self.collection_interval)
                    
                except Exception as e:
                    logger.error(f"Metrics collection error: {e}")
                    time.sleep(10)
        
        collection_thread = threading.Thread(target=collection_loop, daemon=True)
        collection_thread.start()
    
    def _aggregate_metrics(self):
        """Aggregate metrics for reporting"""
        
        current_time = datetime.utcnow()
        
        # Aggregate by hour
        for metric_type, metrics in self.metrics_store.items():
            hourly_key = f"{metric_type}_{current_time.strftime('%Y%m%d_%H')}"
            
            if hourly_key not in self.aggregated_metrics:
                hour_start = current_time.replace(minute=0, second=0, microsecond=0)
                hour_metrics = [
                    m for m in metrics
                    if datetime.fromisoformat(m["timestamp"]) >= hour_start
                ]
                
                if hour_metrics:
                    values = [m["value"] for m in hour_metrics]
                    self.aggregated_metrics[hourly_key] = {
                        "count": len(values),
                        "sum": sum(values),
                        "average": sum(values) / len(values),
                        "min": min(values),
                        "max": max(values),
                        "hour": hour_start.isoformat()
                    }
    
    def _cleanup_old_metrics(self, retention_hours: int = 24):
        """Cleanup metrics older than retention period"""
        
        cutoff_time = datetime.utcnow() - timedelta(hours=retention_hours)
        
        for metric_type in list(self.metrics_store.keys()):
            original_count = len(self.metrics_store[metric_type])
            
            self.metrics_store[metric_type] = [
                m for m in self.metrics_store[metric_type]
                if datetime.fromisoformat(m["timestamp"]) > cutoff_time
            ]
            
            cleaned_count = original_count - len(self.metrics_store[metric_type])
            if cleaned_count > 0:
                logger.debug(f"Cleaned {cleaned_count} old metrics for {metric_type}")
    
    def _calculate_orders_per_minute(self) -> float:
        """Calculate orders per minute"""
        
        one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
        
        recent_orders = [
            m for m in self.metrics_store.get("processing_time", [])
            if datetime.fromisoformat(m["timestamp"]) > one_minute_ago
        ]
        
        return len(recent_orders)
    
    def _calculate_revenue_per_hour(self) -> float:
        """Calculate revenue per hour"""
        
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        
        recent_revenue = [
            m["value"] for m in self.metrics_store.get("order_value", [])
            if datetime.fromisoformat(m["timestamp"]) > one_hour_ago
        ]
        
        return sum(recent_revenue)
    
    def _calculate_satisfaction_score(self) -> float:
        """Calculate customer satisfaction score"""
        
        # Placeholder - would calculate from actual satisfaction metrics
        return 8.5
    
    def _export_as_csv(self) -> str:
        """Export metrics as CSV format"""
        
        csv_lines = ["timestamp,metric_type,value,order_id"]
        
        for metric_type, metrics in self.metrics_store.items():
            for metric in metrics:
                line = f"{metric['timestamp']},{metric_type},{metric['value']},{metric.get('order_id', '')}"
                csv_lines.append(line)
        
        return "\n".join(csv_lines)