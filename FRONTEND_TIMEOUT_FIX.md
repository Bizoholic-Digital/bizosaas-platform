# BizOSaaS - Local Development Quick Fix

## Issue: Frontend Timeout on Startup

### Problem
The Bizoholic frontend is timing out because it's trying to connect to backend services that aren't running:
- Brain API (port 8001)
- Wagtail CMS (port 8002)  
- Auth Service (port 8007)

### Quick Solution: Mock Backend URLs

Create a `.env.local` file to point to mock/unavailable backends gracefully:

```bash
cd brands/bizoholic/frontend

cat > .env.local << 'EOF'
# Local Development - Mock Backend
NEXT_PUBLIC_BRAIN_API_URL=http://localhost:8001
NEXT_PUBLIC_WAGTAIL_URL=http://localhost:8002
NEXT_PUBLIC_AUTH_API_URL=http://localhost:8007

# Disable SSR data fetching for local dev
NEXT_PUBLIC_ENABLE_SSR=false
EOF
```

### Better Solution: Start Backend Services

If you want full functionality, start the backend services:

```bash
# Option 1: Start all services with Docker
./scripts/start-bizoholic.sh

# Option 2: Start just the backends manually
docker compose -f shared/services/docker-compose.services.yml up -d brain-gateway auth cms
```

### Temporary Workaround: Static Mode

For now, you can test the frontend in static mode by:

1. **Wait for the compilation to complete** (it will retry and eventually load)
2. **Access the frontend** at http://localhost:3001
3. **Expect API errors** (this is normal without backends)
4. **UI should still render** (just without dynamic data)

## Current Status

✅ **Running:**
- Bizoholic Frontend: http://localhost:3001 (compiling...)
- Client Portal: http://localhost:3003
- Infrastructure: Postgres, Redis, Vault

⚠️ **Not Running:**
- Brain Gateway (port 8001)
- Wagtail CMS (port 8002)
- Auth Service (port 8007)
- Django CRM (port 8000)

## Recommended Next Steps

### Option A: Frontend-Only Testing (Fastest)
```bash
# Just wait for compilation to finish
# Test UI/UX without backend data
# Good for testing layouts, styles, navigation
```

### Option B: Full Stack Testing (Complete)
```bash
# Start all backend services
./scripts/start-bizoholic.sh

# This will start:
# - Infrastructure (already running ✅)
# - Brain Gateway
# - Auth Service
# - CMS
# - CRM
# - Bizoholic Frontend
```

### Option C: Selective Backend Testing
```bash
# Start only the backends you need
cd shared/services
docker compose -f docker-compose.services.yml up -d brain-gateway

# Then restart the frontend
cd brands/bizoholic/frontend
PORT=3001 npm run dev
```

## Why This Happens

The frontend is configured to fetch data from backend APIs during server-side rendering (SSR). When those APIs aren't available, Next.js retries the requests, causing the timeout warnings.

This is **expected behavior** in a microservices architecture when services aren't all running.
