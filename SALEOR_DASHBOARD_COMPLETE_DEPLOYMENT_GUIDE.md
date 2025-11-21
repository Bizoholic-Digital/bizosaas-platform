# Saleor Dashboard - Complete Deployment Guide
**Date:** November 3, 2025
**Server:** KVM4 (72.60.219.244)
**Architecture:** Official Saleor Dashboard (Pre-built) + Direct Saleor Core API Connection

---

## 🏗️ ARCHITECTURE DECISION

### API Connection: **DIRECT to Saleor Core (NOT via Brain Gateway)**

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                              │
│  https://stg.coreldove.com/dashboard/                       │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ 1. HTTPS Request
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              TRAEFIK (Reverse Proxy)                         │
│  - SSL Termination                                           │
│  - Path routing: /dashboard → saleor-dashboard:80           │
│  - Strip /dashboard prefix                                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ 2. HTTP to Container
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         SALEOR DASHBOARD CONTAINER (Port 9000)               │
│  Image: ghcr.io/saleor/saleor-dashboard:latest             │
│  Type: Static React SPA (served by Nginx)                   │
│  - Loads HTML/CSS/JS in browser                             │
│  - NO server-side API calls                                 │
│  - API_URL configured at build time                         │
└─────────────────────────────────────────────────────────────┘
                   │
                   │ 3. GraphQL Queries (FROM BROWSER)
                   │    NOT from container!
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         SALEOR CORE API (Port 8000)                          │
│  Container: backend-saleor-api                              │
│  Internal IP: 10.0.1.47                                      │
│  GraphQL Endpoint: http://10.0.1.47:8000/graphql/          │
│  - Authentication (JWT tokens)                              │
│  - Products, Orders, Customers CRUD                         │
│  - Permissions & Multi-user management                      │
└─────────────────────────────────────────────────────────────┘
                   │
                   │ 4. Database Queries
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              POSTGRESQL DATABASE                             │
│  Container: backend-saleor-db                               │
└─────────────────────────────────────────────────────────────┘
```

### **WHY DIRECT CONNECTION (Not Brain Gateway)?**

**1. Saleor Dashboard is Client-Side (Browser-Based)**
- Dashboard is a **React SPA** (Single Page Application)
- All GraphQL calls are made **directly from the user's browser**
- Dashboard container only serves static files (HTML/CSS/JS)
- No server-side API proxy layer

**2. API_URL Points to Public or Internal IP**
- Browser needs **direct network access** to Saleor Core
- Options:
  - **Internal IP** (10.0.1.47:8000) - If browser has VPN/direct access
  - **Public domain** (api.stg.coreldove.com) - For remote access
  - **CANNOT use** Brain Gateway because dashboard runs in browser, not container

**3. Brain Gateway is for Server-Side Apps**
- Brain Gateway proxies backend-to-backend communication
- Used by: CoreLdove Storefront, ThrillRing Gaming (Next.js API routes)
- NOT used by: Client-side SPAs like Saleor Dashboard

---

## 📁 DOKPLOY PROJECT STRUCTURE

### **WHERE TO CREATE THE SERVICE**

```
Dokploy UI
│
├── 📦 Projects
│   │
│   ├── 🏢 bizoholic (Business Directory, Client Portal)
│   │
│   ├── 🎮 thrillring (Gaming Platform - Standalone)
│   │
│   └── 🛒 coreldove (E-commerce Stack) ← ✅ **CREATE HERE**
│       │
│       ├── Backend Services
│       │   ├── backend-saleor-api (Saleor Core - GraphQL API)
│       │   ├── backend-saleor-db (PostgreSQL)
│       │   ├── backend-saleor-redis (Cache)
│       │   └── backend-saleor-worker (Celery)
│       │
│       └── Frontend Services
│           ├── frontend-coreldove-storefront (Customer-facing)
│           └── ✨ **frontend-saleor-dashboard** ← NEW SERVICE
```

**Reasoning:**
- Saleor Dashboard manages CoreLdove e-commerce
- Groups all Saleor services in one project
- Shared network access to backend services
- Logical domain structure (stg.coreldove.com/dashboard)

---

## 🚀 COMPLETE DOKPLOY CONFIGURATION

### **Step 1: Access Dokploy UI**

```bash
URL: https://automationhub-n8n-91feb0-194-238-16-237.traefik.me
Server: KVM4 (72.60.219.244)
```

### **Step 2: Navigate to CoreLdove Project**

1. Click **Projects** in sidebar
2. Select **`coreldove`** project
3. Click **"Add Service"** button

### **Step 3: Service Basic Configuration**

**Tab: General**

| Field | Value | Notes |
|-------|-------|-------|
| **Service Name** | `saleor-dashboard` | Lowercase, no spaces |
| **Service Type** | `Docker Image` | NOT "Docker Compose" or "Git" |
| **Description** | `Saleor Dashboard - CoreLdove E-commerce Admin` | Optional |

**Tab: Image**

| Field | Value | Notes |
|-------|-------|-------|
| **Image** | `ghcr.io/saleor/saleor-dashboard:latest` | Official Saleor image |
| **Registry** | `Public` | No authentication needed |
| **Image Pull Policy** | `Always` | Always pull latest version |

---

### **Step 4: Network Configuration**

**Tab: Network → Port Mapping**

Click **"Add Port"** and configure:

| Field | Value | Notes |
|-------|-------|-------|
| **Container Port** | `80` | Nginx inside container |
| **Host Port** | `9000` | External access port |
| **Protocol** | `TCP` | HTTP traffic |
| **Published** | ✅ Enabled | Make port accessible |

**IMPORTANT:** Do NOT use port 3002, 3004, or 3005 (already in use).

---

### **Step 5: Environment Variables**

**Tab: Environment**

Click **"Add Variable"** and configure:

| Variable Name | Value | Notes |
|---------------|-------|-------|
| `API_URL` | `http://10.0.1.47:8000/graphql/` | **CRITICAL: Must point to Saleor Core** |

