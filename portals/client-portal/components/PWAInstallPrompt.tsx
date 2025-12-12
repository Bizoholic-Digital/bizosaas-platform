'use client';

import React, { useState, useEffect } from 'react';
import { Download, X } from 'lucide-react';

export function PWAInstallPrompt() {
    const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
    const [showPrompt, setShowPrompt] = useState(false);

    useEffect(() => {
        const handler = (e: any) => {
            e.preventDefault();
            setDeferredPrompt(e);
            setShowPrompt(true);
        };

        window.addEventListener('beforeinstallprompt', handler);

        return () => {
            window.removeEventListener('beforeinstallprompt', handler);
        };
    }, []);

    const handleInstallClick = async () => {
        if (!deferredPrompt) return;

        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;

        if (outcome === 'accepted') {
            setDeferredPrompt(null);
        }
        setShowPrompt(false);
    };

    if (!showPrompt) return null;

    return (
        <div className="fixed bottom-4 left-4 z-50 bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 flex items-center space-x-4 animate-in slide-in-from-bottom">
            <div className="flex-1">
                <h4 className="font-semibold text-gray-900 dark:text-white">Install App</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">Install BizOSaaS for a better experience</p>
            </div>
            <div className="flex items-center space-x-2">
                <button
                    onClick={() => setShowPrompt(false)}
                    className="p-2 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
                >
                    <X className="w-5 h-5" />
                </button>
                <button
                    onClick={handleInstallClick}
                    className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-medium flex items-center space-x-2"
                >
                    <Download className="w-4 h-4" />
                    <span>Install</span>
                </button>
            </div>
        </div>
    );
}
