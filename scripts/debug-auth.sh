#!/bin/bash
# Debug Auth Service

AUTH_URL="http://127.0.0.1:8007"
EMAIL="admin@bizoholic.com"
PASSWORD="AdminDemo2024!"

echo "1. Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "$AUTH_URL/auth/sso/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\", \"platform\": \"bizoholic\"}")

echo "Response: $LOGIN_RESPONSE"

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Login failed. No token received."
    exit 1
fi

echo ""
echo "2. Token received: ${TOKEN:0:20}..."

echo ""
echo "3. Verifying token with /auth/me..."
ME_RESPONSE=$(curl -s -X GET "$AUTH_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN")

echo "Response: $ME_RESPONSE"

if [[ "$ME_RESPONSE" == *"Unauthorized"* ]] || [[ "$ME_RESPONSE" == *"401"* ]]; then
    echo "❌ Token rejected!"
else
    echo "✅ Token accepted!"
fi
