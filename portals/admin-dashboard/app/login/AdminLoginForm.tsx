'use client';

import { Suspense, useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { UnifiedLoginForm } from '@bizosaas/shared-ui';
import { PlatformBranding } from '@/components/PlatformBranding';
import { signIn } from 'next-auth/react';

export default function AdminLoginForm() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <LoginFormContent />
        </Suspense>
    );
}

function LoginFormContent() {
    const searchParams = useSearchParams();
    const callbackUrl = searchParams.get('callbackUrl') || '/dashboard';

    return (
        <UnifiedLoginForm
            mode="both"
            platformName="Admin Dashboard"
            platformSubtitle="Platform Administration & Management"
            ssoProviderName="BizOSaaS SSO"
            ssoProviderId="authentik"
            defaultRedirectUrl={callbackUrl}
            showDemoCredentials={process.env.NODE_ENV === 'development'}
            className="!bg-transparent"
            BrandingComponent={() => <PlatformBranding platform="BIZOSAAS" size="lg" />}
            onCredentialsLogin={async (email, password) => {
                try {
                    const result = await signIn("credentials", {
                        email,
                        password,
                        redirect: false,
                    });

                    if (result?.ok) {
                        window.location.href = callbackUrl;
                        return { ok: true };
                    }
                    return { ok: false, error: "Invalid credentials" };
                } catch (error) {
                    return { ok: false, error: "Authentication failed" };
                }
            }}
            onSSOLogin={async () => {
                await signIn('authentik', {
                    callbackUrl: callbackUrl,
                })
            }}
        />
    );
}
