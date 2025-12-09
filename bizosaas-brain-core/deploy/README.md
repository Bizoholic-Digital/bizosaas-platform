# BizOSaaS Modular Deployment Guide

This directory contains the modular deployment configuration for the BizOSaaS platform, split into logical stacks for better maintainability, scalability, and independent deployments.

## 📦 Stack Architecture

### 1. Infrastructure Stack (`docker-compose.infra.yml`)
**Purpose**: Foundation services that rarely change
**Contains**:
- PostgreSQL (with pgvector)
- Redis
- HashiCorp Vault
- Temporal + Temporal UI

**Deploy First**: This stack must be deployed before others as it provides core dependencies.

### 2. Core Services Stack (`docker-compose.core.yml`)
**Purpose**: Backend API services
**Contains**:
- Brain Gateway (Main API)
- Auth Service
- GitHub MCP Server

**Deploy Second**: Depends on infrastructure stack for database and cache.

### 3. Frontend Stack (`docker-compose.frontend.yml`)
**Purpose**: User-facing applications
**Contains**:
- Client Portal (Next.js)
- Admin Portal (future)

**Deploy Third**: Depends on core services for API access.

## 🚀 Deployment Order in Dokploy

### Step 1: Create Infrastructure Service
1. Go to Dokploy → **Projects** → **Create New Project** → Name: `bizosaas-infra`
2. Add **Compose Service**:
   - **Name**: `infrastructure`
   - **Repository**: `https://github.com/Bizoholic-Digital/bizosaas-platform`
   - **Branch**: `staging`
   - **Compose Path**: `./bizosaas-brain-core/deploy/docker-compose.infra.yml`
   - **Environment Variables**:
     ```
     POSTGRES_PASSWORD=<your-secure-password>
     VAULT_TOKEN=<your-vault-token>
     ```
3. **Deploy** and wait for all services to be healthy

### Step 2: Create Core Services
1. Create New Project → Name: `bizosaas-core`
2. Add **Compose Service**:
   - **Name**: `core-services`
   - **Repository**: `https://github.com/Bizoholic-Digital/bizosaas-platform`
   - **Branch**: `staging`
   - **Compose Path**: `./bizosaas-brain-core/deploy/docker-compose.core.yml`
   - **Environment Variables**:
     ```
     POSTGRES_PASSWORD=<same-as-infra>
     JWT_SECRET=<your-jwt-secret>
     OPENAI_API_KEY=<your-openai-key>
     ANTHROPIC_API_KEY=<your-anthropic-key>
     GITHUB_TOKEN=<your-github-token>
     ```
3. **Deploy**

### Step 3: Create Frontend Services
1. Create New Project → Name: `bizosaas-frontend`
2. Add **Compose Service**:
   - **Name**: `client-portal`
   - **Repository**: `https://github.com/Bizoholic-Digital/bizosaas-platform`
   - **Branch**: `staging`
   - **Compose Path**: `./bizosaas-brain-core/deploy/docker-compose.frontend.yml`
   - **Environment Variables**:
     ```
     NEXTAUTH_SECRET=<your-nextauth-secret>
     AUTHENTIK_CLIENT_ID=<your-authentik-client-id>
     AUTHENTIK_CLIENT_SECRET=<your-authentik-client-secret>
     AUTHENTIK_ISSUER=<your-authentik-issuer>
     AUTHENTIK_URL=<your-authentik-url>
     ```
3. **Deploy**

## 🌐 Network Configuration

All stacks use two networks:
- **`brain-network`**: Internal communication between services (created by infrastructure stack)
- **`dokploy-network`**: External network for Traefik routing (managed by Dokploy)

The infrastructure stack **creates** `brain-network`, while core and frontend stacks **reference it as external**.

## 🔄 Update Strategy

### Infrastructure Updates (Rare)
```bash
# In Dokploy: bizosaas-infra → infrastructure → Redeploy
# ⚠️ This may cause brief downtime for dependent services
```

