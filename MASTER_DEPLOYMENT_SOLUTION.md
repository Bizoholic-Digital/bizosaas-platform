# Master Deployment Solution Guide (Updated 06/01/2026)

## 1. Core Service Routing Strategy
Due to issues with Dokploy's Overlay network (packet loss from Traefik container), we have implemented a **Bridge Network Strategy** for Traefik routing.

**Key Configuration:**
-   **Services File:** `/etc/dokploy/traefik/dynamic/services.yml` (Server-side only, managed manually)
-   **Network:** `bizosaascore-vault-entjt5` (Bridge network shared by Vault and Traefik)
-   **Addressing:** Services use their IP addresses on this bridge network to ensure connectivity.

**Current IP Map (Dynamic on Restart):**
-   Client Portal: `172.19.0.4:3003` (`http://app.bizoholic.net`)
-   Admin Portal: `172.19.0.5:3004` (`http://admin.bizoholic.net`)
-   Brain Gateway: `172.19.0.6:8000` (`http://api.bizoholic.net`)
-   Vault: `http://vault:8200` (`http://vault.bizoholic.net`)

**Maintenance:**
-   If containers are recreated and get new IPs, `services.yml` must be updated on the server.
-   A template is stored in `infrastructure/dokploy/services-template.yml`.

## 2. Vault Deployment
-   **URL:** `https://vault.bizoholic.net`
-   **Setup:** Accessible via `dokploy-network` and `bizosaascore-vault-entjt5`.
-   **Initialization:** Use `scripts/init-local-vault.sh` to unseal or init if redeployed.

## 3. Deployment Redundancy
-   **Secret Storage:** Primary -> Vault. Fallback -> PostgreSQL (`DatabaseSecretAdapter`).
-   To redeploy apps, use Dokploy UI, but verify IPs if Traefik returns 502.

## 4. Immediate Actions Performed
1.  Fixed network connectivity by attaching Portals/Gateway to `bizosaascore-vault-entjt5`.
2.  Created static `services.yml` to route traffic via local bridge IPs.
3.  Synced working configs to git `staging` branch.
