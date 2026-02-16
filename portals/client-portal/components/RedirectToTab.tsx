'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface RedirectToTabProps {
    tab: string;
}

/**
 * Component that redirects to the main dashboard with a specific tab query parameter
 * This prevents authentication loops by keeping the user on the same route
 */
export default function RedirectToTab({ tab }: RedirectToTabProps) {
    const router = useRouter();

    useEffect(() => {
        // Redirect to main page with tab query parameter
        router.replace(`/?tab=${tab}`);
    }, [tab, router]);

    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
                <p className="text-gray-600 dark:text-gray-400">Loading {tab}...</p>
            </div>
        </div>
    );
}
