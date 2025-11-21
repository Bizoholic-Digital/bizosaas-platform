# BizOSaaS Platform - Dokploy Deployment Strategy

## 🎯 **DEPLOYMENT STRUCTURE OVERVIEW**

Based on your existing Dokploy setup with `bizoholic-website`, `shared_infrastructure`, and `automation-hub`, here's the recommended structure for BizOSaaS platform deployment:

### **Current Dokploy Projects:**
1. **bizoholic-website** - WordPress frontend
2. **shared_infrastructure** - PostgreSQL, Dragonfly, CrewAI
3. **automation-hub** - n8n workflows

### **New BizOSaaS Project Structure:**
4. **bizosaas-platform** - Core BizOSaaS services
5. **bizosaas-storage** - Storage-only backend services
6. **bizosaas-frontend** - Next.js frontend applications

---

## 📋 **PROJECT 1: bizosaas-platform**
**Purpose**: Core BizOSaaS business logic and orchestration

### **Services:**
```yaml
# Service 1: bizosaas-brain (FastAPI)
name: bizosaas-brain
type: docker
image: bizosaas/brain:latest
port: 8001
environment:
  - POSTGRES_HOST=postgres
  - POSTGRES_PASSWORD=SharedInfra2024!SuperSecure
  - REDIS_HOST=redis
  - REDIS_PASSWORD=SecureRedis2024Unified
  - OPENROUTER_API_KEY=sk-or-v1-REDACTED
networks:
  - dokploy-network
volumes:
  - bizosaas-brain-data:/app/data
domain: api.bizoholic.com

# Service 2: unified-dashboard  
name: unified-dashboard
type: docker
image: bizosaas/dashboard:latest
port: 5004
environment:
  - BRAIN_API_URL=http://bizosaas-brain:8001
networks:
  - dokploy-network
domain: admin.bizoholic.com

# Service 3: image-integration
name: image-integration
type: docker  
image: bizosaas/images:latest
port: 4005
environment:
  - PEXELS_API_KEY=${PEXELS_API_KEY}
  - UNSPLASH_ACCESS_KEY=${UNSPLASH_ACCESS_KEY}
  - PIXABAY_API_KEY=${PIXABAY_API_KEY}
networks:
  - dokploy-network

# Service 4: telegram-integration
name: telegram-integration
type: docker
image: bizosaas/telegram:latest  
port: 4006
environment:
  - TELEGRAM_BIZOHOLIC_BOT_TOKEN=7767279872:AAGxwC7AcjSpkdF3xdvuLAw1gfXAplYLhMw
  - TELEGRAM_JONNYAI_BOT_TOKEN=7200437482:AAF8aE2uymF5ukm-ntlEnXx1hfhX1Obcfaw
networks:
  - dokploy-network
domain: bots.bizoholic.com

# Service 5: temporal-workflows (Python workflow orchestration - replacing n8n)
name: temporal-workflows
type: docker
image: bizosaas/temporal:latest
port: 8202
environment:
  - TEMPORAL_HOST=localhost
  - BRAIN_API_URL=http://bizosaas-brain:8001
networks:
  - dokploy-network
```

---

## 📋 **PROJECT 2: bizosaas-storage**
**Purpose**: Storage-only backend services (no business logic)

### **Services:**
```yaml
# Service 1: wagtail-cms-storage (Python CMS - replacing Strapi)
name: wagtail-cms-storage
type: docker
image: bizosaas/wagtail-storage:latest
port: 4000
environment:
  - POSTGRES_HOST=postgres
  - POSTGRES_DB=wagtail_storage
  - POSTGRES_PASSWORD=BizoHolic2024!Secure
networks:
  - dokploy-network
volumes:
  - wagtail-media:/app/media

# Service 2: saleor-storage (Python E-commerce - replacing Medusa.js)
name: saleor-storage
type: docker
image: bizosaas/saleor-storage:latest
port: 4003
environment:
  - POSTGRES_HOST=postgres
  - POSTGRES_DB=saleor_storage
  - POSTGRES_PASSWORD=CorelDove2024!Secure
networks:
  - dokploy-network
volumes:
  - saleor-media:/app/media
```

---

## 📋 **PROJECT 3: bizosaas-frontend**  
**Purpose**: Next.js frontend applications

### **Services:**
```yaml
# Service 1: bizoholic-frontend
name: bizoholic-frontend
type: docker
image: bizosaas/bizoholic-frontend:latest
port: 3000
environment:
  - BRAIN_API_BASE_URL=https://api.bizoholic.com
  - NEXT_PUBLIC_API_URL=https://api.bizoholic.com
networks:
  - dokploy-network
domain: bizoholic.com

# Service 2: coreldove-frontend  
name: coreldove-frontend
type: docker
image: bizosaas/coreldove-frontend:latest
port: 3001
environment:
  - BRAIN_API_BASE_URL=https://api.bizoholic.com
  - NEXT_PUBLIC_API_URL=https://api.bizoholic.com
networks:
  - dokploy-network
domain: coreldove.com

# Service 3: client-dashboard
name: client-dashboard
type: docker
image: bizosaas/client-dashboard:latest
port: 3002
environment:
  - BRAIN_API_URL=https://api.bizoholic.com
networks:
  - dokploy-network
domain: dashboard.bizoholic.com
```

---

## 🔧 **INTEGRATION WITH EXISTING INFRASTRUCTURE**

