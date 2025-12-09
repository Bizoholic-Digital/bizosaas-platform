#!/bin/bash
# Test API Gateway routing

echo "🧪 Testing API Gateway Routing..."
echo "================================="

# Test 1: Gateway Health
echo -e "\n1️⃣  Testing Gateway Health..."
curl -s https://api.bizoholic.com/health | jq '.' || echo "❌ Gateway health check failed"

# Test 2: List Routes
echo -e "\n2️⃣  Listing Gateway Routes..."
curl -s https://api.bizoholic.com/gateway/routes | jq '.' || echo "❌ Routes listing failed"

# Test 3: Auth Service
echo -e "\n3️⃣  Testing Auth Service..."
curl -s https://api.bizoholic.com/auth/health | jq '.' || echo "⚠️  Auth service may not have health endpoint"

# Test 4: CRM Service
echo -e "\n4️⃣  Testing CRM Service..."
curl -s https://api.bizoholic.com/crm/health | jq '.' || echo "⚠️  CRM service may not have health endpoint"

# Test 5: CMS Service
echo -e "\n5️⃣  Testing CMS Service..."
curl -s https://api.bizoholic.com/cms/health | jq '.' || echo "⚠️  CMS service may not have health endpoint"

# Test 6: Directory Service
echo -e "\n6️⃣  Testing Directory Service..."
curl -s https://api.bizoholic.com/directory/health | jq '.' || echo "⚠️  Directory service may not have health endpoint"

# Test 7: AI Service
echo -e "\n7️⃣  Testing AI Service..."
curl -s https://api.bizoholic.com/ai/health | jq '.' || echo "⚠️  AI service may not have health endpoint"

# Test 8: Trading Service
echo -e "\n8️⃣  Testing Trading Service..."
curl -s https://api.bizoholic.com/trading/health | jq '.' || echo "⚠️  Trading service may not have health endpoint"

# Test 9: Sourcing Service
echo -e "\n9️⃣  Testing Sourcing Service..."
curl -s https://api.bizoholic.com/sourcing/health | jq '.' || echo "⚠️  Sourcing service may not have health endpoint"

# Test 10: CoreLDove API
echo -e "\n🔟 Testing CoreLDove GraphQL..."
curl -s https://api.coreldove.com/graphql -X POST -H "Content-Type: application/json" -d '{"query":"{__schema{types{name}}}"}' | jq '.data.__schema.types | length' || echo "⚠️  GraphQL introspection failed"

echo -e "\n================================="
echo "✅ API Gateway tests complete!"
