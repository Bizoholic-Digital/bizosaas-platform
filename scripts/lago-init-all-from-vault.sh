#!/bin/bash
set -e

echo "🔐 Initializing Lago environment from Vault..."

# 1. Fetch all general environment variables
# We use Ruby here because it's available in the Lago container and great for JSON
ENV_JSON=$(curl -s \
  -H "X-Vault-Token: ${VAULT_TOKEN}" \
  "${VAULT_ADDR}/v1/bizosaas/data/lago/env" | \
  ruby -rjson -e 'data = JSON.parse(STDIN.read)["data"]["data"]; data.each { |k, v| puts "#{k}=#{v}" }' 2>/dev/null)

if [ -z "$ENV_JSON" ]; then
  echo "❌ Failed to fetch environment variables from Vault"
  exit 1
fi

# Export variables
while IFS='=' read -r key value; do
  export "$key=$value"
done <<< "$ENV_JSON"

echo "✅ General environment variables loaded"

# 2. Fetch RSA Key (handled separately due to Base64 requirement)
RSA_KEY=$(curl -s \
  -H "X-Vault-Token: ${VAULT_TOKEN}" \
  "${VAULT_ADDR}/v1/bizosaas/data/lago/rsa-key" | \
  ruby -rjson -e 'puts JSON.parse(STDIN.read)["data"]["data"]["private_key"]' 2>/dev/null)

if [ -z "$RSA_KEY" ] || [ "$RSA_KEY" = "null" ]; then
  echo "❌ Failed to fetch RSA key from Vault"
  exit 1
fi

# Base64 encode for production Rails environment
B64_RSA_KEY=$(echo "$RSA_KEY" | base64 -w 0)
export LAGO_RSA_PRIVATE_KEY="$B64_RSA_KEY"

echo "✅ RSA key loaded and encoded"

# 3. Synchronize Standard Rails Vars (for maximum compatibility)
export SECRET_KEY_BASE="$LAGO_SECRET_KEY_BASE"
export DATABASE_URL="$LAGO_DATABASE_URL"
export REDIS_URL="$LAGO_REDIS_URL"

echo "🚀 Starting Lago: $@"

# Execute the original command
exec "$@"
