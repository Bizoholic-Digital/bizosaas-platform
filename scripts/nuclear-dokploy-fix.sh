#!/bin/bash
# Ultimate Dokploy Cache Fix - Nuclear Option

echo "🔧 Ultimate Dokploy Cache Fix..."
echo ""

SERVER="root@72.60.98.213"

echo "Step 1: Stop ALL Core Services containers..."
ssh $SERVER "docker ps -a | grep bizosaascore | awk '{print \$1}' | xargs -r docker stop"

echo ""
echo "Step 2: Remove ALL Core Services containers..."
ssh $SERVER "docker ps -a | grep bizosaascore | awk '{print \$1}' | xargs -r docker rm"

echo ""
echo "Step 3: Remove ALL cached directories..."
ssh $SERVER "rm -rf /etc/dokploy/compose/bizosaascore-*"

echo ""
echo "Step 4: Remove any Dokploy database cache (if exists)..."
ssh $SERVER "docker exec dokploy-dokploy-1 rm -rf /app/.cache 2>/dev/null || true"

echo ""
echo "✅ Nuclear cache clear complete!"
echo ""
echo "📋 Next steps:"
echo "1. In Dokploy UI, DELETE the 'Core Services' deployment completely"
echo "2. Create a NEW deployment called 'Brain Gateway'"
echo "3. Use docker-compose.core.yml"
echo "4. Deploy"
echo ""
echo "This will force Dokploy to start fresh with no cached config."
