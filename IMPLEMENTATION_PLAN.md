# BizOSaaS Platform - Complete Implementation & Testing Plan

**Date**: 2025-12-06  
**Objective**: Complete all features, test thoroughly, containerize, and deploy to production

---

## Executive Summary

### Current Status vs. Architecture Requirements

| Component | Architecture V2 Requirement | Current Status | Gap |
|-----------|---------------------------|----------------|-----|
| **Brain Gateway** | Port 8000, AI Orchestrator | ✅ Running | ⚠️ Vault integration pending |
| **Client Portal** | Port 3003, Control Plane | ✅ Running | ⚠️ Live data wiring needed |
| **Auth Service** | Port 8009, SSO with fastapi-sso | ✅ Running | ⚠️ SSO upgrade needed |
| **Redis** | Caching, Message Broker | ✅ Running | ✅ Complete |
| **PostgreSQL** | User/Tenant/Config storage | ✅ Running | ⚠️ Schema migrations needed |
| **HashiCorp Vault** | Secrets management (SOC2) | ✅ Running | ❌ Not integrated |
| **Temporal** | Workflow orchestration | ✅ Running | ⚠️ Workers not deployed |
| **Observability** | Grafana + Loki + Prometheus | ✅ Running | ✅ Complete |
| **Connectors** | 13 connectors | ✅ Implemented | ⚠️ UI wiring incomplete |
| **AI Agents** | 7 core + 93 scalable | ✅ Framework ready | ❌ RAG/LLM not integrated |

---

## Phase 1: Critical Backend Integration (Priority 1)

### 1.1 HashiCorp Vault Integration

**Status**: ❌ **NOT IMPLEMENTED**  
**Priority**: 🔴 **CRITICAL** (SOC2 requirement)

**Implementation Tasks**:

```python
# File: bizosaas-brain-core/brain-gateway/app/core/vault_client.py

import hvac
import os
from typing import Optional, Dict

class VaultClient:
    def __init__(self):
        self.client = hvac.Client(
            url=os.getenv('VAULT_ADDR', 'http://vault:8200'),
            token=os.getenv('VAULT_TOKEN', 'root')
        )
        
    def store_secret(self, path: str, secret: Dict) -> bool:
        """Store secret in Vault"""
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=secret
            )
            return True
        except Exception as e:
            logger.error(f"Failed to store secret: {e}")
            return False
    
    def get_secret(self, path: str) -> Optional[Dict]:
        """Retrieve secret from Vault"""
        try:
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            return response['data']['data']
        except Exception as e:
            logger.error(f"Failed to retrieve secret: {e}")
            return None

# Singleton instance
vault_client = VaultClient()
```

**Integration Points**:
1. Connector credentials storage
2. OpenAI/Anthropic API keys
3. OAuth tokens
4. Database passwords

**Testing**:
- [ ] Store test secret in Vault
- [ ] Retrieve secret from Vault
- [ ] Update connector to use Vault for credentials
- [ ] Verify no plaintext secrets in database

---

### 1.2 Temporal Workers Deployment

**Status**: ⚠️ **PARTIALLY IMPLEMENTED**  
**Priority**: 🔴 **HIGH**

**Current Gap**: Temporal server is running but no workers are deployed to execute workflows.

**Implementation Tasks**:

```python
# File: bizosaas-brain-core/temporal-worker/worker.py

from temporalio.client import Client
from temporalio.worker import Worker
from workflows.connector_sync import ConnectorSyncWorkflow
from activities.data_sync import sync_wordpress_posts, sync_zoho_contacts

async def main():
    client = await Client.connect("temporal:7233")
    
    worker = Worker(
        client,
        task_queue="bizosaas-main",
        workflows=[ConnectorSyncWorkflow],
        activities=[
            sync_wordpress_posts,
            sync_zoho_contacts,
            # Add all connector sync activities
        ]
    )
    
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
```

**Dockerfile**:
```dockerfile
# File: bizosaas-brain-core/temporal-worker/Dockerfile

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "worker.py"]
```

