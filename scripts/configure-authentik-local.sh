#!/bin/bash
# Authentik Local Configuration Script
# This script helps configure Authentik for BizOSaaS Admin Dashboard

set -e

echo "========================================="
echo "Authentik Configuration for Admin Dashboard"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
AUTHENTIK_URL="http://localhost:9000"
CLIENT_ID="bizosaas-admin-dashboard"
REDIRECT_URI="http://localhost:3004/api/auth/callback/authentik"

echo -e "${BLUE}Step 1: Checking Authentik Status${NC}"
if curl -s -o /dev/null -w "%{http_code}" "$AUTHENTIK_URL" | grep -q "302\|200"; then
    echo -e "${GREEN}✓ Authentik is running at $AUTHENTIK_URL${NC}"
else
    echo -e "${YELLOW}⚠ Authentik may not be running. Starting...${NC}"
    cd "$(dirname "$0")/../bizosaas-brain-core"
    docker compose -f docker-compose.authentik.yml up -d
    echo "Waiting for Authentik to start..."
    sleep 10
fi

echo ""
echo -e "${BLUE}Step 2: Manual Configuration Required${NC}"
echo "Please open your browser and navigate to: $AUTHENTIK_URL"
echo ""
echo "Follow these steps:"
echo ""
echo "=== CREATE OAUTH PROVIDER ==="
echo "1. Navigate to: Applications → Providers → Create"
echo "2. Select: OAuth2/OpenID Provider"
echo "3. Fill in:"
echo "   - Name: BizOSaaS Admin Dashboard Provider"
echo "   - Authorization flow: default-provider-authorization-implicit-consent"
echo "   - Client type: Confidential"
echo "   - Client ID: $CLIENT_ID"
echo "   - Client Secret: <click Generate>"
echo "   - Redirect URIs: $REDIRECT_URI"
echo "   - Scopes: openid, profile, email, groups"
echo "4. Click: Create"
echo "5. SAVE THE CLIENT SECRET!"
echo ""

echo "=== CREATE APPLICATION ==="
echo "1. Navigate to: Applications → Applications → Create"
echo "2. Fill in:"
echo "   - Name: BizOSaaS Admin Dashboard"
echo "   - Slug: bizosaas-admin"
echo "   - Provider: BizOSaaS Admin Dashboard Provider"
echo "   - Launch URL: http://localhost:3004"
echo "3. Click: Create"
echo ""

echo "=== CREATE GROUPS ==="
echo "1. Navigate to: Directory → Groups → Create"
echo "2. Create 'super_admin' group:"
echo "   - Name: super_admin"
echo "   - Is superuser: ✓"
echo "   - Attributes: {\"permissions\": [\"*\"], \"access_level\": \"platform\"}"
echo "3. Create 'platform_admin' group:"
echo "   - Name: platform_admin"
echo "   - Is superuser: ✗"
echo "   - Attributes: {\"permissions\": [\"tenants:*\"], \"access_level\": \"platform\"}"
echo ""

echo "=== CREATE TEST USER ==="
echo "1. Navigate to: Directory → Users → Create"
echo "2. Fill in:"
echo "   - Username: superadmin"
echo "   - Email: superadmin@bizosaas.local"
echo "   - Name: Super Administrator"
echo "3. Set password"
echo "4. Add to group: super_admin"
echo "5. Click: Create"
echo ""

echo -e "${YELLOW}After completing the above steps, press Enter to continue...${NC}"
read -r

echo ""
echo -e "${BLUE}Step 3: Updating Admin Dashboard Environment${NC}"

# Generate AUTH_SECRET
AUTH_SECRET=$(openssl rand -base64 32)

echo "Please enter the Client Secret from Authentik:"
read -r CLIENT_SECRET

# Create .env.local
ENV_FILE="../portals/admin-dashboard/.env.local"
cat > "$ENV_FILE" << EOF
# Authentik SSO Configuration (Local Development)
AUTHENTIK_URL=http://localhost:9000
NEXT_PUBLIC_SSO_URL=http://localhost:9000
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=$CLIENT_ID
AUTHENTIK_CLIENT_SECRET=$CLIENT_SECRET
AUTH_SECRET=$AUTH_SECRET

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000

# Temporal UI
NEXT_PUBLIC_TEMPORAL_UI_URL=http://localhost:8233

# Vault UI  
NEXT_PUBLIC_VAULT_UI_URL=http://localhost:8200

# Environment
NODE_ENV=development

# Port
PORT=3004

# NextAuth URL
NEXTAUTH_URL=http://localhost:3004
NEXTAUTH_URL_INTERNAL=http://localhost:3004
EOF

echo -e "${GREEN}✓ Created $ENV_FILE${NC}"
echo ""

echo -e "${BLUE}Step 4: Configuration Summary${NC}"
echo "Client ID: $CLIENT_ID"
echo "Client Secret: $CLIENT_SECRET"
echo "AUTH_SECRET: $AUTH_SECRET"
echo "Redirect URI: $REDIRECT_URI"
echo ""

echo -e "${GREEN}Configuration complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Restart admin dashboard: cd portals/admin-dashboard && npm run dev"
echo "2. Navigate to: http://localhost:3004"
echo "3. Test SSO login"
echo ""
