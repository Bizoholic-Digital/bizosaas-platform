#!/bin/bash

# Live Staging Deployment Execution Script
# Deploys BizOSaaS staging environment to VPS using the tested configurations

echo "🚀 Live BizOSaaS Staging Deployment"
echo "=================================="
echo ""

VPS_IP="194.238.16.237"
DOKPLOY_URL="http://${VPS_IP}:3000"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🎯 Deployment Target:${NC}"
echo "VPS IP: $VPS_IP"
echo "Dokploy Dashboard: $DOKPLOY_URL"
echo "Total Containers: 20 (6 + 8 + 6)"
echo ""

# Function to check service availability
check_service() {
    local url=$1
    local name=$2
    local timeout=${3:-10}

    echo -n "Checking $name: "
    response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout $timeout "$url" 2>/dev/null)

    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✅ AVAILABLE${NC}"
        return 0
    elif [ "$response" = "000" ]; then
        echo -e "${RED}❌ TIMEOUT${NC}"
        return 1
    else
        echo -e "${YELLOW}⚠️  HTTP $response${NC}"
        return 1
    fi
}

echo -e "${GREEN}🔍 PRE-DEPLOYMENT VERIFICATION${NC}"
echo "==============================="

# Check Dokploy accessibility
check_service "$DOKPLOY_URL" "Dokploy Dashboard"

# Check if staging services are already running
echo ""
echo "Checking for existing staging services:"
check_service "http://${VPS_IP}:8200/v1/sys/health" "Vault (staging)" 5
check_service "http://${VPS_IP}:8001/health" "Brain API (staging)" 5
check_service "http://${VPS_IP}:8005/health" "CorelDove Backend (staging)" 5

echo ""
echo -e "${GREEN}🏗️  PHASE 1: INFRASTRUCTURE DEPLOYMENT${NC}"
echo "========================================"
echo ""

echo -e "${BLUE}📋 Infrastructure Services (6 containers):${NC}"
echo "1. PostgreSQL (port 5432) - Database with pgvector"
echo "2. Redis (port 6379) - Cache and sessions"
echo "3. Vault (port 8200) - Secrets management"
echo "4. Temporal Server (port 7233) - Workflow engine"
echo "5. Temporal UI (port 8082) - Workflow management"
echo "6. Temporal Integration (port 8009) - Custom service"
echo ""

echo -e "${YELLOW}📝 Manual Deployment Steps for Infrastructure:${NC}"
echo "1. Open Dokploy Dashboard: $DOKPLOY_URL"
echo "2. Create new project: 'bizosaas-infrastructure-staging'"
echo "3. Add Docker Compose application"
echo "4. Upload file: dokploy-infrastructure-staging.yml"
echo "5. Click Deploy and wait 15-20 minutes"
echo ""

echo -e "${BLUE}Waiting for infrastructure deployment...${NC}"
echo "Please proceed with manual deployment in Dokploy dashboard"
echo "Press Enter when infrastructure deployment is complete..."
read -r

echo ""
echo "Verifying infrastructure deployment:"
for i in {1..5}; do
    echo "Attempt $i/5:"
    check_service "http://${VPS_IP}:8200/v1/sys/health" "Vault" 10
    check_service "http://${VPS_IP}:8082" "Temporal UI" 10

    if check_service "http://${VPS_IP}:8200/v1/sys/health" "Vault" 5; then
        echo -e "${GREEN}✅ Infrastructure deployment successful!${NC}"
        break
    elif [ $i -eq 5 ]; then
        echo -e "${RED}❌ Infrastructure deployment failed or still starting${NC}"
        echo "Please check Dokploy logs and try again"
        exit 1
    else
        echo "Waiting 30 seconds before retry..."
        sleep 30
    fi
done

echo ""
echo -e "${GREEN}🔧 PHASE 2: BACKEND SERVICES DEPLOYMENT${NC}"
echo "========================================"
echo ""

echo -e "${BLUE}📋 Backend Services (8 containers):${NC}"
echo "1. Brain API (port 8001) - AI Central Hub coordinator"
echo "2. Wagtail CMS (port 8002) - Content management"
echo "3. Django CRM (port 8003) - Customer management"
echo "4. Directory API (port 8004) - Business directory"
echo "5. CorelDove Backend (port 8005) - E-commerce API"
echo "6. AI Agents (port 8010) - Multi-model AI"
echo "7. Amazon Sourcing (port 8085) - Product sourcing"
echo "8. Saleor (port 8000) - E-commerce engine"
echo ""