### **Shared Infrastructure Dependencies:**
```yaml
# Uses existing shared_infrastructure project services:
postgres:
  host: postgres
  port: 5432
  databases:
    - bizosaas_brain
    - wagtail_storage  
    - saleor_storage
    - temporal_workflows

redis:
  host: redis
  port: 6379
  password: SecureRedis2024Unified

temporal:
  host: localhost
  port: 7233
  namespace: bizosaas
  workflows: python-based (replacing n8n)
```

### **WordPress Integration:**
```yaml  
# Existing bizoholic-website project remains
# New BizOSaaS services complement WordPress
wordpress:
  domain: www.bizoholic.com
  admin_user: superadmin
  admin_password: BizoSaaS2024!Admin
  
# API Integration with BizOSaaS
wordpress_api_integration:
  brain_endpoint: https://api.bizoholic.com
  webhook_url: https://api.bizoholic.com/webhooks/wordpress
```

---

## 🌐 **DOMAIN MAPPING STRATEGY**

### **Production Domains:**
```
# Core Platform
api.bizoholic.com          → bizosaas-brain (8001)
admin.bizoholic.com        → unified-dashboard (5004)  
bots.bizoholic.com         → telegram-integration (4006)

# Frontend Applications  
bizoholic.com              → bizoholic-frontend (3000)
coreldove.com              → coreldove-frontend (3001)
dashboard.bizoholic.com    → client-dashboard (3002)

# Existing Services (Keep)
www.bizoholic.com          → WordPress (existing)
automation.bizoholic.com   → Temporal workflows (replacing n8n)
pgadmin.bizoholic.com      → pgAdmin (existing)
```

### **Staging Domains:**
```
# For testing before production
staging-api.bizoholic.com     → bizosaas-brain
staging-admin.bizoholic.com   → unified-dashboard
staging.bizoholic.com         → bizoholic-frontend
staging.coreldove.com         → coreldove-frontend
```

---

## 📦 **DOCKER IMAGES BUILD STRATEGY**

### **Build Configuration:**
```dockerfile
# Example: bizosaas-brain Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### **Multi-Stage Build for Next.js:**
```dockerfile
# Example: bizoholic-frontend Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:18-alpine AS runner  
WORKDIR /app
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
EXPOSE 3000
CMD ["npm", "start"]
```

---

## 🔐 **SECRETS MANAGEMENT**

### **Dokploy Environment Variables:**
```bash
# Core Secrets
POSTGRES_PASSWORD=SharedInfra2024!SuperSecure
REDIS_PASSWORD=SecureRedis2024Unified
JWT_SECRET=super-secret-jwt-key-for-bizosaas-platform-2024

# API Keys (Add to Dokploy Environment)  
OPENROUTER_API_KEY=sk-or-v1-REDACTED
PEXELS_API_KEY=your-pexels-key
UNSPLASH_ACCESS_KEY=your-unsplash-key
PIXABAY_API_KEY=your-pixabay-key

# Telegram Bot Tokens
TELEGRAM_BIZOHOLIC_BOT_TOKEN=7767279872:AAGxwC7AcjSpkdF3xdvuLAw1gfXAplYLhMw
TELEGRAM_JONNYAI_BOT_TOKEN=7200437482:AAF8aE2uymF5ukm-ntlEnXx1hfhX1Obcfaw
# ... other bot tokens

# External Services
N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
WORDPRESS_ADMIN_PASSWORD=BizoSaaS2024!Admin
```

---

## 📊 **MONITORING AND HEALTH CHECKS**

### **Health Check Endpoints:**
```yaml
# Each service health check
bizosaas-brain:     /health
unified-dashboard:  /health  
image-integration:  /health
telegram-integration: /health
wagtail-storage:    /health
saleor-storage:     /health
```

### **Monitoring Dashboard:**
```yaml  
# Optional: Add monitoring service to bizosaas-platform project
name: monitoring-dashboard
type: docker
image: grafana/grafana:latest
port: 3300
environment:
  - GF_SECURITY_ADMIN_PASSWORD=admin-password-change-in-production
volumes:
  - grafana-data:/var/lib/grafana
domain: monitor.bizoholic.com
```

---

## 🚀 **DEPLOYMENT SEQUENCE**

### **Phase 1: Storage Services**
1. Deploy `bizosaas-storage` project first
2. Ensure database connections to shared infrastructure
3. Test storage APIs independently

### **Phase 2: Core Platform**  
1. Deploy `bizosaas-platform` project
2. Configure brain connections to storage services
3. Test unified dashboard connectivity

### **Phase 3: Frontend Applications**
1. Deploy `bizosaas-frontend` project  
2. Configure domain routing
3. Test end-to-end functionality

### **Phase 4: Integration Testing**
1. Test cross-project communication
2. Verify shared infrastructure integration
3. Validate WordPress → BizOSaaS API calls

---

## 💡 **RECOMMENDED IMPLEMENTATION STEPS**

### **Week 1: Local Testing & Containerization**
- [ ] Complete local testing with real credentials
- [ ] Create Docker images for all services
- [ ] Test docker-compose locally

### **Week 2: Staging Deployment**
- [ ] Create staging projects in Dokploy
- [ ] Deploy to staging domains
- [ ] Integration testing

### **Week 3: Production Deployment**  
- [ ] Create production projects
- [ ] Configure production domains
- [ ] Monitor and optimize

### **Week 4: Optimization & Monitoring**
- [ ] Performance tuning
- [ ] Monitoring setup
- [ ] Backup strategy implementation

This deployment strategy maintains your existing infrastructure while cleanly separating BizOSaaS services into logical projects that can scale independently.