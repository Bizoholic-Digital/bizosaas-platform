#!/bin/bash
# Product Sourcing Workflow [P8] - Deployment Script
# BizOSaaS Platform - CoreLDove Integration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVICE_NAME="Product Sourcing Workflow [P8]"
SERVICE_PORT=8026
DOCKER_IMAGE="bizosaas/product-sourcing"
DOCKER_TAG="latest"

echo -e "${BLUE}🚀 Deploying ${SERVICE_NAME}${NC}"
echo "=================================================="

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}📋 Checking Prerequisites${NC}"
echo "================================"

# Check Docker
if command_exists docker; then
    print_status "Docker is installed"
    docker --version
else
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if command_exists docker-compose; then
    print_status "Docker Compose is installed"
    docker-compose --version
else
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check Python
if command_exists python3; then
    print_status "Python 3 is installed"
    python3 --version
else
    print_error "Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

echo ""

# Environment setup
echo -e "${BLUE}⚙️  Setting up Environment${NC}"
echo "================================="

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_warning "Created .env file from .env.example"
        print_warning "Please edit .env file with your API keys and configuration"
        echo ""
        echo "Required environment variables:"
        echo "  - AMAZON_ACCESS_KEY"
        echo "  - AMAZON_SECRET_KEY"
        echo "  - OPENAI_API_KEY"
        echo "  - GOOGLE_API_KEY"
        echo ""
        read -p "Press Enter after updating .env file to continue..."
    else
        print_error ".env.example file not found. Please create environment configuration."
        exit 1
    fi
else
    print_status "Environment file (.env) already exists"
fi

# Check if required environment variables are set
if ! grep -q "AMAZON_ACCESS_KEY=.*[^=]" .env || ! grep -q "OPENAI_API_KEY=.*[^=]" .env; then
    print_warning "Some required API keys may not be configured in .env file"
    print_warning "The service will start but some features may not work without proper API keys"
fi

echo ""

# Build and deployment options
echo -e "${BLUE}🔧 Deployment Options${NC}"
echo "========================="
echo "1. Development deployment (with hot reload)"
echo "2. Production deployment (optimized)"
echo "3. Local testing deployment"
echo "4. Docker only (no external dependencies)"
echo ""
read -p "Select deployment type (1-4): " deploy_type

case $deploy_type in
    1)
        DEPLOYMENT_TYPE="development"
        COMPOSE_FILE="docker-compose.yml"
        ;;
    2)
        DEPLOYMENT_TYPE="production"
        COMPOSE_FILE="docker-compose.prod.yml"
        ;;
    3)
        DEPLOYMENT_TYPE="testing"
        COMPOSE_FILE="docker-compose.test.yml"
        ;;
    4)
        DEPLOYMENT_TYPE="docker-only"
        COMPOSE_FILE="docker-compose.minimal.yml"
        ;;
    *)
        DEPLOYMENT_TYPE="development"
        COMPOSE_FILE="docker-compose.yml"
        ;;
esac

echo ""
print_status "Selected deployment type: $DEPLOYMENT_TYPE"

# Create necessary directories
echo -e "${BLUE}📁 Creating Directories${NC}"
echo "=========================="

mkdir -p logs data temp monitoring/prometheus monitoring/grafana/dashboards monitoring/grafana/datasources
print_status "Created necessary directories"

# Set up database initialization
if [ ! -f "init-db/init.sql" ]; then
    mkdir -p init-db
    cat > init-db/init.sql << 'EOF'
-- Product Sourcing Service Database Initialization

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create product_discoveries table
CREATE TABLE IF NOT EXISTS product_discoveries (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255),
    keywords JSONB,
    filters JSONB,
    status VARCHAR(50) DEFAULT 'pending',
    results JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create product_analyses table
