# BizOSaaS Authentication Configuration Summary

## Session Management Settings

### Client Portal & Admin Dashboard
- **Total Session Duration**: 8 hours
- **Inactivity Timeout**: 30 minutes
- **Strategy**: JWT (stateless)

### How It Works:
1. User logs in → Session created (valid for 8 hours)
2. Every user action → Session timestamp updated
3. If inactive for 30 minutes → Session expires, user logged out
4. If active → Session extends up to 8 hours max

## Authentication Flow

### Client Portal (app.bizoholic.net)
```
User → Login Page → Authentik SSO → Dashboard
                  ↓
            (or Credentials)
```

### Admin Dashboard (admin.bizoholic.net)
```
Admin → Login Page → Authentik SSO → Admin Dashboard
                   ↓
             (or Credentials)
                   ↓
        (Role Check: super_admin/platform_admin)
```

## Environment Variables Required

### Production (.env.production)
```bash
# NextAuth Configuration
NEXTAUTH_URL=https://app.bizoholic.net  # or admin.bizoholic.net
NEXTAUTH_SECRET=<generate-with-openssl-rand-base64-32>

# Authentik SSO
AUTHENTIK_URL=https://auth.bizoholic.com
AUTHENTIK_CLIENT_ID=<from-authentik-provider>
AUTHENTIK_CLIENT_SECRET=<from-authentik-provider>
AUTHENTIK_ISSUER=https://auth.bizoholic.com/application/o/bizosaas/

# Auth Service (Fallback)
AUTH_SERVICE_URL=http://brain-auth:8007
```

## Authentik Configuration Required

### Provider Settings
1. **Name**: BizOSaaS Platform
2. **Client Type**: Confidential
3. **Redirect URIs**:
   - `https://app.bizoholic.net/api/auth/callback/authentik`
   - `https://admin.bizoholic.net/api/auth/callback/authentik`
   - `http://localhost:3003/api/auth/callback/authentik` (dev)
   - `http://localhost:3004/api/auth/callback/authentik` (dev)

### Application Settings
1. **Slug**: `bizosaas`
2. **Provider**: Link to provider above
3. **Launch URL**: `https://app.bizoholic.net`

## Security Features

✅ **Implemented**:
- JWT-based sessions (stateless)
- Inactivity timeout (30 min)
- Maximum session duration (8 hours)
- Role-based access control (Admin Dashboard)
- SSO via Authentik
- Credentials fallback
- HTTPS enforcement (production)
- CSRF protection (NextAuth built-in)

⏳ **Recommended Additions**:
- Rate limiting on login attempts
- 2FA/MFA support (via Authentik)
- Session device tracking
- Audit logging for admin actions

## Testing Checklist

### Client Portal
- [ ] Login with Authentik SSO
- [ ] Login with credentials
- [ ] Session persists on page refresh
- [ ] Auto-logout after 30 min inactivity
- [ ] Manual logout works
- [ ] Redirect to login when session expires

### Admin Dashboard
- [ ] Login with Authentik SSO (admin user)
- [ ] Login with credentials (admin user)
- [ ] Non-admin users redirected to Client Portal
- [ ] Session persists on page refresh
- [ ] Auto-logout after 30 min inactivity
- [ ] Manual logout works
- [ ] Access to admin-only routes enforced

## Deployment Notes

1. **Generate NEXTAUTH_SECRET** for production:
   ```bash
   openssl rand -base64 32
   ```

2. **Set in Dokploy Environment Variables**:
   - Client Portal service
   - Admin Dashboard service

3. **Configure Authentik**:
   - Add redirect URIs
   - Copy Client ID and Secret to env vars

4. **Test Flow**:
   - Test SSO login
   - Test credentials login
   - Test inactivity timeout
   - Test role-based access (admin)
