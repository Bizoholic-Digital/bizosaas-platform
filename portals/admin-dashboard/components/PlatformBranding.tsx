import React from 'react';

interface PlatformBrandingProps {
    platform: string;
    size?: 'sm' | 'md' | 'lg';
}

export function PlatformBranding({ platform, size = 'md' }: PlatformBrandingProps) {
    const sizeClasses = {
        sm: 'text-xl',
        md: 'text-2xl',
        lg: 'text-4xl',
    };

    return (
        <div className="flex flex-col items-center justify-center space-y-2">
            <h1 className={`font-bold tracking-tighter ${sizeClasses[size]}`}>
                <span className="text-primary">{platform}</span>
            </h1>
        </div>
    );
}
