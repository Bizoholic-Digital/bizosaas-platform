---
description: Comprehensive BizOSaaS Platform Fix and Optimization Plan
---

# BizOSaaS Platform - Comprehensive Fix and Optimization Plan

## Current Situation Analysis

### Server Status (KVM2 - 194.238.16.237)
- **Resources**: 2 vCPU, 8GB RAM, 100GB Storage
- **Issue**: Dokploy returning 502 errors, affecting SSO authentication
- **Running Services**: Multiple containers with redundant Redis instances

### Service Inventory

#### ✅ Currently Running Services:
1. **Lago Billing** (Up 12 hours)
   - lago-front, lago-api, lago-worker
   - Target: https://billing.bizoholic.net

2. **Authentik SSO** (Partially healthy)
   - code-authentik-server-1 (starting)
   - code-authentik-worker-1 (starting)
   - authentik-sso-hxogz6-authentik-server-1 (healthy)
   - authentik-sso-hxogz6-authentik-worker-1 (unhealthy)
   - Target: https://auth-sso.bizoholic.net

3. **Brain Gateway + MCPs** (Up 12 hours, healthy)
   - bizosaas-brain-staging
   - 7 MCP services (filesystem, github, slack, meesho, brave-search, fluentcrm, google-drive)
   - Target: https://api.bizoholic.net

4. **Portals** (Up 12 hours, healthy)
   - bizosaas-admin-dashboard-legacy
   - compose-generate-open-source-transmitter-kks6gu-client-portal-1
   - business-directory
   - Targets: 
     - https://admin.bizoholic.net
     - https://app.bizoholic.net
     - https://directory.bizoholic.net

5. **Traefik** (Up 12 hours)
   - traefik_traefik.1.bh1wx5t4p855ytbob5x4ihjoc

6. **Dokploy** (Up 40 hours)
   - dokploy.1.wr24khyh5au3nys1xahhpxat7
   - dokploy-postgres.1.5trtodv6irj0t5hrydcibtvky
   - dokploy-redis.1.ae9u2mjfz7q6rnhmxh6v98mou

7. **WordPress Sites**
   - bizoholicwebsite-wordpress-rbtyli
   - coreldovewebsite-wordpress-fnoyyo

