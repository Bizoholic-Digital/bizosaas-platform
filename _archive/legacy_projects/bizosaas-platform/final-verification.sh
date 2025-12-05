#!/bin/bash
# Complete 22-service verification script

API_KEY="agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi"
VPS_IP="194.238.16.237"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "BizOSaaS Platform - Complete Verification"
echo "Target: 22 Services (100%)"
echo "=========================================="

total=0
running=0

# Function to check service
check_service() {
    local name=$1
    local port=$2
    local category=$3

    total=$((total + 1))

    if timeout 3 nc -zv $VPS_IP $port 2>&1 | grep -q succeeded; then
        echo -e "${GREEN}✓${NC} $name ($port) - ${category}"
        running=$((running + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $name ($port) - ${category}"
        return 1
    fi
}

echo ""
echo -e "${YELLOW}Infrastructure Services (6 total):${NC}"
check_service "PostgreSQL" 5433 "Database"
check_service "Redis" 6380 "Cache"
check_service "Vault" 8201 "Secrets"
check_service "Temporal Server" 7234 "Workflows"
check_service "Temporal UI" 8083 "Workflows UI"
check_service "Superset" 8088 "Analytics"

echo ""
echo -e "${YELLOW}Backend Services (10 total):${NC}"
check_service "Saleor" 8000 "E-commerce"
check_service "Brain API" 8001 "AI Gateway"
check_service "Wagtail CMS" 8002 "Content"
check_service "Django CRM" 8003 "CRM"
check_service "Business Directory Backend" 8004 "Directory API"
check_service "CorelDove Backend" 8005 "E-commerce Bridge"
check_service "Auth Service" 8006 "Authentication"
check_service "Temporal Integration" 8007 "Workflow Service"
check_service "AI Agents" 8008 "AI Services"
check_service "Amazon Sourcing" 8009 "Product Sourcing"

echo ""
echo -e "${YELLOW}Frontend Services (6 total):${NC}"
check_service "Bizoholic Frontend" 3000 "Marketing Site"
check_service "Client Portal" 3001 "Client Dashboard"
check_service "CorelDove Frontend" 3002 "E-commerce Store"
check_service "Business Directory Frontend" 3003 "Directory UI"
check_service "ThrillRing Gaming" 3005 "Gaming Platform"
check_service "Admin Dashboard" 3009 "Admin Interface"

echo ""
echo "=========================================="
percentage=$((running * 100 / total))
echo -e "Status: ${running}/${total} services running (${percentage}%)"

if [ $running -eq 22 ]; then
    echo -e "${GREEN}✓ ALL SERVICES OPERATIONAL!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Configure staging domains"
    echo "2. Enable SSL certificates"
    echo "3. Test application functionality"
elif [ $running -ge 16 ]; then
    echo -e "${YELLOW}⚠ Deployment in progress - most services running${NC}"
    echo "Wait for remaining services to complete building"
else
    echo -e "${RED}✗ Deployment incomplete${NC}"
    echo "Check Dokploy logs for build errors"
fi
echo "=========================================="
