'use client'

import { signIn, getSession } from 'next-auth/react'
import { useRouter, useSearchParams } from 'next/navigation'
import { UnifiedLoginForm } from '@bizosaas/shared-ui'
import { Shield } from 'lucide-react'
import { useClerk } from "@clerk/nextjs"

// Branding is now unified in the component itself

function ClerkAdminLoginForm() {
    const searchParams = useSearchParams()
    const { openSignIn } = useClerk()
    const callbackUrl = searchParams?.get('callbackUrl') || '/dashboard'

    return (
        <UnifiedLoginForm
            mode="both"
            platformName="Admin Dashboard"
            platformSubtitle="Platform Administration & Management"
            ssoProviderName="Clerk SSO"
            ssoProviderId="clerk"
            defaultRedirectUrl="/dashboard"
            showDemoCredentials={process.env.NODE_ENV === 'development'}
            className="!bg-transparent"
            onCredentialsLogin={async (email: string, password: string) => {
                console.log('🔄 [Admin] Attempting login for:', email);
                openSignIn({
                    initialValues: { emailAddress: email },
                });
                return { ok: true };
            }}
            onSSOLogin={async () => {
                console.log('🚀 [Admin] Starting Clerk SSO Flow');
                openSignIn({
                    afterSignInUrl: callbackUrl,
                    afterSignUpUrl: callbackUrl,
                });
            }}
        />
    )
}

function DefaultAdminLoginForm() {
    return (
        <div className="p-8 text-center bg-white dark:bg-slate-900 rounded-3xl shadow-xl border border-red-100 dark:border-red-900/30">
            <Shield className="w-12 h-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-2">Configuration Error</h2>
            <p className="text-slate-600 dark:text-slate-400">
                Clerk authentication is not configured. Please set <code className="text-xs bg-slate-100 dark:bg-slate-800 px-1 rounded">NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY</code>.
            </p>
        </div>
    )
}

export default function AdminLoginForm() {
    const clerkKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;
    if (clerkKey) return <ClerkAdminLoginForm />;
    return <DefaultAdminLoginForm />;
}
