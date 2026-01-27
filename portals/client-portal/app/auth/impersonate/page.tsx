'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { RefreshCw } from 'lucide-react';

export const dynamic = 'force-dynamic';

export default function ImpersonatePage() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const [status, setStatus] = useState('Initializing impersonation session...');

    useEffect(() => {
        const token = searchParams.get('token');

        if (!token) {
            setStatus('Error: No impersonation token provided.');
            return;
        }

        const setupImpersonation = async () => {
            try {
                setStatus('Authenticated. Setting up session...');

                // Store the token in a way your app's auth provider (or custom logic) can pick it up.
                // Since this is a custom token, we might need to store it in localStorage 
                // and have the API client check for it, OR set a cookie if the backend expects that.
                // 
                // For this implementation, we'll use localStorage which 'brain-api.ts' 
                // should be updated to check, or we force a reload.

                // NOTE: This relies on the fact that we modify 'brain-api.ts' or the Auth provider 
                // to prioritize this token if present.
                // However, standard Clerk auth might fight this.
                // Ideally, we exchange this token for a session cookie or similar.

                // Simple approach: Store in localStorage key that our API client checks
                localStorage.setItem('impersonation_token', token);

                // Redirect to dashboard
                setStatus('Redirecting to dashboard...');
                setTimeout(() => {
                    router.push('/dashboard');
                }, 1000);

            } catch (e) {
                console.error(e);
                setStatus('Failed to start impersonation session.');
            }
        };

        setupImpersonation();
    }, [searchParams, router]);

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-slate-50 dark:bg-slate-900">
            <div className="p-8 bg-white dark:bg-slate-800 rounded-lg shadow-lg text-center space-y-4 max-w-md w-full border border-slate-200 dark:border-slate-700">
                <RefreshCw className="w-12 h-12 text-blue-600 animate-spin mx-auto" />
                <h1 className="text-xl font-bold">Impersonating User</h1>
                <p className="text-muted-foreground">{status}</p>

                <div className="text-xs text-amber-600 bg-amber-50 dark:bg-amber-900/20 p-3 rounded mt-4">
                    ⚠️ You are entering "View As" mode. Any actions you take will be recorded as this user.
                </div>
            </div>
        </div>
    );
}
