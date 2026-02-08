# Quick Setup Guide - Restore Frontends & Start Local Dev

## Current Situation

After reorganization, brand frontends are missing from the new structure:
- `brands/bizoholic/` - Only has `backend/`, missing `frontend/`
- `brands/coreldove/frontend/` - Exists ✅
- `brands/thrillring/frontend/` - Exists ✅  
- `brands/quanttrade/frontend/` - Exists ✅

Frontends are located in `_archive/legacy_projects/frontend/apps/` and need to be restored.

## Step 1: Restore Missing Frontends

```bash
# Restore Bizoholic Frontend
cp -r _archive/legacy_projects/bizosaas/frontend/apps/bizoholic-frontend brands/bizoholic/frontend

# Verify restoration
ls -la brands/bizoholic/frontend/
```

## Step 2: Verify All Frontends Have package.json

```bash
# Check all frontends
find brands portals -name "package.json" -path "*/node_modules" -prune -o -name "package.json" -type f -print | grep -v node_modules
```

Expected output:
- `portals/client-portal/package.json` ✅
- `portals/admin-portal/bizosaas-admin/package.json` ✅
- `portals/business-directory/business-directory/package.json` ✅
- `brands/bizoholic/frontend/package.json` ⚠️ (needs restoration)
- `brands/coreldove/frontend/package.json` ✅
- `brands/thrillring/frontend/package.json` ✅
- `brands/quanttrade/frontend/package.json` ✅

## Step 3: Install Dependencies

```bash
# Install for all portals
cd portals/client-portal && npm install && cd ../..
cd portals/admin-portal/bizosaas-admin && npm install && cd ../../..
cd portals/business-directory/business-directory && npm install && cd ../../..

# Install for all brands
cd brands/bizoholic/frontend && npm install && cd ../../..
cd brands/coreldove/frontend && npm install && cd ../../..
cd brands/thrillring/frontend && npm install && cd ../../..
cd brands/quanttrade/frontend && npm install && cd ../../..
```

## Step 4: Start Local Development

```bash
# Start infrastructure
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis vault

# Start Client Portal (test one first)
cd portals/client-portal
PORT=3003 npm run dev
```

Access at: http://localhost:3003

## Step 5: Test Other Frontends

Once Client Portal works, test others:

```bash
# Admin Portal
cd portals/admin-portal/bizosaas-admin
PORT=3009 npm run dev

# Bizoholic
cd brands/bizoholic/frontend
PORT=3001 npm run dev

# CoreLDove
cd brands/coreldove/frontend
PORT=3002 npm run dev
```

## Step 6: Once All Work Locally → Containerize

```bash
# Build Docker images
./scripts/build-frontends-sequential.sh

# Test containerized
./scripts/start-bizoholic.sh
```

## Step 7: Push to GHCR

```bash
# Tag and push (after testing)
docker tag bizosaas/client-portal:latest ghcr.io/bizoholic-digital/client-portal:latest
docker push ghcr.io/bizoholic-digital/client-portal:latest
# ... repeat for all services
```

---

**Current Priority:** Restore `brands/bizoholic/frontend/` and test local development before containerization.
