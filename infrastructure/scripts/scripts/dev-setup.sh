#!/bin/bash
# BizoSaaS Development Environment Setup Script

set -e

echo "🚀 Starting BizoSaaS Development Environment Setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'  
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+ first."
        exit 1
    fi
    
    # Check Python
    if ! command -v python3.11 &> /dev/null; then
        if ! command -v python3 &> /dev/null; then
            print_error "Python 3.11+ is not installed. Please install Python first."
            exit 1
        fi
    fi
    
    # Check K3s (optional)
    if command -v k3s &> /dev/null; then
        print_status "K3s detected - will use existing cluster"
        export USE_K3S=true
    else
        print_warning "K3s not found - will use Docker Compose for local development"
        export USE_K3S=false
    fi
    
    print_status "Prerequisites check passed ✅"
}

# Setup environment variables
setup_environment() {
    print_status "Setting up environment variables..."
    
    if [ ! -f .env ]; then
        cp .env.example .env 2>/dev/null || cat > .env << EOF
# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Database
POSTGRES_HOST=localhost
POSTGRES_USER=admin
POSTGRES_PASSWORD=securepassword
POSTGRES_DB=bizosaas
POSTGRES_PORT=5432

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random-for-development

# AI Services
OPENROUTER_API_KEY=your-openrouter-api-key-here
OPENAI_API_KEY=your-openrouter-api-key-here
OPENAI_BASE_URL=https://openrouter.ai/api/v1

# External APIs (optional)
GOOGLE_ADS_DEVELOPER_TOKEN=
META_ADS_ACCESS_TOKEN=
LINKEDIN_ADS_ACCESS_TOKEN=

# Stripe (optional)
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=

# CORS
CORS_ORIGINS=["http://localhost:3000","http://app.bizosaas.local","http://api.bizosaas.local"]
EOF
        print_warning "Created .env file with default values. Please update API keys!"
    else
        print_status "Using existing .env file"
    fi
}

# Setup local hosts
setup_hosts() {
    print_status "Setting up local host entries..."
    
    # Check if entries already exist
    if grep -q "bizosaas.local" /etc/hosts; then
        print_status "Host entries already exist"
    else
        print_warning "Adding local host entries (requires sudo)..."
        echo "127.0.0.1 bizosaas.local api.bizosaas.local app.bizosaas.local grafana.bizosaas.local traefik.bizosaas.local" | sudo tee -a /etc/hosts
    fi
}

# Install frontend dependencies
setup_frontend() {
    print_status "Setting up frontend dependencies..."
    
    if [ ! -d "frontend/node_modules" ]; then
        cd frontend
        npm install
        cd ..
    else
        print_status "Frontend dependencies already installed"
    fi
}

# Build Docker images
build_images() {
    print_status "Building Docker images..."
    
    # Build identity service
    if [ -d "services/identity-service" ]; then
        print_status "Building Identity & Billing Service..."
        docker build -t bizosaas/identity-service:dev ./services/identity-service
    fi
    
    # Build AI orchestrator
    if [ -d "shared/ai-orchestrator" ]; then
        print_status "Building AI Orchestrator Service..."
        docker build -t bizosaas/ai-orchestrator:dev ./shared/ai-orchestrator
    fi
    
    print_status "Docker images built successfully ✅"
}

# Start services
start_services() {
    print_status "Starting services..."
    
    if [ "$USE_K3S" = "true" ]; then
        print_status "Deploying to K3s cluster..."
        kubectl apply -f infrastructure/k8s/
        
        print_status "Services deployed to K3s ✅"
        print_status "Access URLs:"
        print_status "  - Frontend: http://app.bizosaas.local"
        print_status "  - API: http://api.bizosaas.local"
        print_status "  - AI Service: http://localhost:30082"
    else
        print_status "Starting with Docker Compose..."
        
        # Start core services
        docker-compose up -d --profile local
        
        # Wait for services to be healthy
        print_status "Waiting for services to be ready..."
        sleep 10
        
        # Check service health
        check_service_health
        
        print_status "Services started successfully ✅"
        print_status "Access URLs:"
        print_status "  - Frontend: http://localhost:3000"
        print_status "  - Identity Service: http://localhost:8001"
        print_status "  - AI Orchestrator: http://localhost:8002"
        print_status "  - Traefik Dashboard: http://localhost:8080"
    fi
}

# Check service health
check_service_health() {
    print_status "Checking service health..."
    
    services=(
        "http://localhost:8001/health:Identity Service"
        "http://localhost:8002/health:AI Orchestrator"
    )
    
    for service in "${services[@]}"; do
        url=$(echo $service | cut -d: -f1-3)
        name=$(echo $service | cut -d: -f4-)
        
        if curl -f -s "$url" > /dev/null; then
            print_status "$name is healthy ✅"
        else
            print_warning "$name is not responding ⚠️"
        fi
    done
}

# Start monitoring stack
start_monitoring() {
    if [ "$1" = "--monitoring" ]; then
        print_status "Starting monitoring stack..."
        docker-compose --profile monitoring up -d prometheus grafana
        
        print_status "Monitoring URLs:"
        print_status "  - Prometheus: http://localhost:9090"
        print_status "  - Grafana: http://localhost:3001 (admin/admin123)"
    fi
}

# Main execution
main() {
    echo "🎯 BizoSaaS Development Environment Setup"
    echo "========================================"
    
    check_prerequisites
    setup_environment
    setup_hosts
    setup_frontend
    build_images
    start_services
    start_monitoring $1
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Update .env file with your API keys"
    echo "2. Access the frontend at http://localhost:3000"
    echo "3. Check service health at http://localhost:8001/health"
    echo "4. View API docs at http://localhost:8001/docs"
    echo ""
    echo "🛠️  Development Commands:"
    echo "  npm run dev           # Start frontend in dev mode"
    echo "  docker-compose logs   # View all service logs"
    echo "  docker-compose down   # Stop all services"
    echo ""
    echo "📚 Documentation: http://localhost:3000/docs"
}

# Run main function
main $1