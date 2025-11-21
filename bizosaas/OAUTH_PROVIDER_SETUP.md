# OAuth Provider Setup Guide

## Overview

This guide provides step-by-step instructions for setting up OAuth 2.0 applications with each SSO provider for the BizOSaaS Client Portal.

**Live URL**: `https://stg.bizoholic.com/portal`

**Redirect URIs** (register these with each provider):
- Google: `https://stg.bizoholic.com/portal/auth/callback/google`
- Microsoft: `https://stg.bizoholic.com/portal/auth/callback/microsoft`
- GitHub: `https://stg.bizoholic.com/portal/auth/callback/github`
- Slack: `https://stg.bizoholic.com/portal/auth/callback/slack`
- LinkedIn: `https://stg.bizoholic.com/portal/auth/callback/linkedin`

---

## 1. Google OAuth Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click **Select a Project** → **New Project**
3. Enter project name: `BizOSaaS Client Portal`
4. Click **Create**

### Step 2: Enable Google+ API

1. In the left sidebar, go to **APIs & Services** → **Library**
2. Search for `Google+ API`
3. Click on it and press **Enable**

### Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth 2.0 Client ID**
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: `BizOSaaS Client Portal`
   - User support email: `support@bizoholic.com`
   - Developer contact: `dev@bizoholic.com`
   - Click **Save and Continue**
   - Scopes: Add `openid`, `email`, `profile`
   - Click **Save and Continue**
   - Test users: Add your test email addresses
   - Click **Save and Continue**

4. Create OAuth Client ID:
   - Application type: **Web application**
   - Name: `BizOSaaS Client Portal`
   - Authorized JavaScript origins: `https://stg.bizoholic.com`
   - Authorized redirect URIs: `https://stg.bizoholic.com/portal/auth/callback/google`
   - Click **Create**

5. Copy the **Client ID** and **Client Secret**

### Step 4: Add to Environment Variables

```bash
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

---

## 2. Microsoft/Azure AD OAuth Setup

### Step 1: Register Application

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**

### Step 2: Configure Application

1. Name: `BizOSaaS Client Portal`
2. Supported account types: **Accounts in any organizational directory and personal Microsoft accounts**
3. Redirect URI:
   - Platform: **Web**
   - URI: `https://stg.bizoholic.com/portal/auth/callback/microsoft`
4. Click **Register**

### Step 3: Add API Permissions

1. Go to **API permissions** in the left sidebar
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Select **Delegated permissions**
5. Add the following permissions:
   - `openid`
   - `email`
   - `profile`
   - `User.Read`
6. Click **Add permissions**
7. Click **Grant admin consent** (if you have admin rights)

### Step 4: Create Client Secret

