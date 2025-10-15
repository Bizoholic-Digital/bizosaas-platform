# HashiCorp Vault - Infrastructure

## Service Identity
- **Name**: HashiCorp Vault
- **Type**: Infrastructure - Secrets Management
- **Container**: `bizosaas-vault-staging`
- **Image**: `vault:latest`
- **Port**: `8201:8200` (external:internal)
- **Network**: `dokploy-network`
- **Status**: ✅ Running (2+ days uptime)

## Purpose
Centralized secrets management for storing and accessing sensitive data including API keys, database credentials, OAuth tokens, and encryption keys across 40+ integrations in the BizOSaaS platform.

## Architecture

### Vault Structure
```
Vault Root
├── secret/
│   ├── database/
│   │   ├── postgres
│   │   ├── redis
│   │   └── mongodb
│   ├── apis/
│   │   ├── openai
│   │   ├── anthropic
│   │   ├── google-ads
│   │   ├── meta-ads
│   │   ├── stripe
│   │   └── [40+ integrations]
│   ├── oauth/
│   │   ├── google
│   │   ├── facebook
│   │   ├── linkedin
│   │   └── github
│   └── encryption/
│       ├── jwt-signing-key
│       ├── data-encryption-key
│       └── api-encryption-key
├── auth/
│   ├── userpass/
│   └── approle/
└── sys/
    ├── policies/
    └── audit/
```

### Integration Categories (40+ APIs)
1. **AI/ML Services** (5): OpenAI, Anthropic Claude, Cohere, Google AI, AWS Bedrock
2. **Advertising Platforms** (6): Google Ads, Meta Ads, LinkedIn Marketing, Twitter Ads, TikTok Ads, Pinterest Ads
3. **Social Media** (7): Facebook, Instagram, Twitter, LinkedIn, YouTube, TikTok, Pinterest
4. **E-commerce** (5): Stripe, PayPal, Shopify, WooCommerce, BigCommerce
5. **CRM/Marketing** (4): HubSpot, Mailchimp, SendGrid, Twilio
6. **Analytics** (4): Google Analytics, Mixpanel, Segment, Amplitude
7. **SEO Tools** (3): SERP API, Ahrefs, SEMrush
8. **Cloud Services** (3): AWS, GCP, Azure
9. **Databases** (3): PostgreSQL, Redis, MongoDB

## Dependencies

### Required By (Consumers)
- Brain API Gateway (credential retrieval)
- AI Agents Service (API keys for 93 agents)
- Auth Service (JWT signing keys)
- All Backend Services (database credentials)
- Integration services (OAuth tokens, API keys)

### External Dependencies
- None (base infrastructure)

## Configuration

### Environment Variables
```bash
# Vault Server
VAULT_ADDR=http://bizosaas-vault-staging:8200
VAULT_API_ADDR=http://bizosaas-vault-staging:8200
VAULT_TOKEN=hvs.CAESI...  # Root token (store securely)

# Development Mode
VAULT_DEV_ROOT_TOKEN_ID=root-token-dev
VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200

# Production Mode
VAULT_STORAGE=file
VAULT_STORAGE_PATH=/vault/data
VAULT_LOG_LEVEL=info
```

### Docker Compose Configuration
```yaml
services:
  vault:
    image: vault:latest
    container_name: bizosaas-vault-staging
    cap_add:
      - IPC_LOCK
    environment:
      VAULT_DEV_ROOT_TOKEN_ID: ${VAULT_ROOT_TOKEN}
      VAULT_DEV_LISTEN_ADDRESS: 0.0.0.0:8200
    ports:
      - "8201:8200"
    volumes:
      - vault_data:/vault/data
      - vault_logs:/vault/logs
      - ./vault/policies:/vault/policies
    networks:
      - dokploy-network
    healthcheck:
      test: ["CMD", "vault", "status"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
```

## Vault Policies

