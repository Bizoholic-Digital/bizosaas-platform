'use client'

import { signIn } from 'next-auth/react'
import { UnifiedLoginForm } from '@bizosaas/shared-ui'
import { PlatformBranding } from '@/components/ui/platform-branding'

export function ClientLoginForm() {
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
                    error: result?.error || 'Invalid credentials',
                }
            }}
        />
    )
}
