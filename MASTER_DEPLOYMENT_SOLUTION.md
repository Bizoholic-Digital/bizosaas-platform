# Master Deployment Solution Guide - Clean Migration View

## 1. Universal Deployment Philosophy (Defaults)
The platform is designed to run with standard **Dokploy/Traefik Docker Label** routing. 
-   **Ports**: All frontend services listen on internal port `3000`.
-   **Routing**: Managed automatically by Traefik using Docker/Swarm labels.
-   **Network**: Standard `dokploy-network` (Overlay).

## 2. Stability Recommendation: Docker Compose vs Swarm
If you find that your current VPS has intermittent communication issues via the Overlay network (Swarm), consider migrating to **Portainer + Standard Docker Compose**:
1.  **Why?** Standard Bridge networks are significantly more stable on single-node VPS setups than Swarm Overlay networks.
2.  **How?** Deploy the compose files as "Stacks" in Portainer. You can still use Traefik but configured for the standard Docker provider.

## 3. Current Server Context (Fallback Mode)
On the **current server (72.60.98.213)**, we are using a **Bridge Fallback Strategy** because the host's Overlay network is experiencing packet loss.
-   **DO NOT** redeploy these defaults to the *current* server without ensuring the networking issues are fixed (e.g., via a host reboot or network driver fix).
-   If you move to a **New Server**, simply clone the repo and deploy. It is set to 3000/Labels by default.

## 4. Key Verification Checklist (New Server)
1.  **Clone Repo**: `git clone` on `staging`.
2.  **Environment**: Ensure all `.env` files match the production credentials.
3.  **Vault**: Deploy the `bizosaas-brain-core` stack and run `scripts/init-local-vault.sh`.
4.  **Ingress**: Ensure the new Traefik instance has `providers.docker` enabled.
5.  **PWA**: The Admin Portal PWA is now fully integrated into the code (`layout.tsx`) and requires no manual setup on new servers.

## 5. Summary of Pushed Defaults
-   **Client Portal**: Port 3000 (Internal/External mapped)
-   **Admin Dashboard**: Port 3000 (Internal/External mapped)
-   **Traefik Labels**: Restored to standard discovery format.
