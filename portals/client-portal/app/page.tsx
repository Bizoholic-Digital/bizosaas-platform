'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from "next-auth/react";

export default function RootPage() {
    const router = useRouter();
    const { data: session, status } = useSession();
    const isLoaded = status !== 'loading';
    const isSignedIn = status === 'authenticated';

    useEffect(() => {
        if (!isLoaded) return;

        if (isSignedIn) {
            const user = (status === 'authenticated' && session?.user) ? (session.user as any) : null;
            const onboarded = user?.onboarded;
            router.replace(onboarded ? '/dashboard' : '/onboarding');
        } else {
            router.replace('/login');
        }
    }, [isSignedIn, isLoaded, router, session, status]);

    // Show loading state while redirecting
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
            <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                <p className="text-gray-600 dark:text-gray-400">Loading...</p>
            </div>
        </div>
    );
}
