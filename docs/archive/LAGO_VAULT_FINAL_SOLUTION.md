# 📋 Implementation Plan: Permanent Vault-Based Lago Fix

This document outlines the final, production-ready solution for the Lago Billing Engine. It moves away from local environment variables to a centralized, Vault-first architecture, ensuring security, resiliency across restarts, and zero configuration drift.

## 🏗️ Architecture Overview

1.  **Source of Truth**: All sensitive and configuration data for Lago is moved to **HashiCorp Vault** (`brain-vault`).
2.  **Runtime Initialization**: A robust startup script fetches all necessary environment variables from Vault before launching the Ruby on Rails application.
3.  **Database Integrity**: The database password mismatch issue (caused by volume persistence vs. configuration changes) is resolved by standardizing on Vault-managed credentials and performing a clean volume reset.
4.  **Health-First Lifecycle**: Enhanced Docker Compose health checks ensure services only start when their dependencies (Database, Redis, Migrations) are truly ready.

---

## 🛠️ Step-by-Step Implementation

### Phase 1: Seed Vault with Lago Environment
I will store the complete set of required environment variables in a single Vault path for efficient fetching.

**Path**: `bizosaas/lago/env`
**Keys**:
- `LAGO_POSTGRES_DB`
- `LAGO_POSTGRES_USER`
- `LAGO_POSTGRES_PASSWORD`
- `LAGO_DATABASE_URL`
- `LAGO_REDIS_URL`
- `LAGO_SECRET_KEY_BASE`
- `LAGO_ENCRYPTION_PRIMARY_KEY`
- `LAGO_ENCRYPTION_DETERMINISTIC_KEY`
- `LAGO_ENCRYPTION_KEY_DERIVATION_SALT`
- `RAILS_ENV`
- `LAGO_API_URL`
- `LAGO_FRONT_URL`

### Phase 2: Deploy Enhanced Init Script
A new script `scripts/lago-init-all-from-vault.sh` will replace the specific RSA fetch script. It will:
1.  Fetch the entire JSON object from `bizosaas/lago/env`.
2.  Parse and export every key as an environment variable.
3.  Fetch the RSA key and handle the Base64 encoding.
4.  Execute the original Lago command.

### Phase 3: Cleanup and Reset
To resolve the `PG::ConnectionBad: password authentication failed` error:
1.  Stop all Lago services.
2.  Remove existing `lago-db-data` volume (this wipes the old corrupted/password-mismatched data).
3.  Deploy the new configuration.

### Phase 4: Re-Deployment
Update `docker-compose.lago.yml` to:
- Use the new init script for `lago-api`, `lago-worker`, and `lago-migrate`.
- Ensure `lago-db` health check is correctly configured to prevent "race condition" failures.

---

## 🔐 Vault Seeding Command (for reference)
```bash
docker exec brain-vault sh -c "export VAULT_ADDR=http://127.0.0.1:8200 && export VAULT_TOKEN=staging-root-token-bizosaas-2025 && \
vault kv put bizosaas/lago/env \
  LAGO_POSTGRES_DB=lago \
  LAGO_POSTGRES_USER=lago \
  LAGO_POSTGRES_PASSWORD=lago_password_2025 \
  LAGO_DATABASE_URL=postgresql://lago:lago_password_2025@lago-db:5432/lago \
  LAGO_REDIS_URL=redis://lago-redis:6379/1 \
  LAGO_SECRET_KEY_BASE=b871ed19c83665268c74149028bfdf3787727402660161421715423877960786 \
  LAGO_ENCRYPTION_PRIMARY_KEY=b871ed19c83665268c74149028bfdf37 \
  LAGO_ENCRYPTION_DETERMINISTIC_KEY=c4772099e0df28646077558667c29579 \
  LAGO_ENCRYPTION_KEY_DERIVATION_SALT=5c72d9e685f02604297135317769532e \
  RAILS_ENV=production \
  LAGO_API_URL=https://billing-api.bizoholic.net \
  LAGO_FRONT_URL=https://billing.bizoholic.net"
```

## 🚀 Post-Implementation Checklist
1. Verify `lago-migrate` exits with code 0.
2. Verify `lago-api` is "Up" and responding to health checks.
3. Login at `https://billing.bizoholic.net` with credentials from `credentials.md`.
4. Verify data persistence by restarting the `lago-api` container.