**Testing**:
- [ ] Deploy worker container
- [ ] Trigger test workflow from UI
- [ ] Verify workflow execution in Temporal UI
- [ ] Check activity logs

---

### 1.3 Database Schema & Migrations

**Status**: ⚠️ **INCOMPLETE**  
**Priority**: 🔴 **HIGH**

**Required Tables**:

```sql
-- Audit Logging
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    user_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(255),
    metadata JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Connector Configurations (Vault references only)
CREATE TABLE connector_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    connector_id VARCHAR(50) NOT NULL,
    vault_path VARCHAR(255) NOT NULL, -- Reference to Vault secret
    is_active BOOLEAN DEFAULT true,
    last_sync_at TIMESTAMP,
    sync_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- AI Agent Configurations
CREATE TABLE agent_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    agent_id VARCHAR(50) NOT NULL,
    system_prompt TEXT,
    temperature DECIMAL(3,2) DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 2000,
    enabled_tools JSONB,
    llm_provider VARCHAR(50) DEFAULT 'openai',
    llm_model VARCHAR(100) DEFAULT 'gpt-4-turbo-preview',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Knowledge Base for RAG
CREATE TABLE knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    agent_id VARCHAR(50),
    content TEXT NOT NULL,
    embedding vector(1536), -- pgvector
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_knowledge_embedding ON knowledge_base USING ivfflat (embedding vector_cosine_ops);
```

**Migration Tool**: Use Alembic

```bash
# Install
pip install alembic

# Initialize
cd bizosaas-brain-core/brain-gateway
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Add audit logs and agent configs"

# Apply
alembic upgrade head
```

**Testing**:
- [ ] Run migrations on local database
- [ ] Verify all tables created
- [ ] Test CRUD operations
- [ ] Verify tenant isolation

---

## Phase 2: Frontend-Backend Wiring (Priority 2)

### 2.1 Connector Data Sync

**Current Status**: UI shows mock data  
**Required**: Wire to live backend data

**Implementation**:

```typescript
// File: portals/client-portal/lib/brain-api.ts

export const brainApi = {
  connectors: {
    async list() {
      const res = await fetch(`${BRAIN_API}/connectors`);
      return res.json();
    },
    
    async get(connectorId: string) {
      const res = await fetch(`${BRAIN_API}/connectors/${connectorId}`);
      return res.json();
    },
    
    async connect(connectorId: string, credentials: any) {
      const res = await fetch(`${BRAIN_API}/connectors/${connectorId}/connect`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      });
      return res.json();
    },
    
    async sync(connectorId: string, resourceType: string) {
      const res = await fetch(`${BRAIN_API}/connectors/${connectorId}/sync/${resourceType}`, {
        method: 'POST'
      });
      return res.json();
    },
    
    async getData(connectorId: string, resourceType: string, params?: any) {
      const query = new URLSearchParams(params).toString();
      const res = await fetch(`${BRAIN_API}/connectors/${connectorId}/data/${resourceType}?${query}`);
      return res.json();
    }
  }
};
```

**Update Components**:

```typescript
// File: portals/client-portal/components/CMSContent.tsx

export function CMSContent() {
  const [pages, setPages] = useState([]);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    async function fetchData() {
      try {
        // Get WordPress connector data
        const pagesData = await brainApi.connectors.getData('wordpress', 'pages');
        const postsData = await brainApi.connectors.getData('wordpress', 'posts');
        
        setPages(pagesData.items || []);
        setPosts(postsData.items || []);
      } catch (error) {
        console.error('Failed to fetch CMS data:', error);
      } finally {
        setLoading(false);
      }
    }
    
    fetchData();
  }, []);
  
  // ... rest of component
}
```

**Testing Checklist**:
- [ ] CMS Tab - Pages (WordPress)
- [ ] CMS Tab - Posts (WordPress)
- [ ] CMS Tab - Media (WordPress)
- [ ] CRM Tab - Contacts (Zoho/FluentCRM)
- [ ] CRM Tab - Leads (Zoho)
- [ ] CRM Tab - Deals (Zoho)
- [ ] E-commerce Tab - Products (Shopify/WooCommerce)
- [ ] E-commerce Tab - Orders (Shopify/WooCommerce)
- [ ] E-commerce Tab - Customers (Shopify/WooCommerce)
- [ ] Marketing Tab - Campaigns (Google Ads/Facebook)
- [ ] Analytics Tab - Traffic (Google Analytics)