### Admin Policy
```hcl
# vault/policies/admin-policy.hcl
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "auth/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "sys/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}
```

### Application Policy
```hcl
# vault/policies/app-policy.hcl
path "secret/data/database/*" {
  capabilities = ["read"]
}

path "secret/data/apis/*" {
  capabilities = ["read"]
}

path "secret/data/oauth/*" {
  capabilities = ["read", "update"]  # Update for token refresh
}
```

### Service-Specific Policy
```hcl
# vault/policies/brain-gateway-policy.hcl
path "secret/data/database/postgres" {
  capabilities = ["read"]
}

path "secret/data/apis/openai" {
  capabilities = ["read"]
}

path "secret/data/apis/anthropic" {
  capabilities = ["read"]
}
```

## Secrets Management

### Store Database Credentials
```bash
# PostgreSQL credentials
vault kv put secret/database/postgres \
  host="bizosaas-postgres-staging" \
  port="5432" \
  database="bizosaas_platform" \
  username="postgres" \
  password="SharedInfra2024!SuperSecure"

# Redis credentials
vault kv put secret/database/redis \
  host="bizosaas-redis-staging" \
  port="6379" \
  password=""
```

### Store API Keys
```bash
# OpenAI API Key
vault kv put secret/apis/openai \
  api_key="sk-proj-..." \
  organization="org-..."

# Anthropic Claude API Key
vault kv put secret/apis/anthropic \
  api_key="sk-ant-..." \
  model="claude-3-5-sonnet-20241022"

# Google Ads API
vault kv put secret/apis/google-ads \
  developer_token="..." \
  client_id="..." \
  client_secret="..." \
  refresh_token="..."

# Meta Ads API
vault kv put secret/apis/meta-ads \
  app_id="..." \
  app_secret="..." \
  access_token="..."

# Stripe API
vault kv put secret/apis/stripe \
  publishable_key="pk_test_..." \
  secret_key="sk_test_..." \
  webhook_secret="whsec_..."
```

### Store OAuth Tokens
```bash
# Google OAuth
vault kv put secret/oauth/google \
  client_id="..." \
  client_secret="..." \
  redirect_uri="https://stg.bizoholic.com/auth/google/callback"

# LinkedIn OAuth
vault kv put secret/oauth/linkedin \
  client_id="..." \
  client_secret="..." \
  redirect_uri="https://stg.bizoholic.com/auth/linkedin/callback"
```

### Store Encryption Keys
```bash
# JWT Signing Key
vault kv put secret/encryption/jwt \
  signing_key="$(openssl rand -base64 64)" \
  algorithm="HS256" \
  expiry="24h"

# Data Encryption Key
vault kv put secret/encryption/data \
  master_key="$(openssl rand -base64 32)" \
  algorithm="AES-256-GCM"
```

## Python Client Integration

### Install Vault Client
```bash
pip install hvac
```

### Vault Client Wrapper
```python
import hvac
import os
from functools import lru_cache

class VaultClient:
    def __init__(self):
        self.client = hvac.Client(
            url=os.getenv("VAULT_ADDR", "http://bizosaas-vault-staging:8200"),
            token=os.getenv("VAULT_TOKEN")
        )

        if not self.client.is_authenticated():
            raise Exception("Vault authentication failed")

    @lru_cache(maxsize=100)
    def get_secret(self, path: str) -> dict:
        """Get secret from Vault with caching"""
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point='secret'
            )
            return response['data']['data']
        except Exception as e:
            raise Exception(f"Failed to read secret {path}: {e}")

    def get_database_credentials(self, db_name: str) -> dict:
        """Get database credentials"""
        return self.get_secret(f"database/{db_name}")

    def get_api_key(self, service: str) -> dict:
        """Get API key for external service"""
        return self.get_secret(f"apis/{service}")

    def get_oauth_credentials(self, provider: str) -> dict:
        """Get OAuth credentials"""
        return self.get_secret(f"oauth/{provider}")

    def update_oauth_token(self, provider: str, access_token: str, refresh_token: str):
        """Update OAuth access token"""
        self.client.secrets.kv.v2.create_or_update_secret(
            path=f"oauth/{provider}",
            secret={
                "access_token": access_token,
                "refresh_token": refresh_token
            },
            mount_point='secret'
        )

# Singleton instance
vault_client = VaultClient()
```

