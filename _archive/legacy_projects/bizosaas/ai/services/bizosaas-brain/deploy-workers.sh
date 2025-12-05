#!/bin/bash
# Deploy CrewAI Agent Workers to KVM4 via Docker Swarm

set -e

echo "========================================"
echo "CrewAI Agent Workers Deployment"
echo "========================================"
echo ""

# Configuration
REMOTE_HOST="72.60.219.244"
REMOTE_USER="root"
REMOTE_PASS="&k3civYG5Q6YPb"
IMAGE_NAME="bizosaas-agent-workers"
IMAGE_TAG="latest"
REGISTRY="ghcr.io/bizoholic-digital"
FULL_IMAGE="${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"

# GitHub Container Registry credentials
GHCR_TOKEN="GITHUB_TOKEN_REDACTED"
GHCR_USER="alagiri.rajesh@gmail.com"

# Infrastructure services
RABBITMQ_HOST="infrastructureservices-rabbitmq-gktndk"
KAFKA_HOST="infrastructureservices-kafka-ill4q0"
REDIS_HOST="infrastructureservices-bizosaasredis-w0gw3g"

# AI API Keys
OPENAI_API_KEY="OPENAI_KEY_REDACTED"
OPENROUTER_API_KEY="OPENROUTER_KEY_REDACTED"

echo "Step 1: Building Docker image locally..."
cd /home/alagiri/projects/bizosaas-platform/bizosaas/ai/services/bizosaas-brain

# Build with standard Docker (no BuildKit)
docker build \
  -t ${FULL_IMAGE} \
  -f Dockerfile.workers \
  . 2>&1 | tee /tmp/worker-build-$(date +%Y%m%d-%H%M%S).log

echo ""
echo "Step 2: Logging into GitHub Container Registry..."
echo "${GHCR_TOKEN}" | docker login ghcr.io -u "${GHCR_USER}" --password-stdin

echo ""
echo "Step 3: Pushing image to GHCR..."
docker push ${FULL_IMAGE}

echo ""
echo "Step 4: Deploying to KVM4 server via SSH..."

# Create deployment script for remote execution
cat > /tmp/deploy-workers-remote.sh <<'REMOTE_SCRIPT'
#!/bin/bash
set -e

IMAGE_NAME="{{IMAGE_NAME}}"
FULL_IMAGE="{{FULL_IMAGE}}"
RABBITMQ_HOST="{{RABBITMQ_HOST}}"
KAFKA_HOST="{{KAFKA_HOST}}"
REDIS_HOST="{{REDIS_HOST}}"
OPENAI_API_KEY="{{OPENAI_API_KEY}}"
OPENROUTER_API_KEY="{{OPENROUTER_API_KEY}}"

echo "Pulling latest image..."
docker pull ${FULL_IMAGE}

echo "Removing old worker services if they exist..."
docker service rm agent-workers-order 2>/dev/null || true
docker service rm agent-workers-support 2>/dev/null || true
docker service rm agent-workers-marketing 2>/dev/null || true

echo "Creating Order Processing Workers (4 replicas)..."
docker service create \
  --name agent-workers-order \
  --network dokploy-network \
  --replicas 4 \
  --env QUEUE_NAME=auto_orders \
  --env RABBITMQ_HOST=${RABBITMQ_HOST} \
  --env RABBITMQ_PORT=5672 \
  --env RABBITMQ_USER=admin \
  --env RABBITMQ_PASS="BizOSaaS2025@RabbitMQ!Secure" \
  --env KAFKA_BOOTSTRAP_SERVERS=${KAFKA_HOST}:9092 \
  --env REDIS_HOST=${REDIS_HOST} \
  --env REDIS_PORT=6379 \
  --env OPENAI_API_KEY=${OPENAI_API_KEY} \
  --env OPENROUTER_API_KEY=${OPENROUTER_API_KEY} \
  --restart-condition on-failure \
  --restart-max-attempts 3 \
  ${FULL_IMAGE} \
  python workers/order_agent.py