---

### 2.2 AI Agent Configuration UI

**Current Status**: UI exists but not connected to backend  
**Required**: Save/load agent configurations

**Backend API**:

```python
# File: bizosaas-brain-core/brain-gateway/app/api/agents.py

@router.put("/agents/{agent_id}/config")
async def update_agent_config(
    agent_id: str,
    config: AgentConfigUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update agent configuration"""
    # Save to database
    await db.agent_configs.update(
        agent_id=agent_id,
        tenant_id=current_user.tenant_id,
        system_prompt=config.system_prompt,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        enabled_tools=config.enabled_tools,
        llm_provider=config.llm_provider,
        llm_model=config.llm_model
    )
    
    return {"status": "success"}

@router.get("/agents/{agent_id}/config")
async def get_agent_config(
    agent_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get agent configuration"""
    config = await db.agent_configs.get(
        agent_id=agent_id,
        tenant_id=current_user.tenant_id
    )
    return config
```

**Frontend Integration**:

```typescript
// File: portals/client-portal/app/ai-agents/[agentId]/page.tsx

const handleSaveConfig = async () => {
  try {
    await brainApi.agents.updateConfig(agentId, {
      system_prompt: systemPrompt,
      temperature,
      max_tokens: maxTokens,
      enabled_tools: selectedTools,
      llm_provider: selectedProvider,
      llm_model: selectedModel
    });
    
    toast.success('Agent configuration saved');
  } catch (error) {
    toast.error('Failed to save configuration');
  }
};
```

**Testing**:
- [ ] Load existing agent config
- [ ] Update system prompt
- [ ] Change temperature/tokens
- [ ] Toggle tools on/off
- [ ] Save configuration
- [ ] Verify persistence after reload

---

### 2.3 BYOK (Bring Your Own Key) Integration

**Current Status**: UI exists (`/ai-agents/byok`)  
**Required**: Store keys in Vault, use in AI calls

**Implementation**:

```typescript
// Frontend: portals/client-portal/app/ai-agents/byok/page.tsx

const handleSaveKey = async (service: string, apiKey: string) => {
  try {
    await brainApi.vault.storeKey(service, apiKey);
    toast.success(`${service} API key saved securely`);
  } catch (error) {
    toast.error('Failed to save API key');
  }
};
```

```python
# Backend: bizosaas-brain-core/brain-gateway/app/api/vault.py

@router.post("/vault/keys/{service}")
async def store_api_key(
    service: str,
    key_data: APIKeyData,
    current_user: User = Depends(get_current_user)
):
    """Store API key in Vault"""
    vault_path = f"tenants/{current_user.tenant_id}/api_keys/{service}"
    
    success = vault_client.store_secret(vault_path, {
        "api_key": key_data.api_key,
        "created_at": datetime.utcnow().isoformat(),
        "created_by": current_user.id
    })
    
    if success:
        # Store reference in database
        await db.api_key_refs.create(
            tenant_id=current_user.tenant_id,
            service=service,
            vault_path=vault_path
        )
    
    return {"status": "success" if success else "failed"}
```

**Testing**:
- [ ] Add OpenAI key
- [ ] Add Anthropic key
- [ ] Add OpenRouter key
- [ ] Verify keys stored in Vault (not DB)
- [ ] Test AI agent using stored key
- [ ] Revoke key
- [ ] Verify key deletion

---

## Phase 3: AI Agent & RAG Implementation (Priority 3)

### 3.1 RAG Service Integration

**Current Status**: Skeleton exists in `rag.py`  
**Required**: Full implementation with pgvector

**Implementation**:

