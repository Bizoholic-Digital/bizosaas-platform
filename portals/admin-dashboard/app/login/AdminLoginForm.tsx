'use client'

import { signIn, getSession } from 'next-auth/react'
import { useRouter, useSearchParams } from 'next/navigation'
import { UnifiedLoginForm } from '@bizosaas/shared-ui'
import { Shield } from 'lucide-react'
import { useClerk } from "@clerk/nextjs"

// Branding is now unified in the component itself

export default function AdminLoginForm() {
    const router = useRouter()
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
                // For now, credentials login is handled via Clerk's openSignIn
                // since standard credentials flow via next-auth is being phased out.
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
