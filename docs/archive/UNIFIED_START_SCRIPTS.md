# BizOSaaS Platform - Unified Start Scripts

## Overview

All brand start scripts now **automatically detect** whether to run in:
- **Full Docker Mode** (when Dockerfiles exist)
- **Local Dev Mode** (when Dockerfiles are missing)

## Usage

Simply run the script for any brand:

```bash
./scripts/start-bizoholic.sh
./scripts/start-coreldove.sh
./scripts/start-thrillring.sh
./scripts/start-quanttrade.sh
```

The script will:
1. ✅ Start infrastructure (Postgres, Redis, Vault)
2. ✅ Check if Dockerfiles exist
3. ✅ Auto-select Full Docker or Local Dev mode
4. ✅ Start brand-specific services

## Modes Explained

### Full Docker Mode (When Dockerfiles Exist)

**Bizoholic:**
- Infrastructure: Postgres, Redis, Vault
- Backends: Brain, Auth, CMS, CRM
- Frontend: Bizoholic (Docker)

**CoreLDove:**
- Infrastructure: Postgres, Redis
- Backends: Saleor
- Frontend + Backend: CoreLDove (Docker)

**ThrillRing:**
- Infrastructure: Postgres, Redis
- Backends: Brain Gateway
- Frontend: ThrillRing (Docker)

**QuantTrade:**
- Infrastructure: Postgres, Redis
- Frontend + Backend: QuantTrade (Docker)

### Local Dev Mode (When Dockerfiles Missing)

**All Brands:**
- Infrastructure: Postgres, Redis, Vault (Docker)
- Frontend: npm run dev (manual start)
- Backends: Pending Dockerfile restoration

## Current Status

Since Dockerfiles are currently missing, all scripts run in **Local Dev Mode**:

```bash
./scripts/start-bizoholic.sh
# Output:
# ⚠️  Dockerfiles not found - Starting LOCAL DEV MODE
# 📝 To start the frontend, run in a new terminal:
#    cd brands/bizoholic/frontend && PORT=3001 npm run dev
```

## When Dockerfiles Are Restored

Once you restore the Dockerfiles, the **same scripts** will automatically switch to Full Docker Mode:

```bash
./scripts/start-bizoholic.sh
# Output:
# ✅ Dockerfiles found - Starting FULL DOCKER MODE
# 🧠 Starting Shared Services (Brain, Auth, CMS, CRM)...
# 🌐 Starting Bizoholic Frontend (Docker)...
```

## Benefits

1. **No Script Changes Needed** - Same command works in both modes
2. **Automatic Detection** - Checks for Dockerfiles automatically
3. **Clear Feedback** - Shows which mode is running
4. **Graceful Degradation** - Works without Dockerfiles
5. **Future-Proof** - Automatically upgrades when Dockerfiles added

## Testing

### Test Current Setup (Local Dev Mode)
```bash
# Start infrastructure + get frontend command
./scripts/start-bizoholic.sh

# In new terminal, start frontend
cd brands/bizoholic/frontend && PORT=3001 npm run dev

# Access at http://localhost:3001
```

### Test After Dockerfile Restoration
```bash
# Will automatically use Docker for everything
./scripts/start-bizoholic.sh

# Access at http://localhost:3001 (no manual frontend start needed)
```

## Script Locations

- `scripts/start-bizoholic.sh` - Bizoholic (auto-detect mode)
- `scripts/start-coreldove.sh` - CoreLDove (auto-detect mode)
- `scripts/start-thrillring.sh` - ThrillRing (auto-detect mode)
- `scripts/start-quanttrade.sh` - QuantTrade (auto-detect mode)

## Deprecated Scripts

The following scripts are **no longer needed**:
- `scripts/local-dev-*.sh` - Functionality merged into `start-*.sh`
- `scripts/smart-start-*.sh` - Will be updated later for resource optimization

Use the unified `start-*.sh` scripts for all scenarios.
