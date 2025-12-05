# BizOSaaS Frontend Applications - Docker Containerization Guide

This guide covers the comprehensive Docker containerization of the 4 BizOSaaS frontend applications built with Next.js 14.

## Overview

The BizOSaaS platform now includes 4 containerized frontend applications:

| Application | Port | Purpose | Container Name |
|-------------|------|---------|----------------|
| **Client Portal** | 3006 | Multi-tenant client dashboard | `bizosaas-client-portal-3006` |
| **CoreLDove Frontend** | 3007 | E-commerce storefront | `bizosaas-coreldove-frontend-3007` |
| **Bizoholic Frontend** | 3008 | Marketing agency website | `bizosaas-bizoholic-frontend-3008` |
| **BizOSaaS Admin** | 3009 | Platform administration dashboard | `bizosaas-admin-dashboard-3009` |

## Architecture

### Container Design

Each frontend application uses a **multi-stage Docker build** optimized for production:

```dockerfile
# Build Stage
FROM node:18-alpine AS base
FROM base AS deps        # Dependencies installation
FROM base AS builder     # Application build
FROM base AS runner      # Production runtime
```

### Key Features

- **Production-optimized**: Multi-stage builds minimize image size
- **Security-focused**: Non-root user execution
- **Health checks**: Built-in health monitoring
- **Next.js 14**: Standalone output for optimal containerization
- **Environment-aware**: Configurable for development/production

## File Structure

```
bizosaas-platform/
├── frontend/apps/
│   ├── client-portal/
│   │   ├── Dockerfile
│   │   ├── next.config.js
│   │   ├── .dockerignore
│   │   └── app/api/health/route.ts
│   ├── coreldove-frontend/
│   │   ├── Dockerfile
│   │   ├── next.config.js
│   │   ├── .dockerignore
│   │   └── app/api/health/route.ts
│   ├── bizoholic-frontend/
│   │   ├── Dockerfile
│   │   ├── next.config.js
│   │   ├── .dockerignore
│   │   └── app/api/health/route.ts
│   └── bizosaas-admin/
│       ├── Dockerfile
│       ├── next.config.js
│       ├── .dockerignore
│       └── app/api/health/route.ts
├── docker-compose.bizosaas-platform.yml
├── docker-compose.frontend-apps.yml
└── scripts/
    ├── build-frontend-apps.sh
    └── deploy-frontend-apps.sh
```

## Docker Configuration

### Dockerfile Features

Each Dockerfile includes:

- **Multi-stage build** for optimal image size
- **Security**: Non-root user (nextjs:nodejs)
- **Health checks**: Built-in API health endpoints
- **Environment**: Production-ready configuration
- **Port exposure**: Specific port per application

### Next.js Configuration

Each `next.config.js` includes:

- **Standalone output**: Optimized for containers
- **API rewrites**: Backend service integration
- **CORS headers**: Cross-origin request handling
- **Image optimization**: Container-aware domains
- **Platform identification**: Tenant/platform headers

## Environment Variables

### Common Variables (All Apps)

```bash
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
JWT_SECRET=your-jwt-secret-key
ENVIRONMENT=production
```

### BizOSaaS Platform Integration

```bash
NEXT_PUBLIC_BRAIN_API_URL=http://bizosaas-brain:8001
NEXT_PUBLIC_AUTH_API_URL=http://bizosaas-auth-v2:8007
NEXT_PUBLIC_WAGTAIL_URL=http://bizosaas-wagtail-cms:8000
NEXT_PUBLIC_CRM_API_URL=http://bizosaas-django-crm:8008
NEXT_PUBLIC_SALEOR_API_URL=http://bizosaas-saleor-api:8000
NEXT_PUBLIC_SUPERSET_URL=http://bizosaas-superset:8088
NEXT_PUBLIC_VAULT_URL=http://bizosaas-vault:8200
```

### Application-Specific Variables

#### Client Portal (Port 3006)
```bash
PORT=3006
NEXT_PUBLIC_PLATFORM=client-portal
NEXT_PUBLIC_TENANT=multi-tenant
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_CHAT=true
```