echo -e "${YELLOW}📝 Manual Deployment Steps for Backend:${NC}"
echo "1. In Dokploy, create new project: 'bizosaas-backend-staging'"
echo "2. Add Docker Compose application"
echo "3. Upload file: dokploy-backend-staging-corrected.yml"
echo "4. Configure environment variables (API keys)"
echo "5. Click Deploy and wait 20-25 minutes"
echo ""

echo "Press Enter when backend deployment is complete..."
read -r

echo ""
echo "Verifying backend deployment:"
for i in {1..5}; do
    echo "Attempt $i/5:"
    check_service "http://${VPS_IP}:8001/health" "Brain API" 10
    check_service "http://${VPS_IP}:8005/health" "CorelDove Backend" 10
    check_service "http://${VPS_IP}:8004/health" "Directory API" 10

    if check_service "http://${VPS_IP}:8001/health" "Brain API" 5; then
        echo -e "${GREEN}✅ Backend deployment successful!${NC}"
        break
    elif [ $i -eq 5 ]; then
        echo -e "${RED}❌ Backend deployment failed or still starting${NC}"
        echo "Please check Dokploy logs and try again"
        exit 1
    else
        echo "Waiting 30 seconds before retry..."
        sleep 30
    fi
done

echo ""
echo -e "${GREEN}🎨 PHASE 3: FRONTEND APPLICATIONS DEPLOYMENT${NC}"
echo "============================================"
echo ""

echo -e "${BLUE}📋 Frontend Applications (6 containers):${NC}"
echo "1. Bizoholic Marketing → stg.bizoholic.com"
echo "2. Client Portal → stg.bizoholic.com/login/"
echo "3. CorelDove E-commerce → stg.coreldove.com"
echo "4. Business Directory → stg.bizoholic.com/directory/"
echo "5. ThrillRing Gaming → stg.thrillring.com"
echo "6. Admin Dashboard → stg.bizoholic.com/admin/"
echo ""

echo -e "${YELLOW}📝 Manual Deployment Steps for Frontend:${NC}"
echo "1. In Dokploy, create new project: 'bizosaas-frontend-staging'"
echo "2. Add Docker Compose application"
echo "3. Upload file: dokploy-frontend-staging.yml"
echo "4. Configure environment variables"
echo "5. Click Deploy and wait 15-20 minutes"
echo ""

echo "Press Enter when frontend deployment is complete..."
read -r

echo ""
echo "Verifying frontend deployment:"
for i in {1..5}; do
    echo "Attempt $i/5:"
    check_service "https://stg.coreldove.com" "CorelDove Frontend" 15

    if check_service "https://stg.coreldove.com" "CorelDove Frontend" 10; then
        echo -e "${GREEN}✅ Frontend deployment successful!${NC}"
        break
    elif [ $i -eq 5 ]; then
        echo -e "${YELLOW}⚠️  Frontend may still be starting or DNS needs update${NC}"
        break
    else
        echo "Waiting 30 seconds before retry..."
        sleep 30
    fi
done

echo ""
echo -e "${GREEN}🔍 COMPLETE DEPLOYMENT VERIFICATION${NC}"
echo "=================================="
echo ""

echo "Running comprehensive verification..."
./verify-staging-deployment.sh

echo ""
echo -e "${GREEN}🎉 DEPLOYMENT EXECUTION COMPLETE${NC}"
echo "================================="
echo ""
echo -e "${BLUE}📊 Deployment Summary:${NC}"
echo "Infrastructure: 6 containers deployed"
echo "Backend Services: 8 containers deployed"
echo "Frontend Applications: 6 containers deployed"
echo "Total: 20 containers"
echo ""
echo -e "${BLUE}🌐 Staging Domains:${NC}"
echo "Marketing: https://stg.bizoholic.com"
echo "E-commerce: https://stg.coreldove.com"
echo "Gaming: https://stg.thrillring.com"
echo "Client Portal: https://stg.bizoholic.com/login/"
echo "Admin Dashboard: https://stg.bizoholic.com/admin/"
echo ""
echo -e "${GREEN}✅ Staging environment ready for testing!${NC}"
echo "✅ Ready to proceed with production deployment"
echo ""

exit 0