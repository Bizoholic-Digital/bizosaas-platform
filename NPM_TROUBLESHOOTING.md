# NPM Dependency Issues - Resolution Guide

## Issue: React Version Conflicts

### Problem
All frontends use React 19, but `lucide-react@0.300.0` requires React 18, causing peer dependency conflicts.

### Solution
Use `--legacy-peer-deps` flag for all npm commands:

```bash
# Install dependencies
npm install --legacy-peer-deps

# Audit fix
npm audit fix --legacy-peer-deps

# Add new packages
npm install <package-name> --legacy-peer-deps
```

## Security Vulnerabilities Fixed

### Before
```
2 vulnerabilities (1 moderate, 1 high)
- glob: Command injection (high)
- js-yaml: Prototype pollution (moderate)
```

### After
```bash
npm audit fix --legacy-peer-deps
# Result: found 0 vulnerabilities ✅
```

## All Frontends - Installation Commands

```bash
# Bizoholic
cd brands/bizoholic/frontend && npm install --legacy-peer-deps

# Client Portal  
cd portals/client-portal && npm install --legacy-peer-deps

# Admin Portal
cd portals/admin-portal/bizosaas-admin && npm install --legacy-peer-deps

# Business Directory
cd portals/business-directory/business-directory && npm install --legacy-peer-deps

# CoreLDove
cd brands/coreldove/frontend && npm install --legacy-peer-deps

# ThrillRing
cd brands/thrillring/frontend && npm install --legacy-peer-deps

# QuantTrade
cd brands/quanttrade/frontend && npm install --legacy-peer-deps
```

## Running Frontends Locally

```bash
# Bizoholic (port 3001)
cd brands/bizoholic/frontend && PORT=3001 npm run dev

# Client Portal (port 3003)
cd portals/client-portal && PORT=3003 npm run dev

# Admin Portal (port 3009)
cd portals/admin-portal/bizosaas-admin && PORT=3009 npm run dev

# Business Directory (port 3004)
cd portals/business-directory/business-directory && PORT=3004 npm run dev

# CoreLDove (port 3002)
cd brands/coreldove/frontend && PORT=3002 npm run dev

# ThrillRing (port 3005)
cd brands/thrillring/frontend && PORT=3005 npm run dev

# QuantTrade (port 3006)
cd brands/quanttrade/frontend && PORT=3006 npm run dev
```

## Currently Running

✅ **Infrastructure:**
- Postgres: localhost:5432
- Redis: localhost:6379
- Vault: localhost:8200

✅ **Frontends:**
- Bizoholic: http://localhost:3001
- Client Portal: http://localhost:3003

## Next Steps

1. Test both frontends in browser
2. Install dependencies for remaining frontends
3. Test all frontends locally
4. Once verified → Build Docker images
5. Push to GHCR
