#!/bin/bash

# BizOSaaS Platform - Complete VPS Deployment & Cleanup Script
# Uses local pre-built images strategy
# VPS: 194.238.16.237
# Password: &k3civYG5Q6YPb

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  BizOSaaS Platform - VPS Deployment & Cleanup             ║${NC}"
echo -e "${BLUE}║  23 Services: Infrastructure + Backend + Frontend          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

VPS_HOST="root@194.238.16.237"
VPS_PASSWORD="&k3civYG5Q6YPb"
PROJECT_DIR="/root/bizosaas-platform"

# Compose file paths (using local images)
INFRA_COMPOSE="dokploy-infrastructure-staging-with-superset-build.yml"
BACKEND_COMPOSE="dokploy-backend-staging-local.yml"
FRONTEND_COMPOSE="dokploy-frontend-staging-local.yml"

echo -e "${YELLOW}📋 Deployment Strategy: Local Pre-Built Images${NC}"
echo -e "   Infrastructure: $INFRA_COMPOSE"
echo -e "   Backend: $BACKEND_COMPOSE"
echo -e "   Frontend: $FRONTEND_COMPOSE"
echo ""

# Function to run SSH commands
run_ssh() {
    sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no "$VPS_HOST" "$1"
}

# Function to copy files to VPS
copy_to_vps() {
    sshpass -p "$VPS_PASSWORD" scp -o StrictHostKeyChecking=no "$1" "$VPS_HOST:$2"
}

echo -e "${GREEN}Step 1: Checking VPS connectivity...${NC}"
if run_ssh "echo 'VPS connected successfully'"; then
    echo -e "${GREEN}✓ VPS connection successful${NC}"
else
    echo -e "${RED}✗ Failed to connect to VPS${NC}"
    echo -e "${YELLOW}Install sshpass: sudo apt-get install sshpass${NC}"
    exit 1
fi
echo ""

echo -e "${GREEN}Step 2: Pulling latest code from GitHub...${NC}"
run_ssh "cd $PROJECT_DIR && git pull origin main"
echo -e "${GREEN}✓ Code updated${NC}"
echo ""

echo -e "${GREEN}Step 3: Checking current services status...${NC}"
echo -e "${YELLOW}Currently running containers:${NC}"
run_ssh "docker ps --format 'table {{.Names}}\t{{.Status}}' | head -25"
echo ""

echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  PHASE 1: CLEANUP - Remove unused resources${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${RED}WARNING: This will remove:${NC}"
echo -e "  • All stopped containers"
echo -e "  • All unused images"
echo -e "  • All unused volumes"
echo -e "  • All unused networks"
echo ""
read -p "Do you want to proceed with cleanup? (yes/no): " CONFIRM_CLEANUP

if [ "$CONFIRM_CLEANUP" == "yes" ]; then
    echo -e "${GREEN}Cleaning up VPS...${NC}"

    echo -e "${BLUE}→ Stopping all non-infrastructure containers...${NC}"
    run_ssh "docker ps -q --filter 'name=bizosaas' | xargs -r docker stop" || true

    echo -e "${BLUE}→ Removing stopped containers...${NC}"
    run_ssh "docker container prune -f"

    echo -e "${BLUE}→ Removing unused images...${NC}"
    run_ssh "docker image prune -a -f"

    echo -e "${BLUE}→ Removing unused volumes...${NC}"
    run_ssh "docker volume prune -f"

    echo -e "${BLUE}→ Removing unused networks...${NC}"
    run_ssh "docker network prune -f"

    echo -e "${GREEN}✓ Cleanup complete${NC}"
    echo ""

    echo -e "${GREEN}Disk space after cleanup:${NC}"
    run_ssh "df -h | grep -E 'Filesystem|/dev/sda|/dev/vda'"
    echo ""
else
    echo -e "${YELLOW}Skipping cleanup${NC}"
    echo ""
fi

echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  PHASE 2: DEPLOYMENT - Deploy all 23 services${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${GREEN}Step 1: Deploy Infrastructure Layer (6 services)${NC}"
echo -e "${BLUE}Services: PostgreSQL, Redis, Vault, Temporal Server, Temporal UI, Superset${NC}"
run_ssh "cd $PROJECT_DIR && docker-compose -f $INFRA_COMPOSE up -d"
echo -e "${GREEN}✓ Infrastructure deployed${NC}"
echo ""

echo -e "${YELLOW}Waiting 30 seconds for infrastructure to initialize...${NC}"
sleep 30

echo -e "${GREEN}Step 2: Deploy Backend Layer (10 services)${NC}"
echo -e "${BLUE}Services: Brain Gateway, AI Agents, Auth, Wagtail, Saleor, Django CRM, etc.${NC}"
run_ssh "cd $PROJECT_DIR && docker-compose -f $BACKEND_COMPOSE up -d"
echo -e "${GREEN}✓ Backend deployed${NC}"
echo ""

echo -e "${YELLOW}Waiting 20 seconds for backend services to initialize...${NC}"
sleep 20

echo -e "${GREEN}Step 3: Deploy Frontend Layer (7 services)${NC}"
echo -e "${BLUE}Services: Bizoholic, ThrillRing, CorelDove, Client Portal, Admin, Directory, QuantTrade${NC}"
run_ssh "cd $PROJECT_DIR && docker-compose -f $FRONTEND_COMPOSE up -d"
echo -e "${GREEN}✓ Frontend deployed${NC}"
echo ""

echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  PHASE 3: VERIFICATION - Check all services${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${GREEN}Running services:${NC}"
run_ssh "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | head -30"
echo ""

echo -e "${GREEN}Service count by category:${NC}"
run_ssh "echo 'Infrastructure:' && docker ps --filter 'name=postgres|redis|vault|temporal|superset' --format '{{.Names}}' | wc -l"
run_ssh "echo 'Backend:' && docker ps --filter 'name=brain|saleor|wagtail|crm|auth|ai-agent|coreldove-backend|amazon|directory|quanttrade' --format '{{.Names}}' | wc -l"
run_ssh "echo 'Frontend:' && docker ps --filter 'name=bizoholic-frontend|thrillring|coreldove-frontend|client-portal|admin|directory-frontend|quanttrade-frontend' --format '{{.Names}}' | wc -l"
echo ""

echo -e "${GREEN}Testing Brain Gateway (Port 8001):${NC}"
BRAIN_STATUS=$(run_ssh "curl -s -o /dev/null -w '%{http_code}' http://localhost:8001/health || echo 'FAILED'")
if [ "$BRAIN_STATUS" == "200" ] || [ "$BRAIN_STATUS" == "404" ]; then
    echo -e "${GREEN}✓ Brain Gateway is responding (HTTP $BRAIN_STATUS)${NC}"
else
    echo -e "${RED}✗ Brain Gateway not responding (Status: $BRAIN_STATUS)${NC}"
fi
echo ""

echo -e "${GREEN}Checking service health:${NC}"
run_ssh "docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E 'unhealthy|Restarting' || echo 'All services healthy or no health checks configured'"
echo ""

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Deployment Complete                                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}🎉 Deployment Summary:${NC}"
echo -e "   • Infrastructure: 6 services"
echo -e "   • Backend: 10 services (routing through Brain Gateway: 8001)"
echo -e "   • Frontend: 7 services"
echo -e "   • Total: 23 services"
echo ""

echo -e "${YELLOW}📋 Access URLs:${NC}"
echo -e "   • Brain Gateway: http://194.238.16.237:8001"
echo -e "   • Bizoholic: http://194.238.16.237:3001"
echo -e "   • ThrillRing: http://194.238.16.237:3005"
echo -e "   • CorelDove: http://194.238.16.237:3002"
echo -e "   • Superset: http://194.238.16.237:8088"
echo -e "   • Temporal UI: http://194.238.16.237:8083"
echo ""

echo -e "${YELLOW}📊 Next Steps:${NC}"
echo -e "   1. Test Brain Gateway: curl http://194.238.16.237:8001/health"
echo -e "   2. Check all services: ssh root@194.238.16.237 'docker ps'"
echo -e "   3. View logs: ssh root@194.238.16.237 'docker logs bizosaas-brain-staging'"
echo -e "   4. Fix any issues and redeploy specific services"
echo ""

echo -e "${GREEN}✓ Script complete${NC}"
