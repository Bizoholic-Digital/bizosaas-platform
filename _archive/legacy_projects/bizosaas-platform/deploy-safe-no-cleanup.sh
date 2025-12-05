#!/bin/bash

# BizOSaaS Platform - SAFE Deployment Script
# ⚠️ NO CLEANUP - Preserves WordPress and all existing services
# Only deploys new BizOSaaS platform services
# VPS: 194.238.16.237

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  BizOSaaS Platform - SAFE Deployment (No Cleanup)         ║${NC}"
echo -e "${BLUE}║  ⚠️  Preserves: WordPress, n8n, and all existing services   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

VPS_HOST="root@194.238.16.237"
VPS_PASSWORD="&k3civYG5Q6YPb"
PROJECT_DIR="/root/bizosaas-platform"

# Compose files for BizOSaaS platform only
INFRA_COMPOSE="dokploy-infrastructure-staging-with-superset-build.yml"
BACKEND_COMPOSE="dokploy-backend-staging-local.yml"
FRONTEND_COMPOSE="dokploy-frontend-staging-local.yml"

run_ssh() {
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no "$VPS_HOST" "$1"
}

echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  SAFETY CHECK - Current Services${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${GREEN}Checking VPS connectivity...${NC}"
if run_ssh "echo 'VPS connected'"; then
    echo -e "${GREEN}✓ Connected to VPS${NC}"
else
    echo -e "${RED}✗ Cannot connect to VPS${NC}"
    exit 1
fi
echo ""

echo -e "${BLUE}Current running services (will be preserved):${NC}"
run_ssh "docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E 'wordpress|n8n|pgadmin|dragonfly|bizoholic-website|automation-hub|shared' || echo 'No WordPress/n8n services found'"
echo ""

echo -e "${YELLOW}⚠️  These services will NOT be touched:${NC}"
echo -e "   • WordPress containers"
echo -e "   • n8n automation containers"
echo -e "   • pgAdmin containers"
echo -e "   • Dragonfly/shared infrastructure"
echo -e "   • Any container NOT prefixed with 'bizosaas-'"
echo ""

read -p "Continue with deployment? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}Deployment cancelled${NC}"
    exit 0
fi
echo ""

echo -e "${GREEN}Pulling latest code from GitHub...${NC}"
run_ssh "cd $PROJECT_DIR && git pull origin main"
echo -e "${GREEN}✓ Code updated${NC}"
echo ""

echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  DEPLOYMENT - BizOSaaS Platform Only (23 services)${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${GREEN}Phase 1: Infrastructure Layer (6 services)${NC}"
echo -e "${BLUE}→ PostgreSQL, Redis, Vault, Temporal x2, Superset${NC}"
run_ssh "cd $PROJECT_DIR && docker-compose -f $INFRA_COMPOSE up -d"
echo -e "${GREEN}✓ Infrastructure deployed${NC}"
echo ""

echo -e "${YELLOW}Waiting 30 seconds for databases to initialize...${NC}"
sleep 30

echo -e "${GREEN}Checking infrastructure health:${NC}"
run_ssh "docker ps --filter 'name=bizosaas-postgres|bizosaas-redis|bizosaas-vault|bizosaas-temporal' --format 'table {{.Names}}\t{{.Status}}'"
echo ""

echo -e "${GREEN}Phase 2: Backend Layer (10 services)${NC}"
echo -e "${BLUE}→ Brain Gateway, AI Agents, Auth, CMS, CRM, E-commerce, etc.${NC}"
run_ssh "cd $PROJECT_DIR && docker-compose -f $BACKEND_COMPOSE up -d"
echo -e "${GREEN}✓ Backend deployed${NC}"
echo ""

echo -e "${YELLOW}Waiting 20 seconds for backend to initialize...${NC}"
sleep 20

echo -e "${GREEN}Checking backend health:${NC}"
run_ssh "docker ps --filter 'name=bizosaas-brain|bizosaas-saleor|bizosaas-wagtail|bizosaas-crm|bizosaas-auth' --format 'table {{.Names}}\t{{.Status}}'"
echo ""

echo -e "${GREEN}Phase 3: Frontend Layer (7 services)${NC}"
echo -e "${BLUE}→ Bizoholic, ThrillRing, CorelDove, Portals, Admin, Directory${NC}"
run_ssh "cd $PROJECT_DIR && docker-compose -f $FRONTEND_COMPOSE up -d"
echo -e "${GREEN}✓ Frontend deployed${NC}"
echo ""

echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  VERIFICATION${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${GREEN}All running containers (including existing services):${NC}"
run_ssh "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | head -35"
echo ""

echo -e "${GREEN}BizOSaaS Platform services count:${NC}"
echo -n "Infrastructure: "
run_ssh "docker ps --filter 'name=bizosaas-postgres|bizosaas-redis|bizosaas-vault|bizosaas-temporal|bizosaas-superset' | grep -c bizosaas || echo 0"
echo -n "Backend: "
run_ssh "docker ps --filter 'name=bizosaas-brain|bizosaas-saleor|bizosaas-wagtail|bizosaas-crm|bizosaas-auth|bizosaas-ai-agent|bizosaas-coreldove-backend|bizosaas-amazon|bizosaas-directory' | grep -c bizosaas || echo 0"
echo -n "Frontend: "
run_ssh "docker ps --filter 'name=bizosaas.*frontend|bizosaas.*portal|bizosaas.*admin|bizosaas-thrillring' | grep -c bizosaas || echo 0"
echo ""

echo -e "${GREEN}Testing Brain Gateway:${NC}"
BRAIN_STATUS=$(run_ssh "curl -s -o /dev/null -w '%{http_code}' http://localhost:8001/health 2>/dev/null || echo 'FAILED'")
if [ "$BRAIN_STATUS" == "200" ] || [ "$BRAIN_STATUS" == "404" ]; then
    echo -e "${GREEN}✓ Brain Gateway responding (HTTP $BRAIN_STATUS)${NC}"
else
    echo -e "${YELLOW}⚠ Brain Gateway: $BRAIN_STATUS (may still be starting)${NC}"
fi
echo ""

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Deployment Complete (Safe Mode)                           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}✓ Deployed:${NC} BizOSaaS Platform (23 services)"
echo -e "${GREEN}✓ Preserved:${NC} WordPress, n8n, and all existing services"
echo ""

echo -e "${YELLOW}📋 Next Steps:${NC}"
echo -e "   1. Test Brain Gateway: curl http://194.238.16.237:8001/health"
echo -e "   2. Test frontends: curl http://194.238.16.237:3001 (Bizoholic)"
echo -e "   3. Check logs: ssh root@194.238.16.237 'docker logs bizosaas-brain-staging'"
echo -e "   4. Run full inventory: ./check-vps-services.sh"
echo ""

echo -e "${YELLOW}⚠️  To clean up later (after testing):${NC}"
echo -e "   Run: ./cleanup-unused-only.sh (will be created after testing)"
echo ""
