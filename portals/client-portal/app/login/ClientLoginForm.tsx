'use client'

import { signIn, getSession } from 'next-auth/react'
import { useRouter, useSearchParams } from 'next/navigation'
import { UnifiedLoginForm } from '@bizosaas/shared-ui'
import { PlatformBranding } from '@/components/ui/platform-branding'

export function ClientLoginForm() {
    const router = useRouter()
    const searchParams = useSearchParams()
    const callbackUrl = searchParams?.get('callbackUrl') || '/dashboard'

    const handleRoleBasedRedirect = async () => {
        const session = await getSession();
        // @ts-ignore
        const roles = (session?.user as any)?.roles || [];
        const role = (session?.user as any)?.role;

        const isAdmin = roles.includes('super_admin') || roles.includes('platform_admin') || roles.includes('admin') || role === 'admin';

        if (isAdmin && callbackUrl === '/dashboard') {
            // If they are an admin and didn't specify a callback, send them to admin dash
            window.location.href = 'https://admin.bizoholic.net/dashboard';
        } else {
            // Use hard redirect to ensure session cookie is picked up
            window.location.href = callbackUrl;
        }
    }

    return (
        <UnifiedLoginForm
            mode="both"
            platformName="Client Portal"
            platformSubtitle="Access your projects and services"
            ssoProviderName="BizOSaaS SSO"
            ssoProviderId="authentik"
            defaultRedirectUrl="/dashboard"
            showDemoCredentials={process.env.NODE_ENV === 'development'}
            className="!bg-transparent"
            onCredentialsLogin={async (email, password) => {
                console.log('🔄 [Client] Attempting login for:', email);
                const result = await signIn('credentials', {
                    email,
                    password,
                    redirect: false,
                    callbackUrl
                });

                console.log('✅ [Client] Sign-in result:', result);

                if (result?.ok) {
                    console.log('🚀 [Client] Success, performing role-based redirect');
                    await handleRoleBasedRedirect();
                    return { ok: true };
                }

                return {
                    ok: false,
                    error: result?.error || 'Invalid credentials',
                }
            }}
            onSSOLogin={async () => {
                // For SSO, we let NextAuth handle the redirect via callbackUrl
                await signIn('authentik', {
                    callbackUrl: callbackUrl,
                })
            }}
        />
    )
}
