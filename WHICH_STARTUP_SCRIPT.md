# 🚀 BizOSaaS Startup Scripts - Which One to Use?

## Quick Answer

**Use `start-bizosaas-full.sh`** for the Client Portal integration work!

---

## 📊 Comparison

### `start-bizosaas-full.sh` ✅ RECOMMENDED
**Purpose**: Starts the complete BizOSaaS platform with Client Portal

**What it starts**:
1. **Infrastructure**: PostgreSQL, Redis
2. **Auth Service** (Port 8008) - SSO Authentication
3. **Brain Gateway** (Port 8001) - Centralized API Gateway
4. **Bizoholic Frontend** (Port 3001) - Public website
5. **Client Portal** (Port 3003) - Dashboard we just built ✨

**Use when**:
- Testing the Client Portal Dashboard
- Working on CRM, CMS, E-commerce, Marketing, Analytics integrations
- Testing Admin Dashboard
- Testing multi-tenant features
- Full platform development

**Access Points**:
- Bizoholic Frontend: `http://localhost:3001`
- **Client Portal**: `http://localhost:3003` ✨
- Client Portal Login: `http://localhost:3003/login`
- Brain Gateway: `http://localhost:8001`
- Auth Service: `http://localhost:8008`

---

### `start-bizoholic-full.sh`
**Purpose**: Starts Bizoholic brand services with Docker containers

**What it starts**:
1. **Infrastructure**: PostgreSQL, Redis, Vault
2. **Backend Services** (Docker containers):
   - Brain Gateway
   - Auth Service
   - Django CRM
   - Wagtail CMS
3. **Bizoholic Frontend** (Port 3001)

**Use when**:
- Testing Bizoholic frontend only
- Working on Wagtail CMS content
- Testing Docker container deployments
- Don't need Client Portal

**Access Points**:
- Bizoholic Frontend: `http://localhost:3001`
- Backend services run in Docker

---

## 🎯 For Your Current Work

Since you're working on the **Client Portal Dashboard** with:
- CRM integration
- CMS integration
- E-commerce integration
- Marketing integration
- Analytics integration
- **Admin Dashboard** ✨

**You should use**: `start-bizosaas-full.sh`

---

## 🚀 How to Start

```bash
cd /home/alagiri/projects/bizosaas-platform

# Use this one for Client Portal work ✅
./scripts/start-bizosaas-full.sh
```

---

## 📝 What Gets Started

### With `start-bizosaas-full.sh`:

```
┌─────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE                        │
│  - PostgreSQL (5432)                                    │
│  - Redis (6379)                                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  BACKEND SERVICES                        │
│  - Auth Service (8008)    - SSO Authentication          │
│  - Brain Gateway (8001)   - API Gateway                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                     FRONTENDS                            │
│  - Bizoholic (3001)       - Public Website              │
│  - Client Portal (3003)   - Dashboard ✨                │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 Login Credentials

Once started, you can login to the Client Portal:

**Admin User**:
- URL: `http://localhost:3003/login`
- Email: `admin@bizoholic.com`
- Password: `AdminDemo2024!`

**Client User**:
- URL: `http://localhost:3003/login`
- Email: `client@bizosaas.com`
- Password: `ClientDemo2024!`

**Superadmin** (for Admin Dashboard):
- URL: `http://localhost:3003/login`
- Email: `superadmin@bizosaas.com`
- Password: `SuperAdmin2024!`

---

## 📊 Service Verification

After starting, the script will verify:
- ✅ Auth Service (8008) - Health check
- ✅ Brain Gateway (8001) - Health check
- ✅ Bizoholic Frontend (3001) - Accessibility
- ✅ Client Portal (3003) - Login page

---

## 📝 Logs

View logs for debugging:

```bash
# Auth Service
tail -f /tmp/auth-service.log

# Brain Gateway
tail -f /tmp/brain-gateway.log

# Bizoholic Frontend
tail -f /tmp/bizoholic-frontend.log

# Client Portal
tail -f /tmp/client-portal.log
```

---

## 🛑 How to Stop

```bash
# Stop all services
kill $(cat /tmp/*.pid 2>/dev/null) 2>/dev/null || true

# Stop infrastructure
docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml down
```

---

## ⚠️ Important Notes

1. **Port Conflicts**: The script automatically kills processes on ports 8008, 8001, 3001, 3003
2. **Startup Time**: Wait ~15 seconds for Auth Service to fully initialize
3. **Database**: PostgreSQL must be running before services start
4. **Node Modules**: Ensure `npm install` has been run in both frontend directories

---

## 🎯 Summary

**For Client Portal Development** → Use `start-bizosaas-full.sh` ✅

This script:
- Starts everything you need
- Includes the Client Portal on port 3003
- Runs Auth Service and Brain Gateway locally (not in Docker)
- Perfect for development and testing

**For Bizoholic-only work** → Use `start-bizoholic-full.sh`

This script:
- Starts Bizoholic frontend only
- Runs backend services in Docker
- No Client Portal
- Good for content/CMS work
