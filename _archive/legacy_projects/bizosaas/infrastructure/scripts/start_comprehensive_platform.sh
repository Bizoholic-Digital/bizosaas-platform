#!/bin/bash
# BizOSaaS Comprehensive Platform Startup Script
# Starts all services for complete user journey testing

echo "🚀 Starting BizOSaaS Comprehensive Platform - Autonomous AI Agents SaaS"
echo "======================================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check service health
check_service() {
    local url=$1
    local name=$2
    echo -n "Checking $name... "
    if curl -s -f "$url" > /dev/null; then
        echo -e "${GREEN}✅ Running${NC}"
        return 0
    else
        echo -e "${RED}❌ Not responding${NC}"
        return 1
    fi
}

# Function to start service and wait
start_service() {
    local command=$1
    local name=$2
    local port=$3
    local health_endpoint=$4
    
    echo -e "${BLUE}Starting $name...${NC}"
    eval "$command" &
    
    # Wait for service to be ready
    local retries=30
    while [ $retries -gt 0 ]; do
        if check_service "$health_endpoint" "$name"; then
            break
        fi
        sleep 2
        ((retries--))
    done
    
    if [ $retries -eq 0 ]; then
        echo -e "${RED}❌ $name failed to start after 60 seconds${NC}"
    fi
}

echo -e "${YELLOW}📊 Checking existing services...${NC}"

# Check existing services
echo "Infrastructure Services:"
check_service "http://localhost:5432" "PostgreSQL" || echo "  ⚠️  PostgreSQL may need to be started manually"
check_service "http://localhost:6379" "Redis" || echo "  ⚠️  Redis may need to be started manually"
check_service "http://localhost:8200/v1/sys/health" "HashiCorp Vault"

echo -e "\nPlatform Services:"
check_service "http://localhost:8000/health/" "Saleor E-commerce (CoreLDove)"
check_service "http://localhost:8006/admin/" "Wagtail CMS (Bizoholic)"
check_service "http://localhost:8001/health" "AI Agents Service"
check_service "http://localhost:8007/health/" "Django CRM"
check_service "http://localhost:8080/health" "API Gateway"

echo -e "\nFrontend Services:"
check_service "http://localhost:3000" "BizOSaaS Next.js Dashboard"
check_service "http://localhost:3001" "Bizoholic Website"
check_service "http://localhost:3002" "CoreLDove Storefront"

echo -e "\n${YELLOW}🔧 Starting missing services...${NC}"

# Start services in correct order
cd /home/alagiri/projects/bizoholic/bizosaas

# 1. Start AI Agents Service (46+ agents)
if ! check_service "http://localhost:8001/health" "AI Agents Service" > /dev/null 2>&1; then
    echo -e "${BLUE}🤖 Starting AI Agents Service (46+ autonomous agents)...${NC}"
    cd services/ai-agents && python main.py &
    AI_AGENTS_PID=$!
    sleep 10
    cd ../..
fi

# 2. Start Django CRM
if ! check_service "http://localhost:8007/health/" "Django CRM" > /dev/null 2>&1; then
    echo -e "${BLUE}🏢 Starting Django CRM Service...${NC}"
    cd services/django-crm && python manage.py runserver 0.0.0.0:8007 &
    DJANGO_CRM_PID=$!
    sleep 5
    cd ../..
fi

# 3. Start Business Directory
if ! check_service "http://localhost:8003/health" "Business Directory" > /dev/null 2>&1; then
    echo -e "${BLUE}📊 Starting Business Directory Service...${NC}"
    cd services/business-directory && python directory_service.py &
    BUSINESS_DIR_PID=$!
    sleep 5
    cd ../..
fi

# 4. Start API Gateway (FastAPI centralized brain)
if ! check_service "http://localhost:8080/health" "API Gateway" > /dev/null 2>&1; then
    echo -e "${BLUE}🧠 Starting FastAPI API Gateway (Centralized Brain)...${NC}"
    cd services/api-gateway && python main_enhanced.py &
    API_GATEWAY_PID=$!
    sleep 5
    cd ../..
fi

# 5. Start Wagtail CMS for Bizoholic
if ! check_service "http://localhost:8006/admin/" "Wagtail CMS" > /dev/null 2>&1; then
    echo -e "${BLUE}📝 Starting Wagtail CMS (Bizoholic Backend)...${NC}"
    cd services/wagtail-cms && python manage.py runserver 0.0.0.0:8006 &
    WAGTAIL_PID=$!
    sleep 5
    cd ../..
fi

# 6. Start Frontend Services
if ! check_service "http://localhost:3000" "BizOSaaS Dashboard" > /dev/null 2>&1; then
    echo -e "${BLUE}🖥️ Starting BizOSaaS Next.js Dashboard...${NC}"
    cd services/frontend-nextjs && npm run dev &
    NEXTJS_PID=$!
    sleep 10
    cd ../..
