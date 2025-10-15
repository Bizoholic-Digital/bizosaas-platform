#!/bin/bash

# Direct Staging Deployment Script
# Deploys staging environment to VPS using local Docker Compose files

echo "🚀 Direct Staging Deployment to VPS"
echo "===================================="

VPS_IP="194.238.16.237"
VPS_USER="root"  # Adjust if different
COMPOSE_PROJECT="bizosaas-staging"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📋 Deployment Configuration:${NC}"
echo "VPS IP: $VPS_IP"
echo "Project: $COMPOSE_PROJECT"
echo "Files: dokploy-infrastructure-staging.yml, dokploy-backend-staging.yml, dokploy-frontend-staging.yml"
echo ""

# Function to execute command on VPS
execute_on_vps() {
    local command=$1
    local description=$2

    echo -e "${BLUE}🔧 $description${NC}"
    echo "Command: $command"

    # For now, we'll show what would be executed
    echo -e "${YELLOW}[WOULD EXECUTE ON VPS]: $command${NC}"
    echo ""
}

# Function to copy file to VPS
copy_to_vps() {
    local local_file=$1
    local remote_path=$2
    local description=$3

    echo -e "${BLUE}📁 $description${NC}"
    echo "Local: $local_file"
    echo "Remote: $remote_path"

    # For now, we'll show what would be copied
    echo -e "${YELLOW}[WOULD COPY TO VPS]: $local_file -> $remote_path${NC}"
    echo ""
}

echo -e "${GREEN}🎯 PHASE 1: INFRASTRUCTURE DEPLOYMENT${NC}"
echo "======================================"

# Check if infrastructure file exists
if [ -f "dokploy-infrastructure-staging.yml" ]; then
    echo -e "${GREEN}✅ Found: dokploy-infrastructure-staging.yml${NC}"

    copy_to_vps "dokploy-infrastructure-staging.yml" "/opt/staging/infrastructure/docker-compose.yml" "Copy infrastructure configuration"

    execute_on_vps "cd /opt/staging/infrastructure && docker-compose -p ${COMPOSE_PROJECT}-infra up -d" "Deploy infrastructure services"

    execute_on_vps "docker-compose -p ${COMPOSE_PROJECT}-infra ps" "Check infrastructure container status"

    echo -e "${GREEN}Infrastructure services (6 containers):${NC}"
    echo "- PostgreSQL (port 5432)"
    echo "- Redis (port 6379)"
    echo "- Vault (port 8200)"
    echo "- Temporal Server (port 7233)"
    echo "- Temporal UI (port 8082)"
    echo "- Temporal Integration (port 8009)"

else
    echo -e "${RED}❌ Missing: dokploy-infrastructure-staging.yml${NC}"
fi

echo ""
echo -e "${GREEN}🎯 PHASE 2: BACKEND SERVICES DEPLOYMENT${NC}"
echo "======================================="

# Check if backend file exists
if [ -f "dokploy-backend-staging.yml" ]; then
    echo -e "${GREEN}✅ Found: dokploy-backend-staging.yml${NC}"

    copy_to_vps "dokploy-backend-staging.yml" "/opt/staging/backend/docker-compose.yml" "Copy backend configuration"

    execute_on_vps "cd /opt/staging/backend && docker-compose -p ${COMPOSE_PROJECT}-backend up -d" "Deploy backend services"

    execute_on_vps "docker-compose -p ${COMPOSE_PROJECT}-backend ps" "Check backend container status"

    echo -e "${GREEN}Backend services (8 containers):${NC}"
    echo "- Brain API (port 8001)"
    echo "- Wagtail CMS (port 8002)"
    echo "- Django CRM (port 8003)"
    echo "- Directory API (port 8004)"
    echo "- CorelDove Backend (port 8005)"
    echo "- AI Agents (port 8010)"
    echo "- Amazon Sourcing (port 8085)"
    echo "- Saleor (port 8000)"