```python
# File: bizosaas-brain-core/brain-gateway/app/core/rag.py

from openai import OpenAI
import numpy as np
from typing import List, Dict, Any

class RAGService:
    def __init__(self):
        self.vector_store_url = os.getenv("DATABASE_URL")
        self.openai_client = None
        
    async def initialize(self, api_key: str):
        """Initialize with API key from Vault"""
        self.openai_client = OpenAI(api_key=api_key)
    
    async def ingest_document(self, content: str, metadata: Dict[str, Any], tenant_id: str, agent_id: str = None):
        """Chunk, embed, and store document"""
        # 1. Chunk text
        chunks = self._chunk_text(content, chunk_size=500, overlap=50)
        
        # 2. Generate embeddings
        embeddings = await self._generate_embeddings(chunks)
        
        # 3. Store in pgvector
        for chunk, embedding in zip(chunks, embeddings):
            await db.knowledge_base.create(
                tenant_id=tenant_id,
                agent_id=agent_id,
                content=chunk,
                embedding=embedding,
                metadata=metadata
            )
        
        return len(chunks)
    
    async def retrieve_context(self, query: str, tenant_id: str, agent_id: str = None, limit: int = 5) -> List[str]:
        """Retrieve relevant context for query"""
        # 1. Embed query
        query_embedding = await self._generate_embeddings([query])
        
        # 2. Similarity search
        results = await db.knowledge_base.search_similar(
            embedding=query_embedding[0],
            tenant_id=tenant_id,
            agent_id=agent_id,
            limit=limit
        )
        
        return [r['content'] for r in results]
    
    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    async def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI"""
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        
        return [item.embedding for item in response.data]
```

**Testing**:
- [ ] Upload PDF document
- [ ] Verify chunking
- [ ] Verify embeddings generated
- [ ] Verify storage in pgvector
- [ ] Test similarity search
- [ ] Test retrieval in agent chat

---

### 3.2 LLM Integration (OpenRouter/OpenAI)

**Implementation**:

```python
# File: bizosaas-brain-core/brain-gateway/app/core/llm_client.py

from openai import OpenAI
from typing import List, Dict, Optional

class LLMClient:
    def __init__(self):
        self.clients = {}
    
    async def initialize_provider(self, provider: str, api_key: str):
        """Initialize LLM provider"""
        if provider == 'openai':
            self.clients[provider] = OpenAI(api_key=api_key)
        elif provider == 'openrouter':
            self.clients[provider] = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )
        elif provider == 'anthropic':
            # Use Anthropic SDK
            pass
    
    async def chat_completion(
        self,
        provider: str,
        model: str,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        context: Optional[List[str]] = None
    ) -> str:
        """Generate chat completion with optional RAG context"""
        
        # Inject RAG context if provided
        if context:
            context_message = {
                "role": "system",
                "content": f"Use the following context to answer:\\n\\n{' '.join(context)}"
            }
            messages = [context_message] + messages
        
        client = self.clients.get(provider)
        if not client:
            raise ValueError(f"Provider {provider} not initialized")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content

llm_client = LLMClient()
```

**Update Agent Chat**:

```python
# File: bizosaas-brain-core/brain-gateway/app/api/agents.py

@router.post("/agents/{agent_id}/chat")
async def agent_chat(
    agent_id: str,
    message: ChatMessage,
    current_user: User = Depends(get_current_user)
):
    """Chat with AI agent using RAG + LLM"""
    
    # 1. Get agent config
    config = await db.agent_configs.get(agent_id, current_user.tenant_id)
    
    # 2. Get API key from Vault
    api_key = await vault_client.get_secret(
        f"tenants/{current_user.tenant_id}/api_keys/{config.llm_provider}"
    )
    
    # 3. Initialize LLM
    await llm_client.initialize_provider(config.llm_provider, api_key['api_key'])
    
    # 4. Retrieve RAG context
    context = await rag_service.retrieve_context(
        query=message.content,
        tenant_id=current_user.tenant_id,
        agent_id=agent_id
    )
    
    # 5. Generate response
    response = await llm_client.chat_completion(
        provider=config.llm_provider,
        model=config.llm_model,
        messages=[
            {"role": "system", "content": config.system_prompt},
            {"role": "user", "content": message.content}
        ],
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        context=context
    )
    
    return {"response": response}
```

