#!/bin/bash

# Setup Staging Environment for Testing
# Task: ENV-001 through ENV-007

set -e

echo "🔧 Setting up BizOSaaS Staging Environment"
echo "==========================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
STAGING_HOST="${STAGING_HOST:-staging.bizosaas.com}"
POSTGRES_VERSION="16"
REDIS_VERSION="7"

# Check prerequisites
echo "Checking prerequisites..."

command -v docker >/dev/null 2>&1 || { echo -e "${RED}❌ Docker is required${NC}"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo -e "${RED}❌ Docker Compose is required${NC}"; exit 1; }

echo -e "${GREEN}✓ Prerequisites met${NC}"
echo ""

# ENV-001: Create staging environment
echo "📦 ENV-001: Creating staging environment..."

cat > docker-compose.staging.yml << 'EOF'
version: '3.8'

services:
  # PostgreSQL with pgvector
  postgres-staging:
    image: pgvector/pgvector:pg16
    container_name: bizosaas-postgres-staging
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-admin}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: bizosaas_staging
    ports:
      - "5433:5432"
    volumes:
      - postgres-staging-data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis
  redis-staging:
    image: redis:7-alpine
    container_name: bizosaas-redis-staging
    ports:
      - "6380:6379"
    volumes:
      - redis-staging-data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Vault
  vault-staging:
    image: hashicorp/vault:1.15
    container_name: bizosaas-vault-staging
    ports:
      - "8201:8200"
    environment:
      VAULT_DEV_ROOT_TOKEN_ID: ${VAULT_ROOT_TOKEN}
      VAULT_DEV_LISTEN_ADDRESS: 0.0.0.0:8200
    cap_add:
      - IPC_LOCK
    volumes:
      - vault-staging-data:/vault/data
    healthcheck:
      test: ["CMD", "vault", "status"]
      interval: 10s
      timeout: 5s
      retries: 3

  # Temporal
  temporal-staging:
    image: temporalio/auto-setup:1.22.0
    container_name: bizosaas-temporal-staging
    ports:
      - "7234:7233"
    environment:
      - DB=postgresql
      - DB_PORT=5432
      - POSTGRES_USER=${POSTGRES_USER:-admin}
      - POSTGRES_PWD=${POSTGRES_PASSWORD}
      - POSTGRES_SEEDS=postgres-staging
    depends_on:
      postgres-staging:
        condition: service_healthy

volumes:
  postgres-staging-data:
  redis-staging-data:
  vault-staging-data:
EOF

echo -e "${GREEN}✓ Staging docker-compose created${NC}"

# ENV-002: Set up Vault for secrets management
echo ""
echo "🔐 ENV-002: Setting up Vault for secrets management..."

# Create Vault initialization script
cat > init-vault.sh << 'EOF'
#!/bin/bash
set -e

export VAULT_ADDR='http://localhost:8201'
export VAULT_TOKEN="${VAULT_ROOT_TOKEN}"

# Wait for Vault to be ready
echo "Waiting for Vault..."
until vault status >/dev/null 2>&1; do
    sleep 1
done

# Enable KV secrets engine
vault secrets enable -path=bizosaas kv-v2 || true

# Create secrets
vault kv put bizosaas/database \
    host=bizosaas-postgres-staging \
    port=5432 \
    user=admin \
    password="${POSTGRES_PASSWORD}" \
    database=bizosaas_staging

vault kv put bizosaas/redis \
    host=bizosaas-redis-staging \
    port=6379

vault kv put bizosaas/jwt \
    secret="${JWT_SECRET}"

vault kv put bizosaas/api-keys \
    openai="${OPENAI_API_KEY}" \
    anthropic="${ANTHROPIC_API_KEY}"

# Create policy for application access
vault policy write bizosaas-app - <<POLICY
path "bizosaas/*" {
  capabilities = ["read", "list"]
}
POLICY

echo "✓ Vault secrets configured"
EOF

chmod +x init-vault.sh

echo -e "${GREEN}✓ Vault setup script created${NC}"

# ENV-003: Configure immutable environment configs
echo ""
echo "⚙️  ENV-003: Configuring immutable environment configs..."

cat > .env.staging << 'EOF'
# BizOSaaS Staging Environment Configuration
# DO NOT COMMIT THIS FILE

# Environment
NODE_ENV=staging
ENVIRONMENT=staging

# Database
POSTGRES_USER=admin
POSTGRES_PASSWORD=CHANGE_ME_IN_PRODUCTION
DATABASE_URL=postgresql://admin:CHANGE_ME@bizosaas-postgres-staging:5432/bizosaas_staging

# Redis
REDIS_HOST=bizosaas-redis-staging
REDIS_PORT=6379
REDIS_URL=redis://bizosaas-redis-staging:6379

# Vault
VAULT_ADDR=http://bizosaas-vault-staging:8200
VAULT_ROOT_TOKEN=staging-root-token-bizosaas-2025

# JWT
JWT_SECRET=CHANGE_ME_IN_PRODUCTION
JWT_EXPIRY=24h