**⚠️ CRITICAL NOTES:**

1. **API_URL Format:**
   ```
   http://10.0.1.47:8000/graphql/
   ├─ Protocol: http (NOT https) - Internal communication
   ├─ IP: 10.0.1.47 - Saleor Core internal IP
   ├─ Port: 8000 - Saleor Core API port
   └─ Path: /graphql/ - GraphQL endpoint (trailing slash required!)
   ```

2. **Finding Saleor Core IP:**
   ```bash
   docker inspect backend-saleor-api.1.XXX | grep IPAddress
   ```
   Result should be: `10.0.1.47` (already confirmed)

3. **Alternative for Remote Access:**
   If you need remote access (outside VPN), use:
   ```
   API_URL=https://api.stg.coreldove.com/graphql/
   ```
   Then configure Traefik to route `api.stg.coreldove.com` → `backend-saleor-api:8000`

---

### **Step 6: Traefik Routing (Domain Configuration)**

**Tab: Routing → Domain**

**Primary Configuration:**

| Field | Value | Notes |
|-------|-------|-------|
| **Enable Traefik** | ✅ Enabled | Required for HTTPS |
| **Domain** | `stg.coreldove.com` | CoreLdove staging domain |
| **Path Prefix** | `/dashboard` | Dashboard subdirectory |
| **Certificate Resolver** | `letsencrypt` | Auto SSL certificate |
| **Entry Points** | `websecure` | HTTPS (443) |

**Advanced Labels (Custom Traefik Configuration):**

Click **"Add Label"** for each:

```yaml
# 1. Enable Traefik
traefik.enable=true

# 2. Router configuration
traefik.http.routers.saleor-dashboard.rule=Host(`stg.coreldove.com`) && PathPrefix(`/dashboard`)
traefik.http.routers.saleor-dashboard.entrypoints=websecure
traefik.http.routers.saleor-dashboard.tls=true
traefik.http.routers.saleor-dashboard.tls.certresolver=letsencrypt

# 3. Service configuration (tell Traefik which port to use)
traefik.http.services.saleor-dashboard.loadbalancer.server.port=80

# 4. Strip prefix middleware (CRITICAL!)
traefik.http.middlewares.saleor-dashboard-stripprefix.stripprefix.prefixes=/dashboard
traefik.http.routers.saleor-dashboard.middlewares=saleor-dashboard-stripprefix
```

