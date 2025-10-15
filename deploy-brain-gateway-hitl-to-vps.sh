#!/bin/bash
# Deploy Brain Gateway v2.1.0-HITL to VPS Staging Environment
# Date: October 14, 2025

set -e

echo "==================================================================="
echo "Brain Gateway v2.1.0-HITL Deployment to VPS Staging"
echo "==================================================================="

VPS_IP="194.238.16.237"
VPS_USER="root"
IMAGE_NAME="bizosaas/brain-gateway:v2.1.0-hitl"
CONTAINER_NAME="bizosaas-brain-staging"

echo ""
echo "Step 1: Saving Docker image locally..."
docker save $IMAGE_NAME | gzip > /tmp/brain-gateway-v2.1.0-hitl.tar.gz
echo "✅ Image saved to /tmp/brain-gateway-v2.1.0-hitl.tar.gz"

echo ""
echo "Step 2: Transferring image to VPS ($VPS_IP)..."
scp /tmp/brain-gateway-v2.1.0-hitl.tar.gz $VPS_USER@$VPS_IP:/tmp/
echo "✅ Image transferred to VPS"

echo ""
echo "Step 3: Loading image on VPS..."
ssh $VPS_USER@$VPS_IP "docker load < /tmp/brain-gateway-v2.1.0-hitl.tar.gz && rm /tmp/brain-gateway-v2.1.0-hitl.tar.gz"
echo "✅ Image loaded on VPS"

echo ""
echo "Step 4: Stopping existing Brain Gateway container..."
ssh $VPS_USER@$VPS_IP "docker stop $CONTAINER_NAME 2>/dev/null || true"
ssh $VPS_USER@$VPS_IP "docker rm $CONTAINER_NAME 2>/dev/null || true"
echo "✅ Old container removed"

echo ""
echo "Step 5: Starting new Brain Gateway with HITL..."
ssh $VPS_USER@$VPS_IP << 'EOF'
docker run -d \
  --name bizosaas-brain-staging \
  --network dokploy-network \
  -p 8001:8001 \
  -e REDIS_URL=redis://194.238.16.237:6380/0 \
  -e DATABASE_URL=postgresql://admin:BizOSaaS2025\!StagingDB@194.238.16.237:5433/bizosaas_staging \
  -e ENVIRONMENT=staging \
  -e LOG_LEVEL=INFO \
  --restart unless-stopped \
  bizosaas/brain-gateway:v2.1.0-hitl
EOF
echo "✅ New Brain Gateway container started"

echo ""
echo "Step 6: Waiting for service to start..."
sleep 5

echo ""
echo "Step 7: Verifying deployment..."
ssh $VPS_USER@$VPS_IP "docker ps --filter name=bizosaas-brain-staging --format 'Container: {{.Names}} - Status: {{.Status}}'"
echo ""
ssh $VPS_USER@$VPS_IP "docker logs bizosaas-brain-staging --tail 10"

echo ""
echo "Step 8: Testing health endpoint..."
ssh $VPS_USER@$VPS_IP "curl -s http://localhost:8001/health | jq ."

echo ""
echo "Step 9: Testing HITL workflows endpoint..."
ssh $VPS_USER@$VPS_IP "curl -s http://localhost:8001/api/brain/hitl/workflows | jq '.total'"

echo ""
echo "==================================================================="
echo "✅ Deployment Complete!"
echo "==================================================================="
echo ""
echo "Brain Gateway v2.1.0-HITL is now running on VPS at:"
echo "  - Health: http://$VPS_IP:8001/health"
echo "  - HITL Workflows: http://$VPS_IP:8001/api/brain/hitl/workflows"
echo "  - API Docs: http://$VPS_IP:8001/docs"
echo ""
echo "Next Steps:"
echo "1. Test HITL endpoints from VPS"
echo "2. Integrate AI agents with HITL routing"
echo "3. Connect frontend applications"
echo "4. Test end-to-end workflows"
echo ""
echo "Cleanup local temp file..."
rm -f /tmp/brain-gateway-v2.1.0-hitl.tar.gz
echo "✅ Cleanup complete"
