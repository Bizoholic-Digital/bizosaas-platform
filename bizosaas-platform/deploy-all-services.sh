#!/bin/bash
# Complete BizOSaaS Platform Deployment Script
# Deploys all 22 services to Dokploy staging environment

set -e

echo "=========================================="
echo "BizOSaaS Complete Deployment Script"
echo "Target: 22 services (6 infrastructure + 10 backend + 6 frontend)"
echo "=========================================="

# Configuration
DOKPLOY_URL="https://dk.bizoholic.com"
VPS_IP="194.238.16.237"
GITHUB_REPO="https://github.com/Bizoholic-Digital/bizosaas-platform.git"
BACKEND_COMPOSE="bizosaas-platform/dokploy-backend-staging.yml"
FRONTEND_COMPOSE="bizosaas-platform/dokploy-frontend-staging.yml"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Step 1: Checking infrastructure services...${NC}"
echo "Testing PostgreSQL..."
timeout 5 nc -zv $VPS_IP 5433 2>&1 | grep succeeded && echo -e "${GREEN}✓ PostgreSQL (5433)${NC}" || echo -e "${RED}✗ PostgreSQL (5433)${NC}"

echo "Testing Redis..."
timeout 5 nc -zv $VPS_IP 6380 2>&1 | grep succeeded && echo -e "${GREEN}✓ Redis (6380)${NC}" || echo -e "${RED}✗ Redis (6380)${NC}"

echo "Testing Superset..."
timeout 5 nc -zv $VPS_IP 8088 2>&1 | grep succeeded && echo -e "${GREEN}✓ Superset (8088)${NC}" || echo -e "${RED}✗ Superset (8088)${NC}"

echo ""
echo -e "${YELLOW}Step 2: Backend Services Deployment${NC}"
echo "=========================================="
echo "Services to deploy:"
echo "  1. Saleor (8000)"
echo "  2. Brain API (8001)"
echo "  3. Wagtail CMS (8002)"
echo "  4. Django CRM (8003)"
echo "  5. Business Directory Backend (8004)"
echo "  6. CorelDove Backend (8005)"
echo "  7. Auth Service (8006)"
echo "  8. Temporal Integration (8007)"
echo "  9. AI Agents (8008)"
echo "  10. Amazon Sourcing (8009)"
echo ""
echo "Deployment Options:"
echo ""
echo "OPTION A: SSH Deployment (if you have SSH access)"
echo "----------------------------------------"
echo "ssh root@$VPS_IP << 'ENDSSH'
cd /root/bizosaas-platform || mkdir -p /root/bizosaas-platform
git clone $GITHUB_REPO . || git pull
docker compose -f $BACKEND_COMPOSE up -d --build
ENDSSH"
echo ""
echo "OPTION B: Dokploy UI Deployment (recommended)"
echo "----------------------------------------"
echo "1. Open: $DOKPLOY_URL"
echo "2. Login with: bizoholic.digital@gmail.com"
echo "3. Navigate to: Projects → Backend Services"
echo "4. Settings → Compose File Path: $BACKEND_COMPOSE"
echo "5. Click: Deploy"
echo "6. Wait: 40 minutes"
echo ""
echo "OPTION C: Dokploy API Deployment (if API key works)"
echo "----------------------------------------"
echo "curl -X POST \"$DOKPLOY_URL/api/compose.deploy\" \\"
echo "  -H \"Authorization: Bearer YOUR_API_TOKEN\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"composeId\":\"backend-services-id\"}'"
echo ""

read -p "Press Enter after backend deployment is complete..."

echo ""
echo -e "${YELLOW}Step 3: Frontend Services Deployment${NC}"
echo "=========================================="
echo "Services to deploy:"
echo "  1. Bizoholic Frontend (3000)"
echo "  2. Client Portal (3001)"
echo "  3. CorelDove Frontend (3002)"
echo "  4. Business Directory Frontend (3003)"
echo "  5. ThrillRing Gaming (3005)"
echo "  6. Admin Dashboard (3009)"
echo ""
echo "Deployment via Dokploy UI:"
echo "1. Navigate to: Projects → Frontend Services"
echo "2. Settings → Compose File Path: $FRONTEND_COMPOSE"
echo "3. Click: Deploy"
echo "4. Wait: 30 minutes"
echo ""

read -p "Press Enter after frontend deployment is complete..."

echo ""
echo -e "${YELLOW}Step 4: Verifying All Services${NC}"
echo "=========================================="

# Function to check service
check_service() {
    local name=$1
    local port=$2
    timeout 5 nc -zv $VPS_IP $port 2>&1 | grep succeeded && echo -e "${GREEN}✓ $name ($port)${NC}" || echo -e "${RED}✗ $name ($port)${NC}"
}

echo "Infrastructure (6 services):"
check_service "PostgreSQL" 5433
check_service "Redis" 6380
check_service "Vault" 8201
check_service "Temporal Server" 7234
check_service "Temporal UI" 8083
check_service "Superset" 8088

echo ""
echo "Backend (10 services):"
check_service "Saleor" 8000
check_service "Brain API" 8001
check_service "Wagtail CMS" 8002
check_service "Django CRM" 8003
check_service "Business Directory Backend" 8004
check_service "CorelDove Backend" 8005
check_service "Auth Service" 8006
check_service "Temporal Integration" 8007
check_service "AI Agents" 8008
check_service "Amazon Sourcing" 8009

echo ""
echo "Frontend (6 services):"
check_service "Bizoholic" 3000
check_service "Client Portal" 3001
check_service "CorelDove" 3002
check_service "Business Directory" 3003
check_service "ThrillRing" 3005
check_service "Admin Dashboard" 3009

echo ""
echo -e "${YELLOW}Step 5: Domain Configuration${NC}"
echo "=========================================="
echo "Configure these domains in Dokploy:"
echo ""
echo "1. stg.bizoholic.com → Port 3000 (Bizoholic)"
echo "2. stg.portal.bizoholic.com → Port 3001 (Client Portal)"
echo "3. stg.coreldove.com → Port 3002 (CorelDove)"
echo "4. stg.directory.bizoholic.com → Port 3003 (Business Directory)"
echo "5. stg.thrillring.com → Port 3005 (ThrillRing)"
echo "6. stg.admin.bizoholic.com → Port 3009 (Admin Dashboard)"
echo ""
echo "Enable SSL for all domains via Let's Encrypt"
echo ""

echo -e "${GREEN}=========================================="
echo "Deployment Script Complete!"
echo "==========================================${NC}"
echo ""
echo "Next Steps:"
echo "1. Follow the deployment options above"
echo "2. Configure domains in Dokploy UI"
echo "3. Run: bash verify-staging-deployment.sh"
echo ""
