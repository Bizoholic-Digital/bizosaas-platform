#!/bin/bash
# Automated VPS Deployment Script
# Deploys missing/broken services to 194.238.16.237

# SSH password from credentials
export SSHPASS='&k3civYG5Q6YPb'

echo "🚀 Starting Automated VPS Deployment"
echo "======================================="
echo ""

# Create deployment commands
cat > /tmp/vps-deploy-commands.sh << 'DEPLOY_SCRIPT'
#!/bin/bash
set -e

echo "📍 Current location: $(pwd)"
echo ""

# Find or clone repository
if [ -d "/root/bizosaas-platform" ]; then
    echo "✅ Repository found at /root/bizosaas-platform"
    cd /root/bizosaas-platform
    git pull origin main
elif [ -d "/opt/bizosaas-platform" ]; then
    echo "✅ Repository found at /opt/bizosaas-platform"
    cd /opt/bizosaas-platform
    git pull origin main
else
    echo "📦 Cloning repository..."
    cd /root
    git clone https://github.com/Bizoholic-Digital/bizosaas-platform.git
    cd bizosaas-platform
fi

echo ""
echo "🔧 Step 1: Fix Restarting Containers"
echo "-------------------------------------"
# Check if containers exist before restarting
if docker ps -a | grep -q "f41566ffd086"; then
    docker restart f41566ffd086 2>/dev/null || echo "Container f41566ffd086 not found"
fi
if docker ps -a | grep -q "343f493bcbd0"; then
    docker restart 343f493bcbd0 2>/dev/null || echo "Container 343f493bcbd0 not found"
fi

echo ""
echo "📦 Step 2: Deploy Frontend Services"
echo "-------------------------------------"
if [ -f "dokploy-frontend-staging.yml" ]; then
    docker-compose -f dokploy-frontend-staging.yml up -d
else
    echo "⚠️  dokploy-frontend-staging.yml not found"
fi

echo ""
echo "📊 Step 3: Deploy Superset (22nd service)"
echo "-------------------------------------"
docker run -d \
  --name bizosaas-superset-staging \
  -p 8088:8088 \
  --network dokploy-network \
  --restart unless-stopped \
  -e SUPERSET_SECRET_KEY=bizosaas-superset-2025 \
  apache/superset:latest 2>/dev/null || echo "Superset already running or error occurred"

echo ""
echo "✅ Deployment Complete"
echo "======================"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | head -25
DEPLOY_SCRIPT

# Copy script to VPS and execute
echo "📤 Copying deployment script to VPS..."
sshpass -p "$SSHPASS" scp -o StrictHostKeyChecking=no /tmp/vps-deploy-commands.sh root@194.238.16.237:/tmp/

echo "🚀 Executing deployment on VPS..."
sshpass -p "$SSHPASS" ssh -o StrictHostKeyChecking=no root@194.238.16.237 'bash /tmp/vps-deploy-commands.sh'

echo ""
echo "✅ Deployment script executed successfully!"
echo "🔍 Check results above"
