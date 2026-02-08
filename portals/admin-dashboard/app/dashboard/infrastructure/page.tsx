'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
    Server,
    Database,
    Cpu,
    Activity,
    Shield,
    Zap,
    Clock,
    RefreshCw,
    AlertTriangle,
    CheckCircle2,
    HardDrive,
    Globe,
    Network,
    Terminal,
    Layers,
    Search
} from 'lucide-react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    AreaChart,
    Area
} from 'recharts';

// Mock data for the graphs
const performanceData = [
    { time: '00:00', cpu: 32, ram: 45, latency: 12 },
    { time: '04:00', cpu: 28, ram: 48, latency: 15 },
    { time: '08:00', cpu: 65, ram: 72, latency: 45 },
    { time: '12:00', cpu: 82, ram: 85, latency: 88 },
    { time: '16:00', cpu: 55, ram: 65, latency: 32 },
    { time: '20:00', cpu: 40, ram: 55, latency: 18 },
    { time: '23:59', cpu: 35, ram: 50, latency: 14 },
];

interface ServiceHealth {
    name: string;
    status: 'healthy' | 'warning' | 'error' | 'maintenance';
    uptime: string;
    latency: string;
    load: number;
}

import { adminApi } from '@/lib/api/admin';
import { toast } from 'sonner';
import { PageHeader } from '@/components/dashboard/PageHeader';

