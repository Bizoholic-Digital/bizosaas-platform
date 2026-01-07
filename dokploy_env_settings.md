# Dokploy Environment Settings
Copy and paste these settings into the Environment Variables section for each service in Dokploy UI.

## 1. Vault
**Project:** Vault
```bash
VAULT_DEV_ROOT_TOKEN_ID=<YOUR_VAULT_ROOT_TOKEN>
VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200
```

## 2. Brain Gateway
**Project:** BizOSaaS Brain Gateway
```bash
# Database (Neon Cloud)
DATABASE_URL=postgresql://<USER>:<PASSWORD>@<HOST>/<DB>?sslmode=require

# Vector DB (Same as Database, required for RAG)
VECTOR_DB_URL=postgresql://<USER>:<PASSWORD>@<HOST>/<DB>?sslmode=require

# Redis (Redis Cloud)
REDIS_URL=redis://default:<PASSWORD>@<HOST>:<PORT>/0

# Temporal (Temporal Cloud)
TEMPORAL_HOST=ap-south-2.aws.api.temporal.io:7233
TEMPORAL_NAMESPACE=bizosaas-platform-mtls.mdqxv

# Vault (Internal)
USE_VAULT=true
VAULT_ADDR=http://vault:8200
VAULT_TOKEN=<YOUR_VAULT_TOKEN>

# Plans.so Cloud settings
PLANE_WEBHOOK_SECRET=<YOUR_PLANE_WEBHOOK_SECRET>
PLANE_WEBHOOK_URL=https://silo.plane.so/api/github/plane-webhook

# API Keys
JWT_SECRET=<YOUR_JWT_SECRET>
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
ANTHROPIC_API_KEY=<YOUR_ANTHROPIC_API_KEY>
GOOGLE_API_KEY=<YOUR_GOOGLE_API_KEY>
OPENROUTER_API_KEY=<YOUR_OPENROUTER_API_KEY>
GITHUB_TOKEN=<YOUR_GITHUB_TOKEN>

# Domain Configuration (Optional - Defaults are set in code)
BRAIN_GATEWAY_DOMAIN=api.bizoholic.net
```

## 3. Admin Portal
**Project:** BizOSaaS Frontend (Admin Portal)
```bash
# Clerk Authentication (REQUIRED)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_ZWFzeS1rb2RpYWstNzguY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY=<YOUR_CLERK_SECRET_KEY>
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/login
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/signup
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.net
NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.net

# Internal Brain Gateway connection (Needed for server actions)
BRAIN_GATEWAY_URL=http://bizosaas-brain-staging:8000

# Infrastructure UIs
NEXT_PUBLIC_TEMPORAL_UI_URL=https://temporal.bizoholic.net
NEXT_PUBLIC_VAULT_UI_URL=https://vault.bizoholic.net

# NextAuth
NEXTAUTH_URL=https://admin.bizoholic.net
NEXTAUTH_SECRET=<YOUR_NEXTAUTH_SECRET>

# Application Settings
NODE_ENV=production
PORT=3000

# Domain Configuration (Optional - Defaults are set in code)
ADMIN_PORTAL_DOMAIN=admin.bizoholic.net

# Integrations
# NOTE: PLANE_API_TOKEN is required for fetching data from Plane.so. 
# This is DIFFERENT from the webhook secret. Generate it in Plane.so settings.
# If not provided, the app will run in MOCK MODE for Plane data.
PLANE_API_TOKEN=
```

## 4. Client Portal
**Project:** BizOSaaS Frontend (Client Portal)
```bash
# Clerk Authentication (REQUIRED)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_ZWFzeS1rb2RpYWstNzguY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY=<YOUR_CLERK_SECRET_KEY>
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/login
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/signup
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard

# Internal Networking
PORT=3000
NODE_ENV=production
BRAIN_GATEWAY_URL=http://bizosaas-brain-staging:8000

# Public API Endpoints
NEXT_PUBLIC_API_URL=https://api.bizoholic.net
NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.net
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.net
NEXT_PUBLIC_TEMPORAL_UI_URL=https://temporal.bizoholic.net
NEXT_PUBLIC_VAULT_UI_URL=https://vault.bizoholic.net
PLANE_API_TOKEN=

# Domain Configuration (Optional - Defaults are set in code)
CLIENT_PORTAL_DOMAIN=app.bizoholic.net
```
