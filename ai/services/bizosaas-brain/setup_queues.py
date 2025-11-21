#!/usr/bin/env python3
"""
RabbitMQ Queue Setup for BizOSaaS CrewAI Agent Workers
Creates task queues with proper configuration for AI agent orchestration

This script creates:
- 8 AUTO-PROCESSING queues for automated AI tasks
- 3 HITL queues for human approval workflows
- Dead Letter Exchange (DLX) for failed messages
- Priority queues with TTL configuration
"""

import pika
import sys
import os
from typing import List, Tuple

# RabbitMQ connection parameters from environment or defaults
# Service name from Dokploy infrastructure deployment
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'infrastructureservices-rabbitmq-gktndk')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'BizOSaaS2025@RabbitMQ!Secure')

# Auto-Processing Queues (AI handles automatically)
# Format: (queue_name, max_priority, ttl_milliseconds)
AUTO_QUEUES: List[Tuple[str, int, int]] = [
    ('auto_orders', 10, 3600000),          # High priority, 1h TTL
    ('auto_support_tickets', 10, 7200000), # High priority, 2h TTL
    ('auto_inventory', 5, 1800000),        # Medium priority, 30min TTL
    ('auto_marketing', 5, 14400000),       # Medium priority, 4h TTL
    ('auto_seo', 5, 7200000),              # Medium priority, 2h TTL
    ('auto_social_media', 5, 3600000),     # Medium priority, 1h TTL
    ('auto_email_campaigns', 5, 7200000),  # Medium priority, 2h TTL
    ('auto_analytics', 3, 14400000),       # Low priority, 4h TTL
]

# HITL Queues (Human approval required)
# Format: (queue_name, max_priority, ttl_milliseconds)
HITL_QUEUES: List[Tuple[str, int, int]] = [
    ('hitl_approval', 10, 86400000),    # Critical, 24h TTL
    ('hitl_exceptions', 10, 43200000),  # Critical, 12h TTL
    ('hitl_training', 5, 604800000),    # Training data, 7d TTL
]

def create_connection():
    """Establish connection to RabbitMQ"""
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            virtual_host=RABBITMQ_VHOST,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )

        connection = pika.BlockingConnection(parameters)
        print(f"✅ Connected to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        return connection

    except Exception as e:
        print(f"❌ Failed to connect to RabbitMQ: {e}")
        print(f"   Host: {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        print(f"   VHost: {RABBITMQ_VHOST}")
        print(f"   User: {RABBITMQ_USER}")
        sys.exit(1)

def setup_dead_letter_exchange(channel):
    """Create Dead Letter Exchange for failed messages"""
    try:
        # Declare DLX exchange
        channel.exchange_declare(
            exchange='dlx',
            exchange_type='topic',
            durable=True
        )
        print("✅ Created Dead Letter Exchange (dlx)")

    except Exception as e:
        print(f"⚠️  DLX might already exist: {e}")

def create_queue(channel, queue_name: str, max_priority: int, ttl: int):
    """
    Create a queue with DLX, priority, and TTL configuration

    Args:
        channel: RabbitMQ channel
        queue_name: Name of the queue
        max_priority: Maximum priority level (1-10)
        ttl: Time-to-live in milliseconds
    """
    try:
        # Create main queue with DLX and priority
        channel.queue_declare(
            queue=queue_name,
            durable=True,
            arguments={
                'x-message-ttl': ttl,
                'x-max-priority': max_priority,
                'x-dead-letter-exchange': 'dlx',
                'x-dead-letter-routing-key': f'{queue_name}.dlq'
            }
        )

        # Create corresponding dead letter queue
        dlq_name = f'{queue_name}.dlq'
        channel.queue_declare(
            queue=dlq_name,
            durable=True
        )

        # Bind DLQ to DLX
        channel.queue_bind(
            queue=dlq_name,
            exchange='dlx',
            routing_key=f'{queue_name}.dlq'
        )

        ttl_seconds = ttl / 1000
        ttl_display = f"{ttl_seconds/3600:.1f}h" if ttl_seconds >= 3600 else f"{ttl_seconds/60:.0f}min"

        print(f"✅ Created queue: {queue_name}")
        print(f"   - Priority: {max_priority}")
        print(f"   - TTL: {ttl_display}")
        print(f"   - DLQ: {dlq_name}")

    except Exception as e:
        print(f"❌ Failed to create queue {queue_name}: {e}")

def main():
    """Main setup function"""
    print("=" * 70)
    print("BizOSaaS RabbitMQ Queue Setup")
    print("Creating queues for CrewAI agent workers")
    print("=" * 70)
    print()

    # Establish connection
    connection = create_connection()
    channel = connection.channel()

    # Setup Dead Letter Exchange
    print("\n📦 Setting up Dead Letter Exchange...")
    setup_dead_letter_exchange(channel)

    # Create AUTO queues
    print(f"\n🤖 Creating {len(AUTO_QUEUES)} AUTO-PROCESSING queues...")
    for queue_name, max_priority, ttl in AUTO_QUEUES:
        create_queue(channel, queue_name, max_priority, ttl)

    # Create HITL queues
    print(f"\n👤 Creating {len(HITL_QUEUES)} HITL (Human-in-the-Loop) queues...")
    for queue_name, max_priority, ttl in HITL_QUEUES:
        create_queue(channel, queue_name, max_priority, ttl)

    # Summary
    total_queues = len(AUTO_QUEUES) + len(HITL_QUEUES)
    total_dlqs = total_queues

    print()
    print("=" * 70)
    print("✅ Queue Setup Complete!")
    print("=" * 70)
    print(f"Created {total_queues} main queues:")
    print(f"  - {len(AUTO_QUEUES)} AUTO-PROCESSING queues (AI automation)")
    print(f"  - {len(HITL_QUEUES)} HITL queues (human approval)")
    print(f"Created {total_dlqs} dead letter queues (DLQ)")
    print(f"Total queues: {total_queues + total_dlqs}")
    print()
    print("🎯 Next Steps:")
    print("  1. Deploy agent workers to consume from these queues")
    print("  2. Configure brain-gateway to publish tasks to queues")
    print("  3. Monitor queue depths via RabbitMQ Management UI")
    print()

    # Close connection
    connection.close()

if __name__ == '__main__':
    main()
