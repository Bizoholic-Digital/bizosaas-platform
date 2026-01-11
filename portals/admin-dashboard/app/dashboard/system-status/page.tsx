'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { useSystemStatus } from '@/lib/hooks/useSystemStatus';
import { Activity, Cpu, Database, Globe, RefreshCw, Server, Shield, Zap, Brain, Users, Layout, ShoppingCart, Clock } from 'lucide-react';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

export default function SystemStatusPage() {
    const { metrics, isLoading, refreshStatus, getOverallHealth } = useSystemStatus();

    const health = getOverallHealth();

    return (
        <div className="p-6 space-y-6 bg-slate-50 dark:bg-slate-950 min-h-full">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">System Status</h1>
                    <p className="text-muted-foreground">Real-time health monitoring of all BizOSaaS services.</p>
                </div>
                <Button variant="outline" onClick={refreshStatus} disabled={isLoading}>
                    <RefreshCw className={`mr-2 h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
                    Refresh
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card className="border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                    <CardContent className="p-4 md:p-6 flex items-center">
                        <div className={`w-10 h-10 md:w-12 md:h-12 rounded-lg flex items-center justify-center bg-green-100 text-green-600`}>
                            <Activity className="h-5 w-5 md:h-6 md:w-6" />
                        </div>
                        <div className="ml-3 md:ml-4">
                            <p className="text-[10px] md:text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-tight">Core Health</p>
                            <div className="flex items-baseline gap-2">
                                <p className="text-lg md:text-2xl font-black text-slate-900 dark:text-white leading-none mt-1">{health === 'healthy' ? 'Healthy' : health}</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                    <CardContent className="p-4 md:p-6 flex items-center">
                        <div className={`w-10 h-10 md:w-12 md:h-12 rounded-lg flex items-center justify-center bg-blue-100 text-blue-600`}>
                            <Cpu className="h-5 w-5 md:h-6 md:w-6" />
                        </div>
                        <div className="ml-3 md:ml-4 flex-1">
                            <p className="text-[10px] md:text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-tight">CPU Usage</p>
                            <div className="flex items-baseline gap-2">
                                <p className="text-lg md:text-2xl font-black text-slate-900 dark:text-white leading-none mt-1">{metrics.cpu}%</p>
                            </div>
                            <Progress value={metrics.cpu} className="h-1 mt-1 w-full" />
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                    <CardContent className="p-4 md:p-6 flex items-center">
                        <div className={`w-10 h-10 md:w-12 md:h-12 rounded-lg flex items-center justify-center bg-purple-100 text-purple-600`}>
                            <Server className="h-5 w-5 md:h-6 md:w-6" />
                        </div>
                        <div className="ml-3 md:ml-4 flex-1">
                            <p className="text-[10px] md:text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-tight">Memory</p>
                            <div className="flex items-baseline gap-2">
                                <p className="text-lg md:text-2xl font-black text-slate-900 dark:text-white leading-none mt-1">{metrics.memory}%</p>
                            </div>
                            <Progress value={metrics.memory} className="h-1 mt-1 w-full" />
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                    <CardContent className="p-4 md:p-6 flex items-center">
                        <div className={`w-10 h-10 md:w-12 md:h-12 rounded-lg flex items-center justify-center bg-yellow-100 text-yellow-600`}>
                            <Zap className="h-5 w-5 md:h-6 md:w-6" />
                        </div>
                        <div className="ml-3 md:ml-4">
                            <p className="text-[10px] md:text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-tight">API Traffic</p>
                            <div className="flex items-baseline gap-2">
                                <p className="text-lg md:text-2xl font-black text-slate-900 dark:text-white leading-none mt-1">{metrics.apiRequests}</p>
                                <span className="text-[10px] text-muted-foreground hidden sm:inline-block">req/s</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                    <CardHeader>
                        <CardTitle>Service Connectivity</CardTitle>
                        <CardDescription>Individual health status for integrated core services.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {Object.entries(metrics.services)
                                .filter(([name]) => ['Brain Hub', 'CRM', 'CMS', 'E-commerce'].includes(name))
                                .map(([name, status]) => (
                                    <div key={name} className="flex items-center justify-between p-3 border rounded-lg bg-white dark:bg-slate-900 shadow-sm">
                                        <div className="flex items-center gap-3">
                                            <div className={`p-2 rounded-full ${status === 'healthy' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                                                {name === 'Brain Hub' ? <Brain className="h-5 w-5" /> :
                                                    name === 'CRM' ? <Users className="h-5 w-5" /> :
                                                        name === 'CMS' ? <Layout className="h-5 w-5" /> :
                                                            <ShoppingCart className="h-5 w-5" />}
                                            </div>
                                            <div>
                                                <p className="font-semibold text-slate-900 dark:text-white">{name}</p>
                                                <p className="text-xs text-muted-foreground">Standard Regional Latency: 45ms</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <Badge variant={status === 'healthy' ? 'default' : 'destructive'} className={status === 'healthy' ? 'bg-green-600' : 'bg-red-600'}>
                                                {status === 'healthy' ? 'Operational' : 'Disconnected'}
                                            </Badge>
                                        </div>
                                    </div>
                                ))}
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Infrastructure Health</CardTitle>
                        <CardDescription>Status of core system dependencies.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {['Vault', 'Temporal', 'Redis'].map((name) => {
                                const status = metrics.services[name] || 'down';
                                return (
                                    <div key={name} className="flex items-center justify-between p-3 border rounded-lg bg-white dark:bg-slate-900 shadow-sm">
                                        <div className="flex items-center gap-3">
                                            <div className={`p-2 rounded-full ${status === 'healthy' ? 'bg-blue-100 text-blue-700' : 'bg-slate-100 text-slate-700'}`}>
                                                {name === 'Vault' ? <Shield className="h-5 w-5" /> :
                                                    name === 'Temporal' ? <Clock className="h-5 w-5" /> :
                                                        <Database className="h-5 w-5" />}
                                            </div>
                                            <div>
                                                <p className="font-semibold text-slate-900 dark:text-white">{name}</p>
                                                <p className="text-xs text-muted-foreground">Internal Infrastructure</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <Badge variant={status === 'healthy' ? 'default' : 'destructive'} className={status === 'healthy' ? 'bg-blue-600' : 'bg-slate-600'}>
                                                {status === 'healthy' ? 'UP' : 'DOWN'}
                                            </Badge>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
