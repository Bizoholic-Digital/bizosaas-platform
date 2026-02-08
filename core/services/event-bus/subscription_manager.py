"""
Subscription Manager for BizOSaaS Event Bus

Manages event subscriptions, routing, and subscriber registry
with support for multi-tenancy and dynamic filtering.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

import redis.asyncio as redis
from pydantic import BaseModel
import structlog

logger = structlog.get_logger(__name__)


class EventSubscription(BaseModel):
    """Event subscription model"""
    subscription_id: str
    event_type: str
    service_name: str
    tenant_id: Optional[UUID] = None
    filters: Dict[str, Any] = {}
    created_at: datetime = datetime.utcnow()
    is_active: bool = True
    max_retries: int = 3
    retry_delay_seconds: int = 5
    
    # Subscription metadata
    metadata: Dict[str, Any] = {}
    
    # Performance tracking
    message_count: int = 0
    last_message_at: Optional[datetime] = None
    error_count: int = 0
    last_error_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class SubscriptionStats(BaseModel):
    """Subscription statistics"""
    total_subscriptions: int
    active_subscriptions: int
    subscriptions_by_service: Dict[str, int]
    subscriptions_by_event_type: Dict[str, int]
    subscriptions_by_tenant: Dict[str, int]
    top_event_types: List[Dict[str, Any]]
    subscription_health: Dict[str, Any]


class SubscriptionManager:
    """
    Manages event subscriptions and routing
    
    Features:
    - Dynamic subscription management
    - Multi-tenant subscription isolation
    - Event type filtering and routing
    - Subscription health monitoring
    - Performance metrics tracking
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.logger = logger.bind(component="subscription_manager")
        
        # Redis key patterns
        self.subscription_key_pattern = "eventbus:subscriptions:{subscription_id}"
        self.service_subscriptions_key = "eventbus:service_subscriptions:{service_name}"
        self.event_type_subscriptions_key = "eventbus:event_type_subscriptions:{event_type}"
        self.tenant_subscriptions_key = "eventbus:tenant_subscriptions:{tenant_id}"
        self.subscription_stats_key = "eventbus:subscription_stats"
        
        # Cache for frequently accessed subscriptions
        self.subscription_cache: Dict[str, EventSubscription] = {}
        self.cache_ttl = 300  # 5 minutes
    
    async def initialize(self) -> None:
        """Initialize subscription manager"""
        try:
            # Test Redis connection
            await self.redis_client.ping()
            
            # Initialize stats
            await self._update_subscription_stats()
            
            self.logger.info("Subscription manager initialized")
            
        except Exception as e:
            self.logger.error("Failed to initialize subscription manager", error=str(e))
            raise
    
    async def add_subscription(self, subscription: EventSubscription) -> bool:
        """Add a new subscription"""
        try:
            # Store subscription
            subscription_key = self.subscription_key_pattern.format(
                subscription_id=subscription.subscription_id
            )
            
            await self.redis_client.hset(
                subscription_key,
                mapping={
                    "data": subscription.model_dump_json(),
                    "created_at": subscription.created_at.isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
            )
            
            # Set TTL for subscription (optional cleanup)
            await self.redis_client.expire(subscription_key, 86400 * 30)  # 30 days
            
            # Add to service index
            service_key = self.service_subscriptions_key.format(
                service_name=subscription.service_name
            )
            await self.redis_client.sadd(service_key, subscription.subscription_id)
            
            # Add to event type index
            event_type_key = self.event_type_subscriptions_key.format(
                event_type=subscription.event_type
            )
            await self.redis_client.sadd(event_type_key, subscription.subscription_id)
            
            # Add to tenant index if tenant-specific
            if subscription.tenant_id:
                tenant_key = self.tenant_subscriptions_key.format(
                    tenant_id=subscription.tenant_id
                )
                await self.redis_client.sadd(tenant_key, subscription.subscription_id)
            
            # Update cache
            self.subscription_cache[subscription.subscription_id] = subscription
            
            # Update stats
            await self._update_subscription_stats()
            
            self.logger.info(
                "Subscription added",
                subscription_id=subscription.subscription_id,
                service_name=subscription.service_name,
                event_type=subscription.event_type
            )
            
            return True
            
        except Exception as e:
            self.logger.error(
                "Failed to add subscription",
                subscription_id=subscription.subscription_id,
                error=str(e)
            )
            return False
    
    async def remove_subscription(self, subscription_id: str) -> bool:
        """Remove a subscription"""
        try:
            # Get subscription details first
            subscription = await self.get_subscription(subscription_id)
            if not subscription:
                return False
            
            # Remove from Redis
            subscription_key = self.subscription_key_pattern.format(
                subscription_id=subscription_id
            )
            await self.redis_client.delete(subscription_key)
            
            # Remove from indexes
            service_key = self.service_subscriptions_key.format(
                service_name=subscription.service_name
            )
            await self.redis_client.srem(service_key, subscription_id)
            
            event_type_key = self.event_type_subscriptions_key.format(
                event_type=subscription.event_type
            )
            await self.redis_client.srem(event_type_key, subscription_id)
            
            if subscription.tenant_id:
                tenant_key = self.tenant_subscriptions_key.format(
                    tenant_id=subscription.tenant_id
                )
                await self.redis_client.srem(tenant_key, subscription_id)
            
            # Remove from cache
            self.subscription_cache.pop(subscription_id, None)
            
            # Update stats
            await self._update_subscription_stats()
            
            self.logger.info("Subscription removed", subscription_id=subscription_id)
            return True
            
        except Exception as e:
            self.logger.error(
                "Failed to remove subscription",
                subscription_id=subscription_id,
                error=str(e)
            )
            return False
    
    async def get_subscription(self, subscription_id: str) -> Optional[EventSubscription]:
        """Get subscription by ID"""
        try:
            # Check cache first
            if subscription_id in self.subscription_cache:
                return self.subscription_cache[subscription_id]
            
            # Get from Redis
            subscription_key = self.subscription_key_pattern.format(
                subscription_id=subscription_id
            )
            
            subscription_data = await self.redis_client.hget(subscription_key, "data")
            if not subscription_data:
                return None
            
            # Parse subscription
            subscription = EventSubscription.model_validate_json(subscription_data)
            
            # Update cache
            self.subscription_cache[subscription_id] = subscription
            
            return subscription
            
        except Exception as e:
            self.logger.error(
                "Failed to get subscription",
                subscription_id=subscription_id,
                error=str(e)
            )
            return None
    
    async def get_subscriptions_for_event(
        self, 
        event_type: str,
        tenant_id: Optional[UUID] = None
    ) -> List[EventSubscription]:
        """Get all subscriptions for a specific event type"""
        try:
            # Get subscriptions from event type index
            event_type_key = self.event_type_subscriptions_key.format(
                event_type=event_type
            )
            
            subscription_ids = await self.redis_client.smembers(event_type_key)
            
            subscriptions = []
            for sub_id in subscription_ids:
                subscription = await self.get_subscription(sub_id)
                if not subscription:
                    continue
                
                # Filter by tenant if specified
                if tenant_id and subscription.tenant_id != tenant_id:
                    continue
                
                # Only include active subscriptions
                if subscription.is_active:
                    subscriptions.append(subscription)
            
            return subscriptions
            
        except Exception as e:
            self.logger.error(
                "Failed to get subscriptions for event",
                event_type=event_type,
                error=str(e)
            )
            return []
    
    async def get_subscriptions_for_service(self, service_name: str) -> List[EventSubscription]:
        """Get all subscriptions for a specific service"""
        try:
            service_key = self.service_subscriptions_key.format(service_name=service_name)
            subscription_ids = await self.redis_client.smembers(service_key)
            
            subscriptions = []
            for sub_id in subscription_ids:
                subscription = await self.get_subscription(sub_id)
                if subscription and subscription.is_active:
                    subscriptions.append(subscription)
            
            return subscriptions
            
        except Exception as e:
            self.logger.error(
                "Failed to get subscriptions for service",
                service_name=service_name,
                error=str(e)
            )
            return []
    
    async def get_subscriptions_for_tenant(self, tenant_id: UUID) -> List[EventSubscription]:
        """Get all subscriptions for a specific tenant"""
        try:
            tenant_key = self.tenant_subscriptions_key.format(tenant_id=tenant_id)
            subscription_ids = await self.redis_client.smembers(tenant_key)
            
            subscriptions = []
            for sub_id in subscription_ids:
                subscription = await self.get_subscription(sub_id)
                if subscription and subscription.is_active:
                    subscriptions.append(subscription)
            
            return subscriptions
            
        except Exception as e:
            self.logger.error(
                "Failed to get subscriptions for tenant",
                tenant_id=str(tenant_id),
                error=str(e)
            )
            return []
    
    async def update_subscription_status(
        self, 
        subscription_id: str, 
        is_active: bool
    ) -> bool:
        """Update subscription active status"""
        try:
            subscription = await self.get_subscription(subscription_id)
            if not subscription:
                return False
            
            subscription.is_active = is_active
            
            # Update in Redis
            subscription_key = self.subscription_key_pattern.format(
                subscription_id=subscription_id
            )
            
            await self.redis_client.hset(
                subscription_key,
                mapping={
                    "data": subscription.model_dump_json(),
                    "updated_at": datetime.utcnow().isoformat()
                }
            )
            
            # Update cache
            self.subscription_cache[subscription_id] = subscription
            
            self.logger.info(
                "Subscription status updated",
                subscription_id=subscription_id,
                is_active=is_active
            )
            
            return True
            
        except Exception as e:
            self.logger.error(
                "Failed to update subscription status",
                subscription_id=subscription_id,
                error=str(e)
            )
            return False
    
    async def record_subscription_activity(
        self,
        subscription_id: str,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> None:
        """Record subscription activity for monitoring"""
        try:
            subscription = await self.get_subscription(subscription_id)
            if not subscription:
                return
            
            # Update activity counters
            subscription.message_count += 1
            subscription.last_message_at = datetime.utcnow()
            
            if not success:
                subscription.error_count += 1
                subscription.last_error_at = datetime.utcnow()
                
                if error_message:
                    subscription.metadata["last_error"] = error_message
            
            # Update in Redis
            subscription_key = self.subscription_key_pattern.format(
                subscription_id=subscription_id
            )
            
            await self.redis_client.hset(
                subscription_key,
                mapping={
                    "data": subscription.model_dump_json(),
                    "updated_at": datetime.utcnow().isoformat()
                }
            )
            
            # Update cache
            self.subscription_cache[subscription_id] = subscription
            
        except Exception as e:
            self.logger.error(
                "Failed to record subscription activity",
                subscription_id=subscription_id,
                error=str(e)
            )
    
    async def get_subscription_count(self) -> int:
        """Get total number of active subscriptions"""
        try:
            # Get all subscription keys
            pattern = self.subscription_key_pattern.format(subscription_id="*")
            keys = await self.redis_client.keys(pattern)
            
            # Count active subscriptions
            active_count = 0
            for key in keys:
                subscription_data = await self.redis_client.hget(key, "data")
                if subscription_data:
                    try:
                        subscription = EventSubscription.model_validate_json(subscription_data)
                        if subscription.is_active:
                            active_count += 1
                    except Exception:
                        continue
            
            return active_count
            
        except Exception as e:
            self.logger.error("Failed to get subscription count", error=str(e))
            return 0
    
    async def get_subscription_statistics(self) -> SubscriptionStats:
        """Get comprehensive subscription statistics"""
        try:
            # Get cached stats
            stats_data = await self.redis_client.get(self.subscription_stats_key)
            if stats_data:
                return SubscriptionStats.model_validate_json(stats_data)
            
            # Calculate fresh stats
            await self._update_subscription_stats()
            
            # Get updated stats
            stats_data = await self.redis_client.get(self.subscription_stats_key)
            if stats_data:
                return SubscriptionStats.model_validate_json(stats_data)
            
            # Return empty stats if all else fails
            return SubscriptionStats(
                total_subscriptions=0,
                active_subscriptions=0,
                subscriptions_by_service={},
                subscriptions_by_event_type={},
                subscriptions_by_tenant={},
                top_event_types=[],
                subscription_health={}
            )
            
        except Exception as e:
            self.logger.error("Failed to get subscription statistics", error=str(e))
            return SubscriptionStats(
                total_subscriptions=0,
                active_subscriptions=0,
                subscriptions_by_service={},
                subscriptions_by_event_type={},
                subscriptions_by_tenant={},
                top_event_types=[],
                subscription_health={}
            )
    
    async def cleanup_inactive_subscriptions(self, days_inactive: int = 7) -> int:
        """Clean up subscriptions that haven't been active recently"""
        try:
            cutoff_time = datetime.utcnow().timestamp() - (days_inactive * 24 * 60 * 60)
            
            # Get all subscription keys
            pattern = self.subscription_key_pattern.format(subscription_id="*")
            keys = await self.redis_client.keys(pattern)
            
            cleaned_count = 0
            for key in keys:
                subscription_data = await self.redis_client.hget(key, "data")
                if not subscription_data:
                    continue
                
                try:
                    subscription = EventSubscription.model_validate_json(subscription_data)
                    
                    # Check if subscription is inactive
                    last_activity = subscription.last_message_at or subscription.created_at
                    if last_activity.timestamp() < cutoff_time:
                        await self.remove_subscription(subscription.subscription_id)
                        cleaned_count += 1
                        
                except Exception:
                    continue
            
            self.logger.info("Cleaned up inactive subscriptions", count=cleaned_count)
            return cleaned_count
            
        except Exception as e:
            self.logger.error("Failed to cleanup inactive subscriptions", error=str(e))
            return 0
    
    async def _update_subscription_stats(self) -> None:
        """Update subscription statistics in Redis"""
        try:
            # Get all subscriptions
            pattern = self.subscription_key_pattern.format(subscription_id="*")
            keys = await self.redis_client.keys(pattern)
            
            total_subscriptions = 0
            active_subscriptions = 0
            subscriptions_by_service = {}
            subscriptions_by_event_type = {}
            subscriptions_by_tenant = {}
            healthy_subscriptions = 0
            
            for key in keys:
                subscription_data = await self.redis_client.hget(key, "data")
                if not subscription_data:
                    continue
                
                try:
                    subscription = EventSubscription.model_validate_json(subscription_data)
                    total_subscriptions += 1
                    
                    if subscription.is_active:
                        active_subscriptions += 1
                    
                    # Count by service
                    service_count = subscriptions_by_service.get(subscription.service_name, 0)
                    subscriptions_by_service[subscription.service_name] = service_count + 1
                    
                    # Count by event type
                    event_count = subscriptions_by_event_type.get(subscription.event_type, 0)
                    subscriptions_by_event_type[subscription.event_type] = event_count + 1
                    
                    # Count by tenant
                    if subscription.tenant_id:
                        tenant_key = str(subscription.tenant_id)
                        tenant_count = subscriptions_by_tenant.get(tenant_key, 0)
                        subscriptions_by_tenant[tenant_key] = tenant_count + 1
                    
                    # Check health (error rate < 10%)
                    if subscription.message_count > 0:
                        error_rate = subscription.error_count / subscription.message_count
                        if error_rate < 0.1:
                            healthy_subscriptions += 1
                    else:
                        healthy_subscriptions += 1  # No messages yet, consider healthy
                        
                except Exception:
                    continue
            
            # Create top event types list
            top_event_types = [
                {"event_type": event_type, "count": count}
                for event_type, count in sorted(
                    subscriptions_by_event_type.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
            ]
            
            # Create stats object
            stats = SubscriptionStats(
                total_subscriptions=total_subscriptions,
                active_subscriptions=active_subscriptions,
                subscriptions_by_service=subscriptions_by_service,
                subscriptions_by_event_type=subscriptions_by_event_type,
                subscriptions_by_tenant=subscriptions_by_tenant,
                top_event_types=top_event_types,
                subscription_health={
                    "healthy_subscriptions": healthy_subscriptions,
                    "total_subscriptions": total_subscriptions,
                    "health_percentage": (healthy_subscriptions / total_subscriptions * 100) 
                                        if total_subscriptions > 0 else 100
                }
            )
            
            # Cache stats
            await self.redis_client.setex(
                self.subscription_stats_key,
                300,  # 5 minutes TTL
                stats.model_dump_json()
            )
            
        except Exception as e:
            self.logger.error("Failed to update subscription stats", error=str(e))
    
    def clear_cache(self) -> None:
        """Clear subscription cache"""
        self.subscription_cache.clear()
        self.logger.info("Subscription cache cleared")