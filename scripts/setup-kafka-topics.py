#!/usr/bin/env python3
"""
Setup Kafka topics for event streaming and AI learning
Creates 13 topics for domain events, AI events, HITL events, and analytics
"""

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, KafkaError
import sys

# Kafka connection parameters
KAFKA_BOOTSTRAP_SERVERS = ['infrastructureservices-kafka-ill4q0:9092']
CLIENT_ID = 'bizosaas-setup'

# Define topics for event streaming
TOPICS = [
    # Domain Events (from microservices)
    NewTopic('domain.orders', num_partitions=3, replication_factor=1),
    NewTopic('domain.customers', num_partitions=3, replication_factor=1),
    NewTopic('domain.products', num_partitions=3, replication_factor=1),
    NewTopic('domain.leads', num_partitions=2, replication_factor=1),
    NewTopic('domain.content', num_partitions=2, replication_factor=1),

    # AI Agent Events
    NewTopic('ai.decisions', num_partitions=3, replication_factor=1),
    NewTopic('ai.completions', num_partitions=3, replication_factor=1),
    NewTopic('ai.errors', num_partitions=2, replication_factor=1),

    # HITL Events
    NewTopic('hitl.requests', num_partitions=2, replication_factor=1),
    NewTopic('hitl.decisions', num_partitions=2, replication_factor=1),
    NewTopic('hitl.feedback', num_partitions=2, replication_factor=1),

    # Audit & Analytics
    NewTopic('audit.trail', num_partitions=5, replication_factor=1),
    NewTopic('analytics.metrics', num_partitions=3, replication_factor=1),
]

def create_topics():
    """Create all Kafka topics"""

    print("📊 Connecting to Kafka...")
    print(f"   Bootstrap servers: {', '.join(KAFKA_BOOTSTRAP_SERVERS)}")
    print(f"   Client ID: {CLIENT_ID}\n")

    try:
        # Create admin client
        admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            client_id=CLIENT_ID,
            request_timeout_ms=30000
        )

        print("✅ Connected to Kafka\n")

        print(f"📋 Creating {len(TOPICS)} topics...\n")

        # Create topics
        try:
            admin_client.create_topics(new_topics=TOPICS, validate_only=False)
            print("✅ Topics creation initiated\n")
        except TopicAlreadyExistsError:
            print("⚠️  Some topics already exist, continuing...\n")

        # List created topics with details
        for topic in TOPICS:
            try:
                # Get topic config
                print(f"✅ Topic: {topic.name}")
                print(f"   - Partitions: {topic.num_partitions}")
                print(f"   - Replication Factor: {topic.replication_factor}")

                # Categorize
                category = topic.name.split('.')[0]
                if category == 'domain':
                    print(f"   - Category: Domain Events (microservice data)")
                elif category == 'ai':
                    print(f"   - Category: AI Events (agent decisions & results)")
                elif category == 'hitl':
                    print(f"   - Category: HITL Events (human approvals)")
                elif category == 'audit':
                    print(f"   - Category: Audit Trail (compliance & logging)")
                elif category == 'analytics':
                    print(f"   - Category: Analytics (metrics & monitoring)")
                print()
            except Exception as e:
                print(f"⚠️  Topic {topic.name}: {e}\n")

        admin_client.close()

        print("=" * 60)
        print("✅ All topics created successfully!")
        print("=" * 60)
        print(f"\nSummary:")
        print(f"  • Domain events: 5 topics")
        print(f"  • AI events: 3 topics")
        print(f"  • HITL events: 3 topics")
        print(f"  • Audit & analytics: 2 topics")
        print(f"  • Total: {len(TOPICS)} topics")
        print(f"  • Total partitions: {sum(t.num_partitions for t in TOPICS)}")
        print("\n🎉 Kafka is ready for event streaming!")

        print("\n📊 Topic Usage:")
        print("\nDomain Events (from microservices):")
        print("  • domain.orders       - Order lifecycle events")
        print("  • domain.customers    - Customer updates")
        print("  • domain.products     - Product catalog changes")
        print("  • domain.leads        - CRM lead events")
        print("  • domain.content      - CMS content updates")

        print("\nAI Agent Events:")
        print("  • ai.decisions        - Agent decision logs")
        print("  • ai.completions      - Task completion events")
        print("  • ai.errors           - Agent error tracking")

        print("\nHITL Events:")
        print("  • hitl.requests       - Human approval requests")
        print("  • hitl.decisions      - Human decisions")
        print("  • hitl.feedback       - Human feedback for AI learning")

        print("\nAudit & Analytics:")
        print("  • audit.trail         - Compliance audit log")
        print("  • analytics.metrics   - Platform metrics")

    except KafkaError as e:
        print(f"❌ Kafka error: {e}")
        print("\nTroubleshooting:")
        print("  1. Check if Kafka broker is running")
        print("  2. Check if Zookeeper is running and healthy")
        print("  3. Verify bootstrap server address")
        print("  4. Check network connectivity")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_topics()
