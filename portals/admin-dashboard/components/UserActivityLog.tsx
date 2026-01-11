'use client';

import React, { useState, useEffect } from 'react';
import { adminApi } from '@/lib/api/admin';
import { RefreshCw, Clock, User, Shield, Key, FileText } from 'lucide-react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';

interface ActivityLogProps {
    userId?: string;
}

export function UserActivityLog({ userId }: ActivityLogProps) {
    const [logs, setLogs] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!userId) return;

        const fetchLogs = async () => {
            setLoading(true);
            try {
                const res = await adminApi.getAuditLogs(userId);
                if (res.data && Array.isArray(res.data)) {
                    setLogs(res.data);
                }
            } catch (error) {
                console.error('Failed to fetch activity logs:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchLogs();
    }, [userId]);

    const getActionIcon = (action: string) => {
        if (action.includes('LOGIN')) return <User className="w-4 h-4" />;
        if (action.includes('PERMISSION')) return <Shield className="w-4 h-4" />;
        if (action.includes('PASSWORD')) return <Key className="w-4 h-4" />;
        return <FileText className="w-4 h-4" />;
    };

    const getActionColor = (action: string) => {
        if (action.includes('LOGIN')) return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400';
        if (action.includes('PERMISSION')) return 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400';
        if (action.includes('PASSWORD')) return 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400';
        if (action.includes('DELETE')) return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400';
        return 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-400';
    };

    const formatTimestamp = (timestamp: string) => {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffMins = Math.floor(diffMs / 60000);

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <RefreshCw className="w-8 h-8 animate-spin text-blue-600" />
            </div>
        );
    }

    if (logs.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center h-full text-center space-y-2">
                <Clock className="w-12 h-12 text-muted-foreground opacity-50" />
                <p className="text-muted-foreground">No activity recorded yet</p>
                <p className="text-xs text-muted-foreground">User actions will appear here</p>
            </div>
        );
    }

    return (
        <ScrollArea className="h-full pr-4">
            <div className="space-y-3">
                {logs.map((log, idx) => (
                    <div
                        key={log.id || idx}
                        className="flex gap-3 p-3 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/50 hover:bg-slate-50 dark:hover:bg-slate-900 transition-colors"
                    >
                        <div className={`p-2 rounded-lg h-fit ${getActionColor(log.action)}`}>
                            {getActionIcon(log.action)}
                        </div>
                        <div className="flex-1 min-w-0">
                            <div className="flex items-start justify-between gap-2">
                                <div className="flex-1">
                                    <div className="font-medium text-sm">{log.action.replace(/_/g, ' ')}</div>
                                    {log.details && (
                                        <div className="text-xs text-muted-foreground mt-1">
                                            {typeof log.details === 'string'
                                                ? log.details
                                                : JSON.stringify(log.details, null, 2).substring(0, 100)
                                            }
                                        </div>
                                    )}
                                </div>
                                <div className="text-xs text-muted-foreground whitespace-nowrap">
                                    {formatTimestamp(log.created_at)}
                                </div>
                            </div>
                            {log.ip_address && (
                                <div className="text-xs text-muted-foreground mt-1">
                                    IP: {log.ip_address}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </ScrollArea>
    );
}
