#!/bin/bash
# Fetch Lago RSA key from Vault and set as environment variable

set -e

# Default values if not provided
VAULT_ADDR="${VAULT_ADDR:-http://brain-vault:8200}"
VAULT_TOKEN="${VAULT_TOKEN:-staging-root-token-bizosaas-2025}"

echo "🔐 Fetching RSA key from Vault..."

# Fetch the key from Vault using curl and jq
# We assume jq is installed in the Lago container (it usually is or we can add it)
# If jq is not available, we can use a python one-liner

# Fetch the key from Vault using curl and ruby
RSA_KEY=$(curl -s \
  -H "X-Vault-Token: ${VAULT_TOKEN}" \
  "${VAULT_ADDR}/v1/secret/data/lago/rsa-key" | \
  ruby -rjson -e 'puts JSON.parse(STDIN.read)["data"]["data"]["private_key"]' 2>/dev/null)

if [ -z "$RSA_KEY" ] || [ "$RSA_KEY" = "null" ]; then
  echo "❌ Failed to fetch RSA key from Vault"
  exit 1
fi

echo "✅ RSA key fetched successfully"

# Lago expects the key to be Base64 encoded in production
# See config/initializers/rsa_keys.rb
B64_KEY=$(echo "$RSA_KEY" | base64 -w 0)

# Export for Lago to use
export LAGO_RSA_PRIVATE_KEY="$B64_KEY"

# Execute the original Lago command
exec "$@"
