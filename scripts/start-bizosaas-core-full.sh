#!/bin/bash
# start-bizosaas-core-full.sh
# Starts the entire BizOSaaS Brain Core stack for local development/testing.
# Usage: ./scripts/start-bizosaas-core-full.sh [--wait]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BRAIN_CORE_DIR="$PROJECT_ROOT/bizosaas-brain-core"

# Configuration
MAX_RETRIES=30
RETRY_INTERVAL=2
WAIT_FOR_HEALTH=false

# Check arguments
if [[ "$1" == "--wait" ]]; then
    WAIT_FOR_HEALTH=true
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper function for health checks
wait_for_service() {
    local service_name="$1"
    local check_cmd="$2"
    local retries=$MAX_RETRIES

    echo -ne "${YELLOW}    Waiting for $service_name...${NC}"

    until eval "$check_cmd" > /dev/null 2>&1; do
        ((retries--))
        if [ $retries -le 0 ]; then
            echo -e "\r${RED}✗ Failed to connect to $service_name after $((MAX_RETRIES * RETRY_INTERVAL))s.${NC}"
            return 1
        fi
        echo -ne "."
        sleep $RETRY_INTERVAL
    done
    echo -e "\r${GREEN}✓ $service_name is healthy.             ${NC}"
    return 0
}

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   BizOSaaS Brain Core - Full Startup    ${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# --- Step 1: Check Prerequisites ---
echo -e "${CYAN}[1/6] Checking Prerequisites...${NC}"
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
echo -e "${CYAN}[2/6] Creating Docker Network...${NC}"
docker network create brain-network 2>/dev/null || true
echo -e "${GREEN}✓ Network 'brain-network' ready.${NC}"

# --- Step 3: Infrastructure (Postgres, Redis, Vault) ---
echo -e "${CYAN}[3/6] Starting Infrastructure...${NC}"
cd "$BRAIN_CORE_DIR"
docker compose up -d postgres redis vault
echo -e "${GREEN}✓ Infrastructure containers started.${NC}"

if [ "$WAIT_FOR_HEALTH" = true ]; then
    wait_for_service "Postgres" "docker compose exec -T postgres pg_isready -U postgres"
    wait_for_service "Redis" "docker compose exec -T redis redis-cli ping"
    # Vault might take a moment to initialize
    sleep 5
    wait_for_service "Vault" "curl -s http://localhost:8200/v1/sys/health | grep -q 'initialized'"
fi

# --- Step 4: Start Core Services ---
echo -e "${CYAN}[4/6] Starting Core Services...${NC}"
docker compose up -d brain-gateway ai-agents temporal temporal-ui
echo -e "${GREEN}✓ Core service containers started.${NC}"

if [ "$WAIT_FOR_HEALTH" = true ]; then
    wait_for_service "Temporal" "curl -s http://localhost:7233 || docker compose logs temporal --tail 10 | grep -q 'Started'"
    # Brain Gateway health check
    wait_for_service "Brain Gateway" "curl -s http://localhost:8000/health"
    # Auth Service health check (assuming /health or root endpoint)
    wait_for_service "Auth Service" "curl -s http://localhost:8009/health || curl -s http://localhost:8009/"
fi

# --- Step 5: Start Observability Stack ---
echo -e "${CYAN}[5/6] Starting Observability Stack...${NC}"
docker compose -f docker-compose.observability.yml up -d
echo -e "${GREEN}✓ Observability containers started.${NC}"

# --- Step 6: Start Client Portal ---
echo -e "${CYAN}[6/6] Starting Client Portal...${NC}"
if [ -f "$SCRIPT_DIR/start-client-portal.sh" ]; then
    bash "$SCRIPT_DIR/start-client-portal.sh" > /dev/null 2>&1 &
    CLIENT_PID=$!
    echo -e "${GREEN}✓ Client Portal script running (PID: $CLIENT_PID).${NC}"
    
    if [ "$WAIT_FOR_HEALTH" = true ]; then
        wait_for_service "Client Portal" "curl -s http://localhost:3003"
    fi
else
    echo -e "${YELLOW}Client Portal script not found at $SCRIPT_DIR/start-client-portal.sh${NC}"
    # Try direct docker compose if script missing
    docker compose up -d client-portal
fi

echo ""
echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}      Startup Sequence Complete!         ${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""
echo -e "Service Status Summary:"
echo -e "-----------------------------------------"
printf "${CYAN}%-20s ${GREEN}%-30s${NC}\n" "Service" "URL"
printf "%-20s %-30s\n" "Client Portal" "http://localhost:3003"
printf "%-20s %-30s\n" "Brain Gateway API" "http://localhost:8000"
printf "%-20s %-30s\n" "Auth Service" "http://localhost:8009"
printf "%-20s %-30s\n" "Vault (Secrets)" "http://localhost:8200"
printf "%-20s %-30s\n" "Temporal UI" "http://localhost:8081"
printf "%-20s %-30s\n" "Grafana" "http://localhost:3002"
echo ""
echo -e "${YELLOW}Note: Use './scripts/start-bizosaas-core-full.sh --wait' to block until all services are healthy.${NC}"
echo -e "To view logs: ${YELLOW}docker compose -f $BRAIN_CORE_DIR/docker-compose.yml logs -f${NC}"
echo -e "To stop all:  ${YELLOW}./scripts/stop-bizosaas-core-full.sh${NC}"
