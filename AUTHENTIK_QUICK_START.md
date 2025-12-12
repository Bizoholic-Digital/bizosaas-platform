# 🚀 Quick Start - Authentik Configuration

## ✅ Status: Authentik Running & Ready

```
✓ Authentik Server:    HEALTHY (http://localhost:9000)
✓ Admin Dashboard:     RUNNING (http://localhost:3004)
✓ Configuration Guide: AUTHENTIK_SETUP_GUIDE.md
```

---

## 📋 Quick Configuration Checklist

### 1. Access Authentik
- [ ] Open http://localhost:9000
- [ ] Complete first-time setup OR login with `akadmin`

### 2. Create Admin Dashboard App
- [ ] Navigate to: Applications → Providers → Create
- [ ] Create OAuth2/OIDC Provider:
  - Name: `BizOSaaS Admin Dashboard Provider`
  - Client ID: `bizosaas-admin-dashboard`
  - Client Secret: **SAVE THIS!**
  - Redirect URI: `http://localhost:3004/api/auth/callback/authentik`
- [ ] Create Application:
  - Name: `BizOSaaS Admin Dashboard`
  - Slug: `bizosaas-admin`

### 3. Create Groups
- [ ] `super_admin` (full platform access)
- [ ] `platform_admin` (platform management)
- [ ] `tenant_acme_admin` (example tenant admin)
- [ ] `tenant_acme_user` (example tenant user)

### 4. Create Test Users
- [ ] `superadmin` → group: `super_admin`
- [ ] `platformadmin` → group: `platform_admin`
- [ ] `acmeadmin` → group: `tenant_acme_admin`
- [ ] `acmeuser` → group: `tenant_acme_user`

### 5. Update Environment
```bash
cd portals/admin-dashboard
cp .env.example .env.local
# Edit .env.local with Client Secret from Step 2
# Generate AUTH_SECRET: openssl rand -base64 32
```

### 6. Restart & Test
```bash
# Restart admin dashboard (Ctrl+C then)
npm run dev

# Test: http://localhost:3004
# Should redirect to Authentik login
```

---

## 🔑 Key Information

### Authentik URLs
- **Admin UI**: http://localhost:9000
- **Admin Dashboard**: http://localhost:3004
- **Client Portal**: http://localhost:3003

### Application Slugs
- **Admin Dashboard**: `bizosaas-admin`
- **Client Portal**: `bizosaas`

### Redirect URIs
- **Admin**: `http://localhost:3004/api/auth/callback/authentik`
- **Client**: `http://localhost:3003/api/auth/callback/authentik`

---

## 📚 Documentation

- **Detailed Guide**: `AUTHENTIK_SETUP_GUIDE.md` (step-by-step with screenshots)
- **Architecture**: `UNIFIED_AUTHENTIK_CONFIG.md` (complete architecture)
- **Status**: `AUTHENTIK_FINAL_STATUS.md` (current status)

---

## ⚡ Quick Commands

```bash
# Start Authentik
cd bizosaas-brain-core
docker compose -f docker-compose.authentik.yml up -d

# Check Authentik status
docker ps --filter "name=authentik"

# View Authentik logs
docker compose -f docker-compose.authentik.yml logs -f authentik-server

# Restart Authentik
docker compose -f docker-compose.authentik.yml restart

# Stop Authentik
docker compose -f docker-compose.authentik.yml down

# Generate AUTH_SECRET
openssl rand -base64 32
```

---

## 🎯 Next Action

**Open**: http://localhost:9000

**Follow**: `AUTHENTIK_SETUP_GUIDE.md` for detailed step-by-step instructions

**Time Required**: ~30 minutes

---

## ✅ Success Criteria

- [ ] Can login to Authentik admin UI
- [ ] Admin dashboard app created
- [ ] Groups and users created
- [ ] .env.local updated
- [ ] Can login to admin dashboard via SSO
- [ ] RBAC working (different access for different roles)

---

**Ready? Start here**: http://localhost:9000
