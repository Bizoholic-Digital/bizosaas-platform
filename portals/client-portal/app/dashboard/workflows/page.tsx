'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
    Zap,
    RefreshCw,
    CheckCircle2,
    Clock,
    AlertCircle,
    ExternalLink,
    Play,
    Pause,
    Settings2,
    History,
    Activity,
    Cpu,
    Shield
} from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { toast } from 'sonner';

// Mock workflow data
const MOCK_WORKFLOWS = [
    {
        id: 'wf_001',
        name: 'Marketing Email Sequence',
        type: 'Marketing',
        status: 'running',
        lastRun: '2024-03-20T10:30:00Z',
        successRate: 98.5,
        runsToday: 12,
        description: 'Automates welcome sequence and follow-ups for new leads.'
    },
    {
        id: 'wf_002',
        name: 'Shopify Inventory Sync',
        type: 'E-commerce',
        status: 'paused',
        lastRun: '2024-03-20T08:15:00Z',
        successRate: 100,
        runsToday: 4,
        description: 'Updates product levels between Shopify and local database every 15 minutes.'
    },
    {
        id: 'wf_003',
        name: 'SEO Meta Generator',
        type: 'Content',
        status: 'running',
        lastRun: '2024-03-20T11:00:00Z',
        successRate: 94.2,
        runsToday: 45,
        description: 'AI-powered meta description generation for new WordPress posts.'
    },
    {
        id: 'wf_004',
        name: 'Customer Health Monitor',
        type: 'Analytics',
        status: 'running',
        lastRun: '2024-03-20T11:45:00Z',
        successRate: 99.9,
        runsToday: 1,
        description: 'Daily analysis of customer engagement and churn risk detection.'
    }
];

