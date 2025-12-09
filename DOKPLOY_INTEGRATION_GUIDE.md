# Deploying to KVM2 VPS (Existing Dokploy)

Since Dokploy is already running on port 3000 (`http://194.238.16.237:3000`), we should **continue using Dokploy** rather than switching to Coolify. Dokploy is stable, lightweight, and you already have it configured.

However, we need to adapt our deployment to run *alongside* Dokploy without conflicts.

## ⚠️ Important: Port Conflicts
The BizOSaaS platform uses ports that might conflict with a standard Dokploy setup.
- **Client Portal**: 3003
- **Brain API**: 8000
- **Authentik**: 9000
- **Portainer**: 9001 (We will SKIP deploying Portainer since Dokploy manages containers)

## 📋 Steps to Deploy via Dokploy

### 1. Login to Dokploy
- **URL**: `http://194.238.16.237:3000`
- **Username**: (Your existing admin email)
- **Password**: (Your existing password)

### 2. Create Project
1.  Click **"Projects"** -> **"Create Project"**.
2.  Name: `BizOSaaS`

### 3. Deploy via "Compose" (Recommended)
This acts just like `docker-compose up` but managed by Dokploy.

1.  Click on your `BizOSaaS` project.
2.  Select **"Compose"**.
3.  Click **"Create Compose"**.
    *   **Name**: `bizosaas-stack`
    *   **Description**: `Full BizOSaaS Platform Stack`
4.  In the **"Configuration"** tab -> **"Docker Compose"** editor:
    *   Paste the content of your `bizosaas-brain-core/docker-compose.yml`.
    *   **CRITICAL CHANGE**: Remove the `portainer` service from the YAML before pasting. You typically don't need Portainer if you have Dokploy.
    *   **CRITICAL CHANGE**: Ensure volume paths are relative or named volumes (Dokploy handles this well).

5.  In the **"Environment"** tab:
    *   Add all your secrets from `.env`.
    *   `POSTGRES_PASSWORD=...`
    *   `JWT_SECRET=...`
    *   `VAULT_TOKEN=...`

6.  Click **"Deploy"**.

### 4. Alternative: Manual Deployment (Side-by-Side)
If you prefer not to use the Dokploy UI for this specific stack, you can still SSH in and run it manually as we planned. It will run happily alongside Dokploy as long as ports don't clash.

**Run the script I created:**
```bash
./deploy-to-kvm2.sh
```

*Note: The script I provided basically does a "manual" Docker deployment. Dokploy will still be able to "see" these containers in its "Docker" tab, but it won't manage their lifecycles or deployments automatically unless you import them.*

## 💡 Recommendation
**Stick with the Manual Script (`deploy-to-kvm2.sh`) for now.**

Why?
1.  It's faster to get running right now.
2.  Dokploy's "Compose" feature is great, but migrating our complex `docker-compose.yml` with all its build contexts (`build: ./brain-gateway`) requires the source code to be on the server anyway.
3.  Our script handles the git clone + build process perfectly.

**Plan:**
1.  Run `./deploy-to-kvm2.sh`.
2.  Once running, you can log into Dokploy (`http://194.238.16.237:3000`) and go to the **"Docker"** tab. You will see all your `bizosaas-*` containers running there! You can view logs and restart them from Dokploy's UI. This gives you the best of both worlds.
