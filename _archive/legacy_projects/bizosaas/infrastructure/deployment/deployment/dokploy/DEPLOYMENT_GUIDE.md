# BizOSaaS Dokploy Deployment Guide

## 🏗️ **DEPLOYMENT ARCHITECTURE OVERVIEW**

The BizOSaaS platform is organized into **3 Dokploy projects** that integrate with your existing infrastructure:

### **Existing Dokploy Projects (Keep)**
1. **bizoholic-website** - WordPress frontend
2. **shared_infrastructure** - PostgreSQL, Dragonfly/Redis, CrewAI  
3. **automation-hub** - n8n workflows (will be enhanced with Temporal)

### **New BizOSaaS Projects (Deploy)**
4. **bizosaas-platform** - Core business logic services
5. **bizosaas-storage** - Storage-only backend services  
6. **bizosaas-frontend** - Next.js frontend applications

---

## 📋 **DEPLOYMENT SEQUENCE**

### **Phase 1: Verify Existing Infrastructure**
Before deploying BizOSaaS, ensure your existing projects are healthy:

```bash
# Check existing services
curl -f https://www.bizoholic.com/wp-admin/ # WordPress
curl -f https://b8d.bizoholic.com/health    # n8n
curl -f https://pgadmin.bizoholic.com       # pgAdmin

# Verify database connectivity
psql -h postgres -U postgres -d postgres -c "SELECT 1;"
redis-cli -h redis ping
```

### **Phase 2: Deploy BizOSaaS Platform (Core Services)**
Create Dokploy project: **bizosaas-platform**

**Services:**
- `bizosaas-brain` → https://api.bizoholic.com
- `unified-dashboard` → https://admin.bizoholic.com  
- `telegram-integration` → https://bots.bizoholic.com
- `image-integration` → https://images.bizoholic.com
- `temporal-workflows` → https://automation.bizoholic.com

**Domain Configuration:**
```
api.bizoholic.com          → bizosaas-brain (8001)
admin.bizoholic.com        → unified-dashboard (5004)
bots.bizoholic.com         → telegram-integration (4006)
images.bizoholic.com       → image-integration (4007)
automation.bizoholic.com   → temporal-workflows (8202)
```

### **Phase 3: Deploy BizOSaaS Storage (Backend Services)**
Create Dokploy project: **bizosaas-storage**

**Services:**
- `wagtail-cms` → https://cms.bizoholic.com
- `business-directory` → https://directory.bizoholic.com
- `saleor-backend` → https://api.coreldove.com
- `saleor-storefront` → https://store.coreldove.com

**Domain Configuration:**
```
cms.bizoholic.com       → wagtail-cms (4000)
directory.bizoholic.com → business-directory (4001)
api.coreldove.com       → saleor-backend (4003)
store.coreldove.com     → saleor-storefront (3001)
```

### **Phase 4: Deploy BizOSaaS Frontend (User-Facing)**
Create Dokploy project: **bizosaas-frontend**

**Services:**
- `bizoholic-frontend` → https://bizoholic.com
- `coreldove-frontend` → https://coreldove.com
- `client-dashboard` → https://dashboard.bizoholic.com

**Domain Configuration:**
```
bizoholic.com           → bizoholic-frontend (3000)
coreldove.com           → coreldove-frontend (3002)
dashboard.bizoholic.com → client-dashboard (3003)
```

---

## 🔐 **ENVIRONMENT VARIABLES SETUP**

### **Core Secrets (Required for all projects)**
```bash
# Database (Uses existing shared_infrastructure)
POSTGRES_PASSWORD=SharedInfra2024!SuperSecure
POSTGRES_REPLICATION_PASSWORD=replication_password

# Redis (Uses existing shared_infrastructure)  
REDIS_PASSWORD=SecureRedis2024Unified

# JWT & Security
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production-make-it-very-long-and-random
ENCRYPTION_KEY=your-encryption-key-for-credentials-32-bytes-long-base64-encoded
SERVICE_SECRET=service-to-service-secret-key-change-in-production

# Wagtail CMS
WAGTAIL_SECRET_KEY=wagtail-secret-key-change-in-production-very-long-and-random-key

# Saleor E-commerce
SALEOR_SECRET_KEY=saleor-secret-key-change-in-production-very-long-and-random-key
```

