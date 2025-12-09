#!/bin/bash
# Initialize HashiCorp Vault for BizOSaaS

set -e

export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

# Colors
GREEN='\033[0;32m'
NC='\033[0m'

echo "Waiting for Vault..."
while ! curl -s $VAULT_ADDR/v1/sys/health > /dev/null; do
  sleep 1
done

echo -e "${GREEN}Vault is running!${NC}"

# Enable KV secrets engine version 2
if ! vault secrets list | grep -q "secret/"; then
    echo "Enabling KV v2 secrets engine..."
    docker exec bizosaas-vault vault secrets enable -path=secret kv-v2
else
    echo "KV v2 engine already enabled."
fi

# Store test secret
echo "Storing test secret..."
docker exec bizosaas-vault vault kv put secret/test message="Hello BizOSaaS"

# Read test secret
echo "Reading test secret..."
docker exec bizosaas-vault vault kv get secret/test

echo -e "${GREEN}Vault initialization complete!${NC}"
