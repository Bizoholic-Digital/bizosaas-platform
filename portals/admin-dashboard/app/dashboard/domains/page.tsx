'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Globe,
    Search,
    RefreshCw,
    Database,
    Shield,
    Server,
    ExternalLink,
    MoreVertical,
    Clock,
    Plus,
    Trash2,
    Settings2,
    ArrowUpRight,
    Lock
} from 'lucide-react';
import { adminApi } from '@/lib/api/admin';
import { toast } from 'sonner';
import { PageHeader } from '@/components/dashboard/PageHeader';

export default function DomainsAdminPage() {
    const [domains, setDomains] = useState<any[]>([]);
    const [stats, setStats] = useState<any>(null);
    const [providers, setProviders] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [activeTab, setActiveTab] = useState<'inventory' | 'providers' | 'dns'>('inventory');
    const [selectedDomain, setSelectedDomain] = useState<any>(null);
    const [dnsRecords, setDnsRecords] = useState<any[]>([]);

    const loadData = async () => {
        setLoading(true);
        try {
            const [domainsRes, statsRes, providersRes] = await Promise.all([
                adminApi.getGlobalDomains(),
                adminApi.getDomainAdminStats(),
                adminApi.getDomainProviders()
            ]);

            if (domainsRes.data) setDomains(domainsRes.data);
            if (statsRes.data) setStats(statsRes.data);
            if (providersRes.data) setProviders(providersRes.data);
        } catch (error) {
            console.error("Failed to load domain data:", error);
            toast.error("Failed to sync domain engine");
        } finally {
            setLoading(false);
        }
    };

    const loadDnsRecords = async (domainId: string) => {
        try {
            const res = await adminApi.getDomainDns(domainId);
            if (res.data) setDnsRecords(res.data);
        } catch (error) {
            toast.error("Failed to fetch DNS records");
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const handleSelectDomain = (domain: any) => {
        setSelectedDomain(domain);
        setActiveTab('dns');
        loadDnsRecords(domain.id);
    };

    return (
        <div className="p-4 md:p-8 space-y-8 bg-slate-50 dark:bg-slate-950 min-h-full pb-20">
            <PageHeader
                title={
                    <h1 className="text-3xl font-black text-slate-900 dark:text-white uppercase italic tracking-tighter">
                        Domain <span className="text-blue-600">Control Center</span>
                    </h1>
                }
                description={
                    <p className="text-slate-500 font-medium flex items-center gap-2">
                        <Globe className="w-4 h-4 text-blue-500" />
                        Global domain inventory, multi-provider DNS, and revenue tracking
                    </p>
                }
            >
                <div className="flex items-center gap-2">
                    <Button variant="outline" size="sm" onClick={loadData} disabled={loading}>
                        <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                        Sync Registry
                    </Button>
                    <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                        <Plus className="w-4 h-4 mr-2" />
                        Register Domain
                    </Button>
                </div>
            </PageHeader>

            {/* Platform Revenue Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="border-none shadow-sm bg-white dark:bg-slate-900 border-l-4 border-l-blue-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between mb-2">
                            <p className="text-[10px] uppercase font-black text-slate-500 tracking-widest">Active Domains</p>
                            <Globe className="w-4 h-4 text-blue-500" />
                        </div>
                        <div className="flex items-baseline gap-2">
                            <span className="text-2xl font-black text-slate-900 dark:text-white italic">
                                {stats?.total_active_domains || 0}
                            </span>
                            <Badge className="bg-emerald-500/10 text-emerald-600 border-none text-[10px]">+12%</Badge>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-none shadow-sm bg-white dark:bg-slate-900 border-l-4 border-l-emerald-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between mb-2">
                            <p className="text-[10px] uppercase font-black text-slate-500 tracking-widest">Gross Revenue</p>
                            <ArrowUpRight className="w-4 h-4 text-emerald-500" />
                        </div>
                        <div className="flex items-baseline gap-2">
                            <span className="text-2xl font-black text-slate-900 dark:text-white italic">
                                ${stats?.gross_revenue?.toLocaleString() || '0.00'}
                            </span>
                            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-widest ml-1">USD</span>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-none shadow-sm bg-white dark:bg-slate-900 border-l-4 border-l-indigo-500">
                    <CardContent className="p-6">
                        <div className="flex items-center justify-between mb-2">
                            <p className="text-[10px] uppercase font-black text-slate-500 tracking-widest">Net Profit Margin</p>
                            <Plus className="w-4 h-4 text-indigo-500" />
                        </div>
                        <div className="flex items-baseline gap-2">
                            <span className="text-2xl font-black text-slate-900 dark:text-white italic">
                                ${stats?.net_profit?.toLocaleString() || '0.00'}
                            </span>
                            <Badge className="bg-indigo-500/10 text-indigo-600 border-none text-[10px]">36% AVG</Badge>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Main Tabs */}
            <div className="flex space-x-1 bg-slate-200/50 dark:bg-slate-800/50 p-1 rounded-xl w-fit">
                <button
                    onClick={() => setActiveTab('inventory')}
                    className={`px-4 py-2 text-xs font-black uppercase tracking-widest transition-all rounded-lg ${activeTab === 'inventory' ? 'bg-white dark:bg-slate-700 text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
                >
                    Registry
                </button>
                <button
                    onClick={() => setActiveTab('providers')}
                    className={`px-4 py-2 text-xs font-black uppercase tracking-widest transition-all rounded-lg ${activeTab === 'providers' ? 'bg-white dark:bg-slate-700 text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
                >
                    Providers
                </button>
                {selectedDomain && (
                    <button
                        onClick={() => setActiveTab('dns')}
                        className={`px-4 py-2 text-xs font-black uppercase tracking-widest transition-all rounded-lg ${activeTab === 'dns' ? 'bg-white dark:bg-slate-700 text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
                    >
                        DNS: {selectedDomain.domain_name}
                    </button>
                )}
            </div>

            {activeTab === 'inventory' && (
                <Card className="border-none shadow-xl bg-white dark:bg-slate-900 overflow-hidden">
                    <CardHeader className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/20">
                        <div className="flex items-center justify-between">
                            <div>
                                <CardTitle className="text-lg font-black uppercase italic tracking-tighter">Domain Inventory</CardTitle>
                                <CardDescription className="text-[10px] font-bold uppercase tracking-widest">Managed properties across all tenants</CardDescription>
                            </div>
                            <div className="relative w-64">
                                <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                                <Input
                                    placeholder="Find domain..."
                                    className="pl-9 h-9 rounded-xl border-slate-200 dark:border-slate-800"
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                />
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent className="p-0">
                        <div className="overflow-x-auto">
                            <table className="w-full text-left border-collapse">
                                <thead>
                                    <tr className="bg-slate-50/50 dark:bg-slate-800/30 text-[10px] font-black uppercase tracking-widest text-slate-400 border-b border-slate-100 dark:border-slate-800">
                                        <th className="px-6 py-4">Domain Name</th>
                                        <th className="px-6 py-4">Tenant</th>
                                        <th className="px-6 py-4">Registrar</th>
                                        <th className="px-6 py-4">Status</th>
                                        <th className="px-6 py-4">Expiry</th>
                                        <th className="px-6 py-4 text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                                    {domains.filter(d => d.domain_name.toLowerCase().includes(searchTerm.toLowerCase())).map((domain) => (
                                        <tr key={domain.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/50 transition-colors group">
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-3">
                                                    <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg group-hover:scale-110 transition-transform">
                                                        <Globe className="w-4 h-4 text-blue-600" />
                                                    </div>
                                                    <div>
                                                        <p className="text-sm font-black text-slate-900 dark:text-white">{domain.domain_name}</p>
                                                        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{domain.target_service || 'Unmapped'}</p>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <Badge variant="outline" className="text-[10px] border-slate-200 px-2 py-0">ID: {domain.tenant_id?.slice(0, 8)}</Badge>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-2">
                                                    <span className="text-[10px] font-black uppercase tracking-widest">{domain.registrar}</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <Badge className={`${domain.status === 'active' ? 'bg-emerald-500' : 'bg-red-500'} text-white border-none text-[8px] font-black italic`}>
                                                    {domain.status.toUpperCase()}
                                                </Badge>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500">
                                                    <Clock className="w-3 h-3 text-slate-300" />
                                                    {domain.expiry_date ? new Date(domain.expiry_date).toLocaleDateString() : 'N/A'}
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 text-right">
                                                <div className="flex items-center justify-end gap-2 text-slate-400">
                                                    <Button
                                                        variant="ghost"
                                                        size="sm"
                                                        className="h-8 px-2 text-[10px] font-black hover:bg-blue-50 hover:text-blue-600 rounded-lg"
                                                        onClick={() => handleSelectDomain(domain)}
                                                    >
                                                        MANAGE DNS
                                                    </Button>
                                                    <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-slate-100 rounded-lg">
                                                        <MoreVertical className="w-4 h-4" />
                                                    </Button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </CardContent>
                </Card>
            )}

            {activeTab === 'providers' && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {providers.map((provider) => (
                        <Card key={provider.id} className="border-none shadow-xl bg-white dark:bg-slate-900 group hover:shadow-2xl transition-all">
                            <CardHeader className="pb-2">
                                <div className="flex justify-between items-start">
                                    <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-2xl group-hover:bg-blue-50 dark:group-hover:bg-blue-900/20 transition-colors">
                                        <Server className="w-6 h-6 text-slate-600 dark:text-slate-400 group-hover:text-blue-600" />
                                    </div>
                                    <Badge className={`${provider.status === 'active' ? 'bg-emerald-500' : 'bg-slate-400'} text-white border-none text-[8px] font-black italic`}>
                                        {provider.status.toUpperCase()}
                                    </Badge>
                                </div>
                                <CardTitle className="text-lg font-black uppercase tracking-tight mt-4 italic">{provider.name}</CardTitle>
                                <CardDescription className="text-[10px] font-bold tracking-widest uppercase">Registry Provider #{provider.priority}</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-6 pt-4">
                                <div className="space-y-2">
                                    <div className="flex justify-between text-[10px] font-black uppercase text-slate-500">
                                        <span>Platform Markup</span>
                                        <span className="text-emerald-500">{provider.margin}%</span>
                                    </div>
                                    <div className="h-2 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                                        <div className="h-full bg-emerald-500" style={{ width: `${provider.margin * 2}%` }} />
                                    </div>
                                </div>

                                <div className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-2xl border border-slate-100 dark:border-slate-800">
                                    <div className="flex items-center justify-between mb-3 text-[10px] font-black uppercase text-slate-400">
                                        <span>API Credentials</span>
                                        <Lock className="w-3 h-3" />
                                    </div>
                                    <div className="space-y-2">
                                        <div className="flex justify-between items-center text-xs">
                                            <span className="font-bold text-slate-600">Client ID</span>
                                            <span className="font-mono text-slate-400">********42</span>
                                        </div>
                                        <div className="flex justify-between items-center text-xs">
                                            <span className="font-bold text-slate-600">Client Secret</span>
                                            <span className="font-mono text-slate-400">********RS</span>
                                        </div>
                                    </div>
                                </div>

                                <Button variant="outline" className="w-full h-10 text-[10px] font-black uppercase tracking-widest rounded-xl hover:bg-slate-100 border-slate-200">
                                    <Settings2 className="w-4 h-4 mr-2" />
                                    Configure Provider
                                </Button>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}

            {activeTab === 'dns' && selectedDomain && (
                <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2">
                    <div className="flex items-center justify-between bg-white dark:bg-slate-900 p-6 rounded-2xl shadow-xl border-l-4 border-l-blue-600">
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 bg-blue-50 dark:bg-blue-900/20 rounded-2xl flex items-center justify-center text-blue-600">
                                <Globe className="w-6 h-6" />
                            </div>
                            <div>
                                <h3 className="text-2xl font-black italic tracking-tighter text-slate-900 dark:text-white uppercase leading-none">{selectedDomain.domain_name}</h3>
                                <div className="flex items-center gap-2 mt-2">
                                    <Badge variant="outline" className="text-[10px] font-bold uppercase tracking-widest">{selectedDomain.registrar}</Badge>
                                    <Badge className="bg-emerald-500 text-white border-none text-[8px] font-black italic">CONNECTED</Badge>
                                </div>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <Button variant="outline" className="rounded-xl font-black text-[10px] uppercase h-9 border-slate-200" onClick={() => loadDnsRecords(selectedDomain.id)}>
                                <RefreshCw className="w-4 h-4 mr-2" /> REFRESH RECORDS
                            </Button>
                            <Button className="bg-blue-600 hover:bg-blue-700 rounded-xl font-black text-[10px] uppercase h-9 shadow-lg shadow-blue-500/20">
                                <Plus className="w-4 h-4 mr-2" /> ADD RECORD
                            </Button>
                        </div>
                    </div>

                    <Card className="border-none shadow-xl bg-white dark:bg-slate-900 overflow-hidden">
                        <CardHeader className="bg-slate-50/50 dark:bg-slate-800/20 py-4 border-b border-slate-100 dark:border-slate-800">
                            <CardTitle className="text-sm font-black uppercase tracking-widest text-slate-500 italic">DNS Record Matrix</CardTitle>
                        </CardHeader>
                        <CardContent className="p-0">
                            <div className="overflow-x-auto">
                                <table className="w-full text-left border-collapse">
                                    <thead>
                                        <tr className="text-[10px] font-black uppercase tracking-widest text-slate-400 border-b border-slate-100 dark:border-slate-800">
                                            <th className="px-6 py-4">Type</th>
                                            <th className="px-6 py-4">Host/Name</th>
                                            <th className="px-6 py-4">Value/Target</th>
                                            <th className="px-6 py-4">TTL</th>
                                            <th className="px-6 py-4 text-right">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                                        {dnsRecords.map((record, i) => (
                                            <tr key={i} className="hover:bg-slate-50/50 transition-colors group">
                                                <td className="px-6 py-4">
                                                    <Badge className="bg-indigo-500/10 text-indigo-600 border-none font-black text-[10px] min-w-[40px] justify-center">{record.type}</Badge>
                                                </td>
                                                <td className="px-6 py-4">
                                                    <span className="font-mono text-xs font-bold text-slate-600 dark:text-slate-400">{record.name}</span>
                                                </td>
                                                <td className="px-6 py-4">
                                                    <div className="flex items-center gap-2 group/val max-w-md truncate">
                                                        <span className="font-mono text-xs font-medium text-slate-500 group-hover:text-blue-600 transition-colors uppercase">{record.value}</span>
                                                    </div>
                                                </td>
                                                <td className="px-6 py-4">
                                                    <span className="text-[10px] font-black italic text-slate-400">{record.ttl} SEC</span>
                                                </td>
                                                <td className="px-6 py-4 text-right">
                                                    <div className="flex items-center justify-end gap-2 text-slate-400">
                                                        <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-slate-100 rounded-lg">
                                                            <Settings2 className="w-4 h-4" />
                                                        </Button>
                                                        <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-red-50 hover:text-red-500 rounded-lg">
                                                            <Trash2 className="w-4 h-4" />
                                                        </Button>
                                                    </div>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            )}
        </div>
    );
}
