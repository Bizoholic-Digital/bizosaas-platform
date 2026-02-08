'use client';

import React, { useState } from 'react';
import AdminSettingsLayout from '@/components/settings/AdminSettingsLayout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Database,
    Server,
    Zap,
    Globe,
    Cloud,
    Cpu,
    Shield,
    HardDrive,
    Save,
    Activity,
    Box,
    Terminal,
    RefreshCw
} from 'lucide-react';
import { toast } from 'sonner';

export default function InfrastructureSettingsPage() {
    const [isSyncing, setIsSyncing] = useState(false);

    const handleSync = () => {
        setIsSyncing(true);
        setTimeout(() => {
            setIsSyncing(false);
            toast.success("Infrastructure topology synced successfully!");
        }, 2000);
    };

    return (
        <AdminSettingsLayout>
            <div className="space-y-8 animate-in fade-in duration-500">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <h1 className="text-3xl font-black text-slate-900 dark:text-white uppercase italic tracking-tighter">
                            Infrastructure <span className="text-indigo-600">Stack</span>
                        </h1>
                        <p className="text-slate-500 font-medium flex items-center gap-2">
                            <Server className="w-4 h-4 text-indigo-500" />
                            Cluster connection strings and resource endpoints
                        </p>
                    </div>
                    <div className="flex items-center gap-2">
                        <Button variant="outline" size="sm" className="border-slate-200 dark:border-slate-800" onClick={handleSync} disabled={isSyncing}>
                            <RefreshCw className={`w-4 h-4 mr-2 ${isSyncing ? 'animate-spin' : ''}`} />
                            Sync Topology
                        </Button>
                        <Button size="sm" className="bg-slate-900 hover:bg-slate-800 text-white dark:bg-slate-800 dark:hover:bg-slate-700">
                            <Terminal className="w-4 h-4 mr-2" />
                            SSH Access
                        </Button>
                    </div>
                </div>

                <div className="grid grid-cols-1 gap-6">
                    {/* Database Layer */}
                    <Card className="border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden bg-white dark:bg-slate-900">
                        <CardHeader className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/50">
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-indigo-100 dark:bg-indigo-900/30 rounded-xl">
                                    <Database className="w-5 h-5 text-indigo-600" />
                                </div>
                                <div>
                                    <CardTitle className="text-lg font-black uppercase italic tracking-tighter">Database Layer</CardTitle>
                                    <CardDescription className="text-[10px] uppercase font-bold tracking-widest text-slate-400">PostgreSQL & Redis connection parameters</CardDescription>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="p-6 space-y-6">
                            <div className="space-y-4">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label className="text-[10px] font-black uppercase text-slate-500">Postgres Master Host</Label>
                                        <Input defaultValue="pg-master.bizosaas.internal" className="h-10 bg-slate-50 dark:bg-slate-800 font-bold font-mono text-xs" />
                                    </div>
                                    <div className="space-y-2">
                                        <Label className="text-[10px] font-black uppercase text-slate-500">Postgres Port</Label>
                                        <Input defaultValue="5432" className="h-10 bg-slate-50 dark:bg-slate-800 font-bold font-mono text-xs" />
                                    </div>
                                </div>
                                <div className="space-y-2 border-t pt-4">
                                    <Label className="text-[10px] font-black uppercase text-slate-500 flex items-center gap-2">
                                        <Zap className="w-3 h-3 text-amber-500" />
                                        Redis Cluster Nodes
                                    </Label>
                                    <Input defaultValue="redis-01:6379, redis-02:6379, redis-03:6379" className="h-10 bg-slate-50 dark:bg-slate-800 font-bold font-mono text-xs" />
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Compute & API */}
                    <Card className="border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden bg-white dark:bg-slate-900">
                        <CardHeader className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/50">
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-xl">
                                    <Cpu className="w-5 h-5 text-purple-600" />
                                </div>
                                <div>
                                    <CardTitle className="text-lg font-black uppercase italic tracking-tighter">Compute & API</CardTitle>
                                    <CardDescription className="text-[10px] uppercase font-bold tracking-widest text-slate-400">Brain Gateway and AI Engine endpoints</CardDescription>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="p-6 space-y-4">
                            <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800/50 rounded-2xl border border-slate-100 dark:border-slate-800">
                                <div className="flex items-center gap-4">
                                    <div className="p-2 bg-blue-100 dark:bg-blue-900/40 rounded-lg text-blue-600 font-black text-xs">API</div>
                                    <div>
                                        <span className="text-xs font-black uppercase tracking-tight text-slate-900 dark:text-slate-200">Brain Gateway Endpoint</span>
                                        <p className="text-[10px] text-slate-500 font-mono">https://brain.bizosaas.internal</p>
                                    </div>
                                </div>
                                <Badge className="bg-emerald-500 text-white border-none italic">ONLINE</Badge>
                            </div>

                            <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800/50 rounded-2xl border border-slate-100 dark:border-slate-800">
                                <div className="flex items-center gap-4">
                                    <div className="p-2 bg-purple-100 dark:bg-purple-900/40 rounded-lg text-purple-600 font-black text-xs">AI</div>
                                    <div>
                                        <span className="text-xs font-black uppercase tracking-tight text-slate-900 dark:text-slate-200">Ollama Inference Host</span>
                                        <p className="text-[10px] text-slate-500 font-mono">http://ollama-compute:11434</p>
                                    </div>
                                </div>
                                <Badge className="bg-amber-500 text-white border-none italic">BUSY (88%)</Badge>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </AdminSettingsLayout>
    );
}
