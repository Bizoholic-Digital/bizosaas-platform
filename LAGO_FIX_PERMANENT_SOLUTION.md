# Lago RSA Key Issue - Permanent Vault-Based Solution

## 📊 Analysis & Research

### Current Infrastructure Assessment

**✅ Available Resources:**
- **HashiCorp Vault**: Running in dev mode on `brain-network` (172.20.0.11)
  - Token: `staging-root-token-bizosaas-2025`
  - Address: `http://brain-vault:8200`
  - Status: Healthy and accessible
- **VaultAdapter**: Already implemented in `adapters/vault_adapter.py`
- **Network**: Lago services and Vault are on the same `brain-network`

**❌ Current Problem:**
1. RSA private key stored in `.env.lago` as multi-line text
2. Git sync corrupts line endings/escaping
3. Dokploy pulls corrupted config from git
4. Rails fails to parse malformed key: `OpenSSL::PKey::RSAError`

### Why This Keeps Recurring

```
Local Code (.env.lago with multi-line key)
    ↓ git commit/push
GitHub Repository (potential corruption)
    ↓ Dokploy deployment
Server (.env.lago with corrupted key)
    ↓ Lago restart
CRASH: "Neither PUB key nor PRIV key"
```

## 🎯 Recommended Solution: HashiCorp Vault Integration

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     brain-network (172.20.0.0/16)           │
│                                                             │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │ brain-vault  │◄────────│  lago-api    │                  │
│  │ 172.20.0.11  │  Fetch  │ 172.20.0.X   │                  │
│  │ :8200        │  RSA    │              │                  │
│  └──────────────┘  Key    └──────────────┘                  │
│         ▲                                                   │
│         │ Store Secret (One-time)                           │
│         │                                                   │
│  ┌──────────────┐                                           │
│  │ Setup Script │                                           │
│  └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

### Benefits of Vault Approach

1. **✅ No Git Corruption**: Secret never stored in git
2. **✅ Centralized Management**: Single source of truth
3. **✅ Rotation Support**: Easy key rotation without redeployment
4. **✅ Audit Trail**: Vault logs all secret access
5. **✅ Already Implemented**: VaultAdapter exists and tested
6. **✅ Production Ready**: Industry standard for secret management

## 📋 Implementation Plan

### Phase 1: Store RSA Key in Vault (One-Time Setup)

**Step 1.1: Prepare the RSA Key**
```bash
# On local machine
cd /home/alagiri/projects/bizosaas-platform
cat lago_rsa_valid.pem | base64 -w 0 > lago_rsa_base64.txt
```

**Step 1.2: Store in Vault**
```bash
# On server (via SSH)
ssh root@72.60.98.213

# Store the RSA key in Vault
docker exec brain-vault sh -c '
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=staging-root-token-bizosaas-2025

vault kv put secret/lago/rsa-key \
  private_key="-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA197tD6m8T3V7vD6v27p6n8m+R/TfN7Xf8k0+9fD8k0+9fD8k
YpS0fID6+69QADccroZTb3macwmTY8MmJU7nG3QfSQKBgQDtDJwDcNmMwinhJBQp
3VYIUZBD+eUiwc5Ly6YyvUdIPAguH/2Qq9NYVdZmXR6YTyq3I9XN57AqthKrFAul
z4pmb7O1rduqMyMbXcThuoxSKYO5lLRuxetSe5/HxqfgopY58PuflvwhNThm1a+b
gjTGridl7VLiTOEAqklniBmZhwKBgQDrk0fVL87mxJIE7WBBX8gMPvmo6JisMJkz
Ml6qQLMQ/d2tRz7eRppXuKwsjHEtSjmB+HYh4XEewnEsLOAt66AlRQS7qnkFqz1f
s6chItB/7Z8MeLjEJKcG+1TP6ILl5Zv33wOEYYJkZQMHM6uJ32HAbrWZgjXkPcqu
UiLi1X4TqQKBgFVnwZ4LvpXULrqLASjEMgb1PAEBu+h14xmz2cFWKKSB3IChzf2d
qpuc8Y4X5roBa+Zn5tQ0sWfyCW/R3RB0YezeOeUvKoF7wx5M/m5Fg+DmTCtExG1U
qaAiIkMb88gfS/i8NiwdfeGJBzUlsAtbMiCTBmbWxpH6GObgc2n1wyNpAoGAAcpC
t3n/hn1j5qmvG5AQwxcPapsp3dUYtOzjD0QimDR1pMVv0tySe6wpksUWbxOrUDOF
IkjGRUeQ+Jb2tSKfOulFWe+3r7VXaAzDblsHXpF9reiU7tigdEsgn9vSctDF2KJX
MoBTL1QdK8bWvNt3sLCmrJ3yruNRUPXK0hJxPNECgYEAq+I5v/P9OEZI7UEoeB5I
BM2RR5doij+5kXpJB5UCd8GaXiX3pyRO3whGFamv0vHUDyDFGg8eklJ7zz+LaqK5
3i3LeAjfdcyz7ZgKhQUBAEfFzBto4YGzyh8nZILWHzX5yl8h1VfwRHIGTtLL9bfp
1RKEqnEjqIMoc2ZbvFI2pyw=
-----END RSA PRIVATE KEY-----"
'

# Verify storage
docker exec brain-vault sh -c '
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=staging-root-token-bizosaas-2025
vault kv get secret/lago/rsa-key
'
```

