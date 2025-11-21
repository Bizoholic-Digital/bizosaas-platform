#!/bin/bash
# Deploy API Gateway to KVM4

set -e

cd /home/alagiri/projects/bizosaas-platform/backend/services/api-gateway

echo "🏗️  Building API Gateway Docker image..."
docker build -t ghcr.io/bizoholic-digital/bizosaas-api-gateway:latest .

echo "📦 Pushing to GHCR..."
docker push ghcr.io/bizoholic-digital/bizosaas-api-gateway:latest

echo "🚀 Deploying to KVM4..."
ssh root@72.60.219.244 << 'EOF'

  # Remove existing service if it exists
  docker service rm api-gateway 2>/dev/null || true

  # Wait for cleanup
  sleep 5

  # Create API Gateway service
  docker service create \
    --name api-gateway \
    --network dokploy-network \
    --replicas 2 \
    --publish 8080:8080 \
    --with-registry-auth \
    --constraint 'node.role==manager' \
    --update-parallelism 1 \
    --update-delay 10s \
    --label "traefik.enable=true" \
    --label "traefik.http.routers.api-gateway.rule=Host(\`api.bizoholic.com\`) || Host(\`api.coreldove.com\`)" \
    --label "traefik.http.routers.api-gateway.entrypoints=websecure" \
    --label "traefik.http.routers.api-gateway.tls.certresolver=letsencrypt" \
    --label "traefik.http.services.api-gateway.loadbalancer.server.port=8080" \
    ghcr.io/bizoholic-digital/bizosaas-api-gateway:latest

  echo "✅ API Gateway deployed"

  # Check service status
  sleep 10
  docker service ps api-gateway --no-trunc

EOF

echo ""
echo "✅ Deployment complete!"
echo "🔗 API Gateway accessible at:"
echo "   - https://api.bizoholic.com"
echo "   - https://api.coreldove.com"
echo ""
echo "📊 Test with: curl https://api.bizoholic.com/health"
