# BizOSaaS Platform - Quick Reference Guide

## 🚀 Quick Start Commands

### Start All Services
```bash
cd /home/alagiri/projects/bizosaas-platform
./scripts/start-bizosaas-core-full.sh --wait
```

### Stop All Services
```bash
cd bizosaas-brain-core
docker compose down
docker compose -f docker-compose.authentik.yml down
docker compose -f docker-compose.observability.yml down
```

### View Logs
```bash
# All services
docker compose -f bizosaas-brain-core/docker-compose.yml logs -f

# Specific service
docker logs brain-gateway -f
docker logs brain-auth -f
docker logs client-portal -f
```

### Restart a Service
```bash
docker compose -f bizosaas-brain-core/docker-compose.yml restart brain-gateway
docker compose -f bizosaas-brain-core/docker-compose.yml restart client-portal
```

---

## 🔐 Access URLs & Credentials

### Services
| Service | URL | Purpose |
|---------|-----|---------|
| Client Portal | http://localhost:3003 | Main application |
| Brain Gateway API | http://localhost:8000 | Backend API |
| Auth Service | http://localhost:8009 | Authentication |
| Authentik SSO | http://localhost:9000 | SSO provider |
| Portainer | http://localhost:9001 | Docker management |
| Grafana | http://localhost:3002 | Monitoring |
| Prometheus | http://localhost:9090 | Metrics |
| Temporal UI | http://localhost:8082 | Workflow management |
| Jaeger | http://localhost:16686 | Tracing |
| Vault | http://localhost:8200 | Secrets management |

### Default Credentials
```
Admin User:
  Email: admin@bizosaas.com
  Password: Admin@123

Tenant Admin:
  Email: tenant@bizoholic.com
  Password: Tenant@123

Regular User:
  Email: user@bizoholic.com
  Password: User@123

Vault Token:
  Token: root (development only)

Grafana:
  Username: admin
  Password: admin
```

---

## 🛠️ Common Tasks

### Create New Admin User
```bash
docker exec -it brain-auth python3 /app/seed_users_simple.py
```

### Check Service Health
```bash
curl http://localhost:8000/health  # Brain Gateway
curl http://localhost:8009/health  # Auth Service
curl http://localhost:3003         # Client Portal
```

### Rebuild Client Portal
```bash
cd bizosaas-brain-core
docker compose down client-portal
docker compose build client-portal
docker compose up -d client-portal
```

### Clean Up Docker Resources
```bash
./scripts/cleanup-docker-resources.sh
```

### View Database
```bash
docker exec -it brain-postgres psql -U postgres -d bizosaas
```

### Access Redis CLI
```bash
docker exec -it brain-redis redis-cli
```

---

## 🐛 Troubleshooting

### Service Won't Start
```bash
# Check logs
docker logs <container-name>

# Check if port is in use
sudo lsof -i :<port-number>

# Restart service
docker compose restart <service-name>
```

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Test connection
docker exec brain-postgres pg_isready -U postgres

# Reset database (WARNING: Deletes all data)
docker compose down
docker volume rm bizosaas-brain-core_postgres-data
docker compose up -d
```

### Login Not Working
```bash
# Verify admin user exists
docker exec brain-auth python3 -c "from main import *; import asyncio; asyncio.run(check_users())"

# Reseed users
docker exec brain-auth python3 /app/seed_users_simple.py

# Check auth service logs
docker logs brain-auth --tail 100
```

### Out of Disk Space
```bash
# Check disk usage
docker system df

# Clean up
docker system prune -a --volumes

# Or use cleanup script
./scripts/cleanup-docker-resources.sh
```

---

## 📦 Deployment

### Oracle Cloud Setup
```bash
# 1. Create VM (4 OCPU, 24GB RAM, Ubuntu 22.04)
# 2. SSH into VM
ssh ubuntu@<your-vm-ip>

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Clone repository
git clone https://github.com/Bizoholic-Digital/bizosaas-platform.git
cd bizosaas-platform

# 5. Configure environment
cp .env.example .env
nano .env

# 6. Start services
./scripts/start-bizosaas-core-full.sh --wait
```

### Using Coolify
```bash
# 1. Install Coolify on Oracle Cloud VM
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash

# 2. Access Coolify UI
http://<your-vm-ip>:8000

# 3. Add GitHub repository
# 4. Configure environment variables
# 5. Deploy
```

---

## 🔄 Git Workflow

### Pull Latest Changes
```bash
git pull origin staging
```

### Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### Commit Changes
```bash
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
```

### Merge to Staging
```bash
git checkout staging
git merge feature/your-feature-name
git push origin staging
```

---

## 📊 Monitoring

### View Metrics
- **Grafana**: http://localhost:3002
- **Prometheus**: http://localhost:9090

### View Traces
- **Jaeger**: http://localhost:16686

### View Logs
- **Loki**: Integrated with Grafana

### Container Stats
```bash
docker stats
```

---

## 🔐 Security

### Rotate Secrets
```bash
# Generate new JWT secret
openssl rand -hex 32

# Update .env file
nano bizosaas-brain-core/.env

# Restart services
docker compose restart
```

### Backup Database
```bash
docker exec brain-postgres pg_dump -U postgres bizosaas > backup.sql
```

### Restore Database
```bash
cat backup.sql | docker exec -i brain-postgres psql -U postgres bizosaas
```

---

## 📚 Documentation

- **Implementation Summary**: [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)
- **Deployment Checklist**: [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)
- **MCP Integration**: [bizosaas-brain-core/MCP_INTEGRATION_STRATEGY.md](./bizosaas-brain-core/MCP_INTEGRATION_STRATEGY.md)
- **Architecture**: [bizosaas-brain-core/ARCHITECTURE_RECOMMENDATION_V3.md](./bizosaas-brain-core/ARCHITECTURE_RECOMMENDATION_V3.md)
- **Final Status**: [FINAL_STATUS_REPORT.md](./FINAL_STATUS_REPORT.md)

---

## 🆘 Support

### Check Service Status
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### View All Logs
```bash
docker compose -f bizosaas-brain-core/docker-compose.yml logs --tail=100
```

### Emergency Stop
```bash
docker stop $(docker ps -aq)
```

### Emergency Cleanup
```bash
docker system prune -a --volumes -f
```

---

**Last Updated**: 2025-12-09
**Version**: 1.0.0-beta
