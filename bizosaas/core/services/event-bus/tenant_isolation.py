"""
Tenant Isolation for BizOSaaS Event Bus

Ensures secure multi-tenant operation by isolating events
and subscriptions by tenant context.
"""

import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel
import structlog

from domain_events import BaseEvent

logger = structlog.get_logger(__name__)


class TenantContext(BaseModel):
    """Tenant context for multi-tenant isolation"""
    tenant_id: UUID
    tenant_name: str
    subscription_tier: str = "basic"
    is_active: bool = True
    
    # Security settings
    data_encryption_enabled: bool = True
    audit_logging_enabled: bool = True
    
    # Resource limits
    max_events_per_hour: Optional[int] = None
    max_subscriptions: Optional[int] = None
    max_event_retention_days: int = 30
    
    # Permissions
    allowed_event_types: Optional[List[str]] = None
    blocked_event_types: List[str] = []
    
    # Metadata
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    metadata: Dict[str, Any] = {}


class TenantIsolationError(Exception):
    """Raised when tenant isolation is violated"""
    pass


class TenantEventFilter:
    """Filters events based on tenant permissions"""
    
    def __init__(self, tenant_context: TenantContext):
        self.tenant_context = tenant_context
        self.logger = logger.bind(
            component="tenant_filter",
            tenant_id=str(tenant_context.tenant_id)
        )
    
    def is_event_allowed(self, event: BaseEvent) -> bool:
        """Check if event is allowed for this tenant"""
        try:
            # Check if tenant is active
            if not self.tenant_context.is_active:
                self.logger.warning("Event blocked - tenant inactive")
                return False
            
            # Check allowed event types
            if self.tenant_context.allowed_event_types:
                if event.event_type not in self.tenant_context.allowed_event_types:
                    self.logger.warning(
                        "Event blocked - not in allowed types",
                        event_type=event.event_type
                    )
                    return False
            
            # Check blocked event types
            if event.event_type in self.tenant_context.blocked_event_types:
                self.logger.warning(
                    "Event blocked - in blocked types",
                    event_type=event.event_type
                )
                return False
            
            return True
            
        except Exception as e:
            self.logger.error("Error checking event permissions", error=str(e))
            return False
    
    def filter_event_data(self, event: BaseEvent) -> BaseEvent:
        """Filter sensitive data from events based on tenant settings"""
        try:
            # Create a copy of the event
            filtered_event = event.model_copy(deep=True)
            
            # Apply data filtering based on subscription tier
            if self.tenant_context.subscription_tier == "basic":
                # Remove detailed analytics for basic tier
                if "detailed_analytics" in filtered_event.data:
                    del filtered_event.data["detailed_analytics"]
                
                # Limit metadata
                if len(filtered_event.metadata) > 10:
                    filtered_event.metadata = dict(
                        list(filtered_event.metadata.items())[:10]
                    )
            
            # Apply data encryption if enabled
            if self.tenant_context.data_encryption_enabled:
                filtered_event = self._encrypt_sensitive_data(filtered_event)
            
            return filtered_event
            
        except Exception as e:
            self.logger.error("Error filtering event data", error=str(e))
            return event
    
    def _encrypt_sensitive_data(self, event: BaseEvent) -> BaseEvent:
        """Encrypt sensitive data fields"""
        sensitive_fields = ["email", "phone", "address", "credit_card", "ssn"]
        
        try:
            # Encrypt sensitive fields in event data
            for field in sensitive_fields:
                if field in event.data:
                    event.data[field] = self._simple_encrypt(str(event.data[field]))
            
            # Encrypt sensitive fields in metadata
            for field in sensitive_fields:
                if field in event.metadata:
                    event.metadata[field] = self._simple_encrypt(str(event.metadata[field]))
            
            return event
            
        except Exception as e:
            self.logger.error("Error encrypting sensitive data", error=str(e))
            return event
    
    def _simple_encrypt(self, data: str) -> str:
        """Simple encryption for demo purposes - use proper encryption in production"""
        # In production, use proper encryption like Fernet from cryptography
        # This is just for demonstration
        return hashlib.sha256(f"tenant_{self.tenant_context.tenant_id}_{data}".encode()).hexdigest()[:16] + "..."


