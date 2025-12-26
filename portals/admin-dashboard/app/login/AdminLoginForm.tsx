'use client'

import { signIn, getSession } from 'next-auth/react'
import { useRouter, useSearchParams } from 'next/navigation'
import { UnifiedLoginForm } from '@bizosaas/shared-ui'
import { Shield } from 'lucide-react'

// Simple branding component for admin
const AdminBranding = () => (
    <div className="flex flex-col items-center">
        <div className="p-3 bg-blue-600 rounded-xl shadow-lg mb-2">
            <Shield className="w-8 h-8 text-white" />
        </div>
        <span className="text-sm font-bold tracking-wider text-slate-400 uppercase">System Administration</span>
    </div>
)

export default function AdminLoginForm() {
    const router = useRouter()
    const searchParams = useSearchParams()
    const callbackUrl = searchParams?.get('callbackUrl') || '/dashboard'

    return (
        <UnifiedLoginForm
            mode="both"
            platformName="Admin Dashboard"
            platformSubtitle="Platform-Wide Intelligence & Oversight"
            ssoProviderName="BizOSaaS SSO"
            ssoProviderId="authentik"
            defaultRedirectUrl="/dashboard"
            showDemoCredentials={process.env.NODE_ENV === 'development'}
            className="!bg-transparent"
            BrandingComponent={AdminBranding}
            onCredentialsLogin={async (email, password) => {
                console.log('🔄 [Admin] Attempting login for:', email);
                const result = await signIn('credentials', {
                    email,
                    password,
                    redirect: false,
                    callbackUrl
                });

                console.log('✅ [Admin] Sign-in result:', result);

                if (result?.ok) {
                    console.log('🚀 [Admin] Success, hard redirect to dashboard');
                    window.location.href = callbackUrl;
                    return { ok: true };
                }

                return {
                    ok: false,
                    error: result?.error === 'CredentialsSignin' ? 'Invalid admin credentials' : (result?.error || 'Login failed'),
                }
            }}
            onSSOLogin={async () => {
                await signIn('authentik', {
                    callbackUrl: callbackUrl,
                })
            }}
        />
    )
}
