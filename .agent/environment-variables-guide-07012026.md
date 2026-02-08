# Environment Variables Configuration Guide
## January 7, 2026

## ✅ What Was Done

### 1. **Environment Variable Pattern**
All docker-compose files now use environment variables with default fallbacks:

```yaml
- "traefik.http.routers.SERVICE.rule=Host(`${DOMAIN_VAR:-default.domain.com}`)"
```

**Pattern**: `${VARIABLE_NAME:-default_value}`
- If `VARIABLE_NAME` is set → uses that value
- If `VARIABLE_NAME` is not set → uses `default_value`

### 2. **New Domain Variables**
Added three new environment variables for domain configuration:

| Variable | Default Value | Purpose |
|----------|---------------|---------|
| `BRAIN_GATEWAY_DOMAIN` | `api.bizoholic.net` | Brain Gateway API domain |
| `ADMIN_PORTAL_DOMAIN` | `admin.bizoholic.net` | Admin Dashboard domain |
| `CLIENT_PORTAL_DOMAIN` | `app.bizoholic.net` | Client Portal domain |

### 3. **Created .env.example**
Comprehensive example file with:
- ✅ All environment variables documented
- ✅ Placeholder values (no real secrets)
- ✅ Organized by service
- ✅ Detailed notes and usage instructions

## 📋 How to Use in Dokploy

### Method 1: Using Dokploy UI (Recommended)

#### For Each Service:

1. **Navigate to Service**
   - Go to Dokploy UI
   - Select the service (Brain Gateway, Admin Portal, or Client Portal)

2. **Add Environment Variables**
   - Click on "Environment" or "Settings" tab
   - Add variables one by one or bulk import

3. **Domain Variables** (Optional - defaults work)
   ```bash
   BRAIN_GATEWAY_DOMAIN=api.bizoholic.net
   ADMIN_PORTAL_DOMAIN=admin.bizoholic.net
   CLIENT_PORTAL_DOMAIN=app.bizoholic.net
   ```

4. **Service-Specific Variables**

   **Brain Gateway:**
   ```bash
   DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
   VECTOR_DB_URL=postgresql://user:pass@host/db?sslmode=require
   REDIS_URL=redis://default:pass@host:port/0
   TEMPORAL_HOST=region.aws.api.temporal.io:7233
   TEMPORAL_NAMESPACE=your-namespace
   VAULT_ADDR=http://vault:8200
   VAULT_TOKEN=your-vault-token
   JWT_SECRET=your-jwt-secret
   OPENAI_API_KEY=sk-proj-...
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=...
   OPENROUTER_API_KEY=sk-or-v1-...
   GITHUB_TOKEN=ghp_...
   ```

   **Admin Portal:**
   ```bash
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
   CLERK_SECRET_KEY=sk_test_...
   NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.net
   NEXT_PUBLIC_API_BASE_URL=https://api.bizoholic.net
   BRAIN_GATEWAY_URL=http://bizosaas-brain-staging:8000
   NEXTAUTH_URL=https://admin.bizoholic.net
   NEXTAUTH_SECRET=your-secret
   NODE_ENV=production
   PORT=3004
   ```

   **Client Portal:**
   ```bash
   # Same Clerk credentials as Admin Portal
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
   CLERK_SECRET_KEY=sk_test_...
   NEXT_PUBLIC_API_URL=https://api.bizoholic.net
   BRAIN_GATEWAY_URL=http://bizosaas-brain-staging:8000
   NODE_ENV=production
   PORT=3003
   ```

   **Vault:**
   ```bash
   VAULT_DEV_ROOT_TOKEN_ID=your-token-here
   VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200
   ```

5. **Save and Redeploy**
   - Click "Save"
   - Click "Redeploy"

### Method 2: Using .env File (Local Development)

1. **Copy Example File**
   ```bash
   cp .env.example .env
   ```

2. **Fill in Actual Values**
   - Replace all placeholder values with real credentials
   - Get credentials from your services (Neon, Redis Cloud, Temporal, etc.)

3. **Never Commit .env**
   - The `.env` file is gitignored
   - Only `.env.example` should be in git (with placeholders)

## 🔄 Deployment Workflow

### Step 1: Update Environment Variables in Dokploy

For each service, add/update environment variables in Dokploy UI.

