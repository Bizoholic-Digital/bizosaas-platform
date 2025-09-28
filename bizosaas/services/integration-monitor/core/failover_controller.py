"""
Failover Controller
Implements automatic failover strategies for external integrations
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from config.settings import settings

logger = logging.getLogger(__name__)


class FailoverStrategy(Enum):
    """Failover strategy types"""
    PRIMARY_SECONDARY = "primary_secondary"
    LOAD_BALANCING = "load_balancing"
    CIRCUIT_BREAKER = "circuit_breaker"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    SMART_ROUTING = "smart_routing"


class CircuitBreakerState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery


@dataclass
class FailoverTarget:
    """Failover target configuration"""
    name: str
    priority: int
    weight: float
    health_score: float
    last_used: datetime
    active: bool
    metadata: Dict[str, Any]


@dataclass
class CircuitBreaker:
    """Circuit breaker for an integration"""
    name: str
    state: CircuitBreakerState
    failure_count: int
    last_failure_time: datetime
    last_success_time: datetime
    next_attempt_time: datetime
    failure_threshold: int
    timeout_seconds: int
    half_open_max_calls: int
    half_open_calls: int


@dataclass
class FailoverEvent:
    """Failover event record"""
    integration_name: str
    trigger_reason: str
    from_target: Optional[str]
    to_target: str
    strategy: FailoverStrategy
    timestamp: datetime
    success: bool
    response_time: float
    metadata: Dict[str, Any]


class FailoverController:
    """
    Manages automatic failover between primary and backup providers
    Implements multiple failover strategies based on integration type
    """
    
    def __init__(self, alert_manager):
        self.alert_manager = alert_manager
        
        # Failover targets for each integration
        self.failover_targets: Dict[str, List[FailoverTarget]] = {}
        
        # Circuit breakers for each integration endpoint
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        
        # Current active targets
        self.active_targets: Dict[str, str] = {}
        
        # Failover event history
        self.failover_events: List[FailoverEvent] = []
        
        # Performance tracking
        self.failover_stats = {
            'total_failovers': 0,
            'successful_failovers': 0,
            'failed_failovers': 0,
            'average_failover_time': 0.0
        }
        
        logger.info("Failover Controller initialized")
    
    async def initialize_failover_targets(self):
        """Initialize failover targets for all integrations"""
        try:
            # Load failover configurations
            await self._load_failover_configurations()
            
            # Initialize circuit breakers
            await self._initialize_circuit_breakers()
            
            logger.info(f"Initialized failover targets for {len(self.failover_targets)} integrations")
            
        except Exception as e:
            logger.error(f"Failed to initialize failover targets: {e}")
            raise
    
    async def trigger_failover(self, integration_name: str, health_data: Any) -> bool:
        """
        Trigger failover for an integration based on health data
        
        Args:
            integration_name: Name of the failing integration
            health_data: Current health status data
            
        Returns:
            bool: True if failover was successful, False otherwise
        """
        start_time = time.time()
        
        try:
            logger.warning(f"🔄 Triggering failover for {integration_name}")
            
            # Get integration strategy
            strategy = self._get_failover_strategy(integration_name)
            
            # Execute failover based on strategy
            success = False
            to_target = None
            
            if strategy == FailoverStrategy.PRIMARY_SECONDARY:
                success, to_target = await self._execute_primary_secondary_failover(integration_name, health_data)
            elif strategy == FailoverStrategy.LOAD_BALANCING:
                success, to_target = await self._execute_load_balancing_failover(integration_name, health_data)
            elif strategy == FailoverStrategy.CIRCUIT_BREAKER:
                success, to_target = await self._execute_circuit_breaker_failover(integration_name, health_data)
            elif strategy == FailoverStrategy.GRACEFUL_DEGRADATION:
                success, to_target = await self._execute_graceful_degradation(integration_name, health_data)
            elif strategy == FailoverStrategy.SMART_ROUTING:
                success, to_target = await self._execute_smart_routing_failover(integration_name, health_data)
            else:
                logger.error(f"Unknown failover strategy: {strategy}")
                success = False
            
            # Record failover event
            response_time = time.time() - start_time
            await self._record_failover_event(
                integration_name=integration_name,
                trigger_reason=f"Health check failed: {health_data.status}",
                from_target=self.active_targets.get(integration_name),
                to_target=to_target,
                strategy=strategy,
                success=success,
                response_time=response_time,
                metadata={'health_data': health_data.__dict__ if hasattr(health_data, '__dict__') else str(health_data)}
            )
            
            # Update statistics
            self._update_failover_stats(success, response_time)
            
            # Send alert
            if success:
                await self.alert_manager.send_alert(
                    severity="medium",
                    message=f"Failover successful for {integration_name}",
                    details={
                        'integration': integration_name,
                        'strategy': strategy.value,
                        'to_target': to_target,
                        'response_time': response_time
                    }
                )
                logger.info(f"✅ Failover successful for {integration_name} -> {to_target}")
            else:
                await self.alert_manager.send_alert(
                    severity="high",
                    message=f"Failover failed for {integration_name}",
                    details={
                        'integration': integration_name,
                        'strategy': strategy.value,
                        'response_time': response_time
                    }
                )
                logger.error(f"❌ Failover failed for {integration_name}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failover execution failed for {integration_name}: {e}")
            return False
    
    def _get_failover_strategy(self, integration_name: str) -> FailoverStrategy:
        """Get failover strategy for integration"""
        
        # Check integration category and return appropriate strategy
        if integration_name in settings.PAYMENT_INTEGRATIONS:
            return FailoverStrategy.PRIMARY_SECONDARY
        elif integration_name in settings.MARKETING_INTEGRATIONS:
            return FailoverStrategy.SMART_ROUTING
        elif integration_name in settings.COMMUNICATION_INTEGRATIONS:
            return FailoverStrategy.CIRCUIT_BREAKER
        elif integration_name in settings.ECOMMERCE_INTEGRATIONS:
            return FailoverStrategy.GRACEFUL_DEGRADATION
        elif integration_name in settings.AI_INTEGRATIONS:
            return FailoverStrategy.LOAD_BALANCING
        elif integration_name in settings.INFRASTRUCTURE_INTEGRATIONS:
            return FailoverStrategy.PRIMARY_SECONDARY
        else:
            return FailoverStrategy.CIRCUIT_BREAKER
    
    async def _execute_primary_secondary_failover(self, integration_name: str, health_data: Any) -> Tuple[bool, Optional[str]]:
        """Execute primary/secondary failover strategy"""
        targets = self.failover_targets.get(integration_name, [])
        if len(targets) < 2:
            logger.warning(f"No backup targets available for {integration_name}")
            return False, None
        
        # Sort by priority (lower number = higher priority)
        targets.sort(key=lambda x: x.priority)
        
        current_target = self.active_targets.get(integration_name)
        
        # Find next available target
        for target in targets:
            if target.name != current_target and target.active and target.health_score > 50:
                # Switch to this target
                self.active_targets[integration_name] = target.name
                target.last_used = datetime.now()
                
                logger.info(f"Switched {integration_name} from {current_target} to {target.name}")
                return True, target.name
        
        logger.error(f"No healthy backup targets available for {integration_name}")
        return False, None
    
    async def _execute_load_balancing_failover(self, integration_name: str, health_data: Any) -> Tuple[bool, Optional[str]]:
        """Execute load balancing failover strategy"""
        targets = self.failover_targets.get(integration_name, [])
        if not targets:
            return False, None
        
        # Filter healthy targets
        healthy_targets = [t for t in targets if t.active and t.health_score > 30]
        if not healthy_targets:
            logger.error(f"No healthy targets available for load balancing {integration_name}")
            return False, None
        
        # Select target based on weighted round robin
        selected_target = self._select_weighted_target(healthy_targets)
        
        if selected_target:
            self.active_targets[integration_name] = selected_target.name
            selected_target.last_used = datetime.now()
            
            logger.info(f"Load balanced {integration_name} to {selected_target.name}")
            return True, selected_target.name
        
        return False, None
    
    async def _execute_circuit_breaker_failover(self, integration_name: str, health_data: Any) -> Tuple[bool, Optional[str]]:
        """Execute circuit breaker failover strategy"""
        circuit_breaker = self.circuit_breakers.get(integration_name)
        
        if not circuit_breaker:
            # Create new circuit breaker
            circuit_breaker = CircuitBreaker(
                name=integration_name,
                state=CircuitBreakerState.CLOSED,
                failure_count=1,
                last_failure_time=datetime.now(),
                last_success_time=datetime.now() - timedelta(hours=1),
                next_attempt_time=datetime.now() + timedelta(seconds=settings.CIRCUIT_BREAKER_TIMEOUT),
                failure_threshold=settings.CIRCUIT_BREAKER_FAILURE_THRESHOLD,
                timeout_seconds=settings.CIRCUIT_BREAKER_TIMEOUT,
                half_open_max_calls=settings.CIRCUIT_BREAKER_RECOVERY_THRESHOLD,
                half_open_calls=0
            )
            self.circuit_breakers[integration_name] = circuit_breaker
        
        # Update circuit breaker state
        circuit_breaker.failure_count += 1
        circuit_breaker.last_failure_time = datetime.now()
        
        # Check if threshold exceeded
        if circuit_breaker.failure_count >= circuit_breaker.failure_threshold:
            circuit_breaker.state = CircuitBreakerState.OPEN
            circuit_breaker.next_attempt_time = datetime.now() + timedelta(seconds=circuit_breaker.timeout_seconds)
            
            logger.warning(f"Circuit breaker OPEN for {integration_name}")
            
            # Try to find alternative target
            targets = self.failover_targets.get(integration_name, [])
            healthy_targets = [t for t in targets if t.active and t.health_score > 50]
            
            if healthy_targets:
                selected_target = healthy_targets[0]  # Use first healthy target
                self.active_targets[integration_name] = selected_target.name
                return True, selected_target.name
        
        return False, None
    
    async def _execute_graceful_degradation(self, integration_name: str, health_data: Any) -> Tuple[bool, Optional[str]]:
        """Execute graceful degradation strategy"""
        
        # Enable fallback mode with reduced functionality
        fallback_config = {
            'mode': 'degraded',
            'features_disabled': ['advanced_analytics', 'real_time_sync'],
            'cache_only': True,
            'reduced_rate_limit': True
        }
        
        # Store degraded mode configuration
        self.active_targets[integration_name] = f"{integration_name}_degraded"
        
        logger.info(f"Enabled graceful degradation for {integration_name}")
        return True, f"{integration_name}_degraded"
    
    async def _execute_smart_routing_failover(self, integration_name: str, health_data: Any) -> Tuple[bool, Optional[str]]:
        """Execute smart routing failover strategy"""
        targets = self.failover_targets.get(integration_name, [])
        if not targets:
            return False, None
        
        # Calculate routing scores based on health, response time, and load
        scored_targets = []
        for target in targets:
            if not target.active:
                continue
            
            # Base score from health
            score = target.health_score
            
            # Penalty for recent heavy usage
            time_since_last_use = (datetime.now() - target.last_used).total_seconds()
            if time_since_last_use < 60:  # Used within last minute
                score *= 0.7
            
            # Bonus for lighter weight (less loaded)
            score *= (1.0 + (1.0 - target.weight))
            
            scored_targets.append((target, score))
        
        if not scored_targets:
            return False, None
        
        # Select target with highest score
        best_target = max(scored_targets, key=lambda x: x[1])[0]
        
        self.active_targets[integration_name] = best_target.name
        best_target.last_used = datetime.now()
        
        logger.info(f"Smart routing selected {best_target.name} for {integration_name}")
        return True, best_target.name
    
    def _select_weighted_target(self, targets: List[FailoverTarget]) -> Optional[FailoverTarget]:
        """Select target using weighted round robin"""
        if not targets:
            return None
        
        # Calculate total weight
        total_weight = sum(t.weight * t.health_score / 100.0 for t in targets)
        
        if total_weight <= 0:
            return targets[0]  # Fallback to first target
        
        # Generate random value
        import random
        rand_value = random.uniform(0, total_weight)
        
        # Select target based on weight
        current_weight = 0
        for target in targets:
            current_weight += target.weight * target.health_score / 100.0
            if rand_value <= current_weight:
                return target
        
        return targets[-1]  # Fallback to last target
    
    async def _record_failover_event(self, integration_name: str, trigger_reason: str, 
                                   from_target: Optional[str], to_target: Optional[str],
                                   strategy: FailoverStrategy, success: bool, 
                                   response_time: float, metadata: Dict[str, Any]):
        """Record failover event for analysis"""
        event = FailoverEvent(
            integration_name=integration_name,
            trigger_reason=trigger_reason,
            from_target=from_target,
            to_target=to_target,
            strategy=strategy,
            timestamp=datetime.now(),
            success=success,
            response_time=response_time,
            metadata=metadata
        )
        
        self.failover_events.append(event)
        
        # Keep only last 1000 events
        if len(self.failover_events) > 1000:
            self.failover_events = self.failover_events[-1000:]
        
        # Store in database (would be implemented)
        logger.debug(f"Recorded failover event: {integration_name} -> {to_target}")
    
    def _update_failover_stats(self, success: bool, response_time: float):
        """Update failover statistics"""
        self.failover_stats['total_failovers'] += 1
        
        if success:
            self.failover_stats['successful_failovers'] += 1
        else:
            self.failover_stats['failed_failovers'] += 1
        
        # Update average response time
        total = self.failover_stats['total_failovers']
        current_avg = self.failover_stats['average_failover_time']
        self.failover_stats['average_failover_time'] = (current_avg * (total - 1) + response_time) / total
    
    async def _load_failover_configurations(self):
        """Load failover target configurations"""
        # This would load from database or configuration files
        # For now, create default configurations
        
        # Payment integrations - Primary/Secondary
        self.failover_targets['stripe'] = [
            FailoverTarget('stripe_primary', 1, 1.0, 100.0, datetime.now(), True, {}),
            FailoverTarget('stripe_secondary', 2, 1.0, 95.0, datetime.now(), True, {}),
        ]
        
        self.failover_targets['paypal'] = [
            FailoverTarget('paypal_primary', 1, 1.0, 100.0, datetime.now(), True, {}),
            FailoverTarget('paypal_secondary', 2, 1.0, 95.0, datetime.now(), True, {}),
        ]
        
        # AI integrations - Load Balancing
        self.failover_targets['openai'] = [
            FailoverTarget('openai_us_east', 1, 0.6, 98.0, datetime.now(), True, {}),
            FailoverTarget('openai_us_west', 2, 0.4, 97.0, datetime.now(), True, {}),
        ]
        
        self.failover_targets['anthropic'] = [
            FailoverTarget('anthropic_primary', 1, 0.7, 99.0, datetime.now(), True, {}),
            FailoverTarget('anthropic_fallback', 2, 0.3, 95.0, datetime.now(), True, {}),
        ]
        
        # Marketing integrations - Smart Routing
        self.failover_targets['google_ads'] = [
            FailoverTarget('google_ads_v1', 1, 0.8, 98.0, datetime.now(), True, {}),
            FailoverTarget('google_ads_v2', 2, 0.2, 96.0, datetime.now(), True, {}),
        ]
        
        logger.info("Loaded default failover configurations")
    
    async def _initialize_circuit_breakers(self):
        """Initialize circuit breakers for all integrations"""
        for integration_name in self.failover_targets.keys():
            if integration_name not in self.circuit_breakers:
                self.circuit_breakers[integration_name] = CircuitBreaker(
                    name=integration_name,
                    state=CircuitBreakerState.CLOSED,
                    failure_count=0,
                    last_failure_time=datetime.now(),
                    last_success_time=datetime.now(),
                    next_attempt_time=datetime.now(),
                    failure_threshold=settings.CIRCUIT_BREAKER_FAILURE_THRESHOLD,
                    timeout_seconds=settings.CIRCUIT_BREAKER_TIMEOUT,
                    half_open_max_calls=settings.CIRCUIT_BREAKER_RECOVERY_THRESHOLD,
                    half_open_calls=0
                )
        
        logger.info(f"Initialized {len(self.circuit_breakers)} circuit breakers")
    
    # Public API methods
    
    async def get_failover_status(self, integration_name: str) -> Dict[str, Any]:
        """Get current failover status for integration"""
        targets = self.failover_targets.get(integration_name, [])
        active_target = self.active_targets.get(integration_name)
        circuit_breaker = self.circuit_breakers.get(integration_name)
        
        return {
            'integration': integration_name,
            'active_target': active_target,
            'available_targets': [{'name': t.name, 'priority': t.priority, 'health_score': t.health_score, 'active': t.active} for t in targets],
            'circuit_breaker': {
                'state': circuit_breaker.state.value if circuit_breaker else 'unknown',
                'failure_count': circuit_breaker.failure_count if circuit_breaker else 0
            },
            'strategy': self._get_failover_strategy(integration_name).value
        }
    
    async def get_all_failover_status(self) -> Dict[str, Any]:
        """Get failover status for all integrations"""
        result = {}
        for integration_name in self.failover_targets.keys():
            result[integration_name] = await self.get_failover_status(integration_name)
        return result
    
    async def get_failover_events(self, integration_name: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent failover events"""
        events = self.failover_events
        
        if integration_name:
            events = [e for e in events if e.integration_name == integration_name]
        
        # Return most recent events
        events = sorted(events, key=lambda x: x.timestamp, reverse=True)[:limit]
        
        return [
            {
                'integration': e.integration_name,
                'trigger_reason': e.trigger_reason,
                'from_target': e.from_target,
                'to_target': e.to_target,
                'strategy': e.strategy.value,
                'timestamp': e.timestamp.isoformat(),
                'success': e.success,
                'response_time': e.response_time,
                'metadata': e.metadata
            }
            for e in events
        ]
    
    async def get_failover_statistics(self) -> Dict[str, Any]:
        """Get failover statistics"""
        total = self.failover_stats['total_failovers']
        success_rate = (self.failover_stats['successful_failovers'] / total * 100) if total > 0 else 0
        
        return {
            **self.failover_stats,
            'success_rate': success_rate,
            'active_circuit_breakers': len([cb for cb in self.circuit_breakers.values() if cb.state != CircuitBreakerState.CLOSED]),
            'total_integrations': len(self.failover_targets),
            'total_targets': sum(len(targets) for targets in self.failover_targets.values())
        }
    
    async def manual_failover(self, integration_name: str, target_name: str) -> bool:
        """Manually trigger failover to specific target"""
        targets = self.failover_targets.get(integration_name, [])
        target = next((t for t in targets if t.name == target_name), None)
        
        if not target:
            logger.error(f"Target {target_name} not found for {integration_name}")
            return False
        
        if not target.active:
            logger.error(f"Target {target_name} is not active")
            return False
        
        # Execute manual failover
        old_target = self.active_targets.get(integration_name)
        self.active_targets[integration_name] = target_name
        target.last_used = datetime.now()
        
        # Record event
        await self._record_failover_event(
            integration_name=integration_name,
            trigger_reason="Manual failover",
            from_target=old_target,
            to_target=target_name,
            strategy=FailoverStrategy.PRIMARY_SECONDARY,
            success=True,
            response_time=0.1,
            metadata={'manual': True}
        )
        
        logger.info(f"Manual failover: {integration_name} -> {target_name}")
        return True
    
    async def reset_circuit_breaker(self, integration_name: str) -> bool:
        """Reset circuit breaker for integration"""
        circuit_breaker = self.circuit_breakers.get(integration_name)
        
        if not circuit_breaker:
            return False
        
        circuit_breaker.state = CircuitBreakerState.CLOSED
        circuit_breaker.failure_count = 0
        circuit_breaker.last_success_time = datetime.now()
        circuit_breaker.half_open_calls = 0
        
        logger.info(f"Reset circuit breaker for {integration_name}")
        return True