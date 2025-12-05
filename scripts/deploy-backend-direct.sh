#!/bin/bash
# Direct deployment bypassing Dokploy

echo "=========================================="
echo "Direct Backend Deployment (9 Services)"
echo "=========================================="
echo ""

cd /home/alagiri/projects/bizoholic

echo "Deploying all 9 backend services..."
docker-compose -f dokploy-backend-staging.yml up -d

echo ""
echo "Waiting for services to start..."
sleep 10

echo ""
echo "Checking service status..."
docker-compose -f dokploy-backend-staging.yml ps

echo ""
echo "=========================================="
echo "Deployment complete!"
echo "=========================================="