export default function InfrastructurePage() {
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [lastUpdated, setLastUpdated] = useState(new Date());
    const [healthData, setHealthData] = useState<any>(null);
    const [statsData, setStatsData] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);

    const loadClusterData = async () => {
        setIsRefreshing(true);
        try {
            const [healthRes, statsRes] = await Promise.all([
                adminApi.getHealth(),
                adminApi.getStats()
            ]);

            if (healthRes.data) setHealthData(healthRes.data);
            if (statsRes.data) setStatsData(statsRes.data);

            setLastUpdated(new Date());
        } catch (error) {
            console.error("Failed to sync cluster:", error);
            toast.error("Failed to sync cluster telemetry");
        } finally {
            setIsRefreshing(false);
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadClusterData();
        const interval = setInterval(loadClusterData, 30000); // Auto-refresh every 30s
        return () => clearInterval(interval);
    }, []);

    const handleRefresh = () => {
        loadClusterData();
        toast.success("Cluster telemetry synchronized");
    };

    const services: ServiceHealth[] = [
        { name: 'PostgreSQL Cluster', status: 'healthy', uptime: '99.99%', latency: '2ms', load: 45 },
        { name: 'Redis Cache', status: 'healthy', uptime: '99.99%', latency: '0.5ms', load: 12 },
        { name: 'HashiCorp Vault', status: 'healthy', uptime: '100%', latency: '5ms', load: 8 },
        { name: 'Temporal IO', status: 'healthy', uptime: '99.95%', latency: '12ms', load: 65 },
        { name: 'Ollama AI Engine', status: 'warning', uptime: '98.5%', latency: '450ms', load: 88 },
        { name: 'Brain Gateway', status: 'healthy', uptime: '99.99%', latency: '15ms', load: 32 },
        { name: 'Nginx Proxy Manager', status: 'healthy', uptime: '99.99%', latency: '1ms', load: 15 },
        { name: 'MinIO Object Storage', status: 'healthy', uptime: '99.99%', latency: '8ms', load: 24 },
    ];

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'healthy': return 'bg-emerald-500 text-white';
            case 'warning': return 'bg-amber-500 text-white';
            case 'error': return 'bg-red-500 text-white';
            case 'maintenance': return 'bg-blue-500 text-white';
            default: return 'bg-slate-500 text-white';
        }
    };

    return (
        <div className="p-4 md:p-8 space-y-8 bg-slate-50 dark:bg-slate-950 min-h-full pb-20">
            <PageHeader
                title={
                    <h1 className="text-3xl font-black text-slate-900 dark:text-white uppercase italic tracking-tighter">
                        Infrastructure <span className="text-indigo-600">Commander</span>
                    </h1>
                }
                description={
                    <p className="text-slate-500 font-medium flex items-center gap-2">
                        <Activity className="w-4 h-4 text-emerald-500" />
                        Live cluster telemetry and service health orchestration
                    </p>
                }
            >
                <div className="flex items-center gap-2">
                    <div className="text-right hidden md:block mr-2">
                        <p className="text-[10px] uppercase font-black text-slate-400">Last Sync</p>
                        <p className="text-xs font-bold text-slate-600 dark:text-slate-400">{lastUpdated.toLocaleTimeString()}</p>
                    </div>
                    <Button
                        variant="outline"
                        size="sm"
                        className="border-slate-200 dark:border-slate-800"
                        onClick={handleRefresh}
                        disabled={isRefreshing}
                    >
                        <RefreshCw className={`w-4 h-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
                        Sync Cluster
                    </Button>
                    <Button size="sm" className="bg-indigo-600 hover:bg-indigo-700">
                        <Terminal className="w-4 h-4 mr-2" />
                        Console
                    </Button>
                </div>
            </PageHeader>

            {/* Hardware Pulse */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card className="border-none shadow-sm bg-indigo-50/50 dark:bg-indigo-900/10 border-l-4 border-l-indigo-500">
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between mb-2">
                            <p className="text-[10px] uppercase font-black text-indigo-600 tracking-widest">CPU Compute</p>
                            <Cpu className="w-4 h-4 text-indigo-600" />
                        </div>
                        <div className="flex items-baseline gap-2">
                            <span className="text-2xl font-black text-slate-900 dark:text-white italic">
                                {healthData?.resources?.cpu ?? '0'}%
                            </span>
                            <span className="text-[10px] text-slate-500 font-bold">AVG LOAD</span>
                        </div>
                        <Progress value={healthData?.resources?.cpu ?? 0} className="h-1 mt-3 bg-indigo-100 dark:bg-indigo-900/20" />
                    </CardContent>
                </Card>

                <Card className="border-none shadow-sm bg-emerald-50/50 dark:bg-emerald-900/10 border-l-4 border-l-emerald-500">
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between mb-2">
                            <p className="text-[10px] uppercase font-black text-emerald-600 tracking-widest">Memory Mesh</p>
                            <Server className="w-4 h-4 text-emerald-600" />
                        </div>
                        <div className="flex items-baseline gap-2">
                            <span className="text-2xl font-black text-slate-900 dark:text-white italic">
                                {healthData?.resources?.memory?.percent ?? '0'}%
                            </span>
                            <span className="text-[10px] text-slate-500 font-bold">
                                {healthData?.resources?.memory ?
                                    `${(healthData.resources.memory.used / 1024 / 1024 / 1024).toFixed(1)} GB / ${(healthData.resources.memory.total / 1024 / 1024 / 1024).toFixed(1)} GB`
                                    : '0 GB / 0 GB'}
                            </span>
                        </div>
                        <Progress value={healthData?.resources?.memory?.percent ?? 0} className="h-1 mt-3 bg-emerald-100 dark:bg-emerald-900/20" />
                    </CardContent>
                </Card>

                <Card className="border-none shadow-sm bg-amber-50/50 dark:bg-amber-900/10 border-l-4 border-l-amber-500">
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between mb-2">
                            <p className="text-[10px] uppercase font-black text-amber-600 tracking-widest">Storage Array</p>
                            <HardDrive className="w-4 h-4 text-amber-600" />
                        </div>
                        <div className="flex items-baseline gap-2">
                            <span className="text-2xl font-black text-slate-900 dark:text-white italic">
                                {healthData?.resources?.disk?.percent ?? '0'}%
                            </span>
                            <span className="text-[10px] text-slate-500 font-bold">
                                {healthData?.resources?.disk ?
                                    `${(healthData.resources.disk.used / 1024 / 1024 / 1024).toFixed(1)} GB / ${(healthData.resources.disk.total / 1024 / 1024 / 1024).toFixed(1)} GB`
                                    : '0 GB / 0 GB'}
                            </span>
                        </div>
                        <Progress value={healthData?.resources?.disk?.percent ?? 0} className="h-1 mt-3 bg-amber-100 dark:bg-amber-900/20" />
                    </CardContent>
                </Card>

                <Card className="border-none shadow-sm bg-purple-50/50 dark:bg-purple-900/10 border-l-4 border-l-purple-500">
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between mb-2">
                            <p className="text-[10px] uppercase font-black text-purple-600 tracking-widest">Network Flow</p>
                            <Network className="w-4 h-4 text-purple-600" />
                        </div>
                        <div className="flex items-baseline gap-2">
                            <span className="text-2xl font-black text-slate-900 dark:text-white italic">
                                {statsData?.system?.uptime_seconds ? (statsData.system.uptime_seconds / 3600).toFixed(1) : '0'}
                            </span>
                            <span className="text-[10px] text-slate-500 font-bold">HOURS UPTIME</span>
                        </div>
                        <div className="flex gap-1 mt-4">
                            {[40, 70, 45, 90, 65, 80, 50, 60].map((h, i) => (
                                <div key={i} className="flex-1 bg-purple-200 dark:bg-purple-900/40 rounded-sm overflow-hidden" style={{ height: '12px' }}>
                                    <div className="bg-purple-600 w-full" style={{ height: `${h}%` }} />
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Performance Chart */}
                <Card className="lg:col-span-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xl overflow-hidden">
                    <CardHeader className="border-b border-slate-100 dark:border-slate-800 pb-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <CardTitle className="text-lg font-black uppercase italic tracking-tighter">Cluster Performance</CardTitle>
                                <CardDescription className="text-[10px] font-bold uppercase tracking-widest">24-hour resource allocation matrix</CardDescription>
                            </div>
                            <div className="flex gap-2">
                                <Badge variant="outline" className="text-[10px] border-indigo-200 bg-indigo-50 text-indigo-600 dark:bg-indigo-900/20">CPU</Badge>
                                <Badge variant="outline" className="text-[10px] border-emerald-200 bg-emerald-50 text-emerald-600 dark:bg-emerald-900/20">RAM</Badge>
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent className="pt-6">
                        <div className="h-[300px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={performanceData}>
                                    <defs>
                                        <linearGradient id="colorCpu" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#4f46e5" stopOpacity={0.1} />
                                            <stop offset="95%" stopColor="#4f46e5" stopOpacity={0} />
                                        </linearGradient>
                                        <linearGradient id="colorRam" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.1} />
                                            <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                    <XAxis
                                        dataKey="time"
                                        axisLine={false}
                                        tickLine={false}
                                        tick={{ fontSize: 10, fontWeight: 'bold' }}
                                    />
                                    <YAxis
                                        axisLine={false}
                                        tickLine={false}
                                        tick={{ fontSize: 10, fontWeight: 'bold' }}
                                    />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '12px', color: '#fff' }}
                                        itemStyle={{ fontSize: '12px', fontWeight: 'bold' }}
                                    />
                                    <Area type="monotone" dataKey="cpu" stroke="#4f46e5" fillOpacity={1} fill="url(#colorCpu)" strokeWidth={3} />
                                    <Area type="monotone" dataKey="ram" stroke="#10b981" fillOpacity={1} fill="url(#colorRam)" strokeWidth={3} />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </CardContent>
                </Card>

                {/* Security Pulse */}
                <Card className="border-slate-200 dark:border-slate-800 bg-slate-900 text-white shadow-xl">
                    <CardHeader>
                        <CardTitle className="text-lg font-black uppercase italic tracking-tighter flex items-center gap-2">
                            <Shield className="w-5 h-5 text-indigo-400" />
                            Security Perimeter
                        </CardTitle>
                        <CardDescription className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Active threat mitigation & vault status</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-xs font-bold text-slate-400">VAULT SEAL STATUS</span>
                                <Badge className="bg-emerald-500 text-white border-none">UNSEALED</Badge>
                            </div>
                            <div className="flex items-center gap-2">
                                <Clock className="w-3 h-3 text-indigo-400" />
                                <span className="text-[10px] font-bold text-slate-500">LAST ROTATION: 14H AGO</span>
                            </div>
                        </div>

                        <div className="space-y-4">
                            <div className="flex justify-between items-end">
                                <span className="text-xs font-black uppercase tracking-wider">Firewall Activity</span>
                                <span className="text-indigo-400 font-bold">NORMAL</span>
                            </div>
                            <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                                <div className="h-full bg-indigo-500 w-[75%]" />
                            </div>
                            <p className="text-[10px] text-slate-500 font-medium italic">Blocked 1,245 unauthorized ping attempts in the last 60 minutes.</p>
                        </div>

                        <Button className="w-full bg-white/10 hover:bg-white/20 border-white/10 text-white font-black text-xs uppercase tracking-widest">
                            View Audit Logs
                        </Button>
                    </CardContent>
                </Card>
            </div>

            {/* Service Health Grid */}
            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <h2 className="text-xl font-black text-slate-900 dark:text-white uppercase italic tracking-tighter flex items-center gap-2">
                        <Layers className="w-6 h-6 text-indigo-600" />
                        Core Service <span className="text-indigo-600">Health</span>
                    </h2>
                    <Badge variant="outline" className="border-slate-200 font-bold text-slate-500">{services.length} SERVICES OVERWATCHED</Badge>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {healthData?.services ? Object.entries(healthData.services).map(([name, status]: [string, any], i) => (
                        <Card key={i} className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:shadow-md transition-all group">
                            <CardContent className="p-4">
                                <div className="flex items-start justify-between mb-4">
                                    <div className="p-2 bg-slate-50 dark:bg-slate-800 rounded-xl group-hover:bg-indigo-50 dark:group-hover:bg-indigo-900/20 transition-colors">
                                        {name.includes('db') || name.includes('database') ? <Database className="w-5 h-5 text-indigo-600" /> :
                                            name.includes('redis') ? <Zap className="w-5 h-5 text-amber-500" /> :
                                                name.includes('vault') ? <Shield className="w-5 h-5 text-emerald-500" /> :
                                                    <Layers className="w-5 h-5 text-slate-500" />}
                                    </div>
                                    <Badge className={`${status === 'up' || status === 'ok' ? 'bg-emerald-500' : 'bg-red-500'} text-white border-none text-[8px] font-black italic`}>
                                        {status.toUpperCase()}
                                    </Badge>
                                </div>
                                <h3 className="font-black text-xs uppercase tracking-tight text-slate-900 dark:text-white mb-1">{name.replace(/-/g, ' ')}</h3>
                                <div className="flex items-center justify-between text-[10px] font-bold text-slate-400 mb-3">
                                    <span>UPTIME: 99.9%</span>
                                    <span>ACTIVE</span>
                                </div>
                                <div className="space-y-1">
                                    <div className="flex justify-between text-[8px] font-black uppercase text-slate-500">
                                        <span>Current Load</span>
                                        <span>{(Math.random() * 40 + 10).toFixed(0)}%</span>
                                    </div>
                                    <Progress value={Math.random() * 40 + 10} className="h-1" />
                                </div>
                            </CardContent>
                        </Card>
                    )) : (
                        <div className="col-span-4 py-12 text-center text-slate-400 font-bold uppercase tracking-widest">
                            No service telemetry available
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
