#!/bin/bash
# Deploy RabbitMQ for CrewAI agent task queues

set -e

echo "🐰 Deploying RabbitMQ Cluster..."
echo "================================"

ssh root@72.60.219.244 << 'EOF'

# Remove existing service if it exists
docker service rm rabbitmq 2>/dev/null || true
sleep 5

# Create RabbitMQ service with management UI
docker service create \
  --name rabbitmq \
  --network dokploy-network \
  --replicas 2 \
  --publish 5672:5672 \
  --publish 15672:15672 \
  --env RABBITMQ_DEFAULT_USER=admin \
  --env RABBITMQ_DEFAULT_PASS='BizOSaaS2025@RabbitMQ!Secure' \
  --env RABBITMQ_DEFAULT_VHOST=bizosaas \
  --env RABBITMQ_NODENAME=rabbit@rabbitmq \
  --mount type=volume,source=rabbitmq-data,target=/var/lib/rabbitmq \
  --label "traefik.enable=true" \
  --label "traefik.http.routers.rabbitmq.rule=Host(\`admin.bizoholic.com\`) && PathPrefix(\`/rabbitmq\`)" \
  --label "traefik.http.routers.rabbitmq.entrypoints=websecure" \
  --label "traefik.http.routers.rabbitmq.tls.certresolver=letsencrypt" \
  --label "traefik.http.middlewares.rabbitmq-strip.stripprefix.prefixes=/rabbitmq" \
  --label "traefik.http.routers.rabbitmq.middlewares=rabbitmq-strip@docker" \
  --label "traefik.http.services.rabbitmq.loadbalancer.server.port=15672" \
  rabbitmq:3.13-management

echo ""
echo "✅ RabbitMQ deployed successfully!"
echo ""
echo "📊 Service Details:"
docker service ps rabbitmq --no-trunc

echo ""
echo "🌐 Management UI: https://admin.bizoholic.com/rabbitmq"
echo "🔐 Username: admin"
echo "🔐 Password: BizOSaaS2025@RabbitMQ!Secure"
echo ""
echo "⏰ Waiting for RabbitMQ to be ready (30 seconds)..."

EOF

sleep 30

echo ""
echo "✅ RabbitMQ deployment complete!"
