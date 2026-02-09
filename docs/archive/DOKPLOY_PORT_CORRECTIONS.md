# Dokploy Port Corrections
## Fix Port Mappings for All Frontend Services
**Date:** November 17, 2025

---

## ❌ Current Issues

Your port mappings are **mixed up and incorrect**:

| Service | Current Published | Current Target | Status |
|---------|------------------|----------------|---------|
| bizoholic-frontend | 3001 | 3001 | ✅ CORRECT |
| coreldove-frontend | **3005** ❌ | 3002 | ❌ WRONG Published Port |
| client-portal | **3002** ❌ | **3001** ❌ | ❌ BOTH WRONG |

**Problems:**
1. coreldove-frontend publishing on 3005 (should be 3002)
2. client-portal publishing on 3002 (should be 3003) and targeting 3001 (should be 3003)
3. Port conflicts and mismatches

---

## ✅ CORRECT Port Configuration

**Rule:** Published Port = Target Port = PORT env variable

Each service should have **matching ports** across all three settings:

| Service | Published Port | Target Port | PORT env var | Status |
|---------|---------------|-------------|--------------|--------|
| bizoholic-frontend | 3001 | 3001 | 3001 | ✅ Already correct |
| coreldove-frontend | 3002 | 3002 | 3002 | ❌ Fix needed |
| client-portal | 3003 | 3003 | 3003 | ❌ Fix needed |
| business-directory | 3004 | 3004 | 3004 | ❓ Check current |
| admin-dashboard | 3005 | 3005 | 3005 | ❓ Check current |
| thrillring-gaming | 3006 | 3006 | 3006 | ❓ Check current |

---

## 🔧 Corrections Needed

### 1. bizoholic-frontend ✅
**Current:** Published 3001 → Target 3001
**Action:** ✅ **NO CHANGE NEEDED** - Already correct!

```
Published Port: 3001
Published Port Mode: INGRESS
Target Port: 3001
Protocol: TCP
```

---

### 2. coreldove-frontend ❌ FIX REQUIRED
**Current:** Published **3005** → Target 3002
**Problem:** Published port is wrong (3005 should be 3002)

**CHANGE TO:**
```
Published Port: 3002  ← CHANGE FROM 3005
Published Port Mode: INGRESS
Target Port: 3002  ← Already correct
Protocol: TCP
```

**Why?**
- coreldove-frontend should be on port 3002
- Port 3005 is reserved for admin-dashboard
- Environment variable `PORT=3002` expects this port

---

### 3. client-portal ❌ FIX REQUIRED
**Current:** Published **3002** → Target **3001**
**Problem:** Both ports are wrong!

**CHANGE TO:**
```
Published Port: 3003  ← CHANGE FROM 3002
Published Port Mode: INGRESS
Target Port: 3003  ← CHANGE FROM 3001
Protocol: TCP
```

**Why?**
- client-portal should be on port 3003
- Port 3001 is for bizoholic-frontend
- Port 3002 is for coreldove-frontend
- Environment variable `PORT=3003` expects this port

---

### 4. business-directory
**Should be:**
```
Published Port: 3004
Published Port Mode: INGRESS
Target Port: 3004
Protocol: TCP
```

**Check your current settings and adjust if different**

---

### 5. admin-dashboard
**Should be:**
```
Published Port: 3005
Published Port Mode: INGRESS
Target Port: 3005
Protocol: TCP
```

**Check your current settings and adjust if different**

---

### 6. thrillring-gaming
**Should be:**
```
Published Port: 3006
Published Port Mode: INGRESS
Target Port: 3006
Protocol: TCP
```

**Check your current settings and adjust if different**

---

## 📋 Complete Port Allocation Table

| Service | URL | Published | Target | PORT Env |
|---------|-----|-----------|--------|----------|
| bizoholic-frontend | stg.bizoholic.com | 3001 | 3001 | 3001 |
| coreldove-frontend | stg.coreldove.com | 3002 | 3002 | 3002 |
| client-portal | stg.bizoholic.com/portal | 3003 | 3003 | 3003 |
| business-directory | stg.bizoholic.com/directory | 3004 | 3004 | 3004 |
| admin-dashboard | admin.bizoholic.com | 3005 | 3005 | 3005 |
| thrillring-gaming | stg.thrillring.com | 3006 | 3006 | 3006 |
| analytics-dashboard | analytics.bizoholic.com | 3007 | 3007 | 3007 |

---

## 🚨 Why This Matters

### Port Mismatches Cause:
1. ❌ **Connection failures** - Container listening on wrong port
2. ❌ **502 Bad Gateway errors** - Traefik can't reach the service
3. ❌ **Service conflicts** - Multiple services trying to use same port
4. ❌ **Health check failures** - Health checks on wrong port