**Testing**:
- [ ] Chat with agent (no RAG)
- [ ] Upload knowledge base
- [ ] Chat with agent (with RAG)
- [ ] Verify context retrieval
- [ ] Test different LLM providers
- [ ] Test different models
- [ ] Test temperature variations

---

## Phase 4: Comprehensive UI Testing (Priority 4)

### 4.1 Navigation & Layout Testing

**Test Matrix**:

| Page/Tab | Sub-Tab | Action | Expected Result | Status |
|----------|---------|--------|-----------------|--------|
| `/` | - | Load | Redirect to /login or /dashboard | ⬜ |
| `/login` | - | Credentials login | Redirect to /dashboard | ⬜ |
| `/login` | - | GitHub OAuth | Redirect to /dashboard | ⬜ |
| `/login` | - | Google OAuth | Redirect to /dashboard | ⬜ |
| `/login` | - | Microsoft OAuth | Redirect to /dashboard | ⬜ |
| `/dashboard` | Overview | Load | Show metrics cards | ⬜ |
| `/dashboard` | Overview | Refresh | Update metrics | ⬜ |
| `/ai-agents` | List | Load | Show all agents | ⬜ |
| `/ai-agents` | List | Click agent | Navigate to agent detail | ⬜ |
| `/ai-agents/[id]` | Chat | Send message | Get AI response | ⬜ |
| `/ai-agents/[id]` | Basic | Update name | Save successfully | ⬜ |
| `/ai-agents/[id]` | System Prompt | Update prompt | Save successfully | ⬜ |
| `/ai-agents/[id]` | Fine-Tuning | Add instruction | Save successfully | ⬜ |
| `/ai-agents/[id]` | LLM Config | Change temperature | Save successfully | ⬜ |
| `/ai-agents/[id]` | LLM Config | Change model | Save successfully | ⬜ |
| `/ai-agents/[id]` | Tools | Toggle tool | Save successfully | ⬜ |
| `/ai-agents/[id]` | APIs | View required APIs | Show list | ⬜ |
| `/ai-agents/[id]` | Permissions | Set access | Save successfully | ⬜ |
| `/ai-agents/byok` | - | Add OpenAI key | Store in Vault | ⬜ |
| `/ai-agents/byok` | - | Add Anthropic key | Store in Vault | ⬜ |
| `/ai-agents/byok` | - | Test key | Verify connection | ⬜ |
| `/ai-agents/byok` | - | Revoke key | Delete from Vault | ⬜ |
| `/dashboard/connectors` | List | Load | Show 13 connectors | ⬜ |
| `/dashboard/connectors` | List | Click connector | Navigate to config | ⬜ |
| `/dashboard/connectors/wordpress` | - | Connect | OAuth flow | ⬜ |
| `/dashboard/connectors/wordpress` | - | Sync | Trigger workflow | ⬜ |
| `/dashboard/connectors/zoho` | - | Connect | OAuth flow | ⬜ |
| `/dashboard/connectors/shopify` | - | Connect | OAuth flow | ⬜ |
| `/content/pages` | - | Load | Show WordPress pages | ⬜ |
| `/content/pages` | - | Create | Create new page | ⬜ |
| `/content/pages` | - | Edit | Update page | ⬜ |
| `/content/pages` | - | Delete | Remove page | ⬜ |
| `/content/posts` | - | Load | Show WordPress posts | ⬜ |
| `/content/posts` | - | Create | Create new post | ⬜ |
| `/content/media` | - | Load | Show media library | ⬜ |
| `/content/media` | - | Upload | Upload file | ⬜ |
| `/crm/contacts` | - | Load | Show Zoho contacts | ⬜ |
| `/crm/contacts` | - | Create | Create contact | ⬜ |
| `/crm/contacts` | - | Edit | Update contact | ⬜ |
| `/crm/leads` | - | Load | Show leads | ⬜ |
| `/crm/deals` | - | Load | Show deals | ⬜ |
| `/ecommerce/products` | - | Load | Show Shopify products | ⬜ |
| `/ecommerce/products` | - | Create | Create product | ⬜ |
| `/ecommerce/orders` | - | Load | Show orders | ⬜ |
| `/ecommerce/customers` | - | Load | Show customers | ⬜ |
| `/marketing/campaigns` | - | Load | Show campaigns | ⬜ |
| `/marketing/campaigns` | - | Create | Create campaign | ⬜ |
| `/analytics` | - | Load | Show analytics data | ⬜ |
| `/analytics` | - | Filter by date | Update charts | ⬜ |
| `/settings` | Profile | Update | Save changes | ⬜ |
| `/settings` | Integrations | View webhooks | Show list | ⬜ |
| `/settings` | Billing | View plan | Show details | ⬜ |

