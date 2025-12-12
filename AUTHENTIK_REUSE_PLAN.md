# Authentik Integration - Reusing Existing Setup
## Admin Dashboard + Client Portal + VPS Integration

**Date**: 2025-12-11  
**Status**: ✅ Authentik Already Configured - Ready to Integrate

---

## 🎯 Discovery: Authentik is Already Implemented!

### ✅ What Already Exists

1. **Authentik Docker Compose** ✅
   - File: `bizosaas-brain-core/docker-compose.authentik.yml`
   - Services: authentik-server, authentik-worker, authentik-postgres, authentik-redis
   - Port: 9000 (HTTP), 9443 (HTTPS)
   - Network: `brain-network` (shared with Brain Gateway)

2. **Authentik Adapter** ✅
   - File: `bizosaas-brain-core/brain-gateway/adapters/identity/authentik_adapter.py`
   - Implements: `IdentityPort` interface
   - Features: Token validation, user info extraction, permission checking

3. **Implementation Documentation** ✅
   - File: `AUTHENTIK_IMPLEMENTATION.md`
   - Complete hexagonal architecture guide
   - DDD principles applied

4. **Environment Template** ✅
   - File: `AUTHENTIK_ENV_TEMPLATE.env`
   - Configuration variables defined

---

## 🔄 Current vs Target State

### Current State
```
┌─────────────────────────────────────────────────────────────┐
│  Authentik (Configured but not in startup script)          │
│  - Docker Compose: ✅ Ready                                 │
│  - Adapter: ✅ Implemented                                  │
│  - Port: ✅ Defined                                         │
│  - Integration: ❌ Not connected to portals                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Admin Dashboard (Just Implemented)                         │
│  - NextAuth: ✅ Configured for Authentik                    │
│  - Middleware: ✅ RBAC implemented                          │
│  - Integration: ❌ Needs Authentik running                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Client Portal (Existing)                                   │
│  - NextAuth: ❓ Unknown if configured for Authentik         │
│  - Integration: ❌ Needs update                             │
└─────────────────────────────────────────────────────────────┘
```

### Target State
```
┌──────────────────────────────────────────────────────────────┐
│                    SINGLE AUTHENTIK INSTANCE                 │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Authentik Server (Port 9000)                          │ │
│  │  - OAuth2/OIDC Provider                                │ │
│  │  - User Management                                     │ │
│  │  - MFA                                                 │ │
│  │  - SSO                                                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Applications:                                               │
│  1. BizOSaaS Admin Dashboard (port 3004)                    │
│  2. BizOSaaS Client Portal (port 3003)                      │
│  3. Brain Gateway API (port 8000)                           │
│                                                              │
│  Groups:                                                     │
│  - super_admin (full access to admin dashboard)             │
│  - platform_admin (platform management)                     │
│  - tenant_admin (client portal access)                      │
│  - tenant_user (client portal access)                       │
└──────────────────────────────────────────────────────────────┘
```

---

## 📋 Integration Plan

### Step 1: Update Startup Script to Include Authentik

**File**: `scripts/start-bizosaas-core-full.sh`

**Add after Step 3 (Infrastructure)**:

```bash
# --- Step 3.5: Start Authentik ---
echo -e "${CYAN}[3.5/7] Starting Authentik SSO...${NC}"
docker compose -f docker-compose.authentik.yml up -d
echo -e "${GREEN}✓ Authentik containers started.${NC}"

if [ "$WAIT_FOR_HEALTH" = true ]; then
    wait_for_service "Authentik" "curl -s http://localhost:9000/-/health/ready/"
fi
```

**Update Service Summary**:
```bash
printf "%-20s %-30s\\n" "Authentik SSO" "http://localhost:9000"
printf "%-20s %-30s\\n" "Admin Dashboard" "http://localhost:3004"
```

---

### Step 2: Configure Authentik Applications

**Access Authentik**: `http://localhost:9000`

**Default Credentials** (first time):
- Username: `akadmin`
- Password: Check Authentik logs or set during first login

#### Application 1: Admin Dashboard

**Create OAuth2/OIDC Provider**:
```
Name: BizOSaaS Admin Dashboard Provider
Authorization flow: default-authorization-flow
Client type: Confidential
Client ID: bizosaas-admin-dashboard
Client Secret: <generate and save>
Redirect URIs: 
  - http://localhost:3004/api/auth/callback/authentik
  - https://your-vps-domain.com/api/auth/callback/authentik
Scopes: openid, profile, email, groups
```