### Phase 2: Create Lago Vault Integration Script

**File: `scripts/lago-fetch-rsa-from-vault.sh`**
```bash
#!/bin/bash
# Fetch Lago RSA key from Vault and set as environment variable

set -e

VAULT_ADDR="${VAULT_ADDR:-http://brain-vault:8200}"
VAULT_TOKEN="${VAULT_TOKEN:-staging-root-token-bizosaas-2025}"

echo "🔐 Fetching RSA key from Vault..."

# Fetch the key from Vault
RSA_KEY=$(curl -s \
  -H "X-Vault-Token: ${VAULT_TOKEN}" \
  "${VAULT_ADDR}/v1/secret/data/lago/rsa-key" | \
  jq -r '.data.data.private_key')

if [ -z "$RSA_KEY" ] || [ "$RSA_KEY" = "null" ]; then
  echo "❌ Failed to fetch RSA key from Vault"
  exit 1
fi

echo "✅ RSA key fetched successfully"

# Export for Lago to use
export LAGO_RSA_PRIVATE_KEY="$RSA_KEY"

# Execute the original Lago command
exec "$@"
```

### Phase 3: Update Lago Docker Compose

**File: `docker-compose.lago.yml`**
```yaml
services:
  lago-api:
    image: getlago/api:v1.16.0
    restart: unless-stopped
    depends_on:
      lago-migrate:
        condition: service_completed_successfully
      lago-db:
        condition: service_started
      lago-redis:
        condition: service_started
    environment:
      # Vault configuration
      VAULT_ADDR: http://brain-vault:8200
      VAULT_TOKEN: staging-root-token-bizosaas-2025
      
      # Other Lago configs (without RSA key)
      LAGO_POSTGRES_DB: ${LAGO_POSTGRES_DB:-lago}
      LAGO_POSTGRES_USER: ${LAGO_POSTGRES_USER:-lago}
      LAGO_POSTGRES_PASSWORD: ${LAGO_POSTGRES_PASSWORD:-lago_password_2025}
      LAGO_SECRET_KEY_BASE: ${LAGO_SECRET_KEY_BASE}
      LAGO_ENCRYPTION_PRIMARY_KEY: ${LAGO_ENCRYPTION_PRIMARY_KEY}
      LAGO_ENCRYPTION_DETERMINISTIC_KEY: ${LAGO_ENCRYPTION_DETERMINISTIC_KEY}
      LAGO_ENCRYPTION_KEY_DERIVATION_SALT: ${LAGO_ENCRYPTION_KEY_DERIVATION_SALT}
      LAGO_API_URL: http://lago-api:3000
      LAGO_FRONT_URL: https://billing.bizoholic.net
      RAILS_ENV: production
      LAGO_REDIS_URL: redis://lago-redis:6379/1
      LAGO_DATABASE_URL: postgresql://lago:lago_password_2025@lago-db:5432/lago
    volumes:
      - ./scripts/lago-fetch-rsa-from-vault.sh:/usr/local/bin/fetch-rsa.sh:ro
    entrypoint: ["/bin/bash", "/usr/local/bin/fetch-rsa.sh"]
    command: ["./scripts/start.api.sh"]
    networks:
      - brain-network
      - dokploy-network
    labels:
      traefik.enable: "true"
      traefik.http.routers.lago-api.rule: Host(`${LAGO_API_DOMAIN:-billing-api.bizoholic.net}`)
      traefik.http.routers.lago-api.entrypoints: websecure
      traefik.http.routers.lago-api.tls: "true"
      traefik.http.routers.lago-api.tls.certresolver: letsencrypt
      traefik.http.services.lago-api.loadbalancer.server.port: "3000"
      traefik.docker.network: dokploy-network

  lago-worker:
    image: getlago/api:v1.16.0
    restart: unless-stopped
    depends_on:
      lago-migrate:
        condition: service_completed_successfully
      lago-db:
        condition: service_started
      lago-redis:
        condition: service_started
    environment:
      VAULT_ADDR: http://brain-vault:8200
      VAULT_TOKEN: staging-root-token-bizosaas-2025
      LAGO_POSTGRES_DB: ${LAGO_POSTGRES_DB:-lago}
      LAGO_POSTGRES_USER: ${LAGO_POSTGRES_USER:-lago}
      LAGO_POSTGRES_PASSWORD: ${LAGO_POSTGRES_PASSWORD:-lago_password_2025}
      LAGO_SECRET_KEY_BASE: ${LAGO_SECRET_KEY_BASE}
      LAGO_ENCRYPTION_PRIMARY_KEY: ${LAGO_ENCRYPTION_PRIMARY_KEY}
      LAGO_ENCRYPTION_DETERMINISTIC_KEY: ${LAGO_ENCRYPTION_DETERMINISTIC_KEY}
      LAGO_ENCRYPTION_KEY_DERIVATION_SALT: ${LAGO_ENCRYPTION_KEY_DERIVATION_SALT}
      LAGO_API_URL: http://lago-api:3000
      LAGO_FRONT_URL: https://billing.bizoholic.net
      RAILS_ENV: production
      LAGO_REDIS_URL: redis://lago-redis:6379/1
      LAGO_DATABASE_URL: postgresql://lago:lago_password_2025@lago-db:5432/lago
    volumes:
      - ./scripts/lago-fetch-rsa-from-vault.sh:/usr/local/bin/fetch-rsa.sh:ro
    entrypoint: ["/bin/bash", "/usr/local/bin/fetch-rsa.sh"]
    command: ["./scripts/start.worker.sh"]
    networks:
      - brain-network

networks:
  brain-network:
    external: true
    name: brain-network
  dokploy-network:
    external: true
```

