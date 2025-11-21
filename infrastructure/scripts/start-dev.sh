#!/bin/bash

# BizoholicSaaS Development Environment Startup Script
# This script starts all microservices and supporting infrastructure

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="bizosaas"
COMPOSE_FILE="docker-compose.dev.yml"
ENV_FILE=".env"

echo -e "${BLUE}🚀 Starting BizoholicSaaS Development Environment${NC}"
echo "=================================================="

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}⚠️  Environment file not found. Creating from template...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Created .env file from template${NC}"
        echo -e "${YELLOW}📝 Please edit .env file with your specific configuration${NC}"
    else
        echo -e "${RED}❌ .env.example not found. Please create .env file manually${NC}"
        exit 1
    fi
fi

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose >/dev/null 2>&1; then
    if ! docker compose version >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker Compose is not available${NC}"
        exit 1
    fi
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo -e "${BLUE}🔧 Using Docker Compose: $DOCKER_COMPOSE${NC}"

# Function to check service health
check_service_health() {
    local service=$1
    local port=$2
    local max_attempts=30
    local attempt=1
    
    echo -e "${YELLOW}🏥 Checking health of $service on port $port...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "http://localhost:$port/health" >/dev/null 2>&1; then
            echo -e "${GREEN}✅ $service is healthy${NC}"
            return 0
        fi
        
        echo -e "${YELLOW}⏳ Waiting for $service to be ready (attempt $attempt/$max_attempts)...${NC}"
        sleep 5
        attempt=$((attempt + 1))
    done
    
    echo -e "${RED}❌ $service failed to become healthy${NC}"
    return 1
}

# Function to show service status
show_service_status() {
    echo -e "${BLUE}📊 Service Status:${NC}"
    $DOCKER_COMPOSE -f $COMPOSE_FILE ps
}

# Start infrastructure services first
echo -e "${BLUE}🏗️  Starting infrastructure services...${NC}"
$DOCKER_COMPOSE -f $COMPOSE_FILE up -d postgres redis rabbitmq

echo -e "${YELLOW}⏳ Waiting for infrastructure to be ready...${NC}"
sleep 15

# Check infrastructure health
echo -e "${BLUE}🔍 Checking infrastructure health...${NC}"

# Wait for PostgreSQL
echo -e "${YELLOW}⏳ Waiting for PostgreSQL...${NC}"
until $DOCKER_COMPOSE -f $COMPOSE_FILE exec -T postgres pg_isready -U bizosaas -d bizosaas >/dev/null 2>&1; do
    echo -e "${YELLOW}⏳ PostgreSQL is still starting...${NC}"
    sleep 2
done
echo -e "${GREEN}✅ PostgreSQL is ready${NC}"

# Wait for Redis
echo -e "${YELLOW}⏳ Waiting for Redis...${NC}"
until $DOCKER_COMPOSE -f $COMPOSE_FILE exec -T redis redis-cli ping >/dev/null 2>&1; do
    echo -e "${YELLOW}⏳ Redis is still starting...${NC}"
    sleep 2
done
echo -e "${GREEN}✅ Redis is ready${NC}"

# Start core microservices
echo -e "${BLUE}🚀 Starting core microservices...${NC}"
$DOCKER_COMPOSE -f $COMPOSE_FILE up -d \
    user-management \
    campaign-management \
    analytics \
    integration \
    notification \
    ai-agents

# Wait for core services to be ready
sleep 10

# Check core service health
echo -e "${BLUE}🏥 Checking core services health...${NC}"
check_service_health "User Management" 8001
check_service_health "Campaign Management" 8002
check_service_health "Analytics" 8003
check_service_health "Integration" 8004
check_service_health "Notification" 8005
check_service_health "AI Agents" 8000

# Start API Gateway last
echo -e "${BLUE}🌐 Starting API Gateway...${NC}"
$DOCKER_COMPOSE -f $COMPOSE_FILE up -d api-gateway

sleep 5
check_service_health "API Gateway" 8080

# Start supporting services
echo -e "${BLUE}🔧 Starting supporting services...${NC}"
$DOCKER_COMPOSE -f $COMPOSE_FILE up -d \
    strapi \
    mautic \
    adminer \
    redis-commander

echo -e "${BLUE}🔧 Starting development tools...${NC}"

# Show final status
echo
echo -e "${GREEN}🎉 BizoholicSaaS Development Environment Started Successfully!${NC}"
echo "============================================================"

show_service_status

echo
echo -e "${BLUE}📋 Service Endpoints:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🌐 API Gateway:          http://localhost:8080${NC}"
echo -e "${GREEN}👥 User Management:      http://localhost:8001${NC}"
echo -e "${GREEN}📊 Campaign Management:  http://localhost:8002${NC}"
echo -e "${GREEN}📈 Analytics:            http://localhost:8003${NC}"
echo -e "${GREEN}🔗 Integration:          http://localhost:8004${NC}"
echo -e "${GREEN}📢 Notification:         http://localhost:8005${NC}"
echo -e "${GREEN}🤖 AI Agents:            http://localhost:8000${NC}"
echo
echo -e "${BLUE}🔧 Supporting Services:${NC}"
echo -e "${GREEN}📝 Strapi CMS:           http://localhost:1337${NC}"
echo -e "${GREEN}📧 Mautic:               http://localhost:8090${NC}"
echo -e "${GREEN}💽 Database Admin:       http://localhost:8082${NC}"
echo -e "${GREEN}🔴 Redis Commander:      http://localhost:8083${NC}"

echo
echo -e "${BLUE}📚 API Documentation:${NC}"
echo -e "${GREEN}🌐 API Gateway Docs:     http://localhost:8080/docs${NC}"
echo -e "${GREEN}👥 User Management:      http://localhost:8001/docs${NC}"
echo -e "${GREEN}📊 Campaign Management:  http://localhost:8002/docs${NC}"
echo -e "${GREEN}📈 Analytics:            http://localhost:8003/docs${NC}"
echo -e "${GREEN}🔗 Integration:          http://localhost:8004/docs${NC}"
echo -e "${GREEN}📢 Notification:         http://localhost:8005/docs${NC}"
echo -e "${GREEN}🤖 AI Agents:            http://localhost:8000/docs${NC}"

echo
echo -e "${BLUE}🔑 Default Credentials:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}Database:   bizosaas / bizosaas_password${NC}"
echo -e "${YELLOW}Adminer:    No authentication required${NC}"
echo -e "${YELLOW}RabbitMQ:   bizosaas / bizosaas_password${NC}"

echo
echo -e "${BLUE}🛠️  Useful Commands:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}View logs:         $DOCKER_COMPOSE -f $COMPOSE_FILE logs -f [service]${NC}"
echo -e "${YELLOW}Stop all:          $DOCKER_COMPOSE -f $COMPOSE_FILE down${NC}"
echo -e "${YELLOW}Restart service:   $DOCKER_COMPOSE -f $COMPOSE_FILE restart [service]${NC}"
echo -e "${YELLOW}View status:       $DOCKER_COMPOSE -f $COMPOSE_FILE ps${NC}"
echo -e "${YELLOW}Shell into service: $DOCKER_COMPOSE -f $COMPOSE_FILE exec [service] /bin/bash${NC}"

echo
echo -e "${GREEN}🎯 Quick Test:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}curl http://localhost:8080/health${NC}"

echo
echo -e "${BLUE}📖 For more information, check the README.md file${NC}"
echo -e "${GREEN}✨ Happy coding! ✨${NC}"