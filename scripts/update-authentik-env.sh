#!/bin/bash
# Script to add Authentik environment variables to .env files

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Authentik Environment Variable Setup${NC}"
echo ""

# Prompt for Client ID
read -p "Enter AUTHENTIK_CLIENT_ID (from Authentik Provider): " CLIENT_ID
read -p "Enter AUTHENTIK_CLIENT_SECRET (from Authentik Provider): " CLIENT_SECRET

# Default values
ISSUER="http://localhost:9000/application/o/bizosaas-brain/"
URL="http://localhost:9000"

echo ""
echo -e "${YELLOW}Adding variables to .env files...${NC}"

# Add to root .env
ENV_FILE="/home/alagiri/projects/bizosaas-platform/.env"
if [ -f "$ENV_FILE" ]; then
    echo "" >> "$ENV_FILE"
    echo "# Authentik Configuration" >> "$ENV_FILE"
    echo "AUTHENTIK_CLIENT_ID=$CLIENT_ID" >> "$ENV_FILE"
    echo "AUTHENTIK_CLIENT_SECRET=$CLIENT_SECRET" >> "$ENV_FILE"
    echo "AUTHENTIK_ISSUER=$ISSUER" >> "$ENV_FILE"
    echo "AUTHENTIK_URL=$URL" >> "$ENV_FILE"
    echo -e "${GREEN}✓ Updated $ENV_FILE${NC}"
else
    echo -e "${YELLOW}! $ENV_FILE not found, creating...${NC}"
    echo "# Authentik Configuration" > "$ENV_FILE"
    echo "AUTHENTIK_CLIENT_ID=$CLIENT_ID" >> "$ENV_FILE"
    echo "AUTHENTIK_CLIENT_SECRET=$CLIENT_SECRET" >> "$ENV_FILE"
    echo "AUTHENTIK_ISSUER=$ISSUER" >> "$ENV_FILE"
    echo "AUTHENTIK_URL=$URL" >> "$ENV_FILE"
    echo -e "${GREEN}✓ Created $ENV_FILE${NC}"
fi

# Add to client-portal .env.local
PORTAL_ENV="/home/alagiri/projects/bizosaas-platform/portals/client-portal/.env.local"
if [ -f "$PORTAL_ENV" ]; then
    echo "" >> "$PORTAL_ENV"
    echo "# Authentik Configuration" >> "$PORTAL_ENV"
    echo "AUTHENTIK_CLIENT_ID=$CLIENT_ID" >> "$PORTAL_ENV"
    echo "AUTHENTIK_CLIENT_SECRET=$CLIENT_SECRET" >> "$PORTAL_ENV"
    echo "AUTHENTIK_ISSUER=$ISSUER" >> "$PORTAL_ENV"
    echo -e "${GREEN}✓ Updated $PORTAL_ENV${NC}"
fi

echo ""
echo -e "${GREEN}✅ Environment variables added!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Restart services: docker restart client-portal brain-gateway"
echo "2. Test login at: http://localhost:3003/login"
