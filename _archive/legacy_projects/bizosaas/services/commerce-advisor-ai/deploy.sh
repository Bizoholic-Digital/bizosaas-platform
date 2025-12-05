#!/bin/bash

# BizOSaaS Commerce Advisor AI [P11] Deployment Script
# Comprehensive AI-powered e-commerce intelligence and growth optimization service

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Service configuration
SERVICE_NAME="commerce-advisor-ai"
SERVICE_PORT="8030"
DOCKER_IMAGE="bizosaas/commerce-advisor-ai"
CONTAINER_NAME="bizosaas-commerce-advisor-ai"

echo -e "${BLUE}🚀 Deploying BizOSaaS Commerce Advisor AI [P11]${NC}"
echo -e "${BLUE}================================================${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_status "Docker is running"

# Create network if it doesn't exist
if ! docker network ls | grep -q "bizosaas-network"; then
    print_status "Creating BizOSaaS network..."
    docker network create bizosaas-network
else
    print_status "BizOSaaS network already exists"
fi

# Stop and remove existing container
if docker ps -a | grep -q "$CONTAINER_NAME"; then
    print_status "Stopping existing container..."
    docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true
fi

# Remove existing image
if docker images | grep -q "$DOCKER_IMAGE"; then
    print_status "Removing existing image..."
    docker rmi "$DOCKER_IMAGE" >/dev/null 2>&1 || true
fi

# Build the Docker image
print_status "Building Commerce Advisor AI Docker image..."
docker build -t "$DOCKER_IMAGE" .

# Check if environment file exists
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        print_warning "No .env file found. Copying from .env.example..."
        cp .env.example .env
        print_warning "Please edit .env file with your actual configuration values"
    else
        print_error "No .env or .env.example file found"
        exit 1
    fi
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

# Start the service
print_status "Starting Commerce Advisor AI service..."

docker run -d \
    --name "$CONTAINER_NAME" \
    --network bizosaas-network \
    -p "$SERVICE_PORT:$SERVICE_PORT" \
    -e DATABASE_URL="${DATABASE_URL:-postgresql://postgres:postgres@postgres:5432/bizosaas}" \
    -e REDIS_URL="${REDIS_URL:-redis://redis:6379}" \
    -e BRAIN_API_URL="${BRAIN_API_URL:-http://brain-api:8001}" \
    -e CORELDOVE_API_URL="${CORELDOVE_API_URL:-http://coreldove-frontend:3012}" \
    -e SALEOR_API_URL="${SALEOR_API_URL:-http://saleor-api:8000/graphql/}" \
    -e JWT_SECRET="${JWT_SECRET:-your-secret-key}" \
    -e GOOGLE_ANALYTICS_KEY="${GOOGLE_ANALYTICS_KEY:-}" \
    -e FACEBOOK_PIXEL_KEY="${FACEBOOK_PIXEL_KEY:-}" \
    -e RAZORPAY_KEY="${RAZORPAY_KEY:-}" \
    -e PAYU_KEY="${PAYU_KEY:-}" \
    -v "$(pwd)/templates:/app/templates" \
    -v "$(pwd)/static:/app/static" \
    -v "$(pwd)/models:/app/models" \
    --restart unless-stopped \
    "$DOCKER_IMAGE"

# Wait for service to be ready
print_status "Waiting for service to be ready..."
sleep 10

# Health check
for i in {1..30}; do
    if curl -s -f "http://localhost:$SERVICE_PORT/health" >/dev/null 2>&1; then
        print_status "Commerce Advisor AI service is healthy!"
        break
    fi
    
    if [ $i -eq 30 ]; then
        print_error "Service failed to start properly"
        docker logs "$CONTAINER_NAME" --tail 50
        exit 1
    fi
    
    echo -n "."
    sleep 2
done

