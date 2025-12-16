'use client';

import React from 'react';
import DashboardLayout from '@/components/ui/dashboard-layout';
import { useSystemStatus } from '@/lib/hooks/useSystemStatus';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Activity, CheckCircle, AlertCircle, Clock, Server, Globe, Database, Cpu } from 'lucide-react';

export default function SystemStatusPage() {
    const { metrics, isLoading } = useSystemStatus();

    return (
        <DashboardLayout title="System Status" description="Real-time service monitoring">
            <div className="p-6 space-y-6">
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Overall Status</CardTitle>
                            <Activity className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold capitalize">{metrics?.status || 'Unknown'}</div>
                            <p className="text-xs text-muted-foreground">
                                All systems {metrics?.status === 'healthy' ? 'operational' : 'monitoring'}
                            </p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Active Users</CardTitle>
                            <Globe className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{metrics?.activeUsers || 0}</div>
                            <p className="text-xs text-muted-foreground">
                                Currently online
                            </p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">API Latency</CardTitle>
                            <Server className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">24ms</div>
                            <p className="text-xs text-muted-foreground">
                                Average response time
                            </p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Error Rate</CardTitle>
                            <AlertCircle className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">0.02%</div>
                            <p className="text-xs text-muted-foreground">
                                Last 24 hours
                            </p>
                        </CardContent>
                    </Card>
                </div>

                <h2 className="text-xl font-semibold tracking-tight">Service Health</h2>
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {metrics?.services && Object.entries(metrics.services).map(([service, status]) => (
                        <Card key={service} className={status === 'down' ? 'border-red-200 bg-red-50 dark:bg-red-900/10' : ''}>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-base font-medium">{service}</CardTitle>
                                {status === 'healthy' ? (
                                    <CheckCircle className="h-4 w-4 text-green-500" />
                                ) : status === 'degraded' ? (
                                    <Activity className="h-4 w-4 text-yellow-500" />
                                ) : (
                                    <AlertCircle className="h-4 w-4 text-red-500" />
                                )}
                            </CardHeader>
                            <CardContent>
                                <div className="flex items-center gap-2 mt-2">
                                    <div className={`h-2.5 w-2.5 rounded-full ${status === 'healthy' ? 'bg-green-500' :
                                            status === 'degraded' ? 'bg-yellow-500' : 'bg-red-500'
                                        }`} />
                                    <span className="text-sm capitalize text-muted-foreground">{status}</span>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        </DashboardLayout>
    );
}
