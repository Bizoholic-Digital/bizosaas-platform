#!/bin/bash
# Update frontend compose with inline content

API_KEY="bizoholicKRGZxqgQXBDBzumvvnMhiEZLmnetMTAWwTnFztwuGofadbHagGbJiiMZTqczBDKY"
COMPOSE_ID="hU2yhYOqv3_ftKGGvcAiv"

# Read compose file
COMPOSE_CONTENT=$(cat dokploy-frontend-staging-local.yml)

# Create JSON payload
PAYLOAD=$(jq -n \
  --arg id "$COMPOSE_ID" \
  --arg content "$COMPOSE_CONTENT" \
  '{
    composeId: $id,
    composeFile: $content,
    sourceType: "raw"
  }')

# Update via API
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  https://dk.bizoholic.com/api/compose.update \
  -d "$PAYLOAD" | python3 -m json.tool | head -20

echo ""
echo "✅ Compose file updated to use inline content"
