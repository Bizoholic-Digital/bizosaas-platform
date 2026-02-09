# Missing Dockerfiles - Action Required

## Issue
The `./scripts/start-bizoholic.sh` script failed because backend service Dockerfiles are missing:

```
unable to prepare context: unable to evaluate symlinks in Dockerfile path: 
lstat /home/alagiri/projects/bizosaas-platform/shared/services/brain-gateway/Dockerfile: no such file or directory
```

## Missing Dockerfiles

### Backend Services
- ❌ `shared/services/brain-gateway/Dockerfile`
- ❌ `shared/services/auth/Dockerfile`
- ❌ `shared/services/cms/Dockerfile`
- ❌ `shared/services/crm/Dockerfile`
- ❌ `shared/services/ai-agents/Dockerfile`
- ❌ `shared/services/temporal-integration/Dockerfile`
- ❌ `shared/services/business-directory/Dockerfile`

### Brand Backends
- ❌ `brands/coreldove/backend/Dockerfile`
- ❌ `brands/quanttrade/backend/Dockerfile`

## Current Workaround: Local Development Without Docker

Since Dockerfiles are missing, use **local development mode** instead:

### 1. Start Infrastructure Only
```bash
docker compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d
```

### 2. Run Frontends Locally (npm run dev)
```bash
# Bizoholic
cd brands/bizoholic/frontend && PORT=3001 npm run dev

# Client Portal
cd portals/client-portal && PORT=3003 npm run dev
```

### 3. Run Backends Locally (when needed)
```bash
# Brain Gateway (Python/FastAPI)
cd shared/services/brain-gateway
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8001

# CMS (Django/Wagtail)
cd shared/services/cms
python manage.py runserver 8002
```

## Solution Options

### Option A: Restore from Archive (Recommended)
```bash
# Check if Dockerfiles exist in archive
find _archive/legacy_projects -name "Dockerfile" -path "*/brain-gateway/*"
find _archive/legacy_projects -name "Dockerfile" -path "*/auth/*"

# Copy them to new locations
cp _archive/legacy_projects/.../brain-gateway/Dockerfile shared/services/brain-gateway/
```

### Option B: Create New Dockerfiles

#### Python Services (Brain, CMS, CRM)
```dockerfile
# shared/services/brain-gateway/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8001

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

#### Node.js Services (Auth)
```dockerfile
# shared/services/auth/Dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application
COPY . .

# Expose port
EXPOSE 8007

# Run application
CMD ["node", "server.js"]
```

## Immediate Action Plan

### Phase 1: Local Development (Current)
✅ Use npm run dev for frontends
✅ Use .env.local for configuration
✅ Skip Docker for now

### Phase 2: Restore Dockerfiles
1. Search archive for Dockerfiles
2. Copy to new locations
3. Update paths if needed
4. Test builds

### Phase 3: Containerized Testing
1. Build images: `./scripts/build-frontends-sequential.sh`
2. Test with smart scripts: `./scripts/smart-start-bizoholic.sh`
3. Verify all services work

## Current Status

**Working:**
- ✅ Infrastructure (Postgres, Redis, Vault) via Docker
- ✅ Frontends via npm run dev
- ✅ .env.local configuration

**Not Working:**
- ❌ Backend services via Docker (missing Dockerfiles)
- ❌ Full containerized stack

**Next Step:**
Continue with local development (frontends + infrastructure) until Dockerfiles are restored.