class TenantResourceLimiter:
    """Enforces resource limits per tenant"""
    
    def __init__(self, tenant_context: TenantContext, redis_client):
        self.tenant_context = tenant_context
        self.redis_client = redis_client
        self.logger = logger.bind(
            component="resource_limiter",
            tenant_id=str(tenant_context.tenant_id)
        )
    
    async def check_event_rate_limit(self) -> bool:
        """Check if tenant is within event rate limits"""
        if not self.tenant_context.max_events_per_hour:
            return True
        
        try:
            # Use Redis to track events per hour
            hour_key = f"tenant_events:{self.tenant_context.tenant_id}:{datetime.utcnow().strftime('%Y%m%d%H')}"
            
            # Get current count
            current_count = await self.redis_client.get(hour_key)
            current_count = int(current_count) if current_count else 0
            
            if current_count >= self.tenant_context.max_events_per_hour:
                self.logger.warning(
                    "Event rate limit exceeded",
                    current_count=current_count,
                    limit=self.tenant_context.max_events_per_hour
                )
                return False
            
            # Increment counter
            await self.redis_client.incr(hour_key)
            await self.redis_client.expire(hour_key, 3600)  # 1 hour TTL
            
            return True
            
        except Exception as e:
            self.logger.error("Error checking rate limit", error=str(e))
            return True  # Allow on error to avoid blocking
    
    async def check_subscription_limit(self, current_subscription_count: int) -> bool:
        """Check if tenant is within subscription limits"""
        if not self.tenant_context.max_subscriptions:
            return True
        
        if current_subscription_count >= self.tenant_context.max_subscriptions:
            self.logger.warning(
                "Subscription limit exceeded",
                current_count=current_subscription_count,
                limit=self.tenant_context.max_subscriptions
            )
            return False
        
        return True


