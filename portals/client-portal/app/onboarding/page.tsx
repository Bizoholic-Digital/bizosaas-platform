'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { OnboardingWizard } from '@/components/wizard/OnboardingWizard';
import { useAuth } from '@/components/auth/AuthProvider';

export default function OnboardingPage() {
    const { user, isLoading } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!isLoading && user?.onboarded) {
            router.push('/dashboard');
        }
    }, [user, isLoading, router]);

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            </div>
        );
    }

    if (!user) {
        // Redirection to login should be handled by middleware, but as a fallback:
        return null;
    }

    return <OnboardingWizard />;
}