#### ❌ Issues Identified:
1. **Multiple Authentik instances** (duplicate deployment)
2. **Dokploy 502 error** (dk.bizoholic.com)
3. **SSO authentication failures** on admin and app portals
4. **Multiple Redis instances** (should use Redis Cloud)
5. **No Vault service running** (should be at https://vault.bizoholic.net)
6. **Redundant/old containers** consuming resources

### External Services Available (from credentials.md)
1. **Temporal Cloud**: ap-south-2.aws.api.temporal.io:7233
2. **Redis Cloud**: redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690
3. **Grafana Cloud**: Metrics, Logs, Traces
4. **Neon DB**: PostgreSQL database

---

## Implementation Plan

### Phase 1: Critical Infrastructure Fixes (Priority: URGENT)

#### Step 1.0: Resolve Deployment Build Failures (New Priority)
**Objective**: Fix build errors preventing services from starting.

**1. Bizoholic Frontend**:
- **Error**: `Invalid rewrite found` (source missing)
- **Fix**: Check `next.config.js` and ensure all `rewrites` have a `source` and `destination`.

**2. Thrillring & Business Directory**:
- **Error**: `Missing script: "build"`
- **Fix**: Add `"build": "next build"` (or equivalent) to `package.json`.

**3. Admin Dashboard**:
- **Error**: `COPY portals/admin-dashboard/scripts/vault-injector.js: not found`
- **Fix**: Verify file existence or remove the `COPY` instruction if the file is generated/not needed.

**4. WordPress**:
- **Error**: `refers to undefined network traefik-public`
- **Fix**: Update `docker-compose.bizoholic-cms.yml` to use `dokploy-network` (or create `traefik-public` if strictly required).

#### Step 1.1: Fix Dokploy Service
**Objective**: Restore Dokploy UI access at dk.bizoholic.com

```bash
# SSH into server
ssh root@194.238.16.237

# Check Dokploy logs
docker service logs dokploy.1.wr24khyh5au3nys1xahhpxat7 --tail 100

# Check Traefik configuration
docker service logs traefik_traefik.1.bh1wx5t4p855ytbob5x4ihjoc --tail 100

# Restart Dokploy if needed
docker service update --force dokploy

# Verify Dokploy health
curl -I https://dk.bizoholic.com
```

**Expected Outcome**: Dokploy UI accessible at https://dk.bizoholic.com

---

#### Step 1.2: Clean Up Duplicate Authentik Instances
**Objective**: Remove duplicate Authentik containers, keep only one healthy instance

```bash
# Stop and remove the duplicate "code" instance
docker stop code-authentik-server-1 code-authentik-worker-1
docker rm code-authentik-server-1 code-authentik-worker-1

# Verify the main Authentik instance
docker ps | grep authentik

# Check Authentik health
curl -I https://auth-sso.bizoholic.net
```

**Expected Outcome**: Single Authentik instance running and accessible

---

#### Step 1.3: Deploy/Fix Vault Service
**Objective**: Deploy HashiCorp Vault at https://vault.bizoholic.net

```bash
# Check if Vault compose file exists
cat docker-compose.vault.yml

# Deploy Vault using Dokploy API or CLI
# (Will be done after Dokploy is fixed)
```

**Expected Outcome**: Vault accessible at https://vault.bizoholic.net

---

### Phase 2: Resource Optimization (Priority: HIGH)

#### Step 2.1: Migrate to External Redis Cloud
**Objective**: Remove local Redis instances, use Redis Cloud

**Services to Update**:
- Dokploy (currently using dokploy-redis)
- Any other services using local Redis

**Configuration**:
```yaml
REDIS_URL=redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0
```

**Steps**:
1. Update docker-compose files to use Redis Cloud
2. Remove local Redis containers
3. Verify all services connect successfully

---

#### Step 2.2: Clean Up Unnecessary Containers
**Objective**: Remove old/stopped containers to free resources

```bash
# List all stopped containers
docker ps -a --filter "status=exited"

# Remove old Dokploy instances
docker rm dokploy.1.i9nojxbwynu0tfpfv6ni98u1z
docker rm dokploy.1.pw52isqa1nhpur6j1imhocc4t
docker rm dokploy.1.du8muvu4phdyyw30kq8fsmjd1
docker rm dokploy.1.uz79rppctto135dmp64h32kvc

# Remove old postgres instances
docker rm dokploy-postgres.1.w914i2peo4mqm0q9ilxz0rmmn
docker rm dokploy-postgres.1.dnoba2o8y26dy04g9igynp22a
docker rm dokploy-postgres.1.vte6wt3cjuixf86mhua6bzxzb

# Remove old redis instances
docker rm dokploy-redis.1.fjyukibj1ylkcvzr8py2ueslb
docker rm dokploy-redis.1.ryidv7tpsqkyky8rrrma5sijh
docker rm dokploy-redis.1.pqk9rjx2xoyajlejqa1x18pba
docker rm dokploy-redis.1.nt2s8lt66chm9t9vkgrfffsub

# Prune unused images and volumes
docker image prune -a -f
docker volume prune -f
```

**Expected Outcome**: ~2-3GB storage freed, cleaner container list

---

### Phase 3: Service Domain Configuration (Priority: HIGH)

#### Step 3.1: Verify and Fix Domain Routing

**Services and Domains**:
1. **Lago Billing**: https://billing.bizoholic.net
2. **Business Directory**: https://directory.bizoholic.net
3. **Client Portal**: https://app.bizoholic.net
4. **Admin Portal**: https://admin.bizoholic.net
5. **Authentik SSO**: https://auth-sso.bizoholic.net
6. **Vault**: https://vault.bizoholic.net
7. **Brain Gateway**: https://api.bizoholic.net
8. **Dokploy**: https://dk.bizoholic.com

**Verification Steps**:
```bash
# Test each domain
for domain in billing.bizoholic.net directory.bizoholic.net app.bizoholic.net admin.bizoholic.net auth-sso.bizoholic.net vault.bizoholic.net api.bizoholic.net dk.bizoholic.com; do
  echo "Testing $domain..."
  curl -I https://$domain
done
```

---

### Phase 4: CI/CD Pipeline Integration (Priority: MEDIUM)

#### Step 4.1: Configure GitHub Actions for Dokploy Deployment

**Workflow Structure**:
1. Build Docker images on GitHub Actions
2. Push to GHCR
3. Deploy to Dokploy via API

**Dokploy API Configuration**:
```bash
# Dokploy API Key (from credentials.md)
DOKPLOY_API_KEY=qmyJeutLJCAtIVDvzbJXySiIBtVvtMKkLiKJisOnqTKbSYxfmApKBLUDJPFtZuby
DOKPLOY_URL=https://dk.bizoholic.com
```

**Projects to Configure**:
1. **utilities** (Lago Billing)
2. **portals** (Business Directory, Client Portal, Admin Portal)
3. **project-core** (Authentik, Vault, Brain Gateway + MCPs)

---

### Phase 5: Monitoring and Observability (Priority: MEDIUM)

#### Step 5.1: Configure Grafana Cloud Integration

**Grafana Cloud Token** (from credentials.md):
```
glc_REDACTED_TOKEN_PLACEHOLDER
```

**Services to Monitor**:
- Metrics: Prometheus endpoint
- Logs: Loki integration
- Traces: Tempo integration

---

## Execution Sequence

### Immediate Actions (Next 30 minutes)
1. ✅ Fix Dokploy 502 error
2. ✅ Remove duplicate Authentik instances
3. ✅ Verify all service domains

### Short-term Actions (Next 2 hours)
4. ✅ Deploy Vault service
5. ✅ Clean up old containers
6. ✅ Migrate to Redis Cloud
7. ✅ Configure Traefik labels for all services

### Medium-term Actions (Next 24 hours)
8. ✅ Set up CI/CD pipeline
9. ✅ Configure Grafana Cloud monitoring
10. ✅ Document all service configurations

---

## Resource Allocation Strategy

### CPU Allocation (2 vCPU total)
- **Traefik**: 0.25 CPU
- **Dokploy**: 0.5 CPU
- **Brain Gateway**: 1.0 CPU (limit), 0.5 CPU (reservation)
- **MCPs** (7 services): 0.25 CPU each = 1.75 CPU total (limits)
- **Portals** (3 services): 0.5 CPU each = 1.5 CPU total
- **Authentik**: 0.5 CPU
- **Vault**: 0.25 CPU
- **Lago**: 0.5 CPU

**Note**: Total limits exceed available CPU, but reservations are within limits. Docker will schedule based on actual usage.

### Memory Allocation (8GB total)
- **Traefik**: 256MB
- **Dokploy**: 1GB
- **Brain Gateway**: 1GB (limit), 512MB (reservation)
- **MCPs** (7 services): 128MB each = 896MB total
- **Portals** (3 services): 512MB each = 1.5GB total
- **Authentik**: 1GB
- **Vault**: 512MB
- **Lago**: 1GB

**Total Reserved**: ~5GB (safe margin for 8GB system)

---

## Success Criteria

### Phase 1 Success:
- ✅ Dokploy UI accessible at https://dk.bizoholic.com
- ✅ Single Authentik instance running
- ✅ Vault deployed and accessible
- ✅ All SSO authentication working

### Phase 2 Success:
- ✅ All services using Redis Cloud
- ✅ Old containers removed
- ✅ Storage usage < 50GB
- ✅ Memory usage < 6GB

### Phase 3 Success:
- ✅ All 8 domains responding with 200 OK
- ✅ SSL certificates valid
- ✅ Traefik routing correctly

### Phase 4 Success:
- ✅ GitHub Actions workflows configured
- ✅ Automated deployments working
- ✅ Dokploy API integration tested

### Phase 5 Success:
- ✅ Grafana dashboards showing metrics
- ✅ Logs flowing to Loki
- ✅ Alerts configured

---

## Rollback Plan

If any step fails:
1. **Dokploy issues**: Restart Dokploy service
2. **Service failures**: Revert to previous docker-compose configuration
3. **Redis migration issues**: Keep local Redis temporarily
4. **Domain routing issues**: Check Traefik labels and restart Traefik

---

## Next Steps

1. Execute Phase 1 immediately
2. Monitor resource usage during Phase 2
3. Test all domains after Phase 3
4. Set up CI/CD in Phase 4
5. Enable monitoring in Phase 5
