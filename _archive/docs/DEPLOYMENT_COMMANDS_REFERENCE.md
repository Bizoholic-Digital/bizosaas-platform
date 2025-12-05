# Infrastructure Deployment - Command Reference

## Quick Access

**VPS IP**: 194.238.16.237
**Dokploy URL**: http://194.238.16.237:3000
**Project**: bizosaas-infrastructure-staging

---

## Pre-Deployment Commands

### Check VPS Connectivity
```bash
# Test SSH access
ssh root@194.238.16.237

# Test HTTP access
curl -I http://194.238.16.237:3000

# Check available ports
nmap -p 5432,6379,7233,8009,8082,8200 194.238.16.237
```

### Verify Local Files
```bash
# Check configuration file exists
ls -lh /home/alagiri/projects/bizoholic/dokploy-infrastructure-staging.yml

# Validate docker-compose syntax
docker-compose -f /home/alagiri/projects/bizoholic/dokploy-infrastructure-staging.yml config --quiet

# Check database init script
ls -lh /home/alagiri/projects/bizoholic/init-scripts/01-create-databases.sql
```

---

## Deployment via Dokploy UI

### Access Dokploy
```bash
# Open in browser
xdg-open http://194.238.16.237:3000  # Linux
open http://194.238.16.237:3000      # macOS
start http://194.238.16.237:3000     # Windows

# Or simply navigate to:
http://194.238.16.237:3000
```

### Upload Configuration
```bash
# Configuration file location
/home/alagiri/projects/bizoholic/dokploy-infrastructure-staging.yml

# Copy to clipboard (Linux)
cat /home/alagiri/projects/bizoholic/dokploy-infrastructure-staging.yml | xclip -selection clipboard

# Or use file upload in Dokploy UI
```

---

## Alternative: SSH Deployment

### Deploy via SSH
```bash
# SSH into VPS
ssh root@194.238.16.237

# Navigate to Dokploy projects directory
cd /opt/dokploy/projects

# Create project directory
mkdir -p bizosaas-infrastructure-staging
cd bizosaas-infrastructure-staging

# Upload docker-compose file
# (Use scp or copy from your local machine)

# Deploy with docker-compose
docker-compose -f dokploy-infrastructure-staging.yml up -d

# Check deployment status
docker-compose -f dokploy-infrastructure-staging.yml ps
```

### Upload Files via SCP
```bash
# Upload docker-compose configuration
scp /home/alagiri/projects/bizoholic/dokploy-infrastructure-staging.yml \
    root@194.238.16.237:/opt/dokploy/projects/bizosaas-infrastructure-staging/

# Upload database init script
scp /home/alagiri/projects/bizoholic/init-scripts/01-create-databases.sql \
    root@194.238.16.237:/opt/dokploy/projects/bizosaas-infrastructure-staging/init-scripts/

# Upload verification script
scp /home/alagiri/projects/bizoholic/verify-infrastructure-deployment.sh \
    root@194.238.16.237:/root/
```

---

## Post-Deployment Verification

### Run Automated Verification
```bash
# From local machine (after downloading script)
cd /home/alagiri/projects/bizoholic
chmod +x verify-infrastructure-deployment.sh
./verify-infrastructure-deployment.sh

# Or run on VPS via SSH
ssh root@194.238.16.237 'bash -s' < verify-infrastructure-deployment.sh
```

### Manual Port Checks
```bash
# Check all infrastructure ports
for port in 5432 6379 7233 8009 8082 8200; do
  echo -n "Port $port: "
  nc -zv 194.238.16.237 $port 2>&1 | grep -q succeeded && echo "OPEN" || echo "CLOSED"
done

# Or using telnet
telnet 194.238.16.237 5432  # PostgreSQL
telnet 194.238.16.237 6379  # Redis
telnet 194.238.16.237 8200  # Vault
telnet 194.238.16.237 8082  # Temporal UI
telnet 194.238.16.237 8009  # Temporal Integration
```

### Test HTTP Endpoints
```bash
# Vault health check
curl -s http://194.238.16.237:8200/v1/sys/health | jq .

# Temporal UI
curl -I http://194.238.16.237:8082

# Temporal Integration health
curl -s http://194.238.16.237:8009/health | jq .

# Check all endpoints
for url in \
  "http://194.238.16.237:8200/v1/sys/health" \
  "http://194.238.16.237:8082" \
  "http://194.238.16.237:8009/health"; do
  echo -n "Testing $url: "
  curl -s -o /dev/null -w "%{http_code}\n" "$url"
done
```