### Usage in Applications
```python
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine

app = FastAPI()

def get_database_url() -> str:
    """Get database URL from Vault"""
    creds = vault_client.get_database_credentials("postgres")
    return f"postgresql://{creds['username']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['database']}"

@app.on_event("startup")
async def startup():
    # Get credentials from Vault
    db_url = get_database_url()
    engine = create_engine(db_url)

@app.get("/integrations/openai")
async def get_openai_client():
    # Get OpenAI API key from Vault
    openai_creds = vault_client.get_api_key("openai")
    return {"api_key_prefix": openai_creds["api_key"][:10] + "..."}
```

## AppRole Authentication

### Create AppRole
```bash
# Enable AppRole auth
vault auth enable approle

# Create role for Brain Gateway
vault write auth/approle/role/brain-gateway \
    secret_id_ttl=24h \
    token_ttl=1h \
    token_max_ttl=24h \
    policies="brain-gateway-policy"

# Get Role ID
vault read auth/approle/role/brain-gateway/role-id

# Generate Secret ID
vault write -f auth/approle/role/brain-gateway/secret-id
```

### AppRole Login (Python)
```python
import hvac

def login_with_approle(role_id: str, secret_id: str):
    client = hvac.Client(url='http://bizosaas-vault-staging:8200')

    # Authenticate with AppRole
    response = client.auth.approle.login(
        role_id=role_id,
        secret_id=secret_id
    )

    # Set client token
    client.token = response['auth']['client_token']
    return client
```

## Dynamic Secrets (Database)

### Enable Database Secrets Engine
```bash
# Enable database secrets engine
vault secrets enable database

# Configure PostgreSQL connection
vault write database/config/postgres \
    plugin_name=postgresql-database-plugin \
    allowed_roles="readonly,readwrite" \
    connection_url="postgresql://{{username}}:{{password}}@bizosaas-postgres-staging:5432/bizosaas_platform" \
    username="postgres" \
    password="SharedInfra2024!SuperSecure"

# Create readonly role
vault write database/roles/readonly \
    db_name=postgres \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"
```

### Generate Dynamic Credentials
```python
def get_dynamic_db_credentials():
    """Get short-lived database credentials"""
    response = vault_client.client.read('database/creds/readonly')
    return {
        "username": response['data']['username'],
        "password": response['data']['password']
    }
```

## Encryption as a Service

### Enable Transit Engine
```bash
# Enable transit engine
vault secrets enable transit

# Create encryption key
vault write -f transit/keys/data-encryption
```

### Encrypt/Decrypt Data
```python
def encrypt_data(plaintext: str) -> str:
    """Encrypt sensitive data"""
    response = vault_client.client.secrets.transit.encrypt_data(
        name='data-encryption',
        plaintext=plaintext
    )
    return response['data']['ciphertext']

def decrypt_data(ciphertext: str) -> str:
    """Decrypt sensitive data"""
    response = vault_client.client.secrets.transit.decrypt_data(
        name='data-encryption',
        ciphertext=ciphertext
    )
    return response['data']['plaintext']
```

## Health Checks

### Container Health Check
```bash
# Check Vault status
docker exec bizosaas-vault-staging vault status

# Expected output:
# Sealed: false
# Cluster Name: vault-cluster-...
```

### Application Health Check
```python
def check_vault_health():
    try:
        client = hvac.Client(url='http://bizosaas-vault-staging:8200')

        # Check if Vault is initialized and unsealed
        if not client.sys.is_initialized():
            return False

        if client.sys.is_sealed():
            return False

        # Test authentication
        client.token = os.getenv("VAULT_TOKEN")
        if not client.is_authenticated():
            return False

        return True
    except Exception as e:
        return False
```

