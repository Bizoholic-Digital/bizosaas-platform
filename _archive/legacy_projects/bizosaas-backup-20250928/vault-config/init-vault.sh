#!/bin/bash

# Wait for Vault to be ready
until vault status >/dev/null 2>&1; do
  echo "Waiting for Vault to be ready..."
  sleep 2
done

# Initialize Vault (only if not already initialized)
if ! vault status | grep -q "Sealed.*false"; then
  echo "Initializing Vault..."
  vault operator init -key-shares=1 -key-threshold=1 > /vault/data/init-keys.txt
  
  # Extract unseal key and root token
  UNSEAL_KEY=$(grep 'Unseal Key 1:' /vault/data/init-keys.txt | awk '{print $NF}')
  ROOT_TOKEN=$(grep 'Initial Root Token:' /vault/data/init-keys.txt | awk '{print $NF}')
  
  # Unseal Vault
  vault operator unseal $UNSEAL_KEY
  
  # Login with root token
  vault auth $ROOT_TOKEN
else
  echo "Vault already initialized"
  vault auth bizosaas-vault-dev-token-2025
fi

# Enable KV secrets engine
vault secrets enable -path=secret kv-v2

# Create BizOSaaS secrets
vault kv put secret/bizosaas/database \
  password="SecureBizosaas2024#Consolidated" \
  username="admin" \
  database="bizosaas" \
  host="postgres" \
  port="5432"

vault kv put secret/bizosaas/django \
  secret_key="django-secure-production-key-bizosaas-2025-vault" \
  jwt_secret="bizosaas-jwt-super-secret-key-vault-2025" \
  debug="false"

vault kv put secret/bizosaas/wagtail \
  secret_key="wagtail-secure-production-key-bizosaas-2025-vault" \
  debug="false"

vault kv put secret/bizosaas/redis \
  host="redis" \
  port="6379" \
  db="0"

vault kv put secret/bizosaas/ai-agents \
  openai_api_key="your-openai-api-key-here" \
  anthropic_api_key="your-anthropic-api-key-here"

# Create policies for different services
cat <<EOF > /tmp/brain-api-policy.hcl
path "secret/data/bizosaas/*" {
  capabilities = ["read", "list"]
}

path "secret/metadata/bizosaas/*" {
  capabilities = ["read", "list"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
EOF

cat <<EOF > /tmp/django-crm-policy.hcl
path "secret/data/bizosaas/database" {
  capabilities = ["read"]
}

path "secret/data/bizosaas/django" {
  capabilities = ["read"]
}

path "secret/data/bizosaas/redis" {
  capabilities = ["read"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
EOF

cat <<EOF > /tmp/wagtail-cms-policy.hcl
path "secret/data/bizosaas/database" {
  capabilities = ["read"]
}

path "secret/data/bizosaas/wagtail" {
  capabilities = ["read"]
}

path "secret/data/bizosaas/redis" {
  capabilities = ["read"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
EOF

# Apply policies
vault policy write brain-api-policy /tmp/brain-api-policy.hcl
vault policy write django-crm-policy /tmp/django-crm-policy.hcl
vault policy write wagtail-cms-policy /tmp/wagtail-cms-policy.hcl

# Create tokens for each service
vault token create -policy=brain-api-policy -id=bizosaas-brain-api-token-2025
vault token create -policy=django-crm-policy -id=bizosaas-django-crm-token-2025
vault token create -policy=wagtail-cms-policy -id=bizosaas-wagtail-cms-token-2025

echo "Vault initialization complete!"
echo "Services can now authenticate using their respective tokens."