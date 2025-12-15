# Social Login Implementation Guide

## Overview
Adding Google, Microsoft, and LinkedIn OAuth to both Client Portal and Admin Dashboard.

## Step 1: Configure OAuth Providers in Authentik

### Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials:
   - **Authorized redirect URIs**:
     - `https://sso.bizoholic.net/source/oauth/callback/google/`
     - `https://app.bizoholic.net/api/auth/callback/google`
     - `https://admin.bizoholic.net/api/auth/callback/google`
5. Save Client ID and Client Secret

### Microsoft OAuth Setup
1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to Azure Active Directory → App registrations
3. Create new registration:
   - **Name**: BizOSaaS
   - **Redirect URIs**:
     - `https://sso.bizoholic.net/source/oauth/callback/microsoft/`
     - `https://app.bizoholic.net/api/auth/callback/azure-ad`
     - `https://admin.bizoholic.net/api/auth/callback/azure-ad`
4. Create client secret
5. Save Application (client) ID and Client Secret

### LinkedIn OAuth Setup
1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create new app
3. Add redirect URLs:
   - `https://sso.bizoholic.net/source/oauth/callback/linkedin/`
   - `https://app.bizoholic.net/api/auth/callback/linkedin`
   - `https://admin.bizoholic.net/api/auth/callback/linkedin`
4. Request access to Sign In with LinkedIn
5. Save Client ID and Client Secret

## Step 2: Add to Authentik (Optional - for centralized management)

In Authentik Admin (`https://sso.bizoholic.net/if/admin/`):
1. Go to **Directory → Federation & Social login**
2. Click **Create**
3. Select provider type (Google, Microsoft, LinkedIn)
4. Enter Client ID and Secret
5. Configure scopes:
   - Google: `openid profile email`
   - Microsoft: `openid profile email User.Read`
   - LinkedIn: `r_liteprofile r_emailaddress`

## Step 3: Environment Variables

Add to `.env` or Dokploy environment:

```bash
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Microsoft OAuth
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret
MICROSOFT_TENANT_ID=common  # or your specific tenant ID

# LinkedIn OAuth
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret

# GitHub OAuth (optional)
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

## Step 4: Store Secrets in Vault (Production)

```bash
# Store in HashiCorp Vault
vault kv put secret/bizosaas/oauth \
  google_client_id="..." \
  google_client_secret="..." \
  microsoft_client_id="..." \
  microsoft_client_secret="..." \
  linkedin_client_id="..." \
  linkedin_client_secret="..."
```

## Security Notes

1. **Never commit secrets to Git**
2. **Use Vault in production** for secret management
3. **Rotate secrets regularly** (every 90 days)
4. **Monitor OAuth usage** in provider dashboards
5. **Implement rate limiting** on OAuth endpoints

## Testing Checklist

- [ ] Google login works on Client Portal
- [ ] Google login works on Admin Dashboard
- [ ] Microsoft login works on Client Portal
- [ ] Microsoft login works on Admin Dashboard
- [ ] LinkedIn login works on Client Portal
- [ ] LinkedIn login works on Admin Dashboard
- [ ] User data correctly mapped (email, name)
- [ ] Roles correctly assigned
- [ ] Session persists after OAuth login
- [ ] Logout works correctly

---

**Created**: 2025-12-15
**Status**: Ready for implementation
