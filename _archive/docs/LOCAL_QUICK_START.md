# BizOSaaS Local Development - Quick Start Guide

**Status**: ✅ Ready for Local Testing  
**Date**: 2024-11-24

---

## Current Repository Status

### Git Status
- **Repository**: Connected to GitHub (Bizoholic-Digital/bizosaas-platform)
- **Modified Files**: ~20 files (admin components, Docker configs)
- **Untracked Files**: Backup scripts, deployment docs
- **Status**: Working directory has local changes (safe to proceed)

### Code Availability
- ✅ All frontend apps present
- ✅ All backend services present
- ✅ Docker Compose configurations ready
- ✅ Infrastructure configs available

---

## Quick Start Commands

### Option 1: Start Bizoholic Only (Recommended for Testing)

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas

# Start Bizoholic with dependencies
docker-compose -f docker-compose.unified.yml up -d \
  postgres \
  redis \
  vault \
  bizosaas-brain \
  auth-service \
  wagtail-cms \
  bizoholic-frontend

# Wait for services to start
sleep 60

# Check status
docker-compose ps

# View logs
docker-compose logs -f bizoholic-frontend

# Access
open http://localhost:3001
```

**Services**: 7  
**Memory**: ~2-3GB  
**Time**: ~2 minutes

---

### Option 2: Start CoreLDove Only

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas

# Start CoreLDove with dependencies
docker-compose -f docker-compose.unified.yml up -d \
  postgres \
  redis \
  vault \
  bizosaas-brain \
  auth-service \
  saleor-backend \
  wagtail-cms \
  coreldove-frontend

# Wait for Saleor to initialize
sleep 90

# Check status
docker-compose ps

# Access
open http://localhost:3002
```

**Services**: 8  
**Memory**: ~3-4GB  
**Time**: ~3 minutes

---

### Option 3: Start Full Platform

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas

# Start everything
docker-compose -f docker-compose.unified.yml up -d

# Wait for all services
sleep 120

# Check status
docker-compose ps

# Access points
open http://localhost:3000  # Admin Dashboard
open http://localhost:3001  # Bizoholic
open http://localhost:3002  # CoreLDove
```

**Services**: 20+  
**Memory**: ~8GB  
**Time**: ~5 minutes

---

## Environment Setup (Optional)

### Create .env File

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas

# Copy example
cp .env.unified.example .env

# Edit with your keys
nano .env
```

### Required Variables (Minimal)

```bash
# Database
POSTGRES_PASSWORD=Bizoholic2024Alagiri

# JWT
JWT_SECRET=bizosaas-central-secret-key

# Optional (for full features)
OPENAI_API_KEY=your-key-here
STRIPE_PUBLISHABLE_KEY=your-key-here
```

**Note**: Services will start with default values if .env not provided

---

## Verification Steps

### 1. Check Docker Installation

```bash
docker --version
docker-compose --version
```

### 2. Check Services Running

```bash
cd /home/alagiri/projects/bizosaas-platform/bizosaas
docker-compose ps
```

### 3. Test API Endpoints

```bash
# Brain API
curl http://localhost:8001/health

# Auth Service
curl http://localhost:8007/health

# Wagtail CMS
curl http://localhost:8006/admin/

# Saleor (if running CoreLDove)
curl http://localhost:8000/health/
```

### 4. Check Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs -f bizoholic-frontend

# Last 100 lines
docker-compose logs --tail=100
```

---

## Troubleshooting

### Services Not Starting

```bash
# Check Docker daemon
sudo systemctl status docker

# Restart Docker
sudo systemctl restart docker

# Check ports
sudo netstat -tulpn | grep -E ':(3000|3001|3002|8000|8001|8006|8007|5432|6379)'
```

### Port Conflicts

```bash
# Stop conflicting services
docker-compose down

# Or stop specific service
docker-compose stop bizoholic-frontend
```

### Database Issues

```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres

# Wait and retry
sleep 30
docker-compose up -d
```

### Memory Issues

```bash
# Check Docker resources
docker system df

# Clean up
docker system prune -a

# Increase Docker memory limit (Docker Desktop)
# Settings > Resources > Memory > 8GB
```

---

## Next Steps

### After Services Start

1. **Access Bizoholic**: http://localhost:3001
2. **Access CoreLDove**: http://localhost:3002
3. **Access Admin**: http://localhost:3000

### Test Flows

**Bizoholic**:
- View marketing pages
- Test content from Wagtail
- Check AI features

**CoreLDove**:
- Browse product catalog
- Test shopping cart
- Check Saleor integration

### Stop Services

```bash
# Stop all
docker-compose down

# Stop specific service
docker-compose stop bizoholic-frontend

# Stop and remove volumes (clean slate)
docker-compose down -v
```

---

## Resource Monitoring

### Check Resource Usage

```bash
# Docker stats
docker stats

# System resources
htop

# Disk usage
df -h
```

### Recommended Resources

**Minimal** (Bizoholic OR CoreLDove):
- CPU: 2 cores
- RAM: 4GB
- Disk: 10GB free

**Full Platform**:
- CPU: 4 cores
- RAM: 8GB
- Disk: 20GB free

---

## Common Commands Reference

```bash
# Start services
docker-compose up -d [service-name]

# Stop services
docker-compose stop [service-name]

# Restart service
docker-compose restart [service-name]

# View logs
docker-compose logs -f [service-name]

# Execute command in container
docker-compose exec [service-name] bash

# Check service health
docker-compose ps

# Remove everything
docker-compose down -v
```

---

## Ready to Start!

**Choose your option**:
1. Start Bizoholic (6 services, 2GB RAM)
2. Start CoreLDove (7 services, 3GB RAM)
3. Start Full Platform (20+ services, 8GB RAM)

**All code is ready locally - just run the commands above!**

---

**Status**: ✅ Ready  
**Docker**: Installed  
**Code**: 100% Available  
**Next**: Choose startup option and run
