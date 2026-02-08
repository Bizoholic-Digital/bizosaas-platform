# BizOSaaS Platform - Development Setup Guide

## 🚀 Quick Start

1.  **Open in VS Code**: Open this folder in VS Code.
2.  **Reopen in Container**: When prompted, click "Reopen in Container".
3.  **Start Services**:
    ```bash
    ./scripts/dev-start.sh minimal
    ```

---

## 🛠️ Setup & Optimization

### 1. Optimize Storage (Already Done ✅)
Since your WSL2 VM is located at `D:\vm`, your Docker data is **already on the HDD**.
- **Do NOT** run the storage optimization script.
- **Do NOT** move `/var/lib/docker` to `/mnt/d/...` (this causes severe performance issues).

Your setup is already optimized for storage!

### 2. Use Portainer (Recommended)
Save ~500MB RAM by using Portainer.

```bash
./scripts/setup-portainer.sh
```
Access at: http://localhost:9000

---

## 💻 Development Workflow

### Starting Services
Use profiles to save RAM (16GB limit).

| Profile | Description | RAM Usage | Command |
|---------|-------------|-----------|---------|
| `minimal` | DB, Redis, Vault only | ~1.5GB | `./scripts/dev-start.sh minimal` |
| `backend` | Infra + Brain + Auth | ~4GB | `./scripts/dev-start.sh backend` |
| `frontend` | Infra + Frontend | ~3GB | `./scripts/dev-start.sh frontend` |
| `full` | All Services | ~8GB+ | `./scripts/dev-start.sh full` |

### Switching Brands (Smart Switching)
Switch between brands without restarting shared infrastructure. This saves time and resources.

```bash
./scripts/switch-brand.sh bizoholic
./scripts/switch-brand.sh coreldove
./scripts/switch-brand.sh thrillring
./scripts/switch-brand.sh quanttrade
```

### Stopping Services
```bash
./scripts/dev-stop.sh
```

---

## ☁️ VPS Deployment (Production)

Your VPS has strict limits (2vCPU, 8GB RAM, 100GB Storage).

### 1. Sync to GHCR
Push your local changes to GitHub Container Registry.
```bash
./push-to-ghcr.sh
```

### 2. Deploy on VPS
On the VPS, pull and run:
```bash
# 1. Copy docker-compose.prod.yml to VPS
scp docker-compose.prod.yml user@vps:/path/to/deploy/

# 2. Start services
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Maintenance
Run cleanup script periodically to prevent disk fill-up.
```bash
./scripts/vps-cleanup.sh
```

---

## ❓ Troubleshooting

**High RAM Usage?**
- Stop unused containers: `./scripts/dev-stop.sh`
- Use `minimal` profile.
- Check `docker stats`.

**Disk Full?**
- Run `docker system prune -a`
- Verify data is on HDD: `docker info | grep Root`

**Port Conflicts?**
- Check if other services are running on 5432, 6379, 8001.
- Stop old containers: `docker rm -f $(docker ps -aq)`
