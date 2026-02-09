# Implementation Plan - Restoring Login & Fixing SSO/Billing Access

This plan outlines the steps to resolve the connectivity issues (522/404 errors) for SSO and Billing services and restore the login functionality across the platform using Authentik.

## 1. Fix SSO Routing & SSL
The current Traefik configuration for Authentik is causing conflicts (multiple services mapped to routers) and certificate rate limits.

- [ ] **Task 1.1: Clean up Authentik Traefik Labels**
    - Update `docker-compose.authentik.yml` to use a single, distinct set of labels.
    - Explicitly define the service name in routers to avoid "automatic linking" ambiguity.
    - Ensure both `sso.bizoholic.net` and `auth-sso.bizoholic.net` (if needed) are properly mapped.
- [ ] **Task 1.2: Resolve SSL Rate Limits**
    - Verify Cloudflare SSL settings. If set to "Full (Strict)", temporarily set to "Full" or "Flexible" if Let's Encrypt is blocked, OR fix the challenge issues.
    - Check Traefik's `acme.json` to see current certificate status.

## 2. Restore Platform Login
We need to ensure the main application uses Authentik for authentication.

- [ ] **Task 2.1: Configure Authentik Application/Provider**
    - Log in to Authentik Admin.
    - Verify an "OAuth2/OpenID Provider" is created for the BizOSaaS platform.
    - Create/Verify "Applications" for Client Portal and Admin Dashboard.
- [ ] **Task 2.2: Update Portals Configuration**
    - Update environment variables for `admin-dashboard` and `client-portal` to point to the Authentik OIDC endpoints.
    - Restart portal containers.

## 3. Resolve Billing API Connectivity
Lago API is working internally but 522 externally.

- [ ] **Task 3.1: Check Traefik-Lago Routing**
    - Verify Lago API labels in `docker-compose.lago.yml`.
    - Ensure the `letsencrypt` solver is working for this domain.
- [ ] **Task 3.2: Verify Backend Responses**
    - Double check that the container doesn't restart during ACME challenges.

## 4. Documentation & Verification
- [ ] **Task 4.1: Update Credentials**
    - Document all new service accounts and passwords generated during this session.
- [ ] **Task 4.2: Final E2E Test**
    - Verify login flow from landing page -> Authentik SSO -> Dashboard.
