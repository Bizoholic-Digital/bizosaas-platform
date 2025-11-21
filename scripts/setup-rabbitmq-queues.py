#!/usr/bin/env python3
"""
Setup RabbitMQ queues for CrewAI agent task distribution
Creates 11 queues: 8 AUTO (AI auto-processes) + 3 HITL (human approval required)
"""

import pika
import sys

# RabbitMQ connection parameters
RABBITMQ_HOST = 'infrastructureservices-rabbitmq-gktndk'  # Docker service name in dokploy-network
RABBITMQ_PORT = 5672
RABBITMQ_VHOST = '/'
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = 'guest'

# Auto-Processing Queues (AI handles automatically)
AUTO_QUEUES = [
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
HITL_QUEUES = [
    ('hitl_approval', 10, 86400000),    # Critical, 24h TTL
    ('hitl_exceptions', 10, 43200000),  # Critical, 12h TTL
    ('hitl_training', 5, 604800000),    # Training data, 7d TTL
]

def create_queues():
    """Create all RabbitMQ queues with DLX and priority settings"""

    print("🐰 Connecting to RabbitMQ...")
    print(f"   Host: {RABBITMQ_HOST}:{RABBITMQ_PORT}")
    print(f"   VHost: {RABBITMQ_VHOST}")

    try:
        # Establish connection
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
        channel = connection.channel()

        print("✅ Connected to RabbitMQ\n")

        # Create Dead Letter Exchange for failed messages
        print("📋 Creating Dead Letter Exchange (DLX)...")
        channel.exchange_declare(
            exchange='dlx',
            exchange_type='topic',
            durable=True
        )
        print("✅ DLX created\n")

        all_queues = AUTO_QUEUES + HITL_QUEUES

        print(f"📋 Creating {len(all_queues)} queues...\n")

        for queue_name, max_priority, ttl in all_queues:
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
            channel.queue_declare(
                queue=f'{queue_name}.dlq',
                durable=True
            )

            # Bind DLQ to DLX
            channel.queue_bind(
                queue=f'{queue_name}.dlq',
                exchange='dlx',
                routing_key=f'{queue_name}.dlq'
            )

            ttl_seconds = ttl / 1000
            ttl_display = f"{ttl_seconds/3600:.1f}h" if ttl_seconds >= 3600 else f"{ttl_seconds/60:.0f}min"

            print(f"✅ Created: {queue_name}")
            print(f"   - Priority: {max_priority}")
            print(f"   - TTL: {ttl_display}")
            print(f"   - DLQ: {queue_name}.dlq\n")

        connection.close()

        print("=" * 60)
        print("✅ All queues created successfully!")
        print("=" * 60)
        print(f"\nSummary:")
        print(f"  • AUTO queues: {len(AUTO_QUEUES)}")
        print(f"  • HITL queues: {len(HITL_QUEUES)}")
        print(f"  • Total queues: {len(all_queues)}")
        print(f"  • Dead letter queues: {len(all_queues)}")
        print(f"  • Grand total: {len(all_queues) * 2} queues + 1 DLX exchange")
        print("\n🎉 RabbitMQ is ready for CrewAI agents!")

    except pika.exceptions.AMQPConnectionError as e:
        print(f"❌ Connection error: {e}")
        print("\nTroubleshooting:")
        print("  1. Check if RabbitMQ service is running")
        print("  2. Verify connection details (host, port, vhost, credentials)")
        print("  3. Check network connectivity from this container to RabbitMQ")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_queues()
