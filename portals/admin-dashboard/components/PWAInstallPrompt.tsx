'use client';

import React, { useState, useEffect, createContext, useContext } from 'react';
import { Download, X } from 'lucide-react';
import { Button } from './ui/button';

const PWAContext = createContext<{
    deferredPrompt: any;
    showInstallButton: boolean;
    install: () => Promise<void>;
    hide: () => void;
}>({
    deferredPrompt: null,
    showInstallButton: false,
    install: async () => { },
    hide: () => { },
});

export function PWAProvider({ children }: { children: React.ReactNode }) {
    const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
    const [showInstallButton, setShowInstallButton] = useState(false);

    useEffect(() => {
        const handler = (e: any) => {
            e.preventDefault();
            setDeferredPrompt(e);
            setShowInstallButton(true);
            console.log('PWA: beforeinstallprompt event fired');
        };

        window.addEventListener('beforeinstallprompt', handler);

        // Check if already installed
        if (window.matchMedia('(display-mode: standalone)').matches) {
            setShowInstallButton(false);
        }

        return () => {
            window.removeEventListener('beforeinstallprompt', handler);
        };
    }, []);

    const install = async () => {
        if (!deferredPrompt) return;
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        if (outcome === 'accepted') {
            setDeferredPrompt(null);
            setShowInstallButton(false);
        }
    };

    const hide = () => setShowInstallButton(false);

    return (
        <PWAContext.Provider value={{ deferredPrompt, showInstallButton, install, hide }}>
            {children}
        </PWAContext.Provider>
    );
}

export const usePWAInstall = () => useContext(PWAContext);

export function PWAInstallPrompt() {
    const { showInstallButton, install, hide } = usePWAInstall();

    if (!showInstallButton) return null;

    return (
        <div className="fixed bottom-6 right-6 z-50 animate-in slide-in-from-right-10 flex flex-col items-end gap-2">
            <div className="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-2xl border border-gray-100 dark:border-gray-700 max-w-xs flex flex-col gap-3">
                <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                        <h4 className="font-bold text-gray-900 dark:text-white">Install App</h4>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Get the desktop expierence with offline support.</p>
                    </div>
                    <button onClick={hide} className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full">
                        <X className="w-4 h-4 text-gray-400" />
                    </button>
                </div>
                <Button
                    onClick={install}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-lg shadow-blue-500/20"
                >
                    <Download className="w-4 h-4 mr-2" />
                    Install Now
                </Button>
            </div>
        </div>
    );
}