#### CoreLDove Frontend (Port 3007)
```bash
PORT=3007
NEXT_PUBLIC_PLATFORM=coreldove-ecommerce
NEXT_PUBLIC_TENANT=coreldove
NEXT_PUBLIC_ENABLE_PAYMENTS=true
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

#### Bizoholic Frontend (Port 3008)
```bash
PORT=3008
NEXT_PUBLIC_PLATFORM=bizoholic-marketing
NEXT_PUBLIC_TENANT=bizoholic
NEXT_PUBLIC_ENABLE_LEAD_CAPTURE=true
NEXT_PUBLIC_ENABLE_BLOG=true
```

#### BizOSaaS Admin (Port 3009)
```bash
PORT=3009
NEXT_PUBLIC_PLATFORM=bizosaas-admin
NEXT_PUBLIC_TENANT=bizosaas
NEXT_PUBLIC_ENABLE_USER_MANAGEMENT=true
NEXT_PUBLIC_ENABLE_SYSTEM_MONITORING=true
```

## Deployment

### Quick Start

1. **Build all frontend applications:**
   ```bash
   ./scripts/build-frontend-apps.sh
   ```

2. **Deploy the complete platform:**
   ```bash
   ./scripts/deploy-frontend-apps.sh
   ```

3. **Verify deployment:**
   ```bash
   docker-compose -f docker-compose.bizosaas-platform.yml ps
   ```

### Manual Build Commands

Build individual applications:

```bash
# Client Portal
docker build -t bizosaas/client-portal:latest ./frontend/apps/client-portal

# CoreLDove Frontend
docker build -t bizosaas/coreldove-frontend:latest ./frontend/apps/coreldove-frontend

# Bizoholic Frontend
docker build -t bizosaas/bizoholic-frontend:latest ./frontend/apps/bizoholic-frontend

# BizOSaaS Admin
docker build -t bizosaas/admin-dashboard:latest ./frontend/apps/bizosaas-admin
```

### Docker Compose Deployment

Use the main platform compose file:

```bash
docker-compose -f docker-compose.bizosaas-platform.yml up -d
```

Or use the dedicated frontend compose file:

```bash
docker-compose -f docker-compose.frontend-apps.yml up -d
```

## Health Monitoring

### Health Check Endpoints

Each application provides a health check endpoint:

- **Client Portal**: `http://localhost:3006/api/health`
- **CoreLDove**: `http://localhost:3007/api/health`
- **Bizoholic**: `http://localhost:3008/api/health`
- **Admin Dashboard**: `http://localhost:3009/api/health`

### Health Check Response

```json
{
  "status": "healthy",
  "service": "client-portal",
  "timestamp": "2024-01-15T10:30:00Z",
  "platform": "bizosaas",
  "version": "1.0.0",
  "environment": "production",
  "port": 3006,
  "uptime": 3600,
  "memory": {
    "rss": 125829120,
    "heapTotal": 67108864,
    "heapUsed": 45678912
  }
}
```

### Monitoring Commands

```bash
# Check all services status
docker-compose -f docker-compose.bizosaas-platform.yml ps

# View service logs
docker-compose -f docker-compose.bizosaas-platform.yml logs bizosaas-client-portal

# Follow logs in real-time
docker-compose -f docker-compose.bizosaas-platform.yml logs -f

# Check specific service health
curl http://localhost:3006/api/health
```

## Networking

### Docker Networks

- **Network**: `bizosaas-platform-network`
- **Type**: Bridge network
- **Purpose**: Inter-service communication

### Service Discovery

Services communicate using container names:

```javascript
// Example API calls from frontend
const brainApiUrl = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://bizosaas-brain:8001';
const authApiUrl = process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://bizosaas-auth-v2:8007';
```

### Port Mapping

| Container Port | Host Port | Service |
|----------------|-----------|---------|
| 3006 | 3006 | Client Portal |
| 3007 | 3007 | CoreLDove Frontend |
| 3008 | 3008 | Bizoholic Frontend |
| 3009 | 3009 | BizOSaaS Admin |

## Development vs Production

### Development Mode

For development, run applications locally:

```bash
cd frontend/apps/client-portal && npm run dev
cd frontend/apps/coreldove-frontend && npm run dev
cd frontend/apps/bizoholic-frontend && npm run dev
cd frontend/apps/bizosaas-admin && npm run dev
```

### Production Mode

For production, use containerized deployment:

```bash
./scripts/deploy-frontend-apps.sh
```

### Environment Differences

| Feature | Development | Production |
|---------|-------------|------------|
| Hot Reload | ✅ | ❌ |
| Source Maps | ✅ | ❌ |
| Image Optimization | ❌ | ✅ |
| Bundle Optimization | ❌ | ✅ |
| Security Headers | Basic | Enhanced |
| Error Handling | Detailed | User-friendly |

## Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Check build logs
   docker-compose -f docker-compose.bizosaas-platform.yml logs bizosaas-client-portal
   
   # Rebuild specific service
   docker-compose -f docker-compose.bizosaas-platform.yml build bizosaas-client-portal
   ```

2. **Health Check Failures**
   ```bash
   # Check container status
   docker ps | grep bizosaas
   
   # Check health endpoint manually
   curl -f http://localhost:3006/api/health
   ```

3. **Network Issues**
   ```bash
   # Verify network exists
   docker network ls | grep bizosaas-platform-network
   
   # Recreate network
   docker network rm bizosaas-platform-network
   docker network create bizosaas-platform-network
   ```

4. **Port Conflicts**
   ```bash
   # Check port usage
   netstat -tulpn | grep :3006
   
   # Kill process using port
   sudo kill -9 $(lsof -t -i:3006)
   ```

### Debug Mode

Enable debug logging:

```bash
# Set debug environment
export DEBUG=true
export LOG_LEVEL=debug

# Rebuild with debug
docker-compose -f docker-compose.bizosaas-platform.yml build --no-cache
```

### Log Analysis

```bash
# View application logs
docker-compose -f docker-compose.bizosaas-platform.yml logs bizosaas-client-portal

# View all logs with timestamps
docker-compose -f docker-compose.bizosaas-platform.yml logs -t

# Filter logs by service
docker-compose -f docker-compose.bizosaas-platform.yml logs | grep "client-portal"
```

## Performance Optimization

### Image Size Optimization

- **Multi-stage builds**: Reduce final image size
- **Alpine Linux**: Lightweight base image (node:18-alpine)
- **.dockerignore**: Exclude unnecessary files
- **Layer caching**: Optimize build layer order

### Runtime Optimization

- **Standalone output**: Minimal Next.js runtime
- **Non-root user**: Security without performance impact
- **Health checks**: Efficient monitoring
- **Resource limits**: Memory and CPU constraints

### Build Optimization

```bash
# Build with build cache
docker build --cache-from bizosaas/client-portal:latest ./frontend/apps/client-portal

# Multi-platform builds
docker buildx build --platform linux/amd64,linux/arm64 ./frontend/apps/client-portal
```

## Security

### Container Security

- **Non-root user**: All containers run as `nextjs` user
- **Minimal attack surface**: Alpine Linux base
- **No shell access**: Production containers don't include shell
- **Read-only filesystem**: Where possible

### Network Security

- **Private networks**: Internal service communication
- **Environment variables**: Secure secret management
- **CORS configuration**: Proper cross-origin handling
- **Security headers**: Implemented in Next.js config

### Best Practices

1. **Secrets Management**
   ```bash
   # Use Docker secrets or environment files
   docker-compose -f docker-compose.bizosaas-platform.yml --env-file .env.production up -d
   ```

2. **Image Scanning**
   ```bash
   # Scan for vulnerabilities
   docker scout cves bizosaas/client-portal:latest
   ```

3. **Regular Updates**
   ```bash
   # Update base images regularly
   docker pull node:18-alpine
   ./scripts/build-frontend-apps.sh
   ```

## Scaling

### Horizontal Scaling

Scale individual frontend services:

```bash
# Scale client portal to 3 instances
docker-compose -f docker-compose.bizosaas-platform.yml up -d --scale bizosaas-client-portal=3
```

### Load Balancing

Configure Traefik for load balancing:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.client-portal.rule=Host(`portal.bizosaas.local`)"
  - "traefik.http.services.client-portal.loadbalancer.server.port=3006"
```

### Resource Management

Set resource limits:

```yaml
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
    reservations:
      memory: 256M
      cpus: '0.25'
```

## Maintenance

### Regular Tasks

1. **Update Dependencies**
   ```bash
   cd frontend/apps/client-portal
   npm update
   npm audit fix
   ```

2. **Rebuild Images**
   ```bash
   ./scripts/build-frontend-apps.sh --tag latest
   ```

3. **Clean Up**
   ```bash
   # Remove unused images
   docker image prune -f
   
   # Remove unused volumes
   docker volume prune -f
   ```

### Backup

Backup persistent data:

```bash
# Export volumes
docker run --rm -v bizosaas-client-portal-logs:/data alpine tar czf - -C /data . > client-portal-logs.tar.gz
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Build and Deploy Frontend Apps

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Frontend Apps
        run: ./scripts/build-frontend-apps.sh --push
      - name: Deploy to Production
        run: ./scripts/deploy-frontend-apps.sh
```

## Conclusion

The BizOSaaS frontend applications are now fully containerized with:

- ✅ **Production-ready Docker containers**
- ✅ **Optimized Next.js 14 builds**
- ✅ **Comprehensive health monitoring**
- ✅ **Secure multi-stage builds**
- ✅ **Automated deployment scripts**
- ✅ **Integration with BizOSaaS platform**

This containerization provides a scalable, maintainable, and secure foundation for the BizOSaaS platform's frontend applications.