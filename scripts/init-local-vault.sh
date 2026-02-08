#!/bin/bash

# Configuration
VAULT_CONTAINER="brain-vault"
VAULT_TOKEN="root" # Default dev token from docker-compose

echo "🚀 Waiting for Vault container to be ready..."
until [ "$(docker inspect -f '{{.State.Running}}' $VAULT_CONTAINER 2>/dev/null)" == "true" ]; do
    sleep 2
done

echo "✅ Vault container is running."

# Check if Vault is initialized (in dev mode it usually is)
echo "🔧 Enabling KV-v2 engine at 'secret' path..."
docker exec $VAULT_CONTAINER vault secrets enable -path=secret kv-v2 2>/dev/null || echo "⚠️ Secret path might already exist."

echo "🔧 Creating 'bizosaas' mount point if needed..."
docker exec $VAULT_CONTAINER vault secrets enable -path=bizosaas kv-v2 2>/dev/null || echo "⚠️ bizosaas path might already exist."

echo "🔑 Vault is ready for local development/staging."
echo "Config:"
echo "VAULT_ADDR: http://vault:8200"
echo "VAULT_TOKEN: $VAULT_TOKEN"
