'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
    Layout,
    Globe,
    Shield,
    Zap,
    RefreshCw,
    ExternalLink,
    AlertCircle,
    CheckCircle2,
    Download,
    Terminal,
    Wrench,
    Plus
} from 'lucide-react';
import { adminApi } from '@/lib/api/admin';
import { toast } from 'sonner';
import { PageHeader } from '@/components/dashboard/PageHeader';

export default function CMSOverwatchPage() {
    const [sites, setSites] = useState<any[]>([]);
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    const loadData = async () => {
        setLoading(true);
        try {
            const [sitesRes, statsRes] = await Promise.all([
                adminApi.getCMSSites(),
                adminApi.getCMSPluginStats()
            ]);

            if (sitesRes.data) setSites(sitesRes.data);
            if (statsRes.data) setStats(statsRes.data);
        } catch (error) {
            console.error("Failed to sync CMS fleet:", error);
            toast.error("Telemetry link lost with WordPress fleet");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const triggerBulkDeploy = async (version: string) => {
        try {
            const res = await adminApi.deployCMSPlugin(version);
            if (!res.error) toast.success(`Deployment of v${version} started across fleet`);
            else toast.error("Deployment failed: " + res.error);
        } catch (e) {
            toast.error("Internal deployment error");
        }
    };

    return (
        <div className="p-6 space-y-8 bg-slate-50 dark:bg-slate-950 min-h-full">
            <PageHeader
                title={<>CMS <span className="text-indigo-600">Overwatch</span></>}
                description="Global administration of the BizOSaaS WordPress fleet and BizoConnect plugin distribution."
            >
                <Button variant="outline" className="rounded-xl border-dashed">
                    <Download className="mr-2 h-4 w-4" /> Export Asset List
                </Button>
                <Button onClick={loadData} className="bg-indigo-600 hover:bg-indigo-700 rounded-xl" disabled={loading}>
                    <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Fleet Sync
                </Button>
            </PageHeader>

            {/* Plugin Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm relative overflow-hidden">
                    <CardContent className="p-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Global Plugin Drift</p>
                                <h3 className="text-3xl font-black mt-1">{stats?.latest_version || '1.2.5'}</h3>
                                <p className="text-xs font-bold text-emerald-600 mt-1">Latest Version Active</p>
                            </div>
                            <div className="w-12 h-12 bg-indigo-50 dark:bg-indigo-900/20 rounded-2xl flex items-center justify-center text-indigo-600">
                                <Zap className="w-6 h-6" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Active Fleet Capacity</p>
                                <h3 className="text-3xl font-black mt-1">{sites.length} SITES</h3>
                                <p className="text-xs font-bold text-slate-400 mt-1">Cross-tenant distribution</p>
                            </div>
                            <div className="w-12 h-12 bg-emerald-50 dark:bg-emerald-900/20 rounded-2xl flex items-center justify-center text-emerald-600">
                                <Globe className="w-6 h-6" />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 text-white border-none shadow-xl relative overflow-hidden group">
                    <div className="relative z-10 p-6">
                        <p className="text-[10px] font-black text-indigo-400 uppercase tracking-widest">Fleet Orchestration</p>
                        <h3 className="text-xl font-black mt-2 italic uppercase">Bulk Plugin Update</h3>
                        <div className="mt-4 space-y-2">
                            <Button
                                size="sm"
                                className="w-full bg-white/10 hover:bg-indigo-600 text-white font-black text-[10px] uppercase tracking-widest rounded-xl transition-all"
                                onClick={() => triggerBulkDeploy(stats?.latest_version || "1.2.5")}
                            >
                                Trigger Rollout
                            </Button>
                        </div>
                    </div>
                    <Terminal className="absolute -right-4 -bottom-4 h-24 w-24 opacity-10 rotate-12" />
                </Card>
            </div>

            {/* Site Grid */}
            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <h2 className="text-xl font-black text-slate-900 dark:text-white uppercase italic tracking-tighter flex items-center gap-2">
                        <Layout className="w-6 h-6 text-indigo-600" />
                        Connected <span className="text-indigo-600">Fleet</span>
                    </h2>
                    <div className="flex gap-2">
                        <Badge variant="outline" className="font-bold border-slate-200">INTERNAL CLUSTER</Badge>
                        <Badge className="bg-blue-600 font-bold uppercase text-[9px]">v1.2.0 STABLE</Badge>
                    </div>
                </div>

                <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-100 dark:border-slate-800 shadow-sm overflow-hidden">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="bg-slate-50/50 dark:bg-slate-800/50">
                                <th className="p-4 text-[10px] font-black uppercase tracking-widest text-slate-400">Tenant Identity</th>
                                <th className="p-4 text-[10px] font-black uppercase tracking-widest text-slate-400">Site Endpoint</th>
                                <th className="p-4 text-[10px] font-black uppercase tracking-widest text-slate-400">Plugin State</th>
                                <th className="p-4 text-[10px] font-black uppercase tracking-widest text-slate-400">Platform</th>
                                <th className="p-4 text-[10px] font-black uppercase tracking-widest text-slate-400">Connection</th>
                                <th className="p-4 text-[10px] font-black uppercase tracking-widest text-slate-400 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sites.map((site, i) => (
                                <tr key={i} className="border-t border-slate-50 dark:border-slate-800 hover:bg-slate-50/30 transition-colors">
                                    <td className="p-4">
                                        <div className="flex flex-col">
                                            <span className="text-sm font-black italic">{site.tenant_name}</span>
                                            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-tighter cursor-pointer hover:text-indigo-600 transition-colors">{site.tenant_id.slice(0, 8)}</span>
                                        </div>
                                    </td>
                                    <td className="p-4">
                                        <div className="flex items-center gap-2 text-xs font-bold text-slate-600 dark:text-slate-300">
                                            <span className="truncate max-w-[200px]">{site.site_url}</span>
                                            <ExternalLink className="w-3 h-3 text-slate-400" />
                                        </div>
                                    </td>
                                    <td className="p-4">
                                        <Badge className="bg-emerald-500/10 text-emerald-600 border-none text-[9px] font-black">v1.2.5 (OK)</Badge>
                                    </td>
                                    <td className="p-4 text-xs font-bold uppercase text-indigo-600">{site.platform}</td>
                                    <td className="p-4">
                                        <div className="flex items-center gap-1.5">
                                            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                                            <span className="text-[10px] font-black text-slate-400 uppercase">ACTIVE</span>
                                        </div>
                                    </td>
                                    <td className="p-4 text-right">
                                        <div className="flex justify-end gap-2">
                                            <Button size="icon" variant="ghost" className="h-8 w-8 rounded-lg hover:bg-indigo-50 hover:text-indigo-600"><Terminal className="h-4 w-4" /></Button>
                                            <Button size="icon" variant="ghost" className="h-8 w-8 rounded-lg hover:bg-emerald-50 hover:text-emerald-600"><RefreshCw className="h-4 w-4" /></Button>
                                            <Button size="icon" variant="ghost" className="h-8 w-8 rounded-lg hover:bg-slate-100"><Wrench className="h-4 w-4" /></Button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                            {sites.length === 0 && (
                                <tr>
                                    <td colSpan={6} className="p-20 text-center">
                                        <AlertCircle className="w-12 h-12 text-slate-200 mx-auto mb-4" />
                                        <p className="text-slate-400 font-black uppercase tracking-widest text-xs">No WordPress assets detected</p>
                                        <p className="text-[10px] text-slate-300 font-bold mt-1 uppercase">Sites connected via ZipWP or WP Connector will appear here.</p>
                                        <Button size="sm" variant="outline" className="mt-6 rounded-xl font-black text-[10px] uppercase tracking-widest border-dashed">
                                            <Plus className="w-3 h-3 mr-2" /> Simulate Deployment
                                        </Button>
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
