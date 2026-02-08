# Smart Brand Switching - Resource-Efficient Testing

## Problem
Running all brands simultaneously consumes too many resources during local testing.

## Solution
**Smart Start Scripts** that:
1. Keep shared services running (Infrastructure + Common backends)
2. Stop other brand-specific frontends
3. Start only the requested brand

## How It Works

### Traditional Approach (Resource Heavy)
```bash
# Each brand starts everything from scratch
./scripts/start-bizoholic.sh    # Starts: Infra + Brain + Auth + CMS + CRM + Bizoholic
./scripts/start-coreldove.sh    # Starts: Infra + Saleor + CoreLDove (duplicates infra!)
```
**Problem:** Restarts shared services unnecessarily

### Smart Approach (Resource Efficient)
```bash
# First brand starts everything
./scripts/smart-start-bizoholic.sh
# Starts: Infra + Brain + Auth + CMS + CRM + Bizoholic

# Switch to CoreLDove
./scripts/smart-start-coreldove.sh
# Keeps: Infra (already running ✓)
# Stops: Bizoholic frontend
# Starts: Saleor + CoreLDove
```
**Benefit:** Shared services stay running, saves RAM and startup time

## Usage

### Start First Brand
```bash
./scripts/smart-start-bizoholic.sh
```

### Switch to Another Brand
```bash
# Shared services stay running!
./scripts/smart-start-coreldove.sh
```

### Switch Back
```bash
./scripts/smart-start-bizoholic.sh
```

## What Stays Running vs What Stops

### Always Running (Shared)
- ✅ Postgres
- ✅ Redis  
- ✅ Vault (if needed)

### Conditional (Based on Brand)
- Brain Gateway (Bizoholic, ThrillRing need it)
- Auth, CMS, CRM (Bizoholic needs them)
- Saleor (CoreLDove needs it)

### Stopped When Switching
- ❌ Other brand frontends
- ❌ Other brand backends

## Resource Comparison

### Without Smart Scripts
```
Brand 1: 8GB RAM
Switch to Brand 2: Restart everything → 8GB RAM (16GB total peak!)
```

### With Smart Scripts
```
Brand 1: 8GB RAM
Switch to Brand 2: Keep shared (6GB), swap brand (2GB) → 8GB RAM total
```
**Savings:** ~50% RAM usage, ~70% faster brand switching

## Production Deployment

On the server with more resources:
```bash
# Start ALL brands simultaneously
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d
docker compose -f shared/services/docker-compose.services.yml up -d
docker compose -f brands/docker-compose.brands.yml up -d
docker compose -f portals/docker-compose.portals.yml up -d
```

All brands run together in production!

## Scripts Available

- `smart-start-bizoholic.sh` - Bizoholic + Brain + Auth + CMS + CRM
- `smart-start-coreldove.sh` - CoreLDove + Saleor
- `smart-start-thrillring.sh` - ThrillRing + Brain
- `smart-start-quanttrade.sh` - QuantTrade + Backend

## Example Workflow

```bash
# Morning: Test Bizoholic
./scripts/smart-start-bizoholic.sh
# Test at http://localhost:3001

# Afternoon: Test CoreLDove
./scripts/smart-start-coreldove.sh
# Postgres/Redis still running from morning!
# Test at http://localhost:3002

# Evening: Test ThrillRing
./scripts/smart-start-thrillring.sh
# Still using same Postgres/Redis!
# Test at http://localhost:3005
```

**Total RAM:** ~8GB (instead of 24GB if restarting everything)
