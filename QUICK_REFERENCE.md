# BizOSaaS Platform - Quick Reference

## 🚀 Start All Services
```bash
./scripts/start-bizosaas-full.sh
```

## 🌐 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **Client Portal** | http://localhost:3003 | admin@bizoholic.com / AdminDemo2024! |
| **Bizoholic Frontend** | http://localhost:3001 | - |
| **Brain Gateway** | http://localhost:8001 | - |
| **Auth Service** | http://localhost:8008 | - |

## 🔐 Test Accounts

```
Admin:         admin@bizoholic.com / AdminDemo2024!
Client:        client@bizosaas.com / ClientDemo2024!
Super Admin:   superadmin@bizosaas.com / BizoSaaS2025!Admin
Tenant Admin:  administrator@bizosaas.com / Bizoholic2025!Admin
User:          user@bizosaas.com / Bizoholic2025!User
```

## 📝 View Logs

```bash
# Auth Service
tail -f /tmp/auth-service.log

# Brain Gateway
tail -f /tmp/brain-gateway.log

# Client Portal
tail -f /tmp/client-portal.log

# Bizoholic Frontend
tail -f /tmp/bizoholic-frontend.log
```

## 🛑 Stop All Services

```bash
# Stop Node processes
kill $(cat /tmp/*.pid 2>/dev/null) 2>/dev/null || true

# Stop Docker containers
docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml down
```

## 🔧 Troubleshooting

### Reset Admin Password
```bash
cd shared/services/auth
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"
python3 seed_test_users.py
```

### Check Service Status
```bash
# Check if ports are listening
lsof -i :3001  # Bizoholic Frontend
lsof -i :3003  # Client Portal
lsof -i :8001  # Brain Gateway
lsof -i :8008  # Auth Service
lsof -i :5432  # Postgres
lsof -i :6379  # Redis
```

### Restart Individual Service

**Auth Service:**
```bash
cd shared/services/auth
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"
export REDIS_URL="redis://localhost:6379/0"
uvicorn main:app --host 0.0.0.0 --port 8008 --reload
```

**Brain Gateway:**
```bash
cd shared/services/brain-gateway
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Client Portal:**
```bash
cd portals/client-portal
npm run dev -- --port 3003
```

**Bizoholic Frontend:**
```bash
cd brands/bizoholic/frontend
PORT=3001 npm run dev
```

## 📚 Documentation

- `BIZOSAAS_COMPLETE_SETUP_SUMMARY.md` - Complete setup guide
- `FIX_LOGIN_NOW.md` - Login credential fixes
- `LOGIN_REWRITE_FIX.md` - NextAuth rewrite fix
- `LOGIN_AND_DASHBOARD_FIX.md` - Dashboard protection
- `UNIFIED_LOGIN_AND_DASHBOARD_STRATEGY.md` - Architecture overview

## ✅ Current Status

**Working:**
- ✅ Login & Authentication
- ✅ Dashboard Protection
- ✅ Session Management
- ✅ CRM Fallback Data

**Pending:**
- ⚠️ Logout Button (needs implementation)
- ⚠️ Django CRM Service (optional - using fallback)
- ⚠️ Wagtail CMS Service (optional - using fallback)

## 🎯 Next Steps

1. **Implement Logout:**
   ```typescript
   import { signOut } from 'next-auth/react'
   <button onClick={() => signOut({ callbackUrl: '/login' })}>
     Sign Out
   </button>
   ```

2. **Start CRM/CMS (Optional):**
   ```bash
   docker-compose -f shared/services/docker-compose.services.yml up -d crm cms
   ```

3. **Test Full Flow:**
   - Access http://localhost:3003
   - Login with admin credentials
   - Navigate through dashboard tabs
   - Test logout functionality