**Why Strip Prefix?**
- User visits: `https://stg.coreldove.com/dashboard/`
- Traefik forwards to container as: `http://container/` (NOT `/dashboard/`)
- Dashboard expects root path `/` for serving static files

---

### **Step 7: Resource Limits**

**Tab: Resources**

| Field | Value | Notes |
|-------|-------|-------|
| **CPU Limit** | `0.5` | Half a CPU core |
| **Memory Limit** | `512` (MB) | Static files = lightweight |
| **Memory Reservation** | `256` (MB) | Minimum guaranteed |

**Rationale:**
- Dashboard is just Nginx serving static React files
- No heavy processing or database connections
- Very lightweight compared to backend services

---

### **Step 8: Health Check**

**Tab: Health Check**

| Field | Value | Notes |
|-------|-------|-------|
| **Test Command** | `CMD curl -f http://localhost:80/ || exit 1` | Check if Nginx responds |
| **Interval** | `30s` | Check every 30 seconds |
| **Timeout** | `10s` | Fail if no response in 10s |
| **Retries** | `3` | Retry 3 times before marking unhealthy |
| **Start Period** | `40s` | Grace period after container start |

---

### **Step 9: Deploy**

1. Review all configurations
2. Click **"Deploy"** button (green, top-right)
3. Monitor deployment logs in **"Logs"** tab
4. Wait for status to show **"Running"** (green dot)

**Expected Deployment Time:** 1-2 minutes

---

## ✅ POST-DEPLOYMENT VERIFICATION

### **1. Check Container Status**

**Via Dokploy UI:**
- Navigate to `coreldove` project → `saleor-dashboard` service
- Status should show: 🟢 **Running**
- Check logs for any errors

**Via SSH:**
```bash
ssh root@72.60.219.244
docker ps | grep saleor-dashboard
```

Expected output:
```
CONTAINER ID   IMAGE                                     STATUS
abc123def456   ghcr.io/saleor/saleor-dashboard:latest   Up 2 minutes
```

---

### **2. Test Direct Container Access**

```bash
# From KVM4 server
curl -I http://localhost:9000/
```

**Expected Response:**
```
HTTP/1.1 200 OK
Server: nginx/1.25.x
Content-Type: text/html
```

---

### **3. Test Domain Access**

```bash
# From your local machine
curl -I https://stg.coreldove.com/dashboard/
```

**Expected Response:**
```
HTTP/2 200
server: nginx/1.25.x
content-type: text/html
```

**⚠️ Common Issues:**

| Error | Cause | Solution |
|-------|-------|----------|
| **502 Bad Gateway** | Container not running | Check Dokploy logs, restart service |
| **404 Not Found** | Strip prefix not working | Verify Traefik middleware labels |
| **SSL Certificate Error** | Let's Encrypt failed | Wait 2-3 minutes, certificate provisioning |

---

### **4. Test Dashboard Login (Web Browser)**

1. Open browser: `https://stg.coreldove.com/dashboard/`
2. Should see: **Saleor Dashboard Login Page**
3. Try logging in with Saleor admin credentials

**Default Saleor Admin Credentials** (if fresh install):
```
Email: admin@example.com
Password: admin
```

**⚠️ IMPORTANT:** Change default credentials immediately!

---

### **5. Test API Connection**

After logging in, dashboard should load:
- Products page
- Orders page
- Customers page

**If pages show "Cannot connect to API":**

1. **Check API_URL environment variable:**
   ```bash
   docker inspect saleor-dashboard | grep API_URL
   ```
   Should show: `API_URL=http://10.0.1.47:8000/graphql/`

2. **Test Saleor Core API directly:**
   ```bash
   curl http://10.0.1.47:8000/graphql/ \
     -H "Content-Type: application/json" \
     -d '{"query": "{ shop { name } }"}'
   ```
   Should return shop name, not error

3. **Check CORS settings in Saleor Core:**
   Saleor Core must allow `stg.coreldove.com` in ALLOWED_CLIENT_HOSTS

---

## 🔧 TROUBLESHOOTING

### **Issue 1: Dashboard Loads but Can't Login**

**Symptoms:** Login form appears, but clicking "Login" does nothing or shows error.

