#!/bin/bash

# Fix Authentication Credentials for Authentik and Lago
# Date: 2026-01-25
# Purpose: Reset/Create admin users for both services

set -e

echo "======================================"
echo "Authentication Credentials Fix Script"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Server details
SERVER="root@194.238.16.237"

echo -e "${YELLOW}Step 1: Checking Authentik Status${NC}"
echo "--------------------------------------"

# Check if Authentik container is running
ssh $SERVER "docker ps --filter 'name=authentik-server' --format '{{.Names}}\t{{.Status}}'"

echo ""
echo -e "${YELLOW}Step 2: Resetting Authentik Admin Password${NC}"
echo "--------------------------------------"
echo "Default credentials should be:"
echo "  Username: akadmin"
echo "  Password: Bizoholic2025!Admin"
echo ""

# Check if bootstrap password is set
echo "Checking Authentik environment variables..."
ssh $SERVER "docker exec authentik-server env | grep AUTHENTIK_BOOTSTRAP"

echo ""
echo -e "${YELLOW}Step 3: Creating Authentik Admin User (if needed)${NC}"
echo "--------------------------------------"

# Create admin user using Authentik's management command
ssh $SERVER "docker exec -it authentik-server ak create_admin_group" || true
ssh $SERVER "docker exec -it authentik-server ak bootstrap_tasks" || true

echo ""
echo -e "${YELLOW}Step 4: Checking Lago Status${NC}"
echo "--------------------------------------"

# Check if Lago containers are running
ssh $SERVER "docker ps --filter 'name=lago' --format '{{.Names}}\t{{.Status}}'"

echo ""
echo -e "${YELLOW}Step 5: Creating Lago Admin User${NC}"
echo "--------------------------------------"
echo "Creating admin user with credentials:"
echo "  Email: admin@bizoholic.net"
echo "  Password: Password123!"
echo ""

# Create Lago admin user using Rails console
ssh $SERVER "docker exec lago-api rails runner \"
user = User.find_or_initialize_by(email: 'admin@bizoholic.net')
user.password = 'Password123!'
user.password_confirmation = 'Password123!'
org = Organization.find_or_create_by!(name: 'Bizoholic')
membership = Membership.find_or_create_by!(user: user, organization: org) do |m|
  m.role = :admin
end
user.save!
puts 'Admin user created successfully!'
puts \"Email: #{user.email}\"
puts \"Organization: #{org.name}\"
puts \"Role: #{membership.role}\"
\" 2>&1"

echo ""
echo -e "${GREEN}======================================"
echo "Credentials Summary"
echo "======================================${NC}"
echo ""
echo -e "${GREEN}Authentik SSO:${NC}"
echo "  URL: https://auth-sso.bizoholic.net/if/admin/"
echo "  Username: akadmin"
echo "  Password: Bizoholic2025!Admin"
echo ""
echo -e "${GREEN}Lago Billing:${NC}"
echo "  URL: https://billing.bizoholic.net"
echo "  Email: admin@bizoholic.net"
echo "  Password: Password123!"
echo ""
echo -e "${YELLOW}Note: If Authentik login still doesn't work, you may need to:${NC}"
echo "  1. Check if AUTHENTIK_BOOTSTRAP_PASSWORD is set in docker-compose"
echo "  2. Restart the authentik-server container"
echo "  3. Access the initial setup flow at: https://auth-sso.bizoholic.net/if/flow/initial-setup/"
echo ""
