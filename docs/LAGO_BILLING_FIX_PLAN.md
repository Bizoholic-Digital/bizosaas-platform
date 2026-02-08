# Lago Billing Implementation - Complete Fix Plan
**Date**: 2026-01-13
**Status**: CRITICAL - Services Down

---

## 🔍 Current State Analysis

### 1. **Lago Services Status**
- ✅ **Docker Compose Configuration**: Properly configured in `docker-compose.lago.yml`
- ⚠️ **Services Stopped**: All Lago containers stopped to resolve previous restart loop
- ❌ **RSA Key Issue**: Hardcoded RSA keys causing boot failures
- ❌ **Not Deployed**: Services not running on KVM8 VPS (72.60.98.213)

### 2. **Configuration Files**
```
✅ docker-compose.lago.yml      - Complete, all services defined
✅ .env.lago                    - Generated with proper keys
✅ .env.lago.clean              - Backup configuration
⚠️  scripts/deploy-lago-kvm8.sh - Deployment script (needs verification)
⚠️  scripts/setup-lago-local.sh - Local setup script
```

### 3. **Lago Stack Components**
| Service | Image | Role | Status | Domain |
|---------|-------|------|--------|--------|
| `lago-db` | postgres:14-alpine | Database | ❌ Stopped | Internal |
| `lago-redis` | redis:7-alpine | Cache/Queue | ❌ Stopped | Internal |
| `lago-migrate` | getlago/api:v1.16.0 | Migrations | ❌ Not Run | Internal |
| `lago-api` | getlago/api:v1.16.0 | REST API | ❌ Stopped | `billing-api.bizoholic.net` |
| `lago-worker` | getlago/api:v1.16.0 | Background Jobs | ❌ Stopped | Internal |
| `lago-front` | getlago/front:v1.16.0 | Web UI | ❌ Stopped | `billing.bizoholic.net` |

### 4. **Integration Points**
✅ **Brain Gateway Integration**:
- `app/connectors/lago.py` - Lago connector implementation
- `app/services/billing_service.py` - Billing service using Lago
- `app/seeds/connectors.py` - Default connector configuration
- `app/ports/billing_port.py` - Billing abstraction layer

✅ **API Endpoints**: Brain Gateway exposes:
- `/api/billing/plans` - List subscription plans
- `/api/billing/subscribe` - Create subscription
- `/api/billing/subscriptions` - List customer subscriptions
- `/api/billing/invoices` - Customer invoices
- `/api/billing/usage` - Usage tracking

---

## 🐛 Critical Issues Identified

### Issue #1: **RSA Key Injection Failure**
**Problem**: Hardcoded RSA private key in docker-compose causing services to fail at boot.

**Evidence**:
- Lines 47-74, 96-123, 156-183 in `docker-compose.lago.yml` contain inline RSA key export
- This approach is fragile and causes shell escaping issues
- Previous session logs showed restart loops due to this

**Impact**: Services cannot start → No billing functionality

---

### Issue #2: **Missing .env.lago on Server**
**Problem**: Environment file not deployed to production server.

**Impact**: Even if containers start, they won't have proper configuration

---

### Issue #3: **Network Configuration**
**Problem**: Lago services need to be accessible from:
- Brain Gateway (internal via `brain-network`)
- Public internet (via Traefik on `dokploy-network`)

**Current State**: Both networks configured but services stopped

---

### Issue #4: **No Health Monitoring**
**Problem**: No verification that Lago API is responding after deployment

**Impact**: Silent failures possible

---

## 🎯 Comprehensive Fix Plan

### **Phase 1: Fix RSA Key Handling** (Priority: CRITICAL)

**Option A: Use Docker Secrets** ✅ RECOMMENDED
```yaml
# Create secret file approach
secrets:
  lago_rsa_key:
    file: ./lago_rsa.pem

services:
  lago-api:
    secrets:
      - lago_rsa_key
    environment:
      - LAGO_RSA_PRIVATE_KEY_FILE=/run/secrets/lago_rsa_key
```