**Causes:**
1. Wrong API_URL
2. Saleor Core not running
3. CORS blocking requests

**Solutions:**

```bash
# 1. Verify Saleor Core is running
docker ps | grep backend-saleor-api

# 2. Check Saleor Core logs
docker logs backend-saleor-api.1.XXX --tail 50

# 3. Test GraphQL endpoint
curl -X POST http://10.0.1.47:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { queryType { name } } }"}'

# Should return: {"data":{"__schema":{"queryType":{"name":"Query"}}}}

# 4. Update Saleor Core CORS settings
docker exec -it backend-saleor-api.1.XXX sh
# Edit environment or restart with updated ALLOWED_CLIENT_HOSTS
```

---

### **Issue 2: Static Assets 404 (CSS/JS Not Loading)**

**Symptoms:** Dashboard HTML loads, but no styling. Browser console shows 404 for CSS/JS files.

**Causes:**
1. Strip prefix middleware not applied
2. Wrong base path in dashboard

**Solutions:**

```bash
# 1. Verify Traefik middleware is active
docker logs traefik 2>&1 | grep saleor-dashboard

# Should see: middleware "saleor-dashboard-stripprefix" applied

# 2. Test asset path directly
curl -I https://stg.coreldove.com/dashboard/static/css/main.css

# Should return 200, not 404

# 3. If still failing, check Nginx logs
docker logs saleor-dashboard 2>&1 | tail -50
```

---

### **Issue 3: Cannot Access from Remote Browser**

**Symptoms:** Works on server, fails from external browser.

**Causes:**
1. Firewall blocking port 443
2. DNS not pointing to KVM4
3. SSL certificate not provisioned

**Solutions:**

```bash
# 1. Check DNS
nslookup stg.coreldove.com
# Should resolve to: 72.60.219.244

# 2. Check firewall
sudo ufw status
# Port 443 should be ALLOW

# 3. Check Traefik certificate
docker exec traefik ls /letsencrypt/acme.json
# File should exist

# 4. Force certificate renewal (if needed)
docker restart traefik
```

---

## 🔐 AUTHENTICATION & USER MANAGEMENT

### **How Saleor Dashboard Authentication Works**

1. **User enters credentials** on dashboard login page
2. **Dashboard sends GraphQL mutation** to Saleor Core API:
   ```graphql
   mutation TokenCreate($email: String!, $password: String!) {
     tokenCreate(email: $email, password: $password) {
       token
       refreshToken
       errors { field message }
     }
   }
   ```
3. **Saleor Core validates** credentials against PostgreSQL
4. **Returns JWT tokens** if valid
5. **Dashboard stores tokens** in browser localStorage
6. **All subsequent requests** include JWT token in `Authorization` header

### **Creating Admin Users**

**Method 1: Via Django Admin (Recommended)**

```bash
# SSH into Saleor Core container
docker exec -it backend-saleor-api.1.XXX sh

# Create superuser
python manage.py createsuperuser

# Follow prompts:
Email: admin@coreldove.com
Password: [enter secure password]
Confirm password: [repeat password]

# Exit container
exit
```

**Method 2: Via GraphQL (Dashboard)**

If you already have admin access:
1. Login to dashboard
2. Navigate to **Settings → Staff Members**
3. Click **"Add Staff Member"**
4. Fill in details:
   - Email: `staff@coreldove.com`
   - First Name: `John`
   - Last Name: `Doe`
   - Permissions: Select roles
5. User receives email with setup link

**Method 3: Via Saleor CLI**

```bash
# Install Saleor CLI
npm install -g @saleor/cli

# Create user
saleor user create \
  --email admin@coreldove.com \
  --password SecurePass123! \
  --is-staff \
  --is-superuser
```

---

### **User Roles & Permissions**

Saleor has built-in permission system:

| Role | Permissions | Use Case |
|------|-------------|----------|
| **Superuser** | Full access | Platform administrator |
| **Staff** | Limited access | Store managers |
| **Customer** | No dashboard access | End customers (storefront only) |

**Configuring Permissions:**
1. Dashboard → **Settings → Permission Groups**
2. Create custom groups (e.g., "Product Managers", "Order Processors")
3. Assign granular permissions:
   - Manage products
   - Process orders
   - View customers
   - Manage settings