### **AI API Keys**
```bash
# Primary AI Services
OPENROUTER_API_KEY=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
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### **Telegram Bot Tokens (Real tokens from credentials)**
```bash
TELEGRAM_JONNYAI_BOT_TOKEN=7200437482:AAF8aE2uymF5ukm-ntlEnXx1hfhX1Obcfaw
TELEGRAM_BIZOHOLIC_BOT_TOKEN=7767279872:AAGxwC7AcjSpkdF3xdvuLAw1gfXAplYLhMw  
TELEGRAM_DEALS4ALL_BOT_TOKEN=1217910149:AAHZwP0RnxcaqMheU08so6hpyXL7H8tZfYw
TELEGRAM_BOTTRADER_BOT_TOKEN=7780097136:AAELAgYZsfmBCTuYxwHvqoITqwVjKZp-u0Y
TELEGRAM_GOGOFATHER_BOT_TOKEN=1011283832:AAHtpTljpQFhypOaQJwWei4z4Y5hgoMNSmk
```

### **Image API Keys (Optional - for enhanced functionality)**
```bash
PEXELS_API_KEY=your-pexels-key
UNSPLASH_ACCESS_KEY=your-unsplash-key  
PIXABAY_API_KEY=your-pixabay-key
AMAZON_ACCESS_KEY=your-amazon-access-key
AMAZON_SECRET_KEY=your-amazon-secret-key
AMAZON_PARTNER_TAG=your-amazon-associate-tag
```

---

## 🚀 **DOKPLOY PROJECT SETUP**

### **Project 1: bizosaas-platform**

1. **Create new Dokploy project**: `bizosaas-platform`
2. **Upload docker-compose.yml**: `deployment/dokploy/bizosaas-platform/docker-compose.yml`
3. **Configure environment variables**: Add all core secrets and API keys
4. **Build and deploy**: Let Dokploy build the Docker images
5. **Verify health**: Check all service endpoints are responding

### **Project 2: bizosaas-storage**

1. **Create new Dokploy project**: `bizosaas-storage`  
2. **Upload docker-compose.yml**: `deployment/dokploy/bizosaas-storage/docker-compose.yml`
3. **Configure environment variables**: Add database and CMS secrets
4. **Build and deploy**: Deploy storage services
5. **Initialize databases**: Run database migrations for Wagtail and Saleor

### **Project 3: bizosaas-frontend**

1. **Create new Dokploy project**: `bizosaas-frontend`
2. **Upload docker-compose.yml**: `deployment/dokploy/bizosaas-frontend/docker-compose.yml`  
3. **Configure environment variables**: Add frontend environment variables
4. **Build and deploy**: Deploy Next.js applications
5. **Test user interfaces**: Verify all frontend applications load correctly

---

## 🔗 **INTEGRATION WITH EXISTING INFRASTRUCTURE**

### **Database Integration**
- Uses your existing PostgreSQL from `shared_infrastructure`
- Creates additional databases: `wagtail_storage`, `saleor_storage`
- Maintains compatibility with existing WordPress database

### **Cache Integration**  
- Uses your existing Redis from `shared_infrastructure`
- Different Redis databases for different services (0-5)
- No conflicts with existing WordPress cache

### **Workflow Integration**
- Temporal workflows complement your existing n8n automation
- Can gradually migrate workflows from n8n to Temporal
- Both systems can coexist during transition

### **Domain Integration**
- New subdomains complement your existing WordPress site
- `www.bizoholic.com` remains unchanged  
- New APIs accessible via `api.bizoholic.com`

---

## ✅ **POST-DEPLOYMENT VERIFICATION**

### **Health Checks**
```bash
# Core Platform
curl -f https://api.bizoholic.com/          # Brain API
curl -f https://admin.bizoholic.com/health  # Dashboard
curl -f https://bots.bizoholic.com/health   # Telegram
curl -f https://images.bizoholic.com/health # Images

# Storage Services  
curl -f https://cms.bizoholic.com/admin/         # Wagtail
curl -f https://directory.bizoholic.com/health   # Directory
curl -f https://api.coreldove.com/graphql/       # Saleor API
curl -f https://store.coreldove.com/             # Saleor Store

# Frontend Applications
curl -f https://bizoholic.com/           # Main site
curl -f https://coreldove.com/           # E-commerce
curl -f https://dashboard.bizoholic.com/ # Clients
```

### **Integration Tests**
```bash
# Test API connectivity
curl -f https://api.bizoholic.com/api/dashboard

# Test Telegram bots
curl -f https://bots.bizoholic.com/bots

# Test image search
curl -X POST https://images.bizoholic.com/api/images/search \
  -H "Content-Type: application/json" \
  -d '{"query": "business", "source": "auto", "count": 3}'

# Test CMS
curl -f https://cms.bizoholic.com/api/v2/pages/
```

---

## 🛡️ **SECURITY CONSIDERATIONS**

### **SSL Certificates**
- All domains use Let's Encrypt automatic SSL
- Traefik handles certificate renewal
- HTTPS redirects enabled for all services

### **Network Security**
- All services communicate via internal Docker network
- External access only through Traefik reverse proxy
- Database and Redis not directly exposed

### **Secret Management** 
- Environment variables stored securely in Dokploy
- API keys encrypted at rest
- No secrets in Docker images or code

---

## 📈 **MONITORING & SCALING**

### **Service Monitoring**
- Built-in health checks for all services
- Dokploy dashboard shows service status
- Automatic restart on failure

### **Scaling Strategy**
- Start with single instance of each service
- Scale horizontally by adding more containers
- Database and Redis can handle multiple connections

### **Backup Strategy**
- Database backups via existing infrastructure
- Media files backed up automatically
- Configuration stored in Git

---

## 🔄 **GRADUAL MIGRATION STRATEGY**

### **Phase 1: Core Services (Week 1)**
- Deploy `bizosaas-platform` only
- Test API and admin functionality
- Keep existing WordPress unchanged

### **Phase 2: Storage & CMS (Week 2)** 
- Deploy `bizosaas-storage`
- Migrate content to Wagtail CMS
- Set up Saleor e-commerce

### **Phase 3: Frontend & Integration (Week 3)**
- Deploy `bizosaas-frontend`  
- Integrate with existing WordPress
- Full platform testing

### **Phase 4: Production Optimization (Week 4)**
- Performance optimization
- Security hardening
- Monitoring setup

This deployment strategy ensures minimal disruption to your existing services while providing a robust foundation for the BizOSaaS platform expansion.