#!/bin/bash

# Plane Local Testing Setup Script
# This script sets up Plane for local development and testing

set -e

echo "🚀 Setting up Plane for local testing..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo -e "${BLUE}Step 1: Checking prerequisites...${NC}"

if ! docker ps | grep -q "bizosaas-postgres-staging"; then
    echo -e "${RED}Error: PostgreSQL container 'bizosaas-postgres-staging' is not running${NC}"
    echo "Please start it first with: docker start bizosaas-postgres-staging"
    exit 1
fi

if ! docker ps | grep -q "bizosaas-redis-staging"; then
    echo -e "${RED}Error: Redis container 'bizosaas-redis-staging' is not running${NC}"
    echo "Please start it first with: docker start bizosaas-redis-staging"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites met${NC}"

# Step 2: Create Plane database
echo -e "${BLUE}Step 2: Creating Plane database...${NC}"

docker exec bizosaas-postgres-staging psql -U admin -d bizosaas_staging -c "CREATE DATABASE plane_db;" 2>/dev/null || {
    echo -e "${GREEN}✓ Database already exists${NC}"
}

# Step 3: Start Plane containers
echo -e "${BLUE}Step 3: Starting Plane containers...${NC}"

docker-compose -f docker-compose.plane-local.yml up -d

echo "Waiting for Plane API to be ready..."
sleep 10

# Step 4: Run database migrations
echo -e "${BLUE}Step 4: Running database migrations...${NC}"

docker exec plane-api-local python manage.py migrate

echo -e "${GREEN}✓ Migrations complete${NC}"

# Step 5: Create superuser (interactive)
echo -e "${BLUE}Step 5: Creating admin user...${NC}"
echo "Please enter admin credentials:"

docker exec -it plane-api-local python manage.py createsuperuser

# Step 6: Display access information
echo -e "${GREEN}"
echo "========================================="
echo "✓ Plane setup complete!"
echo "========================================="
echo -e "${NC}"
echo "Access Plane:"
echo "  Web UI: http://localhost:3002"
echo "  API:    http://localhost:8090"
echo ""
echo "Next steps:"
echo "1. Login to http://localhost:3002 with your admin credentials"
echo "2. Create a workspace"
echo "3. Go to Settings → API Tokens"
echo "4. Generate a new API token"
echo "5. Use the token to connect via brain-gateway:"
echo "   - API URL: http://localhost:8090"
echo "   - API Key: <your-generated-token>"
echo ""
echo "To stop Plane:"
echo "  docker-compose -f docker-compose.plane-local.yml down"
echo ""
echo "To view logs:"
echo "  docker-compose -f docker-compose.plane-local.yml logs -f"
