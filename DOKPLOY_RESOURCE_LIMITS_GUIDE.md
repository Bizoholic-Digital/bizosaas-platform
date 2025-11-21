# Dokploy Resource Limits Guide
**Date:** November 3, 2025
**Purpose:** Recommended resource limits for all BizOSaaS services

---

## 🎯 GENERAL PRINCIPLES

### Why Set Resource Limits:
1. ✅ **Prevent Resource Starvation** - One service can't starve others
2. ✅ **Predictable Performance** - Consistent performance across services
3. ✅ **Cost Control** - Prevents unexpected resource spikes
4. ✅ **Better Monitoring** - Easy to identify services needing optimization
5. ✅ **Docker Swarm Best Practice** - Better scheduler placement decisions

### Resource Limit Strategy:
- **CPU Limit**: Maximum CPU cores a service can use
- **Memory Limit**: Hard limit - service killed if exceeded
- **Memory Reservation**: Soft limit - guaranteed minimum memory
- **Replicas**: Number of instances (start with 1, scale as needed)

---

## 📊 RECOMMENDED LIMITS BY SERVICE TYPE

### 🎨 Frontend Services (Next.js)

#### Light Frontends (Marketing/Landing Pages)
**Examples:** Bizoholic Frontend, Business Directory

```yaml
Resources:
  CPU Limit:              0.5 (half a CPU core)
  Memory Limit:           256MB
  Memory Reservation:     128MB
  Replicas:               1
  Restart Policy:         on-failure
```

**Rationale:**
- Mostly static content with SSR/SSG
- Low memory footprint
- Can handle 100-500 concurrent users per replica

---

#### Medium Frontends (Dashboards/Portals)
**Examples:** Client Portal, Analytics Dashboard

```yaml
Resources:
  CPU Limit:              1.0 (1 CPU core)
  Memory Limit:           512MB
  Memory Reservation:     256MB
  Replicas:               1 (can scale to 2-3)
  Restart Policy:         on-failure
```

**Rationale:**
- Interactive dashboards with real-time data
- More API calls and state management
- Can handle 200-1000 concurrent users per replica

---

#### Heavy Frontends (E-commerce/Gaming)
**Examples:** CoreLdove Storefront, ThrillRing Gaming

```yaml
Resources:
  CPU Limit:              1.0-1.5 (1-1.5 CPU cores)
  Memory Limit:           512MB-768MB
  Memory Reservation:     256MB-384MB
  Replicas:               1 (can scale to 2-3)
  Restart Policy:         on-failure
```

**Rationale:**
- Complex state management (cart, user sessions)
- Real-time features (Socket.IO, live stats)
- Heavy GraphQL queries
- Can handle 500-2000 concurrent users per replica

---

### 🧠 Backend Services (FastAPI/Python)

#### Brain Gateway (Central API Gateway)
**Example:** backend-brain-gateway

```yaml
Resources:
  CPU Limit:              2.0 (2 CPU cores)
  Memory Limit:           1GB
  Memory Reservation:     512MB
  Replicas:               1 (critical - scale to 2 for HA)
  Restart Policy:         always
```

**Rationale:**
- Central hub - routes ALL frontend requests
- CrewAI agent orchestration (CPU intensive)
- Must handle high concurrency
- **CRITICAL SERVICE** - consider 2 replicas for HA

---

#### Backend Services (FastAPI Microservices)
**Examples:** Gaming Backend, Saleor API, Wagtail CMS

```yaml
Resources:
  CPU Limit:              1.0-1.5 (1-1.5 CPU cores)
  Memory Limit:           768MB-1GB
  Memory Reservation:     384MB-512MB
  Replicas:               1
  Restart Policy:         on-failure
```

**Rationale:**
- Database queries + business logic
- API response processing
- Background tasks (Celery workers)

---

### 🗄️ Database Services

#### PostgreSQL
**Examples:** Saleor DB, BizOSaaS Main DB

```yaml
Resources:
  CPU Limit:              2.0 (2 CPU cores)
  Memory Limit:           2GB
  Memory Reservation:     1GB
  Replicas:               1 (DO NOT SCALE - stateful)
  Restart Policy:         always
```

