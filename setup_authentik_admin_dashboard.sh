#!/bin/bash

# Authentik OAuth2 Provider Setup for Admin Dashboard
# This script configures Authentik to enable SSO for the Admin Dashboard

set -e

AUTHENTIK_URL="https://sso.bizoholic.net"
ADMIN_DASHBOARD_URL="https://admin.bizoholic.net"

echo "=== Authentik OAuth2 Provider Setup ==="
echo ""
echo "This script will configure Authentik for Admin Dashboard SSO"
echo ""

# Step 1: Get API token from user
echo "Step 1: Get API Token"
echo "---------------------"
echo "Please create an API token in Authentik:"
echo "1. Go to ${AUTHENTIK_URL}/if/admin/#/core/tokens"
echo "2. Click 'Create' button"
echo "3. Set 'User' to 'akadmin'"
echo "4. Set 'Intent' to 'API Token'"
echo "5. Copy the generated token"
echo ""
read -p "Enter your Authentik API token: " API_TOKEN
echo ""

# Step 2: Create OAuth2 Provider
echo "Step 2: Creating OAuth2 Provider..."
echo "-----------------------------------"

PROVIDER_RESPONSE=$(curl -s -X POST "${AUTHENTIK_URL}/api/v3/providers/oauth2/" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin Dashboard",
    "authorization_flow": "default-provider-authorization-implicit-consent",
    "client_type": "confidential",
    "client_id": "Mcaa10L1T1x9LC7uuhRxEzNqnyqUDbp0Nt8rIjT9",
    "client_secret": "rMFQhvLUg48taXrMR4je6Iolc0uHUM0PxhkvmAL378GaCAcxn9Qv2J3AGr3deTpdBS8LzhQhx3CgajptozFw01jmFNRwX0x3L8xx5y1yUrDJbcLJhV3cvmCPyDMk6ATQ",
    "redirect_uris": "https://admin.bizoholic.net/api/auth/callback/authentik\nhttps://admin.bizoholic.net/auth/callback/authentik",
    "signing_key": null,
    "property_mappings": []
  }')

PROVIDER_PK=$(echo "$PROVIDER_RESPONSE" | jq -r '.pk')

if [ "$PROVIDER_PK" == "null" ] || [ -z "$PROVIDER_PK" ]; then
  echo "❌ Error creating provider:"
  echo "$PROVIDER_RESPONSE" | jq '.'
  exit 1
fi

echo "✅ Provider created successfully (ID: $PROVIDER_PK)"
echo ""

# Step 3: Create Application
echo "Step 3: Creating Application..."
echo "-------------------------------"

APP_RESPONSE=$(curl -s -X POST "${AUTHENTIK_URL}/api/v3/core/applications/" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Admin Dashboard\",
    \"slug\": \"admin-dashboard\",
    \"provider\": ${PROVIDER_PK},
    \"meta_launch_url\": \"${ADMIN_DASHBOARD_URL}\",
    \"meta_description\": \"BizOSaaS Admin Dashboard\",
    \"meta_publisher\": \"BizOSaaS\",
    \"policy_engine_mode\": \"any\",
    \"open_in_new_tab\": false
  }")

APP_SLUG=$(echo "$APP_RESPONSE" | jq -r '.slug')

if [ "$APP_SLUG" == "null" ] || [ -z "$APP_SLUG" ]; then
  echo "❌ Error creating application:"
  echo "$APP_RESPONSE" | jq '.'
  exit 1
fi

echo "✅ Application created successfully (Slug: $APP_SLUG)"
echo ""

# Step 4: Summary
echo "=== Setup Complete! ==="
echo ""
echo "✅ OAuth2 Provider: Created"
echo "✅ Application: Created"
echo ""
echo "Admin Dashboard SSO Configuration:"
echo "-----------------------------------"
echo "Client ID: Mcaa10L1T1x9LC7uuhRxEzNqnyqUDbp0Nt8rIjT9"
echo "Client Secret: rMFQhvLUg48taXrMR4je6Iolc0uHUM0PxhkvmAL378GaCAcxn9Qv2J3AGr3deTpdBS8LzhQhx3CgajptozFw01jmFNRwX0x3L8xx5y1yUrDJbcLJhV3cvmCPyDMk6ATQ"
echo "Issuer: ${AUTHENTIK_URL}/application/o/bizosaas/"
echo ""
echo "Next Steps:"
echo "1. The Admin Dashboard is already configured with these credentials"
echo "2. Try logging in at: ${ADMIN_DASHBOARD_URL}"
echo "3. Use email: admin@bizoholic.net"
echo "4. Use password: Hy!HTo$Wa77O#H"
echo ""
