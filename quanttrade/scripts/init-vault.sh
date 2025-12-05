#!/bin/bash
# QuantTrade Vault Initialization (Docker-based)
# Works directly with Vault container

set -e

echo "🔐 Initializing QuantTrade Secrets in Vault (via Docker)..."
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

VAULT_CONTAINER="bizosaas-vault-unified"

# Check if Vault container is running
if ! docker ps | grep -q "$VAULT_CONTAINER"; then
    echo -e "${RED}Error: Vault container '$VAULT_CONTAINER' is not running${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Vault container is running${NC}"
echo ""

# Function to create secret via Docker
create_secret() {
    local path=$1
    shift
    echo -n "Creating secret: $path... "
    
    # Build the command with all key-value pairs
    local cmd="vault kv put secret/$path"
    for arg in "$@"; do
        cmd="$cmd $arg"
    done
    
    if docker exec $VAULT_CONTAINER sh -c "VAULT_TOKEN=root $cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}⚠ (may already exist)${NC}"
    fi
}

echo "Setting up QuantTrade secrets..."
echo ""

# Create Deribit exchange credentials
create_secret "quanttrade/exchanges/deribit" \
    "api_key=YOUR_DERIBIT_API_KEY" \
    "api_secret=YOUR_DERIBIT_API_SECRET" \
    "testnet=true"

# Create Binance exchange credentials
create_secret "quanttrade/exchanges/binance" \
    "api_key=YOUR_BINANCE_API_KEY" \
    "api_secret=YOUR_BINANCE_API_SECRET" \
    "testnet=true"

# Create database credentials
create_secret "quanttrade/database" \
    "host=bizosaas-postgres-unified" \
    "port=5432" \
    "database=bizosaas" \
    "username=postgres" \
    "password=postgres"

# Create Brain API credentials
create_secret "quanttrade/brain-api" \
    "url=http://localhost:8002" \
    "api_key=YOUR_BRAIN_API_KEY"

# Create JWT secret
JWT_SECRET=$(openssl rand -base64 32)
create_secret "quanttrade/auth" \
    "secret_key=$JWT_SECRET" \
    "algorithm=HS256"

# Create trading configuration
create_secret "quanttrade/config" \
    "default_risk_per_trade=0.02" \
    "max_position_size=0.10" \
    "enable_paper_trading=true"

echo ""
echo -e "${GREEN}✅ Vault initialization complete!${NC}"
echo ""
echo "📋 Created secrets:"
echo "  • quanttrade/exchanges/deribit"
echo "  • quanttrade/exchanges/binance"
echo "  • quanttrade/database"
echo "  • quanttrade/brain-api"
echo "  • quanttrade/auth"
echo "  • quanttrade/config"
echo ""
echo "⚠️  Update with real credentials:"
echo ""
echo "docker exec $VAULT_CONTAINER sh -c 'VAULT_TOKEN=root vault kv patch secret/quanttrade/exchanges/deribit api_key=\"YOUR_KEY\" api_secret=\"YOUR_SECRET\"'"
echo ""
echo "🔍 Verify secrets:"
echo "docker exec $VAULT_CONTAINER sh -c 'VAULT_TOKEN=root vault kv get secret/quanttrade/exchanges/deribit'"
echo ""
