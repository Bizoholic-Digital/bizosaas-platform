'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Globe, Shield, Zap, Info, MoreHorizontal, CheckCircle, XCircle, Loader2, RefreshCw, Settings, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useSetHeader } from '@/lib/contexts/HeaderContext';
import { adminApi } from '@/lib/api/admin';

export default function IntegrationsPage() {
    useSetHeader("MCP Registry & Integrations", "Centrally manage and monitor the Model Context Protocol ecosystem.");

    const [mcps, setMcps] = useState<any[]>([]);
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    const loadData = async () => {
        setLoading(true);
        try {
            const [registryRes, statsRes] = await Promise.all([
                adminApi.getMCPRegistry(),
                adminApi.getMCPStats()
            ]);

            if (registryRes.data) {
                setMcps(registryRes.data);
            }
            if (statsRes.data) {
                setStats(statsRes.data);
            }
        } catch (error) {
            console.error("Failed to sync MCP ecosystem:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    return (
        <div className="p-6 space-y-6 bg-slate-50 dark:bg-slate-950 min-h-full">
            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-6">
                        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Global Servers</p>
                        <h3 className="text-2xl font-black mt-1">{stats?.registry_count || 0}</h3>
                        <p className="text-[10px] text-blue-500 font-bold mt-1">Platform Certified</p>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-6">
                        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Active Instances</p>
                        <h3 className="text-2xl font-black mt-1 text-emerald-600">{stats?.active_nodes || 0}</h3>
                        <p className="text-[10px] text-emerald-500/70 font-bold mt-1">Status: Operational</p>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-6">
                        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Avg. Latency</p>
                        <h3 className="text-2xl font-black mt-1">{stats?.average_latency_ms?.toFixed(1) || 0} ms</h3>
                        <p className="text-[10px] text-orange-500 font-bold mt-1">Regional: London-G1</p>
                    </CardContent>
                </Card>

                <Card className="bg-gradient-to-br from-blue-600 to-indigo-700 text-white border-none shadow-xl shadow-blue-500/20">
                    <CardContent className="p-6 relative overflow-hidden">
                        <div className="relative z-10">
                            <p className="text-[10px] font-black text-blue-100 uppercase tracking-widest">Ecosystem Health</p>
                            <h3 className="text-2xl font-black mt-1">{stats?.uptime_percentage || '99.98'}%</h3>
                            <p className="text-[10px] text-blue-200 font-bold mt-1">Cross-cluster stability</p>
                        </div>
                        <Globe className="absolute -right-4 -bottom-4 h-24 w-24 opacity-10 rotate-12" />
                    </CardContent>
                </Card>
            </div>

            <div className="flex justify-between items-center bg-white dark:bg-slate-900 p-6 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm">
                <div className="flex gap-4 items-center">
                    <div className="w-12 h-12 bg-indigo-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-indigo-500/20">
                        <Shield className="w-6 h-6" />
                    </div>
                    <div>
                        <h4 className="font-black text-gray-900 dark:text-gray-100 uppercase tracking-tight">Security & Sandboxing Policy</h4>
                        <p className="text-xs text-gray-500 font-medium max-w-lg">All MCP servers are executed in isolated, kernel-hardened containers with strict namespace separation and automated resource throttling.</p>
                    </div>
                </div>
                <div className="flex gap-2">
                    <Button size="sm" variant="outline" className="rounded-xl font-bold border-gray-100">Audit Logs</Button>
                    <Button size="sm" className="rounded-xl font-bold bg-indigo-600 hover:bg-indigo-700">Update Policy</Button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {loading ? (
                    <div className="col-span-full py-20 flex flex-col items-center justify-center bg-white rounded-3xl border border-gray-100">
                        <Loader2 className="h-10 w-10 animate-spin text-blue-600 mb-4" />
                        <p className="text-gray-500 font-bold uppercase tracking-widest text-xs">Syncing Registry Nodes...</p>
                    </div>
                ) : (
                    mcps.map((mcp) => (
                        <Card key={mcp.id} className="group border-gray-100 dark:border-gray-800 hover:border-blue-300 dark:hover:border-blue-900/50 hover:shadow-xl hover:shadow-blue-500/5 transition-all rounded-3xl overflow-hidden bg-white dark:bg-slate-900">
                            <CardHeader className="pb-2">
                                <div className="flex justify-between items-start">
                                    <div className="space-y-1">
                                        <div className="flex items-center gap-3">
                                            <CardTitle className="text-lg font-black uppercase tracking-tight text-gray-900 dark:text-gray-100">{mcp.name}</CardTitle>
                                            {mcp.is_recommended && (
                                                <Badge className="bg-emerald-500/10 text-emerald-600 border-none text-[8px] font-black uppercase tracking-widest px-1.5 h-4">
                                                    RECOMMENDED
                                                </Badge>
                                            )}
                                            <Badge className="bg-blue-500/10 text-blue-600 border-none text-[8px] font-black uppercase tracking-widest px-1.5 h-4">
                                                {mcp.source_type === 'official' ? 'OFFICIAL' : 'COMMUNITY'}
                                            </Badge>
                                        </div>
                                        <CardDescription className="text-[10px] font-bold text-gray-400">mcp://{mcp.slug}</CardDescription>
                                    </div>
                                    <div className="flex flex-col items-end gap-1">
                                        <div className="text-[10px] font-black text-gray-400 uppercase">Quality Score</div>
                                        <div className={`text-xl font-black ${mcp.quality_score >= 80 ? 'text-emerald-500' : mcp.quality_score >= 50 ? 'text-amber-500' : 'text-slate-400'}`}>
                                            {mcp.quality_score}%
                                        </div>
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent className="pt-2">
                                <div className="flex flex-wrap items-center gap-1.5 mb-4">
                                    {mcp.tags?.slice(0, 5).map((tag: string) => (
                                        <Badge key={tag} variant="outline" className="text-[9px] font-bold border-gray-100 text-gray-400 uppercase tracking-tighter">{tag}</Badge>
                                    ))}
                                </div>
                                <div className="space-y-3 mb-6">
                                    <div className="flex justify-between text-[10px] font-black uppercase tracking-widest text-gray-400">
                                        <span>Installs:</span>
                                        <span className="text-gray-900 dark:text-gray-100 font-bold">{mcp.install_count}</span>
                                    </div>
                                    <div className="flex justify-between text-[10px] font-black uppercase tracking-widest text-gray-400">
                                        <span>Vendor:</span>
                                        <span className="text-gray-900 dark:text-gray-100">{mcp.vendor || 'Platform'}</span>
                                    </div>
                                    <div className="w-full bg-gray-100 dark:bg-gray-800 rounded-full h-1.5 mt-2 overflow-hidden">
                                        <div
                                            className={`h-1.5 rounded-full transition-all duration-1000 ${mcp.quality_score >= 80 ? 'bg-emerald-500' : mcp.quality_score >= 50 ? 'bg-amber-500' : 'bg-slate-300'}`}
                                            style={{ width: `${mcp.quality_score || 0}%` }}
                                        />
                                    </div>
                                </div>
                                <div className="flex gap-2">
                                    <Button size="sm" variant="outline" className="flex-1 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-blue-50 border-gray-100">Review</Button>
                                    <Button size="sm" className="flex-1 rounded-xl text-[10px] font-black uppercase tracking-widest bg-gray-900 hover:bg-black shadow-lg shadow-gray-200">Stats</Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))
                )}
            </div>

            {/* Approval Requests Section */}
            <div className="space-y-4">
                <div className="flex items-center gap-2 px-2">
                    <Clock className="w-5 h-5 text-amber-500" />
                    <h3 className="font-black text-lg uppercase tracking-tight text-gray-900 dark:text-gray-100">Pending MCP Approval Requests</h3>
                    <Badge variant="outline" className="ml-2 bg-amber-50 text-amber-600 border-amber-100 font-bold">New Requests</Badge>
                </div>

                <div className="bg-white dark:bg-slate-900 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm overflow-hidden">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-50 dark:bg-slate-800/50 border-b border-gray-100 dark:border-gray-800">
                                <th className="p-4 text-[10px] font-black uppercase tracking-widest text-gray-400">MCP Name</th>
                                <th className="p-4 text-[10px] font-black uppercase tracking-widest text-gray-400">Type</th>
                                <th className="p-4 text-[10px] font-black uppercase tracking-widest text-gray-400">Requested By</th>
                                <th className="p-4 text-[10px] font-black uppercase tracking-widest text-gray-400">Status</th>
                                <th className="p-4 text-[10px] font-black uppercase tracking-widest text-gray-400 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {/* Empty state or list logic here, for now mockup consistent with statsRes */}
                            <tr className="border-b border-gray-50 dark:border-gray-800/50 hover:bg-slate-50/50 transition-colors">
                                <td className="p-4">
                                    <div className="font-bold text-sm text-gray-900 dark:text-gray-100">WordPress CRM Connector</div>
                                    <div className="text-[10px] text-gray-400 font-mono">github.com/mcp/wp-crm</div>
                                </td>
                                <td className="p-4">
                                    <Badge variant="outline" className="text-[10px] font-bold border-indigo-100 text-indigo-600">AGENT_REQUEST</Badge>
                                </td>
                                <td className="p-4 text-xs font-medium text-gray-600">Agent-Prime (Tenant: 0x4f...)</td>
                                <td className="p-4">
                                    <Badge className="bg-amber-100 text-amber-700 hover:bg-amber-200 border-none text-[10px] font-black">PENDING REVIEW</Badge>
                                </td>
                                <td className="p-4 text-right">
                                    <Button size="sm" variant="ghost" className="text-blue-600 font-bold text-xs hover:bg-blue-50">Approve</Button>
                                    <Button size="sm" variant="ghost" className="text-gray-400 font-bold text-xs">Reject</Button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <div className="p-4 bg-slate-50/30 text-center">
                        <Button variant="link" className="text-xs font-bold text-gray-500 uppercase tracking-widest">View Extended Approval Queue</Button>
                    </div>
                </div>
            </div>

            <Card className="border-dashed border-2 bg-white dark:bg-slate-900 flex items-center border-gray-200 dark:border-gray-800 rounded-3xl hover:bg-slate-50 transition-colors">
                <CardContent className="h-56 flex flex-col items-center justify-center p-6 text-center w-full">
                    <div className="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mb-4 border border-gray-100 shadow-inner">
                        <Zap className="w-8 h-8 text-indigo-600" />
                    </div>
                    <h3 className="font-black text-xl uppercase tracking-tight text-gray-900 dark:text-gray-100">Initialize Custom Protocol</h3>
                    <p className="text-xs text-gray-500 font-medium max-w-sm mx-auto mb-6">Deploy a private MCP server via SSE or Stdout to extend platform intelligence.</p>
                    <Button className="font-black text-xs uppercase tracking-widest bg-blue-600 hover:bg-blue-700 rounded-xl px-8 h-12 shadow-lg shadow-blue-500/20">Register New Server</Button>
                </CardContent>
            </Card>
        </div >
    );
}
