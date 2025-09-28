#!/bin/bash

# Complete Saleor Infrastructure Startup Script
# Starts all Saleor services and ensures proper initialization

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIZOSAAS_DIR="$(dirname "$SCRIPT_DIR")"
COMPOSE_FILE="$BIZOSAAS_DIR/docker-compose.saleor-complete.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🚀 $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${NC}"
}

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Cleanup function
cleanup() {
    if [ $? -ne 0 ]; then
        print_error "Script failed. Check the logs above for details."
        print_info "To stop services: docker-compose -f $COMPOSE_FILE down"
    fi
}

trap cleanup EXIT

print_header "SALEOR COMPLETE INFRASTRUCTURE STARTUP"

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Docker
if ! command -v docker >/dev/null 2>&1; then
    print_error "Docker is not installed or not in PATH"
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    print_error "Docker daemon is not running"
    exit 1
fi

print_status "Docker is available and running"

# Check Docker Compose
if ! docker compose version >/dev/null 2>&1; then
    print_error "Docker Compose is not available"
    exit 1
fi

print_status "Docker Compose is available"

# Check PostgreSQL connectivity
echo "🗄️  Checking PostgreSQL connectivity..."
if timeout 10 bash -c "</dev/tcp/localhost/5432"; then
    print_status "PostgreSQL is accessible on localhost:5432"
else
    print_error "PostgreSQL is not accessible on localhost:5432"
    print_info "Please ensure PostgreSQL is running before starting Saleor"
    exit 1
fi

# Navigate to project directory
cd "$BIZOSAAS_DIR"

# Stop any existing Saleor containers
echo "🛑 Stopping any existing Saleor containers..."
docker-compose -f "$COMPOSE_FILE" down --remove-orphans 2>/dev/null || true
print_status "Existing containers stopped"

# Pull latest images
echo "📥 Pulling latest Saleor images..."
docker-compose -f "$COMPOSE_FILE" pull
print_status "Images updated"

# Start the infrastructure
echo "🚀 Starting Saleor infrastructure..."
docker-compose -f "$COMPOSE_FILE" up -d

# Wait for Redis to be ready
echo "⏳ Waiting for Redis to be ready..."
timeout=60
elapsed=0
while [ $elapsed -lt $timeout ]; do
    if docker exec saleor-redis redis-cli ping >/dev/null 2>&1; then
        print_status "Redis is ready"
        break
    fi
    sleep 2
    elapsed=$((elapsed + 2))
done

if [ $elapsed -ge $timeout ]; then
    print_error "Redis failed to start within $timeout seconds"
    exit 1
fi

# Setup database
echo "🗄️  Setting up Saleor database..."
"$SCRIPT_DIR/setup-saleor-database.sh"

# Wait for Saleor API to be healthy
echo "⏳ Waiting for Saleor API to be healthy..."
timeout=180
elapsed=0
while [ $elapsed -lt $timeout ]; do
    if curl -f http://localhost:8024/health/ >/dev/null 2>&1; then
        print_status "Saleor API is healthy"
        break
    fi
    
    # Check container logs if it's not responding
    if [ $((elapsed % 30)) -eq 0 ] && [ $elapsed -gt 0 ]; then
        print_info "Still waiting... checking container status:"
        docker-compose -f "$COMPOSE_FILE" ps saleor-api
    fi
    
    sleep 5
    elapsed=$((elapsed + 5))
done

if [ $elapsed -ge $timeout ]; then
    print_error "Saleor API failed to become healthy within $timeout seconds"
    print_info "Container logs:"
    docker-compose -f "$COMPOSE_FILE" logs --tail=20 saleor-api
    exit 1
fi

# Initialize database with sample data if needed
echo "📊 Initializing Saleor with sample data..."
docker exec saleor-api python manage.py migrate 2>/dev/null || true
docker exec saleor-api python manage.py populatedb --createsuperuser 2>/dev/null || print_warning "Sample data may already exist"
docker exec saleor-api python manage.py collectstatic --noinput 2>/dev/null || true

# Test GraphQL endpoint
echo "🧪 Testing GraphQL endpoint..."
if curl -f -X POST http://localhost:8024/graphql/ \
    -H "Content-Type: application/json" \
    -d '{"query":"{ shop { name } }"}' >/dev/null 2>&1; then
    print_status "GraphQL endpoint is responding"
else
    print_warning "GraphQL endpoint test failed, but service might still be starting"
fi

# Display service status
echo ""
print_header "SALEOR INFRASTRUCTURE STATUS"

docker-compose -f "$COMPOSE_FILE" ps

echo ""
print_header "SERVICE ACCESS INFORMATION"

echo "🌐 Saleor GraphQL API:"
echo "   URL: http://localhost:8024/graphql/"
echo "   Health: http://localhost:8024/health/"
echo "   Playground: http://localhost:8024/graphql/"
echo ""
echo "🎨 Saleor Dashboard:"
echo "   URL: http://localhost:9001/"
echo ""
echo "👤 Default Admin Credentials:"
echo "   Email: admin@example.com"
echo "   Password: admin"
echo ""
echo "💾 Redis Dashboard:"
echo "   Available on: localhost:6379"
echo ""

print_header "TESTING COMMANDS"

echo "🧪 Test GraphQL endpoint:"
echo "   curl -X POST http://localhost:8024/graphql/ \\"
echo "        -H 'Content-Type: application/json' \\"
echo "        -d '{\"query\":\"{ shop { name description } }\"}'"
echo ""
echo "🔍 Check service logs:"
echo "   docker-compose -f $COMPOSE_FILE logs -f saleor-api"
echo "   docker-compose -f $COMPOSE_FILE logs -f saleor-worker"
echo ""
echo "🛑 Stop all services:"
echo "   docker-compose -f $COMPOSE_FILE down"
echo ""

# Test storefront connection
print_header "STOREFRONT INTEGRATION TEST"

echo "🔗 Testing storefront connectivity from Saleor directory..."
STOREFRONT_DIR="$BIZOSAAS_DIR/services/saleor-storefront"

if [ -d "$STOREFRONT_DIR" ]; then
    print_status "Storefront directory found: $STOREFRONT_DIR"
    
    # Check if the storefront has the correct API URL configured
    if [ -f "$STOREFRONT_DIR/.env.local" ]; then
        if grep -q "NEXT_PUBLIC_SALEOR_API_URL=http://localhost:8024/graphql/" "$STOREFRONT_DIR/.env.local"; then
            print_status "Storefront is configured to connect to localhost:8024"
        else
            print_warning "Storefront may not be configured for localhost:8024"
            print_info "Update .env.local in storefront with: NEXT_PUBLIC_SALEOR_API_URL=http://localhost:8024/graphql/"
        fi
    fi
    
    print_info "To test storefront GraphQL codegen:"
    echo "   cd $STOREFRONT_DIR"
    echo "   pnpm run generate"
else
    print_warning "Storefront directory not found at $STOREFRONT_DIR"
fi

print_status "Saleor infrastructure startup completed successfully!"
print_info "All services are running and ready for development."

# Success exit
trap - EXIT