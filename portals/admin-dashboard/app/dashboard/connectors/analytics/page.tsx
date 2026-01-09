'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    LineChart, Line, AreaChart, Area, PieChart, Pie, Cell
} from 'recharts';
import {
    Globe,
    Zap,
    Activity,
    AlertTriangle,
    CheckCircle2,
    Clock,
    TrendingUp,
    TrendingDown,
    RefreshCw,
    Search,
    Filter,
    Download,
    Share2
} from 'lucide-react';

const connectorTrafficData = [
    { time: '00:00', requests: 450, failures: 2 },
    { time: '04:00', requests: 320, failures: 1 },
    { time: '08:00', requests: 1200, failures: 15 },
    { time: '12:00', requests: 2500, failures: 42 },
    { time: '16:00', requests: 1800, failures: 20 },
    { time: '20:00', requests: 900, failures: 5 },
    { time: '23:59', requests: 600, failures: 3 },
];

const connectorUsageData = [
    { name: 'Google Workspace', calls: 45000, value: 400, color: '#4285F4' },
    { name: 'Mailchimp', calls: 32000, value: 300, color: '#FFE01B' },
    { name: 'WooCommerce', calls: 28000, value: 300, color: '#96588A' },
    { name: 'Slack', calls: 24000, value: 200, color: '#4A154B' },
    { name: 'Stripe', calls: 18000, value: 200, color: '#635BFF' },
    { name: 'HubSpot', calls: 12000, value: 100, color: '#FF7A59' },
];

