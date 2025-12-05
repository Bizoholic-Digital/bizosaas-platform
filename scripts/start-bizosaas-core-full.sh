#!/bin/bash
# start-bizosaas-core-full.sh
# Starts the entire BizOSaaS Brain Core stack for local development/testing.
# Usage: ./scripts/start-bizosaas-core-full.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BRAIN_CORE_DIR="$PROJECT_ROOT/bizosaas-brain-core"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  BizOSaaS Brain Core - Full Startup   ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# --- Step 1: Check Prerequisites ---
echo -e "${YELLOW}[1/5] Checking Prerequisites...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Aborting.${NC}"
    exit 1
fi
if ! command -v docker compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Docker Compose is not available. Aborting.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker and Docker Compose found.${NC}"

# --- Step 2: Create Docker Network ---
echo -e "${YELLOW}[2/5] Creating Docker Network...${NC}"
docker network create brain-network 2>/dev/null || true
echo -e "${GREEN}✓ Network 'brain-network' ready.${NC}"

# --- Step 3: Start Infrastructure (Postgres, Redis) ---
echo -e "${YELLOW}[3/5] Starting Infrastructure (Postgres, Redis)...${NC}"
cd "$BRAIN_CORE_DIR"
docker compose up -d postgres redis
echo -e "${GREEN}✓ Infrastructure services starting.${NC}"

# Wait for Postgres to be healthy
echo -e "${YELLOW}    Waiting for Postgres to be healthy...${NC}"
until docker compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; do
    sleep 2
done
echo -e "${GREEN}✓ Postgres is healthy.${NC}"

# --- Step 4: Start Core Services (Brain Gateway, Auth, Temporal) ---
echo -e "${YELLOW}[4/5] Starting Core Services (Brain Gateway, Auth, Temporal)...${NC}"
docker compose up -d brain-gateway auth-service temporal
echo -e "${GREEN}✓ Core services starting.${NC}"

# --- Step 5: Start Observability Stack (Loki, Prometheus, Grafana, Jaeger) ---
echo -e "${YELLOW}[5/5] Starting Observability Stack...${NC}"
docker compose -f docker-compose.observability.yml up -d
echo -e "${GREEN}✓ Observability stack starting.${NC}"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  All Services Started!               ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Service URLs:"
echo -e "  - Brain Gateway API:  ${GREEN}http://localhost:8000${NC}"
echo -e "  - Auth Service:       ${GREEN}http://localhost:8009${NC}"
echo -e "  - Temporal UI:        ${GREEN}http://localhost:7233${NC} (via CLI)"
echo -e "  - Grafana Dashboard:  ${GREEN}http://localhost:3002${NC} (admin/admin)"
echo -e "  - Prometheus:         ${GREEN}http://localhost:9090${NC}"
echo -e "  - Jaeger UI:          ${GREEN}http://localhost:16686${NC} (admin/admin)"
echo ""
echo -e "To view logs: ${YELLOW}docker compose -f $BRAIN_CORE_DIR/docker-compose.yml logs -f${NC}"
echo -e "To stop all:  ${YELLOW}./scripts/stop-bizosaas-core-full.sh${NC}"
