# BizOSaaS Platform - Complete Testing Guide 🧪

**Version**: 1.0
**Date**: October 8, 2025
**Status**: Production-Ready Testing Guide

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start Testing](#quick-start-testing)
3. [Backend Services Testing](#backend-services-testing)
4. [Frontend Applications Testing](#frontend-applications-testing)
5. [Product Sourcing Testing](#product-sourcing-testing)
6. [BYOK Testing](#byok-testing)
7. [Admin Monitoring Testing](#admin-monitoring-testing)
8. [Integration Testing](#integration-testing)
9. [Performance Testing](#performance-testing)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **OS**: Linux/WSL2
- **Docker**: 20.10+
- **Docker Compose**: 1.29+
- **Node.js**: 18+
- **npm**: 9+
- **curl**: 7.68+
- **jq**: 1.6+ (for JSON parsing)

### Environment Setup
```bash
# Navigate to project directory
cd /home/alagiri/projects/bizoholic/bizosaas

# Verify Docker is running
docker ps

# Verify Node.js version
node --version

# Install jq if not present
sudo apt-get install jq -y
```

---

## Quick Start Testing

### 1. Check All Services Status
```bash
# Check running containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Expected: 18 containers running
# Key containers:
# - bizosaas-brain-unified (Central Hub - 8001)
# - amazon-sourcing-8085 (Product Sourcing - 8085)
# - bizosaas-vault (Vault - 8200)
# - bizosaas-admin-3009 (Admin Portal - 3009)
```

### 2. Quick Health Check
```bash
# Central Hub
curl http://localhost:8001/health

# Expected: {"status":"healthy","service":"bizosaas-brain-core","services_registered":13}

# Amazon Sourcing
curl http://localhost:8085/health

# Expected: {"status":"healthy","service":"amazon-comprehensive-sourcing","version":"2.0.0"}

# Vault
curl http://localhost:8200/v1/sys/health

# Expected: {"initialized":true,"sealed":false}
```

### 3. Quick Frontend Check
```bash
# Admin Portal
curl -s http://localhost:3009 | grep -o '<title>.*</title>'

# Expected: <title>BizOSaaS Admin - Platform Management</title>

# Client Portal
curl -s http://localhost:3006 | head -10

# Business Directory
curl -s http://localhost:3004 | head -10
```

---

## Backend Services Testing

### Test 1: Central Hub Health ✅

**Purpose**: Verify main API gateway is operational

```bash
# Test health endpoint
curl -s http://localhost:8001/health | jq '.'

# Expected Output:
{
  "status": "healthy",
  "service": "bizosaas-brain-core",
  "timestamp": "2025-10-08T...",
  "tenant_registry": "active",
  "services_registered": 13
}
```

**Success Criteria**:
- ✅ Status is "healthy"
- ✅ Services registered = 13
- ✅ Tenant registry is "active"

### Test 2: Registered Services ✅

**Purpose**: Verify all backend services are registered

```bash
# List registered services
curl -s http://localhost:8001/api/brain/registered-services | jq '.services | length'

# Expected: 13
```

**Success Criteria**:
- ✅ Returns 13 registered services

### Test 3: Amazon Sourcing Service ✅

**Purpose**: Verify product sourcing API is functional

```bash
# Health check
curl -s http://localhost:8085/health | jq '.'

# Expected:
{
  "status": "healthy",
  "service": "amazon-comprehensive-sourcing",
  "version": "2.0.0",
  "components": {
    "paapi": "Product Advertising API for sourcing",
    "spapi": "Selling Partner API for listing",
    "saleor": "E-commerce platform integration",
    "ai_enhancement": "AI-powered product enhancement"
  }
}
```

**Success Criteria**:
- ✅ Status is "healthy"
- ✅ Version is "2.0.0"
- ✅ All 4 components listed

### Test 4: Vault Service ✅

**Purpose**: Verify secure secrets storage

```bash
# Check Vault status
curl -s http://localhost:8200/v1/sys/health | jq '.'

# Expected:
{
  "initialized": true,
  "sealed": false,
  "standby": false,
  "version": "1.15.6"
}
```

**Success Criteria**:
- ✅ initialized = true
- ✅ sealed = false
- ✅ Version displayed

### Test 5: Database Services ✅

**Purpose**: Verify PostgreSQL and Redis are running

```bash
# Check PostgreSQL container
docker exec bizosaas-postgres-unified pg_isready

# Expected: /var/run/postgresql:5432 - accepting connections

# Check Redis
docker exec bizosaas-redis-unified redis-cli ping

# Expected: PONG
```

**Success Criteria**:
- ✅ PostgreSQL accepting connections
- ✅ Redis responds with PONG

### Test 6: Wagtail CMS ✅

**Purpose**: Verify content management system

```bash
# Check Wagtail health
curl -s http://localhost:8002/health 2>&1 | head -20

# Container should be healthy
docker ps --filter "name=wagtail" --format "{{.Status}}"

# Expected: Up X hours (healthy)
```

### Test 7: Django CRM ✅

**Purpose**: Verify CRM service

```bash
# Check Django CRM
docker ps --filter "name=django-crm" --format "{{.Status}}"

# Expected: Up X hours (healthy)
```

### Test 8: Saleor E-commerce ✅

**Purpose**: Verify e-commerce engine

```bash
# Check Saleor
docker ps --filter "name=saleor" --format "{{.Status}}"

# Expected: Up X hours
```

---

## Frontend Applications Testing

### Test 1: Admin Dashboard ✅

**URL**: http://localhost:3009

**Manual Test Steps**:
1. Open browser to http://localhost:3009
2. Verify page loads with title "BizOSaaS Admin - Platform Management"
3. Check sidebar navigation is visible
4. Verify main dashboard metrics are displayed
5. Check service health monitor is visible

**Expected Results**:
- ✅ Page loads successfully
- ✅ Navigation menu visible
- ✅ Dashboard cards showing metrics
- ✅ Service health monitor displaying real-time status

**CLI Test**:
```bash
# Verify accessibility
curl -s http://localhost:3009 | grep -o '<title>.*</title>'

# Expected: <title>BizOSaaS Admin - Platform Management</title>
```

### Test 2: Admin Service Monitoring ✅

**URL**: http://localhost:3009/dashboard

**Manual Test Steps**:
1. Navigate to http://localhost:3009/dashboard
2. Scroll to "Service Health Status" section
3. Verify 9 services are listed
4. Check status indicators (green = healthy, red = unhealthy)
5. Verify response times are displayed
6. Click "Refresh" button
7. Observe auto-refresh countdown

**Expected Services**:
1. Central Hub (8001) - ✅ Healthy
2. Amazon Sourcing (8085) - ✅ Healthy
3. Vault (8200) - ✅ Healthy
4. Wagtail CMS (8006)
5. Django CRM (8003)
6. Saleor API (8000)
7. AI Agents (8010)
8. Auth Service (8007)
9. Business Directory (9002)

### Test 3: Client Portal ✅

**URL**: http://localhost:3006

**Manual Test Steps**:
1. Open browser to http://localhost:3006
2. Verify tenant portal loads
3. Check multi-tenant dashboard
4. Verify navigation works

**CLI Test**:
```bash
curl -s http://localhost:3006 | head -20
```

### Test 4: Business Directory ✅

**URL**: http://localhost:3004

**Manual Test Steps**:
1. Open browser to http://localhost:3004
2. Verify directory interface loads
3. Check business listings

### Test 5: Bizoholic Frontend ✅

**URL**: http://localhost:3008

**Manual Test Steps**:
1. Open browser to http://localhost:3008
2. Verify marketing website loads
3. Check contact form
4. Verify CRM integration

---

## Product Sourcing Testing

### Test 1: Basic Product Search ✅

**Purpose**: Verify product sourcing API works

```bash
# Search for yoga mat
curl -s -X POST http://localhost:8085/sourcing/search \
  -H "Content-Type: application/json" \
  -d '{"query": "yoga mat", "limit": 2}' | jq '.'

# Expected: Array of 2 products with complete details
```

**Expected Output**:
```json
[
  {
    "asin": "B0DX1QJFK4",
    "title": "Boldfit Yoga Mats For Women...",
    "price": "379.0",
    "currency": "INR",
    "image_url": "https://m.media-amazon.com/images/...",
    "product_url": "https://www.amazon.in/dp/B0DX1QJFK4",
    "category": "fitness",
    "brand": "Boldfit",
    "rating": 3.9,
    "review_count": 484,
    "availability": "In Stock"
  }
]
```

**Success Criteria**:
- ✅ Returns 2 products
- ✅ Each product has title, price, image
- ✅ ASIN is valid
- ✅ Rating and reviews present

### Test 2: ASIN Validation ✅

**Purpose**: Verify product validation works

```bash
# Validate ASIN
curl -s http://localhost:8085/validation/asin/B0DX1QJFK4 | jq '.'

# Expected: Validation result with eligibility score
```

**Expected Output**:
```json
{
  "asin": "B0DX1QJFK4",
  "marketplace": "amazon.in",
  "validation": {
    "asin": "B0DX1QJFK4",
    "valid": true,
    "available": false,
    "url": "https://www.amazon.in/dp/B0DX1QJFK4"
  },
  "dropship_eligibility": {
    "eligible": false,
    "score": 0,
    "max_score": 6
  }
}
```

**Success Criteria**:
- ✅ ASIN validation returns result
- ✅ Valid field is boolean
- ✅ Dropship eligibility calculated

### Test 3: Category Filtering ✅

```bash
# Search with category filter
curl -s -X POST http://localhost:8085/sourcing/search \
  -H "Content-Type: application/json" \
  -d '{"query": "resistance bands", "category": "fitness", "limit": 3}' | jq 'length'

# Expected: 3
```

### Test 4: CorelDove Integration ✅

**Purpose**: Test frontend to backend integration

**Manual Test Steps**:
1. Open CorelDove frontend (port 3002 or 3007)
2. Navigate to "Source Products" section
3. Enter search term: "yoga mat"
4. Click search
5. Verify products display with images
6. Check "Add to Catalog" button is present
7. Verify "View on Amazon" link works

**CLI Test**:
```bash
# Test CorelDove API route
curl -s 'http://localhost:3002/api/sourcing?query=yoga%20mat&limit=2' | jq '.'

# OR (depending on running instance)
curl -s 'http://localhost:3007/api/sourcing?query=yoga%20mat&limit=2' | jq '.'
```

---

## BYOK Testing

### Test 1: Verify Components Exist ✅

```bash
# Check BYOK components
ls -la /home/alagiri/projects/bizoholic/bizosaas/frontend/apps/client-portal/components/byok/

# Expected: BYOKApiKeyManager.tsx

ls -la /home/alagiri/projects/bizoholic/bizosaas/frontend/apps/client-portal/components/wizard/

# Expected: BYOKSetup.tsx (if exists)
```

### Test 2: Verify API Routes ✅

```bash
# Check API routes exist
ls -la /home/alagiri/projects/bizoholic/bizosaas/frontend/apps/client-portal/app/api/brain/tenant/api-keys/

# Expected:
# - route.ts (GET/POST)
# - [keyId]/ directory with route.ts (DELETE/ROTATE)
```

### Test 3: Vault Configuration ✅

```bash
# Check Vault secrets engine
docker exec bizosaas-vault vault secrets list 2>/dev/null

# Expected: Shows configured secret engines including bizosaas/
```

### Test 4: Manual BYOK UI Testing ✅

**URL**: http://localhost:3006/settings (or wherever Settings page is)

**Manual Test Steps**:
1. Navigate to Settings page
2. Click "API Keys" tab
3. Click "Add API Key" button
4. Verify provider selection grid shows 9 providers:
   - OpenAI
   - Anthropic Claude
   - Azure OpenAI
   - Cohere
   - Mistral AI
   - DeepSeek
   - Google Gemini
   - OpenRouter
   - HuggingFace
5. Select a provider (e.g., OpenAI)
6. Enter key name: "Test Key"
7. Enter API key value
8. Click "Add API Key"
9. Verify success message
10. Check key appears in list (masked)
11. Click eye icon to unmask key
12. Click delete icon to remove key

**Success Criteria**:
- ✅ All 9 providers displayed
- ✅ Can add API key
- ✅ Key is masked by default
- ✅ Can unmask key
- ✅ Can delete key

---

## Admin Monitoring Testing

### Test 1: Access Monitoring Dashboard ✅

**URL**: http://localhost:3009/dashboard

```bash
# Verify dashboard is accessible
curl -s http://localhost:3009/dashboard | grep -o "Service Health"

# Expected: "Service Health" found in HTML
```

### Test 2: Service Health Monitor ✅

**Manual Test Steps**:
1. Open http://localhost:3009/dashboard
2. Scroll to "Service Health Status" section
3. Verify summary cards show:
   - Total Services (9)
   - Healthy count
   - Issues count
4. Check service list displays all 9 services
5. Verify status badges (Healthy/Unhealthy/Checking)
6. Check response times are shown (in milliseconds)
7. Wait 30 seconds and verify auto-refresh occurs
8. Click "Refresh" button manually

**Expected Behavior**:
- ✅ All 9 services listed
- ✅ Status indicators visible (green/red/blue)
- ✅ Response times displayed
- ✅ Auto-refresh every 30 seconds
- ✅ Manual refresh works

### Test 3: Service Status Indicators ✅

**Check each service**:
1. Central Hub - Should show green (Healthy)
2. Amazon Sourcing - Should show green (Healthy)
3. Vault - Should show green (Healthy)
4. Others - Status depends on actual health

**If service is unhealthy**:
- Badge should be red
- Error message should display
- Response time may be higher or show timeout

---

## Integration Testing

### Test 1: End-to-End Product Flow ✅

**Purpose**: Test complete product sourcing to catalog flow

**Steps**:
1. Search for product via API
2. Retrieve product details
3. Transform to Saleor format
4. Display in frontend
5. Add to catalog

```bash
# Step 1: Search
PRODUCT=$(curl -s -X POST http://localhost:8085/sourcing/search \
  -H "Content-Type: application/json" \
  -d '{"query": "yoga mat", "limit": 1}')

# Step 2: Extract ASIN
ASIN=$(echo $PRODUCT | jq -r '.[0].asin')
echo "ASIN: $ASIN"

# Step 3: Validate ASIN
curl -s http://localhost:8085/validation/asin/$ASIN | jq '.validation.valid'

# Expected: true
```

### Test 2: Multi-Tenant Flow ✅

**Purpose**: Test tenant isolation

```bash
# Test with different tenant IDs
curl -s http://localhost:3006/api/brain/tenant/api-keys \
  -H "X-Tenant-ID: tenant-001" | jq '.'

curl -s http://localhost:3006/api/brain/tenant/api-keys \
  -H "X-Tenant-ID: tenant-002" | jq '.'

# Each should return isolated data
```

### Test 3: CRM Integration ✅

**Purpose**: Test contact form to CRM flow

**Manual Steps**:
1. Navigate to Bizoholic frontend (port 3008 or 3000)
2. Fill out contact form:
   - Name: "Test User"
   - Email: "test@example.com"
   - Company: "Test Corp"
   - Message: "Testing CRM integration"
3. Submit form
4. Verify success message
5. Check Django CRM for new lead

---

## Performance Testing

### Test 1: API Response Times ✅

```bash
# Test Central Hub response time
time curl -s http://localhost:8001/health > /dev/null

# Expected: < 500ms

# Test Amazon Sourcing response time
time curl -s http://localhost:8085/health > /dev/null

# Expected: < 500ms
```

### Test 2: Product Search Performance ✅

```bash
# Measure search time
time curl -s -X POST http://localhost:8085/sourcing/search \
  -H "Content-Type: application/json" \
  -d '{"query": "yoga mat", "limit": 5}' > /dev/null

# Expected: < 3 seconds
```

### Test 3: Concurrent Requests ✅

```bash
# Test 10 concurrent health checks
for i in {1..10}; do
  curl -s http://localhost:8001/health &
done
wait

# All should complete successfully
```

---

## Troubleshooting

### Issue 1: Container Not Running

**Symptom**: Service not accessible

**Solution**:
```bash
# Check container status
docker ps -a --filter "name=bizosaas"

# Restart container
docker restart <container-name>

# Check logs
docker logs <container-name> --tail 50
```

### Issue 2: Port Already in Use

**Symptom**: Cannot start service on port

**Solution**:
```bash
# Find process using port
sudo lsof -i :8001

# Kill process
sudo kill -9 <PID>
```

### Issue 3: Frontend Permission Errors

**Symptom**: `.next` permission denied

**Solution**:
```bash
# Fix ownership
cd /path/to/frontend
sudo chown -R $USER:$USER .next

# Or clean and rebuild
rm -rf .next
npm run build
```

### Issue 4: Vault Sealed

**Symptom**: Vault shows `"sealed":true`

**Solution**:
```bash
# Check seal status
curl http://localhost:8200/v1/sys/health | jq '.sealed'

# If true, check container logs
docker logs bizosaas-vault
```

### Issue 5: Service 503 Error

**Symptom**: Service returns 503

**Solution**:
```bash
# Check if service is registered
curl http://localhost:8001/api/brain/registered-services | jq '.services'

# Restart Central Hub
docker restart bizosaas-brain-unified
```

---

## Test Checklist Summary

### Backend Services (13 tests)
- [ ] Central Hub health check
- [ ] Amazon Sourcing health check
- [ ] Vault status check
- [ ] PostgreSQL connection
- [ ] Redis connection
- [ ] Wagtail CMS health
- [ ] Django CRM health
- [ ] Saleor status
- [ ] AI Agents status
- [ ] Business Directory status
- [ ] Temporal services
- [ ] All containers running
- [ ] All services registered

### Frontend Applications (5 tests)
- [ ] Admin Dashboard accessible
- [ ] Service monitoring visible
- [ ] Client Portal accessible
- [ ] Business Directory accessible
- [ ] Bizoholic Frontend accessible

### Product Sourcing (4 tests)
- [ ] Basic product search works
- [ ] ASIN validation works
- [ ] Category filtering works
- [ ] CorelDove integration works

### BYOK (4 tests)
- [ ] Components exist
- [ ] API routes present
- [ ] Vault configured
- [ ] UI functional

### Admin Monitoring (3 tests)
- [ ] Dashboard accessible
- [ ] Service monitor visible
- [ ] Auto-refresh working

### Integration (3 tests)
- [ ] End-to-end product flow
- [ ] Multi-tenant isolation
- [ ] CRM integration

### Performance (3 tests)
- [ ] API response < 500ms
- [ ] Product search < 3s
- [ ] Concurrent requests work

**Total Tests**: 35

---

## Automated Test Script

Save as `test-platform.sh`:

```bash
#!/bin/bash

echo "=== BizOSaaS Platform Test Suite ==="
echo ""

# Backend Services
echo "1. Testing Central Hub..."
curl -s http://localhost:8001/health | jq -r '.status' | grep -q "healthy" && echo "✅ PASS" || echo "❌ FAIL"

echo "2. Testing Amazon Sourcing..."
curl -s http://localhost:8085/health | jq -r '.status' | grep -q "healthy" && echo "✅ PASS" || echo "❌ FAIL"

echo "3. Testing Vault..."
curl -s http://localhost:8200/v1/sys/health | jq -r '.initialized' | grep -q "true" && echo "✅ PASS" || echo "❌ FAIL"

echo "4. Testing Product Search..."
curl -s -X POST http://localhost:8085/sourcing/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "limit": 1}' | jq -r '.[0].asin' | grep -q "B0" && echo "✅ PASS" || echo "❌ FAIL"

echo "5. Testing Admin Portal..."
curl -s http://localhost:3009 | grep -q "BizOSaaS Admin" && echo "✅ PASS" || echo "❌ FAIL"

echo ""
echo "=== Test Suite Complete ==="
```

**Run tests**:
```bash
chmod +x test-platform.sh
./test-platform.sh
```

---

## Next Steps After Testing

1. ✅ All tests passing → **Ready for production**
2. ⚠️ Some tests failing → **Review troubleshooting section**
3. 📊 Performance issues → **Check resource allocation**
4. 🔧 Integration issues → **Verify service connections**

---

**Testing Guide Version**: 1.0
**Last Updated**: October 8, 2025
**Platform Version**: Production-Ready

🎉 **Happy Testing!** 🎉
