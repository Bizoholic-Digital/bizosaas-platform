#!/bin/bash
# stop-bizosaas-core-full.sh
# Stops all BizOSaaS Brain Core services.
# Usage: ./scripts/stop-bizosaas-core-full.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BRAIN_CORE_DIR="$PROJECT_ROOT/bizosaas-brain-core"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Stopping BizOSaaS Brain Core services...${NC}"

cd "$BRAIN_CORE_DIR"

# Stop Observability
docker compose -f docker-compose.observability.yml down 2>/dev/null || true

# Stop Core Services
docker compose down 2>/dev/null || true

echo -e "${GREEN}✓ All services stopped.${NC}"
