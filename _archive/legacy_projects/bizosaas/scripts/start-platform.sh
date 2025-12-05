#!/bin/bash

# BizOSaaS Platform - Complete Startup Script
# Starts all platform services in the correct order
# Run with: bash scripts/start-platform.sh

set -e

echo "🚀 BizOSaaS Platform - Complete Startup"
echo "======================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if service is running
check_service() {
    local service_name=$1
    local port=$2

    if docker ps | grep -q "$service_name"; then
        echo -e "${GREEN}✓${NC} $service_name is running"
        return 0
    else
        echo -e "${RED}✗${NC} $service_name is NOT running"
        return 1
    fi
}

# Function to wait for service health
wait_for_health() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=0

    echo -n "  Waiting for $service_name to be healthy..."

    while [ $attempt -lt $max_attempts ]; do
        if curl -sf "$url" > /dev/null 2>&1; then
            echo -e " ${GREEN}✓${NC}"
            return 0
        fi
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done

    echo -e " ${YELLOW}⚠${NC} (timeout, continuing anyway)"
    return 1
}

echo "📊 Current Platform Status:"
echo ""

# Check infrastructure
echo "Infrastructure Services:"
check_service "bizosaas-postgres-unified" "5432"
check_service "bizosaas-redis-unified" "6379"
check_service "bizosaas-vault" "8200"

echo ""
echo "Backend Services:"
check_service "bizosaas-brain-unified" "8001"
check_service "bizosaas-django-crm" "8003"
check_service "bizosaas-wagtail-cms" "8002"
check_service "bizosaas-saleor-unified" "8000"
check_service "bizosaas-auth-unified" "8007"
check_service "bizosaas-temporal-unified" "8009"
check_service "bizosaas-ai-agents" "8010"

echo ""
echo "Frontend Applications:"
check_service "bizoholic-frontend" "3000"
check_service "client-portal" "3001"
check_service "coreldove-frontend" "3002"
check_service "business-directory" "3004"
check_service "thrillring-gaming" "3005"
check_service "bizosaas-admin" "3009"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Ask if user wants to start monitoring stack
echo "Optional: Start Monitoring Stack (Elasticsearch, Prometheus, Grafana)?"
echo "  This adds ~4GB memory usage but enables full LLM monitoring dashboards."
echo ""
read -p "Start monitoring stack? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔧 Starting Monitoring Stack..."
    cd /home/alagiri/projects/bizoholic/bizosaas/ai/services/bizosaas-brain

    if [ -f "docker-compose.brain-monitoring.yml" ]; then
        docker-compose -f docker-compose.brain-monitoring.yml up -d
        echo ""
        echo "Monitoring services starting..."

        wait_for_health "http://localhost:9200/_cluster/health" "Elasticsearch"
        wait_for_health "http://localhost:9090/-/healthy" "Prometheus"
        wait_for_health "http://localhost:3030/api/health" "Grafana"

        echo ""
        echo "📊 Monitoring Stack URLs:"
        echo "  Grafana:       http://localhost:3030 (admin/bizosaas2025)"
        echo "  Prometheus:    http://localhost:9090"
        echo "  Elasticsearch: http://localhost:9200"
        echo "  Kibana:        http://localhost:5601"
    else
        echo -e "${RED}✗${NC} docker-compose.brain-monitoring.yml not found"
    fi

    cd - > /dev/null
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ BizOSaaS Platform Status Check Complete!"
echo ""
echo "🌐 Access URLs:"
echo ""
echo "FRONTEND APPLICATIONS:"
echo "  Bizoholic Marketing:    http://localhost:3000"
echo "  Client Portal:          http://localhost:3001"
echo "  CorelDove E-commerce:   http://localhost:3002"
echo "  Business Directory:     http://localhost:3004"
echo "  ThrillRing Gaming:      http://localhost:3005"
echo "  BizOSaaS Admin:         http://localhost:3009"
echo ""
echo "BACKEND APIs:"
echo "  Brain API Gateway:      http://localhost:8001/docs"
echo "  Wagtail CMS:            http://localhost:8002/admin"
echo "  Django CRM:             http://localhost:8003/admin"
echo "  Auth Service:           http://localhost:8007/docs"
echo "  AI Agents:              http://localhost:8010/docs"
echo "  Temporal UI:            http://localhost:8082"
echo "  Apache Superset:        http://localhost:8088"
echo ""
echo "📝 Quick Tests:"
echo "  curl http://localhost:8001/health        # Brain API health"
echo "  curl http://localhost:8001/api/brain/llm/providers/health  # LLM providers"
echo ""
echo "📖 Documentation:"
echo "  Platform Status:   /bizosaas/PLATFORM_STATUS_REPORT.md"
echo "  Integration Guide: /bizosaas/COMPLETE_INTEGRATION_VERIFICATION.md"
echo "  LLM Integration:   /bizosaas/LLM_INTEGRATION_COMPLETE_SUMMARY.md"
echo ""
echo "🎉 Platform ready for testing!"
