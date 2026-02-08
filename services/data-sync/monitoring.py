#!/usr/bin/env python3

"""
BizOSaaS Data Synchronization - Monitoring Module
Real-time monitoring and alerting for data synchronization
"""

import asyncio
import logging
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

import redis.asyncio as redis
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class AlertLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    RATE = "rate"

@dataclass
class SyncMetric:
    name: str
    type: MetricType
    value: float
    labels: Dict[str, str]
    timestamp: datetime
    description: str

@dataclass
class Alert:
    id: str
    level: AlertLevel
    title: str
    message: str
    metric_name: str
    threshold_value: float
    current_value: float
    platform: str
    tenant_id: Optional[str]
    created_at: datetime
    resolved_at: Optional[datetime] = None

class SyncMonitor:
    """Monitors data synchronization performance and health"""
    
    def __init__(self, redis_client, db_pool):
        self.redis_client = redis_client
        self.db_pool = db_pool
        self.metrics = {}
        self.alert_rules = self._load_alert_rules()
        self.running = False
        
    def _load_alert_rules(self) -> Dict[str, Any]:
        """Load alerting rules and thresholds"""
        return {
            "sync_failure_rate": {
                "threshold": 0.05,  # 5% failure rate
                "level": AlertLevel.WARNING,
                "window_minutes": 15,
                "description": "Sync failure rate exceeds threshold"
            },
            "sync_latency_p95": {
                "threshold": 5000,  # 5 seconds
                "level": AlertLevel.WARNING,
                "window_minutes": 10,
                "description": "95th percentile sync latency too high"
            },
            "queue_depth": {
                "threshold": 1000,  # 1000 pending events
                "level": AlertLevel.ERROR,
                "window_minutes": 5,
                "description": "Sync queue depth too high"
            },
            "platform_health": {
                "threshold": 0.95,  # 95% health score
                "level": AlertLevel.CRITICAL,
                "window_minutes": 5,
                "description": "Platform health score below threshold"
            },
            "error_rate": {
                "threshold": 0.10,  # 10% error rate
                "level": AlertLevel.ERROR,
                "window_minutes": 10,
                "description": "Error rate exceeds threshold"
            },
            "processing_time": {
                "threshold": 10000,  # 10 seconds
                "level": AlertLevel.WARNING,
                "window_minutes": 15,
                "description": "Average processing time too high"
            }
        }
    
    async def start(self):
        """Start monitoring"""
        self.running = True
        logger.info("🚀 Starting Sync Monitor...")
        
        # Start monitoring tasks
        asyncio.create_task(self._collect_metrics())
        asyncio.create_task(self._evaluate_alerts())
        asyncio.create_task(self._cleanup_old_data())
        
        logger.info("✅ Sync Monitor started successfully")
    
    async def stop(self):
        """Stop monitoring"""
        self.running = False
        logger.info("🔄 Stopping Sync Monitor...")
    
    async def record_metric(self, metric: SyncMetric):
        """Record a synchronization metric"""
        try:
            # Store in Redis for real-time access
            metric_key = f"metrics:{metric.name}:{metric.timestamp.strftime('%Y%m%d_%H%M')}"
            metric_data = {
                "type": metric.type.value,
                "value": metric.value,
                "labels": metric.labels,
                "timestamp": metric.timestamp.isoformat(),
                "description": metric.description
            }
            
            await self.redis_client.setex(metric_key, 3600, json.dumps(metric_data))  # 1 hour TTL
            
            # Store in database for historical analysis
            await self._store_metric_in_db(metric)
            
            # Update in-memory cache
            self.metrics[metric.name] = metric
            
            logger.debug(f"📊 Recorded metric: {metric.name} = {metric.value}")
            
        except Exception as e:
            logger.error(f"❌ Failed to record metric {metric.name}: {e}")
    
    async def get_metrics(self, 
                         metric_names: Optional[List[str]] = None,
                         start_time: Optional[datetime] = None,
                         end_time: Optional[datetime] = None,
                         platform: Optional[str] = None,
                         tenant_id: Optional[str] = None) -> List[SyncMetric]:
        """Get metrics with filtering"""
        try:
            conditions = []
            params = []
            param_count = 0
            
            if metric_names:
                param_count += 1
                conditions.append(f"metric_name = ANY(${param_count})")
                params.append(metric_names)
            
            if start_time:
                param_count += 1
                conditions.append(f"timestamp >= ${param_count}")
                params.append(start_time)
            
            if end_time:
                param_count += 1
                conditions.append(f"timestamp <= ${param_count}")
                params.append(end_time)
            
            if platform:
                param_count += 1
                conditions.append(f"labels->>'platform' = ${param_count}")
                params.append(platform)
            
            if tenant_id:
                param_count += 1
                conditions.append(f"labels->>'tenant_id' = ${param_count}")
                params.append(tenant_id)
            
            where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
            
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(f"""
                    SELECT * FROM sync_metrics 
                    {where_clause}
                    ORDER BY timestamp DESC
                    LIMIT 1000
                """, *params)
                
                metrics = []
                for row in rows:
                    metric = SyncMetric(
                        name=row['metric_name'],
                        type=MetricType(row['metric_type']),
                        value=row['value'],
                        labels=row['labels'],
                        timestamp=row['timestamp'],
                        description=row['description']
                    )
                    metrics.append(metric)
                
                return metrics
                
        except Exception as e:
            logger.error(f"❌ Failed to get metrics: {e}")
            return []
    
    async def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Get metrics for monitoring dashboard"""
        try:
            # Get current metrics from last hour
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(hours=1)
            
            async with self.db_pool.acquire() as conn:
                # Sync success rate
                sync_stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(*) as total_syncs,
                        COUNT(CASE WHEN labels->>'status' = 'completed' THEN 1 END) as successful_syncs,
                        COUNT(CASE WHEN labels->>'status' = 'failed' THEN 1 END) as failed_syncs,
                        AVG(CASE WHEN metric_name = 'sync_processing_time' THEN value END) as avg_processing_time
                    FROM sync_metrics 
                    WHERE timestamp >= $1 AND timestamp <= $2
                    AND metric_name IN ('sync_event_processed', 'sync_processing_time')
                """, start_time, end_time)
                
                # Platform health
                platform_health = await conn.fetch("""
                    SELECT 
                        labels->>'platform' as platform,
                        AVG(value) as health_score
                    FROM sync_metrics 
                    WHERE timestamp >= $1 AND timestamp <= $2
                    AND metric_name = 'platform_health_score'
                    GROUP BY labels->>'platform'
                """, start_time, end_time)
                
                # Queue depths
                queue_depths = await conn.fetch("""
                    SELECT 
                        labels->>'queue' as queue_name,
                        MAX(value) as max_depth,
                        AVG(value) as avg_depth
                    FROM sync_metrics 
                    WHERE timestamp >= $1 AND timestamp <= $2
                    AND metric_name = 'queue_depth'
                    GROUP BY labels->>'queue'
                """, start_time, end_time)
                
                # Error rates
                error_stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(CASE WHEN metric_name = 'sync_error' THEN 1 END) as total_errors,
                        COUNT(CASE WHEN metric_name = 'sync_error' AND labels->>'level' = 'critical' THEN 1 END) as critical_errors
                    FROM sync_metrics 
                    WHERE timestamp >= $1 AND timestamp <= $2
                """, start_time, end_time)
                
                # Active alerts
                active_alerts = await conn.fetch("""
                    SELECT * FROM sync_alerts 
                    WHERE resolved_at IS NULL
                    ORDER BY created_at DESC
                """)
                
                total_syncs = sync_stats['total_syncs'] or 0
                success_rate = (sync_stats['successful_syncs'] or 0) / max(total_syncs, 1) * 100
                failure_rate = (sync_stats['failed_syncs'] or 0) / max(total_syncs, 1) * 100
                
                return {
                    "overview": {
                        "total_syncs": total_syncs,
                        "success_rate": round(success_rate, 2),
                        "failure_rate": round(failure_rate, 2),
                        "avg_processing_time_ms": sync_stats['avg_processing_time'] or 0,
                        "total_errors": error_stats['total_errors'] or 0,
                        "critical_errors": error_stats['critical_errors'] or 0
                    },
                    "platform_health": [
                        {
                            "platform": row['platform'],
                            "health_score": round(row['health_score'], 2)
                        }
                        for row in platform_health
                    ],
                    "queue_status": [
                        {
                            "queue": row['queue_name'],
                            "max_depth": row['max_depth'],
                            "avg_depth": round(row['avg_depth'], 2)
                        }
                        for row in queue_depths
                    ],
                    "active_alerts": [
                        {
                            "id": row['id'],
                            "level": row['level'],
                            "title": row['title'],
                            "platform": row['platform'],
                            "created_at": row['created_at'].isoformat()
                        }
                        for row in active_alerts
                    ],
                    "timestamp": end_time.isoformat()
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get dashboard metrics: {e}")
            return {"error": str(e)}
    
    async def create_alert(self, alert: Alert):
        """Create a new alert"""
        try:
            # Store in database
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO sync_alerts (
                        id, level, title, message, metric_name, threshold_value,
                        current_value, platform, tenant_id, created_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                """, alert.id, alert.level.value, alert.title, alert.message,
                alert.metric_name, alert.threshold_value, alert.current_value,
                alert.platform, alert.tenant_id, alert.created_at)
            
            # Store in Redis for real-time notifications
            alert_data = {
                "id": alert.id,
                "level": alert.level.value,
                "title": alert.title,
                "message": alert.message,
                "platform": alert.platform,
                "created_at": alert.created_at.isoformat()
            }
            
            await self.redis_client.lpush("alerts:active", json.dumps(alert_data))
            await self.redis_client.publish("alerts:new", json.dumps(alert_data))
            
            logger.warning(f"🚨 Alert created: {alert.title} ({alert.level.value})")
            
        except Exception as e:
            logger.error(f"❌ Failed to create alert: {e}")
    
    async def resolve_alert(self, alert_id: str, resolution_note: str = ""):
        """Resolve an alert"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE sync_alerts 
                    SET resolved_at = NOW(), resolution_note = $2
                    WHERE id = $1 AND resolved_at IS NULL
                """, alert_id, resolution_note)
            
            # Remove from Redis active alerts
            alert_data = {"id": alert_id, "resolved_at": datetime.now(timezone.utc).isoformat()}
            await self.redis_client.publish("alerts:resolved", json.dumps(alert_data))
            
            logger.info(f"✅ Alert resolved: {alert_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to resolve alert: {e}")
    
    async def _collect_metrics(self):
        """Collect system metrics periodically"""
        while self.running:
            try:
                await asyncio.sleep(60)  # Collect every minute
                
                # Collect queue depths
                await self._collect_queue_metrics()
                
                # Collect performance metrics
                await self._collect_performance_metrics()
                
                # Collect platform health metrics
                await self._collect_platform_health()
                
                # Collect error metrics
                await self._collect_error_metrics()
                
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
    
    async def _collect_queue_metrics(self):
        """Collect queue depth and processing metrics"""
        try:
            queues = ["events:critical", "events:high", "events:normal", "events:low"]
            
            for queue in queues:
                depth = await self.redis_client.llen(queue)
                
                metric = SyncMetric(
                    name="queue_depth",
                    type=MetricType.GAUGE,
                    value=float(depth),
                    labels={"queue": queue},
                    timestamp=datetime.now(timezone.utc),
                    description=f"Depth of {queue} queue"
                )
                
                await self.record_metric(metric)
                
        except Exception as e:
            logger.error(f"Error collecting queue metrics: {e}")
    
    async def _collect_performance_metrics(self):
        """Collect processing performance metrics"""
        try:
            # Get recent sync events from database
            async with self.db_pool.acquire() as conn:
                stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(*) as total_events,
                        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_events,
                        COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_events,
                        AVG(processing_time_ms) as avg_processing_time,
                        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY processing_time_ms) as p95_processing_time
                    FROM sync_events 
                    WHERE created_at >= NOW() - INTERVAL '5 minutes'
                """)
                
                if stats['total_events']:
                    # Success rate
                    success_rate = stats['completed_events'] / stats['total_events']
                    failure_rate = stats['failed_events'] / stats['total_events']
                    
                    metrics = [
                        SyncMetric(
                            name="sync_success_rate",
                            type=MetricType.RATE,
                            value=success_rate,
                            labels={"window": "5m"},
                            timestamp=datetime.now(timezone.utc),
                            description="Sync success rate over 5 minutes"
                        ),
                        SyncMetric(
                            name="sync_failure_rate",
                            type=MetricType.RATE,
                            value=failure_rate,
                            labels={"window": "5m"},
                            timestamp=datetime.now(timezone.utc),
                            description="Sync failure rate over 5 minutes"
                        ),
                        SyncMetric(
                            name="sync_processing_time_avg",
                            type=MetricType.GAUGE,
                            value=float(stats['avg_processing_time'] or 0),
                            labels={"window": "5m"},
                            timestamp=datetime.now(timezone.utc),
                            description="Average sync processing time"
                        ),
                        SyncMetric(
                            name="sync_processing_time_p95",
                            type=MetricType.GAUGE,
                            value=float(stats['p95_processing_time'] or 0),
                            labels={"window": "5m"},
                            timestamp=datetime.now(timezone.utc),
                            description="95th percentile sync processing time"
                        )
                    ]
                    
                    for metric in metrics:
                        await self.record_metric(metric)
                        
        except Exception as e:
            logger.error(f"Error collecting performance metrics: {e}")
    
    async def _collect_platform_health(self):
        """Collect platform health metrics"""
        try:
            platforms = ["bizoholic", "coreldove", "bizosaas"]
            
            for platform in platforms:
                # Check platform status from database
                async with self.db_pool.acquire() as conn:
                    status = await conn.fetchrow("""
                        SELECT status, last_seen FROM platform_status 
                        WHERE platform = $1
                    """, platform)
                    
                    if status:
                        # Calculate health score based on last_seen and status
                        last_seen = status['last_seen']
                        if last_seen:
                            time_diff = (datetime.now(timezone.utc) - last_seen).total_seconds()
                            
                            if time_diff < 60:  # Less than 1 minute
                                health_score = 1.0
                            elif time_diff < 300:  # Less than 5 minutes
                                health_score = 0.8
                            elif time_diff < 900:  # Less than 15 minutes
                                health_score = 0.5
                            else:
                                health_score = 0.0
                            
                            if status['status'] != 'healthy':
                                health_score *= 0.5
                        else:
                            health_score = 0.0
                        
                        metric = SyncMetric(
                            name="platform_health_score",
                            type=MetricType.GAUGE,
                            value=health_score,
                            labels={"platform": platform},
                            timestamp=datetime.now(timezone.utc),
                            description=f"Health score for {platform} platform"
                        )
                        
                        await self.record_metric(metric)
                        
        except Exception as e:
            logger.error(f"Error collecting platform health: {e}")
    
    async def _collect_error_metrics(self):
        """Collect error and exception metrics"""
        try:
            # Get recent errors from database
            async with self.db_pool.acquire() as conn:
                error_stats = await conn.fetch("""
                    SELECT 
                        platform,
                        error_type,
                        COUNT(*) as error_count
                    FROM sync_errors 
                    WHERE created_at >= NOW() - INTERVAL '5 minutes'
                    GROUP BY platform, error_type
                """)
                
                for stat in error_stats:
                    metric = SyncMetric(
                        name="sync_error_count",
                        type=MetricType.COUNTER,
                        value=float(stat['error_count']),
                        labels={
                            "platform": stat['platform'],
                            "error_type": stat['error_type'],
                            "window": "5m"
                        },
                        timestamp=datetime.now(timezone.utc),
                        description="Error count by platform and type"
                    )
                    
                    await self.record_metric(metric)
                    
        except Exception as e:
            logger.error(f"Error collecting error metrics: {e}")
    
    async def _evaluate_alerts(self):
        """Evaluate alert rules and create alerts if needed"""
        while self.running:
            try:
                await asyncio.sleep(60)  # Evaluate every minute
                
                for metric_name, rule in self.alert_rules.items():
                    await self._evaluate_alert_rule(metric_name, rule)
                    
            except Exception as e:
                logger.error(f"Error evaluating alerts: {e}")
    
    async def _evaluate_alert_rule(self, metric_name: str, rule: Dict[str, Any]):
        """Evaluate a specific alert rule"""
        try:
            threshold = rule["threshold"]
            level = AlertLevel(rule["level"])
            window_minutes = rule["window_minutes"]
            description = rule["description"]
            
            # Get recent metric values
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(minutes=window_minutes)
            
            async with self.db_pool.acquire() as conn:
                # Get latest value for the metric
                latest_value = await conn.fetchval("""
                    SELECT value FROM sync_metrics 
                    WHERE metric_name = $1 AND timestamp >= $2 AND timestamp <= $3
                    ORDER BY timestamp DESC
                    LIMIT 1
                """, metric_name, start_time, end_time)
                
                if latest_value is not None:
                    # Check if alert should be triggered
                    should_alert = False
                    
                    if metric_name in ["sync_failure_rate", "error_rate"]:
                        should_alert = latest_value > threshold
                    elif metric_name in ["sync_latency_p95", "processing_time", "queue_depth"]:
                        should_alert = latest_value > threshold
                    elif metric_name == "platform_health":
                        should_alert = latest_value < threshold
                    
                    if should_alert:
                        # Check if similar alert already exists
                        existing_alert = await conn.fetchval("""
                            SELECT id FROM sync_alerts 
                            WHERE metric_name = $1 AND resolved_at IS NULL
                            AND created_at >= NOW() - INTERVAL '1 hour'
                        """, metric_name)
                        
                        if not existing_alert:
                            # Create new alert
                            alert_id = f"alert_{metric_name}_{int(datetime.now().timestamp())}"
                            
                            alert = Alert(
                                id=alert_id,
                                level=level,
                                title=f"{metric_name.replace('_', ' ').title()} Alert",
                                message=f"{description}. Current value: {latest_value}, Threshold: {threshold}",
                                metric_name=metric_name,
                                threshold_value=threshold,
                                current_value=latest_value,
                                platform="all",
                                tenant_id=None,
                                created_at=datetime.now(timezone.utc)
                            )
                            
                            await self.create_alert(alert)
                            
        except Exception as e:
            logger.error(f"Error evaluating alert rule {metric_name}: {e}")
    
    async def _cleanup_old_data(self):
        """Clean up old metrics and alerts"""
        while self.running:
            try:
                # Clean up every hour
                await asyncio.sleep(3600)
                
                # Clean up old metrics (keep 7 days)
                cutoff_time = datetime.now(timezone.utc) - timedelta(days=7)
                
                async with self.db_pool.acquire() as conn:
                    deleted_metrics = await conn.execute("""
                        DELETE FROM sync_metrics WHERE timestamp < $1
                    """, cutoff_time)
                    
                    # Clean up resolved alerts (keep 30 days)
                    alert_cutoff = datetime.now(timezone.utc) - timedelta(days=30)
                    deleted_alerts = await conn.execute("""
                        DELETE FROM sync_alerts 
                        WHERE resolved_at IS NOT NULL AND resolved_at < $1
                    """, alert_cutoff)
                    
                    logger.info(f"🧹 Cleaned up {deleted_metrics} old metrics and {deleted_alerts} old alerts")
                    
            except Exception as e:
                logger.error(f"Error cleaning up old data: {e}")
    
    async def _store_metric_in_db(self, metric: SyncMetric):
        """Store metric in database"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO sync_metrics (
                        metric_name, metric_type, value, labels, timestamp, description
                    ) VALUES ($1, $2, $3, $4, $5, $6)
                """, metric.name, metric.type.value, metric.value,
                json.dumps(metric.labels), metric.timestamp, metric.description)
                
        except Exception as e:
            logger.error(f"Failed to store metric in database: {e}")

async def create_monitoring_tables(db_pool):
    """Create monitoring tables"""
    try:
        async with db_pool.acquire() as conn:
            # Create metrics table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS sync_metrics (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    metric_name VARCHAR(255) NOT NULL,
                    metric_type VARCHAR(50) NOT NULL,
                    value FLOAT NOT NULL,
                    labels JSONB DEFAULT '{}',
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    description TEXT
                );
            """)
            
            # Create alerts table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS sync_alerts (
                    id VARCHAR(255) PRIMARY KEY,
                    level VARCHAR(50) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    metric_name VARCHAR(255) NOT NULL,
                    threshold_value FLOAT NOT NULL,
                    current_value FLOAT NOT NULL,
                    platform VARCHAR(100) NOT NULL,
                    tenant_id UUID,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    resolved_at TIMESTAMP WITH TIME ZONE,
                    resolution_note TEXT
                );
            """)
            
            # Create indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_sync_metrics_name ON sync_metrics(metric_name);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_sync_metrics_timestamp ON sync_metrics(timestamp);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_sync_alerts_level ON sync_alerts(level);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_sync_alerts_created ON sync_alerts(created_at);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_sync_alerts_resolved ON sync_alerts(resolved_at);")
            
            logger.info("✅ Monitoring tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create monitoring tables: {e}")