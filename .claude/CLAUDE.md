# Bizoholic AI Marketing Agency Platform

## Domain Knowledge
- AI-powered marketing automation
- Client onboarding and campaign management
- CrewAI and LangChain integration
- WordPress frontend with n8n backend automation
- Integrated with BizOSaaS platform

## Current Architecture
- WordPress frontend (bizoholic.com)
- n8n workflows for marketing automation
- AI agent integration for campaign optimization
- Client portal and dashboard
- BizOSaaS backend integration

## Development Priorities
1. AI agent workflow optimization
2. Client onboarding automation
3. Campaign performance analytics
4. Integration with BizOSaaS platform
5. NextJS migration for better AI integration

## AI Integration
- CrewAI for agent orchestration
- LangChain for AI workflow management
- Custom AI models for marketing optimization
- Automated content generation

## BizOSaaS Integration
- Shared authentication system
- Common client database
- Unified analytics dashboard
- Cross-platform data synchronization

## K3s Deployment Approach (IMPORTANT)

### Golden Rules for K3s Development
1. **Build with Docker**: Use Docker to build container images
2. **Deploy with K3s**: Use kubectl and K8s manifests (NOT docker-compose)
3. **Monitor with Lens**: Use Lens Desktop on Windows 11 for monitoring
4. **Local Registry**: Push images to local registry for K3s access

### Deployment Workflow
```bash
# 1. Build container images (Docker)
docker build -t localhost:5000/bizosaas/service:tag ./path/to/service

# 2. Push to local registry (K3s access)
docker push localhost:5000/bizosaas/service:tag

# 3. Deploy to K3s cluster (NOT docker-compose)
kubectl apply -f k8s/manifests/

# 4. Monitor with Lens Desktop
# Open Lens → ~/.kube/config → bizosaas-dev namespace
```

### Technology Stack
- **Orchestration**: K3s (lightweight Kubernetes)
- **Cache**: Dragonfly (25x faster than Redis for AI)
- **Search**: Meilisearch (96% less memory than Elasticsearch)
- **Vector DB**: pgvector (inside PostgreSQL)
- **Frontend**: Next.js 14 with ShadCN UI
- **Backend**: FastAPI with DDD principles
- **AI**: CrewAI + LangChain
- **Monitoring**: Lens Desktop on Windows 11

### Module Reuse Strategy
- **Authentication**: fastapi-users (reuse)
- **CRM**: Fork from amoca-education/crm-fastapi-react
- **Analytics**: Cube.js (JavaScript, better for embedded)
- **CMS**: Strapi (Node.js, good plugin ecosystem)
- **Payments**: Multi-gateway (Stripe, PayPal, Razorpay, PayU)

### Task Tracking
- **Master Document**: `/bizosaas/docs/MASTER_TASK_LIST.md`
- **Phase Details**: `/bizosaas/docs/phases/PHASE_X_TASKS.md`
- **Architecture**: `/bizosaas/docs/ARCHITECTURE.md`

## 🚨 CRITICAL: Container Image Reuse Policy (MANDATORY)

**ZERO REDUNDANCY RULE**: Before creating ANY new Docker images or containers, MUST analyze existing images and reuse 100% wherever possible.

### Existing Container Inventory (Updated Sept 20, 2025)
**Running Containers:**
- `bizosaas-elasticsearch` (healthy) - Port 9200:9200, 9300:9300
- `sqladmin-dashboard` (restarting) - needs dependency fix
- `bizosaas-admin-3000` (unhealthy) - Port 3000:8080 
- `bizosaas-auth-v2-8007` (restarting) - needs schema fix
- `bizosaas-brain-8001` (healthy) - Port 8001:8001
- `wagtail-cms-8006` (healthy) - Port 8006:8000
- `bizosaas-saleor-db-5433` (healthy) - Port 5433:5432
- `bizosaas-saleor-redis-6380` (healthy) - Port 6380:6379
- `bizosaas-redis-6379` (healthy) - Port 6379:6379
- `bizosaas-vault-8200` (unhealthy) - Port 8200:8200

**Available Images for Reuse:**
- `bizosaas/auth-service-v2:latest` (608MB) - ✅ REUSE
- `bizosaas/brain-gateway:latest` (609MB) - ✅ REUSE  
- `bizosaas/wagtail-cms:latest` (1.06GB) - ✅ REUSE
- `bizosaas/sqladmin-dashboard:latest` (1.05GB) - ✅ REUSE
- `bizosaas/tailadmin-v2-unified:latest` (303MB) - ✅ REUSE
- `bizoholic-bizoholic-frontend:latest` (234MB) - ✅ REUSE
- `bizoholic-coreldove-frontend:latest` (234MB) - ✅ REUSE
- `bizosaas/amazon-sourcing:latest` (334MB) - ✅ REUSE
- `bizosaas/ai-agents:latest` (604MB) - ✅ REUSE
- `bizosaas/crm:latest` (894MB) - ✅ REUSE
- `ghcr.io/saleor/saleor:3.20` (1.46GB) - ✅ REUSE
- `postgres:15-alpine` (391MB) - ✅ REUSE
- `redis:7-alpine` (60.6MB) - ✅ REUSE

**🚫 FORBIDDEN ACTIONS:**
1. Creating new images when existing ones can be reused
2. Building redundant services without checking inventory
3. Deploying duplicate functionality across containers
4. Ignoring existing healthy services

**✅ MANDATORY PROCESS:**
1. Check existing images with `docker images`
2. Verify container functionality with `docker ps`
3. Reuse and fix existing containers FIRST
4. Only create new images if absolutely no alternative exists
5. Document any new images in this inventory

**Implementation Priority:**
1. Fix failing containers using existing images
2. Eliminate redundant containers
3. Consolidate overlapping services
4. Optimize resource usage across platform