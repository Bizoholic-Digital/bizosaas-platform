#!/usr/bin/env python3

"""
Monitoring Service for SQLAdmin Dashboard
Real-time metrics collection and analysis for BizOSaaS infrastructure
"""

import asyncio
import psutil
import time
import aioredis
import psycopg2
import httpx
import docker
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import create_engine, text
from dataclasses import dataclass
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MonitoringConfig:
    """Configuration for monitoring service"""
    database_url: str
    redis_url: str
    collection_interval: int = 60  # seconds
    retention_days: int = 30
    alert_thresholds: Dict[str, float] = None
    enabled_collectors: List[str] = None

class MetricsCollector:
    """Base class for metrics collectors"""
    
    def __init__(self, config: MonitoringConfig, db_session: async_sessionmaker):
        self.config = config
        self.db_session = db_session
        self.is_running = False
    
    async def collect(self) -> Dict[str, Any]:
        """Collect metrics - to be implemented by subclasses"""
        raise NotImplementedError
    
    async def store_metrics(self, metrics: Dict[str, Any], table_name: str):
        """Store metrics in database"""
        try:
            async with self.db_session() as session:
                # Build insert query dynamically based on metrics
                columns = list(metrics.keys())
                values = list(metrics.values())
                placeholders = [f"${i+1}" for i in range(len(values))]
                
                query = f"""
                INSERT INTO {table_name} ({', '.join(columns)})
                VALUES ({', '.join(placeholders)})
                """
                
                await session.execute(text(query), values)
                await session.commit()
                
        except Exception as e:
            logger.error(f"Failed to store metrics for {table_name}: {e}")

class DatabaseMetricsCollector(MetricsCollector):
    """Collect PostgreSQL database metrics"""
    
    async def collect(self) -> Dict[str, Any]:
        """Collect database health metrics"""
        try:
            async with self.db_session() as session:
                # Connection statistics
                conn_stats = await session.execute(text("""
                    SELECT 
                        count(*) as total_connections,
                        count(*) FILTER (WHERE state = 'active') as active_connections,
                        count(*) FILTER (WHERE state = 'idle') as idle_connections
                    FROM pg_stat_activity 
                    WHERE datname = current_database()
                """))
                conn_data = conn_stats.fetchone()
                
                # Database size
                db_size = await session.execute(text("""
                    SELECT pg_database_size(current_database()) / (1024*1024) as size_mb
                """))
                size_data = db_size.fetchone()
                
                # Cache hit ratio
                cache_hit = await session.execute(text("""
                    SELECT 
                        CASE 
                            WHEN (blks_hit + blks_read) = 0 THEN 0
                            ELSE round(blks_hit::numeric / (blks_hit + blks_read) * 100, 2)
                        END as cache_hit_ratio
                    FROM pg_stat_database 
                    WHERE datname = current_database()
                """))
                cache_data = cache_hit.fetchone()
                
                # Slow queries (queries taking > 1 second)
                slow_queries = await session.execute(text("""
                    SELECT count(*) as slow_query_count
                    FROM pg_stat_statements 
                    WHERE mean_exec_time > 1000
                """))
                slow_data = slow_queries.fetchone() if slow_queries else (0,)
                
                # System metrics
                cpu_percent = psutil.cpu_percent()
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                metrics = {
                    'timestamp': datetime.now(timezone.utc),
                    'active_connections': conn_data[1] if conn_data else 0,
                    'total_connections': conn_data[0] if conn_data else 0,
                    'max_connections': 100,  # Default, could be queried from pg_settings
                    'idle_connections': conn_data[2] if conn_data else 0,
                    'database_size_mb': int(size_data[0]) if size_data else 0,
                    'cache_hit_ratio': float(cache_data[0]) if cache_data else 0.0,
                    'slow_query_count': slow_data[0] if slow_data else 0,
                    'deadlock_count': 0,  # Would need pg_stat_database
                    'cpu_usage_percent': cpu_percent,
                    'memory_usage_percent': memory.percent,
                    'disk_usage_percent': disk.percent
                }
                
                await self.store_metrics(metrics, 'database_health_metrics')
                return metrics
                
        except Exception as e:
            logger.error(f"Failed to collect database metrics: {e}")
            return {}

