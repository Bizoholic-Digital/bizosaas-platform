'use client';

import React from 'react';
import { ShieldAlert, Trash2 } from 'lucide-react';

export default function GlobalError({
    error,
    reset,
}: {
    error: Error & { digest?: string };
    reset: () => void;
}) {
    const handleClearAndReload = () => {
        localStorage.clear();
        sessionStorage.clear();

        // Clear cookies
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i];
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=" + window.location.hostname;
        }

        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.getRegistrations().then(registrations => {
                for (let registration of registrations) {
                    registration.unregister();
                }
            });
        }

        window.location.href = '/';
    };

    return (
        <html>
            <body className="min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col items-center justify-center p-6 text-center font-sans">
                <div className="w-20 h-20 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mb-6">
                    <ShieldAlert className="w-10 h-10 text-red-600 dark:text-red-400" />
                </div>

                <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">
                    Critical System Error
                </h1>

                <p className="text-slate-600 dark:text-slate-400 mb-8 max-w-md mx-auto">
                    The platform encountered a critical error during initialization. This is strongly related to stale browser data from the previous system.
                </p>

                <button
                    onClick={handleClearAndReload}
                    className="flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white px-8 py-4 rounded-xl font-bold transition-all shadow-lg text-lg"
                >
                    <Trash2 className="w-6 h-6" />
                    Reset All Data & Start Fresh
                </button>

                {error.digest && (
                    <p className="mt-12 text-xs font-mono text-slate-400">
                        Error ID: {error.digest}
                    </p>
                )}
            </body>
        </html>
    );
}