### Test Database Connectivity
```bash
# PostgreSQL connection test
PGPASSWORD="BizOSaaS2025!StagingDB" psql \
  -h 194.238.16.237 \
  -p 5432 \
  -U admin \
  -d bizosaas_staging \
  -c "SELECT version();"

# List databases
PGPASSWORD="BizOSaaS2025!StagingDB" psql \
  -h 194.238.16.237 \
  -p 5432 \
  -U admin \
  -d postgres \
  -c "\l"

# Check pgvector extension
PGPASSWORD="BizOSaaS2025!StagingDB" psql \
  -h 194.238.16.237 \
  -p 5432 \
  -U admin \
  -d bizosaas_staging \
  -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

### Test Redis Connectivity
```bash
# Redis PING test
redis-cli -h 194.238.16.237 -p 6379 ping

# Redis INFO
redis-cli -h 194.238.16.237 -p 6379 info server

# Test SET/GET
redis-cli -h 194.238.16.237 -p 6379 SET test_key "test_value"
redis-cli -h 194.238.16.237 -p 6379 GET test_key
redis-cli -h 194.238.16.237 -p 6379 DEL test_key
```

---

## Container Management Commands

### Via SSH on VPS

#### Check Container Status
```bash
# List all containers
docker ps

# Filter infrastructure containers
docker ps | grep bizosaas

# Show container stats
docker stats --no-stream

# Check specific container
docker inspect bizosaas-postgres-staging
```

#### View Logs
```bash
# View all infrastructure logs
docker-compose -f dokploy-infrastructure-staging.yml logs

# Follow logs in real-time
docker-compose -f dokploy-infrastructure-staging.yml logs -f

# View specific service logs
docker logs bizosaas-postgres-staging
docker logs bizosaas-redis-staging
docker logs bizosaas-vault-staging
docker logs bizosaas-temporal-server-staging
docker logs bizosaas-temporal-ui-staging
docker logs bizosaas-temporal-integration-staging

# Follow specific container logs
docker logs -f bizosaas-postgres-staging

# View last 100 lines
docker logs --tail 100 bizosaas-postgres-staging
```

#### Restart Containers
```bash
# Restart all infrastructure services
docker-compose -f dokploy-infrastructure-staging.yml restart

# Restart specific container
docker restart bizosaas-postgres-staging
docker restart bizosaas-redis-staging
docker restart bizosaas-vault-staging
docker restart bizosaas-temporal-server-staging
docker restart bizosaas-temporal-ui-staging
docker restart bizosaas-temporal-integration-staging
```

#### Stop/Start Services
```bash
# Stop all services
docker-compose -f dokploy-infrastructure-staging.yml stop

# Start all services
docker-compose -f dokploy-infrastructure-staging.yml start

# Stop and remove containers
docker-compose -f dokploy-infrastructure-staging.yml down

# Stop and remove with volumes (WARNING: DATA LOSS!)
docker-compose -f dokploy-infrastructure-staging.yml down -v
```

#### Execute Commands in Containers
```bash
# PostgreSQL shell
docker exec -it bizosaas-postgres-staging psql -U admin -d bizosaas_staging

# Redis CLI
docker exec -it bizosaas-redis-staging redis-cli

# Vault CLI
docker exec -it bizosaas-vault-staging vault status

# Check container shell
docker exec -it bizosaas-postgres-staging bash
```

---

## Database Management Commands

### PostgreSQL Operations

#### Backup Database
```bash
# Backup main database
docker exec bizosaas-postgres-staging pg_dump -U admin bizosaas_staging > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup all databases
docker exec bizosaas-postgres-staging pg_dumpall -U admin > backup_all_$(date +%Y%m%d_%H%M%S).sql

# Backup to compressed file
docker exec bizosaas-postgres-staging pg_dump -U admin bizosaas_staging | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

#### Restore Database
```bash
# Restore from backup
cat backup_20251010.sql | docker exec -i bizosaas-postgres-staging psql -U admin -d bizosaas_staging

# Restore from compressed backup
gunzip -c backup_20251010.sql.gz | docker exec -i bizosaas-postgres-staging psql -U admin -d bizosaas_staging
```

