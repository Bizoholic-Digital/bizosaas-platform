'use client'

import { signIn, getSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { UnifiedLoginForm } from '@bizosaas/shared-ui'
import { PlatformBranding } from '@/components/ui/platform-branding'

export function ClientLoginForm() {
    const router = useRouter()

    const handleRoleBasedRedirect = async () => {
        const session = await getSession();
        // @ts-ignore
        const role = (session?.user as any)?.role;

        if (role === 'super_admin' || role === 'platform_admin') {
            // Redirect to Admin Dashboard
            window.location.href = process.env.NEXT_PUBLIC_ADMIN_URL || 'https://admin.bizoholic.net';
        } else {
            // Use hard redirect to ensure session cookie is picked up
            window.location.href = '/dashboard';
        }
    }

    return (
        <UnifiedLoginForm
            mode="credentials"
            platformName="Client Portal"
            platformSubtitle="Access your projects and services"
            defaultRedirectUrl="/dashboard"
            showDemoCredentials={process.env.NODE_ENV === 'development'}
            className="!bg-transparent"
            BrandingComponent={() => <PlatformBranding platform="BIZOHOLIC" size="lg" />}
            onCredentialsLogin={async (email, password) => {
                const result = await signIn('credentials', {
                    email,
                    password,
                    redirect: false,
                })

                if (result?.ok) {
                    await handleRoleBasedRedirect();
                }

                return {
                    ok: result?.ok || false,
                    error: result?.error || 'Invalid credentials',
                }
            }}
        />
    )
}
