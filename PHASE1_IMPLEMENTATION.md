# Phase 1 Implementation - Immediate Actions

## Priority 1: Critical Backend Integration

### Task 1.1: Install Required Dependencies

```bash
# Navigate to brain-gateway
cd /home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway

# Install Python dependencies
pip install hvac alembic openai anthropic langchain pgvector psycopg2-binary

# Update requirements.txt
cat >> requirements.txt << EOF
hvac==2.1.0
alembic==1.13.1
openai==1.7.0
anthropic==0.8.0
langchain==0.1.0
pgvector==0.2.4
psycopg2-binary==2.9.9
EOF
```

### Task 1.2: Initialize Database Migrations

```bash
# Initialize Alembic
cd /home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway
alembic init migrations

# Create initial migration
alembic revision --autogenerate -m "Initial schema with audit logs and agent configs"

# Apply migrations
alembic upgrade head
```

### Task 1.3: Implement Vault Client

Create: `bizosaas-brain-core/brain-gateway/app/core/vault_client.py`

```python
import hvac
import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class VaultClient:
    """HashiCorp Vault client for secure secrets management"""
    
    def __init__(self):
        self.vault_addr = os.getenv('VAULT_ADDR', 'http://vault:8200')
        self.vault_token = os.getenv('VAULT_TOKEN', 'root')
        self.client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Vault client"""
        try:
            self.client = hvac.Client(
                url=self.vault_addr,
                token=self.vault_token
            )
            
            if not self.client.is_authenticated():
                raise Exception("Vault authentication failed")
            
            # Enable KV v2 secrets engine if not already enabled
            try:
                self.client.sys.enable_secrets_engine(
                    backend_type='kv',
                    path='secret',
                    options={'version': '2'}
                )
            except Exception:
                # Already enabled
                pass
                
            logger.info(f"Vault client initialized: {self.vault_addr}")
        except Exception as e:
            logger.error(f"Failed to initialize Vault client: {e}")
            raise
    
    def store_secret(self, path: str, secret: Dict[str, Any]) -> bool:
        """
        Store secret in Vault
        
        Args:
            path: Secret path (e.g., "tenants/123/api_keys/openai")
            secret: Secret data dictionary
        
        Returns:
            bool: True if successful
        """
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=secret,
                mount_point='secret'
            )
            logger.info(f"Secret stored: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to store secret at {path}: {e}")
            return False
    
    def get_secret(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve secret from Vault
        
        Args:
            path: Secret path
        
        Returns:
            Dict with secret data or None if not found
        """
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point='secret'
            )
            return response['data']['data']
        except Exception as e:
            logger.error(f"Failed to retrieve secret from {path}: {e}")
            return None
    
    def delete_secret(self, path: str) -> bool:
        """Delete secret from Vault"""
        try:
            self.client.secrets.kv.v2.delete_metadata_and_all_versions(
                path=path,
                mount_point='secret'
            )
            logger.info(f"Secret deleted: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete secret at {path}: {e}")
            return False
    
    def list_secrets(self, path: str) -> list:
        """List secrets at path"""
        try:
            response = self.client.secrets.kv.v2.list_secrets(
                path=path,
                mount_point='secret'
            )
            return response['data']['keys']
        except Exception as e:
            logger.error(f"Failed to list secrets at {path}: {e}")
            return []

# Singleton instance
vault_client = VaultClient()
```

### Task 1.4: Create Database Models

Create: `bizosaas-brain-core/brain-gateway/app/models/database.py`

```python
from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, Text, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(String(50), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(255))
    metadata = Column(JSONB)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ConnectorConfig(Base):
    __tablename__ = 'connector_configs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    connector_id = Column(String(50), nullable=False)
    vault_path = Column(String(255), nullable=False)  # Reference to Vault
    is_active = Column(Boolean, default=True)
    last_sync_at = Column(DateTime(timezone=True))
    sync_status = Column(String(20))
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AgentConfig(Base):
    __tablename__ = 'agent_configs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    agent_id = Column(String(50), nullable=False)
    system_prompt = Column(Text)
    temperature = Column(DECIMAL(3, 2), default=0.7)
    max_tokens = Column(Integer, default=2000)
    enabled_tools = Column(JSONB)
    llm_provider = Column(String(50), default='openai')
    llm_model = Column(String(100), default='gpt-4-turbo-preview')
    is_active = Column(Boolean, default=True)
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    agent_id = Column(String(50))
    content = Column(Text, nullable=False)
    # embedding will be added via pgvector extension
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### Task 1.5: Update Brain Gateway to Use Vault

Update: `bizosaas-brain-core/brain-gateway/app/api/vault.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.vault_client import vault_client
from app.core.auth import get_current_user
from typing import Dict, Any
from datetime import datetime

router = APIRouter(prefix="/vault", tags=["vault"])

class APIKeyData(BaseModel):
    service: str
    api_key: str
    metadata: Dict[str, Any] = {}

class SecretData(BaseModel):
    data: Dict[str, Any]

@router.post("/keys/{service}")
async def store_api_key(
    service: str,
    key_data: APIKeyData,
    current_user: dict = Depends(get_current_user)
):
    """Store API key in Vault (BYOK)"""
    tenant_id = current_user.get('tenant_id')
    user_id = current_user.get('id')
    
    vault_path = f"tenants/{tenant_id}/api_keys/{service}"
    
    secret = {
        "api_key": key_data.api_key,
        "service": service,
        "created_at": datetime.utcnow().isoformat(),
        "created_by": user_id,
        **key_data.metadata
    }
    
    success = vault_client.store_secret(vault_path, secret)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to store API key")
    
    # Store reference in database (not the actual key)
    # TODO: Add database record
    
    return {
        "status": "success",
        "service": service,
        "vault_path": vault_path
    }

