# 🚀 Deployment & Configuration Manifest
## BizOSaaS Admin Dashboard (PWA Enabled)

**Date**: 2025-12-11 16:15 IST
**Status**: Ready for Production Deployment

---

## 🎨 UI & Architecture Decision

**Decision**: **Stick with Current Architecture** (Do NOT migrate to TailAdmin v2)

**Rationale**:
The current admin dashboard uses a modern, robust stack based on **Shadcn UI** (Radix UI + Tailwind CSS), React Hook Form, Zod, and TanStack Query.
- **Superior to TailAdmin**: TailAdmin is typically a simpler HTML/CSS template. Shadcn UI provides accessible, headless components that are far more scalable for a complex SaaS platform.
- **Modern Stack**: We are using the "Vercel/Next.js" recommended stack (Next.js 15, Server Components).
- **Consistency**: Matches the high-quality architecture of the Brain Gateway and Client Portal.

---

## 📱 PWA Implementation

**Status**: ✅ Enabled

- **Plugin**: `@ducanh2912/next-pwa` (Next.js 15 compatible)
- **Manifest**: `app/manifest.ts` (Native Next.js Metadata Route)
- **Features**:
  - Installable (Add to Home Screen)
  - Offline support (Service Worker)
  - Standalone display mode

---

## 🛳️ Dokploy VPS Deployment Configuration

Use these details to configure the service in Dokploy.

### 1. Project Context
- **Project Name**: `bizosaas-platform` (or your existing project)
- **Service Name**: `bizosaas-admin-dashboard`

### 2. Deployment Source
- **Repository**: `https://github.com/<your-org>/bizosaas-platform` (Replace <your-org>)
- **Branch**: `main`
- **Build Context**: `./portals/admin-dashboard`
- **Dockerfile Path**: `./Dockerfile` (relative to build context)

### 3. Environment Variables (Copy & Paste)

```env
# Authentik SSO (Production)
AUTHENTIK_URL=https://sso.bizoholic.net
NEXT_PUBLIC_SSO_URL=https://sso.bizoholic.net
AUTHENTIK_ISSUER=https://sso.bizoholic.net/application/o/bizosaas-admin/
AUTHENTIK_CLIENT_ID=bizosaas-admin-dashboard
AUTHENTIK_CLIENT_SECRET=<GET_FROM_AUTHENTIK_VPS>
AUTH_SECRET=<GENERATE_WITH_OPENSSL_RAND_BASE64_32>

# Internal Services
NEXT_PUBLIC_BRAIN_GATEWAY_URL=https://api.bizoholic.net
NEXT_PUBLIC_TEMPORAL_UI_URL=https://temporal.bizoholic.net
NEXT_PUBLIC_VAULT_UI_URL=https://vault.bizoholic.net

# NextAuth Configuration
NEXTAUTH_URL=https://admin.bizoholic.net
NEXTAUTH_URL_INTERNAL=http://localhost:3004

# Application Settings
NODE_ENV=production
PORT=3004
```

### 4. Domain & Networking
- **Domain**: `admin.bizoholic.net`
- **Internal Port**: `3004`
- **HTTPS/SSL**: Enabled (Let's Encrypt)
- **Redirect HTTP to HTTPS**: Enabled

---

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/deploy-admin-dashboard.yml`) is already configured to build and deploy automatically on push to `main`.

**To trigger deployment**:
1. Commit all changes.
2. Push to `main`.
3. GitHub Actions will build the Docker image and deploy to VPS.

---

## 📝 Immediate Next Steps

1. **Commit PWA Changes**:
   ```bash
   git add portals/admin-dashboard/next.config.js portals/admin-dashboard/app/manifest.ts portals/admin-dashboard/package.json portals/admin-dashboard/package-lock.json
   git commit -m "feat: enable PWA for admin dashboard"
   git push origin main
   ```

2. **Configure VPS Authentik**:
   - Create the `bizosaas-admin` application if not exists.
   - Get the Client Secret updates the Dokploy environment variable.

3. **Verify Deployment**:
   - Visit `https://admin.bizoholic.net`
   - Check "Install App" icon in browser bar.
