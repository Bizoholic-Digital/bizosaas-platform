'use client';

import React, { Suspense } from 'react';
import { ConnectorsContent } from '@/components/ConnectorsContent';
import { RefreshCw } from 'lucide-react';

export default function ConnectorsPage() {
    return (
        <div className="p-6">
            <Suspense fallback={
                <div className="flex items-center justify-center p-12">
                    <RefreshCw className="h-8 w-8 animate-spin text-primary" />
                </div>
            }>
                <ConnectorsContent />
            </Suspense>
        </div>
    );
}