---

### 4.2 Error Handling Testing

**Test Scenarios**:

| Scenario | Expected Behavior | Status |
|----------|-------------------|--------|
| API timeout | Show error toast, retry option | ⬜ |
| 401 Unauthorized | Redirect to login | ⬜ |
| 403 Forbidden | Show permission error | ⬜ |
| 404 Not Found | Show not found page | ⬜ |
| 500 Server Error | Show error page with support link | ⬜ |
| Network offline | Show offline indicator | ⬜ |
| Invalid form input | Show validation errors | ⬜ |
| Duplicate entry | Show conflict error | ⬜ |
| Rate limit exceeded | Show rate limit message | ⬜ |

---

### 4.3 Performance Testing

**Metrics to Track**:

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Page Load Time (Dashboard) | < 2s | TBD | ⬜ |
| API Response Time (List) | < 500ms | TBD | ⬜ |
| API Response Time (Detail) | < 300ms | TBD | ⬜ |
| AI Chat Response Time | < 5s | TBD | ⬜ |
| Connector Sync Time | < 30s | TBD | ⬜ |
| Database Query Time | < 100ms | TBD | ⬜ |
| Memory Usage (Frontend) | < 100MB | TBD | ⬜ |
| Memory Usage (Backend) | < 512MB | TBD | ⬜ |

---

## Phase 5: Containerization & Deployment (Priority 5)

### 5.1 Production Docker Configuration

**Update docker-compose.yml for production**:

```yaml
# File: bizosaas-brain-core/docker-compose.prod.yml

version: '3.8'

services:
  postgres:
    image: ankane/pgvector:v0.5.1
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: unless-stopped
    
  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    restart: unless-stopped
    
  vault:
    image: hashicorp/vault:latest
    environment:
      VAULT_ADDR: ${VAULT_ADDR}
    volumes:
      - vault-data:/vault/data
      - ./vault-config.hcl:/vault/config/vault.hcl
    cap_add:
      - IPC_LOCK
    restart: unless-stopped
    
  temporal:
    image: temporalio/auto-setup:latest
    environment:
      - DB=postgresql
      - POSTGRES_SEEDS=postgres
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PWD=${POSTGRES_PASSWORD}
    depends_on:
      - postgres
    restart: unless-stopped
    
  temporal-worker:
    build: ./temporal-worker
    environment:
      - TEMPORAL_HOST=temporal:7233
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - temporal
    restart: unless-stopped
    
  brain-gateway:
    build: ./brain-gateway
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - VAULT_ADDR=${VAULT_ADDR}
      - VAULT_TOKEN=${VAULT_TOKEN}
    depends_on:
      - postgres
      - redis
      - vault
    restart: unless-stopped
    
  auth-service:
    build: ./auth
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    
  client-portal:
    build: ./portals/client-portal
    environment:
      - NEXT_PUBLIC_BRAIN_GATEWAY_URL=${BRAIN_GATEWAY_URL}
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
      - NEXTAUTH_URL=${NEXTAUTH_URL}
    depends_on:
      - brain-gateway
      - auth-service
    restart: unless-stopped

volumes:
  postgres-data:
  redis-data:
  vault-data:
```

**Production Dockerfile for Client Portal**:

```dockerfile
# File: portals/client-portal/Dockerfile.prod

FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-alpine AS runner

WORKDIR /app
ENV NODE_ENV=production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3003
CMD ["node", "server.js"]
```