**Option B: Base64 Encode in .env** ⚠️ SIMPLER BUT LESS SECURE
```bash
# In .env.lago
LAGO_RSA_PRIVATE_KEY_BASE64=<base64-encoded-key>

# In docker-compose command
command: |
  export LAGO_RSA_PRIVATE_KEY=$(echo $LAGO_RSA_PRIVATE_KEY_BASE64 | base64 -d)
  ./scripts/start.api.sh
```

**Option C: Mount as Volume** ✅ CLEAN SOLUTION
```yaml
volumes:
  - ./lago_rsa_private.pem:/app/config/lago_rsa_private.pem:ro
environment:
  - LAGO_RSA_PRIVATE_KEY_PATH=/app/config/lago_rsa_private.pem
```

**Recommendation**: Use Option C (Volume Mount) for production stability.

---

### **Phase 2: Deployment & Service Startup**

#### Step 2.1: Create RSA Key File
```bash
# Extract from .env.lago
cat > lago_rsa_private.pem << 'EOF'
<key from .env.lago>
EOF
chmod 600 lago_rsa_private.pem
```

#### Step 2.2: Update docker-compose.lago.yml
**Changes Required**:
1. Remove inline RSA export from all `command` sections
2. Add volume mount for RSA key
3. Update environment variables
4. Ensure proper dependency chain

#### Step 2.3: Deploy to Server
```bash
# 1. Copy files to server
scp docker-compose.lago.yml root@72.60.98.213:/root/lago/
scp .env.lago root@72.60.98.213:/root/lago/
scp lago_rsa_private.pem root@72.60.98.213:/root/lago/

# 2. SSH and deploy
ssh root@72.60.98.213
cd /root/lago
docker compose -f docker-compose.lago.yml up -d
```

#### Step 2.4: Verify Services
```bash
# Check all containers running
docker ps | grep lago

# Check logs
docker logs lago-api --tail 50
docker logs lago-worker --tail 50
docker logs lago-front --tail 20

# Test API health
curl http://localhost:3010/api/v1/health
```

---

### **Phase 3: Traefik & DNS Configuration**

#### Step 3.1: Verify Traefik Labels
Current configuration in docker-compose.lago.yml looks correct:
- `lago-api` → `billing-api.bizoholic.net`
- `lago-front` → `billing.bizoholic.net`

#### Step 3.2: DNS Verification
```bash
# Ensure DNS A records exist:
billing-api.bizoholic.net → 72.60.98.213
billing.bizoholic.net → 72.60.98.213
```

#### Step 3.3: SSL Certificate Generation
Traefik should auto-generate Let's Encrypt certificates. Verify:
```bash
docker logs traefik 2>&1 | grep lago
```

---

### **Phase 4: Brain Gateway Integration**

#### Step 4.1: Update Connector Configuration
File: `bizosaas-brain-core/brain-gateway/app/seeds/connectors.py`

Current config (line 62-65):
```python
active_connectors["default_tenant:lago"] = {
    "connector_id": "lago",
    "credentials": {
        "api_url": "http://lago-api:3000",  # ⚠️ Update if using Traefik
        # Missing API key!
    }
}
```

**Required Changes**:
1. Add API key to connector configuration
2. Decide: Internal URL (`http://lago-api:3000`) vs External (`https://billing-api.bizoholic.net`)

**Recommendation**: Use internal URL for better performance and security.

#### Step 4.2: Generate Lago API Key
```bash
# SSH to server
docker exec -it lago-api rake lago:generate_api_key
# Copy the generated API key
```

#### Step 4.3: Configure in Brain Gateway
Update `.env` or environment variables for brain-gateway:
```env
LAGO_API_URL=http://lago-api:3000
LAGO_API_KEY=<generated-api-key>
```

---

### **Phase 5: Testing & Validation**

#### Test 5.1: Direct Lago API Test
```bash
# Get organization (should return 200)
curl -H "Authorization: Bearer <API_KEY>" \
  http://lago-api:3000/api/v1/organizations

# List plans
curl -H "Authorization: Bearer <API_KEY>" \
  http://lago-api:3000/api/v1/plans
```

