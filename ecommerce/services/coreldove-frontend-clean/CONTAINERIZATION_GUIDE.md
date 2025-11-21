# CoreLDove Frontend Containerization Guide

## Overview

This guide provides instructions for containerizing the CoreLDove frontend application while following the zero redundancy policy and preserving the working development environment.

## Current Status

- ✅ Working frontend on port 3012 via `npm run dev`
- ✅ Production-ready Dockerfile created
- ✅ Docker compose configurations ready
- ✅ Automated containerization script prepared
- ⏳ Docker daemon issues resolved (restart required)

## Files Created

### Docker Configuration Files

1. **Dockerfile.production** - Optimized production container image
2. **Dockerfile.optimized** - Multi-stage build with security features
3. **docker-compose.production.yml** - Production deployment configuration
4. **containerize-coreldove.sh** - Automated containerization script

### Key Features

- **Zero Redundancy**: Reuses existing `bizosaas/brain-gateway:latest` image
- **Security**: Non-root user, minimal attack surface
- **Performance**: Multi-stage builds, optimized dependencies
- **Health Checks**: Built-in container health monitoring
- **Network Integration**: Uses existing `bizosaas-network`

## Quick Start

### Option 1: Automated Script (Recommended)

```bash
cd /home/alagiri/projects/bizoholic/bizosaas-platform/ecommerce/services/coreldove-frontend-clean
./containerize-coreldove.sh
```

### Option 2: Docker Compose

```bash
# Production deployment
docker-compose -f docker-compose.production.yml up -d

# Check status
docker-compose -f docker-compose.production.yml ps
```

### Option 3: Manual Docker Commands

```bash
# Build image
docker build -f Dockerfile.production -t bizosaas/coreldove-frontend:latest .

# Run container
docker run -d \
  --name coreldove-frontend-3012 \
  --restart unless-stopped \
  -p 3012:3012 \
  --network bizosaas-network \
  -e NODE_ENV=production \
  -e PORT=3012 \
  bizosaas/coreldove-frontend:latest
```

## Docker Image Reuse Strategy

Following the zero redundancy policy, this configuration reuses:

- **bizosaas/brain-gateway:latest** (609MB) - For backend API
- **bizosaas-network** - Existing container network
- **node:18-alpine** - Standard base image
- **Port mappings** - Consistent with existing services

## Environment Variables

| Variable | Value | Description |
|----------|--------|-------------|
| NODE_ENV | production | Production environment |
| PORT | 3012 | Container port |
| NEXT_TELEMETRY_DISABLED | 1 | Disable Next.js telemetry |
| NEXT_PUBLIC_API_BASE_URL | http://localhost:8001 | API endpoint |
| NEXT_PUBLIC_BRAIN_API_URL | http://bizosaas-brain-8001:8001 | Brain API |
| NEXT_PUBLIC_SALEOR_API_URL | http://bizosaas-saleor-api-8003:8000 | Saleor API |

## Container Security Features

- **Non-root user**: Runs as `nextjs` user (UID: 1001)
- **Read-only filesystem**: Limited write access
- **Resource limits**: Memory and CPU constraints
- **Health checks**: Automatic health monitoring
- **Signal handling**: Proper process termination

## Monitoring and Management

### Check Container Status
```bash
docker ps | grep coreldove
docker logs coreldove-frontend-3012
```

### Health Check
```bash
curl -f http://localhost:3012/
```

### Resource Usage
```bash
docker stats coreldove-frontend-3012
```

## Troubleshooting

### Docker Daemon Issues

If Docker daemon is not responding:

1. **Restart Docker Desktop**:
   ```bash
   # From Windows PowerShell
   Stop-Process -Name "Docker Desktop" -Force
   Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
   ```

2. **Clear Docker Cache**:
   ```bash
   docker system prune -a
   ```

3. **WSL Reset** (if using WSL):
   ```bash
   wsl --shutdown
   ```

### Port Conflicts

If port 3012 is in use:

1. **Stop npm dev process**:
   ```bash
   pkill -f "next dev --port 3012"
   ```

2. **Stop existing container**:
   ```bash
   docker stop coreldove-frontend-3012
   docker rm coreldove-frontend-3012
   ```

### Build Issues

If container build fails:

1. **Check dependencies**:
   ```bash
   npm install --legacy-peer-deps
   ```

2. **Clean build**:
   ```bash
   rm -rf .next node_modules
   npm install --legacy-peer-deps
   npm run build
   ```

## Migration from npm dev to Container

### Before Migration
- Frontend running via `npm run dev` on port 3012
- Development environment fully functional

### After Migration
- Frontend running in production container on port 3012
- Same functionality, improved security and performance
- Consistent with other containerized services

### Rollback Process
If needed, you can always return to npm dev:

```bash
# Stop container
docker stop coreldove-frontend-3012
docker rm coreldove-frontend-3012

# Start npm dev
cd /home/alagiri/projects/bizoholic/bizosaas-platform/ecommerce/services/coreldove-frontend-clean
npm run dev
```

## Integration with BizOSaaS Platform

This containerized frontend integrates with:

- **bizosaas-brain-8001** - Core API service
- **bizosaas-saleor-db-5433** - E-commerce database
- **bizosaas-redis-6379** - Cache layer
- **bizosaas-network** - Internal container network

## Performance Optimizations

- **Multi-stage builds** - Smaller final image size
- **Node.js optimizations** - Production-ready configuration
- **Resource limits** - Prevents resource contention
- **Health checks** - Automatic failure detection
- **Restart policies** - Automatic recovery

## Next Steps

1. **Test containerized deployment** once Docker daemon is resolved
2. **Monitor performance** compared to npm dev
3. **Integrate with CI/CD pipeline** for automated deployments
4. **Set up logging aggregation** for production monitoring
5. **Configure SSL/TLS** for production domains

## Support

For issues or questions about containerization:
1. Check Docker daemon status first
2. Review container logs: `docker logs coreldove-frontend-3012`
3. Verify network connectivity to dependent services
4. Test health endpoints for integration services