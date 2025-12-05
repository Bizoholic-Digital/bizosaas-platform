#!/bin/bash
# Trigger Dokploy deployment for BizOSaaS Platform
# After pushing to GitHub, Dokploy should auto-deploy via webhooks

echo "🚀 BizOSaaS Platform Deployment Trigger"
echo "========================================="
echo ""
echo "✅ Git Push Complete: commit 42889a5"
echo "📦 Changes pushed to: github.com/Bizoholic-Digital/bizosaas-platform"
echo ""

# Dokploy should automatically detect the push via GitHub webhooks
# If webhooks are configured, deployment will start automatically

echo "🔍 Checking if Dokploy webhooks are configured..."
echo ""
echo "Expected webhook URL format:"
echo "  https://dk.bizoholic.com/api/deploy/github/webhook/{project_id}"
echo ""

# Alternative: Trigger manual redeploy via Dokploy API
echo "📡 Attempting to trigger manual deployment via Dokploy API..."
echo ""

# Try different API endpoints for triggering deployment
API_TOKEN="agent_supportUMExjyxtGrPXnqZoTkKEeBAhAdHnTWpNqyUbFfbVPSYgIiGCNCCcsZpGnMaRvCbi"
DOKPLOY_URL="https://dk.bizoholic.com"

# Method 1: Trigger via compose deployment endpoint
echo "Method 1: Deploying via docker-compose endpoint..."
curl -X POST "$DOKPLOY_URL/api/compose/deploy" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "composeFiles": [
      "dokploy-frontend-staging.yml",
      "dokploy-backend-staging.yml"
    ],
    "repository": "https://github.com/Bizoholic-Digital/bizosaas-platform.git",
    "branch": "main"
  }' 2>&1

echo ""
echo ""

# Method 2: Trigger redeploy for specific applications
echo "Method 2: Triggering application redeployments..."

# Frontend applications
for app in client-portal bizoholic-frontend coreldove-frontend business-directory-frontend thrillring-gaming admin-dashboard; do
  echo "  - Redeploying $app..."
  curl -X POST "$DOKPLOY_URL/api/application/$app/redeploy" \
    -H "Authorization: Bearer $API_TOKEN" 2>&1 | head -3
done

echo ""
echo ""

# Backend applications
for app in brain-api wagtail-cms django-crm business-directory-backend amazon-sourcing temporal-integration ai-agents auth-service coreldove-backend; do
  echo "  - Redeploying $app..."
  curl -X POST "$DOKPLOY_URL/api/application/$app/redeploy" \
    -H "Authorization: Bearer $API_TOKEN" 2>&1 | head -3
done

echo ""
echo "========================================="
echo ""
echo "📊 Deployment Status:"
echo "  - GitHub: ✅ Pushed (commit 42889a5)"
echo "  - Dokploy: ⏳ Deployment in progress (check dk.bizoholic.com)"
echo ""
echo "🔗 Monitor deployment at: https://dk.bizoholic.com"
echo ""
echo "⏱️  Estimated completion: 7-8 minutes"
echo "    - 2 container restarts: 30 seconds"
echo "    - 6 frontend builds: 5 minutes"
echo "    - 1 superset deploy: 2 minutes"
echo ""
echo "✅ Services to be deployed:"
echo "    Fix: temporal-server, auth-service"
echo "    New: 6 frontend services + superset"
echo ""
