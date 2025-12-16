# 📋 Final Dokploy Environment Configuration

Please copy and paste these exact blocks into the "Environment" tab of each respective service in Dokploy.

---

## 1. Service: `client-portal` (Frontend)

**⚠️ IMPORTANT**: Set `PORT=3001` to avoid conflicts.

```env
# --- Network Configuration ---
PORT=3001
NODE_ENV=production

# --- Internal Networking (Critical for 500 Error Fix) ---
BRAIN_GATEWAY_URL=http://brain-gateway:8001

# --- Authentication (Authentik SSO) ---
AUTHENTIK_URL=https://sso.bizoholic.net
NEXT_PUBLIC_SSO_URL=https://sso.bizoholic.net
AUTHENTIK_ISSUER=https://sso.bizoholic.net/application/o/bizosaas/
AUTHENTIK_CLIENT_ID=<REDACTED>
AUTHENTIK_CLIENT_SECRET=<REDACTED>

# --- NextAuth Session Security ---
NEXTAUTH_URL=https://app.bizoholic.net
NEXTAUTH_SECRET=<REDACTED>
AUTH_SECRET=<REDACTED>
AUTH_TRUST_HOST=true

# --- Public API Endpoints (Browser Access) ---
NEXT_PUBLIC_API_URL=https://api.bizoholic.net
NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.net
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.net
NEXT_PUBLIC_AUTH_URL=https://auth-api.bizoholic.net
NEXT_PUBLIC_BRAIN_API_URL=https://api.bizoholic.net
NEXT_PUBLIC_TEMPORAL_UI_URL=https://temporal.bizoholic.net
NEXT_PUBLIC_VAULT_UI_URL=https://vault.bizoholic.net
```

---

## 2. Service: `brain-gateway` (Core Backend)

```env
# --- Server Config ---
PORT=8001
HOST=0.0.0.0

# --- Database & Cache ---
POSTGRES_HOST=postgres
POSTGRES_DB=bizosaas
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<REDACTED>
REDIS_HOST=redis
VAULT_ADDR=http://vault:8200

# --- Security Secrets ---
JWT_SECRET=<REDACTED>
AUTH_SECRET=<REDACTED>
AUTHENTIK_CLIENT_ID=<REDACTED>
AUTHENTIK_CLIENT_SECRET=<REDACTED>

# --- LLM Provider Keys (Critical for AI) ---
OPENAI_API_KEY=<REDACTED>
ANTHROPIC_API_KEY=<REDACTED>
GOOGLE_API_KEY=<REDACTED>
OPENROUTER_API_KEY=<REDACTED>

# --- Optional/Unused Keys (Can be left blank or filled) ---
COHERE_API_KEY=your-cohere-key-here
MISTRAL_API_KEY=your-mistral-key-here
GROQ_API_KEY=gsk_your-groq-key-here
TOGETHER_API_KEY=your-together-key-here
PERPLEXITY_API_KEY=pplx-your-perplexity-key-here
GITHUB_TOKEN=<REDACTED>
```
