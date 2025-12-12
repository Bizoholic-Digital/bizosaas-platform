'use client';

import React, { useState, useEffect } from 'react';
import { WifiOff } from 'lucide-react';

export function OfflineBanner() {
    const [isOnline, setIsOnline] = useState(true);

    useEffect(() => {
        // Initial check
        if (typeof navigator !== 'undefined') {
            setIsOnline(navigator.onLine);
        }

        const handleOnline = () => setIsOnline(true);
        const handleOffline = () => setIsOnline(false);

        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);

        return () => {
            window.removeEventListener('online', handleOnline);
            window.removeEventListener('offline', handleOffline);
        };
    }, []);

    if (isOnline) return null;

    return (
        <div className="fixed top-0 left-0 right-0 z-[60] bg-red-600 text-white text-center py-1 text-sm font-medium flex items-center justify-center space-x-2">
            <WifiOff className="w-4 h-4" />
            <span>You are currently offline. functionality may be limited.</span>
        </div>
    );
}
