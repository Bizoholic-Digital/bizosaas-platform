#!/usr/bin/env python3
"""
Kafka Topics Setup for BizOSaaS Event Streaming
Creates event topics for AI agent orchestration and domain events

This script creates:
- 5 Domain event topics (orders, customers, products, leads, content)
- 3 AI agent event topics (decisions, completions, errors)
- 3 HITL event topics (requests, decisions, feedback)
- 2 System topics (audit trail, analytics metrics)
"""

import sys
import os
from typing import List, Tuple
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, KafkaError

# Kafka connection parameters from environment or defaults
# Service name from Dokploy infrastructure deployment
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    'KAFKA_BOOTSTRAP_SERVERS',
    'infrastructureservices-kafka-ill4q0:9092'
)

# Topic definitions: (name, partitions, replication_factor)
DOMAIN_TOPICS: List[Tuple[str, int, int]] = [
    ('domain.orders', 3, 2),          # Order domain events
    ('domain.customers', 3, 2),       # Customer domain events
    ('domain.products', 3, 2),        # Product domain events
    ('domain.leads', 2, 2),           # Lead generation events
    ('domain.content', 2, 2),         # Content management events
]

AI_AGENT_TOPICS: List[Tuple[str, int, int]] = [
    ('ai.decisions', 3, 2),           # AI decision events
    ('ai.completions', 3, 2),         # Task completion events
    ('ai.errors', 2, 2),              # Error and failure events
]

HITL_TOPICS: List[Tuple[str, int, int]] = [
    ('hitl.requests', 2, 2),          # Human approval requests
    ('hitl.decisions', 2, 2),         # Human decisions
    ('hitl.feedback', 2, 2),          # Human feedback for learning
]

SYSTEM_TOPICS: List[Tuple[str, int, int]] = [
    ('audit.trail', 5, 2),            # Complete audit log
    ('analytics.metrics', 3, 2),      # Performance metrics
]

def create_admin_client():
    """Create Kafka admin client"""
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            client_id='bizosaas-setup',
            request_timeout_ms=30000,
            connections_max_idle_ms=540000
        )
        print(f"✅ Connected to Kafka at {KAFKA_BOOTSTRAP_SERVERS}")
        return admin_client

    except Exception as e:
        print(f"❌ Failed to connect to Kafka: {e}")
        print(f"   Bootstrap servers: {KAFKA_BOOTSTRAP_SERVERS}")
        sys.exit(1)

def create_topics(admin_client, topics: List[Tuple[str, int, int]], category: str):
    """
    Create Kafka topics

    Args:
        admin_client: Kafka admin client
        topics: List of (topic_name, num_partitions, replication_factor)
        category: Category name for logging
    """
    new_topics = []

    for topic_name, num_partitions, replication_factor in topics:
        new_topics.append(
            NewTopic(
                name=topic_name,
                num_partitions=num_partitions,
                replication_factor=replication_factor
            )
        )

    try:
        # Create topics
        result = admin_client.create_topics(
            new_topics=new_topics,
            validate_only=False,
            timeout_ms=30000
        )

        # Check results
        for topic_name, future in result.topic_futures.items():
            try:
                future.result()  # Will raise exception if creation failed
                topic_info = next(
                    (t for t in topics if t[0] == topic_name),
                    None
                )
                if topic_info:
                    _, partitions, rf = topic_info
                    print(f"✅ Created topic: {topic_name}")
                    print(f"   - Partitions: {partitions}")
                    print(f"   - Replication Factor: {rf}")

            except TopicAlreadyExistsError:
                print(f"⚠️  Topic already exists: {topic_name}")

            except Exception as e:
                print(f"❌ Failed to create topic {topic_name}: {e}")

    except Exception as e:
        print(f"❌ Error creating {category} topics: {e}")

def list_topics(admin_client):
    """List all topics"""
    try:
        metadata = admin_client.list_topics(timeout=10)
        topics = list(metadata)
        print(f"\n📋 Total topics in cluster: {len(topics)}")

        # Filter BizOSaaS topics
        bizosaas_topics = [t for t in topics if any(
            t.startswith(prefix)
            for prefix in ['domain.', 'ai.', 'hitl.', 'audit.', 'analytics.']
        )]

        if bizosaas_topics:
            print(f"📋 BizOSaaS topics ({len(bizosaas_topics)}):")
            for topic in sorted(bizosaas_topics):
                print(f"   - {topic}")

    except Exception as e:
        print(f"⚠️  Could not list topics: {e}")

def main():
    """Main setup function"""
    print("=" * 70)
    print("BizOSaaS Kafka Topics Setup")
    print("Creating event streaming topics for AI orchestration")
    print("=" * 70)
    print()

    # Create admin client
    admin_client = create_admin_client()

    # Create domain event topics
    print(f"\n🏢 Creating {len(DOMAIN_TOPICS)} DOMAIN event topics...")
    create_topics(admin_client, DOMAIN_TOPICS, "domain")

    # Create AI agent topics
    print(f"\n🤖 Creating {len(AI_AGENT_TOPICS)} AI AGENT event topics...")
    create_topics(admin_client, AI_AGENT_TOPICS, "AI agent")

    # Create HITL topics
    print(f"\n👤 Creating {len(HITL_TOPICS)} HITL event topics...")
    create_topics(admin_client, HITL_TOPICS, "HITL")

    # Create system topics
    print(f"\n⚙️  Creating {len(SYSTEM_TOPICS)} SYSTEM event topics...")
    create_topics(admin_client, SYSTEM_TOPICS, "system")

    # List all topics
    list_topics(admin_client)

    # Summary
    total_topics = (
        len(DOMAIN_TOPICS) +
        len(AI_AGENT_TOPICS) +
        len(HITL_TOPICS) +
        len(SYSTEM_TOPICS)
    )

    total_partitions = sum(
        partitions
        for topics in [DOMAIN_TOPICS, AI_AGENT_TOPICS, HITL_TOPICS, SYSTEM_TOPICS]
        for _, partitions, _ in topics
    )

    print()
    print("=" * 70)
    print("✅ Kafka Topics Setup Complete!")
    print("=" * 70)
    print(f"Created {total_topics} topics:")
    print(f"  - {len(DOMAIN_TOPICS)} Domain event topics")
    print(f"  - {len(AI_AGENT_TOPICS)} AI agent topics")
    print(f"  - {len(HITL_TOPICS)} HITL topics")
    print(f"  - {len(SYSTEM_TOPICS)} System topics")
    print(f"Total partitions: {total_partitions}")
    print()
    print("🎯 Event Flow:")
    print("  1. Services publish domain events → domain.* topics")
    print("  2. AI agents publish decisions → ai.* topics")
    print("  3. HITL workflows publish → hitl.* topics")
    print("  4. All events archived → audit.trail")
    print("  5. Metrics aggregated → analytics.metrics")
    print()
    print("🔗 Next Steps:")
    print("  1. Configure brain-gateway to publish events")
    print("  2. Configure agent workers to consume and publish")
    print("  3. Set up stream processing (optional)")
    print("  4. Monitor topic lag and throughput")
    print()

    # Close admin client
    admin_client.close()

if __name__ == '__main__':
    main()