# Display service information
echo ""
echo -e "${GREEN}🎉 Commerce Advisor AI [P11] deployed successfully!${NC}"
echo -e "${BLUE}================================================${NC}"
echo -e "${YELLOW}Service Details:${NC}"
echo -e "  📊 Dashboard: ${GREEN}http://localhost:$SERVICE_PORT${NC}"
echo -e "  📚 API Docs: ${GREEN}http://localhost:$SERVICE_PORT/docs${NC}"
echo -e "  🔍 Health Check: ${GREEN}http://localhost:$SERVICE_PORT/health${NC}"
echo -e "  🐳 Container: ${GREEN}$CONTAINER_NAME${NC}"
echo -e "  🔌 Port: ${GREEN}$SERVICE_PORT${NC}"
echo ""
echo -e "${YELLOW}Key Features:${NC}"
echo -e "  🛍️  Product Optimization Engine"
echo -e "  📈 Inventory Intelligence & Demand Forecasting"
echo -e "  💰 Dynamic Pricing AI & Market Analysis"
echo -e "  📊 Sales Performance Analytics"
echo -e "  👥 Customer Analytics & Behavioral Insights"
echo -e "  🌍 Market Intelligence & Competitive Analysis"
echo -e "  🎯 CoreLDove E-commerce Integration"
echo -e "  🚀 Growth Strategy Development"
echo ""
echo -e "${YELLOW}API Endpoints:${NC}"
echo -e "  POST /api/v1/products/optimize - Product catalog optimization"
echo -e "  POST /api/v1/inventory/forecast - Inventory demand forecasting"
echo -e "  POST /api/v1/pricing/optimize - Dynamic pricing optimization"
echo -e "  POST /api/v1/customers/analyze - Customer behavior analysis"
echo -e "  POST /api/v1/sales/analytics - Sales performance analytics"
echo -e "  POST /api/v1/market/intelligence - Market intelligence analysis"
echo -e "  POST /api/v1/growth/strategy - AI-powered growth strategy"
echo -e "  GET  /api/v1/dashboard/commerce - Commerce dashboard data"
echo ""
echo -e "${YELLOW}Integration Points:${NC}"
echo -e "  🧠 Brain API (Port 8001): Central intelligence routing"
echo -e "  🛒 CoreLDove Frontend (Port 3012): E-commerce platform integration"
echo -e "  🛍️  Saleor Backend: E-commerce engine integration"
echo -e "  📊 Product Sourcing [P8]: Product discovery integration"
echo -e "  ✅ Supplier Validation [P9]: Supplier quality integration"
echo -e "  📢 Marketing Strategist [P10]: Campaign coordination"
echo ""

# Show logs
echo -e "${YELLOW}Recent logs:${NC}"
docker logs "$CONTAINER_NAME" --tail 20

echo ""
echo -e "${GREEN}✅ Commerce Advisor AI is ready for e-commerce intelligence!${NC}"

# Check integration with other services
echo ""
echo -e "${BLUE}🔗 Checking integration with other services...${NC}"

# Check Brain API
if curl -s -f "http://localhost:8001/health" >/dev/null 2>&1; then
    print_status "Brain API (8001) - Connected"
else
    print_warning "Brain API (8001) - Not available"
fi

# Check Marketing Strategist AI
if curl -s -f "http://localhost:8029/health" >/dev/null 2>&1; then
    print_status "Marketing Strategist AI (8029) - Connected"
else
    print_warning "Marketing Strategist AI (8029) - Not available"
fi

# Check Product Sourcing
if curl -s -f "http://localhost:8026/health" >/dev/null 2>&1; then
    print_status "Product Sourcing (8026) - Connected"
else
    print_warning "Product Sourcing (8026) - Not available"
fi

# Check Supplier Validation
if curl -s -f "http://localhost:8027/health" >/dev/null 2>&1; then
    print_status "Supplier Validation (8027) - Connected"
else
    print_warning "Supplier Validation (8027) - Not available"
fi

echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo -e "1. Configure API keys in .env file for external integrations"
echo -e "2. Set up CoreLDove frontend integration"
echo -e "3. Configure Saleor backend connection"
echo -e "4. Import product catalog for analysis"
echo -e "5. Set up customer data synchronization"
echo -e "6. Configure market intelligence data sources"
echo -e "7. Test AI recommendations and optimization features"
echo ""
echo -e "${GREEN}🎯 Commerce Advisor AI [P11] is ready to optimize your e-commerce operations!${NC}"