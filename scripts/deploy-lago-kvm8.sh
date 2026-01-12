#!/bin/bash
set -e

# ═══════════════════════════════════════════════════════════════════════════
# Lago Billing Deployment Script for KVM8 Server (72.60.98.213)
# ═══════════════════════════════════════════════════════════════════════════

echo "🚀 Deploying Lago Billing Engine to KVM8 Server..."
echo "═══════════════════════════════════════════════════════════════════════════"

# Server details
SERVER_IP="72.60.98.213"
SERVER_USER="root"
DEPLOY_DIR="/opt/lago-billing"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Step 1: Preparing deployment files...${NC}"

# Create temporary deployment directory
TEMP_DIR=$(mktemp -d)
echo "Created temp directory: $TEMP_DIR"

# Copy necessary files
cp docker-compose.lago.yml "$TEMP_DIR/"
cp .env.lago "$TEMP_DIR/"

echo -e "${GREEN}✓ Files prepared${NC}"

echo -e "${BLUE}📤 Step 2: Uploading files to KVM8 server...${NC}"

# Create deployment directory on server
ssh ${SERVER_USER}@${SERVER_IP} "mkdir -p ${DEPLOY_DIR}"

# Upload files
scp "$TEMP_DIR/docker-compose.lago.yml" ${SERVER_USER}@${SERVER_IP}:${DEPLOY_DIR}/
scp "$TEMP_DIR/.env.lago" ${SERVER_USER}@${SERVER_IP}:${DEPLOY_DIR}/

echo -e "${GREEN}✓ Files uploaded${NC}"

echo -e "${BLUE}🔧 Step 3: Setting up Docker networks on server...${NC}"

ssh ${SERVER_USER}@${SERVER_IP} << 'ENDSSH'
# Create networks if they don't exist
docker network inspect brain-network >/dev/null 2>&1 || docker network create brain-network
docker network inspect dokploy-network >/dev/null 2>&1 || docker network create dokploy-network
echo "✓ Networks ready"
ENDSSH

echo -e "${GREEN}✓ Networks configured${NC}"

echo -e "${BLUE}🐳 Step 4: Deploying Lago services...${NC}"

ssh ${SERVER_USER}@${SERVER_IP} << ENDSSH
cd ${DEPLOY_DIR}

echo "Pulling latest Lago images..."
docker compose -f docker-compose.lago.yml --env-file .env.lago pull

echo "Starting Lago services..."
docker compose -f docker-compose.lago.yml --env-file .env.lago up -d

echo "Waiting for services to initialize..."
sleep 15

echo "Checking service status..."
docker compose -f docker-compose.lago.yml ps
ENDSSH

echo -e "${GREEN}✓ Deployment complete${NC}"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ Lago Billing Engine deployed successfully!${NC}"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "📍 Access Points:"
echo "   Dashboard: https://billing.bizoholic.net"
echo "   API:       https://lago-api.bizoholic.net"
echo ""
echo "🔍 Verify deployment:"
echo "   ssh ${SERVER_USER}@${SERVER_IP}"
echo "   cd ${DEPLOY_DIR}"
echo "   docker compose -f docker-compose.lago.yml ps"
echo ""
echo "📊 View logs:"
echo "   docker logs lago-api"
echo "   docker logs lago-front"
echo "   docker logs lago-worker"
echo ""
echo -e "${YELLOW}⚠️  Next Steps:${NC}"
echo "   1. Ensure DNS records point to ${SERVER_IP}:"
echo "      - billing.bizoholic.net → ${SERVER_IP}"
echo "      - lago-api.bizoholic.net → ${SERVER_IP}"
echo "   2. Access https://billing.bizoholic.net to create admin account"
echo "   3. Generate API key in Lago dashboard"
echo "   4. Update Brain Gateway with Lago API key"
echo ""

# Cleanup
rm -rf "$TEMP_DIR"
echo "Cleaned up temporary files"