@router.get("/keys/{service}")
async def get_api_key(
    service: str,
    current_user: dict = Depends(get_current_user)
):
    """Retrieve API key from Vault"""
    tenant_id = current_user.get('tenant_id')
    vault_path = f"tenants/{tenant_id}/api_keys/{service}"
    
    secret = vault_client.get_secret(vault_path)
    
    if not secret:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Don't return the actual key, just metadata
    return {
        "service": service,
        "created_at": secret.get('created_at'),
        "has_key": True
    }

@router.delete("/keys/{service}")
async def delete_api_key(
    service: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete API key from Vault"""
    tenant_id = current_user.get('tenant_id')
    vault_path = f"tenants/{tenant_id}/api_keys/{service}"
    
    success = vault_client.delete_secret(vault_path)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete API key")
    
    return {"status": "success", "service": service}

@router.get("/keys")
async def list_api_keys(current_user: dict = Depends(get_current_user)):
    """List all stored API keys for tenant"""
    tenant_id = current_user.get('tenant_id')
    vault_path = f"tenants/{tenant_id}/api_keys"
    
    keys = vault_client.list_secrets(vault_path)
    
    return {"keys": keys}
```

### Task 1.6: Test Vault Integration

```bash
# Test storing a secret
curl -X POST http://localhost:8000/vault/keys/openai \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "service": "openai",
    "api_key": "sk-test-key",
    "metadata": {"model": "gpt-4"}
  }'

# Test retrieving secret metadata
curl -X GET http://localhost:8000/vault/keys/openai \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Test listing keys
curl -X GET http://localhost:8000/vault/keys \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Verify in Vault directly
docker exec -it brain-vault vault kv get secret/tenants/YOUR_TENANT_ID/api_keys/openai
```

---

## Task 1.7: Wire Frontend BYOK Page

Update: `portals/client-portal/lib/brain-api.ts`

```typescript
export const brainApi = {
  // ... existing code ...
  
  vault: {
    async storeKey(service: string, apiKey: string, metadata: any = {}) {
      const res = await fetch(`${BRAIN_API}/vault/keys/${service}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${await getToken()}`
        },
        body: JSON.stringify({ service, api_key: apiKey, metadata })
      });
      
      if (!res.ok) throw new Error('Failed to store API key');
      return res.json();
    },
    
    async getKey(service: string) {
      const res = await fetch(`${BRAIN_API}/vault/keys/${service}`, {
        headers: {
          'Authorization': `Bearer ${await getToken()}`
        }
      });
      
      if (!res.ok) throw new Error('Failed to get API key');
      return res.json();
    },
    
    async deleteKey(service: string) {
      const res = await fetch(`${BRAIN_API}/vault/keys/${service}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${await getToken()}`
        }
      });
      
      if (!res.ok) throw new Error('Failed to delete API key');
      return res.json();
    },
    
    async listKeys() {
      const res = await fetch(`${BRAIN_API}/vault/keys`, {
        headers: {
          'Authorization': `Bearer ${await getToken()}`
        }
      });
      
      if (!res.ok) throw new Error('Failed to list API keys');
      return res.json();
    }
  }
};

async function getToken() {
  // Get JWT token from NextAuth session
  const session = await getSession();
  return session?.access_token || '';
}
```

Update: `portals/client-portal/app/ai-agents/byok/page.tsx`

```typescript
// Add actual API integration
const handleSaveKey = async (service: string, apiKey: string) => {
  try {
    setLoading(true);
    await brainApi.vault.storeKey(service, apiKey);
    toast.success(`${service} API key saved securely in Vault`);
    
    // Refresh key list
    await loadKeys();
  } catch (error) {
    toast.error('Failed to save API key');
    console.error(error);
  } finally {
    setLoading(false);
  }
};

const handleDeleteKey = async (service: string) => {
  try {
    setLoading(true);
    await brainApi.vault.deleteKey(service);
    toast.success(`${service} API key deleted`);
    
    // Refresh key list
    await loadKeys();
  } catch (error) {
    toast.error('Failed to delete API key');
    console.error(error);
  } finally {
    setLoading(false);
  }
};

const loadKeys = async () => {
  try {
    const { keys } = await brainApi.vault.listKeys();
    setStoredKeys(keys);
  } catch (error) {
    console.error('Failed to load keys:', error);
  }
};

useEffect(() => {
  loadKeys();
}, []);
```

---

## Testing Checklist for Phase 1

- [ ] Vault client initializes successfully
- [ ] Can store secret in Vault via API
- [ ] Can retrieve secret from Vault via API
- [ ] Can delete secret from Vault via API
- [ ] Can list secrets from Vault via API
- [ ] Frontend BYOK page can save OpenAI key
- [ ] Frontend BYOK page can save Anthropic key
- [ ] Frontend BYOK page can delete keys
- [ ] Frontend BYOK page shows stored keys
- [ ] Database migrations run successfully
- [ ] Audit log table created
- [ ] Agent config table created
- [ ] Knowledge base table created

---

## Estimated Time

- Task 1.1: 15 minutes
- Task 1.2: 30 minutes
- Task 1.3: 1 hour
- Task 1.4: 1 hour
- Task 1.5: 1 hour
- Task 1.6: 30 minutes
- Task 1.7: 1 hour

**Total**: ~5.5 hours

---

## Next Steps After Phase 1

1. Implement RAG service with pgvector
2. Implement LLM client for OpenAI/Anthropic
3. Wire AI agent chat to use real LLM
4. Implement connector data sync
5. Deploy Temporal workers

---

**Status**: Ready to begin  
**First Command**: Install dependencies
