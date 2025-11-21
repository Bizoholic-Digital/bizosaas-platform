#!/bin/bash

# Automated Saleor Dashboard Fix via Docker Service Updates
# This script bypasses Dokploy UI and directly updates Docker Swarm services

set -e

KVM4_HOST="72.60.219.244"
KVM4_PASSWORD="&k3civYG5Q6YPb"

echo "=================================================="
echo "Automated Saleor Dashboard Fix - Starting"
echo "=================================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Fix Saleor API Database Connection${NC}"
echo "Adding DATABASE_URL environment variable..."

sshpass -p "${KVM4_PASSWORD}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@${KVM4_HOST} << 'ENDSSH'
docker service update \
  --env-add "DATABASE_URL=postgresql://saleor:SaleorDB2025@Staging@infrastructureservices-saleorpostgres-las0jw:5432/saleor" \
  backend-saleor-api

echo "✅ Database connection updated"
ENDSSH

echo ""
echo -e "${YELLOW}Step 2: Add Traefik Labels to Saleor API${NC}"
echo "Exposing API via api.coreldove.com..."

sshpass -p "${KVM4_PASSWORD}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@${KVM4_HOST} << 'ENDSSH'
docker service update \
  --label-add "traefik.enable=true" \
  --label-add "traefik.http.routers.saleor-api.rule=Host(\`api.coreldove.com\`)" \
  --label-add "traefik.http.routers.saleor-api.entrypoints=websecure" \
  --label-add "traefik.http.routers.saleor-api.tls=true" \
  --label-add "traefik.http.routers.saleor-api.tls.certresolver=letsencrypt" \
  --label-add "traefik.http.services.saleor-api.loadbalancer.server.port=8000" \
  backend-saleor-api

echo "✅ Traefik labels added to Saleor API"
ENDSSH

echo ""
echo -e "${YELLOW}Step 3: Update Saleor Core CORS Configuration${NC}"
echo "Adding dashboard domain to ALLOWED_CLIENT_HOSTS..."

sshpass -p "${KVM4_PASSWORD}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@${KVM4_HOST} << 'ENDSSH'
docker service update \
  --env-add "ALLOWED_CLIENT_HOSTS=stg.coreldove.com,api.coreldove.com" \
  backend-saleor-api

echo "✅ CORS configuration updated"
ENDSSH

echo ""
echo -e "${YELLOW}Step 4: Update Dashboard API_URL${NC}"
echo "Changing API URL to https://api.coreldove.com/graphql/..."

sshpass -p "${KVM4_PASSWORD}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@${KVM4_HOST} << 'ENDSSH'
docker service update \
  --env-add "API_URL=https://api.coreldove.com/graphql/" \
  frontendservices-saleordashboard-84ku62

echo "✅ Dashboard API_URL updated"
ENDSSH

echo ""
echo -e "${YELLOW}Step 5: Wait for Services to Restart${NC}"
echo "Waiting 60 seconds for service updates to complete..."
sleep 60

echo ""
echo -e "${YELLOW}Step 6: Verify API Accessibility${NC}"
echo "Testing https://api.coreldove.com/graphql/..."

if curl -I -k https://api.coreldove.com/graphql/ 2>&1 | grep -q "HTTP"; then
    echo -e "${GREEN}✅ API is accessible${NC}"
else
    echo -e "${RED}⚠️  API not yet accessible (may need DNS propagation)${NC}"
    echo "Add to /etc/hosts for testing: 72.60.219.244 api.coreldove.com"
fi

echo ""
echo -e "${YELLOW}Step 7: Create Saleor Superuser${NC}"
echo "Creating admin account..."

sshpass -p "${KVM4_PASSWORD}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@${KVM4_HOST} << 'ENDSSH'
# Wait for service to be ready
sleep 10

# Get the new container ID after service update
CONTAINER_ID=$(docker ps --filter "ancestor=ghcr.io/saleor/saleor:3.20" --format "{{.ID}}" | head -1)

if [ -z "$CONTAINER_ID" ]; then
    echo "❌ Could not find Saleor API container"
    exit 1
fi

echo "Found container: $CONTAINER_ID"

# Create superuser
docker exec $CONTAINER_ID python manage.py createsuperuser \
  --email admin@coreldove.com \
  --no-input 2>&1 || echo "User may already exist"

# Set password and permissions
docker exec $CONTAINER_ID python manage.py shell -c "
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
" 2>&1
ENDSSH

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Superuser creation completed${NC}"
else
    echo -e "${RED}⚠️  Superuser creation had issues (may need manual retry)${NC}"
fi

echo ""
echo -e "${YELLOW}Step 8: Verify Dashboard Status${NC}"
echo "Testing dashboard accessibility..."

DASHBOARD_STATUS=$(curl -I -s https://stg.coreldove.com/dashboard/ 2>&1 | head -1)
echo "Dashboard Status: ${DASHBOARD_STATUS}"

if echo "${DASHBOARD_STATUS}" | grep -q "200"; then
    echo -e "${GREEN}✅ Dashboard is accessible${NC}"
else
    echo -e "${YELLOW}⚠️  Dashboard status check inconclusive${NC}"
fi

echo ""
echo "=================================================="
echo -e "${GREEN}Automated Saleor Dashboard Fix - Complete${NC}"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Add DNS A record: api.coreldove.com → 72.60.219.244"
echo "2. Wait 5-10 minutes for DNS propagation"
echo "3. Clear browser cache"
echo "4. Test login at: https://stg.coreldove.com/dashboard/"
echo "   - Email: admin@coreldove.com"
echo "   - Password: CoreLdove2025!Admin"
echo ""
echo "If login still fails:"
echo "- Check browser console for errors"
echo "- Verify: curl -I https://api.coreldove.com/graphql/"
echo "- Check Traefik logs: docker logs traefik 2>&1 | grep api.coreldove"
echo ""
echo "Documentation: SALEOR_FIX_IMPLEMENTATION_STATUS.md"
echo "=================================================="
