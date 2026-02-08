"""
Integration Monitor Engine
Core monitoring system for all third-party integrations
"""

import asyncio
import aiohttp
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from config.settings import settings, get_integration_config
from core.integration_registry import IntegrationRegistry
from core.health_checker import HealthChecker
from core.metrics_collector import MetricsCollector
from database.models import IntegrationStatus, HealthCheckResult, Alert
from database.connection import get_db_session

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status enumeration"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class AlertSeverity(Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class IntegrationHealth:
    """Integration health data structure"""
    name: str
    status: HealthStatus
    response_time: float
    error_rate: float
    uptime: float
    last_check: datetime
    consecutive_failures: int
    health_score: float
    cost_today: float
    rate_limit_usage: float
    next_check: datetime
    metadata: Dict[str, Any]


@dataclass
class MonitoringMetrics:
    """Monitoring metrics data structure"""
    total_integrations: int
    healthy_count: int
    degraded_count: int
    unhealthy_count: int
    average_response_time: float
    total_error_rate: float
    average_uptime: float
    active_alerts: int
    failovers_today: int
    cost_today: float


class IntegrationMonitorEngine:
    """
    Core monitoring engine that orchestrates health checks,
    metrics collection, and integration with failover controller
    """
    
    def __init__(self, failover_controller, alert_manager, websocket_manager):
        self.failover_controller = failover_controller
        self.alert_manager = alert_manager
        self.websocket_manager = websocket_manager
        
        self.integration_registry = IntegrationRegistry()
        self.health_checker = HealthChecker()
        self.metrics_collector = MetricsCollector()
        
        self.is_monitoring = False
        self.monitor_task = None
        
        # In-memory cache for health status
        self.health_cache: Dict[str, IntegrationHealth] = {}
        self.last_metrics_update = time.time()
        
        # Performance tracking
        self.check_counter = 0
        self.total_checks = 0
        self.start_time = time.time()
        
        logger.info("Integration Monitor Engine initialized")
    
    async def start_monitoring(self):
        """Start the monitoring engine"""
        if self.is_monitoring:
            logger.warning("Monitoring is already active")
            return
        
        self.is_monitoring = True
        logger.info("🚀 Starting integration monitoring engine")
        
        try:
            # Initialize integrations
            await self.integration_registry.load_integrations()
            integrations = await self.integration_registry.get_active_integrations()
            logger.info(f"Loaded {len(integrations)} active integrations")
            
            # Start monitoring loop
            while self.is_monitoring:
                start_cycle = time.time()
                
                # Perform health checks
                await self._run_monitoring_cycle()
                
                # Update metrics
                await self._update_metrics()
                
                # Send real-time updates
                await self._broadcast_updates()
                
                # Calculate sleep time to maintain interval
                cycle_time = time.time() - start_cycle
                sleep_time = max(0, settings.MONITOR_INTERVAL - cycle_time)
                
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                else:
                    logger.warning(f"Monitoring cycle took {cycle_time:.2f}s, exceeding interval of {settings.MONITOR_INTERVAL}s")
                
        except Exception as e:
            logger.error(f"Monitoring engine failed: {e}")
            self.is_monitoring = False
            raise
    
    async def stop_monitoring(self):
        """Stop the monitoring engine"""
        logger.info("🛑 Stopping integration monitoring engine")
        self.is_monitoring = False
        
        if self.monitor_task:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
    
    async def _run_monitoring_cycle(self):
        """Run a single monitoring cycle"""
        integrations = await self.integration_registry.get_active_integrations()
        
        # Create tasks for parallel health checks
        tasks = []
        for integration in integrations:
            task = asyncio.create_task(self._check_integration_health(integration))
            tasks.append(task)
        
        # Wait for all health checks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Health check failed for {integrations[i]['name']}: {result}")
                await self._handle_check_failure(integrations[i], str(result))
            else:
                await self._process_health_result(result)
        
        self.check_counter += 1
        self.total_checks += len(integrations)
    
    async def _check_integration_health(self, integration: Dict[str, Any]) -> IntegrationHealth:
        """Check health of a single integration"""
        start_time = time.time()
        integration_name = integration['name']
        config = get_integration_config(integration_name)
        
        try:
            # Perform health check
            health_result = await self.health_checker.check_health(integration)
            response_time = time.time() - start_time
            
            # Calculate health metrics
            health_score = self._calculate_health_score(health_result, response_time)
            status = self._determine_health_status(health_result, response_time, config)
            
            # Get current cache entry for trend analysis
            current_health = self.health_cache.get(integration_name)
            consecutive_failures = 0
            if current_health and status == HealthStatus.UNHEALTHY:
                if current_health.status == HealthStatus.UNHEALTHY:
                    consecutive_failures = current_health.consecutive_failures + 1
                else:
                    consecutive_failures = 1
            
            # Calculate uptime and error rate
            uptime = await self._calculate_uptime(integration_name)
            error_rate = await self._calculate_error_rate(integration_name)
            
            # Get cost and rate limit data
            cost_today = await self._get_cost_today(integration_name)
            rate_limit_usage = await self._get_rate_limit_usage(integration_name)
            
            # Create health object
            health = IntegrationHealth(
                name=integration_name,
                status=status,
                response_time=response_time,
                error_rate=error_rate,
                uptime=uptime,
                last_check=datetime.now(),
                consecutive_failures=consecutive_failures,
                health_score=health_score,
                cost_today=cost_today,
                rate_limit_usage=rate_limit_usage,
                next_check=datetime.now() + timedelta(seconds=config['health_check_interval']),
                metadata=health_result.get('metadata', {})
            )
            
            # Store in cache
            self.health_cache[integration_name] = health
            
            # Store in database
            await self._store_health_result(health)
            
            return health
            
        except Exception as e:
            logger.error(f"Health check failed for {integration_name}: {e}")
            
            # Create failed health object
            health = IntegrationHealth(
                name=integration_name,
                status=HealthStatus.UNKNOWN,
                response_time=time.time() - start_time,
                error_rate=1.0,
                uptime=0.0,
                last_check=datetime.now(),
                consecutive_failures=1,
                health_score=0.0,
                cost_today=0.0,
                rate_limit_usage=0.0,
                next_check=datetime.now() + timedelta(seconds=config['health_check_interval']),
                metadata={'error': str(e)}
            )
            
            self.health_cache[integration_name] = health
            return health
    
    def _calculate_health_score(self, health_result: Dict[str, Any], response_time: float) -> float:
        """Calculate composite health score (0-100)"""
        score = 100.0
        
        # Response time penalty
        if response_time > settings.RESPONSE_TIME_CRITICAL:
            score -= 50
        elif response_time > settings.RESPONSE_TIME_WARNING:
            score -= 20
        
        # Status code penalty
        status_code = health_result.get('status_code', 200)
        if status_code >= 500:
            score -= 40
        elif status_code >= 400:
            score -= 20
        
        # Additional checks from health result
        if not health_result.get('success', True):
            score -= 30
        
        return max(0.0, score)
    
    def _determine_health_status(self, health_result: Dict[str, Any], response_time: float, config: Dict[str, Any]) -> HealthStatus:
        """Determine health status based on result and configuration"""
        
        # Check if completely failed
        if not health_result.get('success', True):
            return HealthStatus.UNHEALTHY
        
        status_code = health_result.get('status_code', 200)
        
        # Critical failures
        if status_code >= 500 or response_time > settings.RESPONSE_TIME_CRITICAL:
            return HealthStatus.UNHEALTHY
        
        # Degraded performance
        if status_code >= 400 or response_time > settings.RESPONSE_TIME_WARNING:
            return HealthStatus.DEGRADED
        
        # Healthy
        return HealthStatus.HEALTHY
    
    async def _calculate_uptime(self, integration_name: str) -> float:
        """Calculate uptime percentage for last 24 hours"""
        try:
            async with get_db_session() as session:
                # Get health checks from last 24 hours
                since = datetime.now() - timedelta(hours=24)
                
                # This would be a database query in real implementation
                # For now, return a calculated value based on current health
                current_health = self.health_cache.get(integration_name)
                if current_health:
                    if current_health.status == HealthStatus.HEALTHY:
                        return 0.999
                    elif current_health.status == HealthStatus.DEGRADED:
                        return 0.995
                    else:
                        return 0.990
                
                return 0.999  # Default high uptime
                
        except Exception as e:
            logger.error(f"Failed to calculate uptime for {integration_name}: {e}")
            return 0.999
    
    async def _calculate_error_rate(self, integration_name: str) -> float:
        """Calculate error rate for last hour"""
        try:
            # This would query actual error logs in real implementation
            current_health = self.health_cache.get(integration_name)
            if current_health:
                if current_health.status == HealthStatus.UNHEALTHY:
                    return 0.05  # 5% error rate
                elif current_health.status == HealthStatus.DEGRADED:
                    return 0.02  # 2% error rate
                else:
                    return 0.001  # 0.1% error rate
            
            return 0.001  # Default low error rate
            
        except Exception as e:
            logger.error(f"Failed to calculate error rate for {integration_name}: {e}")
            return 0.001
    
    async def _get_cost_today(self, integration_name: str) -> float:
        """Get API usage cost for today"""
        try:
            # This would query actual billing data in real implementation
            # For now, return estimated costs based on integration type
            config = get_integration_config(integration_name)
            
            if integration_name in settings.AI_INTEGRATIONS:
                return 15.50  # AI services typically more expensive
            elif integration_name in settings.PAYMENT_INTEGRATIONS:
                return 5.25   # Payment processing costs
            elif integration_name in settings.MARKETING_INTEGRATIONS:
                return 25.75  # Marketing platform costs
            else:
                return 2.10   # Other services
                
        except Exception as e:
            logger.error(f"Failed to get cost for {integration_name}: {e}")
            return 0.0
    
    async def _get_rate_limit_usage(self, integration_name: str) -> float:
        """Get current rate limit usage percentage"""
        try:
            # This would query actual rate limit data in real implementation
            # For now, return simulated usage
            import random
            return random.uniform(0.1, 0.8)  # 10-80% usage
            
        except Exception as e:
            logger.error(f"Failed to get rate limit usage for {integration_name}: {e}")
            return 0.0
    
    async def _process_health_result(self, health: IntegrationHealth):
        """Process health check result and trigger actions"""
        
        # Check if failover is needed
        if health.consecutive_failures >= settings.FAILOVER_THRESHOLD:
            logger.warning(f"Triggering failover for {health.name} after {health.consecutive_failures} failures")
            await self.failover_controller.trigger_failover(health.name, health)
        
        # Check if alerts need to be sent
        await self._check_alert_conditions(health)
        
        # Update metrics
        await self.metrics_collector.record_health_check(health)
    
    async def _check_alert_conditions(self, health: IntegrationHealth):
        """Check if alert conditions are met"""
        
        # Critical alerts
        if health.status == HealthStatus.UNHEALTHY:
            await self.alert_manager.send_alert(
                severity=AlertSeverity.CRITICAL,
                message=f"Integration {health.name} is unhealthy",
                details={
                    'integration': health.name,
                    'status': health.status.value,
                    'response_time': health.response_time,
                    'consecutive_failures': health.consecutive_failures,
                    'error_rate': health.error_rate
                }
            )
        
        # High response time alerts
        if health.response_time > settings.RESPONSE_TIME_CRITICAL:
            await self.alert_manager.send_alert(
                severity=AlertSeverity.HIGH,
                message=f"Integration {health.name} has critical response time",
                details={
                    'integration': health.name,
                    'response_time': health.response_time,
                    'threshold': settings.RESPONSE_TIME_CRITICAL
                }
            )
        
        # Error rate alerts
        if health.error_rate > settings.ERROR_RATE_CRITICAL:
            await self.alert_manager.send_alert(
                severity=AlertSeverity.HIGH,
                message=f"Integration {health.name} has high error rate",
                details={
                    'integration': health.name,
                    'error_rate': health.error_rate,
                    'threshold': settings.ERROR_RATE_CRITICAL
                }
            )
        
        # Cost alerts
        if health.cost_today > settings.COST_ALERT_THRESHOLD:
            await self.alert_manager.send_alert(
                severity=AlertSeverity.MEDIUM,
                message=f"Integration {health.name} exceeded cost threshold",
                details={
                    'integration': health.name,
                    'cost_today': health.cost_today,
                    'threshold': settings.COST_ALERT_THRESHOLD
                }
            )
    
    async def _handle_check_failure(self, integration: Dict[str, Any], error: str):
        """Handle health check failure"""
        integration_name = integration['name']
        
        logger.error(f"Health check failed for {integration_name}: {error}")
        
        # Create failed health entry
        health = IntegrationHealth(
            name=integration_name,
            status=HealthStatus.UNKNOWN,
            response_time=settings.HEALTH_CHECK_TIMEOUT,
            error_rate=1.0,
            uptime=0.0,
            last_check=datetime.now(),
            consecutive_failures=1,
            health_score=0.0,
            cost_today=0.0,
            rate_limit_usage=0.0,
            next_check=datetime.now() + timedelta(seconds=60),  # Retry in 1 minute
            metadata={'error': error}
        )
        
        self.health_cache[integration_name] = health
        await self._process_health_result(health)
    
    async def _store_health_result(self, health: IntegrationHealth):
        """Store health result in database"""
        try:
            async with get_db_session() as session:
                # This would store in actual database
                # For now, just log
                logger.debug(f"Storing health result for {health.name}: {health.status.value}")
                
        except Exception as e:
            logger.error(f"Failed to store health result: {e}")
    
    async def _update_metrics(self):
        """Update aggregated metrics"""
        if time.time() - self.last_metrics_update < 60:  # Update every minute
            return
        
        try:
            metrics = self._calculate_monitoring_metrics()
            await self.metrics_collector.update_system_metrics(metrics)
            self.last_metrics_update = time.time()
            
        except Exception as e:
            logger.error(f"Failed to update metrics: {e}")
    
    def _calculate_monitoring_metrics(self) -> MonitoringMetrics:
        """Calculate current monitoring metrics"""
        if not self.health_cache:
            return MonitoringMetrics(
                total_integrations=0,
                healthy_count=0,
                degraded_count=0,
                unhealthy_count=0,
                average_response_time=0.0,
                total_error_rate=0.0,
                average_uptime=0.0,
                active_alerts=0,
                failovers_today=0,
                cost_today=0.0
            )
        
        total = len(self.health_cache)
        healthy = sum(1 for h in self.health_cache.values() if h.status == HealthStatus.HEALTHY)
        degraded = sum(1 for h in self.health_cache.values() if h.status == HealthStatus.DEGRADED)
        unhealthy = sum(1 for h in self.health_cache.values() if h.status == HealthStatus.UNHEALTHY)
        
        avg_response_time = sum(h.response_time for h in self.health_cache.values()) / total
        total_error_rate = sum(h.error_rate for h in self.health_cache.values()) / total
        avg_uptime = sum(h.uptime for h in self.health_cache.values()) / total
        total_cost = sum(h.cost_today for h in self.health_cache.values())
        
        return MonitoringMetrics(
            total_integrations=total,
            healthy_count=healthy,
            degraded_count=degraded,
            unhealthy_count=unhealthy,
            average_response_time=avg_response_time,
            total_error_rate=total_error_rate,
            average_uptime=avg_uptime,
            active_alerts=0,  # Would be calculated from alert manager
            failovers_today=0,  # Would be calculated from failover controller
            cost_today=total_cost
        )
    
    async def _broadcast_updates(self):
        """Broadcast real-time updates via WebSocket"""
        try:
            if self.websocket_manager.has_connections():
                update_data = {
                    'type': 'health_update',
                    'timestamp': datetime.now().isoformat(),
                    'data': {
                        'integrations': {name: asdict(health) for name, health in self.health_cache.items()},
                        'metrics': asdict(self._calculate_monitoring_metrics())
                    }
                }
                
                await self.websocket_manager.broadcast(update_data)
                
        except Exception as e:
            logger.error(f"Failed to broadcast updates: {e}")
    
    # Public API methods
    
    async def get_integration_health(self, integration_name: str) -> Optional[IntegrationHealth]:
        """Get current health status for an integration"""
        return self.health_cache.get(integration_name)
    
    async def get_all_integrations_health(self) -> Dict[str, IntegrationHealth]:
        """Get health status for all integrations"""
        return self.health_cache.copy()
    
    async def get_monitoring_metrics(self) -> MonitoringMetrics:
        """Get current monitoring metrics"""
        return self._calculate_monitoring_metrics()
    
    async def force_health_check(self, integration_name: str) -> IntegrationHealth:
        """Force immediate health check for specific integration"""
        integrations = await self.integration_registry.get_active_integrations()
        integration = next((i for i in integrations if i['name'] == integration_name), None)
        
        if not integration:
            raise ValueError(f"Integration {integration_name} not found")
        
        return await self._check_integration_health(integration)
    
    async def get_performance_stats(self) -> Dict[str, Any]:
        """Get monitoring engine performance statistics"""
        uptime = time.time() - self.start_time
        
        return {
            'uptime_seconds': uptime,
            'total_checks_performed': self.total_checks,
            'monitoring_cycles': self.check_counter,
            'checks_per_cycle': self.total_checks / max(self.check_counter, 1),
            'average_cycle_time': uptime / max(self.check_counter, 1),
            'integrations_monitored': len(self.health_cache),
            'cache_size_bytes': len(str(self.health_cache)),
            'is_monitoring': self.is_monitoring
        }