### Phase 4: Update Local `.env.lago` (Remove RSA Key)

**File: `.env.lago`**
```bash
# Database Configuration
LAGO_POSTGRES_DB=lago
LAGO_POSTGRES_USER=lago
LAGO_POSTGRES_PASSWORD=lago_password_2025

# Encryption Keys
LAGO_SECRET_KEY_BASE=b871ed19c83665268c74149028bfdf3787727402660161421715423877960786
LAGO_ENCRYPTION_PRIMARY_KEY=b871ed19c83665268c74149028bfdf37
LAGO_ENCRYPTION_DETERMINISTIC_KEY=c4772099e0df28646077558667c29579
LAGO_ENCRYPTION_KEY_DERIVATION_SALT=5c72d9e685f02604297135317769532e

# URLs
LAGO_API_URL=http://lago-api:3000
LAGO_FRONT_URL=https://billing.bizoholic.net
RAILS_ENV=production

# Redis & Database
LAGO_REDIS_URL=redis://lago-redis:6379/1
LAGO_DATABASE_URL=postgresql://lago:lago_password_2025@lago-db:5432/lago

# NOTE: LAGO_RSA_PRIVATE_KEY is now fetched from Vault at runtime
# No need to store it in this file anymore
```

## 🚀 Deployment Steps

### Step 1: Store Secret in Vault (Execute Once)
```bash
# Run the Vault storage script from Phase 1.2
```

### Step 2: Update Local Repository
```bash
cd /home/alagiri/projects/bizosaas-platform

# Create the fetch script
mkdir -p scripts
cat > scripts/lago-fetch-rsa-from-vault.sh << 'EOF'
#!/bin/bash
set -e
VAULT_ADDR="${VAULT_ADDR:-http://brain-vault:8200}"
VAULT_TOKEN="${VAULT_TOKEN:-staging-root-token-bizosaas-2025}"
echo "🔐 Fetching RSA key from Vault..."
RSA_KEY=$(curl -s -H "X-Vault-Token: ${VAULT_TOKEN}" "${VAULT_ADDR}/v1/secret/data/lago/rsa-key" | jq -r '.data.data.private_key')
if [ -z "$RSA_KEY" ] || [ "$RSA_KEY" = "null" ]; then
  echo "❌ Failed to fetch RSA key from Vault"
  exit 1
fi
echo "✅ RSA key fetched successfully"
export LAGO_RSA_PRIVATE_KEY="$RSA_KEY"
exec "$@"
EOF

chmod +x scripts/lago-fetch-rsa-from-vault.sh

# Update .env.lago (remove RSA key)
sed -i '/^LAGO_RSA_PRIVATE_KEY=/d' .env.lago
echo "# NOTE: LAGO_RSA_PRIVATE_KEY is now fetched from Vault at runtime" >> .env.lago

# Commit changes
git add scripts/lago-fetch-rsa-from-vault.sh .env.lago docker-compose.lago.yml
git commit -m "feat: Integrate Lago with Vault for RSA key management"
git push origin main
```