# API Keys (from Vault)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# URLs
CLIENT_PORTAL_URL=https://staging.bizosaas.com
ADMIN_DASHBOARD_URL=https://admin-staging.bizosaas.com
API_URL=https://api-staging.bizosaas.com

# Feature Flags
FEATURE_AI_AGENTS=true
FEATURE_ADVANCED_ANALYTICS=true
FEATURE_BETA_FEATURES=false

# Observability
LOKI_URL=http://loki:3100
PROMETHEUS_URL=http://prometheus:9090
GRAFANA_URL=http://grafana:3000
EOF

echo -e "${GREEN}✓ Environment config template created${NC}"
echo -e "${YELLOW}⚠ Update .env.staging with actual secrets${NC}"

# ENV-004: Set up feature flags
echo ""
echo "🚩 ENV-004: Setting up feature flags..."

cat > feature-flags.json << 'EOF'
{
  "flags": {
    "ai_agents": {
      "enabled": true,
      "tenants": ["*"],
      "safe_off_default": false,
      "description": "Enable AI agent functionality"
    },
    "advanced_analytics": {
      "enabled": true,
      "tenants": ["enterprise"],
      "safe_off_default": false,
      "description": "Advanced analytics dashboard"
    },
    "beta_features": {
      "enabled": false,
      "tenants": [],
      "safe_off_default": true,
      "description": "Beta features for testing"
    },
    "new_billing_flow": {
      "enabled": false,
      "tenants": ["test-tenant-1"],
      "safe_off_default": true,
      "description": "New billing workflow (testing)"
    }
  },
  "overrides": {
    "tenant-specific": {},
    "user-specific": {}
  }
}
EOF

echo -e "${GREEN}✓ Feature flags configured${NC}"

# ENV-006: Configure Redis DB isolation
echo ""
echo "💾 ENV-006: Configuring Redis DB isolation..."

cat > redis-db-mapping.md << 'EOF'
# Redis Database Isolation

| DB Index | Service | Purpose |
|----------|---------|---------|
| 0 | Brain Gateway | API caching, sessions |
| 1 | Auth Service | Tokens, rate limiting |
| 2 | Client Portal | UI state, sessions |
| 3 | Admin Dashboard | Admin sessions |
| 4 | Plane | Project cache |
| 5 | Lago | Billing cache |
| 6 | Authentik | SSO sessions |
| 7 | Temporal | Workflow cache |
| 8 | Prometheus | Metrics buffer |
| 9 | Grafana | Dashboard cache |

## Usage Example

```python
# Brain Gateway
redis_client = redis.Redis(host='redis-staging', port=6379, db=0)

# Auth Service
redis_client = redis.Redis(host='redis-staging', port=6379, db=1)
```
EOF

echo -e "${GREEN}✓ Redis DB mapping documented${NC}"

# ENV-007: Set up PostgreSQL databases
echo ""
echo "🗄️  ENV-007: Setting up PostgreSQL databases..."

cat > init-db.sql << 'EOF'
-- Create databases for each service
CREATE DATABASE bizosaas_staging;
CREATE DATABASE plane_db;
CREATE DATABASE lago;
CREATE DATABASE authentik;
CREATE DATABASE temporal;

-- Create pgvector extension for RAG
\c bizosaas_staging;
CREATE EXTENSION IF NOT EXISTS vector;

-- Create tenant isolation function
CREATE OR REPLACE FUNCTION check_tenant_isolation()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.tenant_id IS NULL THEN
        RAISE EXCEPTION 'tenant_id cannot be NULL';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE bizosaas_staging TO admin;
GRANT ALL PRIVILEGES ON DATABASE plane_db TO admin;
GRANT ALL PRIVILEGES ON DATABASE lago TO admin;
GRANT ALL PRIVILEGES ON DATABASE authentik TO admin;
GRANT ALL PRIVILEGES ON DATABASE temporal TO admin;
EOF

echo -e "${GREEN}✓ Database initialization script created${NC}"

# Start services
echo ""
echo "🚀 Starting staging services..."

if [ "$1" == "--start" ]; then
    # Load environment variables
    if [ -f .env.staging ]; then
        export $(cat .env.staging | grep -v '^#' | xargs)
    fi
    
    docker-compose -f docker-compose.staging.yml up -d
    
    echo ""
    echo "Waiting for services to be healthy..."
    sleep 10
    
    # Initialize Vault
    ./init-vault.sh
    
    echo ""
    echo -e "${GREEN}✅ Staging environment is ready!${NC}"
    echo ""
    echo "Services:"
    echo "  PostgreSQL: localhost:5433"
    echo "  Redis: localhost:6380"
    echo "  Vault: http://localhost:8201"
    echo "  Temporal: localhost:7234"
    echo ""
    echo "Next steps:"
    echo "  1. Update .env.staging with actual secrets"
    echo "  2. Run database migrations"
    echo "  3. Seed test data"
else
    echo ""
    echo -e "${GREEN}✅ Staging environment configuration complete!${NC}"
    echo ""
    echo "To start the environment:"
    echo "  ./setup-staging-env.sh --start"
fi
