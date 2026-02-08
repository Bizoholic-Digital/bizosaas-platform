#!/bin/bash
API_KEY="mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
DOKPLOY_URL="https://dk.bizoholic.com"
PROJECT_ID="WfVYVHpPQh_h5s4GpyDdW" # portals project
ENV_ID="j5ifoftZ7sMPQCpcSUBE3"

# 1. Create Compose
echo "Creating Admin Portal..."
CREATE_RES=$(curl -s -X POST "$DOKPLOY_URL/api/compose.create" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "'"$PROJECT_ID"'",
    "name": "admin-portal-fixed",
    "description": "Admin Dashboard",
    "composeType": "docker-compose",
    "environmentId": "'"$ENV_ID"'"
  }')

COMPOSE_ID=$(echo "$CREATE_RES" | jq -r '.composeId')
echo "Created Compose ID: $COMPOSE_ID"

if [ "$COMPOSE_ID" == "null" ]; then
    echo "Failed to create compose"
    echo "$CREATE_RES"
    exit 1
fi

# 2. Update Configuration (GitHub Source)
echo "Updating configuration..."
curl -s -X POST "$DOKPLOY_URL/api/compose.update" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "composeId": "'"$COMPOSE_ID"'",
    "composePath": "docker-compose.admin-portal.yml",
    "sourceType": "github",
    "githubId": "QZnupLM5a8IgYpTloLpdZ",
    "owner": "Bizoholic-Digital",
    "repository": "bizosaas-platform",
    "branch": "staging",
    "autoDeploy": true,
    "env": "NEXT_PUBLIC_API_URL=https://api.bizoholic.net\nAPI_URL=https://api.bizoholic.net\nAUTH_AUTHENTIK_ID=bizosaas-portal\nNEXT_PUBLIC_AUTH_AUTHENTIK_ID=bizosaas-portal\nAUTH_AUTHENTIK_SECRET=BizOSaaS2024!AuthentikSecret\nAUTH_AUTHENTIK_ISSUER=https://auth-sso.bizoholic.net/application/o/bizosaas-platform/\nNEXTAUTH_URL=https://admin.bizoholic.net\nAUTH_URL=https://admin.bizoholic.net\nNEXTAUTH_SECRET=BizOSaaS2025!Secret!NextAuth\nAUTH_SECRET=BizOSaaS2025!Secret!NextAuth\nAUTH_TRUST_HOST=true\nAUTH_SUCCESS_URL=https://admin.bizoholic.net/dashboard\nNODE_ENV=production\nNEXT_PUBLIC_APP_URL=https://admin.bizoholic.net\nPORT=3004"
  }' | jq '.'

# 3. Deploy
echo "Deploying..."
curl -s -X POST "$DOKPLOY_URL/api/compose.deploy" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "composeId": "'"$COMPOSE_ID"'"
  }' | jq '.'
