#!/bin/bash
# start-client-portal.sh
# Starts the Client Portal frontend on port 3003

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PORTAL_DIR="$PROJECT_ROOT/portals/client-portal"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Starting Client Portal...${NC}"
cd "$PORTAL_DIR"

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo -e "${GREEN}Client Portal running at http://localhost:3003${NC}"
# Use npx next dev directly to override the package.json script's port 3000
npx next dev -p 3003