export default function WorkflowsPage() {
    const [workflows, setWorkflows] = useState(MOCK_WORKFLOWS);
    const [isLoading, setIsLoading] = useState(false);

    const handleToggleStatus = (id: string) => {
        setWorkflows(prev => prev.map(wf => {
            if (wf.id === id) {
                const newStatus = wf.status === 'running' ? 'paused' : 'running';
                toast.success(`${wf.name} ${newStatus === 'running' ? 'resumed' : 'paused'}`);
                return { ...wf, status: newStatus };
            }
            return wf;
        }));
    };

    const handleRefresh = () => {
        setIsLoading(true);
        setTimeout(() => {
            setIsLoading(false);
            toast.success("Workflow statuses updated");
        }, 1000);
    };

    return (
        <div className="p-3 md:p-6 space-y-4 md:space-y-6 max-w-7xl mx-auto overflow-x-hidden">
            {/* Status Bar */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div className="flex items-center gap-2">
                    <div className="flex -space-x-2">
                        {[1, 2, 3].map(i => (
                            <div key={i} className="h-6 w-6 md:h-8 md:w-8 rounded-full border-2 border-white dark:border-slate-900 bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
                                <Cpu className="h-3 w-3 md:h-4 md:w-4 text-emerald-600 dark:text-emerald-400" />
                            </div>
                        ))}
                    </div>
                    <div className="text-[10px] md:text-sm font-medium">
                        <span className="text-emerald-600 dark:text-emerald-400">3 Active Workers</span>
                        <span className="text-slate-400 mx-2 md:mx-4 tracking-tighter">|</span>
                        <span className="text-slate-500">System Healthy</span>
                    </div>
                </div>

                <div className="grid grid-cols-2 md:flex gap-2 w-full md:w-auto">
                    <Button variant="outline" size="sm" onClick={handleRefresh} disabled={isLoading} className="text-[10px] md:text-xs">
                        <RefreshCw className={`mr-1 md:mr-2 h-3 w-3 md:h-4 md:w-4 ${isLoading ? 'animate-spin' : ''}`} />
                        Refresh
                    </Button>
                    <Button size="sm" className="bg-purple-600 hover:bg-purple-700 text-[10px] md:text-xs">
                        <Zap className="mr-1 md:mr-2 h-3 w-3 md:h-4 md:w-4" />
                        New Workflow
                    </Button>
                </div>
            </div>

            {/* Summary Metrics */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
                {[
                    { label: 'Total', value: '24', icon: Activity, color: 'text-blue-600', bg: 'bg-blue-50' },
                    { label: 'Success', value: '1.2k', icon: CheckCircle2, color: 'text-emerald-600', bg: 'bg-emerald-50' },
                    { label: 'Errors', value: '3', icon: AlertCircle, color: 'text-red-600', bg: 'bg-red-50' },
                    { label: 'Latency', value: '45ms', icon: Clock, color: 'text-purple-600', bg: 'bg-purple-50' },
                ].map((m, i) => (
                    <Card key={i} className="border-none shadow-sm bg-white dark:bg-slate-900/50">
                        <CardContent className="p-3 md:p-6 flex items-center justify-between">
                            <div>
                                <p className="text-[10px] md:text-sm text-muted-foreground font-bold uppercase tracking-tight">{m.label}</p>
                                <h3 className="text-lg md:text-2xl font-black mt-1 leading-none">{m.value}</h3>
                            </div>
                            <div className={`p-2 md:p-3 rounded-lg md:rounded-xl ${m.bg} dark:bg-slate-800 ${m.color}`}>
                                <m.icon className="h-4 w-4 md:h-5 md:w-5" />
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            <Tabs defaultValue="active" className="w-full">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-4">
                    <TabsList className="bg-slate-100/50 dark:bg-slate-800/50 p-1 rounded-xl">
                        <TabsTrigger value="active" className="text-xs md:text-sm rounded-lg">Active</TabsTrigger>
                        <TabsTrigger value="history" className="text-xs md:text-sm rounded-lg">History</TabsTrigger>
                        <TabsTrigger value="workers" className="text-xs md:text-sm rounded-lg">Nodes</TabsTrigger>
                    </TabsList>

                    <a
                        href="https://temporal.bizoholic.net"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[10px] text-purple-600 hover:text-purple-700 flex items-center gap-1.5 font-bold bg-purple-50 dark:bg-purple-900/20 px-3 py-2 rounded-lg transition-colors"
                    >
                        <Shield className="h-3 w-3" />
                        Temporal Cloud
                        <ExternalLink className="h-3 w-3" />
                    </a>
                </div>

                <TabsContent value="active" className="mt-0">
                    <div className="grid grid-cols-1 gap-4">
                        {workflows.map(wf => (
                            <Card key={wf.id} className="group hover:shadow-md transition-all border-slate-100 dark:border-slate-800">
                                <CardContent className="p-0">
                                    <div className="flex flex-col md:flex-row items-center p-5 gap-6">
                                        <div className={`h-10 w-10 md:h-12 md:w-12 rounded-lg md:rounded-xl flex items-center justify-center shrink-0 ${wf.status === 'running'
                                            ? 'bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600'
                                            : 'bg-amber-50 dark:bg-amber-900/20 text-amber-600'
                                            }`}>
                                            {wf.status === 'running' ? <RefreshCw className="h-5 w-5 md:h-6 md:w-6 animate-[spin_4s_linear_infinite]" /> : <Pause className="h-5 w-5 md:h-6 md:w-6" />}
                                        </div>

                                        <div className="flex-1 space-y-1">
                                            <div className="flex items-center gap-2">
                                                <h3 className="text-lg font-semibold">{wf.name}</h3>
                                                <Badge variant="outline" className="text-[10px] uppercase font-bold tracking-wider">
                                                    {wf.type}
                                                </Badge>
                                                {wf.status === 'running' && (
                                                    <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                                                )}
                                            </div>
                                            <p className="text-sm text-muted-foreground line-clamp-1">{wf.description}</p>
                                        </div>

                                        <div className="hidden lg:grid grid-cols-3 gap-8 px-6 border-x border-slate-100 dark:border-slate-800">
                                            <div className="text-center">
                                                <p className="text-[10px] text-muted-foreground font-bold uppercase mb-1">Success Rate</p>
                                                <p className="text-sm font-semibold text-emerald-600">{wf.successRate}%</p>
                                            </div>
                                            <div className="text-center">
                                                <p className="text-[10px] text-muted-foreground font-bold uppercase mb-1">Runs Today</p>
                                                <p className="text-sm font-semibold">{wf.runsToday}</p>
                                            </div>
                                            <div className="text-center">
                                                <p className="text-[10px] text-muted-foreground font-bold uppercase mb-1">Last Sync</p>
                                                <p className="text-sm font-semibold text-slate-500">{new Date(wf.lastRun).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
                                            </div>
                                        </div>

                                        <div className="flex items-center gap-2">
                                            <Button size="sm" variant="ghost" onClick={() => handleToggleStatus(wf.id)}>
                                                {wf.status === 'running' ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                                            </Button>
                                            <Button size="sm" variant="outline">
                                                <Settings2 className="h-4 w-4 mr-2" />
                                                Config
                                            </Button>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </TabsContent>

                <TabsContent value="history">
                    <Card className="border-dashed border-2">
                        <CardContent className="h-64 flex flex-col items-center justify-center text-muted-foreground">
                            <History className="h-10 w-10 mb-4 opacity-20" />
                            <p>Viewing historical executions for the last 30 days...</p>
                            <Button variant="link" className="mt-2 text-purple-600">Download CSV Log</Button>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="workers">
                    <Card className="border-dashed border-2">
                        <CardContent className="h-64 flex flex-col items-center justify-center text-muted-foreground">
                            <Cpu className="h-10 w-10 mb-4 opacity-20" />
                            <p>Worker orchestration is handled by the Brain Gateway.</p>
                            <p className="text-sm">Currently 3 healthy nodes distributed across US regions.</p>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>

            {/* Recommendation Box */}
            <div className="bg-purple-50 dark:bg-purple-900/10 border border-purple-100 dark:border-purple-800/20 rounded-2xl p-6 mt-8">
                <div className="flex gap-4">
                    <div className="h-10 w-10 bg-purple-100 dark:bg-purple-900/40 rounded-full flex items-center justify-center shrink-0">
                        <Zap className="h-5 w-5 text-purple-600" />
                    </div>
                    <div>
                        <h4 className="font-bold text-purple-900 dark:text-purple-100">AI-Powered Suggestion</h4>
                        <p className="text-sm text-purple-800 dark:text-purple-300 mt-1 leading-relaxed">
                            Your "Marketing Email Sequence" has a slight drop in success rate (98.5%) due to 2 bounce errors this morning.
                            We recommend enabling the "Automatic Lead Cleaning" workflow to filter invalid emails before execution.
                        </p>
                        <Button size="sm" variant="link" className="text-purple-700 dark:text-purple-400 p-0 h-auto mt-2 font-bold group">
                            Optimize Workflow <ExternalLink className="ml-1 h-3 w-3 group-hover:translate-x-0.5 transition-transform" />
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
}
