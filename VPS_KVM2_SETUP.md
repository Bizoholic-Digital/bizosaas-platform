# Deploying to KVM2 VPS (Hosting)

We will deploy the BizOSaaS platform to your existing **KVM2** server (`194.238.16.237`).

## 📋 Server Details
- **IP**: `194.238.16.237`
- **User**: `root`
- **Known Password**: `&k3civYG5Q6YPb` (from reference logs)

## 🚀 How to Deploy

I have created an automated script `deploy-to-kvm2.sh` that handles everything.

### Option 1: Run from Local Terminal (Recommended)
If you have SSH access to KVM2 configured (or can enter the password), simply run:

```bash
chmod +x deploy-to-kvm2.sh
./deploy-to-kvm2.sh
```

**What this script does:**
1.  Connects to `194.238.16.237`.
2.  Installs Docker (if missing).
3.  Clones the latest code from GitHub (`staging` branch).
4.  Sets up the environment.
5.  Runs the startup script to launch all Docker containers.
6.  Outputs the URLs for your deployed services.

### Option 2: Manual Deployment (Failed Script/No SSH from here)
If you cannot run the script locally, SSH into the server yourself and run these commands:

```bash
# 1. SSH into the server
ssh root@194.238.16.237
# (Enter password: &k3civYG5Q6YPb)

# 2. Update System
apt-get update && apt-get upgrade -y
command -v docker >/dev/null 2>&1 || curl -fsSL https://get.docker.com | sh
apt-get install -y docker-compose-plugin

# 3. Clone Repository
cd /root
git clone -b staging https://github.com/Bizoholic-Digital/bizosaas-platform.git
cd bizosaas-platform

# 4. Configure .env
cp .env.example .env
nano .env  # (Optional: Edit secrets if needed)

# 5. Start Services
chmod +x scripts/start-bizosaas-core-full.sh
./scripts/start-bizosaas-core-full.sh --wait
```

## 🔍 Accessing Your Deployment
Once complete, your services will be available at:

- **Client Portal**: http://194.238.16.237:3003
- **Brain Gateway**: http://194.238.16.237:8000
- **Auth Service**: http://194.238.16.237:8009
- **Authentik SSO**: http://194.238.16.237:9000
- **Portainer**: http://194.238.16.237:9001