#### Database Queries
```bash
# List all databases
docker exec bizosaas-postgres-staging psql -U admin -d postgres -c "\l"

# List all tables in database
docker exec bizosaas-postgres-staging psql -U admin -d bizosaas_staging -c "\dt"

# Check database size
docker exec bizosaas-postgres-staging psql -U admin -d postgres -c "SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) AS size FROM pg_database;"

# Check active connections
docker exec bizosaas-postgres-staging psql -U admin -d postgres -c "SELECT * FROM pg_stat_activity;"
```

### Redis Operations

#### Backup Redis
```bash
# Trigger Redis save
docker exec bizosaas-redis-staging redis-cli SAVE

# Copy RDB file
docker cp bizosaas-redis-staging:/data/dump.rdb ./redis_backup_$(date +%Y%m%d_%H%M%S).rdb
```

#### Redis Monitoring
```bash
# Monitor Redis commands
docker exec bizosaas-redis-staging redis-cli MONITOR

# Check Redis stats
docker exec bizosaas-redis-staging redis-cli INFO

# Check memory usage
docker exec bizosaas-redis-staging redis-cli INFO memory

# List all keys (use carefully!)
docker exec bizosaas-redis-staging redis-cli KEYS "*"

# Get Redis configuration
docker exec bizosaas-redis-staging redis-cli CONFIG GET "*"
```

---

## Vault Management Commands

### Vault Operations

#### Vault Status
```bash
# Check Vault status
curl http://194.238.16.237:8200/v1/sys/health

# Via container
docker exec bizosaas-vault-staging vault status
```

#### Vault Token Management
```bash
# Login with root token
docker exec -it bizosaas-vault-staging vault login staging-root-token-bizosaas-2025

# Create new token
docker exec bizosaas-vault-staging vault token create

# List tokens
docker exec bizosaas-vault-staging vault token lookup
```

#### Vault Secrets Management
```bash
# Enable KV secrets engine (if not enabled)
docker exec bizosaas-vault-staging vault secrets enable -path=secret kv-v2

# Write secret
docker exec bizosaas-vault-staging vault kv put secret/test key=value

# Read secret
docker exec bizosaas-vault-staging vault kv get secret/test

# List secrets
docker exec bizosaas-vault-staging vault kv list secret/
```

---

## Temporal Management Commands

### Temporal Operations

#### Temporal Server Status
```bash
# Check Temporal Server health
docker exec bizosaas-temporal-server-staging tctl cluster health

# List namespaces
docker exec bizosaas-temporal-server-staging tctl namespace list

# Create namespace
docker exec bizosaas-temporal-server-staging tctl namespace register --namespace test-namespace
```

#### Workflow Management
```bash
# List workflows
docker exec bizosaas-temporal-server-staging tctl workflow list

# Describe workflow
docker exec bizosaas-temporal-server-staging tctl workflow describe --workflow-id <workflow-id>

# Show workflow history
docker exec bizosaas-temporal-server-staging tctl workflow show --workflow-id <workflow-id>
```

---

## Network Management Commands

### Network Operations

#### Check Network
```bash
# List Docker networks
docker network ls

# Inspect infrastructure network
docker network inspect bizosaas-staging-network

# Show connected containers
docker network inspect bizosaas-staging-network --format='{{range .Containers}}{{.Name}} {{end}}'
```

#### Test Internal Connectivity
```bash
# Test from one container to another
docker exec bizosaas-temporal-integration-staging ping -c 3 bizosaas-postgres-staging

# Test PostgreSQL from Temporal Server
docker exec bizosaas-temporal-server-staging nc -zv bizosaas-postgres-staging 5432

# Test Redis from Temporal Integration
docker exec bizosaas-temporal-integration-staging nc -zv bizosaas-redis-staging 6379
```

---

## Volume Management Commands

### Volume Operations

#### List Volumes
```bash
# List all volumes
docker volume ls

# Inspect specific volume
docker volume inspect postgres_staging_data
docker volume inspect redis_staging_data
docker volume inspect vault_staging_data
docker volume inspect temporal_staging_data
```

#### Backup Volumes
```bash
# Backup PostgreSQL volume
docker run --rm -v postgres_staging_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup_$(date +%Y%m%d).tar.gz -C /data .

# Backup Redis volume
docker run --rm -v redis_staging_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/redis_backup_$(date +%Y%m%d).tar.gz -C /data .

# Backup Vault volume
docker run --rm -v vault_staging_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/vault_backup_$(date +%Y%m%d).tar.gz -C /data .
```

