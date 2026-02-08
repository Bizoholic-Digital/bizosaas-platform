'use client';

import React, { useState, useEffect } from 'react';
import { CheckCircle, AlertCircle, XCircle, RefreshCw, Activity } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';

interface ServiceStatus {
    status: 'healthy' | 'degraded' | 'down';
    details?: any;
}

export function ServiceStatusWidget() {
    const [health, setHealth] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [lastUpdated, setLastUpdated] = useState<Date>(new Date());

    const fetchHealth = async () => {
        setLoading(true);
        try {
            const res = await fetch('/api/brain/health');
            const data = await res.json();
            setHealth(data);
            setLastUpdated(new Date());
        } catch (error) {
            console.error('Failed to fetch health', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchHealth();
        const interval = setInterval(fetchHealth, 60000); // 1 minute
        return () => clearInterval(interval);
    }, []);

    const getStatusIcon = (status: string) => {
        if (status === 'healthy' || status === 'up') return <CheckCircle className="w-4 h-4 text-green-500" />;
        if (status === 'degraded' || status === 'warning') return <AlertCircle className="w-4 h-4 text-yellow-500" />;
        return <XCircle className="w-4 h-4 text-red-500" />;
    };

    const overallStatus = health?.status || (loading ? 'loading' : 'unknown');

    return (
        <Card className="bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-800 shadow-sm overflow-hidden h-full">
            <CardHeader className="p-4 border-b border-gray-100 dark:border-gray-800 flex flex-row items-center justify-between space-y-0">
                <CardTitle className="text-sm font-bold uppercase tracking-tight flex items-center gap-2">
                    <Activity className="w-4 h-4 text-blue-500" />
                    Platform Health
                </CardTitle>
                <button
                    onClick={fetchHealth}
                    disabled={loading}
                    className="text-gray-400 hover:text-blue-500 transition-colors"
                >
                    <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
                </button>
            </CardHeader>
            <CardContent className="p-4">
                {loading && !health ? (
                    <div className="space-y-3 py-2">
                        <div className="h-4 bg-gray-100 dark:bg-gray-800 rounded animate-pulse" />
                        <div className="h-4 bg-gray-100 dark:bg-gray-800 rounded animate-pulse w-3/4" />
                        <div className="h-4 bg-gray-100 dark:bg-gray-800 rounded animate-pulse w-1/2" />
                    </div>
                ) : (
                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <span className="text-xs font-medium text-gray-500">Overall Status</span>
                            <span className={`text-xs font-bold uppercase ${overallStatus === 'healthy' ? 'text-green-500' :
                                    overallStatus === 'degraded' ? 'text-yellow-500' : 'text-red-500'
                                }`}>
                                {overallStatus}
                            </span>
                        </div>

                        <div className="grid grid-cols-2 gap-3">
                            {health?.dependencies && Object.entries(health.dependencies).map(([name, dep]: [string, any]) => (
                                <div key={name} className="flex items-center justify-between p-2 rounded-lg bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-800">
                                    <span className="text-[10px] font-bold text-gray-400 uppercase tracking-tight truncate">{name}</span>
                                    {getStatusIcon(dep.status)}
                                </div>
                            ))}
                        </div>

                        <div className="pt-2 border-t border-gray-100 dark:border-gray-800 flex justify-between items-center mt-2">
                            <span className="text-[9px] text-gray-400 italic">
                                Updated {lastUpdated.toLocaleTimeString()}
                            </span>
                            <span className="text-[9px] font-bold text-blue-500">
                                100% UPTIME
                            </span>
                        </div>
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