class RedisMetricsCollector(MetricsCollector):
    """Collect Redis cache metrics"""
    
    def __init__(self, config: MonitoringConfig, db_session: async_sessionmaker):
        super().__init__(config, db_session)
        self.redis_client = None
    
    async def _get_redis_client(self):
        """Get Redis client connection"""
        if not self.redis_client:
            try:
                self.redis_client = await aioredis.from_url(
                    self.config.redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                return None
        return self.redis_client
    
    async def collect(self) -> Dict[str, Any]:
        """Collect Redis health metrics"""
        try:
            redis = await self._get_redis_client()
            if not redis:
                return {}
            
            # Get Redis info
            info = await redis.info()
            
            # Calculate hit rate
            keyspace_hits = info.get('keyspace_hits', 0)
            keyspace_misses = info.get('keyspace_misses', 0)
            total_ops = keyspace_hits + keyspace_misses
            hit_rate = (keyspace_hits / total_ops * 100) if total_ops > 0 else 0
            
            # Get memory info
            used_memory = info.get('used_memory', 0)
            used_memory_peak = info.get('used_memory_peak', 0)
            
            # Get client info
            connected_clients = info.get('connected_clients', 0)
            blocked_clients = info.get('blocked_clients', 0)
            
            # Calculate total keys across all databases
            total_keys = 0
            for key, value in info.items():
                if key.startswith('db') and isinstance(value, dict):
                    total_keys += value.get('keys', 0)
            
            metrics = {
                'timestamp': datetime.now(timezone.utc),
                'connected_clients': connected_clients,
                'blocked_clients': blocked_clients,
                'used_memory_mb': used_memory // (1024 * 1024),
                'used_memory_peak_mb': used_memory_peak // (1024 * 1024),
                'memory_usage_percent': (used_memory / used_memory_peak * 100) if used_memory_peak > 0 else 0,
                'keyspace_hits': keyspace_hits,
                'keyspace_misses': keyspace_misses,
                'hit_rate_percent': hit_rate,
                'evicted_keys': info.get('evicted_keys', 0),
                'expired_keys': info.get('expired_keys', 0),
                'total_keys': total_keys,
                'operations_per_second': info.get('instantaneous_ops_per_sec', 0),
                'network_input_mb': info.get('total_net_input_bytes', 0) / (1024 * 1024),
                'network_output_mb': info.get('total_net_output_bytes', 0) / (1024 * 1024),
                'cpu_usage_percent': info.get('used_cpu_sys', 0) + info.get('used_cpu_user', 0)
            }
            
            await self.store_metrics(metrics, 'redis_health_metrics')
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect Redis metrics: {e}")
            return {}

class ContainerMetricsCollector(MetricsCollector):
    """Collect Docker container metrics"""
    
    def __init__(self, config: MonitoringConfig, db_session: async_sessionmaker):
        super().__init__(config, db_session)
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            self.docker_client = None
    
    async def collect(self) -> Dict[str, Any]:
        """Collect container metrics"""
        if not self.docker_client:
            return {}
        
        try:
            containers = self.docker_client.containers.list(all=True)
            all_metrics = []
            
            for container in containers:
                try:
                    # Get container stats
                    stats = container.stats(stream=False)
                    
                    # Calculate CPU usage
                    cpu_percent = 0
                    if 'cpu_stats' in stats and 'precpu_stats' in stats:
                        cpu_stats = stats['cpu_stats']
                        precpu_stats = stats['precpu_stats']
                        
                        cpu_delta = cpu_stats['cpu_usage']['total_usage'] - precpu_stats['cpu_usage']['total_usage']
                        system_delta = cpu_stats['system_cpu_usage'] - precpu_stats['system_cpu_usage']
                        
                        if system_delta > 0 and cpu_delta > 0:
                            cpu_percent = (cpu_delta / system_delta) * len(cpu_stats['cpu_usage']['percpu_usage']) * 100
                    
                    # Calculate memory usage
                    memory_usage = stats.get('memory_stats', {}).get('usage', 0)
                    memory_limit = stats.get('memory_stats', {}).get('limit', 0)
                    memory_percent = (memory_usage / memory_limit * 100) if memory_limit > 0 else 0
                    
                    # Network stats
                    networks = stats.get('networks', {})
                    rx_bytes = sum(net.get('rx_bytes', 0) for net in networks.values())
                    tx_bytes = sum(net.get('tx_bytes', 0) for net in networks.values())
                    
                    # Block IO stats
                    blkio_stats = stats.get('blkio_stats', {})
                    read_bytes = sum(stat.get('value', 0) for stat in blkio_stats.get('io_service_bytes_recursive', []) if stat.get('op') == 'Read')
                    write_bytes = sum(stat.get('value', 0) for stat in blkio_stats.get('io_service_bytes_recursive', []) if stat.get('op') == 'Write')
                    
                    metrics = {
                        'timestamp': datetime.now(timezone.utc),
                        'container_name': container.name,
                        'container_id': container.id[:12],
                        'status': container.status,
                        'cpu_usage_percent': round(cpu_percent, 2),
                        'memory_usage_mb': memory_usage / (1024 * 1024),
                        'memory_limit_mb': memory_limit / (1024 * 1024),
                        'memory_usage_percent': round(memory_percent, 2),
                        'network_rx_mb': rx_bytes / (1024 * 1024),
                        'network_tx_mb': tx_bytes / (1024 * 1024),
                        'disk_read_mb': read_bytes / (1024 * 1024),
                        'disk_write_mb': write_bytes / (1024 * 1024),
                        'restart_count': container.attrs.get('RestartCount', 0),
                        'uptime_seconds': int(time.time() - container.attrs.get('State', {}).get('StartedAt', time.time())),
                        'health_status': container.attrs.get('State', {}).get('Health', {}).get('Status', 'unknown')
                    }
                    
                    await self.store_metrics(metrics, 'container_metrics')
                    all_metrics.append(metrics)
                    
                except Exception as e:
                    logger.error(f"Failed to collect metrics for container {container.name}: {e}")
            
            return {'containers': all_metrics}
            
        except Exception as e:
            logger.error(f"Failed to collect container metrics: {e}")
            return {}

class APIEndpointMetricsCollector(MetricsCollector):
    """Collect API endpoint performance metrics"""
    
    def __init__(self, config: MonitoringConfig, db_session: async_sessionmaker):
        super().__init__(config, db_session)
        self.endpoints_to_monitor = [
            {'url': 'http://localhost:3002/api/health', 'service': 'unified-auth'},
            {'url': 'http://localhost:3001/api/health', 'service': 'tailadmin'},
            {'url': 'http://localhost:5000/api/system/health', 'service': 'sqladmin'},
        ]
    
    async def collect(self) -> Dict[str, Any]:
        """Collect API endpoint metrics"""
        all_metrics = []
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            for endpoint in self.endpoints_to_monitor:
                try:
                    start_time = time.time()
                    response = await client.get(endpoint['url'])
                    response_time = int((time.time() - start_time) * 1000)
                    
                    metrics = {
                        'timestamp': datetime.now(timezone.utc),
                        'endpoint_url': endpoint['url'],
                        'method': 'GET',
                        'service_name': endpoint['service'],
                        'response_time_ms': response_time,
                        'status_code': response.status_code,
                        'success_count': 1 if response.status_code < 400 else 0,
                        'error_count': 1 if response.status_code >= 400 else 0,
                        'total_requests': 1,
                        'average_response_time': float(response_time),
                        'error_rate_percent': 100.0 if response.status_code >= 400 else 0.0
                    }
                    
                    await self.store_metrics(metrics, 'api_endpoint_metrics')
                    all_metrics.append(metrics)
                    
                except Exception as e:
                    logger.error(f"Failed to monitor endpoint {endpoint['url']}: {e}")
                    
                    # Record failure
                    metrics = {
                        'timestamp': datetime.now(timezone.utc),
                        'endpoint_url': endpoint['url'],
                        'method': 'GET',
                        'service_name': endpoint['service'],
                        'response_time_ms': 0,
                        'status_code': 0,
                        'success_count': 0,
                        'error_count': 1,
                        'total_requests': 1,
                        'average_response_time': 0.0,
                        'error_rate_percent': 100.0
                    }
                    
                    await self.store_metrics(metrics, 'api_endpoint_metrics')
                    all_metrics.append(metrics)
        
        return {'endpoints': all_metrics}

class AlertManager:
    """Manage system alerts based on metrics"""
    
    def __init__(self, config: MonitoringConfig, db_session: async_sessionmaker):
        self.config = config
        self.db_session = db_session
        self.alert_thresholds = config.alert_thresholds or {
            'cpu_usage_warning': 80.0,
            'cpu_usage_critical': 95.0,
            'memory_usage_warning': 85.0,
            'memory_usage_critical': 95.0,
            'response_time_warning': 2000,  # ms
            'response_time_critical': 5000,  # ms
            'error_rate_warning': 5.0,  # percent
            'error_rate_critical': 10.0,  # percent
            'cache_hit_rate_warning': 80.0,  # percent
        }
    
    async def check_database_alerts(self, metrics: Dict[str, Any]):
        """Check for database-related alerts"""
        if not metrics:
            return
        
        alerts = []
        
        # CPU usage alerts
        cpu_usage = metrics.get('cpu_usage_percent', 0)
        if cpu_usage > self.alert_thresholds['cpu_usage_critical']:
            alerts.append({
                'alert_type': 'performance',
                'severity': 'critical',
                'title': 'Critical Database CPU Usage',
                'description': f'Database CPU usage is at {cpu_usage:.1f}%',
                'current_value': cpu_usage,
                'threshold_value': self.alert_thresholds['cpu_usage_critical'],
                'source_service': 'postgresql'
            })
        elif cpu_usage > self.alert_thresholds['cpu_usage_warning']:
            alerts.append({
                'alert_type': 'performance',
                'severity': 'warning',
                'title': 'High Database CPU Usage',
                'description': f'Database CPU usage is at {cpu_usage:.1f}%',
                'current_value': cpu_usage,
                'threshold_value': self.alert_thresholds['cpu_usage_warning'],
                'source_service': 'postgresql'
            })
        
        # Memory usage alerts
        memory_usage = metrics.get('memory_usage_percent', 0)
        if memory_usage > self.alert_thresholds['memory_usage_critical']:
            alerts.append({
                'alert_type': 'performance',
                'severity': 'critical',
                'title': 'Critical Database Memory Usage',
                'description': f'Database memory usage is at {memory_usage:.1f}%',
                'current_value': memory_usage,
                'threshold_value': self.alert_thresholds['memory_usage_critical'],
                'source_service': 'postgresql'
            })
        
        # Cache hit rate alerts
        cache_hit_ratio = metrics.get('cache_hit_ratio', 100)
        if cache_hit_ratio < self.alert_thresholds['cache_hit_rate_warning']:
            alerts.append({
                'alert_type': 'performance',
                'severity': 'warning',
                'title': 'Low Database Cache Hit Rate',
                'description': f'Database cache hit rate is at {cache_hit_ratio:.1f}%',
                'current_value': cache_hit_ratio,
                'threshold_value': self.alert_thresholds['cache_hit_rate_warning'],
                'source_service': 'postgresql'
            })
        
        # Store alerts
        for alert in alerts:
            await self.create_alert(alert)
    
    async def check_api_alerts(self, metrics: Dict[str, Any]):
        """Check for API-related alerts"""
        endpoints = metrics.get('endpoints', [])
        
        for endpoint_metric in endpoints:
            alerts = []
            
            # Response time alerts
            response_time = endpoint_metric.get('response_time_ms', 0)
            if response_time > self.alert_thresholds['response_time_critical']:
                alerts.append({
                    'alert_type': 'performance',
                    'severity': 'critical',
                    'title': 'Critical API Response Time',
                    'description': f"API {endpoint_metric['service_name']} response time is {response_time}ms",
                    'current_value': response_time,
                    'threshold_value': self.alert_thresholds['response_time_critical'],
                    'source_service': endpoint_metric['service_name']
                })
            
            # Error rate alerts
            error_rate = endpoint_metric.get('error_rate_percent', 0)
            if error_rate > self.alert_thresholds['error_rate_critical']:
                alerts.append({
                    'alert_type': 'performance',
                    'severity': 'critical',
                    'title': 'Critical API Error Rate',
                    'description': f"API {endpoint_metric['service_name']} error rate is {error_rate:.1f}%",
                    'current_value': error_rate,
                    'threshold_value': self.alert_thresholds['error_rate_critical'],
                    'source_service': endpoint_metric['service_name']
                })
            
            # Store alerts
            for alert in alerts:
                await self.create_alert(alert)
    
    async def create_alert(self, alert_data: Dict[str, Any]):
        """Create a new system alert"""
        try:
            async with self.db_session() as session:
                # Check if similar alert already exists and is active
                existing_alert = await session.execute(text("""
                    SELECT id FROM system_alerts 
                    WHERE alert_type = :alert_type 
                    AND source_service = :source_service 
                    AND is_active = true 
                    AND created_at > NOW() - INTERVAL '1 hour'
                """), {
                    'alert_type': alert_data['alert_type'],
                    'source_service': alert_data['source_service']
                })
                
                if existing_alert.fetchone():
                    return  # Don't create duplicate alerts
                
                # Create new alert
                await session.execute(text("""
                    INSERT INTO system_alerts (
                        alert_type, severity, title, description, source_service,
                        current_value, threshold_value, alert_data
                    ) VALUES (
                        :alert_type, :severity, :title, :description, :source_service,
                        :current_value, :threshold_value, :alert_data
                    )
                """), {
                    **alert_data,
                    'alert_data': json.dumps(alert_data)
                })
                
                await session.commit()
                logger.info(f"Created alert: {alert_data['title']}")
                
        except Exception as e:
            logger.error(f"Failed to create alert: {e}")

class MonitoringService:
    """Main monitoring service coordinator"""
    
    def __init__(self, config: MonitoringConfig):
        self.config = config
        self.engine = create_engine(config.database_url.replace('+asyncpg', ''))
        self.async_engine = create_async_engine(config.database_url)
        self.db_session = async_sessionmaker(self.async_engine, expire_on_commit=False)
        
        # Initialize collectors
        self.collectors = []
        if 'database' in config.enabled_collectors:
            self.collectors.append(DatabaseMetricsCollector(config, self.db_session))
        if 'redis' in config.enabled_collectors:
            self.collectors.append(RedisMetricsCollector(config, self.db_session))
        if 'containers' in config.enabled_collectors:
            self.collectors.append(ContainerMetricsCollector(config, self.db_session))
        if 'api_endpoints' in config.enabled_collectors:
            self.collectors.append(APIEndpointMetricsCollector(config, self.db_session))
        
        # Initialize alert manager
        self.alert_manager = AlertManager(config, self.db_session)
        
        self.is_running = False
    
    async def start(self):
        """Start the monitoring service"""
        self.is_running = True
        logger.info("Starting monitoring service...")
        
        while self.is_running:
            try:
                # Collect metrics from all collectors
                tasks = [collector.collect() for collector in self.collectors]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results and check for alerts
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        logger.error(f"Collector {i} failed: {result}")
                        continue
                    
                    if not result:
                        continue
                    
                    # Check for alerts based on metrics
                    collector = self.collectors[i]
                    if isinstance(collector, DatabaseMetricsCollector):
                        await self.alert_manager.check_database_alerts(result)
                    elif isinstance(collector, APIEndpointMetricsCollector):
                        await self.alert_manager.check_api_alerts(result)
                
                logger.info("Metrics collection cycle completed")
                
                # Wait for next collection interval
                await asyncio.sleep(self.config.collection_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring service: {e}")
                await asyncio.sleep(self.config.collection_interval)
    
    async def stop(self):
        """Stop the monitoring service"""
        self.is_running = False
        logger.info("Monitoring service stopped")
    
    async def cleanup_old_metrics(self):
        """Clean up old metrics data"""
        try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=self.config.retention_days)
            
            tables_to_cleanup = [
                'database_health_metrics',
                'redis_health_metrics',
                'container_metrics',
                'api_endpoint_metrics',
                'user_session_analytics',
                'authentication_logs'
            ]
            
            async with self.db_session() as session:
                for table in tables_to_cleanup:
                    result = await session.execute(text(f"""
                        DELETE FROM {table} 
                        WHERE timestamp < :cutoff_date
                    """), {'cutoff_date': cutoff_date})
                    
                    deleted_count = result.rowcount
                    if deleted_count > 0:
                        logger.info(f"Cleaned up {deleted_count} old records from {table}")
                
                await session.commit()
                
        except Exception as e:
            logger.error(f"Failed to cleanup old metrics: {e}")

# ============================================================================
# CONFIGURATION AND STARTUP
# ============================================================================

def create_monitoring_config() -> MonitoringConfig:
    """Create monitoring configuration from environment variables"""
    return MonitoringConfig(
        database_url=os.getenv("DATABASE_URL", "postgresql+asyncpg://bizosaas:bizosaas@localhost:5432/bizosaas"),
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        collection_interval=int(os.getenv("MONITORING_INTERVAL", "60")),
        retention_days=int(os.getenv("MONITORING_RETENTION_DAYS", "30")),
        alert_thresholds={
            'cpu_usage_warning': float(os.getenv("CPU_WARNING_THRESHOLD", "80.0")),
            'cpu_usage_critical': float(os.getenv("CPU_CRITICAL_THRESHOLD", "95.0")),
            'memory_usage_warning': float(os.getenv("MEMORY_WARNING_THRESHOLD", "85.0")),
            'memory_usage_critical': float(os.getenv("MEMORY_CRITICAL_THRESHOLD", "95.0")),
            'response_time_warning': float(os.getenv("RESPONSE_TIME_WARNING", "2000")),
            'response_time_critical': float(os.getenv("RESPONSE_TIME_CRITICAL", "5000")),
            'error_rate_warning': float(os.getenv("ERROR_RATE_WARNING", "5.0")),
            'error_rate_critical': float(os.getenv("ERROR_RATE_CRITICAL", "10.0")),
            'cache_hit_rate_warning': float(os.getenv("CACHE_HIT_RATE_WARNING", "80.0")),
        },
        enabled_collectors=os.getenv("ENABLED_COLLECTORS", "database,redis,containers,api_endpoints").split(",")
    )

async def main():
    """Main entry point for monitoring service"""
    config = create_monitoring_config()
    service = MonitoringService(config)
    
    try:
        # Start monitoring service
        await service.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    finally:
        await service.stop()

if __name__ == "__main__":
    asyncio.run(main())