CREATE TABLE IF NOT EXISTS product_analyses (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(255),
    asin VARCHAR(255),
    product_data JSONB,
    scoring_results JSONB,
    classification VARCHAR(50),
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trend_analyses table
CREATE TABLE IF NOT EXISTS trend_analyses (
    id SERIAL PRIMARY KEY,
    query VARCHAR(500) NOT NULL,
    platforms JSONB,
    trend_data JSONB,
    overall_score FLOAT,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_product_discoveries_task_id ON product_discoveries(task_id);
CREATE INDEX IF NOT EXISTS idx_product_discoveries_user_id ON product_discoveries(user_id);
CREATE INDEX IF NOT EXISTS idx_product_discoveries_status ON product_discoveries(status);
CREATE INDEX IF NOT EXISTS idx_product_analyses_asin ON product_analyses(asin);
CREATE INDEX IF NOT EXISTS idx_product_analyses_classification ON product_analyses(classification);
CREATE INDEX IF NOT EXISTS idx_trend_analyses_query ON trend_analyses USING gin(to_tsvector('english', query));

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for updated_at
DROP TRIGGER IF EXISTS update_product_discoveries_updated_at ON product_discoveries;
CREATE TRIGGER update_product_discoveries_updated_at
    BEFORE UPDATE ON product_discoveries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
EOF
    print_status "Created database initialization script"
fi

# Set up monitoring configuration
if [ ! -f "monitoring/prometheus.yml" ]; then
    cat > monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'product-sourcing'
    static_configs:
      - targets: ['product-sourcing:8026']
    scrape_interval: 10s
    metrics_path: '/metrics'

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
EOF
    print_status "Created Prometheus configuration"
fi

# Docker operations
echo ""
echo -e "${BLUE}🐳 Docker Operations${NC}"
echo "======================="

# Stop existing containers
if docker-compose ps | grep -q "product-sourcing"; then
    print_status "Stopping existing containers..."
    docker-compose down
fi

# Build Docker image
echo ""
print_status "Building Docker image..."
docker build -t $DOCKER_IMAGE:$DOCKER_TAG .

if [ $? -eq 0 ]; then
    print_status "Docker image built successfully"
else
    print_error "Failed to build Docker image"
    exit 1
fi

# Start services
echo ""
print_status "Starting services with $COMPOSE_FILE..."

if [ -f "$COMPOSE_FILE" ]; then
    docker-compose -f $COMPOSE_FILE up -d
else
    print_warning "$COMPOSE_FILE not found, using default docker-compose.yml"
    docker-compose up -d
fi

if [ $? -eq 0 ]; then
    print_status "Services started successfully"
else
    print_error "Failed to start services"
    exit 1
fi

# Wait for services to be ready
echo ""
echo -e "${BLUE}⏳ Waiting for Services${NC}"
echo "========================="

print_status "Waiting for Product Sourcing service to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:$SERVICE_PORT/health > /dev/null; then
        print_status "Product Sourcing service is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Service failed to start within 30 seconds"
        echo "Check logs with: docker-compose logs product-sourcing"
        exit 1
    fi
    sleep 1
done

# Verify deployment
echo ""
echo -e "${BLUE}✅ Verifying Deployment${NC}"
echo "=========================="

# Test health endpoint
health_response=$(curl -s http://localhost:$SERVICE_PORT/health)
if echo "$health_response" | grep -q "healthy"; then
    print_status "Health check passed"
else
    print_error "Health check failed"
    echo "Response: $health_response"
fi

# Test API endpoints
api_docs_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$SERVICE_PORT/docs)
if [ "$api_docs_response" = "200" ]; then
    print_status "API documentation accessible"
else
    print_warning "API documentation not accessible (HTTP $api_docs_response)"
fi

# Check database connection
db_test=$(docker-compose exec -T product-sourcing python -c "
import asyncio
import asyncpg
import os
async def test_db():
    try:
        conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
        await conn.close()
        print('Database connection successful')
    except Exception as e:
        print(f'Database connection failed: {e}')
asyncio.run(test_db())
" 2>/dev/null)

if echo "$db_test" | grep -q "successful"; then
    print_status "Database connection verified"
else
    print_warning "Database connection issues detected"
fi

# Display service information
echo ""
echo -e "${BLUE}🌐 Service Information${NC}"
echo "========================"
echo "Service URL:           http://localhost:$SERVICE_PORT"
echo "API Documentation:     http://localhost:$SERVICE_PORT/docs"
echo "ReDoc Documentation:   http://localhost:$SERVICE_PORT/redoc"
echo "Health Check:          http://localhost:$SERVICE_PORT/health"

if docker-compose ps | grep -q "flower"; then
    echo "Celery Monitoring:     http://localhost:5556"
fi

if docker-compose ps | grep -q "grafana"; then
    echo "Grafana Dashboard:     http://localhost:3001 (admin/admin)"
fi

if docker-compose ps | grep -q "prometheus"; then
    echo "Prometheus Metrics:    http://localhost:9091"
fi

echo ""
echo -e "${BLUE}📊 Container Status${NC}"
echo "==================="
docker-compose ps

echo ""
echo -e "${BLUE}💾 Resource Usage${NC}"
echo "=================="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep -E "(product-sourcing|redis|postgres)"

# Deployment completion
echo ""
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "=========================="
print_status "$SERVICE_NAME is now running on port $SERVICE_PORT"
print_status "Deployment type: $DEPLOYMENT_TYPE"

# Show quick start commands
echo ""
echo -e "${BLUE}🚀 Quick Start Commands${NC}"
echo "========================="
echo "Test the service:"
echo "  curl http://localhost:$SERVICE_PORT/health"
echo ""
echo "View logs:"
echo "  docker-compose logs -f product-sourcing"
echo ""
echo "Stop services:"
echo "  docker-compose down"
echo ""
echo "Restart services:"
echo "  docker-compose restart"
echo ""
echo "Update service:"
echo "  docker-compose pull && docker-compose up -d"

# Show example API call
echo ""
echo -e "${BLUE}📝 Example API Usage${NC}"
echo "====================="
cat << 'EOF'
# Test trending products
curl -X GET "http://localhost:8026/api/product-sourcing/trends?category=electronics&limit=5"

# Start product discovery
curl -X POST "http://localhost:8026/api/product-sourcing/discover" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["wireless earbuds", "bluetooth headphones"],
    "category": "electronics",
    "market_region": "IN"
  }'

# Analyze specific product
curl -X POST "http://localhost:8026/api/product-sourcing/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "product_title": "Premium Wireless Headphones",
    "current_price": 2999,
    "category": "electronics"
  }'
EOF

echo ""
echo -e "${GREEN}✨ Deployment successful! Service is ready for use.${NC}"

# Optional: Open browser to documentation
if command_exists xdg-open; then
    read -p "Open API documentation in browser? (y/N): " open_browser
    if [[ $open_browser =~ ^[Yy]$ ]]; then
        xdg-open "http://localhost:$SERVICE_PORT/docs"
    fi
elif command_exists open; then
    read -p "Open API documentation in browser? (y/N): " open_browser
    if [[ $open_browser =~ ^[Yy]$ ]]; then
        open "http://localhost:$SERVICE_PORT/docs"
    fi
fi

echo ""
print_status "For support and documentation, visit: http://localhost:$SERVICE_PORT/docs"
echo "Happy product sourcing! 🛍️"