### Example Problem:
```
client-portal:
  - Environment says: PORT=3003 (app listens on 3003)
  - Dokploy publishes: 3002 (Traefik routes to 3002)
  - Dokploy targets: 3001 (tries to reach container on 3001)

Result: 502 Bad Gateway (nothing listening on 3001!)
```

---

## 🔧 How to Fix in Dokploy

### For Each Service:

1. **Go to Dokploy Dashboard:**
   ```
   https://dk4.bizoholic.com/dashboard
   ```

2. **Navigate to the service** (e.g., "coreldove-frontend")

3. **Go to "Ports" or "Network" section**

4. **Update the port mapping:**
   - Click "Edit" or similar option
   - Change Published Port
   - Change Target Port
   - Both should match the service's designated port

5. **Save changes**

6. **Redeploy the service** to apply changes

---

## ✅ Verification Steps

After fixing each service's ports:

### 1. Check Container Status
```bash
# The container should be listening on the correct port
docker ps | grep <service-name>
```

### 2. Check Service Logs
```bash
# Should show "Listening on port XXXX" matching your config
docker logs <container-id>
```

### 3. Test Locally (if possible)
```bash
# Should get a response
curl http://localhost:3001  # bizoholic-frontend
curl http://localhost:3002  # coreldove-frontend
curl http://localhost:3003  # client-portal
# etc.
```

### 4. Check Public URL
```bash
# Should load without 502 errors
curl https://stg.bizoholic.com
curl https://stg.coreldove.com
curl https://stg.bizoholic.com/portal
```

---

## 📊 Port Assignment Logic

**Why these specific ports?**

```
3001 - bizoholic-frontend    (main site, first frontend)
3002 - coreldove-frontend    (e-commerce, second frontend)
3003 - client-portal         (client dashboard)
3004 - business-directory    (directory listing)
3005 - admin-dashboard       (admin panel)
3006 - thrillring-gaming     (gaming platform)
3007 - analytics-dashboard   (analytics/BI)
```

**Pattern:**
- Start at 3001
- Increment by 1 for each frontend
- No gaps, no conflicts
- Easy to remember and debug

---

## 🎯 Quick Fix Summary

### Immediate Actions Required:

1. **coreldove-frontend:**
   - Change Published Port: 3005 → **3002**
   - Keep Target Port: 3002

2. **client-portal:**
   - Change Published Port: 3002 → **3003**
   - Change Target Port: 3001 → **3003**

3. **Verify other services have correct ports:**
   - business-directory: 3004/3004
   - admin-dashboard: 3005/3005
   - thrillring-gaming: 3006/3006

---

## ⚠️ Important Notes

### After Changing Ports:

1. **Redeploy the service** - Port changes require restart
2. **Check health status** - Ensure service comes up healthy
3. **Test the URL** - Verify no 502 errors
4. **Check logs** - Look for "listening on port XXXX"

### Common Pitfalls:

- ❌ Changing environment PORT but not Dokploy ports
- ❌ Publishing correct port but wrong target port
- ❌ Using port already in use by another service
- ❌ Forgetting to redeploy after changing ports

### Best Practice:

**Triple consistency:**
```bash
# All three must match:
1. Environment Variable:  PORT=3003
2. Dokploy Published:     3003
3. Dokploy Target:        3003
```

---

## 🔍 Debugging Port Issues

If you get 502 errors after fixing:

1. **Check container logs:**
   ```bash
   docker service logs <service-name>
   ```

2. **Verify port binding:**
   ```bash
   docker service ps <service-name>
   netstat -tulpn | grep 300X
   ```

3. **Check Traefik routing:**
   - Verify Traefik labels are correct
   - Check Traefik dashboard for routes

4. **Test direct container access:**
   ```bash
   # From within Docker network
   curl http://<service-name>:300X
   ```

---

## ✅ Final Checklist

After applying all port corrections:

- [ ] bizoholic-frontend: 3001 → 3001 ✅
- [ ] coreldove-frontend: 3002 → 3002 (fixed from 3005)
- [ ] client-portal: 3003 → 3003 (fixed from 3002/3001)
- [ ] business-directory: 3004 → 3004
- [ ] admin-dashboard: 3005 → 3005
- [ ] thrillring-gaming: 3006 → 3006
- [ ] All services redeployed
- [ ] All services showing healthy status
- [ ] All URLs accessible without 502 errors
- [ ] All services routing through Brain Gateway

---

**Status:** 🔧 Port Corrections Required
**Priority:** 🔴 HIGH - Required for proper service access
**Impact:** Fixes 502 errors and service connectivity issues