---

### 5.2 Deployment Checklist

**Pre-Deployment**:
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] SSL certificates obtained
- [ ] Database backups configured
- [ ] Monitoring alerts configured
- [ ] Documentation updated
- [x] **DevOps & Infrastructure**
  - [x] Implement robust CI/CD pipeline (GitHub Actions)
  - [x] Set up local Docker Registry
  - [x] Configure local domains (*.bizosaas.local)
  - [ ] Implement monitoring & alerting (Prometheus/Grafana) - *In Progress*
  - [ ] Set up backup strategies for databases

**Deployment Steps**:
1. [ ] Build all Docker images
2. [ ] Push images to registry
3. [ ] Deploy to staging environment
4. [ ] Run smoke tests on staging
5. [ ] Deploy to production
6. [ ] Verify all services healthy
7. [ ] Run production smoke tests
8. [ ] Monitor for 24 hours

**Post-Deployment**:
- [ ] Verify all URLs accessible
- [ ] Test critical user journeys
- [ ] Check error logs
- [ ] Monitor performance metrics
- [ ] Verify backup jobs running

---

## Phase 6: Documentation Updates

### 6.1 Update ARCHITECTURE_RECOMMENDATION_V2.md

**Changes Needed**:
- ✅ Confirm all 8 services are running
- ✅ Document Vault integration
- ✅ Document Temporal worker deployment
- ✅ Update connector count (13 confirmed)
- ✅ Document AI agent architecture

### 6.2 Update FEATURE_GAP_ANALYSIS.md

**Changes Needed**:
- ✅ Mark completed items
- ✅ Update remaining gaps
- ✅ Add new implementation details
- ✅ Update testing status

---

## Success Criteria

### Minimum Viable Product (MVP)
- ✅ All infrastructure services running
- ✅ Authentication working (credentials + OAuth)
- ⬜ At least 3 connectors fully functional (WordPress, Zoho, Shopify)
- ⬜ AI agents responding with real LLM (not mocked)
- ⬜ RAG working with knowledge base
- ⬜ BYOK storing keys in Vault
- ⬜ All UI tabs showing live data
- ⬜ No critical bugs

### Production Ready
- ⬜ All 13 connectors functional
- ⬜ All 7 AI agents operational
- ⬜ Temporal workflows executing
- ⬜ Audit logging capturing events
- ⬜ SSO with Google/Microsoft working
- ⬜ Multi-tenancy strictly enforced
- ⬜ Performance targets met
- ⬜ Security audit passed
- ⬜ Load testing passed
- ⬜ Disaster recovery tested

---

## Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Backend Integration | 3-4 days | None |
| Phase 2: Frontend Wiring | 2-3 days | Phase 1 |
| Phase 3: AI & RAG | 3-4 days | Phase 1 |
| Phase 4: Testing | 2-3 days | Phase 2, 3 |
| Phase 5: Deployment | 1-2 days | Phase 4 |
| Phase 6: Documentation | 1 day | All phases |

**Total Estimated Time**: 12-17 days

---

## Next Immediate Actions

1. **Install Dependencies**:
   ```bash
   pip install hvac alembic openai anthropic
   ```

2. **Run Database Migrations**:
   ```bash
   cd bizosaas-brain-core/brain-gateway
   alembic init migrations
   alembic revision --autogenerate -m "Initial schema"
   alembic upgrade head
   ```

3. **Deploy Temporal Worker**:
   ```bash
   cd bizosaas-brain-core
   docker-compose up -d temporal-worker
   ```

4. **Test Vault Integration**:
   ```bash
   # Store test secret
   curl -X POST http://localhost:8200/v1/secret/data/test \
     -H "X-Vault-Token: root" \
     -d '{"data": {"key": "value"}}'
   ```

5. **Wire First Connector (WordPress)**:
   - Update `CMSContent.tsx` to use `brainApi`
   - Test data fetching
   - Verify live data display

---

**Status**: Ready to begin implementation  
**Priority**: Start with Phase 1 (Backend Integration)  
**First Task**: Vault integration for secure secrets management