echo "Creating Support Ticket Workers (6 replicas)..."
docker service create \
  --name agent-workers-support \
  --network dokploy-network \
  --replicas 6 \
  --env QUEUE_NAME=auto_support_tickets \
  --env RABBITMQ_HOST=${RABBITMQ_HOST} \
  --env RABBITMQ_PORT=5672 \
  --env RABBITMQ_USER=admin \
  --env RABBITMQ_PASS="BizOSaaS2025@RabbitMQ!Secure" \
  --env KAFKA_BOOTSTRAP_SERVERS=${KAFKA_HOST}:9092 \
  --env REDIS_HOST=${REDIS_HOST} \
  --env REDIS_PORT=6379 \
  --env OPENAI_API_KEY=${OPENAI_API_KEY} \
  --env OPENROUTER_API_KEY=${OPENROUTER_API_KEY} \
  --restart-condition on-failure \
  --restart-max-attempts 3 \
  ${FULL_IMAGE} \
  python workers/support_agent.py

echo "Creating Marketing Campaign Workers (4 replicas)..."
docker service create \
  --name agent-workers-marketing \
  --network dokploy-network \
  --replicas 4 \
  --env QUEUE_NAME=auto_marketing \
  --env RABBITMQ_HOST=${RABBITMQ_HOST} \
  --env RABBITMQ_PORT=5672 \
  --env RABBITMQ_USER=admin \
  --env RABBITMQ_PASS="BizOSaaS2025@RabbitMQ!Secure" \
  --env KAFKA_BOOTSTRAP_SERVERS=${KAFKA_HOST}:9092 \
  --env REDIS_HOST=${REDIS_HOST} \
  --env REDIS_PORT=6379 \
  --env OPENAI_API_KEY=${OPENAI_API_KEY} \
  --env OPENROUTER_API_KEY=${OPENROUTER_API_KEY} \
  --restart-condition on-failure \
  --restart-max-attempts 3 \
  ${FULL_IMAGE} \
  python workers/marketing_agent.py

echo ""
echo "Worker services created successfully!"
echo ""
echo "Service Status:"
docker service ls | grep agent-workers

echo ""
echo "Deployment complete!"
REMOTE_SCRIPT

# Replace placeholders
sed -i "s|{{IMAGE_NAME}}|${IMAGE_NAME}|g" /tmp/deploy-workers-remote.sh
sed -i "s|{{FULL_IMAGE}}|${FULL_IMAGE}|g" /tmp/deploy-workers-remote.sh
sed -i "s|{{RABBITMQ_HOST}}|${RABBITMQ_HOST}|g" /tmp/deploy-workers-remote.sh
sed -i "s|{{KAFKA_HOST}}|${KAFKA_HOST}|g" /tmp/deploy-workers-remote.sh
sed -i "s|{{REDIS_HOST}}|${REDIS_HOST}|g" /tmp/deploy-workers-remote.sh
sed -i "s|{{OPENAI_API_KEY}}|${OPENAI_API_KEY}|g" /tmp/deploy-workers-remote.sh
sed -i "s|{{OPENROUTER_API_KEY}}|${OPENROUTER_API_KEY}|g" /tmp/deploy-workers-remote.sh

# Copy and execute on remote server
sshpass -p "${REMOTE_PASS}" scp -o StrictHostKeyChecking=no \
  /tmp/deploy-workers-remote.sh ${REMOTE_USER}@${REMOTE_HOST}:/tmp/

sshpass -p "${REMOTE_PASS}" ssh -o StrictHostKeyChecking=no \
  ${REMOTE_USER}@${REMOTE_HOST} \
  "chmod +x /tmp/deploy-workers-remote.sh && /tmp/deploy-workers-remote.sh"

echo ""
echo "========================================"
echo "Deployment Complete!"
echo "========================================"
echo ""
echo "Deployed Services:"
echo "- agent-workers-order (4 replicas)"
echo "- agent-workers-support (6 replicas)"
echo "- agent-workers-marketing (4 replicas)"
echo ""
echo "Total: 14 worker replicas processing tasks from RabbitMQ"
echo ""