---

## 🔄 FUTURE: BRAIN GATEWAY INTEGRATION (OPTIONAL)

Currently, dashboard connects **directly** to Saleor Core. If you want to route through Brain Gateway later:

### **Why Use Brain Gateway?**

1. **Centralized logging** - All API calls logged in one place
2. **Rate limiting** - Protect Saleor API from abuse
3. **Analytics** - Track dashboard usage patterns
4. **Multi-tenancy** - Support multiple Saleor instances

### **How to Implement**

**Step 1: Update Brain Gateway (FastAPI)**

```python
# /app/api/routes/saleor.py

@router.post("/saleor/graphql")
async def proxy_saleor_graphql(request: Request):
    """
    Proxy GraphQL requests to Saleor Core
    """
    body = await request.json()

    # Forward to Saleor Core
    response = requests.post(
        "http://backend-saleor-api:8000/graphql/",
        json=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": request.headers.get("Authorization", "")
        }
    )

    return response.json()
```

**Step 2: Update Dashboard API_URL**

```bash
# Change from:
API_URL=http://10.0.1.47:8000/graphql/

# To:
API_URL=https://api.stg.coreldove.com/saleor/graphql/
```

**Step 3: Configure Traefik**

Route `api.stg.coreldove.com` → Brain Gateway → Saleor Core

**⚠️ NOTE:** This is **optional** and adds complexity. Only implement if you need centralized management.

---

## 📊 MONITORING & MAINTENANCE

### **Key Metrics to Monitor**

1. **Container Health**
   ```bash
   docker ps --filter name=saleor-dashboard
   ```

2. **Resource Usage**
   ```bash
   docker stats saleor-dashboard --no-stream
   ```

3. **Response Times**
   - Dashboard load time: < 2 seconds
   - GraphQL queries: < 500ms

4. **Error Rates**
   - Check Dokploy logs for 5xx errors
   - Monitor Saleor Core API errors

### **Regular Maintenance Tasks**

| Task | Frequency | Command |
|------|-----------|---------|
| **Update Dashboard Image** | Monthly | Re-deploy with `:latest` tag |
| **Check Logs** | Daily | View in Dokploy UI |
| **Monitor Disk Space** | Weekly | `df -h` on KVM4 |
| **Review User Access** | Monthly | Audit staff members in dashboard |
| **SSL Certificate Renewal** | Auto (90 days) | Traefik handles automatically |

---

## 🎯 SUCCESS CRITERIA CHECKLIST

- [ ] Container status: **Running** in Dokploy
- [ ] `https://stg.coreldove.com/dashboard/` returns **200 OK**
- [ ] Dashboard login page loads with **styling**
- [ ] Can login with **Saleor admin credentials**
- [ ] Products page loads **product list** from API
- [ ] Orders page loads **order list** from API
- [ ] No **CORS errors** in browser console
- [ ] Resource usage: **< 512MB RAM, < 0.5 CPU**
- [ ] Response time: **< 2 seconds** for page load

---

## 📝 SUMMARY

**Deployment Type:** Official Saleor Dashboard (Pre-built Docker Image)

**Project Location:** Dokploy → CoreLdove Project → Frontend Services

**Architecture:** Direct connection to Saleor Core API (No Brain Gateway)

**Authentication:** Saleor's built-in JWT-based auth (Not FastAPI Auth)

**Domain:** `https://stg.coreldove.com/dashboard/`

**Key Configuration:**
- Image: `ghcr.io/saleor/saleor-dashboard:latest`
- Port: 9000:80
- API_URL: `http://10.0.1.47:8000/graphql/`
- Traefik: Strip `/dashboard` prefix

**Next Steps:**
1. Deploy via Dokploy UI (1-2 hours)
2. Verify login and API connection
3. Create admin users
4. Update roadmap documentation

**Benefits:**
- Zero maintenance (official image)
- Automatic security updates
- Complete feature set
- Production-ready
- Follows containerized microservices architecture

---

**Deployment Date:** November 3, 2025
**Deployed By:** BizOSaaS Platform Team
**Status:** ✅ Ready for Deployment