### Core Services Updates (Occasional)
```bash
# In Dokploy: bizosaas-core → core-services → Redeploy
# Frontend remains available during core updates
```

### Frontend Updates (Frequent)
```bash
# In Dokploy: bizosaas-frontend → client-portal → Redeploy
# Zero downtime if using blue-green deployment
```

## 📊 Resource Allocation

### Infrastructure Stack
- **Total**: ~1.5 CPU, ~1.5GB RAM
- Postgres: 0.5 CPU, 512MB
- Redis: 0.2 CPU, 256MB
- Vault: 0.2 CPU, 256MB
- Temporal: 0.5 CPU, 512MB
- Temporal UI: 0.2 CPU, 256MB

### Core Services Stack
- **Total**: ~1.0 CPU, ~1GB RAM
- Brain Gateway: 0.5 CPU, 512MB
- Auth Service: 0.3 CPU, 256MB
- GitHub MCP: 0.2 CPU, 256MB

### Frontend Stack
- **Total**: ~0.5 CPU, ~512MB RAM
- Client Portal: 0.5 CPU, 512MB

**Grand Total**: ~3 CPU, ~3GB RAM (well within VPS limits)

## 🔍 Monitoring & Logs

### View Logs for Each Stack
```bash
# Infrastructure
docker compose -f bizosaas-brain-core/deploy/docker-compose.infra.yml logs -f

# Core Services
docker compose -f bizosaas-brain-core/deploy/docker-compose.core.yml logs -f

# Frontend
docker compose -f bizosaas-brain-core/deploy/docker-compose.frontend.yml logs -f
```

### Health Checks
- Infrastructure: `http://your-server:5432` (Postgres), `http://your-server:6379` (Redis)
- Core: `https://api.bizoholic.net/health`, `https://auth-api.bizoholic.net/health`
- Frontend: `https://app.bizoholic.net`

## 🛠️ Troubleshooting

### Issue: "network brain-network not found"
**Solution**: Deploy infrastructure stack first. It creates the network.

### Issue: "cannot connect to postgres"
**Solution**: Ensure infrastructure stack is healthy before deploying core/frontend.

### Issue: Services can't communicate
**Solution**: Verify all stacks are using `brain-network` and it's marked as `external: true` in core/frontend.

## 📝 Environment Variables Reference

### Required for All Stacks
- `POSTGRES_PASSWORD`: Shared across infra and core

### Infrastructure Only
- `VAULT_TOKEN`: Vault root token

### Core Services Only
- `JWT_SECRET`: For auth service
- `OPENAI_API_KEY`: For AI features
- `ANTHROPIC_API_KEY`: For Claude integration
- `GITHUB_TOKEN`: For MCP GitHub integration

### Frontend Only
- `NEXTAUTH_SECRET`: NextAuth encryption key
- `AUTHENTIK_CLIENT_ID`: OAuth client ID
- `AUTHENTIK_CLIENT_SECRET`: OAuth client secret
- `AUTHENTIK_ISSUER`: OAuth issuer URL
- `AUTHENTIK_URL`: Authentik server URL

## 🎯 Benefits of This Architecture

1. **Independent Scaling**: Scale frontend without touching backend
2. **Faster Deployments**: Update only what changed
3. **Better Resource Management**: Monitor and limit resources per stack
4. **Easier Debugging**: Isolated logs and metrics per stack
5. **Production Ready**: Follows microservices best practices
6. **Cost Effective**: Deploy only what you need in each environment

## 🔐 Security Notes

- All secrets should be stored in Dokploy's environment variables (encrypted)
- Never commit `.env` files with real credentials
- Use Vault for runtime secret management
- Rotate credentials regularly
- Use strong, unique passwords for each service

## 📚 Additional Resources

- [Dokploy Documentation](https://docs.dokploy.com)
- [Docker Compose Networking](https://docs.docker.com/compose/networking/)
- [Traefik Configuration](https://doc.traefik.io/traefik/)
