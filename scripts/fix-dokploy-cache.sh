#!/bin/bash
# Fix Dokploy Core Services Deployment - Clear Cache

echo "🔧 Fixing Dokploy Core Services deployment..."
echo ""

# SSH password (you'll be prompted)
SERVER="root@72.60.98.213"

echo "Step 1: Stopping Core Services containers..."
ssh $SERVER "cd /etc/dokploy/compose/bizosaascore-coreservices-cux333 && docker-compose down 2>/dev/null || true"

echo ""
echo "Step 2: Removing cached deployment directory..."
ssh $SERVER "rm -rf /etc/dokploy/compose/bizosaascore-coreservices-cux333"

echo ""
echo "✅ Cache cleared!"
echo ""
echo "📋 Next steps:"
echo "1. Go to Dokploy UI"
echo "2. Find 'Core Services' deployment"
echo "3. Click 'Redeploy'"
echo "4. It will re-clone from GitHub with the updated compose file"
echo ""
echo "Expected result: brain-gateway will deploy successfully (no auth-service error)"
