'use client';

import React, { useEffect } from 'react';
import { RefreshCw, ShieldAlert, Trash2 } from 'lucide-react';

export default function GlobalError({
    error,
    reset,
}: {
    error: Error & { digest?: string };
    reset: () => void;
}) {
    useEffect(() => {
        // Log the error to an error reporting service
        console.error('Global Application Error:', error);
    }, [error]);

    const handleClearAndReload = () => {
        // Aggressively clear everything
        localStorage.clear();
        sessionStorage.clear();

        // Clear all cookies
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i];
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=" + window.location.hostname;
        }

        // Unregister service workers
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.getRegistrations().then(registrations => {
                for (let registration of registrations) {
                    registration.unregister();
                }
            });
        }

        // Hard reload
        window.location.href = '/';
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-slate-50 dark:bg-slate-900 text-center">
            <div className="w-20 h-20 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mb-6">
                <ShieldAlert className="w-10 h-10 text-red-600 dark:text-red-400" />
            </div>

            <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">
                Application Error
            </h1>

            <p className="text-slate-600 dark:text-slate-400 mb-8 max-w-md mx-auto">
                Something went wrong while loading the platform. This is often caused by outdated browser data.
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
                <button
                    onClick={() => reset()}
                    className="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold transition-all shadow-md"
                >
                    <RefreshCw className="w-4 h-4" />
                    Try Again
                </button>

                <button
                    onClick={handleClearAndReload}
                    className="flex items-center justify-center gap-2 bg-white dark:bg-slate-800 text-red-600 dark:text-red-400 border border-red-200 dark:border-red-900/50 px-6 py-3 rounded-xl font-semibold transition-all shadow-sm hover:bg-red-50 dark:hover:bg-red-900/10"
                >
                    <Trash2 className="w-4 h-4" />
                    Reset & Nuke Cache
                </button>
            </div>

            {error.digest && (
                <p className="mt-12 text-xs font-mono text-slate-400">
                    Error ID: {error.digest}
                </p>
            )}
        </div>
    );
}
