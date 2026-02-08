#!/bin/bash
# Deploy ONLY missing/broken services to VPS via Dokploy
# VPS: 194.238.16.237 | Dokploy: dk.bizoholic.com

set -e

API_TOKEN="agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi"
DOKPLOY_URL="https://dk.bizoholic.com"

echo "🎯 Targeted Deployment - Only Missing/Broken Services"
echo "=================================================="
echo ""

# Since API is returning Unauthorized, we'll use docker commands via SSH
# This is more reliable for immediate deployment

echo "📋 Services that need attention:"
echo "1. Fix: 2 restarting containers (temporal, auth)"
echo "2. Deploy: 6 frontend services (ALL missing)"
echo "3. Deploy: Superset (22nd service)"
echo ""

# Generate SSH commands for VPS deployment
cat > /tmp/vps-deploy-commands.sh << 'SSHEOF'
#!/bin/bash
echo "🔧 Step 1: Fix Restarting Containers"
docker restart f41566ffd086  # temporal-server
docker restart 343f493bcbd0  # auth-service
sleep 5
docker ps | grep -E "f41566ffd086|343f493bcbd0"

echo ""
echo "📦 Step 2: Deploy Frontend Services (6 missing)"
cd /root/bizosaas-platform || cd /opt/bizosaas-platform || echo "Repository not found - need to clone"

# Pull latest changes from GitHub
git pull origin main

# Deploy all 6 frontend services
docker-compose -f dokploy-frontend-staging.yml pull
docker-compose -f dokploy-frontend-staging.yml up -d --no-build

echo ""
echo "📊 Step 3: Deploy Superset (22nd service)"
# Check if superset-staging.yml exists, if not create it
if [ ! -f superset-staging.yml ]; then
  cat > superset-staging.yml << 'SUPERSET'
version: '3.8'
services:
  superset:
    image: apache/superset:latest
    container_name: bizosaas-superset-staging
    ports:
      - "8088:8088"
    environment:
      - SUPERSET_SECRET_KEY=bizosaas-superset-secret-2025
    networks:
      - dokploy-network
    restart: unless-stopped
    command:
      - /bin/sh
      - -c
      - |
        superset db upgrade
        superset fab create-admin --username admin --firstname Admin --lastname User --email admin@bizosaas.com --password admin123 || true
        superset init
        superset run -h 0.0.0.0 -p 8088 --with-threads --reload

networks:
  dokploy-network:
    external: true
SUPERSET
fi

docker-compose -f superset-staging.yml up -d

echo ""
echo "✅ Verification"
echo "Total containers (should be ~22):"
docker ps --format "table {{.Names}}\t{{.Status}}" | wc -l

echo ""
echo "Running services:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | head -25
SSHEOF

chmod +x /tmp/vps-deploy-commands.sh

echo "📝 Generated deployment commands in: /tmp/vps-deploy-commands.sh"
echo ""
echo "🚀 To execute on VPS, run:"
echo "   ssh root@194.238.16.237 'bash -s' < /tmp/vps-deploy-commands.sh"
echo ""
echo "   OR copy and execute manually on VPS"
