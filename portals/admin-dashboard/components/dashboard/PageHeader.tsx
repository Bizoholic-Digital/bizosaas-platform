import React, { ReactNode } from 'react';
import { useSetHeader } from '@/lib/contexts/HeaderContext';

interface PageHeaderProps {
    title: ReactNode;
    description: ReactNode;
    children?: ReactNode; // Actions
    hideInContent?: boolean;
}

export function PageHeader({ title, description, children, hideInContent = false }: PageHeaderProps) {
    // If title and description are strings, we can sync them to the global header
    const titleStr = typeof title === 'string' ? title : "";
    const descStr = typeof description === 'string' ? description : "";

    // We only call useSetHeader if we have something to set
    // This is a bit tricky with ReactNodes, but we do our best
    useSetHeader(titleStr, descStr);

    if (hideInContent) {
        if (!children) return null;
        return (
            <div className="flex justify-end mb-6">
                <div className="flex flex-wrap gap-2 w-full md:w-auto pt-2 md:pt-0">
                    {children}
                </div>
            </div>
        );
    }

    return (
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
            <div className="space-y-1">
                {typeof title === 'string' ? (
                    <h1 className="text-3xl font-black text-slate-900 dark:text-white uppercase italic tracking-tighter">
                        {title}
                    </h1>
                ) : (
                    title
                )}
                {typeof description === 'string' ? (
                    <p className="text-slate-500 font-medium">{description}</p>
                ) : (
                    description
                )}
            </div>
            {children && (
                <div className="flex flex-wrap gap-2 w-full md:w-auto pt-2 md:pt-0">
                    {children}
                </div>
            )}
        </div>
    );
}
