'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useUser } from "@clerk/nextjs";

export default function RootPage() {
    const router = useRouter();
    const { isSignedIn, isLoaded, user } = useUser();

    useEffect(() => {
        if (!isLoaded) return; // Wait for session to load

        if (isSignedIn) {
            // Check if user has completed onboarding
            const onboarded = user?.publicMetadata?.onboarded;

            if (onboarded) {
                // User is authenticated and onboarded, redirect to dashboard
                router.replace('/dashboard');
            } else {
                // User is authenticated but NOT onboarded, redirect to onboarding
                router.replace('/onboarding');
            }
        } else {
            // User is not authenticated, redirect to login
            router.replace('/login');
        }
    }, [isSignedIn, isLoaded, user, router]);

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
