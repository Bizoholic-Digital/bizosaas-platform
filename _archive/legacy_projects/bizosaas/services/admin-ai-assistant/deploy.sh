#!/bin/bash

# BizOSaaS Admin AI Assistant Deployment Script
# This script deploys the Admin AI Assistant service with all dependencies

set -e  # Exit on any error

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is available
check_port() {
    local port=$1
    if netstat -tuln | grep -q ":$port "; then
        return 1
    else
        return 0
    fi
}

print_status "🚀 Starting BizOSaaS Admin AI Assistant Deployment"

# Check prerequisites
print_status "Checking prerequisites..."

if ! command_exists docker; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_success "Prerequisites check passed"

# Check if ports are available
print_status "Checking port availability..."

PORTS=(8028 5432 6379)
for port in "${PORTS[@]}"; do
    if ! check_port $port; then
        print_warning "Port $port is already in use. This might cause conflicts."
    fi
done

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating environment file from template..."
    cp .env.example .env
    print_warning "Please edit .env file with your specific configuration before starting the service"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p data/postgres
mkdir -p data/redis

# Set permissions
chmod 755 logs
chmod 755 data/postgres
chmod 755 data/redis

# Build and start services
print_status "Building Docker images..."
docker-compose build --no-cache

print_status "Starting services..."
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."

# Function to wait for service
wait_for_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            print_success "$service_name is ready"
            return 0
        fi
        
        print_status "Waiting for $service_name... (attempt $attempt/$max_attempts)"
        sleep 5
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name failed to start within expected time"
    return 1
}

# Wait for database
print_status "Waiting for PostgreSQL..."
sleep 10

# Wait for Redis
print_status "Waiting for Redis..."
sleep 5

# Wait for Admin AI Assistant
wait_for_service "Admin AI Assistant" "http://localhost:8028/health"

# Show service status
print_status "Checking service status..."
docker-compose ps

# Show logs for the main service
print_status "Showing recent logs..."
docker-compose logs --tail=20 admin-ai-assistant

# Create initial database setup if needed
print_status "Ensuring database is properly initialized..."
docker-compose exec -T postgres psql -U postgres -d bizosaas -c "SELECT 1;" > /dev/null 2>&1

# Test API endpoints
print_status "Testing API endpoints..."

# Test health endpoint
if curl -s -f "http://localhost:8028/health" > /dev/null; then
    print_success "Health endpoint is working"
else
    print_error "Health endpoint is not responding"
fi

# Test dashboard
if curl -s -f "http://localhost:8028/dashboard" > /dev/null; then
    print_success "Dashboard is accessible"
else
    print_error "Dashboard is not accessible"
fi

print_success "🎉 BizOSaaS Admin AI Assistant deployment completed!"

echo ""
echo "🔗 Service URLs:"
echo "   Dashboard: http://localhost:8028/dashboard"
echo "   API Docs:  http://localhost:8028/docs"
echo "   Health:    http://localhost:8028/health"
echo ""

echo "🛠️  Management Commands:"
echo "   View logs:     docker-compose logs -f admin-ai-assistant"
echo "   Stop service:  docker-compose down"
echo "   Restart:       docker-compose restart admin-ai-assistant"
echo "   Update:        docker-compose pull && docker-compose up -d"
echo ""

echo "📊 Database Access:"
echo "   PostgreSQL: localhost:5432 (user: postgres, db: bizosaas)"
echo "   Redis:      localhost:6379"
echo ""

echo "🔒 Security Notes:"
echo "   - Change default passwords in .env file"
echo "   - Update ADMIN_API_KEY in .env file"
echo "   - Configure firewall rules for production deployment"
echo ""

# Check for any warnings or errors in logs
ERRORS=$(docker-compose logs admin-ai-assistant 2>&1 | grep -i error | wc -l)
WARNINGS=$(docker-compose logs admin-ai-assistant 2>&1 | grep -i warning | wc -l)

if [ $ERRORS -gt 0 ]; then
    print_warning "Found $ERRORS error(s) in logs. Check with: docker-compose logs admin-ai-assistant"
fi

if [ $WARNINGS -gt 0 ]; then
    print_warning "Found $WARNINGS warning(s) in logs."
fi

print_status "Deployment script completed successfully!"
print_status "The Admin AI Assistant is now monitoring your BizOSaaS platform!"

exit 0