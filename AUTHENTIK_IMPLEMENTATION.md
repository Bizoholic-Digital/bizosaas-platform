# Authentik Integration Implementation Plan

**Version**: 1.0  
**Date**: 2025-12-08  
**Architecture**: DDD + Hexagonal (Ports & Adapters)  
**Goal**: Replace custom auth with Authentik while maintaining architectural integrity.

---

## Executive Summary

This document details the step-by-step implementation of **Authentik** as the central Identity Provider for BizOSaaS, following **Domain-Driven Design (DDD)** and **Hexagonal Architecture** principles.

The key principle: **The Brain Core should NOT know Authentik exists.** It should only know about the **Identity Port** interface.

---

## 1. Current State Analysis

### Current Auth Architecture
```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  Client Portal  │─────▶│  Brain Gateway  │──────▶│  Auth Service   │
│  (NextAuth)     │       │  (Proxy)        │       │ (Custom FastAPI)│
│                 │       │                 │       │                 │
│  - Credentials  │       │  - /api/auth/*  │       │  - JWT Issue    │
│  - LocalStorage │       │  - Forward      │       │  - User CRUD    │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

### Problems with Current State
1. **Tight Coupling**: Gateway directly proxies to custom auth (line 51-54 in `main.py`).
2. **No SSO**: Cannot authenticate WordPress or other services.
3. **No MFA**: Not implemented.
4. **Not a Port/Adapter**: Auth logic is a concrete implementation, not an interface.

---

## 2. Target State (Hexagonal)

### Architecture After Authentik
```
                         ┌───────────────────────────────────────┐
                         │             DOMAIN CORE               │
                         │  ┌─────────────────────────────────┐  │
                         │  │   Identity Port (Interface)     │  │
                         │  │   - authenticate(token)         │  │
                         │  │   - get_user_info(token)        │  │
                         │  │   - has_permission(user, perm)  │  │
                         │  └─────────────────────────────────┘  │
                         └──────────────────┬────────────────────┘
                                            │
         ┌──────────────────────────────────┴───────────────────────────────┐
         │                                                                   │
         ▼                                                                   ▼
┌─────────────────────┐                                         ┌─────────────────────┐
│   Authentik Adapter │                                         │  (Future) Keycloak  │
│   (Primary)         │                                         │   Adapter           │
│                     │                                         │                     │
│  - OIDC Token Valid │                                         │  (Same interface)   │
│  - User Info API    │                                         │                     │
└─────────────────────┘                                         └─────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                              Authentik (External Service)                          │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────────┐  │
│   │   Users     │  │   MFA       │  │   SSO       │  │   OAuth2 / OIDC Provider │  │
│   └─────────────┘  └─────────────┘  └─────────────┘  └──────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Implementation Steps (Hexagonal Approach)

### Phase 1: Define the Identity Port (Interface)

**File**: `bizosaas-brain-core/brain-gateway/domain/ports/identity_port.py`

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class AuthenticatedUser:
    """Domain Entity for authenticated user."""
    id: str
    email: str
    name: str
    roles: List[str]
    tenant_id: Optional[str] = None
    permissions: List[str] = None

class IdentityPort(ABC):
    """Port (Interface) for Identity operations.
    
    The Domain Core depends ONLY on this interface.
    Adapters (Authentik, Keycloak, etc.) implement this.
    """
    
    @abstractmethod
    async def validate_token(self, token: str) -> bool:
        """Validate if a token is valid and not expired."""
        pass
    
    @abstractmethod
    async def get_user_from_token(self, token: str) -> Optional[AuthenticatedUser]:
        """Extract user information from a valid token."""
        pass
    
    @abstractmethod
    async def has_permission(self, user: AuthenticatedUser, permission: str) -> bool:
        """Check if user has a specific permission."""
        pass
    
    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[AuthenticatedUser]:
        """Retrieve user details by ID."""
        pass
```

### Phase 2: Implement the Authentik Adapter

**File**: `bizosaas-brain-core/brain-gateway/adapters/identity/authentik_adapter.py`

```python
import httpx
from typing import Optional, List
from domain.ports.identity_port import IdentityPort, AuthenticatedUser

