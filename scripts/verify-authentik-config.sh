#!/bin/bash
# Authentik Configuration Verification Script
# This script helps verify your Authentik configuration

set -e

echo "========================================="
echo "Authentik Configuration Verification"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Check Authentik is running
echo -e "${BLUE}[1/6] Checking Authentik Status...${NC}"
if curl -s -o /dev/null -w "%{http_code}" http://localhost:9000 | grep -q "302\|200"; then
    echo -e "${GREEN}✓ Authentik is running at http://localhost:9000${NC}"
else
    echo -e "${RED}✗ Authentik is not accessible${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}[2/6] Checking Admin Dashboard Status...${NC}"
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3004 | grep -q "302\|200\|307"; then
    echo -e "${GREEN}✓ Admin Dashboard is running at http://localhost:3004${NC}"
else
    echo -e "${YELLOW}⚠ Admin Dashboard may not be running${NC}"
    echo "Start it with: cd portals/admin-dashboard && npm run dev"
fi

echo ""
echo -e "${BLUE}[3/6] Checking .env.local file...${NC}"
if [ -f "portals/admin-dashboard/.env.local" ]; then
    echo -e "${GREEN}✓ .env.local exists${NC}"
    
    # Check required variables
    if grep -q "AUTHENTIK_CLIENT_SECRET=" portals/admin-dashboard/.env.local; then
        if grep -q "AUTHENTIK_CLIENT_SECRET=your-client-secret-here\|AUTHENTIK_CLIENT_SECRET=$" portals/admin-dashboard/.env.local; then
            echo -e "${YELLOW}⚠ AUTHENTIK_CLIENT_SECRET not set (still has placeholder)${NC}"
        else
            echo -e "${GREEN}✓ AUTHENTIK_CLIENT_SECRET is set${NC}"
        fi
    else
        echo -e "${RED}✗ AUTHENTIK_CLIENT_SECRET not found${NC}"
    fi
    
    if grep -q "AUTH_SECRET=" portals/admin-dashboard/.env.local; then
        if grep -q "AUTH_SECRET=your-auth-secret\|AUTH_SECRET=$" portals/admin-dashboard/.env.local; then
            echo -e "${YELLOW}⚠ AUTH_SECRET not set (still has placeholder)${NC}"
        else
            echo -e "${GREEN}✓ AUTH_SECRET is set${NC}"
        fi
    else
        echo -e "${RED}✗ AUTH_SECRET not found${NC}"
    fi
else
    echo -e "${RED}✗ .env.local does not exist${NC}"
    echo "Create it with: cd portals/admin-dashboard && cp .env.example .env.local"
fi

echo ""
echo -e "${BLUE}[4/6] Configuration Checklist${NC}"
echo "Please verify you have completed these steps in Authentik UI:"
echo ""
echo "□ Created OAuth Provider:"
echo "  - Name: BizOSaaS Admin Dashboard Provider"
echo "  - Client ID: bizosaas-admin-dashboard"
echo "  - Redirect URI: http://localhost:3004/api/auth/callback/authentik"
echo ""
echo "□ Created Application:"
echo "  - Name: BizOSaaS Admin Dashboard"
echo "  - Slug: bizosaas-admin"
echo ""
echo "□ Created Groups:"
echo "  - super_admin (is_superuser: checked)"
echo "  - platform_admin (is_superuser: unchecked)"
echo ""
echo "□ Created Test User:"
echo "  - Username: superadmin"
echo "  - Added to super_admin group"
echo ""

echo -e "${BLUE}[5/6] Next Steps${NC}"
echo ""
echo "If you haven't configured Authentik yet:"
echo "  1. Open: http://localhost:9000"
echo "  2. Follow: QUICK_START_NOW.md"
echo ""
echo "If Authentik is configured:"
echo "  1. Update .env.local with Client Secret"
echo "  2. Generate AUTH_SECRET: openssl rand -base64 32"
echo "  3. Restart admin dashboard: cd portals/admin-dashboard && npm run dev"
echo "  4. Test login: http://localhost:3004"
echo ""

echo -e "${BLUE}[6/6] Test Authentication${NC}"
echo ""
echo "To test the authentication flow:"
echo "  1. Open: http://localhost:3004"
echo "  2. Click: 'Sign in with SSO'"
echo "  3. Login with: superadmin / <your-password>"
echo "  4. Should redirect back to dashboard"
echo ""

echo "========================================="
echo -e "${GREEN}Verification Complete!${NC}"
echo "========================================="
echo ""
echo "Open Authentik UI: http://localhost:9000"
echo "Open Admin Dashboard: http://localhost:3004"
echo ""
