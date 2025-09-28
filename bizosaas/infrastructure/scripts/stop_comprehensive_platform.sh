#!/bin/bash
# BizOSaaS Comprehensive Platform Stop Script

echo "🛑 Stopping BizOSaaS Comprehensive Platform"
echo "==========================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load saved PIDs
if [ -f .platform_pids ]; then
    source .platform_pids
    echo -e "${YELLOW}Stopping platform services...${NC}"
    
    # Stop services
    [ ! -z "$AI_AGENTS_PID" ] && kill $AI_AGENTS_PID 2>/dev/null && echo -e "${GREEN}Stopped AI Agents Service${NC}"
    [ ! -z "$DJANGO_CRM_PID" ] && kill $DJANGO_CRM_PID 2>/dev/null && echo -e "${GREEN}Stopped Django CRM${NC}"
    [ ! -z "$BUSINESS_DIR_PID" ] && kill $BUSINESS_DIR_PID 2>/dev/null && echo -e "${GREEN}Stopped Business Directory${NC}"
    [ ! -z "$API_GATEWAY_PID" ] && kill $API_GATEWAY_PID 2>/dev/null && echo -e "${GREEN}Stopped API Gateway${NC}"
    [ ! -z "$WAGTAIL_PID" ] && kill $WAGTAIL_PID 2>/dev/null && echo -e "${GREEN}Stopped Wagtail CMS${NC}"
    [ ! -z "$NEXTJS_PID" ] && kill $NEXTJS_PID 2>/dev/null && echo -e "${GREEN}Stopped Next.js Dashboard${NC}"
    [ ! -z "$CORELDOVE_PID" ] && kill $CORELDOVE_PID 2>/dev/null && echo -e "${GREEN}Stopped CoreLDove Storefront${NC}"
    
    rm .platform_pids
else
    echo -e "${YELLOW}No PID file found, attempting to find and kill processes...${NC}"
    
    # Kill by process name
    pkill -f "main.py" 2>/dev/null && echo -e "${GREEN}Stopped AI Agents${NC}"
    pkill -f "manage.py runserver.*8007" 2>/dev/null && echo -e "${GREEN}Stopped Django CRM${NC}"
    pkill -f "directory_service.py" 2>/dev/null && echo -e "${GREEN}Stopped Business Directory${NC}"
    pkill -f "main_enhanced.py" 2>/dev/null && echo -e "${GREEN}Stopped API Gateway${NC}"
    pkill -f "manage.py runserver.*8006" 2>/dev/null && echo -e "${GREEN}Stopped Wagtail CMS${NC}"
    pkill -f "npm run dev" 2>/dev/null && echo -e "${GREEN}Stopped Frontend Services${NC}"
fi

echo -e "\n${GREEN}✅ BizOSaaS Platform services stopped${NC}"
echo -e "${YELLOW}Note: Infrastructure services (PostgreSQL, Redis, Vault, Saleor) left running${NC}"