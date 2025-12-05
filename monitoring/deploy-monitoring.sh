#!/bin/bash
# Deploy Monitoring Services
# Grafana + Prometheus as containerized microservices

set -e

echo "🔍 Deploying BizOSaaS Monitoring Services"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running from correct directory
if [ ! -f "docker-compose.monitoring.yml" ]; then
    echo "Error: Please run this script from the monitoring directory"
    exit 1
fi

echo -e "${BLUE}Step 1: Create BizOSaaS Network (if not exists)${NC}"
echo "================================================"
docker network create bizosaas-network 2>/dev/null && echo -e "${GREEN}✓ Network created${NC}" || echo -e "${YELLOW}Network already exists${NC}"

echo ""
echo -e "${BLUE}Step 2: Create Grafana Database${NC}"
echo "================================"
docker exec bizosaas-postgres-unified psql -U postgres -c "CREATE DATABASE grafana;" 2>/dev/null && echo -e "${GREEN}✓ Database created${NC}" || echo -e "${YELLOW}Database already exists${NC}"

echo ""
echo -e "${BLUE}Step 3: Start Monitoring Services${NC}"
echo "=================================="
docker compose -f docker-compose.monitoring.yml up -d

echo ""
echo -e "${BLUE}Step 4: Wait for Services${NC}"
echo "========================="
echo "Waiting for Prometheus..."
sleep 5

echo "Waiting for Grafana..."
sleep 10

echo ""
echo -e "${GREEN}✅ Monitoring Services Deployed!${NC}"
echo "================================"
echo ""
echo "📊 Access Points:"
echo "  • Prometheus:  http://localhost:9090"
echo "  • Grafana:     http://localhost:3000"
echo "    - Username: admin"
echo "    - Password: admin (change on first login)"
echo ""
echo "📈 Exporters:"
echo "  • Node Exporter:     http://localhost:9100"
echo "  • Postgres Exporter: http://localhost:9187"
echo "  • Redis Exporter:    http://localhost:9121"
echo ""
echo "🔧 Services:"
echo "  • bizosaas-prometheus"
echo "  • bizosaas-grafana"
echo "  • bizosaas-node-exporter"
echo "  • bizosaas-postgres-exporter"
echo "  • bizosaas-redis-exporter"
echo ""
echo "📝 Next Steps:"
echo "  1. Access Grafana at http://localhost:3000"
echo "  2. Login with admin/admin"
echo "  3. Change password"
echo "  4. Explore pre-configured dashboards"
echo ""
echo "🔍 View logs:"
echo "  docker compose -f docker-compose.monitoring.yml logs -f"
echo ""
echo -e "${GREEN}Happy Monitoring! 📊${NC}"