1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Description: `Client Portal Secret`
4. Expires: **24 months** (or as per security policy)
5. Click **Add**
6. **Copy the secret value immediately** (you won't see it again)

### Step 5: Note Application Details

1. Go to **Overview**
2. Copy **Application (client) ID**
3. Copy **Directory (tenant) ID** (if needed)

### Step 6: Add to Environment Variables

```bash
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret
```

---

## 3. GitHub OAuth Setup

### Step 1: Create OAuth App

1. Go to [GitHub Settings](https://github.com/settings/developers)
2. Click **OAuth Apps** → **New OAuth App**

### Step 2: Register Application

1. Application name: `BizOSaaS Client Portal`
2. Homepage URL: `https://stg.bizoholic.com`
3. Application description: `SSO for BizOSaaS Client Portal`
4. Authorization callback URL: `https://stg.bizoholic.com/portal/auth/callback/github`
5. Click **Register application**

### Step 3: Generate Client Secret

1. Click **Generate a new client secret**
2. **Copy the secret immediately** (you won't see it again)
3. Copy the **Client ID** from the top

### Step 4: Add to Environment Variables

```bash
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

---

## 4. Slack OAuth Setup

### Step 1: Create Slack App

1. Go to [Slack API](https://api.slack.com/apps)
2. Click **Create New App**
3. Choose **From scratch**
4. App Name: `BizOSaaS Client Portal`
5. Pick a workspace to develop your app: Select your workspace
6. Click **Create App**

### Step 2: Configure OAuth & Permissions

1. In the left sidebar, click **OAuth & Permissions**
2. Scroll to **Redirect URLs**
3. Click **Add New Redirect URL**
4. Enter: `https://stg.bizoholic.com/portal/auth/callback/slack`
5. Click **Add**
6. Click **Save URLs**

### Step 3: Add Scopes

1. Scroll to **Scopes** section
2. Under **User Token Scopes**, click **Add an OAuth Scope**
3. Add the following scopes:
   - `identity.basic`
   - `identity.email`
   - `identity.avatar` (optional)

### Step 4: Get Client Credentials

1. Scroll to **App Credentials** at the top
2. Copy **Client ID**
3. Copy **Client Secret**

### Step 5: Add to Environment Variables

```bash
SLACK_CLIENT_ID=your_slack_client_id
SLACK_CLIENT_SECRET=your_slack_client_secret
```

---

## 5. LinkedIn OAuth Setup

### Step 1: Create LinkedIn App

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers)
2. Click **Create app**

### Step 2: Fill Application Details

1. App name: `BizOSaaS Client Portal`
2. LinkedIn Page: Select or create a company page
3. App logo: Upload your logo (optional)
4. Legal Agreement: Check the box
5. Click **Create app**

### Step 3: Request Sign In with LinkedIn

1. Go to the **Products** tab
2. Find **Sign In with LinkedIn**
3. Click **Request access**
4. Wait for approval (usually instant for basic access)

### Step 4: Configure OAuth Settings

1. Go to the **Auth** tab
2. Under **OAuth 2.0 settings**:
   - Authorized redirect URLs: Add `https://stg.bizoholic.com/portal/auth/callback/linkedin`
   - Click **Update**

### Step 5: Get Client Credentials

1. Under **Application credentials**, copy:
   - **Client ID**
   - **Client Secret**

### Step 6: Add to Environment Variables

```bash
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
```

---

## Environment Variables Summary

Add all OAuth credentials to your auth-service-v2 environment:

```bash
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Microsoft OAuth
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret

# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Slack OAuth
SLACK_CLIENT_ID=your_slack_client_id
SLACK_CLIENT_SECRET=your_slack_client_secret

# LinkedIn OAuth
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret

# Application URL (for redirect URI generation)
NEXT_PUBLIC_APP_URL=https://stg.bizoholic.com/portal
```

---

## Deployment Checklist

### Backend (auth-service-v2)

- [ ] Install dependencies: `pip install httpx==0.25.2 authlib==1.3.0`
- [ ] Add environment variables to Dokploy
- [ ] Run database migration: `psql -f migrations/001_add_oauth_accounts.sql`
- [ ] Restart auth-service-v2
- [ ] Test OAuth endpoints: `GET /api/auth/oauth/providers`

### Frontend (client-portal)

- [ ] Build new image with SSO UI: v2.2.4
- [ ] Push to GHCR
- [ ] Deploy to staging
- [ ] Verify SSO buttons appear on login page
- [ ] Test OAuth flow with one provider

---

## Testing OAuth Flow

### Manual Test Steps

1. **Visit login page**: https://stg.bizoholic.com/portal/login
2. **Click SSO button**: (e.g., "Google")
3. **Verify redirect**: Should go to Google OAuth consent page
4. **Authorize**: Grant permissions
5. **Verify callback**: Should redirect to `/portal/auth/callback/google`
6. **Verify login**: Should redirect to `/portal/dashboard` with valid session
7. **Check cookies**: HttpOnly `refresh_token` cookie should be set
8. **Test logout**: Verify session is cleared

### Expected Response Flow

```
POST /api/auth/oauth/google/authorize
→ Returns: { "authorization_url": "https://accounts.google.com/...", "state": "..." }

User authorizes on Google
→ Redirects to: /portal/auth/callback/google?code=...&state=...

GET /api/auth/oauth/google/callback?code=...&state=...
→ Returns: { "access_token": "...", "refresh_token": "...", "user": {...} }

Frontend stores tokens
→ Redirects to: /portal/dashboard
```

---

## Troubleshooting

### Provider Redirect Issues

**Symptom**: OAuth provider shows "Redirect URI mismatch" error

**Fix**: Verify redirect URI is exactly:
- `https://stg.bizoholic.com/portal/auth/callback/{provider}`
- No trailing slash
- Correct https protocol
- Correct domain

### State Verification Failed

**Symptom**: "Invalid or expired OAuth state" error

**Fix**:
- State expires after 5 minutes
- Use Redis for production (currently in-memory)
- Check system time synchronization

### Email Not Provided

**Symptom**: "Email not provided by OAuth provider"

**Fix**:
- Verify email scope is requested
- Some providers require separate API call for email (LinkedIn)
- Check OAuth consent screen configuration

### CSP Blocking Redirect

**Symptom**: Browser console shows CSP violation

**Fix**: Verify `form-action` CSP directive includes OAuth provider domains (already configured in v2.2.4)

---

## Security Considerations

### Production Recommendations

1. **Token Storage**: Encrypt OAuth access/refresh tokens in database
2. **State Management**: Use Redis with TTL for state parameter storage
3. **Rate Limiting**: Implement rate limiting on OAuth endpoints
4. **Audit Logging**: Log all OAuth authentication attempts
5. **Account Linking**: Implement email verification before linking accounts
6. **Revocation**: Implement OAuth token revocation on logout
7. **Scope Minimization**: Only request necessary OAuth scopes

### Monitoring

- Track OAuth provider availability
- Monitor failed authentication attempts
- Alert on unusual OAuth activity patterns
- Track SSO adoption rates by provider

---

## Next Steps

1. **Complete OAuth setup** for all 5 providers
2. **Deploy auth-service-v2** with OAuth endpoints
3. **Deploy client-portal v2.2.4** with SSO UI
4. **Test each provider** end-to-end
5. **Monitor for errors** in production logs
6. **Document any provider-specific issues**
7. **Plan enterprise SSO** (SAML 2.0) for Phase 2