**Create Application**:
```
Name: BizOSaaS Admin Dashboard
Slug: bizosaas-admin
Provider: BizOSaaS Admin Dashboard Provider
Launch URL: http://localhost:3004
```

#### Application 2: Client Portal

**Create OAuth2/OIDC Provider**:
```
Name: BizOSaaS Client Portal Provider
Authorization flow: default-authorization-flow
Client type: Confidential
Client ID: bizosaas-client-portal
Client Secret: <generate and save>
Redirect URIs:
  - http://localhost:3003/api/auth/callback/authentik
  - https://your-vps-domain.com/api/auth/callback/authentik
Scopes: openid, profile, email, groups
```

**Create Application**:
```
Name: BizOSaaS Client Portal
Slug: bizosaas-client
Provider: BizOSaaS Client Portal Provider
Launch URL: http://localhost:3003
```

#### Application 3: Brain Gateway API

**Create OAuth2/OIDC Provider**:
```
Name: BizOSaaS Brain Gateway Provider
Authorization flow: default-authorization-flow
Client type: Confidential
Client ID: bizosaas-brain-gateway
Client Secret: <generate and save>
Redirect URIs: N/A (API only)
Scopes: openid, profile, email, groups
```

---

### Step 3: Create Groups and Assign Permissions

**Create Groups**:
```
1. super_admin
   - Description: Full platform access
   - Attributes: { "permissions": ["*"] }

2. platform_admin
   - Description: Platform management
   - Attributes: { "permissions": ["tenants:*", "monitoring:*", "analytics:*"] }

3. tenant_admin
   - Description: Tenant administration
   - Attributes: { "permissions": ["tenant:manage", "users:manage"] }

4. tenant_user
   - Description: Regular tenant user
   - Attributes: { "permissions": ["tenant:view"] }
```

**Assign Users to Groups**:
- Create test users
- Assign to appropriate groups

---

### Step 4: Update Environment Variables

#### Admin Dashboard

**File**: `portals/admin-dashboard/.env.local`

```env
# Authentik SSO Configuration
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<from-authentik-step-2>
AUTH_SECRET=<generate-with-openssl-rand-base64-32>

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000

# NextAuth
NEXTAUTH_URL=http://localhost:3004
NEXTAUTH_URL_INTERNAL=http://localhost:3004
```

#### Client Portal

**File**: `portals/client-portal/.env.local`

```env
# Authentik SSO Configuration
AUTHENTIK_ISSUER=http://localhost:9000/application/o/bizosaas-client/
AUTHENTIK_CLIENT_ID=bizosaas-client-portal
AUTHENTIK_CLIENT_SECRET=<from-authentik-step-2>
AUTH_SECRET=<generate-with-openssl-rand-base64-32>

# Brain Gateway
NEXT_PUBLIC_BRAIN_GATEWAY_URL=http://localhost:8000

# NextAuth
NEXTAUTH_URL=http://localhost:3003
NEXTAUTH_URL_INTERNAL=http://localhost:3003
```

#### Brain Gateway

**File**: `bizosaas-brain-core/brain-gateway/.env`

```env
# Authentik Configuration
AUTHENTIK_URL=http://authentik-server:9000
AUTHENTIK_CLIENT_ID=bizosaas-brain-gateway
AUTHENTIK_CLIENT_SECRET=<from-authentik-step-2>
```

---

### Step 5: Update Client Portal with Authentik Integration

**Check if client portal already has NextAuth configured**:
```bash
ls -la portals/client-portal/lib/auth.ts
ls -la portals/client-portal/app/api/auth/
```

**If not configured, create similar to admin dashboard**:
- Copy auth configuration from admin dashboard
- Update client ID and issuer
- Update middleware for tenant-level RBAC

---

### Step 6: VPS Integration

**Same Authentik instance for VPS**:

1. **Update Redirect URIs in Authentik**:
   - Add VPS domain to redirect URIs
   - Example: `https://bizosaas.yourdomain.com/api/auth/callback/authentik`

2. **Update Environment Variables on VPS**:
   ```env
   AUTHENTIK_ISSUER=https://auth.yourdomain.com/application/o/bizosaas-admin/
   NEXTAUTH_URL=https://admin.yourdomain.com
   ```

3. **Use Same Authentik Database**:
   - Backup local Authentik database
   - Restore on VPS
   - Or configure Authentik to use external PostgreSQL

---