class TenantAuditLogger:
    """Logs tenant activities for compliance and security"""
    
    def __init__(self, tenant_context: TenantContext, redis_client):
        self.tenant_context = tenant_context
        self.redis_client = redis_client
        self.logger = logger.bind(
            component="audit_logger",
            tenant_id=str(tenant_context.tenant_id)
        )
    
    async def log_event_activity(
        self,
        action: str,
        event: BaseEvent,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log tenant event activity"""
        if not self.tenant_context.audit_logging_enabled:
            return
        
        try:
            audit_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "tenant_id": str(self.tenant_context.tenant_id),
                "action": action,
                "event_id": str(event.event_id),
                "event_type": event.event_type,
                "source_service": event.source_service,
                "details": details or {}
            }
            
            # Store in Redis with TTL based on retention policy
            audit_key = f"tenant_audit:{self.tenant_context.tenant_id}:{event.event_id}"
            await self.redis_client.setex(
                audit_key,
                self.tenant_context.max_event_retention_days * 24 * 60 * 60,
                str(audit_entry)
            )
            
            self.logger.info("Audit entry created", action=action, event_type=event.event_type)
            
        except Exception as e:
            self.logger.error("Error logging audit entry", error=str(e))
    
    async def get_audit_trail(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get audit trail for tenant"""
        try:
            # Get all audit keys for tenant
            pattern = f"tenant_audit:{self.tenant_context.tenant_id}:*"
            keys = await self.redis_client.keys(pattern)
            
            audit_entries = []
            for key in keys[:limit]:  # Limit results
                entry = await self.redis_client.get(key)
                if entry:
                    try:
                        audit_entries.append(eval(entry))  # Convert string back to dict
                    except Exception:
                        continue
            
            # Sort by timestamp
            audit_entries.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            return audit_entries[:limit]
            
        except Exception as e:
            self.logger.error("Error retrieving audit trail", error=str(e))
            return []


def ensure_tenant_isolation(event: BaseEvent, tenant_context: TenantContext) -> BaseEvent:
    """
    Ensure event is properly isolated for tenant
    
    This is the main function used by the event bus to enforce tenant isolation
    """
    try:
        # Verify tenant ID matches
        if event.tenant_id != tenant_context.tenant_id:
            raise TenantIsolationError(
                f"Event tenant ID {event.tenant_id} doesn't match context {tenant_context.tenant_id}"
            )
        
        # Apply tenant filtering
        event_filter = TenantEventFilter(tenant_context)
        
        # Check if event is allowed
        if not event_filter.is_event_allowed(event):
            raise TenantIsolationError(f"Event type {event.event_type} not allowed for tenant")
        
        # Filter and encrypt data
        filtered_event = event_filter.filter_event_data(event)
        
        # Add tenant isolation metadata
        filtered_event.metadata.update({
            "tenant_isolation": {
                "tenant_id": str(tenant_context.tenant_id),
                "subscription_tier": tenant_context.subscription_tier,
                "isolation_applied_at": datetime.utcnow().isoformat()
            }
        })
        
        return filtered_event
        
    except Exception as e:
        logger.error(
            "Tenant isolation failed",
            tenant_id=str(tenant_context.tenant_id),
            event_id=str(event.event_id),
            error=str(e)
        )
        raise


def validate_tenant_access(
    event: BaseEvent,
    requesting_tenant_id: UUID
) -> bool:
    """
    Validate that a tenant can access an event
    
    Used for API endpoints and event queries
    """
    try:
        # Check tenant ID match
        if event.tenant_id != requesting_tenant_id:
            logger.warning(
                "Tenant access denied",
                event_tenant_id=str(event.tenant_id),
                requesting_tenant_id=str(requesting_tenant_id)
            )
            return False
        
        return True
        
    except Exception as e:
        logger.error("Error validating tenant access", error=str(e))
        return False


def create_tenant_routing_key(base_key: str, tenant_id: UUID) -> str:
    """Create tenant-specific routing key"""
    return f"tenant.{tenant_id}.{base_key}"


def extract_tenant_from_routing_key(routing_key: str) -> Optional[UUID]:
    """Extract tenant ID from routing key"""
    try:
        if routing_key.startswith("tenant."):
            parts = routing_key.split(".")
            if len(parts) >= 2:
                return UUID(parts[1])
        return None
    except Exception:
        return None


class TenantContextManager:
    """Manages tenant contexts and settings"""
    
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.logger = logger.bind(component="tenant_context_manager")
        self.context_cache: Dict[UUID, TenantContext] = {}
    
    async def get_tenant_context(self, tenant_id: UUID) -> Optional[TenantContext]:
        """Get tenant context by ID"""
        try:
            # Check cache first
            if tenant_id in self.context_cache:
                return self.context_cache[tenant_id]
            
            # Get from Redis
            context_key = f"tenant_context:{tenant_id}"
            context_data = await self.redis_client.get(context_key)
            
            if context_data:
                context = TenantContext.model_validate_json(context_data)
                self.context_cache[tenant_id] = context
                return context
            
            # Create default context if not found
            default_context = TenantContext(
                tenant_id=tenant_id,
                tenant_name=f"Tenant {tenant_id}",
                subscription_tier="basic"
            )
            
            await self.store_tenant_context(default_context)
            return default_context
            
        except Exception as e:
            self.logger.error("Error getting tenant context", tenant_id=str(tenant_id), error=str(e))
            return None
    
    async def store_tenant_context(self, context: TenantContext) -> bool:
        """Store tenant context"""
        try:
            context_key = f"tenant_context:{context.tenant_id}"
            await self.redis_client.set(context_key, context.model_dump_json())
            
            # Update cache
            self.context_cache[context.tenant_id] = context
            
            self.logger.info("Tenant context stored", tenant_id=str(context.tenant_id))
            return True
            
        except Exception as e:
            self.logger.error("Error storing tenant context", error=str(e))
            return False
    
    def clear_cache(self) -> None:
        """Clear context cache"""
        self.context_cache.clear()