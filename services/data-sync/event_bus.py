#!/usr/bin/env python3

"""
BizOSaaS Data Synchronization - Event Bus Module
Message routing and transformation between platforms
"""

import asyncio
import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
from enum import Enum

import redis.asyncio as redis
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class EventPriority(int, Enum):
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4

class MessageType(str, Enum):
    SYNC_EVENT = "sync_event"
    PLATFORM_STATUS = "platform_status"
    HEALTH_CHECK = "health_check"
    BATCH_OPERATION = "batch_operation"
    ERROR_REPORT = "error_report"

@dataclass
class EventMessage:
    id: str
    type: MessageType
    priority: EventPriority
    source: str
    targets: List[str]
    payload: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: datetime
    expires_at: Optional[datetime] = None

class EventTransformer:
    """Transforms events between different platform formats"""
    
    def __init__(self):
        self.transformation_rules = self._load_transformation_rules()
    
    def _load_transformation_rules(self) -> Dict[str, Any]:
        """Load platform-specific transformation rules"""
        return {
            "bizoholic": {
                "user": {
                    "field_mappings": {
                        "user_id": "id",
                        "full_name": "name",
                        "email_address": "email",
                        "phone_number": "phone"
                    },
                    "required_fields": ["id", "email", "name"],
                    "api_format": "rest",
                    "date_format": "iso8601"
                },
                "lead": {
                    "field_mappings": {
                        "lead_id": "id",
                        "contact_name": "name",
                        "contact_email": "email",
                        "lead_score": "score",
                        "lead_status": "status"
                    },
                    "required_fields": ["id", "email", "status"],
                    "api_format": "rest",
                    "date_format": "iso8601"
                },
                "campaign": {
                    "field_mappings": {
                        "campaign_id": "id",
                        "campaign_name": "name",
                        "campaign_budget": "budget",
                        "campaign_status": "status"
                    },
                    "required_fields": ["id", "name", "status"],
                    "api_format": "rest",
                    "date_format": "iso8601"
                }
            },
            "coreldove": {
                "user": {
                    "field_mappings": {
                        "customer_id": "id",
                        "customer_name": "name",
                        "customer_email": "email",
                        "customer_phone": "phone"
                    },
                    "required_fields": ["id", "email", "name"],
                    "api_format": "graphql",
                    "date_format": "iso8601",
                    "currency": "INR"
                },
                "product": {
                    "field_mappings": {
                        "product_id": "id",
                        "product_name": "name",
                        "product_price": "price",
                        "product_inventory": "stock"
                    },
                    "required_fields": ["id", "name", "price"],
                    "api_format": "graphql",
                    "date_format": "iso8601",
                    "currency": "INR"
                },
                "order": {
                    "field_mappings": {
                        "order_id": "id",
                        "order_total": "total",
                        "order_status": "status",
                        "order_items": "items"
                    },
                    "required_fields": ["id", "total", "status"],
                    "api_format": "graphql",
                    "date_format": "iso8601",
                    "currency": "INR"
                }
            },
            "bizosaas": {
                "user": {
                    "field_mappings": {
                        "user_id": "id",
                        "user_name": "name",
                        "user_email": "email",
                        "user_phone": "phone"
                    },
                    "required_fields": ["id", "email", "name"],
                    "api_format": "rest",
                    "date_format": "iso8601"
                },
                "tenant": {
                    "field_mappings": {
                        "tenant_id": "id",
                        "tenant_name": "name",
                        "subscription_tier": "plan",
                        "tenant_status": "status"
                    },
                    "required_fields": ["id", "name", "plan"],
                    "api_format": "rest",
                    "date_format": "iso8601"
                }
            }
        }
    
    async def transform_event(self, event: Dict[str, Any], source_platform: str, target_platform: str) -> Dict[str, Any]:
        """Transform event data for target platform"""
        try:
            entity_type = event.get("entity_type", "")
            source_rules = self.transformation_rules.get(source_platform, {}).get(entity_type, {})
            target_rules = self.transformation_rules.get(target_platform, {}).get(entity_type, {})
            
            if not source_rules or not target_rules:
                logger.warning(f"No transformation rules for {entity_type}: {source_platform} -> {target_platform}")
                return event
            
            # Transform field mappings
            transformed_data = {}
            source_mappings = source_rules.get("field_mappings", {})
            target_mappings = target_rules.get("field_mappings", {})
            
            # Reverse source mappings for lookup
            reverse_source_mappings = {v: k for k, v in source_mappings.items()}
            
            for target_field, common_field in target_mappings.items():
                # Find corresponding source field
                source_field = reverse_source_mappings.get(common_field, common_field)
                
                if source_field in event.get("data", {}):
                    value = event["data"][source_field]
                    
                    # Apply value transformations
                    transformed_value = await self._transform_value(
                        value, source_field, target_field, source_platform, target_platform
                    )
                    transformed_data[target_field] = transformed_value
            
            # Copy unmapped fields
            for field, value in event.get("data", {}).items():
                if field not in source_mappings and field not in transformed_data:
                    transformed_data[field] = value
            
            # Apply platform-specific transformations
            transformed_data = await self._apply_platform_transformations(
                transformed_data, source_platform, target_platform, entity_type
            )
            
            # Create transformed event
            transformed_event = event.copy()
            transformed_event["data"] = transformed_data
            transformed_event["_transformation"] = {
                "source_platform": source_platform,
                "target_platform": target_platform,
                "transformed_at": datetime.now(timezone.utc).isoformat(),
                "transformation_version": "1.0"
            }
            
            logger.info(f"✅ Transformed {entity_type} event: {source_platform} -> {target_platform}")
            return transformed_event
            
        except Exception as e:
            logger.error(f"❌ Failed to transform event: {e}")
            return event
    
    async def _transform_value(self, value: Any, source_field: str, target_field: str, 
                             source_platform: str, target_platform: str) -> Any:
        """Transform individual field values"""
        
        # Currency conversion
        if "price" in source_field.lower() or "amount" in source_field.lower() or "total" in source_field.lower():
            if source_platform == "bizoholic" and target_platform == "coreldove":
                # USD to INR conversion
                return float(value) * 83 if value else 0
            elif source_platform == "coreldove" and target_platform == "bizoholic":
                # INR to USD conversion
                return float(value) / 83 if value else 0
        
        # Date format transformations
        if "date" in source_field.lower() or "time" in source_field.lower():
            if isinstance(value, str):
                try:
                    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    return dt.isoformat()
                except:
                    return value
        
        # Status code mappings
        if "status" in source_field.lower():
            status_mappings = {
                ("bizoholic", "coreldove"): {
                    "active": "published",
                    "inactive": "draft",
                    "pending": "pending_review"
                },
                ("coreldove", "bizoholic"): {
                    "published": "active",
                    "draft": "inactive",
                    "pending_review": "pending"
                }
            }
            mapping = status_mappings.get((source_platform, target_platform), {})
            return mapping.get(value, value)
        
        return value
    
    async def _apply_platform_transformations(self, data: Dict[str, Any], source_platform: str, 
                                            target_platform: str, entity_type: str) -> Dict[str, Any]:
        """Apply platform-specific transformations"""
        
        # CoreLDove specific transformations
        if target_platform == "coreldove":
            # Add platform metadata
            data["_platform_context"] = {
                "currency": "INR",
                "locale": "en-IN",
                "timezone": "Asia/Kolkata"
            }
            
            # Ensure required GraphQL fields
            if entity_type == "product" and "variants" not in data:
                data["variants"] = []
        
        # Bizoholic specific transformations
        elif target_platform == "bizoholic":
            # Add platform metadata
            data["_platform_context"] = {
                "currency": "USD",
                "locale": "en-US",
                "timezone": "UTC"
            }
            
            # Ensure marketing fields
            if entity_type == "lead" and "source" not in data:
                data["source"] = "cross_platform_sync"
        
        # BizOSaaS specific transformations
        elif target_platform == "bizosaas":
            # Add tenant context
            if "tenant_id" not in data:
                data["tenant_id"] = "default"
            
            # Add sync metadata
            data["_sync_metadata"] = {
                "synced_from": source_platform,
                "sync_timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        return data

class EventBus:
    """Central event bus for cross-platform message routing"""
    
    def __init__(self, redis_client, db_pool):
        self.redis_client = redis_client
        self.db_pool = db_pool
        self.transformer = EventTransformer()
        self.subscribers = {}
        self.message_handlers = {}
        self.running = False
    
    async def start(self):
        """Start the event bus"""
        self.running = True
        logger.info("🚀 Starting Event Bus...")
        
        # Start message processing tasks
        asyncio.create_task(self._process_priority_queue())
        asyncio.create_task(self._process_normal_queue())
        asyncio.create_task(self._cleanup_expired_messages())
        
        logger.info("✅ Event Bus started successfully")
    
    async def stop(self):
        """Stop the event bus"""
        self.running = False
        logger.info("🔄 Stopping Event Bus...")
    
    async def publish(self, message: EventMessage) -> bool:
        """Publish a message to the event bus"""
        try:
            # Serialize message
            message_data = {
                "id": message.id,
                "type": message.type.value,
                "priority": message.priority.value,
                "source": message.source,
                "targets": message.targets,
                "payload": message.payload,
                "metadata": message.metadata,
                "created_at": message.created_at.isoformat(),
                "expires_at": message.expires_at.isoformat() if message.expires_at else None
            }
            
            # Route to appropriate queue based on priority
            queue_name = self._get_queue_name(message.priority)
            
            await self.redis_client.lpush(queue_name, json.dumps(message_data))
            
            # Publish to subscribers
            await self.redis_client.publish(f"events:{message.type.value}", json.dumps(message_data))
            
            # Store in database for audit
            await self._store_message(message)
            
            logger.info(f"✅ Published message {message.id} to queue {queue_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to publish message {message.id}: {e}")
            return False
    
    async def subscribe(self, message_type: MessageType, handler: Callable):
        """Subscribe to specific message type"""
        if message_type not in self.subscribers:
            self.subscribers[message_type] = []
        
        self.subscribers[message_type].append(handler)
        self.message_handlers[f"events:{message_type.value}"] = handler
        
        logger.info(f"✅ Subscribed to {message_type.value}")
    
    async def _process_priority_queue(self):
        """Process high-priority messages"""
        queue_name = self._get_queue_name(EventPriority.CRITICAL)
        
        while self.running:
            try:
                # Block for up to 5 seconds waiting for messages
                result = await self.redis_client.brpop(queue_name, timeout=5)
                
                if result:
                    _, message_data = result
                    message = json.loads(message_data)
                    await self._process_message(message)
                
            except Exception as e:
                logger.error(f"Error processing priority queue: {e}")
                await asyncio.sleep(1)
    
    async def _process_normal_queue(self):
        """Process normal priority messages"""
        queue_names = [
            self._get_queue_name(EventPriority.HIGH),
            self._get_queue_name(EventPriority.NORMAL),
            self._get_queue_name(EventPriority.LOW)
        ]
        
        while self.running:
            try:
                # Round-robin processing of different priority queues
                for queue_name in queue_names:
                    result = await self.redis_client.brpop(queue_name, timeout=1)
                    
                    if result:
                        _, message_data = result
                        message = json.loads(message_data)
                        await self._process_message(message)
                        break
                    
            except Exception as e:
                logger.error(f"Error processing normal queue: {e}")
                await asyncio.sleep(1)
    
    async def _process_message(self, message_data: Dict[str, Any]):
        """Process an individual message"""
        try:
            message_id = message_data["id"]
            message_type = MessageType(message_data["type"])
            
            # Check if message has expired
            if message_data.get("expires_at"):
                expires_at = datetime.fromisoformat(message_data["expires_at"])
                if datetime.now(timezone.utc) > expires_at:
                    logger.warning(f"Message {message_id} expired, skipping")
                    return
            
            # Route to platform-specific handlers
            if message_type == MessageType.SYNC_EVENT:
                await self._handle_sync_event(message_data)
            elif message_type == MessageType.PLATFORM_STATUS:
                await self._handle_platform_status(message_data)
            elif message_type == MessageType.HEALTH_CHECK:
                await self._handle_health_check(message_data)
            elif message_type == MessageType.BATCH_OPERATION:
                await self._handle_batch_operation(message_data)
            elif message_type == MessageType.ERROR_REPORT:
                await self._handle_error_report(message_data)
            
            # Call registered subscribers
            if message_type in self.subscribers:
                for handler in self.subscribers[message_type]:
                    try:
                        await handler(message_data)
                    except Exception as e:
                        logger.error(f"Subscriber handler error: {e}")
            
            logger.info(f"✅ Processed message {message_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to process message: {e}")
    
    async def _handle_sync_event(self, message_data: Dict[str, Any]):
        """Handle sync event messages"""
        payload = message_data["payload"]
        source_platform = message_data["source"]
        targets = message_data["targets"]
        
        # Transform event for each target platform
        for target_platform in targets:
            if target_platform == source_platform:
                continue
            
            transformed_payload = await self.transformer.transform_event(
                payload, source_platform, target_platform
            )
            
            # Send to target platform
            await self._send_to_platform(transformed_payload, target_platform)
    
    async def _handle_platform_status(self, message_data: Dict[str, Any]):
        """Handle platform status updates"""
        payload = message_data["payload"]
        source_platform = message_data["source"]
        
        # Update platform status in database
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO platform_status (platform, status, last_seen, metadata)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (platform) DO UPDATE SET
                        status = EXCLUDED.status,
                        last_seen = EXCLUDED.last_seen,
                        metadata = EXCLUDED.metadata
                """, source_platform, payload.get("status", "unknown"),
                datetime.now(timezone.utc), json.dumps(payload.get("metadata", {})))
                
        except Exception as e:
            logger.error(f"Failed to update platform status: {e}")
    
    async def _handle_health_check(self, message_data: Dict[str, Any]):
        """Handle health check messages"""
        payload = message_data["payload"]
        source_platform = message_data["source"]
        
        # Respond with current system health
        health_response = {
            "platform": "bizosaas-data-sync",
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": {
                "redis": "healthy",
                "postgresql": "healthy",
                "event_bus": "running"
            }
        }
        
        # Send response back to source platform
        response_message = EventMessage(
            id=f"health_response_{datetime.now().timestamp()}",
            type=MessageType.PLATFORM_STATUS,
            priority=EventPriority.HIGH,
            source="bizosaas-data-sync",
            targets=[source_platform],
            payload=health_response,
            metadata={"response_to": message_data["id"]},
            created_at=datetime.now(timezone.utc)
        )
        
        await self.publish(response_message)
    
    async def _handle_batch_operation(self, message_data: Dict[str, Any]):
        """Handle batch operation messages"""
        payload = message_data["payload"]
        operation_type = payload.get("operation_type")
        
        if operation_type == "bulk_sync":
            # Process bulk synchronization
            entities = payload.get("entities", [])
            for entity in entities:
                # Create individual sync events
                sync_message = EventMessage(
                    id=f"bulk_sync_{entity.get('id', '')}_{datetime.now().timestamp()}",
                    type=MessageType.SYNC_EVENT,
                    priority=EventPriority.NORMAL,
                    source=message_data["source"],
                    targets=message_data["targets"],
                    payload=entity,
                    metadata={"batch_operation": True},
                    created_at=datetime.now(timezone.utc)
                )
                await self.publish(sync_message)
    
    async def _handle_error_report(self, message_data: Dict[str, Any]):
        """Handle error report messages"""
        payload = message_data["payload"]
        source_platform = message_data["source"]
        
        # Store error in database
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO sync_errors (
                        platform, error_type, error_message, metadata, created_at
                    ) VALUES ($1, $2, $3, $4, $5)
                """, source_platform, payload.get("error_type", "unknown"),
                payload.get("error_message", ""), json.dumps(payload.get("metadata", {})),
                datetime.now(timezone.utc))
                
        except Exception as e:
            logger.error(f"Failed to store error report: {e}")
    
    async def _send_to_platform(self, payload: Dict[str, Any], target_platform: str):
        """Send transformed payload to target platform"""
        # This would integrate with the actual platform APIs
        # For now, we'll store in a platform-specific queue
        
        platform_queue = f"platform_events:{target_platform}"
        await self.redis_client.lpush(platform_queue, json.dumps(payload))
        
        logger.info(f"✅ Sent event to {target_platform}")
    
    async def _cleanup_expired_messages(self):
        """Clean up expired messages periodically"""
        while self.running:
            try:
                # Clean up every 5 minutes
                await asyncio.sleep(300)
                
                # Remove expired messages from database
                async with self.db_pool.acquire() as conn:
                    deleted = await conn.execute("""
                        DELETE FROM event_messages 
                        WHERE expires_at IS NOT NULL AND expires_at < NOW()
                    """)
                    
                    if deleted:
                        logger.info(f"🧹 Cleaned up {deleted} expired messages")
                        
            except Exception as e:
                logger.error(f"Error cleaning up expired messages: {e}")
    
    def _get_queue_name(self, priority: EventPriority) -> str:
        """Get queue name for priority level"""
        queue_names = {
            EventPriority.CRITICAL: "events:critical",
            EventPriority.HIGH: "events:high",
            EventPriority.NORMAL: "events:normal",
            EventPriority.LOW: "events:low"
        }
        return queue_names.get(priority, "events:normal")
    
    async def _store_message(self, message: EventMessage):
        """Store message in database for audit trail"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO event_messages (
                        message_id, message_type, priority, source, targets,
                        payload, metadata, created_at, expires_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """, message.id, message.type.value, message.priority.value,
                message.source, message.targets, json.dumps(message.payload),
                json.dumps(message.metadata), message.created_at, message.expires_at)
                
        except Exception as e:
            logger.error(f"Failed to store message: {e}")

