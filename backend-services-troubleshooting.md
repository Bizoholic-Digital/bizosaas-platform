# Backend Services Troubleshooting Guide
## Phase 2 Deployment - Common Issues & Solutions

### Quick Issue Finder
1. [Container Won't Start](#issue-1-container-wont-start)
2. [Health Check Failing](#issue-2-health-check-failing)
3. [Database Connection Issues](#issue-3-database-connection-issues)
4. [Redis Connection Timeout](#issue-4-redis-connection-timeout)
5. [API Key Not Working](#issue-5-api-key-not-working)
6. [High Memory Usage](#issue-6-high-memory-usage)
7. [Slow Response Times](#issue-7-slow-response-times)
8. [Port Conflicts](#issue-8-port-conflicts)
9. [Network Issues](#issue-9-network-issues)
10. [Build Failures](#issue-10-build-failures)

---

## Issue 1: Container Won't Start

### Symptoms
- Container shows "Exited" status
- Container keeps restarting
- Docker logs show immediate exit

### Diagnostic Commands
```bash
# Check container status
ssh root@194.238.16.237 'docker ps -a --filter name=<container-name>'

# View recent logs
ssh root@194.238.16.237 'docker logs <container-name> --tail 100'

# Check exit code
ssh root@194.238.16.237 'docker inspect <container-name> --format="{{.State.ExitCode}}"'
```

### Common Causes & Solutions

#### Cause 1.1: Missing Environment Variables
**Error Pattern**: `KeyError: 'VARIABLE_NAME'` or `Environment variable not found`

**Solution**:
```bash
# Check current environment variables
ssh root@194.238.16.237 'docker inspect <container-name> | grep -A 20 "Env"'

# Add missing variable in Dokploy UI
# Navigate to: Application → Environment Variables → Add Variable

# Or set via docker-compose
# Add to dokploy-backend-staging.yml under environment section

# Redeploy
# In Dokploy: Click "Redeploy" button
```

#### Cause 1.2: Database Not Available
**Error Pattern**: `Connection refused` or `Could not connect to database`

**Solution**:
```bash
# Verify PostgreSQL is running
ssh root@194.238.16.237 'docker ps --filter name=postgres-staging'

# Test database connectivity
ssh root@194.238.16.237 'docker exec bizosaas-postgres-staging pg_isready'

# If PostgreSQL not running, start infrastructure first
# See: PHASE1_INFRASTRUCTURE_DEPLOYMENT.md

# Restart backend service after infrastructure is up
ssh root@194.238.16.237 'docker restart <container-name>'
```

#### Cause 1.3: Port Already in Use
**Error Pattern**: `Address already in use` or `bind: address already in use`

**Solution**:
```bash
# Find what's using the port
ssh root@194.238.16.237 'netstat -tulpn | grep <port>'

# Stop conflicting container
ssh root@194.238.16.237 'docker stop <conflicting-container>'

# Or change port in docker-compose.yml
# ports:
#   - "8001:8001"  # Change to "8101:8001" if 8001 is taken

# Restart service
ssh root@194.238.16.237 'docker restart <container-name>'
```

#### Cause 1.4: Insufficient Permissions
**Error Pattern**: `Permission denied` or `Cannot write to directory`

**Solution**:
```bash
# Check container user
ssh root@194.238.16.237 'docker exec <container-name> whoami'

# Fix permissions on volume mounts
ssh root@194.238.16.237 'docker exec <container-name> ls -la /app'

# Rebuild with correct user permissions
# Update Dockerfile with proper USER directive
```

---

## Issue 2: Health Check Failing

### Symptoms
- Container shows "unhealthy" status
- `/health` endpoint returns 500 or times out
- Service appears running but marked unhealthy

### Diagnostic Commands
```bash
# Check health status
ssh root@194.238.16.237 'docker inspect --format="{{json .State.Health}}" <container-name> | jq'

# Test health endpoint directly
curl -v http://194.238.16.237:<port>/health

# Check health check logs
ssh root@194.238.16.237 'docker inspect --format="{{range .State.Health.Log}}{{.Output}}{{end}}" <container-name>'
```

### Common Causes & Solutions

#### Cause 2.1: Service Not Fully Started
**Error Pattern**: Connection refused on health check

**Solution**:
```bash
# Increase health check start period
# In docker-compose.yml:
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
  interval: 30s
  timeout: 10s
  retries: 5
  start_period: 60s  # Increase this if service takes time to start

# Redeploy with updated configuration
```

#### Cause 2.2: Database Migrations Pending
**Error Pattern**: `Database schema out of sync` or `Migration not applied`

**Solution**:
```bash
# For Django services (Wagtail, Django CRM)
ssh root@194.238.16.237 'docker exec <container-name> python manage.py migrate'

# For Node.js services
ssh root@194.238.16.237 'docker exec <container-name> npm run db:migrate'

# Restart service
ssh root@194.238.16.237 'docker restart <container-name>'
```

#### Cause 2.3: Dependencies Not Ready
**Error Pattern**: Service starts before dependencies

**Solution**:
```bash
# Ensure proper depends_on configuration
# In docker-compose.yml:
depends_on:
  postgres:
    condition: service_healthy
  redis:
    condition: service_healthy

# Or use wait-for-it script
# Add to Dockerfile:
# COPY wait-for-it.sh /wait-for-it.sh
# RUN chmod +x /wait-for-it.sh

# Update CMD:
# CMD ["/wait-for-it.sh", "postgres:5432", "--", "npm", "start"]
```

---

## Issue 3: Database Connection Issues

### Symptoms
- "Connection refused" errors
- "Host not found" errors
- Timeout connecting to PostgreSQL

### Diagnostic Commands
```bash
# Test database connectivity from container
ssh root@194.238.16.237 'docker exec <container-name> nc -zv bizosaas-postgres-staging 5432'

# Test from host
ssh root@194.238.16.237 'nc -zv localhost 5432'

# Check PostgreSQL logs
ssh root@194.238.16.237 'docker logs bizosaas-postgres-staging --tail 100'

# Verify connection string
ssh root@194.238.16.237 'docker exec <container-name> env | grep DATABASE_URL'
```

### Common Causes & Solutions

#### Cause 3.1: Wrong Database Host
**Error Pattern**: `getaddrinfo ENOTFOUND` or `Unknown host`

**Solution**:
```bash
# In staging, use container name not localhost
# Correct:   postgresql://admin:password@bizosaas-postgres-staging:5432/dbname
# Incorrect: postgresql://admin:password@localhost:5432/dbname

# Update environment variable
# DATABASE_URL=postgresql://admin:BizOSaaS2025!StagingDB@bizosaas-postgres-staging:5432/bizosaas_staging

# Redeploy service
```

#### Cause 3.2: Database Credentials Invalid
**Error Pattern**: `authentication failed` or `password authentication failed`

**Solution**:
```bash
# Verify credentials in infrastructure project
ssh root@194.238.16.237 'docker exec bizosaas-postgres-staging env | grep POSTGRES_PASSWORD'

# Match credentials in backend service
# Ensure POSTGRES_PASSWORD matches in both projects

# Update in Dokploy environment variables
# Redeploy backend service
```

#### Cause 3.3: Connection Pool Exhausted
**Error Pattern**: `too many clients` or `connection pool timeout`

**Solution**:
```bash
# Check current connections
ssh root@194.238.16.237 'docker exec bizosaas-postgres-staging psql -U admin -d bizosaas_staging -c "SELECT count(*) FROM pg_stat_activity;"'

# Increase max connections in PostgreSQL
# In infrastructure docker-compose:
# command: postgres -c max_connections=200

# Or reduce connection pool size in application
# In backend service config:
# pool: { min: 2, max: 10 }  # Reduce max from default

# Restart both infrastructure and backend
```

#### Cause 3.4: Not in Same Network
**Error Pattern**: `Name does not resolve` or `network not found`

**Solution**:
```bash
# Check network membership
ssh root@194.238.16.237 'docker network inspect bizosaas-staging-network'

# Ensure both containers are in same network
# Should see both infrastructure and backend containers listed

# If not in network, reconnect
ssh root@194.238.16.237 'docker network connect bizosaas-staging-network <container-name>'

# Or redeploy with correct network configuration
# networks:
#   - bizosaas-staging-network
```

---

## Issue 4: Redis Connection Timeout

### Symptoms
- Cache operations timing out
- "ECONNREFUSED" errors for Redis
- Session storage failures

### Diagnostic Commands
```bash
# Test Redis connectivity
ssh root@194.238.16.237 'docker exec <container-name> nc -zv bizosaas-redis-staging 6379'

# Test Redis from container
ssh root@194.238.16.237 'docker exec <container-name> redis-cli -h bizosaas-redis-staging ping'

# Check Redis health
ssh root@194.238.16.237 'docker exec bizosaas-redis-staging redis-cli ping'

# Check Redis logs
ssh root@194.238.16.237 'docker logs bizosaas-redis-staging --tail 50'
```

### Solutions

#### Solution 4.1: Use Correct Redis Host
```bash
# Correct Redis URL format for staging
REDIS_URL=redis://bizosaas-redis-staging:6379/1

# Not localhost
# Not 127.0.0.1

# Update environment variable and redeploy
```

#### Solution 4.2: Redis Database Number Conflict
```bash
# Each service should use different Redis database number
# Brain API:       redis://bizosaas-redis-staging:6379/1
# Wagtail CMS:     redis://bizosaas-redis-staging:6379/2
# Django CRM:      redis://bizosaas-redis-staging:6379/3
# Directory API:   redis://bizosaas-redis-staging:6379/4
# CorelDove:       redis://bizosaas-redis-staging:6379/5
# AI Agents:       redis://bizosaas-redis-staging:6379/6
# Amazon Sourcing: redis://bizosaas-redis-staging:6379/7
# Saleor:          redis://bizosaas-redis-staging:6379/8

# Update if conflicts exist
```

#### Solution 4.3: Redis Memory Limit Reached
```bash
# Check Redis memory usage
ssh root@194.238.16.237 'docker exec bizosaas-redis-staging redis-cli info memory'

# Increase memory limit in infrastructure
# Or enable eviction policy
# In infrastructure docker-compose:
# command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru

# Restart Redis
ssh root@194.238.16.237 'docker restart bizosaas-redis-staging'
```

---

## Issue 5: API Key Not Working

### Symptoms
- 401 Unauthorized responses
- "Invalid API key" errors
- AI services not responding

### Diagnostic Commands
```bash
# Check if environment variable is set
ssh root@194.238.16.237 'docker exec <container-name> env | grep API_KEY'

# Test API key validity (OpenRouter)
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" https://openrouter.ai/api/v1/models

# Test API key validity (OpenAI)
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models

# Test API key validity (Anthropic)
curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/messages
```

### Solutions

#### Solution 5.1: API Key Not Set in Environment
```bash
# Add missing API key in Dokploy
# Navigate to: Application → Environment Variables
# Add: OPENROUTER_API_KEY=sk-or-v1-...

# Redeploy service
# Click "Redeploy" button
```

#### Solution 5.2: API Key Has Extra Spaces/Quotes
```bash
# Check for hidden characters
ssh root@194.238.16.237 'docker exec <container-name> env | grep API_KEY | cat -A'

# Should NOT show quotes or spaces
# Correct:   OPENROUTER_API_KEY=sk-or-v1-abc123
# Incorrect: OPENROUTER_API_KEY="sk-or-v1-abc123"
# Incorrect: OPENROUTER_API_KEY=sk-or-v1-abc123

# Update without quotes/spaces in Dokploy
```

#### Solution 5.3: API Key Expired or Revoked
```bash
# Generate new API key from provider
# OpenRouter: https://openrouter.ai/keys
# OpenAI: https://platform.openai.com/api-keys
# Anthropic: https://console.anthropic.com/settings/keys

# Update in Dokploy environment variables
# Redeploy service
```

#### Solution 5.4: Insufficient API Key Permissions
```bash
# Check API key permissions in provider dashboard
# Ensure key has required scopes/permissions

# For AWS (Amazon Sourcing):
# IAM → User → Permissions → Product Advertising API

# For Stripe:
# Dashboard → Developers → API Keys → Verify "Write" access

# Create new key with correct permissions if needed
```

---

## Issue 6: High Memory Usage

### Symptoms
- Container using >80% memory
- OOM (Out of Memory) kills
- System becoming unresponsive

### Diagnostic Commands
```bash
# Check memory usage
ssh root@194.238.16.237 'docker stats --no-stream <container-name>'

# Check memory limit
ssh root@194.238.16.237 'docker inspect <container-name> | grep -A 5 Memory'

# Check system memory
ssh root@194.238.16.237 'free -h'

# Identify memory-hungry processes
ssh root@194.238.16.237 'docker exec <container-name> ps aux --sort=-%mem | head -10'
```

### Solutions

#### Solution 6.1: Set Memory Limits
```bash
# In docker-compose.yml, add resource limits:
deploy:
  resources:
    limits:
      memory: 512M
    reservations:
      memory: 256M

# Restart service with new limits
```

#### Solution 6.2: Memory Leak in Application
```bash
# Enable garbage collection logging (Node.js)
# In docker-compose environment:
NODE_OPTIONS=--max-old-space-size=512 --expose-gc

# For Python services
# In docker-compose environment:
PYTHONUNBUFFERED=1

# Monitor for leaks
ssh root@194.238.16.237 'docker exec <container-name> node --inspect'
```

#### Solution 6.3: Too Many Workers/Processes
```bash
# Reduce worker count
# For Node.js (cluster mode):
WORKERS=2  # Reduce from default

# For Django/Python (Gunicorn):
GUNICORN_WORKERS=2  # Reduce workers
GUNICORN_THREADS=2   # Reduce threads

# Update environment variables and redeploy
```

---

## Issue 7: Slow Response Times

### Symptoms
- API requests taking >5 seconds
- Timeouts on health checks
- Frontend appears sluggish

### Diagnostic Commands
```bash
# Measure response time
time curl http://194.238.16.237:<port>/health

# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s http://194.238.16.237:<port>/api/endpoint

# Monitor real-time performance
ssh root@194.238.16.237 'docker stats <container-name>'

# Check for blocking operations in logs
ssh root@194.238.16.237 'docker logs <container-name> --tail 100 | grep -i "slow\|timeout\|wait"'
```

### Solutions

#### Solution 7.1: Enable Response Caching
```bash
# Verify Redis cache is being used
ssh root@194.238.16.237 'docker exec <container-name> redis-cli -h bizosaas-redis-staging info stats'

# Check cache hit rate
# Should be >70% for good performance

# Enable caching in application
# For Express.js:
# app.use(cacheMiddleware({ ttl: 300 }))

# For Django:
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://bizosaas-redis-staging:6379/2',
#     }
# }
```

#### Solution 7.2: Add Database Indexes
```bash
# Check slow queries
ssh root@194.238.16.237 'docker exec bizosaas-postgres-staging psql -U admin -d bizosaas_staging -c "SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"'

# Add missing indexes
# In Django migrations or SQL:
# CREATE INDEX idx_table_column ON table_name(column_name);

# Analyze and optimize tables
ssh root@194.238.16.237 'docker exec bizosaas-postgres-staging psql -U admin -d bizosaas_staging -c "ANALYZE;"'
```

#### Solution 7.3: Increase Resource Allocation
```bash
# In docker-compose.yml:
deploy:
  resources:
    limits:
      cpus: '2.0'      # Increase CPU
      memory: 1024M    # Increase memory
    reservations:
      cpus: '1.0'
      memory: 512M

# Redeploy with new limits
```

---

## Issue 8: Port Conflicts

### Symptoms
- "Address already in use" error
- Service won't bind to port
- Multiple services trying same port

### Diagnostic Commands
```bash
# Check what's using a port
ssh root@194.238.16.237 'netstat -tulpn | grep <port>'

# List all exposed ports
ssh root@194.238.16.237 'docker ps --format "{{.Names}}\t{{.Ports}}"'

# Check for duplicate port mappings
ssh root@194.238.16.237 'docker-compose -f dokploy-backend-staging.yml config | grep -A 1 "ports:"'
```

### Solutions

#### Solution 8.1: Change External Port
```bash
# In docker-compose.yml:
# Original:
ports:
  - "8001:8001"

# Change to:
ports:
  - "8101:8001"  # External port 8101, internal stays 8001

# Update all references to new port
# Redeploy
```

#### Solution 8.2: Remove Port Duplication
```bash
# Check docker-compose for duplicate port assignments
# Each service must have unique external port

# Brain API:     8001:8001
# Wagtail:       8002:8002
# Django CRM:    8003:8003
# Directory:     8004:8004
# CorelDove:     8005:8005
# AI Agents:     8010:8010
# Amazon:        8085:8085
# Saleor:        8000:8000

# Ensure no overlaps
```

---

## Issue 9: Network Issues

### Symptoms
- Services can't communicate
- DNS resolution failures
- "network not found" errors

### Diagnostic Commands
```bash
# Check network exists
ssh root@194.238.16.237 'docker network ls | grep bizosaas-staging-network'

# Inspect network
ssh root@194.238.16.237 'docker network inspect bizosaas-staging-network'

# Test DNS resolution
ssh root@194.238.16.237 'docker exec <container-name> nslookup bizosaas-postgres-staging'

# Test network connectivity
ssh root@194.238.16.237 'docker exec <container-name> ping -c 3 bizosaas-postgres-staging'
```

### Solutions

#### Solution 9.1: Create Missing Network
```bash
# Create network if it doesn't exist
ssh root@194.238.16.237 'docker network create bizosaas-staging-network'

# Reconnect containers to network
ssh root@194.238.16.237 'docker network connect bizosaas-staging-network <container-name>'

# Or redeploy with correct network configuration
```

#### Solution 9.2: Network Configuration Mismatch
```bash
# In docker-compose.yml:
networks:
  bizosaas-staging-network:
    external: true  # Must be external: true

# NOT:
# networks:
#   bizosaas-staging-network:
#     driver: bridge  # This creates new network instead of using existing

# Correct and redeploy
```

---

## Issue 10: Build Failures

### Symptoms
- Deployment fails during build
- "Cannot find Dockerfile" error
- Build context errors

### Diagnostic Commands
```bash
# Check Dockerfile exists
git ls-remote https://github.com/Bizoholic-Digital/bizosaas-platform.git

# Verify Dockerfile path
# In docker-compose:
# dockerfile: ai/services/bizosaas-brain/Dockerfile

# Check build logs in Dokploy
# Navigate to: Application → Build Logs
```

### Solutions

#### Solution 10.1: Incorrect Dockerfile Path
```bash
# Verify path in repository
# Correct paths:
# - ai/services/bizosaas-brain/Dockerfile
# - cms/wagtail-cms/Dockerfile
# - backend/django-crm/Dockerfile
# - backend/business-directory/Dockerfile
# - ecommerce/services/coreldove-backend/Dockerfile
# - ai/services/ai-agents/Dockerfile
# - integrations/amazon-sourcing/Dockerfile

# Update in docker-compose.yml
# Redeploy
```

#### Solution 10.2: Build Timeout
```bash
# Increase build timeout in Dokploy
# Settings → Build Timeout → 30 minutes

# Or pre-build images locally and push to registry
docker build -t brain-api:latest -f ai/services/bizosaas-brain/Dockerfile .
docker tag brain-api:latest registry.example.com/brain-api:latest
docker push registry.example.com/brain-api:latest

# Update docker-compose to use pre-built image
```

---

## Emergency Procedures

### Full Service Restart
```bash
# Stop all backend services
ssh root@194.238.16.237 'cd /path/to/project && docker-compose -f dokploy-backend-staging.yml down'

# Start all services
ssh root@194.238.16.237 'cd /path/to/project && docker-compose -f dokploy-backend-staging.yml up -d'

# Or via Dokploy UI:
# Navigate to Project → Stop All → Start All
```

### Rollback to Previous Version
```bash
# In Dokploy, click "Deployments" tab
# Find previous successful deployment
# Click "Rollback" button

# Or manually:
ssh root@194.238.16.237 'docker pull <previous-image-tag>'
ssh root@194.238.16.237 'docker-compose -f dokploy-backend-staging.yml up -d'
```

### Complete Reset
```bash
# WARNING: This removes all data

# Stop all services
ssh root@194.238.16.237 'docker-compose -f dokploy-backend-staging.yml down -v'

# Remove all containers
ssh root@194.238.16.237 'docker rm -f $(docker ps -a --filter "name=staging" -q)'

# Remove volumes (WARNING: DATA LOSS)
ssh root@194.238.16.237 'docker volume prune -f'

# Redeploy from scratch
# Follow PHASE2_BACKEND_DEPLOYMENT.md
```

---

## Getting Help

### Check Logs First
```bash
# Always start with logs
ssh root@194.238.16.237 'docker logs <container-name> --tail 200'

# Follow logs in real-time
ssh root@194.238.16.237 'docker logs -f <container-name>'

# Search for specific errors
ssh root@194.238.16.237 'docker logs <container-name> | grep -i error'
```

### Collect Diagnostic Information
```bash
# Container status
ssh root@194.238.16.237 'docker ps -a'

# Resource usage
ssh root@194.238.16.237 'docker stats --no-stream'

# Network configuration
ssh root@194.238.16.237 'docker network inspect bizosaas-staging-network'

# Environment variables (sanitize sensitive info)
ssh root@194.238.16.237 'docker exec <container-name> env'

# System resources
ssh root@194.238.16.237 'free -h && df -h'
```

### Contact Support
When reporting issues, include:
1. Container name
2. Error message from logs
3. Steps to reproduce
4. Output of diagnostic commands
5. Recent changes made

---

**Document Version**: 1.0
**Last Updated**: October 10, 2025
**For**: Phase 2 Backend Services Deployment
