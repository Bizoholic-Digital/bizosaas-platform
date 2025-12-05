"""
Message Broker Implementations for BizOSaaS Event Bus

Provides abstraction layer for different message brokers (Redis, RabbitMQ, Kafka)
with unified interface for event publishing and subscription.
"""

import asyncio
import json
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import urlparse

import aio_pika
import redis.asyncio as redis
# from aiokafka import AIOKafkaConsumer, AIOKafkaProducer  # Temporarily disabled
import structlog

logger = structlog.get_logger(__name__)


class MessageBrokerInterface(ABC):
    """Abstract interface for message brokers"""
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the message broker"""
        pass
    
    @abstractmethod
    async def publish(
        self, 
        routing_key: str, 
        message: str, 
        priority: int = 5
    ) -> bool:
        """Publish a message"""
        pass
    
    @abstractmethod
    async def subscribe(
        self, 
        routing_key: str, 
        callback: Callable[[str], None]
    ) -> str:
        """Subscribe to messages"""
        pass
    
    @abstractmethod
    async def unsubscribe(self, routing_key: str) -> bool:
        """Unsubscribe from messages"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check broker health"""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close broker connections"""
        pass


class RedisMessageBroker(MessageBrokerInterface):
    """
    Redis-based message broker implementation
    
    Uses Redis Pub/Sub for real-time messaging and Redis Streams
    for reliable message delivery with acknowledgments.
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.subscribers: Dict[str, Any] = {}
        self.pubsub = None
        self.logger = logger.bind(component="redis_broker")
        self.is_initialized = False
    
    async def initialize(self) -> None:
        """Initialize Redis message broker"""
        try:
            # Create pub/sub connection
            self.pubsub = self.redis_client.pubsub()
            
            # Test connection
            await self.redis_client.ping()
            
            self.is_initialized = True
            self.logger.info("Redis message broker initialized")
            
        except Exception as e:
            self.logger.error("Failed to initialize Redis broker", error=str(e))
            raise
    
    async def publish(
        self, 
        routing_key: str, 
        message: str, 
        priority: int = 5
    ) -> bool:
        """
        Publish message to Redis
        
        Uses both pub/sub for real-time delivery and streams for reliability
        """
        try:
            # Prepare message with metadata
            message_data = {
                "content": message,
                "priority": priority,
                "routing_key": routing_key,
                "timestamp": asyncio.get_event_loop().time()
            }
            
            # Publish to pub/sub for real-time subscribers
            await self.redis_client.publish(routing_key, json.dumps(message_data))
            
            # Add to stream for reliable delivery (optional)
            stream_key = f"stream:{routing_key}"
            await self.redis_client.xadd(
                stream_key,
                message_data,
                maxlen=10000  # Keep last 10k messages
            )
            
            self.logger.debug(
                "Message published",
                routing_key=routing_key,
                priority=priority
            )
            
            return True
            
        except Exception as e:
            self.logger.error(
                "Failed to publish message",
                routing_key=routing_key,
                error=str(e)
            )
            return False
    
    async def subscribe(
        self, 
        routing_key: str, 
        callback: Callable[[str], None]
    ) -> str:
        """Subscribe to Redis messages"""
        try:
            # Subscribe to pub/sub
            await self.pubsub.subscribe(routing_key)
            
            # Start message processing task
            subscription_id = f"{routing_key}:{id(callback)}"
            
            async def message_processor():
                async for message in self.pubsub.listen():
                    if message["type"] == "message":
                        try:
                            message_data = json.loads(message["data"])
                            await callback(message_data["content"])
                        except Exception as e:
                            self.logger.error(
                                "Message processing failed",
                                routing_key=routing_key,
                                error=str(e)
                            )
            
            # Store subscription
            task = asyncio.create_task(message_processor())
            self.subscribers[subscription_id] = {
                "routing_key": routing_key,
                "callback": callback,
                "task": task
            }
            
            self.logger.info("Subscription created", routing_key=routing_key)
            return subscription_id
            
        except Exception as e:
            self.logger.error(
                "Failed to subscribe",
                routing_key=routing_key,
                error=str(e)
            )
            raise
    
    async def unsubscribe(self, routing_key: str) -> bool:
        """Unsubscribe from Redis messages"""
        try:
            # Find and cancel subscription
            to_remove = []
            for sub_id, sub_info in self.subscribers.items():
                if sub_info["routing_key"] == routing_key:
                    sub_info["task"].cancel()
                    to_remove.append(sub_id)
            
            # Remove from subscribers
            for sub_id in to_remove:
                del self.subscribers[sub_id]
            
            # Unsubscribe from pub/sub
            await self.pubsub.unsubscribe(routing_key)
            
            self.logger.info("Unsubscribed", routing_key=routing_key)
            return True
            
        except Exception as e:
            self.logger.error(
                "Failed to unsubscribe",
                routing_key=routing_key,
                error=str(e)
            )
            return False
    
    async def health_check(self) -> bool:
        """Check Redis broker health"""
        try:
            await self.redis_client.ping()
            return True
        except Exception:
            return False
    
    async def close(self) -> None:
        """Close Redis connections"""
        try:
            # Cancel all subscription tasks
            for sub_info in self.subscribers.values():
                sub_info["task"].cancel()
            
            self.subscribers.clear()
            
            # Close pub/sub
            if self.pubsub:
                await self.pubsub.close()
            
            self.logger.info("Redis message broker closed")
            
        except Exception as e:
            self.logger.error("Error closing Redis broker", error=str(e))


