# Vault Migration Plan for Next.js Portals

## Overview
Currently, the Next.js applications (Client Portal & Admin Dashboard) rely on `.env` files for configuration. While this is standard for many setups, your security architecture uses HashiCorp Vault. This document outlines the plan to migrate the Next.js portals to effectively use Vault.

## The Challenge
Unlike Python/Django services which can fetch secrets at runtime using `hvac` (via `vault_config_helper.py`), Next.js applications have two distinct phases:
1.  **Build Time (`next build`)**: Requires `NEXT_PUBLIC_` variables to be present in the environment to be baked into the static JavaScript bundles.
2.  **Runtime (`next start`)**: Requires server-side secrets (like `NEXTAUTH_SECRET`, `AUTHENTIK_CLIENT_SECRET`) to be present in the environment *before* the Node.js process starts.

## Strategy: Init Container / Entrypoint Script

We cannot easily change how `next start` works, so we must wrap it. We will use a script that fetches secrets from Vault and exports them as environment variables **before** starting the application.

### Phase 1: Create the Vault Injection Script

Create a shared script `scripts/deploy-with-vault.js` (using Node.js to avoid extra dependencies like `jq` or `curl` complexity in minimal alpine images):

```javascript
// scripts/vault-injector.js
const vault = require('node-vault')({
  apiVersion: 'v1',
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN
});

async function injectSecrets() {
  try {
    const secretPath = process.env.VAULT_SECRET_PATH; // e.g., 'secret/data/bizosaas/portals/client'
    const { data } = await vault.read(secretPath);
    
    // Print exports for eval
    Object.entries(data.data).forEach(([key, value]) => {
      console.log(`export ${key}="${value}"`);
    });
  } catch (err) {
    console.error('Failed to fetch from Vault:', err);
    process.exit(1);
  }
}

injectSecrets();
```

### Phase 2: Update Docker Entrypoint

Modify the `Dockerfile` for both portals to use a custom entrypoint or modify the command.

**Current:**
```dockerfile
CMD ["npm", "start"]
```

**Proposed:**
```dockerfile
# Copy the injector script
COPY scripts/vault-injector.js ./scripts/vault-injector.js

# Install minimal vault client if needed, or use fetch in the script
# RUN npm install node-vault

# Update Command to:
# 1. Login to Vault (if using AppRole, handle that auth first)
# 2. Source the secrets
# 3. Start Next.js
CMD ["sh", "-c", "eval $(node scripts/vault-injector.js) && npm start"]
```

### Phase 3: Build-Time Variables

For `NEXT_PUBLIC_` variables, these *must* be available during `docker build`.
*   **Option A (Current):** Keep using CI/CD secrets injected as `--build-arg`.
*   **Option B (Advanced):** Fetch from Vault during the CI pipeline and pass as ARGs.

**Recommendation:** For now, keep `NEXT_PUBLIC` variables (which are not truly secret, just configuration) in standard CI/CD variables or `.env`, and move **Server-Side Secrets** (`NEXTAUTH_SECRET`, `AUTHENTIK_SECRET`) to Vault.

## Specific Implementation Steps

1.  **Install Vault Client:** Add helper library to `package.json` or use `fetch` in a zero-dependency script.
2.  **Configure Vault Paths:**
    *   `secret/data/bizosaas/client-portal`
    *   `secret/data/bizosaas/admin-dashboard`
3.  **Update Deployment Yaml:** Update Dokploy/Docker Compose to provide `VAULT_ADDR` and authentication credentials (Token or AppRole) to the container.

## Immediate Action
For the current deployment, verify that the critical variables are set in Dokploy's "Environment" tab:
*   `NEXTAUTH_URL`
*   `NEXTAUTH_SECRET` (Must be consistent!)
*   `AUTHENTIK_CLIENT_SECRET`