async def create_event_bus_tables(db_pool):
    """Create event bus tables"""
    try:
        async with db_pool.acquire() as conn:
            # Create event messages table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS event_messages (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    message_id VARCHAR(255) UNIQUE NOT NULL,
                    message_type VARCHAR(100) NOT NULL,
                    priority INTEGER NOT NULL,
                    source VARCHAR(100) NOT NULL,
                    targets TEXT[] NOT NULL,
                    payload JSONB NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    expires_at TIMESTAMP WITH TIME ZONE
                );
            """)
            
            # Create platform status table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS platform_status (
                    platform VARCHAR(100) PRIMARY KEY,
                    status VARCHAR(50) NOT NULL,
                    last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    metadata JSONB DEFAULT '{}'
                );
            """)
            
            # Create sync errors table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS sync_errors (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    platform VARCHAR(100) NOT NULL,
                    error_type VARCHAR(100) NOT NULL,
                    error_message TEXT NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)
            
            # Create indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_event_messages_type ON event_messages(message_type);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_event_messages_priority ON event_messages(priority);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_event_messages_created ON event_messages(created_at);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_sync_errors_platform ON sync_errors(platform);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_sync_errors_created ON sync_errors(created_at);")
            
            logger.info("✅ Event bus tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create event bus tables: {e}")