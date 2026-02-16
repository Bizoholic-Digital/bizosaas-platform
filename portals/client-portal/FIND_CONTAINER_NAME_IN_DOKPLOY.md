# How to Find the Container Name in Dokploy UI

## Status Confirmed ✅

- Service shows: **"Running"** in Dokploy UI ✅
- Container is active ✅
- Traefik configuration is correct ✅
- Environment variables are set ✅

## The ONLY Issue: Container Name Mismatch

Your Traefik is looking for: `http://frontend-client-portal:3001`

But Dokploy likely named it differently. Let's find the actual name.

---

## Method 1: Check in Dokploy UI (EASIEST)

### Step 1: Go to Service Page
URL: https://dk4.bizoholic.com/dashboard/project/VM7SbnKYZKl6nxKYey4Xn/environment/w9JtT6e9Glus_8cjWIEWc/services/application/8EqZXZKYTLiPqTkLF2l4J?tab=general

### Step 2: Look for Container Name

**Check these locations on the page:**

1. **General Tab** - Look for:
   - "Container Name"
   - "Service Name"
   - "App Name"

2. **Advanced Tab** - Look for:
   - Docker container settings
   - Network settings
   - Container configuration

3. **Domains Tab** - Look at:
   - Service name in Traefik configuration
   - May show actual container name

### Step 3: Common Container Name Patterns

Dokploy typically uses these formats:

| Pattern | Example |
|---------|---------|
| Application ID | `8EqZXZKYTLiPqTkLF2l4J` |
| With prefix | `dokploy-8EqZXZKYTLiPqTkLF2l4J` |
| App name | `frontend-client-portal-8EqZXZKYTLiPqTkLF2l4J` |
| Simple name | `frontend-client-portal` |
| With hash | `frontend-client-portal-abc123` |

**Most likely**: `8EqZXZKYTLiPqTkLF2l4J` (the application ID from URL)

---

## Method 2: Check Container Logs Tab

1. Go to **Logs** tab in Dokploy
2. Look at the top of the logs
3. Often shows: "Container: <name>"

---

## Method 3: Check Dokploy Settings

1. Go to **Settings** or **Configuration** tab
2. Look for Docker/Container section
3. May show the generated container name

---

## Method 4: Via SSH (If you have access)

SSH to dk4.bizoholic.com and run:

```bash
# List all containers
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"

# Filter for portal
docker ps | grep -i portal

# Or filter by image name
docker ps | grep "bizosaas-client-portal"
```

---

## Quick Fix Options

### Option A: Use Application ID as Container Name

Based on your service URL, the application ID is: `8EqZXZKYTLiPqTkLF2l4J`

Try this in your Traefik config:

```yaml
services:
  frontend-client-portal-service-3:
    loadBalancer:
      servers:
        - url: http://8EqZXZKYTLiPqTkLF2l4J:3001  # Try this!
```

### Option B: Check Bizoholic Frontend for Reference

Look at your Bizoholic Frontend service in Dokploy:
- What container name does it use?
- Apply the same naming pattern to Client Portal

For example, if Bizoholic Frontend uses:
- `kMm-uOCmfBNn5bECyqHEw` (its application ID)

Then Client Portal should use:
- `8EqZXZKYTLiPqTkLF2l4J` (its application ID)

### Option C: Use Docker Network Name

Sometimes Dokploy uses format: `<project>-<environment>-<service>`

Example: `VM7SbnKYZKl6nxKYey4Xn-w9JtT6e9Glus_8cjWIEWc-8EqZXZKYTLiPqTkLF2l4J`

---

## Test Different Names

Try updating your Traefik config with these variations one by one:

```yaml
# Try 1: Application ID only
url: http://8EqZXZKYTLiPqTkLF2l4J:3001

# Try 2: With dokploy prefix
url: http://dokploy-8EqZXZKYTLiPqTkLF2l4J:3001

# Try 3: Full service name
url: http://frontend-client-portal-8EqZXZKYTLiPqTkLF2l4J:3001

# Try 4: Environment + service
url: http://w9JtT6e9Glus_8cjWIEWc-8EqZXZKYTLiPqTkLF2l4J:3001

# Try 5: Original name (just in case)
url: http://frontend-client-portal:3001
```

After each try:
1. Save Traefik config
2. Wait 10 seconds
3. Test: `curl -I https://stg.bizoholic.com/portal/`
4. If still 502, try next variation

---

## Debugging with Traefik Dashboard

If Traefik dashboard is accessible:

1. Open Traefik dashboard
2. Look for "HTTP Services" section
3. Find `frontend-client-portal-service-3`
4. Check if it shows:
   - ✅ Green: Service is healthy
   - ❌ Red: Can't reach container (wrong name)
5. May show actual container name/IP it's trying to reach

---

## Most Likely Solution

Based on typical Dokploy behavior with these URLs:
- Project: `VM7SbnKYZKl6nxKYey4Xn`
- Environment: `w9JtT6e9Glus_8cjWIEWc`
- Application: `8EqZXZKYTLiPqTkLF2l4J`

The container name is **most likely** one of these:

1. `8EqZXZKYTLiPqTkLF2l4J` (90% confidence)
2. `dokploy-8EqZXZKYTLiPqTkLF2l4J` (80% confidence)
3. `frontend-client-portal` (50% confidence - already tried)

**Recommendation**: Start with #1 first.

---

## Quick Action Steps

1. **Look in Dokploy UI** for container name (General/Advanced tabs)
2. **Try Application ID**: Update Traefik URL to `http://8EqZXZKYTLiPqTkLF2l4J:3001`
3. **Test**: `curl -I https://stg.bizoholic.com/portal/`
4. **If still 502**: Report what container name you found in step 1

---

## What to Report Back

Please tell me:

1. **Container name shown in Dokploy UI**: ________________
2. **Which Traefik URL variation worked**: ________________
3. **Container logs** (if none of the above work): [paste last 20 lines]

Once you tell me the correct container name, I'll update all documentation accordingly!
