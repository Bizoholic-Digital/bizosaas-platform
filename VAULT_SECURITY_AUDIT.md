# HashiCorp Vault Security Audit - BizOSaaS Platform

**Date**: October 15, 2025, 5:45 PM
**Vault Container**: `caf72d99ef8a` (bizosaas-vault-staging)
**Status**: ⚠️ CRITICAL SECURITY ISSUES FOUND

---

## 🚨 CRITICAL FINDINGS

### 1. Hardcoded Secrets in Compose Files (HIGH SEVERITY)

**All sensitive credentials are currently HARDCODED** in compose files instead of using Vault:

#### Database Credentials (EXPOSED)
```yaml
# dokploy-backend-staging-local.yml
DATABASE_URL=postgres://admin:BizOSaaS2025!StagingDB@194.238.16.237:5433/saleor_staging
```
- ❌ Username: `admin` (hardcoded)
- ❌ Password: `BizOSaaS2025!StagingDB` (hardcoded)
- ❌ Same password used across ALL services
- 🔥 **Impact**: Complete database access if compose file leaked

#### Redis Credentials (EXPOSED)
```yaml
REDIS_URL=redis://194.238.16.237:6380/1
```
- ❌ No authentication configured
- 🔥 **Impact**: Cache poisoning, session hijacking possible

#### Secret Keys (EXPOSED)
```yaml
SECRET_KEY=staging-secret-key-saleor-bizosaas-2025
JWT_SECRET=staging-jwt-secret-bizosaas-2025-secure
```
- ❌ Django SECRET_KEY hardcoded
- ❌ JWT signing key hardcoded
- 🔥 **Impact**: Session forgery, authentication bypass

---

## 📊 Hardcoded Secrets Inventory

### Backend Services (10 services)

| Service | Database Password | Secret Key | JWT Key | API Keys |
|---------|-------------------|------------|---------|----------|
| Saleor | ✅ Hardcoded | ✅ Hardcoded | N/A | N/A |
| Brain Gateway | ✅ Hardcoded | N/A | N/A | ⚠️ ${OPENAI_API_KEY} |
| Wagtail CMS | ✅ Hardcoded | ✅ Hardcoded | N/A | N/A |
| Django CRM | ✅ Hardcoded | ✅ Hardcoded | N/A | N/A |
| Business Directory | ✅ Hardcoded | ✅ Hardcoded | N/A | N/A |
| CorelDove Backend | ✅ Hardcoded | ✅ Hardcoded | N/A | N/A |
| Auth Service | ✅ Hardcoded | ✅ Hardcoded | ✅ Hardcoded | N/A |
| AI Agents | ✅ Hardcoded | N/A | N/A | ⚠️ ${OPENAI_API_KEY} |
| Amazon Sourcing | ✅ Hardcoded | N/A | N/A | ⚠️ ${AMAZON_*} |
| QuantTrade | ✅ Hardcoded | ✅ Hardcoded | N/A | N/A |

**Summary**:
- ❌ 10/10 services have hardcoded database passwords
- ❌ 7/10 services have hardcoded secret keys
- ⚠️ 3/10 use environment variables (still not Vault)

### Infrastructure Services (6 services)

| Service | Root Password | Admin Credentials |
|---------|---------------|-------------------|
| PostgreSQL | ✅ Hardcoded: `BizOSaaS2025!StagingDB` | ✅ Hardcoded: `admin` |
| Redis | ❌ No password (open access) | N/A |
| Vault | ⚠️ Dev token (unsealed) | ⚠️ `bizosaas-dev-root-token` |
| Temporal | ⚠️ Unknown | ⚠️ Unknown |
| Superset | ⚠️ Unknown | ⚠️ Unknown |

---

## 🎯 Current Vault Integration Status

### Services with Vault Configuration (2/23)

#### 1. Wagtail CMS
```yaml
environment:
  - VAULT_ADDR=http://bizosaas-vault-staging:8200
  - VAULT_TOKEN=bizosaas-dev-root-token
  - VAULT_MOUNT_PATH=bizosaas
```
- ✅ Vault environment variables present
- ❌ **BUT**: Still using hardcoded DATABASE_URL and SECRET_KEY
- ❌ **Vault token hardcoded** (defeats the purpose)

