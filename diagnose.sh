#!/bin/bash
# Quick Diagnostic Script for BizOSaaS Platform Issues

echo "==================================="
echo "BizOSaaS Platform Diagnostics"
echo "==================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker containers
echo "1. Checking Docker Containers..."
echo "-----------------------------------"
ssh root@72.60.98.213 "docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E 'brain|admin|authentik|client-portal'" || echo -e "${RED}✗ Failed to connect to server${NC}"
echo ""

# Check brain-gateway health
echo "2. Checking Brain Gateway Health..."
echo "-----------------------------------"
if curl -s -f https://api.bizoholic.net/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Brain Gateway is healthy${NC}"
else
    echo -e "${RED}✗ Brain Gateway is not responding${NC}"
fi
echo ""

# Check brain-gateway logs for errors
echo "3. Checking Brain Gateway Logs..."
echo "-----------------------------------"
ssh root@72.60.98.213 "docker logs brain-gateway 2>&1 | tail -20" || echo -e "${RED}✗ Failed to fetch logs${NC}"
echo ""

# Check if seeding completed
echo "4. Checking Connector Seeding..."
echo "-----------------------------------"
ssh root@72.60.98.213 "docker logs brain-gateway 2>&1 | grep -E 'Seeding|Brain'" || echo -e "${YELLOW}⚠ No seeding logs found${NC}"
echo ""

# Check Authentik
echo "5. Checking Authentik..."
echo "-----------------------------------"
if curl -s -f https://sso.bizoholic.net/.well-known/openid-configuration > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Authentik is accessible${NC}"
else
    echo -e "${RED}✗ Authentik is not responding${NC}"
fi
echo ""

# Check Admin Dashboard
echo "6. Checking Admin Dashboard..."
echo "-----------------------------------"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://admin.bizoholic.net)
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "307" ] || [ "$HTTP_CODE" = "302" ]; then
    echo -e "${GREEN}✓ Admin Dashboard is accessible (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${RED}✗ Admin Dashboard returned HTTP $HTTP_CODE${NC}"
fi
echo ""

# Check Client Portal
echo "7. Checking Client Portal..."
echo "-----------------------------------"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://app.bizoholic.net)
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "307" ] || [ "$HTTP_CODE" = "302" ]; then
    echo -e "${GREEN}✓ Client Portal is accessible (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${RED}✗ Client Portal returned HTTP $HTTP_CODE${NC}"
fi
echo ""

# Check connectors API
echo "8. Checking Connectors API..."
echo "-----------------------------------"
if curl -s -f https://api.bizoholic.net/api/connectors/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Connectors API is responding${NC}"
    echo "Connector count:"
    curl -s https://api.bizoholic.net/api/connectors/ | jq '. | length' 2>/dev/null || echo "  (jq not installed, cannot parse)"
else
    echo -e "${RED}✗ Connectors API returned error${NC}"
fi
echo ""

echo "==================================="
echo "Diagnostics Complete"
echo "==================================="
echo ""
echo "Next Steps:"
echo "1. Review the troubleshooting guide: critical_issues_troubleshooting.md"
echo "2. Check specific service logs for detailed errors"
echo "3. Verify environment variables in Dokploy"
