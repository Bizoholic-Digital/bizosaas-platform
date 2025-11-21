# Dokploy Resource Limits - 4 vCPU Configuration
**Date:** November 3, 2025
**Server:** KVM4 (72.60.219.244) - 4 vCPU, 8GB RAM
**Strategy:** Memory limits ONLY (no CPU limits)

---

## 🎯 CRITICAL DECISION: Memory Only, No CPU Limits

### Why NO CPU Limits for 4 vCPU System:

With only **4 vCPUs total**, setting CPU limits would cause severe performance issues:

1. ❌ **1 CPU per frontend** = 5 frontends would need 5 vCPUs (we only have 4!)
2. ❌ **Backend services** also need CPU (Brain Gateway, Saleor, databases)
3. ❌ **Infrastructure** needs CPU (Traefik, Dokploy, system processes)
4. ✅ **Docker's default** = Fair share scheduling across ALL services

### Recommended Approach: **Memory Limits ONLY**

```yaml
Resources:
  CPU Limit:           NONE (let Docker schedule fairly)
  Memory Limit:        SET (prevent OOM killer)
  Memory Reservation:  SET (guarantee minimum)
```

---

## 📊 MEMORY ALLOCATION STRATEGY

### Total Available: 8GB RAM
```
8GB Total RAM
- 1GB System/OS reserved
= 7GB Available for services
```

### Allocation Plan:
```
Frontend Services:     2.5GB (5 services × 512MB each)
Backend Services:      2.5GB (Brain Gateway 1GB + Saleor 1GB + Gaming 512MB)
Databases:             1.5GB (PostgreSQL 1GB + Redis 512MB)
Infrastructure:        0.5GB (Traefik, Dokploy, monitoring)
-------------------------------------------
TOTAL:                 7GB
```

---

## 🎨 FRONTEND SERVICES - MEMORY ONLY

### All Next.js Frontends (Standard Configuration)

```yaml
Resources:
  Memory Limit:           512MB
  Memory Reservation:     256MB
  Replicas:               1
  Restart Policy:         on-failure
```

**Applies to:**
1. ✅ Bizoholic Frontend (port 3001)
2. ✅ Client Portal (port 3002)
3. ✅ Business Directory (port 3004)
4. ✅ CoreLdove Storefront (port 3005)
5. ✅ ThrillRing Gaming (port 3006)

**Total:** 5 × 512MB = 2.5GB

---

## 🧠 BACKEND SERVICES - MEMORY ONLY

### Brain Gateway (CRITICAL)

```yaml
Resources:
  Memory Limit:           1GB
  Memory Reservation:     512MB
  Replicas:               1 (consider 2 for HA later)
  Restart Policy:         always
```

**Why 1GB:**
- Central hub for ALL frontend requests
- CrewAI agent orchestration (memory intensive)
- Must handle high concurrency

---

### Saleor API

```yaml
Resources:
  Memory Limit:           1GB
  Memory Reservation:     512MB
  Replicas:               1
  Restart Policy:         on-failure
```

---

### Gaming Backend

```yaml
Resources:
  Memory Limit:           512MB
  Memory Reservation:     256MB
  Replicas:               1
  Restart Policy:         on-failure
```

**Total Backend:** 1GB + 1GB + 512MB = 2.5GB

---

## 🗄️ DATABASE SERVICES - MEMORY ONLY

### PostgreSQL

```yaml
Resources:
  Memory Limit:           1GB
  Memory Reservation:     512MB
  Replicas:               1 (NEVER scale without replication)
  Restart Policy:         always
```

---

### Redis

```yaml
Resources:
  Memory Limit:           512MB
  Memory Reservation:     256MB
  Replicas:               1
  Restart Policy:         always
```

**Total Databases:** 1GB + 512MB = 1.5GB

---

## ⚙️ DOKPLOY UI CONFIGURATION

### For ThrillRing Gaming (Example):

**Navigate to:** Projects → BizOSaaS Platform → ThrillRing Gaming → Advanced → Resources

```
❌ CPU Limit:                 LEAVE EMPTY (critical!)
✅ Memory Limit:               512
✅ Memory Reservation:         256
   Unit:                       MB
   Replicas:                   1
   Restart Policy:             on-failure
```

### For Brain Gateway:

```
❌ CPU Limit:                 LEAVE EMPTY (critical!)
✅ Memory Limit:               1024
✅ Memory Reservation:         512
   Unit:                       MB
   Replicas:                   1
   Restart Policy:             always
```

### For PostgreSQL:

```
❌ CPU Limit:                 LEAVE EMPTY (critical!)
✅ Memory Limit:               1024
✅ Memory Reservation:         512
   Unit:                       MB
   Replicas:                   1 (NEVER change!)
   Restart Policy:             always
```

---

## 📋 COMPLETE SERVICE RESOURCE TABLE