#### 2. Django CRM
```yaml
environment:
  - VAULT_ADDR=http://bizosaas-vault-staging:8200
  - VAULT_TOKEN=bizosaas-dev-root-token
  - VAULT_MOUNT_PATH=bizosaas
```
- ✅ Vault environment variables present
- ❌ **BUT**: Still using hardcoded credentials
- ❌ **Vault token hardcoded**

### Services WITHOUT Vault Integration (21/23)

- Saleor, Brain Gateway, Business Directory, CorelDove Backend
- Auth Service, AI Agents, Amazon Sourcing, QuantTrade
- All 7 frontend services
- All 4 other infrastructure services

---

## 🔒 Recommended Vault Secret Structure

### Database Secrets
```bash
vault kv put bizosaas/database/postgres \
  username=admin \
  password=<strong-random-password> \
  host=bizosaas-postgres-staging \
  port=5432

vault kv put bizosaas/database/redis \
  password=<strong-random-password> \
  host=bizosaas-redis-staging \
  port=6379
```

### Application Secrets
```bash
vault kv put bizosaas/apps/saleor \
  secret_key=<cryptographically-secure-key> \
  database_url=postgres://...from-vault...

vault kv put bizosaas/apps/auth-service \
  secret_key=<unique-key> \
  jwt_secret=<unique-jwt-key> \
  database_url=postgres://...from-vault...

vault kv put bizosaas/apps/django-crm \
  secret_key=<unique-key> \
  database_url=postgres://...from-vault...
```

### External API Keys
```bash
vault kv put bizosaas/external/openai \
  api_key=<openai-key>

vault kv put bizosaas/external/amazon \
  access_key=<amazon-access-key> \
  secret_key=<amazon-secret-key>

vault kv put bizosaas/external/stripe \
  publishable_key=<stripe-pub-key> \
  secret_key=<stripe-secret-key>
```

---

## 📋 Migration Plan to Vault

### Phase 1: Infrastructure Secrets (HIGH PRIORITY)
1. **PostgreSQL Password Rotation**
   - Generate new strong password in Vault
   - Update PostgreSQL to use new password
   - Update all services to read from Vault

2. **Redis Authentication**
   - Enable Redis password authentication
   - Store password in Vault
   - Update all services

3. **Vault Token Management**
   - Replace dev root token with app-specific tokens
   - Implement AppRole authentication
   - One token per service with minimal permissions

### Phase 2: Application Secrets (MEDIUM PRIORITY)
1. **Django SECRET_KEY**
   - Generate unique keys per service
   - Store in Vault at `bizosaas/apps/{service}/secret_key`
   - Update each Django service to read from Vault

2. **JWT Secrets**
   - Generate strong JWT signing keys
   - Store in Vault at `bizosaas/apps/auth-service/jwt_secret`
   - Update Auth Service configuration

3. **API Keys**
   - Migrate OPENAI_API_KEY to Vault
   - Migrate Amazon credentials to Vault
   - Use environment variable placeholders that read from Vault

### Phase 3: Service Updates (IMPLEMENTATION)

**For each service, update compose file from:**
```yaml
environment:
  - DATABASE_URL=postgres://admin:password@host:5432/db
  - SECRET_KEY=hardcoded-key
```

**To:**
```yaml
environment:
  - VAULT_ADDR=http://bizosaas-vault-staging:8200
  - VAULT_TOKEN=${VAULT_APP_TOKEN}  # Unique per service
  - VAULT_MOUNT_PATH=bizosaas
  - VAULT_SECRET_PATH=apps/service-name
```

**Application code must then:**
```python
import hvac

vault_client = hvac.Client(
    url=os.getenv('VAULT_ADDR'),
    token=os.getenv('VAULT_TOKEN')
)

secrets = vault_client.secrets.kv.v2.read_secret_version(
    path=os.getenv('VAULT_SECRET_PATH'),
    mount_point=os.getenv('VAULT_MOUNT_PATH')
)

DATABASE_URL = secrets['data']['data']['database_url']
SECRET_KEY = secrets['data']['data']['secret_key']
```

---

## 🔧 Implementation Checklist

### Vault Configuration
- [ ] Verify Vault is sealed/unsealed properly
- [ ] Enable KV v2 secrets engine at `bizosaas/`
- [ ] Create AppRole auth method
- [ ] Generate unique tokens per service
- [ ] Set token TTL and renewal policies

