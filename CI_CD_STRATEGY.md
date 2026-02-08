# CI/CD & Deployment Guide (Dokploy + GHCR)

This guide outlines our standardized deployment process for the BizOSaaS Platform, including **CorelDove**, **Bizoholic**, and future tenants like **ThrillRing**.

## 🏗 Architecture Overview

1.  **Code Repository**: GitHub (Staging/Main branches)
2.  **CI Pipeline**: GitHub Actions
3.  **Artifact Registry**: GitHub Container Registry (GHCR)
4.  **Production Host**: VPS (KVM2) via **Dokploy**

## 🔄 The CI/CD Flow

1.  **Push Code**: Developer pushes code to `staging` branch.
2.  **Build**: GitHub Action automatically builds optimized Docker images for:
    *   `client-portal` (Next.js BFF - Uses NextAuth + Authentik)
    *   `brain-gateway` (FastAPI Core)
    *   `auth-service` (Permission & Context Manager - RBAC bridge for Authentik)
3.  **Push Registry**: Images are pushed to `ghcr.io/bizoholic-digital/bizosaas-platform/<service>:staging`.
4.  **Deploy**: Dokploy (on VPS) detects the new image tag (or via webhook) and pulls the update.

## 🛠 Usage Instructions

### 1. Configure GitHub Actions (Already Done)
The `.github/workflows/ci-cd.yml` file is configured to build specific services.

### 2. Configure Dokploy (VPS)
For each service you want valid CI/CD for:

1.  **Login to Dokploy** (`http://194.238.16.237:3000`).
2.  **Add Registry**:
    *   Go to **Project Settings** -> **Registries**.
    *   **Name**: `GitHub Container Registry`
    *   **URL**: `ghcr.io`
    *   **Username**: (GitHub Username)
    *   **Password**: (GitHub Personal Access Token with `read:packages` scope)
3.  **For Each Service** (e.g., Client Portal):
    *   Go to **Application** (or Docker).
    *   **Image**: `ghcr.io/bizoholic-digital/bizosaas-platform/client-portal:staging`
    *   **Registry**: Select the one created above.
    *   **Auto Deploy**: Enabled (optional, or use Webhook).

## 🌍 Tenant Strategy (WordPress/CMS)

For **CorelDove**, **Bizoholic**, and **ThrillRing**:

*   **Hosting**: These are hosted as separate applications (containers) on the same VPS managed by Dokploy.
*   **Integration**: The **Client Portal** connects to them via APIs.
*   **Configuration**:
    *   In the Client Portal's `.env` (managed in Dokploy):
        ```env
        TENANT_CORELDOVE_API=https://coreldove.com/wp-json
        TENANT_BIZOHOLIC_API=https://bizoholic.com/wp-json
        TENANT_THRILLRING_API=https://thrillring.com/wp-json
        ```
    *   This keeps the core platform cleanly separated from the individual tenant CMS instances.

## 🚀 Recommended Next Step
Run the manual `deploy-to-kvm2.sh` script first to establish the baseline. Then, migrate the critical `client-portal` to use the GHCR image via Dokploy for automated updates.
