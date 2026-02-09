#!/bin/bash

# CoreLDove Saleor E-commerce Platform Startup Script
# Integrates official Saleor Docker images with BizOSaaS ecosystem

set -e

echo "🚀 Starting CoreLDove E-commerce Platform with Saleor..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if required environment file exists
if [ ! -f ".env.coreldove-saleor" ]; then
    echo -e "${YELLOW}Warning: .env.coreldove-saleor not found. Creating from template...${NC}"
    cp .env.coreldove-saleor .env.local
    echo -e "${RED}Please update .env.local with your actual API keys and credentials${NC}"
    echo -e "${YELLOW}Required configurations:${NC}"
    echo "- SALEOR_API_TOKEN (generate from Saleor admin)"
    echo "- AMAZON_API_KEY and AMAZON_SECRET_KEY (for product sourcing)"
    echo "- STRIPE keys (for payments)"
    echo "- VAULT_TOKEN (for secure credential storage)"
    exit 1
fi

# Load environment variables
set -a
source .env.coreldove-saleor
set +a

# Function to check if service is running
check_service() {
    local service_name=$1
    local url=$2
    local max_attempts=${3:-30}
    local attempt=0

    echo -e "${BLUE}Checking $service_name...${NC}"
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $service_name is ready${NC}"
            return 0
        fi
        
        echo -e "${YELLOW}⏳ Waiting for $service_name... (attempt $((attempt + 1))/$max_attempts)${NC}"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo -e "${RED}✗ $service_name failed to start within expected time${NC}"
    return 1
}

# Function to setup Saleor database
setup_saleor_database() {
    echo -e "${BLUE}Setting up Saleor database...${NC}"
    
    # Check if PostgreSQL is available
    if ! docker exec bizoholic-postgres pg_isready -U admin > /dev/null 2>&1; then
        echo -e "${RED}PostgreSQL is not available. Please start PostgreSQL container first.${NC}"
        exit 1
    fi
    
    # Create Saleor database if it doesn't exist (already exists based on our check earlier)
    docker exec bizoholic-postgres psql -U admin -d postgres -c "SELECT 1 FROM pg_database WHERE datname='coreldove_saleor';" | grep -q 1 || \
    docker exec bizoholic-postgres psql -U admin -d postgres -c "CREATE DATABASE coreldove_saleor OWNER admin;" 2>/dev/null || true
    
    echo -e "${GREEN}✓ Saleor database setup complete${NC}"
}

# Check shared infrastructure
echo -e "${BLUE}Checking shared infrastructure...${NC}"

# Check PostgreSQL (we use existing bizoholic-postgres container)
if ! docker ps | grep -q "bizoholic-postgres"; then
    echo -e "${RED}PostgreSQL container is not running. Please start the PostgreSQL container first.${NC}"
    exit 1
fi

# Check Redis
if ! docker ps | grep -q "shared-redis-dev"; then
    echo -e "${RED}Shared Redis is not running. Please check shared infrastructure.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Shared infrastructure is ready${NC}"

# Setup database
setup_saleor_database

# Stop any existing CoreLDove containers
echo -e "${BLUE}Stopping existing CoreLDove containers...${NC}"
docker compose -f docker-compose.coreldove-saleor.yml down > /dev/null 2>&1 || true

# Build and start CoreLDove services
echo -e "${BLUE}Building and starting CoreLDove services...${NC}"
docker compose -f docker-compose.coreldove-saleor.yml up -d --build

# Wait for services to be ready
echo -e "${BLUE}Waiting for services to be ready...${NC}"

# Check Saleor API
check_service "Saleor API" "http://localhost:8020/health/" 60

# Check Saleor Dashboard
check_service "Saleor Dashboard" "http://localhost:9020/" 30

# Check CoreLDove Bridge Service
check_service "CoreLDove Bridge" "http://localhost:8021/health" 30

# Check CoreLDove Sourcing Service
check_service "CoreLDove Sourcing" "http://localhost:8010/health" 30

# Check CoreLDove Storefront
check_service "CoreLDove Storefront" "http://localhost:3001/api/health" 45

# Run Saleor migrations and setup
echo -e "${BLUE}Running Saleor migrations and initial setup...${NC}"
docker compose -f docker-compose.coreldove-saleor.yml exec -T saleor-api python manage.py migrate
docker compose -f docker-compose.coreldove-saleor.yml exec -T saleor-api python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo -e "${BLUE}Setting up Saleor admin user...${NC}"
docker compose -f docker-compose.coreldove-saleor.yml exec -T saleor-api python manage.py createsuperuser \
    --email admin@coreldove.local \
    --no-input 2>/dev/null || echo "Admin user already exists"

# Populate sample data (optional)
echo -e "${YELLOW}Do you want to populate sample product data? (y/N)${NC}"
read -r populate_data
if [[ $populate_data =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Populating sample data...${NC}"
    docker compose -f docker-compose.coreldove-saleor.yml exec -T saleor-api python manage.py populatedb --createsuperuser
fi

echo
echo -e "${GREEN}🎉 CoreLDove E-commerce Platform is ready!${NC}"
echo
echo -e "${BLUE}Access URLs:${NC}"
echo -e "📱 Storefront (Customer):     ${GREEN}http://localhost:3001${NC}"
echo -e "⚙️  Admin Dashboard:          ${GREEN}http://localhost:9020${NC}"
echo -e "🔌 GraphQL API:               ${GREEN}http://localhost:8020/graphql/${NC}"
echo -e "🤖 Bridge Service:            ${GREEN}http://localhost:8021/docs${NC}"
echo -e "📦 Sourcing Service:          ${GREEN}http://localhost:8010/docs${NC}"
echo
echo -e "${BLUE}Admin Credentials:${NC}"
echo -e "Email: ${YELLOW}admin@coreldove.local${NC}"
echo -e "Password: ${YELLOW}admin${NC}"
echo
echo -e "${BLUE}Integration Status:${NC}"
echo -e "✓ Saleor GraphQL API (official)"
echo -e "✓ BizOSaaS Frontend Integration" 
echo -e "✓ AI-Powered Product Sourcing"
echo -e "✓ Marketing Automation Bridge"
echo -e "✓ Multi-tenant Architecture"
echo
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "1. Configure your API keys in .env.coreldove-saleor"
echo -e "2. Set up payment methods in Saleor dashboard"
echo -e "3. Configure product categories and types"
echo -e "4. Test the AI sourcing workflow"
echo -e "5. Connect marketing automation"
echo
echo -e "${GREEN}Happy selling! 🛒${NC}"