class RabbitMQBroker(MessageBrokerInterface):
    """
    RabbitMQ-based message broker implementation
    
    Provides advanced routing, durability, and acknowledgments
    for enterprise-grade message delivery.
    """
    
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self.connection = None
        self.channel = None
        self.exchange_name = "bizosaas.events"
        self.subscribers: Dict[str, Dict[str, Any]] = {}
        self.logger = logger.bind(component="rabbitmq_broker")
    
    async def initialize(self) -> None:
        """Initialize RabbitMQ connection"""
        try:
            # Establish connection
            self.connection = await aio_pika.connect_robust(self.connection_url)
            self.channel = await self.connection.channel()
            
            # Set quality of service
            await self.channel.set_qos(prefetch_count=100)
            
            # Declare exchange
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name,
                aio_pika.ExchangeType.TOPIC,
                durable=True
            )
            
            self.logger.info("RabbitMQ message broker initialized")
            
        except Exception as e:
            self.logger.error("Failed to initialize RabbitMQ", error=str(e))
            raise
    
    async def publish(
        self, 
        routing_key: str, 
        message: str, 
        priority: int = 5
    ) -> bool:
        """Publish message to RabbitMQ"""
        try:
            # Create message
            message_obj = aio_pika.Message(
                body=message.encode('utf-8'),
                priority=priority,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            )
            
            # Publish message
            await self.exchange.publish(
                message_obj,
                routing_key=routing_key
            )
            
            self.logger.debug(
                "Message published to RabbitMQ",
                routing_key=routing_key,
                priority=priority
            )
            
            return True
            
        except Exception as e:
            self.logger.error(
                "Failed to publish to RabbitMQ",
                routing_key=routing_key,
                error=str(e)
            )
            return False
    
    async def subscribe(
        self, 
        routing_key: str, 
        callback: Callable[[str], None]
    ) -> str:
        """Subscribe to RabbitMQ messages"""
        try:
            # Create queue
            queue_name = f"bizosaas.{routing_key.replace('.', '_').replace('*', 'any')}"
            queue = await self.channel.declare_queue(
                queue_name,
                durable=True,
                auto_delete=False
            )
            
            # Bind queue to exchange
            await queue.bind(self.exchange, routing_key)
            
            # Create message handler
            async def message_handler(message: aio_pika.IncomingMessage):
                async with message.process():
                    try:
                        content = message.body.decode('utf-8')
                        await callback(content)
                    except Exception as e:
                        self.logger.error(
                            "RabbitMQ message processing failed",
                            routing_key=routing_key,
                            error=str(e)
                        )
                        # Message will be rejected and potentially requeued
                        raise
            
            # Start consuming
            consumer_tag = await queue.consume(message_handler)
            
            subscription_id = f"{routing_key}:{consumer_tag}"
            self.subscribers[subscription_id] = {
                "routing_key": routing_key,
                "queue": queue,
                "consumer_tag": consumer_tag,
                "callback": callback
            }
            
            self.logger.info(
                "RabbitMQ subscription created",
                routing_key=routing_key,
                queue_name=queue_name
            )
            
            return subscription_id
            
        except Exception as e:
            self.logger.error(
                "Failed to subscribe to RabbitMQ",
                routing_key=routing_key,
                error=str(e)
            )
            raise
    
    async def unsubscribe(self, routing_key: str) -> bool:
        """Unsubscribe from RabbitMQ messages"""
        try:
            to_remove = []
            for sub_id, sub_info in self.subscribers.items():
                if sub_info["routing_key"] == routing_key:
                    # Cancel consumer
                    await sub_info["queue"].cancel(sub_info["consumer_tag"])
                    to_remove.append(sub_id)
            
            # Remove subscriptions
            for sub_id in to_remove:
                del self.subscribers[sub_id]
            
            self.logger.info("Unsubscribed from RabbitMQ", routing_key=routing_key)
            return True
            
        except Exception as e:
            self.logger.error(
                "Failed to unsubscribe from RabbitMQ",
                routing_key=routing_key,
                error=str(e)
            )
            return False
    
    async def health_check(self) -> bool:
        """Check RabbitMQ health"""
        try:
            if self.connection and not self.connection.is_closed:
                return True
            return False
        except Exception:
            return False
    
    async def close(self) -> None:
        """Close RabbitMQ connections"""
        try:
            # Cancel all consumers
            for sub_info in self.subscribers.values():
                try:
                    await sub_info["queue"].cancel(sub_info["consumer_tag"])
                except Exception:
                    pass
            
            self.subscribers.clear()
            
            # Close connection
            if self.connection and not self.connection.is_closed:
                await self.connection.close()
            
            self.logger.info("RabbitMQ message broker closed")
            
        except Exception as e:
            self.logger.error("Error closing RabbitMQ", error=str(e))