class AuthentikAdapter(IdentityPort):
    """Adapter that implements IdentityPort using Authentik OIDC."""
    
    def __init__(self, authentik_url: str, client_id: str, client_secret: str):
        self.authentik_url = authentik_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_introspection_url = f"{authentik_url}/application/o/introspect/"
        self.userinfo_url = f"{authentik_url}/application/o/userinfo/"
    
    async def validate_token(self, token: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_introspection_url,
                data={
                    "token": token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("active", False)
            return False
    
    async def get_user_from_token(self, token: str) -> Optional[AuthenticatedUser]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.userinfo_url,
                headers={"Authorization": f"Bearer {token}"},
            )
            if response.status_code == 200:
                data = response.json()
                return AuthenticatedUser(
                    id=data.get("sub"),
                    email=data.get("email"),
                    name=data.get("name"),
                    roles=data.get("groups", []),
                    tenant_id=data.get("tenant_id"),
                    permissions=data.get("permissions", []),
                )
            return None
    
    async def has_permission(self, user: AuthenticatedUser, permission: str) -> bool:
        return permission in (user.permissions or [])
    
    async def get_user_by_id(self, user_id: str) -> Optional[AuthenticatedUser]:
        # Call Authentik Admin API (requires separate auth)
        # Implementation depends on Authentik API
        pass
```

### Phase 3: Update Brain Gateway to Use the Port

**File**: `bizosaas-brain-core/brain-gateway/app/dependencies.py`

```python
from functools import lru_cache
from adapters.identity.authentik_adapter import AuthentikAdapter
from domain.ports.identity_port import IdentityPort
import os

@lru_cache()
def get_identity_port() -> IdentityPort:
    """Dependency Injection: Returns the configured Identity Adapter."""
    return AuthentikAdapter(
        authentik_url=os.getenv("AUTHENTIK_URL", "http://authentik:9000"),
        client_id=os.getenv("AUTHENTIK_CLIENT_ID"),
        client_secret=os.getenv("AUTHENTIK_CLIENT_SECRET"),
    )
```

### Phase 4: Create Auth Middleware Using the Port

**File**: `bizosaas-brain-core/brain-gateway/app/middleware/auth_middleware.py`

```python
from fastapi import Request, HTTPException, Depends
from app.dependencies import get_identity_port
from domain.ports.identity_port import IdentityPort, AuthenticatedUser

async def get_current_user(
    request: Request,
    identity: IdentityPort = Depends(get_identity_port)
) -> AuthenticatedUser:
    """FastAPI dependency that validates token and returns user."""
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = auth_header.split(" ")[1]
    
    if not await identity.validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = await identity.get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def require_permission(permission: str):
    """Decorator factory for permission-based access control."""
    async def permission_checker(
        user: AuthenticatedUser = Depends(get_current_user),
        identity: IdentityPort = Depends(get_identity_port)
    ):
        if not await identity.has_permission(user, permission):
            raise HTTPException(status_code=403, detail=f"Permission denied: {permission}")
        return user
    return permission_checker
```

### Phase 5: Update Client Portal NextAuth Configuration

**File**: `portals/client-portal/app/api/auth/[...nextauth]/route.ts`

```typescript
import NextAuth from "next-auth";
import AuthentikProvider from "next-auth/providers/authentik";

export const authOptions = {
  providers: [
    AuthentikProvider({
      clientId: process.env.AUTHENTIK_CLIENT_ID!,
      clientSecret: process.env.AUTHENTIK_CLIENT_SECRET!,
      issuer: process.env.AUTHENTIK_ISSUER, // e.g., http://localhost:9000/application/o/bizosaas/
    }),
  ],
  callbacks: {
    async jwt({ token, account, profile }) {
      if (account) {
        token.accessToken = account.access_token;
        token.idToken = account.id_token;
        token.roles = profile?.groups || [];
      }
      return token;
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken;
      session.user.roles = token.roles;
      return session;
    },
  },
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
```

### Phase 6: Local Docker Compose for Authentik

**File**: `bizosaas-brain-core/docker-compose.authentik.yml`

```yaml
version: "3.9"

services:
  authentik-postgres:
    image: postgres:15-alpine
    container_name: authentik-postgres
    environment:
      POSTGRES_DB: authentik
      POSTGRES_USER: authentik
      POSTGRES_PASSWORD: authentik_secret
    volumes:
      - authentik_postgres_data:/var/lib/postgresql/data
    networks:
      - brain-network

  authentik-redis:
    image: redis:alpine
    container_name: authentik-redis
    networks:
      - brain-network

  authentik-server:
    image: ghcr.io/goauthentik/server:latest
    container_name: authentik-server
    command: server
    environment:
      AUTHENTIK_SECRET_KEY: "your-super-secret-key-change-in-production"
      AUTHENTIK_REDIS__HOST: authentik-redis
      AUTHENTIK_POSTGRESQL__HOST: authentik-postgres
      AUTHENTIK_POSTGRESQL__USER: authentik
      AUTHENTIK_POSTGRESQL__NAME: authentik
      AUTHENTIK_POSTGRESQL__PASSWORD: authentik_secret
    ports:
      - "9000:9000"
      - "9443:9443"
    depends_on:
      - authentik-postgres
      - authentik-redis
    networks:
      - brain-network

  authentik-worker:
    image: ghcr.io/goauthentik/server:latest
    container_name: authentik-worker
    command: worker
    environment:
      AUTHENTIK_SECRET_KEY: "your-super-secret-key-change-in-production"
      AUTHENTIK_REDIS__HOST: authentik-redis
      AUTHENTIK_POSTGRESQL__HOST: authentik-postgres
      AUTHENTIK_POSTGRESQL__USER: authentik
      AUTHENTIK_POSTGRESQL__NAME: authentik
      AUTHENTIK_POSTGRESQL__PASSWORD: authentik_secret
    depends_on:
      - authentik-postgres
      - authentik-redis
    networks:
      - brain-network

volumes:
  authentik_postgres_data:

networks:
  brain-network:
    external: true
```

---

## 4. Vault Integration

Secrets that move to Vault:
- `AUTHENTIK_CLIENT_SECRET`
- `AUTHENTIK_SECRET_KEY`
- Database passwords

Brain Gateway retrieves these at startup via Vault Agent or direct API.

---

## 5. Testing Strategy

### Unit Tests (Domain Layer)
- Mock `IdentityPort` interface.
- Test permission logic.
- Test user entity validation.

### Integration Tests
- Start Authentik locally.
- Test token validation flow.
- Test OIDC callback.

### E2E Tests
- Login via Portal → Authentik → Callback → Dashboard.
- API call with token → Gateway validates via Authentik.

---

## 6. Migration Checklist

- [ ] **Phase 1**: Create `domain/ports/identity_port.py`
- [ ] **Phase 2**: Create `adapters/identity/authentik_adapter.py`
- [ ] **Phase 3**: Update Gateway dependencies
- [ ] **Phase 4**: Create auth middleware
- [ ] **Phase 5**: Update NextAuth config
- [ ] **Phase 6**: Add Authentik to Docker Compose
- [ ] **Phase 7**: Configure Authentik (Create Application, Provider)
- [ ] **Phase 8**: Test Login Flow
- [ ] **Phase 9**: Remove old `auth-service` container
- [ ] **Phase 10**: Deploy to Oracle Cloud

---

## 7. Files to Keep Open for Reference

| Document | Purpose |
|----------|---------|
| `DDD-Hexogonal-Architecture.md` | Architecture principles |
| `AUTH_VS_AUTHENTIK.md` | Decision rationale |
| `AUTHENTIK_IMPLEMENTATION.md` (this file) | Implementation steps |
| `brain-gateway/main.py` | Gateway structure |
| `client-portal/components/auth/AuthProvider.tsx` | Current auth flow |
| `docker-compose.yml` | Service definitions |

---

## 8. Environment Variables Required

```bash
# Authentik Configuration
AUTHENTIK_URL=http://localhost:9000
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas/
AUTHENTIK_CLIENT_ID=bizosaas-brain
AUTHENTIK_CLIENT_SECRET=<from-vault>

# Vault (for secrets)
VAULT_ADDR=http://localhost:8200
VAULT_TOKEN=<root-token-for-dev>
```

---

## Conclusion

This implementation follows **Hexagonal Architecture** by:
1. Defining a stable **Identity Port** interface.
2. Implementing an **Authentik Adapter** that can be swapped.
3. Brain Core never imports Authentik SDK directly.

And follows **DDD** by:
1. **Bounded Context**: Identity is isolated.
2. **Domain Entities**: `AuthenticatedUser` is a domain object.
3. **Ports & Adapters**: External IdP accessed only through ports.