| Service | Type | Memory Limit | Memory Reserve | CPU Limit | Replicas |
|---------|------|--------------|----------------|-----------|----------|
| **Bizoholic Frontend** | Frontend | 512MB | 256MB | **NONE** | 1 |
| **Client Portal** | Frontend | 512MB | 256MB | **NONE** | 1 |
| **Business Directory** | Frontend | 512MB | 256MB | **NONE** | 1 |
| **CoreLdove Storefront** | Frontend | 512MB | 256MB | **NONE** | 1 |
| **ThrillRing Gaming** | Frontend | 512MB | 256MB | **NONE** | 1 |
| **Brain Gateway** | Backend | 1GB | 512MB | **NONE** | 1 |
| **Saleor API** | Backend | 1GB | 512MB | **NONE** | 1 |
| **Gaming Backend** | Backend | 512MB | 256MB | **NONE** | 1 |
| **PostgreSQL** | Database | 1GB | 512MB | **NONE** | 1 |
| **Redis** | Database | 512MB | 256MB | **NONE** | 1 |
| | | | | | |
| **TOTAL** | | **7GB** | **3.5GB** | **NONE** | 10 |

---

## 🚨 CRITICAL WARNINGS

### 1. NEVER Set CPU Limits on 4 vCPU System

❌ **Wrong:**
```yaml
CPU Limit: 1.0
```

✅ **Correct:**
```yaml
CPU Limit: [LEAVE EMPTY]
```

**Why:** Docker will fairly share 4 vCPUs across all services automatically. Setting limits will cause CPU starvation.

---

### 2. Memory Limits Are MANDATORY

Without memory limits:
- One service can consume all 8GB RAM
- OOM killer randomly kills services
- System becomes unstable

**Always set:**
- ✅ Memory Limit (hard limit)
- ✅ Memory Reservation (guaranteed minimum)

---

### 3. PostgreSQL Special Rules

```yaml
Replicas: 1 (NEVER increase without proper replication setup)
Restart Policy: always (data service must always restart)
Volumes: MUST be persistent
```

---

## 🔍 MONITORING & ADJUSTMENT

### Check Current Usage:

```bash
ssh root@72.60.219.244

# View real-time resource usage
docker stats

# View all services
docker service ls

# Check specific service
docker stats <container-id>
```

### When to Adjust Memory Limits:

**Increase if:**
- Service frequently OOM killed (check `docker logs`)
- Memory usage consistently > 90% of limit
- Performance degrading under load

**Decrease if:**
- Memory usage consistently < 30% of limit
- Need to free up memory for new services

---

## 📈 SCALING STRATEGY FOR 4 vCPU

### Option 1: Vertical Scaling (Recommended)
**Upgrade to 8 vCPU server:**
- Then can set CPU limits (0.5-1.0 per service)
- Better performance isolation
- Cost: ~$20-40/month more

### Option 2: Horizontal Scaling
**Keep 4 vCPU, add second server:**
- Split services across 2 servers
- Frontend on Server 1, Backend on Server 2
- Requires network configuration
- Cost: Similar to vertical scaling

### Option 3: Optimize Current (Free)
**Stay on 4 vCPU:**
- Use memory limits only (current plan)
- Monitor and adjust as needed
- Deploy services incrementally
- Cost: $0

---

## ✅ IMPLEMENTATION CHECKLIST

### Phase 1: Update Existing Services (Priority)

- [ ] **Bizoholic Frontend**: 512MB limit, 256MB reserve, NO CPU limit
- [ ] **Client Portal**: 512MB limit, 256MB reserve, NO CPU limit
- [ ] **Business Directory**: 512MB limit, 256MB reserve, NO CPU limit
- [ ] **CoreLdove Storefront**: 512MB limit, 256MB reserve, NO CPU limit

### Phase 2: Deploy New Services

- [ ] **ThrillRing Gaming**: 512MB limit, 256MB reserve, NO CPU limit
- [ ] **Analytics Dashboard**: 512MB limit, 256MB reserve, NO CPU limit (when ready)

### Phase 3: Backend Services

- [ ] **Brain Gateway**: 1GB limit, 512MB reserve, NO CPU limit
- [ ] **Saleor API**: 1GB limit, 512MB reserve, NO CPU limit
- [ ] **Gaming Backend**: 512MB limit, 256MB reserve, NO CPU limit (when deployed)

### Phase 4: Database Services

- [ ] **PostgreSQL**: 1GB limit, 512MB reserve, NO CPU limit
- [ ] **Redis**: 512MB limit, 256MB reserve, NO CPU limit

---

## 📝 QUICK REFERENCE

### For Each Service in Dokploy:

1. **Navigate:** Projects → Service → Advanced → Resources
2. **Set Memory:**
   - Memory Limit: 512 (or 1024 for backends/DB)
   - Memory Reservation: 256 (or 512 for backends/DB)
   - Unit: MB
3. **Leave Empty:** CPU Limit field
4. **Set Restart:** on-failure (or always for critical services)
5. **Click:** Update → Redeploy

---

## 🎯 SUMMARY

**For 4 vCPU System:**
- ❌ **NO CPU Limits** - Let Docker schedule fairly
- ✅ **YES Memory Limits** - Prevent OOM issues
- ✅ **Total Memory Budget:** 7GB across all services
- ✅ **Per Frontend:** 512MB limit, 256MB reserve
- ✅ **Per Backend:** 512MB-1GB limit, 256MB-512MB reserve
- ✅ **Per Database:** 512MB-1GB limit, 256MB-512MB reserve

**Next Step:** Apply memory-only limits to ALL services via Dokploy UI!
