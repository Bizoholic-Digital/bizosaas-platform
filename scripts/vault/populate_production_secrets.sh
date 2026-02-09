#!/bin/bash
# populate_production_secrets.sh
# Interactive script to populate core production secrets into Vault

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔐 Vault Production Secret Population Tool${NC}"
echo "==========================================="

# Check if Vault container is running
if ! docker ps | grep -q bizosaas-vault; then
    echo -e "${RED}Error: bizosaas-vault container is not running.${NC}"
    echo "Please run: docker compose up -d vault"
    exit 1
fi

echo -e "${YELLOW}This script will ask for your production secrets and store them securely in Vault.${NC}"
echo "You will need your Vault ROOT TOKEN (generated during unseal)."
echo ""

# Get Vault Token
read -s -p "Enter Vault Root Token: " VAULT_TOKEN
echo ""
if [ -z "$VAULT_TOKEN" ]; then
    echo -e "${RED}Token cannot be empty.${NC}"
    exit 1
fi

# Function to store secret
store_secret() {
    local path=$1
    local key=$2
    local value=$3
    
    echo -n "Storing $path... "
    # We use docker exec to run vault kv put inside the container
    # We pass the token via env var ensuring it's not logged (mostly)
    # But passing via command line arg is visible in ps. 
    # Better: Use VAULT_TOKEN env var inside container.
    
    # Check if secret exists first to avoid overwriting blindly? 
    # No, we want to update.
    
    # We construct the JSON payload
    # Note: Vault KV v2 uses "data" wrapper implicitly with "kv put"
    
    # Exec into container
    docker exec -e VAULT_TOKEN="$VAULT_TOKEN" -e VAULT_ADDR="http://127.0.0.1:8200" bizosaas-vault \
        vault kv put -mount=secret "$path" "$key=$value" > /dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}Failed${NC}"
    fi
}

echo ""
echo "=== 1. Core Platform Secrets ==="
read -s -p "Enter Django Secret Key: " DJANGO_KEY
echo ""
if [ ! -z "$DJANGO_KEY" ]; then
    store_secret "production/core/django" "secret_key" "$DJANGO_KEY"
fi

read -s -p "Enter Postgres Password: " DB_PASS
echo ""
if [ ! -z "$DB_PASS" ]; then
    store_secret "production/core/database" "password" "$DB_PASS"
fi

read -s -p "Enter Redis Password: " REDIS_PASS
echo ""
if [ ! -z "$REDIS_PASS" ]; then
    store_secret "production/core/redis" "password" "$REDIS_PASS"
fi

echo ""
echo "=== 2. Integration Credentials ==="
echo "Leave empty to skip."

read -s -p "Enter Shopify App Client Secret: " SHOPIFY_SECRET
echo ""
if [ ! -z "$SHOPIFY_SECRET" ]; then
    store_secret "production/integrations/shopify" "client_secret" "$SHOPIFY_SECRET"
fi

read -s -p "Enter HubSpot App Developer Key: " HUBSPOT_KEY
echo ""
if [ ! -z "$HUBSPOT_KEY" ]; then
    store_secret "production/integrations/hubspot" "developer_key" "$HUBSPOT_KEY"
fi

read -s -p "Enter Google OAuth Client Secret: " GOOGLE_SECRET
echo ""
if [ ! -z "$GOOGLE_SECRET" ]; then
    store_secret "production/integrations/google" "client_secret" "$GOOGLE_SECRET"
fi

echo ""
echo -e "${GREEN}✅ Secret population complete!${NC}"
echo "You can verify secrets by entering the Vault container:"
echo "docker exec -it bizosaas-vault vault kv get -mount=secret production/core/django"