### Step 3: Deploy via Dokploy
```bash
# Trigger redeploy in Dokploy UI for "Lago Billing" service
# OR manually via CLI:
ssh root@72.60.98.213 "cd /etc/dokploy/compose/bizosaasbraingateway-lagobilling-g0n3if/code && \
  git pull && \
  docker compose -p bizosaasbraingateway-lagobilling-g0n3if -f docker-compose.lago.yml up -d --force-recreate"
```

## ✅ Verification & Testing

### Test 1: Verify Vault Secret
```bash
ssh root@72.60.98.213
docker exec brain-vault sh -c '
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=staging-root-token-bizosaas-2025
vault kv get secret/lago/rsa-key
'
```

### Test 2: Check Lago API Startup
```bash
ssh root@72.60.98.213
docker logs bizosaasbraingateway-lagobilling-g0n3if-lago-api-1 -f
# Look for: "✅ RSA key fetched successfully" and "Puma starting"
```

### Test 3: Verify RSA Key Loading
```bash
ssh root@72.60.98.213
docker exec bizosaasbraingateway-lagobilling-g0n3if-lago-api-1 \
  rails runner "puts LAGO_RSA_PRIVATE_KEY.class"
# Expected output: OpenSSL::PKey::RSA
```

### Test 4: Health Check
```bash
curl -f https://billing-api.bizoholic.net/health
```

## 🔄 Key Rotation Procedure

When you need to rotate the RSA key:

```bash
# 1. Generate new key
openssl genrsa -out new_lago_rsa.pem 2048

# 2. Update Vault
ssh root@72.60.98.213
docker exec brain-vault sh -c '
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=staging-root-token-bizosaas-2025
vault kv put secret/lago/rsa-key private_key="$(cat new_lago_rsa.pem)"
'

# 3. Restart Lago services
docker compose -p bizosaasbraingateway-lagobilling-g0n3if -f docker-compose.lago.yml restart lago-api lago-worker

# No git commit needed! 🎉
```

## 🛡️ Security Benefits

1. **Zero Secrets in Git**: RSA key never committed to repository
2. **Centralized Audit**: Vault logs all secret access attempts
3. **Easy Rotation**: Update Vault, restart services - done
4. **Access Control**: Vault policies can restrict who accesses what
5. **Encryption at Rest**: Vault encrypts all stored secrets

## 📊 Comparison: Before vs After

| Aspect | Before (`.env.lago`) | After (Vault) |
|--------|---------------------|---------------|
| Secret Storage | Git repository | Vault KV store |
| Corruption Risk | High (line endings) | None |
| Rotation | Redeploy required | Restart only |
| Audit Trail | None | Full Vault audit |
| Security | Low (plaintext in git) | High (encrypted) |
| Sync Issues | Frequent | Never |

## 🔧 Troubleshooting

### Issue: "Failed to fetch RSA key from Vault"
```bash
# Check Vault connectivity
docker exec bizosaasbraingateway-lagobilling-g0n3if-lago-api-1 \
  curl -v http://brain-vault:8200/v1/sys/health

# Check if secret exists
docker exec brain-vault sh -c '
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=staging-root-token-bizosaas-2025
vault kv get secret/lago/rsa-key
'
```

### Issue: Lago still crashes with RSA error
```bash
# Check if fetch script is mounted
docker exec bizosaasbraingateway-lagobilling-g0n3if-lago-api-1 \
  cat /usr/local/bin/fetch-rsa.sh

# Check environment variables
docker exec bizosaasbraingateway-lagobilling-g0n3if-lago-api-1 env | grep VAULT
```

## 🎯 Next Steps

1. ✅ **Immediate**: Store RSA key in Vault
2. ✅ **Short-term**: Update docker-compose and deploy
3. ✅ **Long-term**: Migrate other secrets (DB passwords, encryption keys) to Vault
4. ✅ **Future**: Implement Vault dynamic secrets for database credentials

---

**Status**: Ready for implementation
**Estimated Time**: 30 minutes
**Risk Level**: Low (can rollback to base64 approach if needed)
