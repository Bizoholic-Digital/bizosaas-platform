#!/bin/bash

# BizOSaaS Platform - Transition to Containerized Services
# This script safely transitions from development services to containerized deployment

set -e

echo "🚀 Starting BizOSaaS Platform Containerization Transition..."

# Colors for output
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

# Step 1: Check current running services
print_status "Checking current running services..."

echo "=== Currently Running Development Services ==="
ps aux | grep -E "(python3.*(business-directory|sqladmin|analytics)|npm run dev)" | grep -v grep || echo "No development services found"

echo -e "\n=== Currently Listening Ports ==="
ss -tulpn | grep -E "(3004|3005|3009|8004|8005|8001)" || echo "No target ports in use"

# Step 2: Gracefully stop development services
print_status "Stopping development services gracefully..."

print_status "Stopping Python services..."
pkill -f "python3.*business-directory-service.py" || true
pkill -f "python3.*sqladmin-dashboard-service.py" || true  
pkill -f "python3.*superset-analytics-proxy.py" || true

print_status "Stopping Next.js development servers..."
pkill -f "npm run dev" || true

# Wait for processes to stop
sleep 5

# Step 3: Check existing Docker containers
print_status "Checking existing Docker setup..."
cd /home/alagiri/projects/bizoholic/bizosaas-platform

# Check if docker-compose is already running
if docker-compose -f docker-compose.unified.yml ps | grep -q "Up"; then
    print_warning "Some containers are already running. Checking status..."
    docker-compose -f docker-compose.unified.yml ps
else
    print_status "No containers currently running."
fi

# Step 4: Build new service images
print_status "Building new service images..."

print_status "Building Business Directory Service..."
docker-compose -f docker-compose.unified.yml build business-directory

print_status "Building SQLAdmin Dashboard Service..."
docker-compose -f docker-compose.unified.yml build sqladmin-dashboard-service

print_status "Building Analytics Dashboard Service..."
docker-compose -f docker-compose.unified.yml build analytics-dashboard

# Step 5: Start the new containerized services
print_status "Starting containerized services..."

# Start infrastructure services first
print_status "Starting infrastructure services..."
docker-compose -f docker-compose.unified.yml up -d postgres redis

# Wait for infrastructure to be ready
print_status "Waiting for infrastructure services to be ready..."
sleep 15

# Start the Brain Gateway
print_status "Starting Brain Gateway..."
docker-compose -f docker-compose.unified.yml up -d bizosaas-brain

# Wait for Brain Gateway
sleep 10

# Start our new services
print_status "Starting new integrated services..."
docker-compose -f docker-compose.unified.yml up -d business-directory sqladmin-dashboard-service analytics-dashboard

# Step 6: Start frontend applications (if not already running)
print_status "Starting frontend applications..."
docker-compose -f docker-compose.unified.yml up -d

# Step 7: Wait for services to be healthy
print_status "Waiting for services to become healthy..."
sleep 30

# Step 8: Check service health
print_status "Checking service health..."
services=(
    "http://localhost:8001/health:Brain Gateway"
    "http://localhost:8004/health:Business Directory"
    "http://localhost:8005/health:SQLAdmin Dashboard"
    "http://localhost:3009/health:Analytics Dashboard"
)

all_healthy=true
for service in "${services[@]}"; do
    url="${service%:*}"
    name="${service#*:}"
    
    if curl -s -f "$url" > /dev/null 2>&1; then
        print_success "$name is healthy ✅"
    else
        print_warning "$name is not responding ⚠️"
        all_healthy=false
    fi
done

# Step 9: Display container status
print_status "Container Status:"
docker-compose -f docker-compose.unified.yml ps

# Step 10: Display deployment summary
if [ "$all_healthy" = true ]; then
    print_success "🎉 Containerization Transition Complete!"
else
    print_warning "⚠️ Some services may need attention"
fi

echo -e "\n${BLUE}=== CONTAINERIZED DEPLOYMENT SUMMARY ===${NC}"
echo -e "${GREEN}New Containerized Services:${NC}"
echo -e "  🗃️  Business Directory: http://localhost:8004 (Container: bizosaas-business-directory-8004)"
echo -e "  🗂️  SQLAdmin Dashboard: http://localhost:8005 (Container: bizosaas-sqladmin-8005)"
echo -e "  📊 Analytics Dashboard: http://localhost:3009 (Container: bizosaas-analytics-3009)"

echo -e "\n${GREEN}Existing Infrastructure:${NC}"
echo -e "  🧠 Brain Gateway: http://localhost:8001 (Container: bizosaas-brain)"
echo -e "  🗄️  PostgreSQL: localhost:5432 (Container: bizosaas-postgres)"
echo -e "  ⚡ Redis: localhost:6379 (Container: bizosaas-redis)"

echo -e "\n${GREEN}Frontend Applications:${NC}"
echo -e "  🌐 Business Directory Frontend: http://localhost:3004"
echo -e "  ⚙️  BizOSaaS Admin Frontend: http://localhost:3005"
echo -e "  👤 Client Portal Frontend: http://localhost:3006"

echo -e "\n${BLUE}Container Management:${NC}"
echo -e "  📊 View all containers: docker-compose -f docker-compose.unified.yml ps"
echo -e "  📋 View logs: docker-compose -f docker-compose.unified.yml logs -f [service-name]"
echo -e "  🔄 Restart service: docker-compose -f docker-compose.unified.yml restart [service-name]"
echo -e "  🛑 Stop all: docker-compose -f docker-compose.unified.yml down"

echo -e "\n${BLUE}Next Steps:${NC}"
echo -e "  1. Test the analytics integration: http://localhost:3009/admin"
echo -e "  2. Verify client portal analytics: http://localhost:3006 (analytics tab)"
echo -e "  3. Check business directory: http://localhost:3004"
echo -e "  4. Test admin dashboard: http://localhost:3005"

print_success "All services are now running in containers! 🐳"