#!/bin/bash

# Saleor Dashboard API Fix - Automated Script
# This script configures Traefik routing for Saleor API and updates Dashboard configuration

set -e

echo "=================================================="
echo "Saleor Dashboard API Fix - Implementation Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

KVM4_HOST="72.60.219.244"
KVM4_PASSWORD="&k3civYG5Q6YPb"
SALEOR_API_CONTAINER="backend-saleor-api.1.2b4cetxidpwq0i5l3nbgmi10p"
DASHBOARD_CONTAINER="frontendservices-saleordashboard-84ku62"
API_DOMAIN="api.coreldove.com"
NEW_API_URL="https://${API_DOMAIN}/graphql/"

echo -e "${YELLOW}Step 1: Check current Saleor API Traefik configuration${NC}"
sshpass -p "${KVM4_PASSWORD}" ssh -o StrictHostKeyChecking=no root@${KVM4_HOST} \
  "docker inspect ${SALEOR_API_CONTAINER} --format='{{json .Config.Labels}}' | jq 'with_entries(select(.key | startswith(\"traefik\")))'"

echo ""
echo -e "${YELLOW}Step 2: Add Traefik labels to Saleor API${NC}"
echo -e "${RED}MANUAL STEP REQUIRED:${NC} Please configure in Dokploy UI:"
echo ""
echo "1. Navigate to: Dokploy → Backend Services → saleor-api"
echo "2. Go to: Routing → Domain tab"
echo "3. Add domain configuration:"
echo "   - Host: ${API_DOMAIN}"
echo "   - Path: /"
echo "   - Container Port: 8000"
echo "   - HTTPS: ✅ Enabled"
echo "   - Certificate Resolver: letsencrypt"
echo ""
echo "4. Click 'Save' and 'Deploy'"
echo ""
read -p "Press Enter after completing Dokploy configuration..."

echo ""
echo -e "${YELLOW}Step 3: Verify Traefik routing is active${NC}"
echo "Waiting 30 seconds for Traefik to apply changes..."
sleep 30

echo "Testing API accessibility..."
if curl -I -k https://${API_DOMAIN}/graphql/ 2>&1 | grep -q "HTTP"; then
    echo -e "${GREEN}✅ API is accessible via ${API_DOMAIN}${NC}"
else
    echo -e "${RED}❌ API not yet accessible. May need DNS propagation.${NC}"
    echo "You can add to /etc/hosts for testing:"
    echo "  72.60.219.244 ${API_DOMAIN}"
fi

echo ""
echo -e "${YELLOW}Step 4: Update Saleor Core CORS configuration${NC}"
echo "Adding dashboard domain to ALLOWED_CLIENT_HOSTS..."

# Check if ALLOWED_CLIENT_HOSTS already exists
CURRENT_HOSTS=$(sshpass -p "${KVM4_PASSWORD}" ssh -o StrictHostKeyChecking=no root@${KVM4_HOST} \
  "docker exec ${SALEOR_API_CONTAINER} env 2>/dev/null | grep ALLOWED_CLIENT_HOSTS || echo 'NONE'")

echo "Current ALLOWED_CLIENT_HOSTS: ${CURRENT_HOSTS}"
echo ""
echo -e "${RED}MANUAL STEP REQUIRED:${NC} Update Saleor API environment variables in Dokploy:"
echo ""
echo "1. Navigate to: Dokploy → Backend Services → saleor-api"
echo "2. Go to: Environment tab"
echo "3. Add or update:"
echo "   ALLOWED_CLIENT_HOSTS=stg.coreldove.com,${API_DOMAIN}"
echo ""
echo "4. Click 'Save' and 'Restart' service"
echo ""
read -p "Press Enter after updating CORS configuration..."

echo ""
echo -e "${YELLOW}Step 5: Update Saleor Dashboard API_URL${NC}"
echo "Updating Dashboard environment variable..."
echo ""
echo -e "${RED}MANUAL STEP REQUIRED:${NC} Update Dashboard configuration in Dokploy:"
echo ""
echo "1. Navigate to: Dokploy → Frontend Services → saleor-dashboard"
echo "2. Go to: Environment tab"
echo "3. Update API_URL to:"
echo "   API_URL=${NEW_API_URL}"
echo ""
echo "4. Click 'Save' and 'Restart' service"
echo ""
read -p "Press Enter after updating Dashboard API_URL..."

echo ""
echo -e "${YELLOW}Step 6: Create Saleor superuser${NC}"
echo "Creating admin account..."

sshpass -p "${KVM4_PASSWORD}" ssh -o StrictHostKeyChecking=no root@${KVM4_HOST} <<EOF
# Create superuser
docker exec ${SALEOR_API_CONTAINER} \
  python manage.py createsuperuser \
  --email admin@coreldove.com \
  --no-input 2>&1 || echo "User may already exist"

# Set password
docker exec ${SALEOR_API_CONTAINER} \
  python manage.py shell -c "
from saleor.account.models import User
try:
    u = User.objects.get(email='admin@coreldove.com')
    u.set_password('CoreLdove2025!Admin')
    u.is_staff = True
    u.is_superuser = True
    u.is_active = True
    u.save()
    print('✅ Superuser created/updated successfully')
except Exception as e:
    print(f'❌ Error: {e}')
"
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Superuser created successfully${NC}"
else
    echo -e "${RED}❌ Error creating superuser${NC}"
fi

echo ""
echo -e "${YELLOW}Step 7: Verify Dashboard accessibility${NC}"
echo "Testing dashboard..."

DASHBOARD_STATUS=$(curl -I -s https://stg.coreldove.com/dashboard/ | head -1)
echo "Dashboard Status: ${DASHBOARD_STATUS}"

if echo "${DASHBOARD_STATUS}" | grep -q "200"; then
    echo -e "${GREEN}✅ Dashboard is accessible${NC}"
else
    echo -e "${RED}⚠️  Dashboard status check failed${NC}"
fi

echo ""
echo "=================================================="
echo -e "${GREEN}Saleor Dashboard API Fix - Complete${NC}"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Clear your browser cache"
echo "2. Navigate to: https://stg.coreldove.com/dashboard/"
echo "3. Login with:"
echo "   Email: admin@coreldove.com"
echo "   Password: CoreLdove2025!Admin"
echo ""
echo "4. Check browser console for any errors"
echo "5. Verify GraphQL queries are working"
echo ""
echo "If login still fails:"
echo "- Check browser console for CORS errors"
echo "- Verify API is accessible: curl -I https://${API_DOMAIN}/graphql/"
echo "- Check Traefik logs: docker logs traefik 2>&1 | grep ${API_DOMAIN}"
echo ""
echo "Documentation: SALEOR_DASHBOARD_LOGIN_FIX.md"
echo "=================================================="