**Rationale:**
- Heavy query processing
- Index building and caching
- Transaction management
- **STATEFUL** - never scale replicas without replication setup

---

#### Redis (Cache/Queue)
**Example:** Redis cache, Celery broker

```yaml
Resources:
  CPU Limit:              0.5 (half a CPU core)
  Memory Limit:           512MB
  Memory Reservation:     256MB
  Replicas:               1
  Restart Policy:         always
```

**Rationale:**
- In-memory operations (low CPU)
- Memory-dependent performance
- Fast key-value lookups

---

### 📦 Official Images (Pre-built)

#### Saleor Dashboard
**Example:** Saleor Admin UI (port 9000)

```yaml
Resources:
  CPU Limit:              0.5 (half a CPU core)
  Memory Limit:           256MB
  Memory Reservation:     128MB
  Replicas:               1
  Restart Policy:         on-failure
```

**Rationale:**
- Pre-built static UI
- Low resource requirements
- Admin-only access (low concurrency)

---

## 🚀 CURRENT SERVICE RESOURCE ALLOCATION

### Frontend Services (KVM4: 72.60.219.244)

| Service | Port | CPU Limit | Memory Limit | Memory Reserve | Status |
|---------|------|-----------|--------------|----------------|--------|
| **Bizoholic Frontend** | 3001 | 0.5 | 256MB | 128MB | ⏳ To Update |
| **Client Portal** | 3002→3001 | 1.0 | 512MB | 256MB | ⏳ To Update |
| **Business Directory** | 3004 | 0.5 | 256MB | 128MB | ⏳ To Update |
| **CoreLdove Storefront** | 3005 | 1.0 | 512MB | 256MB | ⏳ To Update |
| **ThrillRing Gaming** | 3006 | 1.0 | 512MB | 256MB | ✅ Configured |

### Backend Services (KVM4: 72.60.219.244)

| Service | Port | CPU Limit | Memory Limit | Memory Reserve | Status |
|---------|------|-----------|--------------|----------------|--------|
| **Brain Gateway** | 8001 | 2.0 | 1GB | 512MB | ⏳ To Update |
| **Saleor API** | 8000 | 1.5 | 1GB | 512MB | ⏳ To Update |
| **Gaming Backend** | TBD | 1.0 | 768MB | 384MB | ⏳ To Deploy |

### Database Services (KVM4: 72.60.219.244)

| Service | Port | CPU Limit | Memory Limit | Memory Reserve | Status |
|---------|------|-----------|--------------|----------------|--------|
| **PostgreSQL** | 5432 | 2.0 | 2GB | 1GB | ⏳ To Update |
| **Redis** | 6379 | 0.5 | 512MB | 256MB | ⏳ To Update |

---

## ⚙️ HOW TO SET RESOURCE LIMITS IN DOKPLOY

### Via Dokploy UI:

1. **Navigate to Service**
   ```
   Projects → BizOSaaS Platform → Select Service
   ```

2. **Go to Advanced Settings**
   ```
   Service Details → Advanced → Resources
   ```

3. **Set Resource Limits**
   ```
   CPU Limit:           [value] (e.g., 1.0)
   Memory Limit:        [value]MB (e.g., 512)
   Memory Reservation:  [value]MB (e.g., 256)
   ```

4. **Set Replica & Restart Policy**
   ```
   Replicas:            1
   Restart Policy:      on-failure (or always for critical services)
   ```

5. **Save and Redeploy**
   ```
   Click "Update" → Redeploy Service
   ```

---

### Via Docker Compose (if not using Dokploy UI):

```yaml
services:
  thrillring-gaming:
    image: ghcr.io/bizoholic-digital/bizosaas-thrillring-gaming:latest
    deploy:
      replicas: 1
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
```

---

## 🔍 MONITORING RESOURCE USAGE

### Check Current Resource Usage:

```bash
# SSH to KVM4
ssh root@72.60.219.244

# View service resource usage
docker stats

# View specific service
docker stats <container-id>

# View all frontend services
docker stats $(docker ps --filter name=frontend --format "{{.ID}}")
```

### Identify Services Needing Adjustment:

```bash
# Services using > 80% of memory limit - increase limit
# Services using < 20% of memory limit - decrease limit
# Services frequently restarting - likely OOM (out of memory)
```

---

## 📈 SCALING GUIDELINES

### When to Increase Limits:

1. **Memory**:
   - Service frequently OOM killed
   - Memory usage consistently > 80% of limit
   - Slow performance during peak hours

2. **CPU**:
   - CPU usage consistently > 80%
   - Request timeouts increasing
   - Response times degrading

### When to Add Replicas (Horizontal Scaling):

1. **Traffic Patterns**:
   - Consistent high traffic (> 1000 concurrent users)
   - Peak hour load exceeds single replica capacity
   - Geographic distribution benefits (latency reduction)

2. **High Availability**:
   - Critical services (Brain Gateway)
   - 24/7 uptime requirement
   - Zero-downtime deployments needed

### When to Decrease Limits:

1. **Over-Provisioned**:
   - Memory usage consistently < 30% of limit
   - CPU usage consistently < 30%
   - No performance issues reported

2. **Cost Optimization**:
   - Server resource constraints
   - Reduce unused capacity

---

## 🚨 SPECIAL CONSIDERATIONS

### Brain Gateway (CRITICAL):

```yaml
# Recommended Configuration
CPU Limit:              2.0
Memory Limit:           1GB
Memory Reservation:     512MB
Replicas:               2 (for High Availability)
Restart Policy:         always
```

**Why 2 Replicas:**
- Central point of failure
- ALL frontends depend on it
- Load balancing for high concurrency
- Zero-downtime deployments

### Stateful Services (Databases):

```yaml
# PostgreSQL / MongoDB
Replicas:               1 (NEVER scale without replication setup)
Restart Policy:         always (critical data service)
Volumes:                MUST persist data
```

**Critical:**
- **DO NOT** scale database replicas without proper replication configuration
- Always use persistent volumes
- Always set restart policy to "always"

### Socket.IO Services (ThrillRing):

```yaml
# If using Socket.IO
Session Affinity:       YES (sticky sessions)
Load Balancer:          Configure session stickiness
Replicas:               Use with caution (state management)
```

**Note:** Socket.IO requires sticky sessions for multi-replica deployments

---

## ✅ IMPLEMENTATION PRIORITY

### Phase 1: Critical Services (Do First)
1. ✅ Brain Gateway (2.0 CPU, 1GB memory, 2 replicas)
2. ✅ PostgreSQL (2.0 CPU, 2GB memory, 1 replica)
3. ✅ Redis (0.5 CPU, 512MB memory, 1 replica)

### Phase 2: Frontend Services
1. ✅ CoreLdove Storefront (1.0 CPU, 512MB memory)
2. ✅ ThrillRing Gaming (1.0 CPU, 512MB memory)
3. ✅ Client Portal (1.0 CPU, 512MB memory)
4. ✅ Bizoholic Frontend (0.5 CPU, 256MB memory)
5. ✅ Business Directory (0.5 CPU, 256MB memory)

### Phase 3: Backend Services
1. ✅ Saleor API (1.5 CPU, 1GB memory)
2. ✅ Gaming Backend (1.0 CPU, 768MB memory)
3. ✅ Other microservices as deployed

---

## 📝 SUMMARY

**Recommendation:** ✅ **YES - Set resource limits for ALL services**

**Benefits:**
- Prevents one service from consuming all resources
- Predictable, stable performance
- Better cost control and monitoring
- Docker Swarm best practices

**Quick Reference:**
- **Light Frontends**: 0.5 CPU, 256MB memory
- **Medium Frontends**: 1.0 CPU, 512MB memory
- **Heavy Frontends**: 1.0-1.5 CPU, 512-768MB memory
- **Backend Services**: 1.0-1.5 CPU, 768MB-1GB memory
- **Brain Gateway**: 2.0 CPU, 1GB memory, **2 replicas**
- **PostgreSQL**: 2.0 CPU, 2GB memory, 1 replica
- **Redis**: 0.5 CPU, 512MB memory, 1 replica

---

**Next Step:** Update resource limits for all existing services via Dokploy UI!