else
    echo -e "${RED}❌ Missing: dokploy-backend-staging.yml${NC}"
fi

echo ""
echo -e "${GREEN}🎯 PHASE 3: FRONTEND APPLICATIONS DEPLOYMENT${NC}"
echo "============================================"

# Check if frontend file exists
if [ -f "dokploy-frontend-staging.yml" ]; then
    echo -e "${GREEN}✅ Found: dokploy-frontend-staging.yml${NC}"

    copy_to_vps "dokploy-frontend-staging.yml" "/opt/staging/frontend/docker-compose.yml" "Copy frontend configuration"

    execute_on_vps "cd /opt/staging/frontend && docker-compose -p ${COMPOSE_PROJECT}-frontend up -d" "Deploy frontend services"

    execute_on_vps "docker-compose -p ${COMPOSE_PROJECT}-frontend ps" "Check frontend container status"

    echo -e "${GREEN}Frontend applications (6 containers):${NC}"
    echo "- Bizoholic Marketing → stg.bizoholic.com"
    echo "- Client Portal → stg.bizoholic.com/login/"
    echo "- CorelDove E-commerce → stg.coreldove.com"
    echo "- Business Directory → stg.bizoholic.com/directory/"
    echo "- ThrillRing Gaming → stg.thrillring.com"
    echo "- Admin Dashboard → stg.bizoholic.com/admin/"

else
    echo -e "${RED}❌ Missing: dokploy-frontend-staging.yml${NC}"
fi

echo ""
echo -e "${GREEN}🎯 DEPLOYMENT VERIFICATION${NC}"
echo "============================="

execute_on_vps "docker ps --filter 'name=bizosaas-staging' --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}'" "List all staging containers"

execute_on_vps "docker network ls | grep staging" "Check staging networks"

echo ""
echo -e "${GREEN}🔍 HEALTH CHECKS${NC}"
echo "================"

# Infrastructure health checks
echo "Infrastructure Health:"
execute_on_vps "curl -f http://localhost:8200/v1/sys/health" "Test Vault health"
execute_on_vps "curl -f http://localhost:8082" "Test Temporal UI"
execute_on_vps "curl -f http://localhost:8009/health" "Test Temporal Integration"

# Backend health checks
echo ""
echo "Backend Health:"
execute_on_vps "curl -f http://localhost:8001/health" "Test Brain API"
execute_on_vps "curl -f http://localhost:8005/health" "Test CorelDove Backend"
execute_on_vps "curl -f http://localhost:8004/health" "Test Directory API"

# Frontend accessibility checks
echo ""
echo "Frontend Accessibility:"
execute_on_vps "curl -I https://stg.bizoholic.com" "Test Bizoholic Marketing"
execute_on_vps "curl -I https://stg.coreldove.com" "Test CorelDove E-commerce"
execute_on_vps "curl -I https://stg.thrillring.com" "Test ThrillRing Gaming"

echo ""
echo -e "${GREEN}🎉 DEPLOYMENT SUMMARY${NC}"
echo "===================="
echo "Total containers to deploy: 20"
echo "- Infrastructure: 6 containers"
echo "- Backend: 8 containers"
echo "- Frontend: 6 containers"
echo ""
echo "Staging domains:"
echo "- stg.bizoholic.com"
echo "- stg.coreldove.com"
echo "- stg.thrillring.com"
echo ""
echo -e "${YELLOW}📋 MANUAL EXECUTION REQUIRED:${NC}"
echo "This script shows the commands that need to be executed."
echo "To actually deploy, you need to:"
echo "1. SSH into the VPS: ssh $VPS_USER@$VPS_IP"
echo "2. Copy the Docker Compose files to the VPS"
echo "3. Execute the docker-compose commands shown above"
echo "4. Configure Traefik routing for the domains"
echo "5. Verify SSL certificate generation"
echo ""

exit 0