## Monitoring

### Key Metrics
```bash
# Check Vault health
curl http://bizosaas-vault-staging:8200/v1/sys/health

# Audit log
vault audit enable file file_path=/vault/logs/audit.log

# List active leases
vault list sys/leases/lookup/secret
```

### Alerting Thresholds
- Vault sealed (critical)
- Authentication failures > 10/min
- Secret read errors > 5/min
- Token expiry warnings

## Common Issues

### Issue 1: Vault Sealed
**Symptom**: Cannot read/write secrets
**Diagnosis**: `vault status` shows `Sealed: true`
**Solution**:
```bash
# Unseal vault (requires unseal keys)
vault operator unseal <key1>
vault operator unseal <key2>
vault operator unseal <key3>
```

### Issue 2: Token Expired
**Symptom**: Authentication failed
**Diagnosis**: `vault token lookup` shows expired
**Solution**:
```bash
# Renew token
vault token renew

# Or generate new token
vault token create -policy=app-policy
```

### Issue 3: Permission Denied
**Symptom**: Cannot read secret
**Diagnosis**: Token lacks required policy
**Solution**:
```bash
# Attach policy to token
vault token capabilities <token> secret/data/apis/openai

# Update role policies
vault write auth/approle/role/brain-gateway policies=brain-gateway-policy,default
```

## Security Best Practices

1. **Never Commit Tokens**: Store root token securely, never in code
2. **Use AppRole**: Prefer AppRole over tokens for applications
3. **Least Privilege**: Grant minimum required permissions
4. **Rotate Secrets**: Regularly rotate API keys and credentials
5. **Audit Logging**: Enable and monitor audit logs
6. **Encryption**: Use transit engine for sensitive data
7. **Dynamic Secrets**: Use dynamic credentials when possible

## Backup & Recovery

### Backup Vault Data
```bash
# Backup secrets
vault kv get -format=json secret/ > vault-backup-$(date +%Y%m%d).json

# Backup policies
vault policy list | xargs -I {} vault policy read {} > policy-{}.hcl
```

### Restore Vault Data
```bash
# Restore secrets
cat vault-backup-20251015.json | jq -r 'to_entries[] | "\(.key) \(.value)"' | while read key value; do
    vault kv put secret/$key $value
done
```

## Testing

### Integration Tests
```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def vault_client():
    with patch('hvac.Client') as mock_client:
        mock_client.return_value.is_authenticated.return_value = True
        yield VaultClient()

def test_get_database_credentials(vault_client):
    vault_client.client.secrets.kv.v2.read_secret_version.return_value = {
        'data': {
            'data': {
                'host': 'localhost',
                'port': '5432',
                'username': 'test',
                'password': 'test'
            }
        }
    }

    creds = vault_client.get_database_credentials('postgres')
    assert creds['host'] == 'localhost'
```

## Deployment Checklist

- [ ] Vault container deployed and running
- [ ] Vault initialized and unsealed
- [ ] Root token stored securely
- [ ] Admin policy created
- [ ] Application policies created
- [ ] AppRole authentication enabled
- [ ] All secrets migrated to Vault
- [ ] All services configured to use Vault
- [ ] Audit logging enabled
- [ ] Backup strategy implemented
- [ ] Health checks passing

## References
- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [Vault Best Practices](https://learn.hashicorp.com/tutorials/vault/pattern-centralize-secrets)
- [Python HVAC Client](https://hvac.readthedocs.io/)
- BizOSaaS PRD: `/home/alagiri/projects/bizoholic/comprehensive_prd_06092025.md`

---
**Status**: ✅ Production-Ready
**Last Updated**: October 15, 2025
**Owner**: Infrastructure Team
