'use client';

import React from 'react';

/**
 * The ultimate isolation provider. 
 * If the loop persists with this, then the issue is in layout.tsx 
 * or a global library import.
 */
export function Providers({ children }: { children: React.ReactNode }) {
    return (
        <div id="providers-root">
            {children}
        </div>
    );
}
