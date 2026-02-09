# BizOSaaS Platform - Project Structure Clarification

**Date**: 2026-01-23 05:52 UTC

---

## 📊 Current Project Structure in Dokploy

You have **5 projects** in Dokploy, organized as follows:

### 1. **platform-core** (ID: `p4fmYaVZ_iDFDH4XSDnOU`)
**Description**: BizOSaaS API and AI Core  
**Purpose**: Core infrastructure and backend services

**Services**:
- ✅ **Authentik SSO** (`authentik_sso`) - Authentication service
- ✅ **Vault** (`vault`) - Secret management
- ✅ **core-stack** (`compose-synthesize-online-feed-gb95pq`) - Main backend API/AI services

### 2. **portals** (ID: `WfVYVHpPQh_h5s4GpyDdW`)
**Description**: User and Admin Frontends  
**Purpose**: All user-facing web applications

**Services**:
- ✅ **admin-portal** - Admin dashboard
- ✅ **client-portal** - Client application
- ✅ **business-directory** - Business directory portal

### 3. **utilities** (ID: `p3sOOoRvMY35MboY_oaGn`)
**Description**: Billing and Background Services  
**Purpose**: Support services like billing, background jobs

**Services**: (Currently empty)

### 4. **bizoholic-website** (ID: `FwOlHIRQx_IumFujBM1yI`)
**Description**: WordPress website for Bizoholic  
**Services**: WordPress instance

### 5. **coreldove-website** (ID: `8TKvjouZq2qC4gehXAtdC`)
**Description**: WordPress website for Coreldove  
**Services**: WordPress instance

---

## ✅ **Answer to Your Question**

### **You DO NOT need to create a new "bizosaas-platform" project!**

The structure is already correct:

1. **Infrastructure services** (Authentik, Vault) → Already in `platform-core` ✅
2. **Backend API/AI services** (core-stack) → Already in `platform-core` ✅
3. **Frontend portals** → Already in `portals` ✅

### **The `core-stack` service is correctly placed**

The `core-stack` service with appName `compose-synthesize-online-feed-gb95pq` is:
- ✅ **Location**: `platform-core` project (correct)
- ✅ **Environment**: Has all required variables (DATABASE_URL, REDIS_URL, etc.)
- ✅ **Purpose**: Main backend API and AI processing

---

## 🎯 **Recommended Project Organization**

Your current structure is actually **well-organized**. Here's what each project should contain:

### **platform-core** (Backend & Infrastructure)
```
├── Authentik SSO (authentication)
├── Vault (secrets management)
└── core-stack (main backend API/AI)
    ├── FastAPI backend
    ├── AI/ML services
    ├── Background workers
    └── MCP servers
```

### **portals** (Frontend Applications)
```
├── admin-portal (admin.bizoholic.net)
├── client-portal (app.bizoholic.net)
└── business-directory (directory.bizoholic.net)
```

### **utilities** (Support Services)
```
└── (Future services like Lago billing, Plane, etc.)
```

---

## 🔧 **What You Should Do Instead**

Since your structure is already correct, you should:

### 1. **Keep the Current Structure** ✅
- `platform-core` for all backend/infrastructure
- `portals` for all frontend applications
- `utilities` for support services

### 2. **Verify core-stack Configuration**
The `core-stack` service already has the correct environment variables:

```bash
DATABASE_URL=postgresql://...
VECTOR_DB_URL=postgresql://...
REDIS_URL=redis://...
VAULT_TOKEN=staging-root-token-bizosaas-2025
JWT_SECRET=...
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_API_KEY=...
TEMPORAL_HOST=localhost:7233
TEMPORAL_NAMESPACE=default
```

### 3. **Add Missing Variables to core-stack** (if needed)
If your backend needs to integrate with Authentik, add these to `core-stack`:

```bash
AUTH_AUTHENTIK_ISSUER=https://auth-sso.bizoholic.net/application/o/bizosaas-platform/
AUTH_AUTHENTIK_ID=bizosaas-portal
AUTH_AUTHENTIK_SECRET=BizOSaaS2024!AuthentikSecret
```

---

## 📝 **Project Naming Clarification**

| What You Called It | What It Actually Is | Dokploy Project Name |
|-------------------|---------------------|---------------------|
| "bizosaas-platform" | The entire platform | Multiple projects |
| Backend/API | Core services | `platform-core` |
| Frontend apps | User interfaces | `portals` |
| Infrastructure | Auth, Vault, etc. | `platform-core` |

**Note**: "bizosaas-platform" is the **application slug** in Authentik, not a Dokploy project name.

---

## 🚀 **Next Steps**

### 1. **No New Project Needed**
- ✅ Keep using `platform-core` for backend
- ✅ Keep using `portals` for frontends

### 2. **Update core-stack if Needed**
If your backend API needs to validate Authentik tokens:

```bash
# Add to core-stack environment variables
python3 -c "
import requests, json
API_KEY = 'mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug'
BASE_URL = 'https://dk.bizoholic.com/api/trpc'

# Get current env
url = f'{BASE_URL}/compose.one?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22composeId%22%3A%22QiOdwXQi4ZQCM3Qg_KNcl%22%7D%7D%7D'
resp = requests.get(url, headers={'x-api-key': API_KEY})
data = resp.json()[0]['result']['data']['json']
current_env = data.get('env', '')

# Add Authentik variables
new_env = current_env + '''
AUTH_AUTHENTIK_ISSUER=https://auth-sso.bizoholic.net/application/o/bizosaas-platform/
AUTH_AUTHENTIK_ID=bizosaas-portal
AUTH_AUTHENTIK_SECRET=BizOSaaS2024!AuthentikSecret
'''

# Update
payload = {'0': {'json': {'composeId': 'QiOdwXQi4ZQCM3Qg_KNcl', 'env': new_env, 'sourceType': 'raw'}}}
resp = requests.post(f'{BASE_URL}/compose.update?batch=1', headers={'x-api-key': API_KEY, 'Content-Type': 'application/json'}, json=payload)
print('Updated:', resp.status_code == 200)
"
```

### 3. **Configure Authentik Application**
Follow the steps in `AUTHENTIK_STATUS.md` to create the OAuth2 application.

---

## 💡 **Summary**

**Question**: Should I create a new "bizosaas-platform" project?  
**Answer**: **NO** - Your current structure is correct!

- ✅ `platform-core` = Backend + Infrastructure (Authentik, Vault, core-stack)
- ✅ `portals` = All frontend applications
- ✅ `utilities` = Support services (billing, etc.)

The name "bizosaas-platform" is used in:
- Authentik application slug
- OAuth2 issuer URL path
- General reference to the entire system

But it's **NOT** a separate Dokploy project. Everything is already organized correctly! 🎉
