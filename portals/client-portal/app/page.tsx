'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from "next-auth/react";

export default function RootPage() {
    const router = useRouter();
    const { status } = useSession();
    const isLoaded = status !== 'loading';
    const isSignedIn = status === 'authenticated';

    useEffect(() => {
        if (!isLoaded) return; // Wait for session to load

        if (isSignedIn) {
            router.replace('/dashboard');
        } else {
            router.replace('/login');
        }
    }, [isSignedIn, isLoaded, router]);

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
