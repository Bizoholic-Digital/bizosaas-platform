#!/bin/bash
# Deploy Kafka cluster for event streaming

set -e

echo "📊 Deploying Kafka Cluster..."
echo "=============================="

ssh root@72.60.219.244 << 'EOF'

# Remove existing services if they exist
docker service rm kafka 2>/dev/null || true
docker service rm zookeeper 2>/dev/null || true
sleep 5

echo "1️⃣  Deploying Zookeeper..."
# Step 1: Deploy Zookeeper (Kafka dependency)
docker service create \
  --name zookeeper \
  --network dokploy-network \
  --replicas 1 \
  --publish 2181:2181 \
  --env ZOOKEEPER_CLIENT_PORT=2181 \
  --env ZOOKEEPER_TICK_TIME=2000 \
  --mount type=volume,source=zookeeper-data,target=/var/lib/zookeeper/data \
  --mount type=volume,source=zookeeper-logs,target=/var/lib/zookeeper/log \
  confluentinc/cp-zookeeper:7.5.0

echo "⏰ Waiting for Zookeeper to be ready (30 seconds)..."
sleep 30

echo ""
echo "2️⃣  Deploying Kafka..."
# Step 2: Deploy Kafka
docker service create \
  --name kafka \
  --network dokploy-network \
  --replicas 2 \
  --publish 9092:9092 \
  --env KAFKA_BROKER_ID=1 \
  --env KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
  --env KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 \
  --env KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=2 \
  --env KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=2 \
  --env KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=2 \
  --env KAFKA_AUTO_CREATE_TOPICS_ENABLE=true \
  --mount type=volume,source=kafka-data,target=/var/lib/kafka/data \
  confluentinc/cp-kafka:7.5.0

echo ""
echo "✅ Kafka cluster deployed successfully!"
echo ""
echo "📊 Service Details:"
docker service ps zookeeper --no-trunc
docker service ps kafka --no-trunc

echo ""
echo "⏰ Waiting for Kafka to be ready (30 seconds)..."

EOF

sleep 30

echo ""
echo "✅ Kafka deployment complete!"
echo "📊 2 Kafka brokers running"
echo "🔗 Internal URL: kafka:9092"