fi

# 7. Start CoreLDove Storefront
if ! check_service "http://localhost:3002" "CoreLDove Storefront" > /dev/null 2>&1; then
    echo -e "${BLUE}🛍️ Starting CoreLDove E-commerce Storefront...${NC}"
    cd services/saleor-storefront && npm run dev -- --port 3002 &
    CORELDOVE_PID=$!
    sleep 10
    cd ../..
fi

echo -e "\n${YELLOW}⏳ Waiting for all services to be ready...${NC}"
sleep 15

echo -e "\n${GREEN}🎉 BizOSaaS Platform Status Check${NC}"
echo "=================================="

# Final health check
echo -e "\n${BLUE}🏗️ Infrastructure Services:${NC}"
check_service "http://localhost:5432" "PostgreSQL (Multi-tenant + pgvector)"
check_service "http://localhost:6379" "Redis (Caching + Sessions)"
check_service "http://localhost:8200/v1/sys/health" "HashiCorp Vault (BYOK + Secrets)"

echo -e "\n${BLUE}🧠 Core Platform Services:${NC}"
check_service "http://localhost:8080/health" "FastAPI API Gateway (Centralized Brain)"
check_service "http://localhost:8001/health" "AI Agents Service (46+ Autonomous Agents)"
check_service "http://localhost:8003/health" "Business Directory (Multi-tenant Data)"
check_service "http://localhost:8007/health/" "Django CRM (Client Management)"

echo -e "\n${BLUE}📊 Content & E-commerce Backends:${NC}"
check_service "http://localhost:8006/admin/" "Wagtail CMS (Bizoholic Content)"
check_service "http://localhost:8000/health/" "Saleor E-commerce (CoreLDove Products)"

echo -e "\n${BLUE}🖥️ Frontend Applications:${NC}"
check_service "http://localhost:3000" "BizOSaaS Unified Dashboard"
check_service "http://localhost:3001" "Bizoholic Website (Wagtail-powered)"
check_service "http://localhost:3002" "CoreLDove Storefront (Saleor-powered)"

echo -e "\n${GREEN}🎯 User Journey Testing URLs:${NC}"
echo "==============================="
echo "🏠 BizOSaaS Main Dashboard: http://localhost:3000"
echo "🤖 AI Agents Interface: http://localhost:3000/ai-agents"
echo "📊 Business Analytics: http://localhost:3000/analytics"
echo "🏢 Bizoholic Website: http://localhost:3001"
echo "🛍️ CoreLDove E-commerce: http://localhost:3002"
echo "⚙️ Wagtail Admin: http://localhost:8006/admin/ (admin/admin123)"
echo "🛒 Saleor Admin: http://localhost:8000/dashboard/ (admin@example.com/admin)"
echo "🔐 Vault UI: http://localhost:8200/ui (Token: bizosaas-root-token)"

echo -e "\n${GREEN}🧪 API Testing Endpoints:${NC}"
echo "========================="
echo "🧠 API Gateway: http://localhost:8080/docs"
echo "🤖 AI Agents API: http://localhost:8001/docs"
echo "📊 Business Directory API: http://localhost:8003/docs"
echo "🏢 CRM API: http://localhost:8007/api/docs/"
echo "📝 Wagtail API: http://localhost:8006/api/v2/"
echo "🛍️ Saleor GraphQL: http://localhost:8000/graphql/"

echo -e "\n${YELLOW}📋 Testing Checklist:${NC}"
echo "===================="
echo "✅ 1. Access BizOSaaS Dashboard and verify AI agents are active"
echo "✅ 2. Visit Bizoholic website and check dynamic content from Wagtail"
echo "✅ 3. Browse CoreLDove storefront and verify products from Saleor"
echo "✅ 4. Test Amazon product sourcing workflow through AI agents"
echo "✅ 5. Verify SSO login across all platforms"
echo "✅ 6. Test multi-tenant data isolation"
echo "✅ 7. Validate secure credentials through Vault integration"

echo -e "\n${GREEN}🚀 BizOSaaS Platform is now running!${NC}"
echo -e "${BLUE}Ready for comprehensive user journey testing${NC}"

# Save PIDs for cleanup
echo "AI_AGENTS_PID=$AI_AGENTS_PID" > .platform_pids
echo "DJANGO_CRM_PID=$DJANGO_CRM_PID" >> .platform_pids
echo "BUSINESS_DIR_PID=$BUSINESS_DIR_PID" >> .platform_pids
echo "API_GATEWAY_PID=$API_GATEWAY_PID" >> .platform_pids
echo "WAGTAIL_PID=$WAGTAIL_PID" >> .platform_pids
echo "NEXTJS_PID=$NEXTJS_PID" >> .platform_pids
echo "CORELDOVE_PID=$CORELDOVE_PID" >> .platform_pids