#### Test 5.2: Brain Gateway Billing Endpoints
```bash
# List plans via Brain Gateway
curl https://api.bizoholic.net/api/billing/plans

# Create a subscription (requires auth)
curl -X POST https://api.bizoholic.net/api/billing/subscribe \
  -H "Authorization: Bearer <user-token>" \
  -d '{"plan_code": "startup", "customer_id": "test-tenant"}'
```

#### Test 5.3: Web UI Access
- Navigate to `https://billing.bizoholic.net`
- Login with admin credentials
- Verify dashboard loads

---

### **Phase 6: Data Seeding**

#### Step 6.1: Create Default Plans
```bash
# Use Lago CLI or API to create billing plans
docker exec -it lago-api rails console

# In Rails console:
Plan.create!(
  name: "Starter",
  code: "starter",
  amount_cents: 4900,
  amount_currency: "USD",
  interval: "monthly"
)
```

**Recommended Plans**:
1. **Free Tier**: $0/month (100 AI requests)
2. **Starter**: $49/month (1,000 AI requests)
3. **Growth**: $199/month (10,000 AI requests)
4. **Scale**: $499/month (50,000 AI requests)
5. **Enterprise**: Custom pricing

#### Step 6.2: Seed via Brain Gateway
Alternative: Use Brain Gateway's billing service to programmatically create plans.

---

## 📋 Step-by-Step Execution Checklist

### Pre-Deployment
- [ ] Backup current `.env.lago`
- [ ] Extract RSA key to separate file
- [ ] Test docker-compose locally (optional)
- [ ] Verify DNS records

### Deployment
- [ ] Update `docker-compose.lago.yml` (remove inline RSA)
- [ ] Copy files to server
- [ ] Start services: `docker compose up -d`
- [ ] Monitor logs for errors
- [ ] Verify all 6 containers running

### Configuration
- [ ] Generate Lago API key
- [ ] Update Brain Gateway connector config
- [ ] Restart Brain Gateway
- [ ] Test connector validation

### Testing
- [ ] Test Lago API directly
- [ ] Test Brain Gateway billing endpoints
- [ ] Access Lago UI via browser
- [ ] Create test subscription

### Production Readiness
- [ ] Seed billing plans
- [ ] Configure webhooks (optional)
- [ ] Set up monitoring/alerts
- [ ] Document admin procedures

---

## 🚨 Rollback Plan

If deployment fails:

**Option 1: Quick Rollback**
```bash
docker compose -f docker-compose.lago.yml down
# Keep data volumes intact
```

**Option 2: Full Cleanup**
```bash
docker compose -f docker-compose.lago.yml down -v
# Removes all data - only if irreversibly broken
```

---

## 📊 Expected Outcomes

### After Phase 1-2 (Service Startup)
✅ All 6 Lago containers running
✅ Lago API responding on port 3010
✅ No restart loops

### After Phase 3 (Traefik)
✅ `https://billing-api.bizoholic.net` → Lago API
✅ `https://billing.bizoholic.net` → Lago UI
✅ SSL certificates auto-generated

### After Phase 4 (Integration)
✅ Brain Gateway can communicate with Lago
✅ Billing endpoints functional via Brain API

### After Phase 5-6 (Complete)
✅ Full billing workflow operational
✅ Plans available for selection
✅ Subscriptions can be created
✅ Invoices generated

---

## 🔧 Monitoring Commands

```bash
# Container health
docker ps --filter name=lago

# Live logs
docker compose -f docker-compose.lago.yml logs -f

# Database connection
docker exec -it lago-db psql -U lago -d lago

# Redis status
docker exec -it lago-redis redis-cli ping

# API health endpoint
curl http://localhost:3010/health
```

---

## 📝 Next Steps

**Immediate Priority**:
1. Fix RSA key handling (choose Option C - volume mount)
2. Update docker-compose.lago.yml
3. Deploy to KVM8 server
4. Verify services running

**Would you like me to**:
- [ ] Create the updated `docker-compose.lago.yml` with volume mount approach?
- [ ] Write the deployment script with all steps automated?
- [ ] Create seed data script for billing plans?
- [ ] Set up monitoring/health checks?

**Estimated Time to Full Recovery**: 45-60 minutes with this plan.
