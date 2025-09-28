#!/bin/bash

# BizOSaaS Production Environment Startup Script
# Standardized container naming: bizosaas-[service-name]-main
# Project identifier: bizosaas

set -e

echo "🚀 Starting BizOSaaS Production Environment"
echo "=========================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if container is healthy
check_container_health() {
    local container_name=$1
    local max_attempts=30
    local attempt=1

    print_status "Checking health of $container_name..."
    
    while [ $attempt -le $max_attempts ]; do
        if docker ps --filter "name=$container_name" --filter "health=healthy" --format "{{.Names}}" | grep -q "$container_name"; then
            print_success "$container_name is healthy!"
            return 0
        elif docker ps --filter "name=$container_name" --format "{{.Names}}" | grep -q "$container_name"; then
            echo -n "."
            sleep 2
            ((attempt++))
        else
            print_error "$container_name is not running!"
            return 1
        fi
    done
    
    print_warning "$container_name health check timeout (but container is running)"
    return 0
}

# Function to wait for service to be ready
wait_for_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=1

    print_status "Waiting for $service_name to be ready at $url..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$url" >/dev/null 2>&1; then
            print_success "$service_name is ready!"
            return 0
        else
            echo -n "."
            sleep 2
            ((attempt++))
        fi
    done
    
    print_warning "$service_name readiness check timeout"
    return 1
}

# Clean up old containers with different naming patterns
print_status "Cleaning up old containers..."
docker ps -a --filter "label=bizosaas.service.category" --format "{{.Names}}" | while read container; do
    if [[ ! "$container" =~ bizosaas-.*-main$ ]]; then
        print_status "Removing old container: $container"
        docker rm -f "$container" 2>/dev/null || true
    fi
done

# Remove unused images
print_status "Cleaning up unused images..."
docker image prune -f > /dev/null 2>&1

# Remove old networks
print_status "Cleaning up old networks..."
docker network ls --filter "name=bizosaas" --format "{{.Name}}" | while read network; do
    if [ "$network" != "bizosaas-network" ]; then
        docker network rm "$network" 2>/dev/null || true
    fi
done

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env 2>/dev/null || echo "Warning: No .env.example found"
fi

# Stop any conflicting containers on the same ports
print_status "Stopping conflicting containers..."
conflicting_containers=(
    "shared-postgres" "shared-dragonfly" "shared-vault" "shared-traefik"
    "bizoholic-postgres" "bizoholic-redis" "bizoholic-strapi" "bizoholic-byok-manager"
    "strapi-latest-bizosaas"
)

for container in "${conflicting_containers[@]}"; do
    if docker ps -q -f name="$container" >/dev/null; then
        print_status "Stopping conflicting container: $container"
        docker stop "$container" 2>/dev/null || true
        docker rm "$container" 2>/dev/null || true
    fi
done

# Start the production environment
print_status "Starting BizOSaaS production environment..."
docker-compose -f docker-compose.production.yml up -d --build

# Wait for infrastructure services
print_status "Waiting for infrastructure services..."
check_container_health "bizosaas-postgres-main"
check_container_health "bizosaas-redis-main"

# Wait for core services
print_status "Waiting for core services..."
wait_for_service "AI Agents" "http://localhost:8000/health"
wait_for_service "CRM" "http://localhost:8007/health"
wait_for_service "Vault Service" "http://localhost:8201/health"

# Wait for e-commerce services
print_status "Waiting for e-commerce services..."
wait_for_service "Saleor GraphQL" "http://localhost:8020/graphql/"
wait_for_service "Business Directory" "http://localhost:8003/health"

# Wait for frontend services
print_status "Waiting for frontend services..."
wait_for_service "Website" "http://localhost:3000"
wait_for_service "Client Sites" "http://localhost:3004"
wait_for_service "Wagtail CMS" "http://localhost:8006"

echo ""
echo "🎉 BizOSaaS Production Environment Started Successfully!"
echo "======================================================"
echo ""
echo "📊 Service Status:"
echo "=================="
docker-compose -f docker-compose.production.yml ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "🌐 Access URLs:"
echo "==============="
echo "• Main Website:           http://localhost:3000"
echo "• Multi-tenant Sites:     http://localhost:3004"
echo "• AI Agents API:          http://localhost:8000"
echo "• CRM System:             http://localhost:8007"
echo "• Business Directory:     http://localhost:8003"
echo "• Saleor E-commerce:      http://localhost:8020"
echo "• Wagtail CMS:           http://localhost:8006/admin/"
echo "• Vault Management:      http://localhost:8200"
echo "• Traefik Dashboard:     http://localhost:8080"
echo ""
echo "🔐 Default Credentials:"
echo "======================="
echo "• Database: admin / BizoholicSecure2025"
echo "• Wagtail CMS: admin / BizoholicSecure2025"
echo "• Vault Root Token: myroot"
echo ""
echo "🧪 Health Checks:"
echo "=================="
echo "curl http://localhost:8000/health     # AI Agents"
echo "curl http://localhost:8007/health     # CRM"
echo "curl http://localhost:8003/health     # Directory"
echo "curl http://localhost:8020/graphql/   # Saleor"
echo ""
echo "📝 Management Commands:"
echo "======================="
echo "docker-compose -f docker-compose.production.yml ps     # Check status"
echo "docker-compose -f docker-compose.production.yml logs   # View logs"
echo "docker-compose -f docker-compose.production.yml stop   # Stop all"
echo ""

# Create a status check script
cat > check-bizosaas-status.sh << 'EOF'
#!/bin/bash
echo "🔍 BizOSaaS System Status Check"
echo "==============================="

services=(
    "http://localhost:8000/health:AI Agents"
    "http://localhost:8007/health:CRM System"
    "http://localhost:8003/health:Business Directory"
    "http://localhost:8020/graphql/:Saleor API"
    "http://localhost:3000:Website"
    "http://localhost:3004:Client Sites"
    "http://localhost:8006:Wagtail CMS"
)

for service in "${services[@]}"; do
    url="${service%:*}"
    name="${service#*:}"
    
    if curl -f -s "$url" >/dev/null 2>&1; then
        echo "✅ $name - OK"
    else
        echo "❌ $name - FAILED"
    fi
done

echo ""
echo "📊 Container Status:"
docker ps --filter "label=bizosaas.service.category" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
EOF

chmod +x check-bizosaas-status.sh

print_success "BizOSaaS Production Environment is ready!"
print_status "Use './check-bizosaas-status.sh' to check system health anytime"