### Step 2: Redeploy Services

Deploy in this order:

1. **Vault** (if not running)
   ```
   Dokploy UI → Vault → Redeploy
   ```

2. **Brain Gateway**
   ```
   Dokploy UI → Brain Gateway → Redeploy
   ```
   - Wait for healthy status
   - Verify: `https://api.bizoholic.net/health`

3. **Admin Portal**
   ```
   Dokploy UI → Admin Portal → Redeploy
   ```
   - Wait for healthy status
   - Verify: `https://admin.bizoholic.net`

4. **Client Portal**
   ```
   Dokploy UI → Client Portal → Redeploy
   ```
   - Wait for healthy status
   - Verify: `https://app.bizoholic.net`

## 🎯 Benefits

### ✅ Flexibility
- Change domains without modifying code
- Easy environment-specific configuration
- Support for multiple deployment environments

### ✅ Security
- No secrets in git repository
- Credentials managed in Dokploy UI
- Separate credentials per environment

### ✅ Maintainability
- Single source of truth for configuration
- Easy to update and track changes
- Clear documentation in .env.example

## 📝 Important Notes

### Domain Configuration

**Default Behavior:**
- If you don't set domain variables, defaults are used
- Defaults: `api.bizoholic.net`, `admin.bizoholic.net`, `app.bizoholic.net`

**Custom Domains:**
- Set domain variables in Dokploy UI
- Redeploy service
- Traefik automatically handles routing and SSL

**Traefik.me Domains:**
- Dokploy provides automatic `*.traefik.me` domains
- No DNS configuration needed
- Useful for testing

### Internal vs External URLs

**Internal URLs** (Docker network):
```bash
BRAIN_GATEWAY_URL=http://bizosaas-brain-staging:8000
VAULT_ADDR=http://vault:8200
```
- Used for service-to-service communication
- Not accessible from outside

**External URLs** (Public):
```bash
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.net
NEXT_PUBLIC_VAULT_UI_URL=https://vault.bizoholic.net
```
- Used by browser/client
- Accessible via Traefik

### Port Configuration

**Internal Ports** (Container):
- Brain Gateway: 8000
- Admin Portal: 3004
- Client Portal: 3003
- Vault: 8200

**External Ports** (Host):
- All traffic goes through Traefik: 80 (HTTP) and 443 (HTTPS)
- No direct port binding to host

## 🔍 Verification

After deployment, verify environment variables are loaded:

```bash
# Check container environment
docker exec CONTAINER_NAME env | grep DOMAIN

# Example for brain-gateway
docker exec bizosaas-brain-staging env | grep BRAIN_GATEWAY_DOMAIN

# Should output:
# BRAIN_GATEWAY_DOMAIN=api.bizoholic.net
```

## 🐛 Troubleshooting

### Issue: Domain not working after setting variable

**Solution:**
1. Verify variable is set in Dokploy UI
2. Redeploy the service
3. Check container logs: `docker logs CONTAINER_NAME`
4. Verify Traefik labels: `docker inspect CONTAINER_NAME | grep traefik`

### Issue: Service using wrong domain

**Solution:**
1. Check environment variable value in Dokploy
2. Ensure no typos in variable name
3. Redeploy service to apply changes
4. Clear browser cache

### Issue: SSL certificate not generated

**Solution:**
1. Verify DNS points to server IP
2. Ensure ports 80 and 443 are open
3. Check Traefik logs: `docker logs dokploy-traefik`
4. Wait 1-2 minutes for Let's Encrypt

## 📦 Git Commit

**Commit**: `46a19f8`
**Branch**: `staging`
**Files Changed**:
- `docker-compose.core.yml` - Added domain variables
- `docker-compose.admin-portal.yml` - Added domain variables
- `docker-compose.client-portal.yml` - Added domain variables
- `.env.example` - Created with all variables

## 🚀 Next Steps

1. ✅ Changes committed and pushed to GitHub
2. ⏳ Add environment variables in Dokploy UI for each service
3. ⏳ Redeploy services in order (Vault → Brain → Admin → Client)
4. ⏳ Verify all domains are accessible
5. ⏳ Test login flows
6. ⏳ Monitor service health

---

**Remember**: The `.env.example` file contains placeholders. Use the actual credentials provided by the user when configuring Dokploy UI environment variables.