## 🚀 Execution Steps (Local Development)

### Step 1: Start Authentik (5 min)

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas-brain-core
docker compose -f docker-compose.authentik.yml up -d

# Wait for Authentik to be ready
docker compose -f docker-compose.authentik.yml logs -f authentik-server
# Look for: "Application startup complete"
```

**Access**: `http://localhost:9000`

---

### Step 2: Configure Authentik (15 min)

1. First-time setup (if needed)
2. Create 3 OAuth providers (admin, client, brain)
3. Create 3 applications
4. Create 4 groups
5. Create test users
6. Assign users to groups

---

### Step 3: Update Environment Files (5 min)

```bash
# Admin Dashboard
cd portals/admin-dashboard
cp .env.example .env.local
# Edit .env.local with Authentik credentials

# Client Portal (if needed)
cd ../client-portal
# Update .env.local with Authentik credentials

# Brain Gateway
cd ../../bizosaas-brain-core/brain-gateway
# Update .env with Authentik credentials
```

---

### Step 4: Update Startup Script (5 min)

**Edit**: `scripts/start-bizosaas-core-full.sh`

Add Authentik startup after infrastructure step.

---

### Step 5: Test Integration (10 min)

```bash
# Start everything
./scripts/start-bizosaas-core-full.sh --wait

# Test Admin Dashboard
# Navigate to http://localhost:3004
# Should redirect to Authentik login
# Login and verify redirect back

# Test Client Portal
# Navigate to http://localhost:3003
# Should redirect to Authentik login
# Login and verify redirect back
```

---

## 📊 Architecture Benefits

### Single Sign-On (SSO)
- ✅ One login for all portals
- ✅ Centralized user management
- ✅ MFA support
- ✅ Session management

### Security
- ✅ OAuth 2.0 / OIDC standard
- ✅ Secure token validation
- ✅ Role-based access control
- ✅ Audit logging

### Scalability
- ✅ Same Authentik for local + VPS
- ✅ Easy to add new applications
- ✅ Centralized group management
- ✅ Can integrate with external IdPs (Google, GitHub, etc.)

---

## 🎯 Next Steps (Priority Order)

### Immediate (Today)
1. ✅ Start Authentik locally
2. ✅ Configure 3 applications in Authentik
3. ✅ Update environment variables
4. ✅ Test admin dashboard login
5. ✅ Test client portal login (if configured)

### Short-term (This Week)
1. ⏳ Update startup script to include Authentik
2. ⏳ Configure client portal with Authentik (if not done)
3. ⏳ Test end-to-end authentication flow
4. ⏳ Document Authentik configuration

### Medium-term (Next Week)
1. ⏳ Deploy Authentik to VPS
2. ⏳ Update redirect URIs for production
3. ⏳ Configure SSL/TLS
4. ⏳ Backup Authentik database

---

## 📁 Files to Update

### Startup Script
- `scripts/start-bizosaas-core-full.sh` - Add Authentik startup

### Environment Files
- `portals/admin-dashboard/.env.local` - Authentik credentials
- `portals/client-portal/.env.local` - Authentik credentials (if needed)
- `bizosaas-brain-core/brain-gateway/.env` - Authentik credentials

### Client Portal (If Not Configured)
- `portals/client-portal/lib/auth.ts` - NextAuth configuration
- `portals/client-portal/middleware.ts` - Auth middleware
- `portals/client-portal/app/login/page.tsx` - Login page

---

## ✅ Success Criteria

- [ ] Authentik running on port 9000
- [ ] 3 applications configured in Authentik
- [ ] 4 groups created with permissions
- [ ] Admin dashboard login via Authentik working
- [ ] Client portal login via Authentik working (if applicable)
- [ ] Brain Gateway validates tokens via Authentik
- [ ] Startup script includes Authentik
- [ ] VPS integration documented

---

## 🔗 Resources

- **Authentik Docs**: https://goauthentik.io/docs/
- **Authentik UI**: http://localhost:9000
- **Admin Dashboard**: http://localhost:3004
- **Client Portal**: http://localhost:3003
- **Brain Gateway**: http://localhost:8000

---

## 🎉 Conclusion

**Good News**: Authentik is already implemented and ready to use!

**Action Plan**:
1. Start Authentik with existing docker-compose
2. Configure applications in Authentik UI
3. Update environment variables
4. Test authentication flows
5. Update startup script
6. Deploy to VPS with same configuration

**No need to rebuild** - just configure and integrate!
