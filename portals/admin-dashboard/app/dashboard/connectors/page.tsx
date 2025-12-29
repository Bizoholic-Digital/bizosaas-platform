'use client';

import React from 'react';
import { ConnectorsContent } from '@/components/ConnectorsContent';

export default function AdminConnectorsPage() {
    return (
        <div className="flex flex-col min-h-full bg-slate-50 dark:bg-slate-950 p-6 space-y-6">
            <ConnectorsContent />
        </div>
    );
}
