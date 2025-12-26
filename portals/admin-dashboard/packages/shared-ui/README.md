# BizOSaaS Shared UI Components

Reusable UI components shared across all BizOSaaS portals.

## Installation

This package is part of the monorepo and can be imported directly:

```typescript
import { UnifiedLoginForm } from '@bizosaas/shared-ui'
```

## Components

### UnifiedLoginForm

A flexible, configurable login component that supports:
- SSO authentication (Authentik, Okta, etc.)
- Email/Password credentials
- Both SSO and credentials (hybrid mode)

#### Usage Examples

**Admin Dashboard (SSO Only):**

```typescript
import { signIn } from '@/lib/auth'
import { UnifiedLoginForm } from '@bizosaas/shared-ui'
import { PlatformBranding } from '@/components/ui/platform-branding'

export default function AdminLoginPage({ searchParams }: { searchParams: { callbackUrl?: string } }) {
  return (
    <UnifiedLoginForm
      mode="sso"
      platformName="Admin Dashboard"
      platformSubtitle="Platform Administration & Management"
      ssoProviderName="Authentik"
      ssoProviderId="authentik"
      defaultRedirectUrl="/dashboard"
      BrandingComponent={() => <PlatformBranding platform="BIZOSAAS" size="lg" />}
      onSSOLogin={async () => {
        'use server'
        await signIn('authentik', {
          redirectTo: searchParams.callbackUrl || '/dashboard',
        })
      }}
    />
  )
}
```

**Client Portal (Credentials Only):**

```typescript
'use client'

import { signIn } from 'next-auth/react'
import { UnifiedLoginForm } from '@bizosaas/shared-ui'
import { PlatformBranding } from '@/components/ui/platform-branding'

export default function ClientLoginPage() {
  return (
    <UnifiedLoginForm
      mode="credentials"
      platformName="Client Portal"
      platformSubtitle="Access your projects and services"
      defaultRedirectUrl="/"
      showDemoCredentials={process.env.NODE_ENV === 'development'}
      BrandingComponent={() => <PlatformBranding platform="BIZOHOLIC" size="lg" />}
      onCredentialsLogin={async (email, password) => {
        const result = await signIn('credentials', {
          email,
          password,
          redirect: false,
        })
        return {
          ok: result?.ok || false,
          error: result?.error,
        }
      }}
    />
  )
}
```

**Hybrid Mode (Both SSO and Credentials):**

```typescript
'use client'

import { signIn } from 'next-auth/react'
import { UnifiedLoginForm } from '@bizosaas/shared-ui'

export default function HybridLoginPage() {
  return (
    <UnifiedLoginForm
      mode="both"
      platformName="BizOSaaS Platform"
      platformSubtitle="Choose your preferred sign-in method"
      ssoProviderName="Authentik"
      defaultRedirectUrl="/dashboard"
      onCredentialsLogin={async (email, password) => {
        const result = await signIn('credentials', { email, password, redirect: false })
        return { ok: result?.ok || false, error: result?.error }
      }}
      onSSOLogin={async () => {
        await signIn('authentik')
      }}
    />
  )
}
```

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `mode` | `'sso' \| 'credentials' \| 'both'` | ✅ | Authentication mode |
| `platformName` | `string` | ✅ | Platform name to display |
| `platformSubtitle` | `string` | ❌ | Platform subtitle/description |
| `ssoProviderName` | `string` | ❌ | SSO provider name (default: 'SSO') |
| `ssoProviderId` | `string` | ❌ | SSO provider ID for NextAuth (default: 'authentik') |
| `defaultRedirectUrl` | `string` | ❌ | Default redirect URL after login (default: '/') |
| `BrandingComponent` | `React.ComponentType` | ❌ | Custom branding component |
| `showDemoCredentials` | `boolean` | ❌ | Show demo credentials (default: false) |
| `className` | `string` | ❌ | Custom CSS classes |
| `onCredentialsLogin` | `(email, password) => Promise<{ok, error?}>` | ❌ | Credentials login callback |
| `onSSOLogin` | `() => Promise<void>` | ❌ | SSO login callback |

## Benefits

✅ **Single Source of Truth** - One component for all login screens  
✅ **Consistent UX** - Same look and feel across all portals  
✅ **Flexible** - Supports SSO, credentials, or both  
✅ **Maintainable** - Update once, apply everywhere  
✅ **Type-Safe** - Full TypeScript support  

## Development

```bash
# Type check
npm run type-check

# Lint
npm run lint
```
