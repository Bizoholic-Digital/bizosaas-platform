#!/bin/bash
# File: infrastructure/vault/scripts/vault-init.sh

set -e

# Configuration
VAULT_ADDR=${VAULT_ADDR:-"http://localhost:8200"}
VAULT_TOKEN=${VAULT_TOKEN:-""}

if [ -z "$VAULT_TOKEN" ]; then
    echo "ERROR: VAULT_TOKEN is not set."
    exit 1
fi

export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$VAULT_TOKEN

echo "--- Configuring Vault for BizOSaaS ---"

# 1. Enable KV v2 engine if not already enabled
if ! vault secrets list | grep -q "^secret/"; then
    echo "Enabling KV v2 engine at secret/..."
    vault secrets enable -path=secret kv-v2
else
    echo "KV v2 engine already enabled at secret/"
fi

# 2. Enable AppRole auth method
if ! vault auth list | grep -q "^approle/"; then
    echo "Enabling AppRole auth method..."
    vault auth enable approle
else
    echo "AppRole auth method already enabled"
fi

# 3. Create Gateway Policy
echo "Applying gateway-policy.hcl..."
vault policy write brain-gateway infrastructure/vault/policies/gateway-policy.hcl

# 4. Create AppRole for Brain Gateway
echo "Configuring AppRole: brain-gateway..."
vault write auth/approle/role/brain-gateway \
    secret_id_ttl=0 \
    token_num_uses=0 \
    token_ttl=24h \
    token_max_ttl=24h \
    policies="brain-gateway"

# 5. Enable Audit Logging to stdout
echo "Enabling audit logging to stdout..."
vault audit enable file file_path=stdout || echo "Audit logging already enabled or failed"

# 6. Fetch Role ID and Secret ID
ROLE_ID=$(vault read -field=role_id auth/approle/role/brain-gateway/role-id)
SECRET_ID=$(vault write -f -field=secret_id auth/approle/role/brain-gateway/secret-id)

echo "--- SUCCESS! ---"
echo "ROLE_ID: $ROLE_ID"
echo "SECRET_ID: $SECRET_ID"
echo ""
echo "Action required: Update Brain Gateway .env with these values."