class KafkaBroker(MessageBrokerInterface):
    """
    Apache Kafka message broker implementation
    
    Provides high-throughput, distributed messaging for
    large-scale event streaming scenarios.
    """
    
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.consumers: Dict[str, AIOKafkaConsumer] = {}
        self.topic_prefix = "bizosaas"
        self.logger = logger.bind(component="kafka_broker")
    
    async def initialize(self) -> None:
        """Initialize Kafka producer"""
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                compression_type="gzip"
            )
            
            await self.producer.start()
            self.logger.info("Kafka message broker initialized")
            
        except Exception as e:
            self.logger.error("Failed to initialize Kafka", error=str(e))
            raise
    
    async def publish(
        self, 
        routing_key: str, 
        message: str, 
        priority: int = 5
    ) -> bool:
        """Publish message to Kafka"""
        try:
            # Convert routing key to topic name
            topic = f"{self.topic_prefix}.{routing_key.replace('.', '_')}"
            
            # Prepare message
            message_data = {
                "content": message,
                "priority": priority,
                "routing_key": routing_key
            }
            
            # Send message
            await self.producer.send_and_wait(topic, message_data)
            
            self.logger.debug(
                "Message published to Kafka",
                topic=topic,
                routing_key=routing_key
            )
            
            return True
            
        except Exception as e:
            self.logger.error(
                "Failed to publish to Kafka",
                routing_key=routing_key,
                error=str(e)
            )
            return False
    
    async def subscribe(
        self, 
        routing_key: str, 
        callback: Callable[[str], None]
    ) -> str:
        """Subscribe to Kafka messages"""
        try:
            # Convert routing key to topic pattern
            topic_pattern = f"{self.topic_prefix}.{routing_key.replace('.', '_').replace('*', '.*')}"
            
            # Create consumer
            consumer = AIOKafkaConsumer(
                topic_pattern,
                bootstrap_servers=self.bootstrap_servers,
                group_id=f"bizosaas-eventbus-{routing_key}",
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest'
            )
            
            await consumer.start()
            
            # Create consumption task
            subscription_id = f"{routing_key}:{id(consumer)}"
            
            async def consume_messages():
                try:
                    async for message in consumer:
                        try:
                            await callback(message.value["content"])
                        except Exception as e:
                            self.logger.error(
                                "Kafka message processing failed",
                                topic=message.topic,
                                error=str(e)
                            )
                except Exception as e:
                    self.logger.error(
                        "Kafka consumer error",
                        subscription_id=subscription_id,
                        error=str(e)
                    )
            
            # Start consumption task
            task = asyncio.create_task(consume_messages())
            
            self.consumers[subscription_id] = {
                "consumer": consumer,
                "task": task,
                "routing_key": routing_key
            }
            
            self.logger.info(
                "Kafka subscription created",
                routing_key=routing_key,
                topic_pattern=topic_pattern
            )
            
            return subscription_id
            
        except Exception as e:
            self.logger.error(
                "Failed to subscribe to Kafka",
                routing_key=routing_key,
                error=str(e)
            )
            raise
    
    async def unsubscribe(self, routing_key: str) -> bool:
        """Unsubscribe from Kafka messages"""
        try:
            to_remove = []
            for sub_id, consumer_info in self.consumers.items():
                if consumer_info["routing_key"] == routing_key:
                    # Stop consumer
                    consumer_info["task"].cancel()
                    await consumer_info["consumer"].stop()
                    to_remove.append(sub_id)
            
            # Remove consumers
            for sub_id in to_remove:
                del self.consumers[sub_id]
            
            self.logger.info("Unsubscribed from Kafka", routing_key=routing_key)
            return True
            
        except Exception as e:
            self.logger.error(
                "Failed to unsubscribe from Kafka",
                routing_key=routing_key,
                error=str(e)
            )
            return False
    
    async def health_check(self) -> bool:
        """Check Kafka health"""
        try:
            if self.producer:
                # Try to get cluster metadata
                metadata = await self.producer.client.fetch_metadata()
                return len(metadata.brokers) > 0
            return False
        except Exception:
            return False
    
    async def close(self) -> None:
        """Close Kafka connections"""
        try:
            # Stop all consumers
            for consumer_info in self.consumers.values():
                consumer_info["task"].cancel()
                await consumer_info["consumer"].stop()
            
            self.consumers.clear()
            
            # Stop producer
            if self.producer:
                await self.producer.stop()
            
            self.logger.info("Kafka message broker closed")
            
        except Exception as e:
            self.logger.error("Error closing Kafka", error=str(e))


def create_message_broker(
    broker_type: str,
    **kwargs
) -> MessageBrokerInterface:
    """Factory function to create message brokers"""
    
    if broker_type.lower() == "redis":
        redis_client = kwargs.get("redis_client")
        if not redis_client:
            raise ValueError("Redis client required for Redis broker")
        return RedisMessageBroker(redis_client)
    
    elif broker_type.lower() == "rabbitmq":
        connection_url = kwargs.get("connection_url")
        if not connection_url:
            raise ValueError("Connection URL required for RabbitMQ broker")
        return RabbitMQBroker(connection_url)
    
    elif broker_type.lower() == "kafka":
        bootstrap_servers = kwargs.get("bootstrap_servers")
        if not bootstrap_servers:
            raise ValueError("Bootstrap servers required for Kafka broker")
        return KafkaBroker(bootstrap_servers)
    
    else:
        raise ValueError(f"Unsupported broker type: {broker_type}")