export default function ConnectorAnalyticsPage() {
    const [isRefreshing, setIsRefreshing] = useState(false);

    const handleRefresh = () => {
        setIsRefreshing(true);
        setTimeout(() => setIsRefreshing(false), 1500);
    };

    return (
        <div className="p-4 md:p-8 space-y-8 bg-slate-50 dark:bg-slate-950 min-h-full pb-20">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-black text-slate-900 dark:text-white uppercase italic tracking-tighter">
                        Connector <span className="text-indigo-600">Intelligence</span>
                    </h1>
                    <p className="text-slate-500 font-medium flex items-center gap-2">
                        <Globe className="w-4 h-4 text-indigo-500" />
                        Global integration traffic, reliability, and throughput metrics
                    </p>
                </div>
                <div className="flex items-center gap-2">
                    <Button variant="outline" size="sm" className="border-slate-200 dark:border-slate-800" onClick={handleRefresh}>
                        <RefreshCw className={isRefreshing ? 'animate-spin w-4 h-4 mr-2' : 'w-4 h-4 mr-2'} />
                        Recalculate
                    </Button>
                    <Button size="sm" className="bg-indigo-600 hover:bg-indigo-700">
                        <Download className="w-4 h-4 mr-2" />
                        Export Data
                    </Button>
                </div>
            </div>

            {/* Global Pulse Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card className="border-none shadow-sm bg-white dark:bg-slate-900">
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg">
                                <Activity className="w-4 h-4 text-indigo-600" />
                            </div>
                            <Badge variant="outline" className="border-indigo-100 bg-indigo-50 text-indigo-600 text-[8px] font-black italic">LAST 24H</Badge>
                        </div>
                        <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-1">Total API Requests</p>
                        <div className="flex items-baseline gap-2">
                            <span className="text-3xl font-black italic text-slate-900 dark:text-white">1.2M</span>
                            <span className="text-xs font-bold text-emerald-500 flex items-center">
                                <TrendingUp className="w-3 h-3 mr-1" />
                                14%
                            </span>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-none shadow-sm bg-white dark:bg-slate-900">
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg">
                                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                            </div>
                            <Badge className="bg-emerald-500 text-white border-none text-[8px] font-black italic font-sans">99.8% SUCCESS</Badge>
                        </div>
                        <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-1">Global Reliability</p>
                        <div className="flex items-baseline gap-2">
                            <span className="text-3xl font-black italic text-slate-900 dark:text-white">Active</span>
                            <span className="text-[10px] font-bold text-slate-400">NO OUTAGES</span>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-none shadow-sm bg-white dark:bg-slate-900">
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-amber-50 dark:bg-amber-900/20 rounded-lg">
                                <Clock className="w-4 h-4 text-amber-600" />
                            </div>
                            <Badge variant="outline" className="border-amber-100 bg-amber-50 text-amber-600 text-[8px] font-black italic">SYSTEM AVG</Badge>
                        </div>
                        <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-1">Latency P95</p>
                        <div className="flex items-baseline gap-2">
                            <span className="text-3xl font-black italic text-slate-900 dark:text-white">450ms</span>
                            <span className="text-xs font-bold text-red-500 flex items-center">
                                <TrendingUp className="w-3 h-3 mr-1" />
                                8%
                            </span>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-none shadow-sm bg-white dark:bg-slate-900">
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                                <Zap className="w-4 h-4 text-purple-600" />
                            </div>
                            <Badge variant="outline" className="border-purple-100 bg-purple-50 text-purple-600 text-[8px] font-black italic">PEAK LOAD</Badge>
                        </div>
                        <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-1">Throughput</p>
                        <div className="flex items-baseline gap-2">
                            <span className="text-3xl font-black italic text-slate-900 dark:text-white">8.4 GB</span>
                            <span className="text-[10px] font-bold text-slate-400">DAILY EGRESS</span>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Traffic Matrix */}
                <Card className="lg:col-span-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xl overflow-hidden">
                    <CardHeader className="border-b border-slate-50 dark:border-slate-800 pb-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <CardTitle className="text-lg font-black uppercase italic tracking-tighter">Traffic Velocity Map</CardTitle>
                                <CardDescription className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Real-time request vs failure distribution</CardDescription>
                            </div>
                            <Badge className="bg-indigo-600 text-white border-none italic">LIVE FEED</Badge>
                        </div>
                    </CardHeader>
                    <CardContent className="pt-6">
                        <div className="h-[300px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={connectorTrafficData}>
                                    <defs>
                                        <linearGradient id="colorReq" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#4f46e5" stopOpacity={0.1} />
                                            <stop offset="95%" stopColor="#4f46e5" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                    <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fontSize: 10, fontWeight: 'bold' }} />
                                    <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fontWeight: 'bold' }} />
                                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '12px', color: '#fff' }} />
                                    <Area type="monotone" dataKey="requests" stroke="#4f46e5" fillOpacity={1} fill="url(#colorReq)" strokeWidth={3} />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </CardContent>
                </Card>

                {/* Top Connectors */}
                <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xl">
                    <CardHeader>
                        <CardTitle className="text-lg font-black uppercase italic tracking-tighter">Connector Share</CardTitle>
                        <CardDescription className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Market share by API invocation</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="h-[250px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={connectorUsageData}
                                        innerRadius={60}
                                        outerRadius={80}
                                        paddingAngle={5}
                                        dataKey="value"
                                    >
                                        {connectorUsageData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.color} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                        <div className="space-y-2 mt-4">
                            {connectorUsageData.slice(0, 4).map((item, i) => (
                                <div key={i} className="flex justify-between items-center text-xs font-bold">
                                    <div className="flex items-center gap-2">
                                        <div className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color }} />
                                        <span className="text-slate-600 dark:text-slate-400 uppercase tracking-tight">{item.name}</span>
                                    </div>
                                    <span className="font-black text-slate-900 dark:text-white">{(item.calls / 1000).toFixed(1)}K</span>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Reliability Leaderboard */}
            <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xl overflow-hidden">
                <CardHeader className="border-b border-slate-50 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/20">
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                        <div>
                            <CardTitle className="text-lg font-black uppercase italic tracking-tighter">Reliability Leaderboard</CardTitle>
                            <CardDescription className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Detailed connector performance matrix</CardDescription>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="relative">
                                <Search className="w-3 h-3 absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" />
                                <input className="pl-8 pr-4 py-2 border rounded-full text-[10px] font-bold bg-slate-100 dark:bg-slate-800 border-none w-48" placeholder="SEARCH CONNECTORS..." />
                            </div>
                            <Button variant="outline" size="sm" className="h-8 text-[10px] font-black uppercase border-slate-200"><Filter className="w-3 h-3 mr-1" /> Filter</Button>
                        </div>
                    </div>
                </CardHeader>
                <CardContent className="p-0">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead>
                                <tr className="border-b border-slate-50 dark:border-slate-800 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] bg-slate-50/30 dark:bg-slate-800/10">
                                    <th className="px-6 py-4">Integration Entity</th>
                                    <th className="px-6 py-4">Total Calls</th>
                                    <th className="px-6 py-4">Reliability</th>
                                    <th className="px-6 py-4">Egress Throttle</th>
                                    <th className="px-6 py-4">Last Event</th>
                                    <th className="px-6 py-4">State</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-50 dark:divide-slate-800">
                                {connectorUsageData.map((item, i) => (
                                    <tr key={i} className="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors group">
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-3">
                                                <div className="w-8 h-8 rounded-lg flex items-center justify-center border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800 shadow-sm transition-transform group-hover:scale-110">
                                                    <Globe className="w-4 h-4 text-slate-400" />
                                                </div>
                                                <span className="text-xs font-black uppercase italic tracking-tight text-slate-900 dark:text-white">{item.name}</span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 font-mono font-black text-xs text-indigo-600">{item.calls.toLocaleString()}</td>
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-2">
                                                <div className="flex-1 bg-slate-100 dark:bg-slate-800 rounded-full h-1 w-20">
                                                    <div className="bg-emerald-500 h-full rounded-full" style={{ width: '99.8%' }} />
                                                </div>
                                                <span className="text-[10px] font-black text-emerald-600 italic">99.8%</span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 font-bold text-[10px] text-slate-500">2.4 MB/S</td>
                                        <td className="px-6 py-4 text-[10px] font-medium text-slate-500 italic">2 SECONDS AGO</td>
                                        <td className="px-6 py-4">
                                            <Badge className="bg-emerald-500 text-white border-none italic text-[8px] font-black">STABLE</Badge>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
