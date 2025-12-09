# Portainer Setup & Management Guide

## Overview

Portainer provides a user-friendly UI to manage your Docker environment. We use it to:
1. View container logs
2. Restart services
3. Monitor resource usage
4. Manage stacks

## Access

- **URL**: [https://localhost:9443](https://localhost:9443)
- **Credential**: Configured on first login

## Importing the BizOSaaS Stack

For full control, you should import the `docker-compose.registry.yml` into Portainer.

1. **Login** to Portainer.
2. Go to **Local** environment.
3. Click **Stacks** -> **Add stack**.
4. **Name**: `bizosaas`
5. **Build method**: `Upload`
6. **Upload**: Select `docker-compose.registry.yml` from your project root.
7. **Environment variables**: Upload your `.env.local` file.
8. Click **Deploy the stack**.

> **Note**: Since we deployed via script, Portainer might show "Limited Control" initially. To gain full control, remove the script-deployed stack (`docker-compose down`) and re-deploy via Portainer using the steps above.

## Connecting to Registry

To pull updated images within Portainer:

1. Go to **Registries**.
2. Click **Add registry**.
3. **Select**: Custom registry.
4. **Name**: `Local Registry`
5. **Registry URL**: `localhost:5000`
6. Click **Add registry**.

Now you can use this registry to pull images directly from Portainer.

## Managing CI/CD Deployments

When GitHub Actions pushes new images to the registry, you can update services in Portainer:

1. Go to **Services** (or Containers).
2. Find the service (e.g., `bizosaas-client-portal`).
3. Click **Recreate**.
4. Enable **Pull latest image**.
5. Click **Recreate**.

This mimics the continuous deployment process manually.

---

**Troubleshooting**

- **Port 9443 conflict**: If Portainer fails to start, check if another service uses 9443 or 9000.
- **Volume errors**: Portainer persists data in `portainer_data`. If you lose password, you may need to recreate the container.
