"""
Base CrewAI Worker Class
Foundation for all agent workers with RabbitMQ consumption and Kafka event publishing
"""

import pika
import json
import logging
import os
import signal
import sys
from datetime import datetime
from typing import Callable, Dict, Any, Optional
from crewai import Agent, Task, Crew
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CrewAIWorker:
    """
    Base class for CrewAI agent workers

    Features:
    - RabbitMQ message consumption with retry logic
    - CrewAI agent integration for task processing
    - Kafka event publishing for results
    - Error handling with Dead Letter Queue
    - Graceful shutdown handling
    - Metrics collection
    """

    def __init__(
        self,
        queue_name: str,
        agent: Agent,
        result_handler: Optional[Callable[[str, Dict[str, Any]], None]] = None
    ):
        """
        Initialize worker

        Args:
            queue_name: RabbitMQ queue to consume from
            agent: CrewAI Agent instance
            result_handler: Optional callback for handling results
        """
        self.queue_name = queue_name
        self.agent = agent
        self.result_handler = result_handler
        self.connection = None
        self.channel = None
        self.kafka_producer = None
        self.should_stop = False

        # Configuration from environment
        self.rabbitmq_host = os.getenv('RABBITMQ_HOST', 'infrastructureservices-rabbitmq-gktndk')
        self.rabbitmq_port = int(os.getenv('RABBITMQ_PORT', '5672'))
        self.rabbitmq_user = os.getenv('RABBITMQ_USER', 'admin')
        self.rabbitmq_pass = os.getenv('RABBITMQ_PASS', 'BizOSaaS2025@RabbitMQ!Secure')
        self.rabbitmq_vhost = os.getenv('RABBITMQ_VHOST', '/')

        self.kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'infrastructureservices-kafka-ill4q0:9092')

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        # Connect to infrastructure
        self._connect_rabbitmq()
        self._connect_kafka()

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.should_stop = True
        if self.channel and self.channel.is_open:
            self.channel.stop_consuming()

    def _connect_rabbitmq(self):
        """Establish RabbitMQ connection with retry logic"""
        max_retries = 5
        retry_count = 0

        while retry_count < max_retries and not self.should_stop:
            try:
                credentials = pika.PlainCredentials(
                    self.rabbitmq_user,
                    self.rabbitmq_pass
                )
                parameters = pika.ConnectionParameters(
                    host=self.rabbitmq_host,
                    port=self.rabbitmq_port,
                    virtual_host=self.rabbitmq_vhost,
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )

                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
                self.channel.basic_qos(prefetch_count=1)

                logger.info(f"✅ Connected to RabbitMQ at {self.rabbitmq_host}:{self.rabbitmq_port}")
                logger.info(f"📥 Consuming from queue: {self.queue_name}")
                return

            except Exception as e:
                retry_count += 1
                logger.error(f"❌ RabbitMQ connection failed (attempt {retry_count}/{max_retries}): {e}")
                if retry_count < max_retries:
                    import time
                    time.sleep(5 * retry_count)  # Exponential backoff
                else:
                    raise

    def _connect_kafka(self):
        """Establish Kafka producer connection"""
        try:
            self.kafka_producer = KafkaProducer(
                bootstrap_servers=self.kafka_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',
                retries=3,
                max_in_flight_requests_per_connection=1
            )
            logger.info(f"✅ Connected to Kafka at {self.kafka_servers}")

        except Exception as e:
            logger.error(f"⚠️  Kafka connection failed: {e}")
            logger.warning("Worker will continue without Kafka event publishing")
            self.kafka_producer = None

    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process task with CrewAI agent

        Args:
            task_data: Task data from queue

        Returns:
            Result dictionary with status and output
        """
        start_time = datetime.now()
        task_id = task_data.get('id', 'unknown')

        try:
            logger.info(f"🤖 Processing task {task_id} with agent: {self.agent.role}")

            # Create CrewAI task
            task = Task(
                description=task_data.get('description', 'Process task'),
                agent=self.agent,
                expected_output=task_data.get('expected_output', 'Task completion result')
            )

            # Execute with CrewAI
            crew = Crew(
                agents=[self.agent],
                tasks=[task],
                verbose=True
            )

            result = crew.kickoff()

            execution_time = (datetime.now() - start_time).total_seconds()

            return {
                'status': 'completed',
                'task_id': task_id,
                'result': str(result),
                'execution_time_seconds': execution_time,
                'agent_role': self.agent.role,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"❌ Task {task_id} processing failed: {e}")

            return {
                'status': 'failed',
                'task_id': task_id,
                'error': str(e),
                'error_type': type(e).__name__,
                'execution_time_seconds': execution_time,
                'agent_role': self.agent.role,
                'timestamp': datetime.now().isoformat()
            }

    def publish_event(self, topic: str, event: Dict[str, Any], key: Optional[str] = None):
        """
        Publish event to Kafka

        Args:
            topic: Kafka topic name
            event: Event data
            key: Optional message key for partitioning
        """
        if not self.kafka_producer:
            logger.warning(f"Kafka not available, event not published to {topic}")
            return

        try:
            future = self.kafka_producer.send(topic, value=event, key=key)
            future.get(timeout=10)  # Wait for confirmation
            logger.debug(f"📤 Published event to {topic}")

        except KafkaError as e:
            logger.error(f"❌ Failed to publish to Kafka topic {topic}: {e}")
        except Exception as e:
            logger.error(f"❌ Unexpected error publishing to Kafka: {e}")

    def callback(self, ch, method, properties, body):
        """
        RabbitMQ message callback

        Args:
            ch: Channel
            method: Method
            properties: Message properties
            body: Message body
        """
        try:
            # Parse task data
            task_data = json.loads(body)
            task_id = task_data.get('id', 'unknown')

            logger.info(f"📥 Received task: {task_id} from queue: {self.queue_name}")

            # Process task with CrewAI agent
            result = self.process_task(task_data)

            # Publish completion event to Kafka
            if result['status'] == 'completed':
                self.publish_event('ai.completions', result, key=task_id)
            else:
                self.publish_event('ai.errors', result, key=task_id)

            # Call result handler if provided
            if self.result_handler:
                try:
                    self.result_handler(task_id, result)
                except Exception as e:
                    logger.error(f"Result handler error: {e}")

            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"✅ Task {task_id} completed with status: {result['status']}")

        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON in message: {e}")
            # Reject message, don't requeue (goes to DLQ)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")
            # Reject and requeue for retry
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def start(self):
        """Start consuming messages from queue"""
        logger.info("=" * 70)
        logger.info(f"🎧 CrewAI Worker Started")
        logger.info(f"   Queue: {self.queue_name}")
        logger.info(f"   Agent: {self.agent.role}")
        logger.info(f"   Goal: {self.agent.goal}")
        logger.info("=" * 70)

        try:
            self.channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self.callback
            )

            logger.info("⏳ Waiting for tasks... (Press Ctrl+C to exit)")
            self.channel.start_consuming()

        except KeyboardInterrupt:
            logger.info("🛑 Received interrupt signal, stopping...")
            self.should_stop = True

        except Exception as e:
            logger.error(f"❌ Consumer error: {e}")

        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup connections"""
        logger.info("🧹 Cleaning up connections...")

        try:
            if self.channel and self.channel.is_open:
                self.channel.close()
                logger.info("✅ RabbitMQ channel closed")
        except Exception as e:
            logger.error(f"Error closing channel: {e}")

        try:
            if self.connection and self.connection.is_open:
                self.connection.close()
                logger.info("✅ RabbitMQ connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")

        try:
            if self.kafka_producer:
                self.kafka_producer.flush()
                self.kafka_producer.close()
                logger.info("✅ Kafka producer closed")
        except Exception as e:
            logger.error(f"Error closing Kafka producer: {e}")

        logger.info("👋 Worker shutdown complete")