### Secret Migration
- [ ] Migrate PostgreSQL credentials
- [ ] Migrate Redis credentials
- [ ] Migrate all Django SECRET_KEYs
- [ ] Migrate JWT secrets
- [ ] Migrate external API keys (OpenAI, Amazon, Stripe)

### Service Updates
- [ ] Update Saleor to use Vault
- [ ] Update Brain Gateway to use Vault
- [ ] Update Wagtail (fix existing integration)
- [ ] Update Django CRM (fix existing integration)
- [ ] Update Business Directory to use Vault
- [ ] Update CorelDove Backend to use Vault
- [ ] Update Auth Service to use Vault
- [ ] Update AI Agents to use Vault
- [ ] Update Amazon Sourcing to use Vault
- [ ] Update QuantTrade to use Vault

### Testing
- [ ] Verify each service can read secrets from Vault
- [ ] Test token rotation
- [ ] Test service restart with Vault integration
- [ ] Verify secrets are NOT logged

### Cleanup
- [ ] Remove hardcoded credentials from compose files
- [ ] Rotate all exposed credentials
- [ ] Update documentation with Vault usage
- [ ] Set up secret rotation policies

---

## 🚨 IMMEDIATE SECURITY ACTIONS REQUIRED

### 1. Rotate Exposed Credentials (URGENT)
Since credentials are in Git history:
```bash
# PostgreSQL
ALTER USER admin WITH PASSWORD '<new-strong-password>';

# Generate new Django SECRET_KEYs
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate new JWT secret
openssl rand -base64 64
```

### 2. Enable Redis Authentication (URGENT)
```yaml
# dokploy-infrastructure-staging-with-superset-build.yml
redis:
  command: redis-server --requirepass <strong-password-from-vault>
```

### 3. Implement Vault AppRole (HIGH)
```bash
vault auth enable approle

# Create policy for each service
vault policy write saleor-policy - <<EOF
path "bizosaas/data/apps/saleor" { capabilities = ["read"] }
EOF

# Create AppRole
vault write auth/approle/role/saleor \
  token_policies="saleor-policy" \
  token_ttl=1h \
  token_max_ttl=4h
```

---

## 📊 Security Risk Assessment

### Current Risk Level: 🔴 **CRITICAL**

**Vulnerabilities**:
1. Database password leaked in compose files (accessible via Dokploy UI)
2. Same password used across 10+ services (lateral movement risk)
3. Secret keys in Git history (session hijacking possible)
4. Redis unauthenticated (cache poisoning, DoS)
5. Vault dev token hardcoded (defeats Vault purpose)

**Impact if Exploited**:
- Complete database compromise
- Authentication bypass on all services
- Session hijacking across platform
- Data exfiltration from 23 services
- Lateral movement through entire infrastructure

**Likelihood**: HIGH (credentials in Git, Dokploy accessible)

---

## 📈 Post-Vault Migration Benefits

1. **Centralized Secret Management**: All secrets in one secure location
2. **Dynamic Secrets**: Short-lived credentials with auto-rotation
3. **Audit Trail**: Every secret access logged
4. **Zero Hardcoding**: No secrets in code or config files
5. **Access Control**: Per-service least-privilege access
6. **Compliance**: Meets SOC2, GDPR, PCI-DSS requirements

---

## 🎯 Timeline Estimate

| Phase | Tasks | Duration |
|-------|-------|----------|
| Phase 1: Vault Setup | Enable engines, policies, AppRoles | 2-4 hours |
| Phase 2: Secret Migration | Move all secrets to Vault | 4-6 hours |
| Phase 3: Service Updates | Update 23 services | 8-12 hours |
| Phase 4: Testing | End-to-end validation | 2-4 hours |
| Phase 5: Credential Rotation | Rotate all exposed secrets | 2-3 hours |
| **Total** | | **18-29 hours** |

---

**Status**: ⚠️ **VAULT PRESENT BUT NOT ACTIVELY USED**
**Priority**: 🔴 **HIGH - Security vulnerability**
**Next Action**: Implement Phase 1 (Vault setup and infrastructure secrets)

**Last Updated**: October 15, 2025, 5:45 PM
