#!/bin/bash
# Sync Traefik labels from Dokploy database to Docker Swarm service
# This script ensures labels persist across Dokploy redeployments
#
# Usage:
#   Run this script after every Dokploy deployment
#   Or set up as a cron job: */5 * * * * /path/to/sync-traefik-labels.sh

set -e

# Configuration
POSTGRES_CONTAINER="dokploy-postgres.1.atiqv1xxe7p5r54iktb58szxn"
DB_NAME="dokploy"
DB_USER="dokploy"
APPLICATION_ID="3uYBtxpH1Qc7H8uTfmOfy"
SERVICE_NAME="backend-brain-gateway"

echo "🔄 Syncing Traefik labels from Dokploy database to Docker service..."

# Read labels from Dokploy database
LABELS_JSON=$(docker exec "$POSTGRES_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -t -c \
  "SELECT \"labelsSwarm\" FROM application WHERE \"applicationId\" = '$APPLICATION_ID';" | tr -d '[:space:]')

if [ -z "$LABELS_JSON" ] || [ "$LABELS_JSON" = "null" ]; then
  echo "⚠️  No labels found in database. Skipping..."
  exit 0
fi

echo "📋 Found labels in database"

# Parse JSON and build docker service update command
UPDATE_CMD="docker service update"

# Extract each label from JSON and add to command
for key in $(echo "$LABELS_JSON" | jq -r 'keys[]' 2>/dev/null); do
  value=$(echo "$LABELS_JSON" | jq -r ".[\"$key\"]" 2>/dev/null)
  UPDATE_CMD="$UPDATE_CMD --label-add '$key=$value'"
done

UPDATE_CMD="$UPDATE_CMD $SERVICE_NAME"

# Get current service labels
CURRENT_LABELS=$(docker service inspect "$SERVICE_NAME" --format '{{json .Spec.Labels}}' 2>/dev/null || echo "{}")

# Compare with database labels
if [ "$CURRENT_LABELS" = "$LABELS_JSON" ]; then
  echo "✅ Labels already in sync. No update needed."
  exit 0
fi

echo "🔧 Applying labels to service..."

# Apply labels one by one
echo "$LABELS_JSON" | jq -r 'to_entries[] | "\(.key)=\(.value)"' | while read -r label; do
  docker service update --label-add "$label" "$SERVICE_NAME" > /dev/null 2>&1
done

echo "✅ Traefik labels synced successfully!"

# Verify
echo ""
echo "🔍 Current service labels:"
docker service inspect "$SERVICE_NAME" --format '{{json .Spec.Labels}}' | jq .
