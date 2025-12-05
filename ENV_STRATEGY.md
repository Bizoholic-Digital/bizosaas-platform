# Environment Variables Strategy - Local vs Production

## Overview

**Local Development:** `.env.local` (non-sensitive, convenience)
**Production:** HashiCorp Vault (sensitive, secure)

## Local Development (.env.local)

### Purpose
- **Non-sensitive** configuration only
- **Developer convenience** (no Vault setup needed)
- **Fast iteration** during development

### What Goes in .env.local
```bash
# API Endpoints (local)
NEXT_PUBLIC_BRAIN_API_URL=http://localhost:8001
NEXT_PUBLIC_WAGTAIL_URL=http://localhost:8002
NEXT_PUBLIC_AUTH_API_URL=http://localhost:8007

# Feature Flags
NEXT_PUBLIC_ENABLE_SSR=true
NEXT_PUBLIC_PWA_ENABLED=true

# Non-sensitive IDs
NEXT_PUBLIC_TENANT_ID=bizoholic
NEXT_PUBLIC_PLATFORM_TYPE=marketing-website
```

### What NEVER Goes in .env.local
❌ API Keys
❌ Database passwords
❌ JWT secrets
❌ OAuth client secrets
❌ Encryption keys

## Production (Vault)

### Purpose
- **All sensitive** credentials
- **Centralized** secret management
- **Rotation** and auditing
- **Access control**

### What Goes in Vault
```bash
# Stored in Vault at: secret/bizosaas/production/
DATABASE_URL=postgresql://user:SECURE_PASSWORD@host:5432/db
JWT_SECRET=SECURE_RANDOM_STRING
STRIPE_SECRET_KEY=sk_live_...
OPENAI_API_KEY=sk-...
AWS_SECRET_ACCESS_KEY=...
```

### How Services Access Vault

#### Backend Services (Python/Node)
```python
# Example: Brain Gateway
import hvac

client = hvac.Client(url='http://vault:8200')
client.token = os.getenv('VAULT_TOKEN')

secrets = client.secrets.kv.v2.read_secret_version(
    path='bizosaas/production/brain-gateway'
)

OPENAI_API_KEY = secrets['data']['data']['OPENAI_API_KEY']
```

#### Frontend Services (Next.js)
Frontends should **NEVER** access Vault directly. Instead:
1. Backend API fetches secrets from Vault
2. Backend provides data to frontend via API
3. Frontend uses public environment variables only

## Hybrid Approach (Recommended)

### Local Development
```bash
# .env.local (checked into git, non-sensitive)
NEXT_PUBLIC_API_URL=http://localhost:8001
VAULT_ENABLED=false
```

### Staging/Production
```bash
# .env.production (checked into git)
NEXT_PUBLIC_API_URL=https://api.bizosaas.com
VAULT_ENABLED=true
VAULT_ADDR=https://vault.bizosaas.com:8200

# Actual secrets fetched from Vault at runtime
```

## Implementation

### 1. Update next.config.js
```javascript
const nextConfig = {
  env: {
    // Public variables (safe to expose)
    NEXT_PUBLIC_VAULT_ENABLED: process.env.VAULT_ENABLED || 'false',
  },
  
  // For production builds
  output: 'standalone',
  
  // Trace only necessary files
  outputFileTracingRoot: process.env.OUTPUT_TRACING_ROOT,
}
```

### 2. Backend Service Configuration
```python
# shared/services/brain-gateway/config.py
import os
from vault_client import get_secret

if os.getenv('VAULT_ENABLED') == 'true':
    # Production: Use Vault
    OPENAI_API_KEY = get_secret('openai_api_key')
    DATABASE_URL = get_secret('database_url')
else:
    # Local: Use environment variables
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-test-key')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/bizosaas')
```

### 3. Docker Compose Integration
```yaml
# shared/services/docker-compose.services.yml
services:
  brain-gateway:
    environment:
      - VAULT_ENABLED=${VAULT_ENABLED:-false}
      - VAULT_ADDR=${VAULT_ADDR:-http://vault:8200}
      - VAULT_TOKEN=${VAULT_TOKEN}
```

## Security Best Practices

### ✅ DO
- Use `.env.local` for local development convenience
- Store ALL sensitive data in Vault for production
- Use different Vault paths per environment (dev/staging/prod)
- Rotate secrets regularly via Vault
- Use Vault's dynamic secrets when possible

### ❌ DON'T
- Commit `.env.local` with sensitive data
- Use same secrets across environments
- Hardcode secrets in code
- Expose Vault tokens in frontend
- Store production secrets in `.env` files

## Migration Path

### Phase 1: Local Development (Current)
```bash
# Use .env.local for convenience
# No Vault required
```

### Phase 2: Staging Deployment
```bash
# Enable Vault
# Migrate sensitive secrets to Vault
# Keep non-sensitive in .env.production
```

### Phase 3: Production
```bash
# All sensitive data in Vault
# Automated secret rotation
# Audit logging enabled
```

---

**Current Status:** Phase 1 (Local Development)
**Next:** Once local testing works, implement Vault integration for staging/production
