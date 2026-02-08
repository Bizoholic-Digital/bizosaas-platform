# Authentik Configuration Guide
**Date**: 2026-01-25  
**Status**: REQUIRED for Login to Work

You have successfully migrated the codebase to use Authentik. Now you must configure Authentik itself to accept these login requests.

---

## 🚀 Step 1: Login to Authentik Admin

1.  **URL**: [https://auth-sso.bizoholic.net/if/admin/](https://auth-sso.bizoholic.net/if/admin/)
    *   *If you haven't set a password yet, use the recovery link provided earlier.*
2.  Navigate to the **Admin Interface** (click "Admin Interface" in top right if you land on user dashboard).

---

## ⚙️ Step 2: Create Provider

1.  Go to **Applications** -> **Providers**.
2.  Click **Create**.
3.  Select **OAuth2/OpenID Provider**.
4.  **Name**: `BizOSaaS Platform Provider`
5.  **Authentication Flow**: `default-authentication-flow` (or similar).
6.  **Authorization Flow**: `default-provider-authorization-explicit-consent` (or implicit).
7.  **Client Type**: `Confidential`
8.  **Client ID**: `bizosaas-portal`  <-- **CRITICAL** (Must match code)
9.  **Client Secret**: `BizOSaaS2024!AuthentikSecret` <-- **CRITICAL** (Must match code)
10. **Redirect URIs**:
    *   `https://admin.bizoholic.net/api/auth/callback/authentik`
    *   `https://app.bizoholic.net/api/auth/callback/authentik`
    *   `https://directory.bizoholic.net/api/auth/callback/authentik`
    *   *(Note: Enter each one on a new line or use regex `.*` for testing)*
11. **Signing Key**: Select the default certificate.
12. Click **Finish**.

---

## 📱 Step 3: Create Application

1.  Go to **Applications** -> **Applications**.
2.  Click **Create**.
3.  **Name**: `BizOSaaS Platform`
4.  **Slug**: `bizosaas-platform` <-- **CRITICAL** (Used in Issuer URL)
5.  **Provider**: Select `BizOSaaS Platform Provider` (created in Step 2).
6.  **Launch URL**: `https://app.bizoholic.net`
7.  Click **Create**.

---

## 👥 Step 4: Verify Users

1.  Go to **Directory** -> **Users**.
2.  Ensure you have a user to test with (e.g., `admin@bizoholic.net`).
3.  Set a password for the user if needed.

---

## 🔍 Verification

Once configured, go to:
*   [https://app.bizoholic.net](https://app.bizoholic.net) -> Login -> Should redirect to Authentik.
*   [https://admin.bizoholic.net](https://admin.bizoholic.net) -> Login -> Should redirect to Authentik.

If you see "Client ID mismatch" or "Issuer mismatch", double-check Steps 2 and 3.