#### Restore Volumes
```bash
# Restore PostgreSQL volume
docker run --rm -v postgres_staging_data:/data -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/postgres_backup_20251010.tar.gz"
```

---

## Monitoring Commands

### Resource Usage

#### Check System Resources
```bash
# Check disk usage
df -h

# Check Docker disk usage
docker system df

# Check container resource usage
docker stats --no-stream

# Check specific container resources
docker stats bizosaas-postgres-staging --no-stream
```

#### Monitor Performance
```bash
# Real-time container stats
docker stats

# Top processes in container
docker top bizosaas-postgres-staging

# Check container events
docker events --filter 'container=bizosaas-postgres-staging'
```

---

## Troubleshooting Commands

### Debug Container Issues

#### Container Not Starting
```bash
# Check container logs
docker logs bizosaas-postgres-staging

# Inspect container configuration
docker inspect bizosaas-postgres-staging

# Check container processes
docker top bizosaas-postgres-staging

# Verify image exists
docker images | grep bizosaas
```

#### Port Conflicts
```bash
# Check which process is using port
sudo netstat -tlnp | grep :5432
sudo lsof -i :5432

# Kill process using port (if needed)
sudo kill -9 $(sudo lsof -t -i:5432)
```

#### Network Issues
```bash
# Restart Docker daemon
sudo systemctl restart docker

# Recreate network
docker network rm bizosaas-staging-network
docker network create bizosaas-staging-network

# Check firewall rules
sudo ufw status
sudo iptables -L -n
```

---

## Cleanup Commands

### Remove Infrastructure

#### Stop and Remove Containers
```bash
# Stop all services gracefully
docker-compose -f dokploy-infrastructure-staging.yml stop

# Remove containers
docker-compose -f dokploy-infrastructure-staging.yml rm -f

# Stop and remove in one command
docker-compose -f dokploy-infrastructure-staging.yml down
```

#### Remove Volumes (WARNING: DATA LOSS!)
```bash
# Remove all infrastructure volumes
docker volume rm postgres_staging_data
docker volume rm redis_staging_data
docker volume rm vault_staging_data
docker volume rm temporal_staging_data

# Or remove with docker-compose
docker-compose -f dokploy-infrastructure-staging.yml down -v
```

#### Clean Up Everything
```bash
# Remove unused containers
docker container prune -f

# Remove unused images
docker image prune -a -f

# Remove unused volumes
docker volume prune -f

# Remove unused networks
docker network prune -f

# Clean up everything
docker system prune -a --volumes -f
```

---

## Emergency Commands

### Quick Recovery

#### Force Restart All Services
```bash
# Force restart all containers
docker-compose -f dokploy-infrastructure-staging.yml restart --force-recreate

# Or individual containers
docker restart -t 10 bizosaas-postgres-staging
```

#### Reset Everything
```bash
# Stop everything
docker-compose -f dokploy-infrastructure-staging.yml down

# Remove volumes (CAREFUL!)
docker volume rm postgres_staging_data redis_staging_data vault_staging_data temporal_staging_data

# Redeploy from scratch
docker-compose -f dokploy-infrastructure-staging.yml up -d
```

---

## Useful Aliases

Add these to your `.bashrc` or `.zshrc`:

```bash
# Infrastructure aliases
alias infra-ps='docker-compose -f dokploy-infrastructure-staging.yml ps'
alias infra-logs='docker-compose -f dokploy-infrastructure-staging.yml logs -f'
alias infra-restart='docker-compose -f dokploy-infrastructure-staging.yml restart'
alias infra-stop='docker-compose -f dokploy-infrastructure-staging.yml stop'
alias infra-start='docker-compose -f dokploy-infrastructure-staging.yml start'

# Database aliases
alias pg-shell='docker exec -it bizosaas-postgres-staging psql -U admin -d bizosaas_staging'
alias redis-cli='docker exec -it bizosaas-redis-staging redis-cli'
alias vault-cli='docker exec -it bizosaas-vault-staging vault'

# Monitoring aliases
alias infra-stats='docker stats --no-stream'
alias infra-health='./verify-infrastructure-deployment.sh'
```

---

**Command Reference Complete - Infrastructure Management Made Easy!**
