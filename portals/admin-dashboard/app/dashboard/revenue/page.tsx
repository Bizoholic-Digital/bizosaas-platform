'use client';

import React, { useState, useEffect } from 'react';
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CardDescription
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
    DollarSign,
    TrendingUp,
    Globe,
    ShoppingCart,
    ArrowUpRight,
    ArrowDownRight,
    RefreshCw,
    Calendar,
    Filter,
    Download,
    MoreVertical,
    ChevronRight,
    PieChart,
    Target,
    CheckCircle2
} from 'lucide-react';
import { PageHeader } from '@/components/dashboard/PageHeader';
import { adminApi } from '@/lib/api/admin';
import { toast } from 'sonner';

export default function RevenuePage() {
    const [stats, setStats] = useState<any>(null);
    const [transactions, setTransactions] = useState<any[]>([]);
    const [domains, setDomains] = useState<any[]>([]);
    const [dunning, setDunning] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState<'overview' | 'transactions' | 'domains' | 'dunning'>('overview');

    const loadData = async () => {
        setLoading(true);
        try {
            const [statsRes, transRes, domainsRes, dunningRes] = await Promise.all([
                adminApi.getRevenueStats(),
                adminApi.getRevenueTransactions(),
                adminApi.getGlobalDomains(),
                adminApi.getDunningQueue()
            ]);

            if (statsRes.data) setStats(statsRes.data);
            if (transRes.data) setTransactions(transRes.data);
            if (domainsRes.data) setDomains(domainsRes.data);
            if (dunningRes.data) setDunning(dunningRes.data);
        } catch (error) {
            console.error("Failed to load revenue data:", error);
            toast.error("Failed to sync financial data");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    return (
        <div className="p-6 space-y-6 bg-slate-50 dark:bg-slate-950 min-h-full">
            <PageHeader
                title={
                    <>Platform <span className="text-emerald-600">Revenue</span></>
                }
                description="Track portal earnings, affiliate commissions, and global domain inventory."
            >
                <Button variant="outline" className="rounded-xl border-dashed">
                    <Download className="mr-2 h-4 w-4" /> Export Report
                </Button>
                <Button onClick={loadData} className="bg-emerald-600 hover:bg-emerald-700 rounded-xl" disabled={loading}>
                    <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Sync Data
                </Button>
            </PageHeader>

            {/* Financial Overview Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm relative overflow-hidden group">
                    <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                        <DollarSign className="w-24 h-24 -mr-8 -mt-8" />
                    </div>
                    <CardHeader className="pb-2">
                        <p className="text-xs font-black text-slate-500 uppercase tracking-widest">Total Gross Revenue</p>
                        <div className="flex items-center justify-between">
                            <h3 className="text-3xl font-black mt-1">${stats?.total_revenue?.toLocaleString() || '0.00'}</h3>
                            <div className="flex items-center text-emerald-500 text-xs font-bold bg-emerald-50 dark:bg-emerald-900/20 px-2 py-0.5 rounded-full">
                                <ArrowUpRight className="w-3 h-3 mr-1" /> +12.4%
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <p className="text-[10px] text-slate-400 font-bold uppercase tracking-tight italic">Combined earnings from all platform sources</p>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm relative overflow-hidden group">
                    <CardHeader className="pb-2">
                        <p className="text-xs font-black text-slate-500 uppercase tracking-widest">Portal Commissions</p>
                        <div className="flex items-center justify-between">
                            <h3 className="text-3xl font-black mt-1 text-indigo-600">${stats?.total_commission?.toLocaleString() || '0.00'}</h3>
                            <div className="flex items-center text-indigo-500 text-xs font-bold bg-indigo-50 dark:bg-indigo-900/20 px-2 py-0.5 rounded-full">
                                <Target className="w-3 h-3 mr-1" /> $1.2k Target
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <p className="text-[10px] text-slate-400 font-bold uppercase tracking-tight italic">Net earnings for the BizOSaaS infrastructure</p>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm relative overflow-hidden group">
                    <CardHeader className="pb-2">
                        <p className="text-xs font-black text-slate-500 uppercase tracking-widest">Active Assets</p>
                        <div className="flex items-center justify-between">
                            <h3 className="text-3xl font-black mt-1 text-emerald-600">{domains?.length || 0}</h3>
                            <div className="text-xs font-bold text-slate-400">Domains Managed</div>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <p className="text-[10px] text-slate-400 font-bold uppercase tracking-tight italic">Total number of domains and premium services</p>
                    </CardContent>
                </Card>
            </div>

            {/* Tabs */}
            <div className="flex space-x-6 border-b border-slate-200 dark:border-slate-800 pb-px">
                {[
                    { id: 'overview', label: 'Revenue Sources', icon: PieChart },
                    { id: 'transactions', label: 'Recent Transactions', icon: DollarSign },
                    { id: 'domains', label: 'Domain Inventory', icon: Globe },
                    { id: 'dunning', label: 'Dunning & Retries', icon: RefreshCw }
                ].map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id as any)}
                        className={`flex items-center gap-2 pb-4 text-xs font-black uppercase tracking-widest transition-all relative ${activeTab === tab.id
                            ? 'text-indigo-600'
                            : 'text-slate-500 hover:text-slate-800'
                            }`}
                    >
                        <tab.icon className="w-4 h-4" />
                        {tab.label}
                        {activeTab === tab.id && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-600" />}
                    </button>
                ))}
            </div>

            <Card className="border-none shadow-sm min-h-[400px]">
                {activeTab === 'overview' && (
                    <CardContent className="p-8">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                            <div>
                                <h4 className="text-sm font-black uppercase tracking-widest text-slate-400 mb-6">Earnings by Category</h4>
                                <div className="space-y-6">
                                    {Object.entries(stats?.sources || {}).map(([source, amount]: any) => (
                                        <div key={source} className="group">
                                            <div className="flex items-center justify-between mb-2">
                                                <div className="flex items-center gap-3">
                                                    <div className={`w-3 h-3 rounded-full ${source === 'domain_purchase' ? 'bg-indigo-500' : 'bg-emerald-500'}`} />
                                                    <span className="text-xs font-bold uppercase tracking-tight">{source.replace('_', ' ')}</span>
                                                </div>
                                                <span className="text-sm font-black">${amount.toLocaleString()}</span>
                                            </div>
                                            <div className="h-2 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                                                <div
                                                    className={`h-full transition-all duration-1000 ${source === 'domain_purchase' ? 'bg-indigo-500' : 'bg-emerald-500'}`}
                                                    style={{ width: `${(amount / (stats?.total_revenue || 1)) * 100}%` }}
                                                />
                                            </div>
                                        </div>
                                    ))}
                                    {Object.keys(stats?.sources || {}).length === 0 && (
                                        <div className="text-center p-12 text-slate-400 italic">No revenue data available yet</div>
                                    )}
                                </div>
                            </div>

                            <div className="bg-slate-50 dark:bg-slate-900/50 rounded-3xl p-6 border-2 border-dashed border-slate-200 dark:border-slate-800 flex flex-col items-center justify-center text-center">
                                <TrendingUp className="w-12 h-12 text-indigo-500 mb-4 opacity-20" />
                                <h4 className="font-black text-lg uppercase tracking-tighter">Projected Growth</h4>
                                <p className="text-sm text-slate-500 mt-2 max-w-xs">Based on current onboarding trends, commissions are expected to hit <span className="text-indigo-600 font-bold">$2,400</span> by end of quarter.</p>
                                <Button variant="ghost" className="mt-6 text-xs font-black uppercase tracking-widest hover:text-indigo-600">View Detailed Forecast <ChevronRight className="w-4 h-4 ml-1" /></Button>
                            </div>
                        </div>
                    </CardContent>
                )}

                {activeTab === 'transactions' && (
                    <CardContent className="p-0">
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead>
                                    <tr className="border-b border-slate-100 dark:border-slate-800">
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Date</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Source</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">User / Identity</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Amount</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Status</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400 text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {transactions.map((t) => (
                                        <tr key={t.id} className="border-b border-slate-50 dark:border-slate-900 hover:bg-slate-50/50 dark:hover:bg-slate-900/50 transition-colors">
                                            <td className="p-6">
                                                <div className="flex flex-col">
                                                    <span className="text-xs font-bold">{new Date(t.created_at).toLocaleDateString()}</span>
                                                    <span className="text-[10px] text-slate-400">{new Date(t.created_at).toLocaleTimeString()}</span>
                                                </div>
                                            </td>
                                            <td className="p-6">
                                                <div className="flex items-center gap-2">
                                                    <div className="w-8 h-8 bg-slate-100 dark:bg-slate-800 rounded-lg flex items-center justify-center">
                                                        {t.source_type === 'domain_purchase' ? <Globe className="w-4 h-4 text-indigo-500" /> : <DollarSign className="w-4 h-4 text-emerald-500" />}
                                                    </div>
                                                    <div className="flex flex-col">
                                                        <span className="text-xs font-black uppercase tracking-tight italic">{t.source_type.replace('_', ' ')}</span>
                                                        <span className="text-[10px] text-slate-400 font-bold">{t.partner || 'Internal'}</span>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="p-6">
                                                <div className="flex flex-col">
                                                    <span className="text-xs font-bold">{t.user_email}</span>
                                                    <span className="text-[10px] text-slate-400 font-bold uppercase tracking-widest tracking-tighter cursor-pointer hover:text-indigo-600 transition-colors">View Profile</span>
                                                </div>
                                            </td>
                                            <td className="p-6">
                                                <div className="flex flex-col">
                                                    <span className="text-sm font-black text-slate-900 dark:text-white">${t.amount.toFixed(2)}</span>
                                                    <span className="text-[10px] text-emerald-600 font-bold">{t.commission > 0 ? `+$${t.commission.toFixed(2)} EARNED` : 'NO CUT'}</span>
                                                </div>
                                            </td>
                                            <td className="p-6">
                                                <Badge className={
                                                    t.status === 'completed' ? 'bg-emerald-500/10 text-emerald-600' :
                                                        t.status === 'pending' ? 'bg-amber-500/10 text-amber-600' :
                                                            'bg-slate-500/10 text-slate-600'
                                                }>
                                                    {t.status.toUpperCase()}
                                                </Badge>
                                            </td>
                                            <td className="p-6 text-right">
                                                <Button variant="ghost" size="icon" className="rounded-xl">
                                                    <MoreVertical className="w-4 h-4" />
                                                </Button>
                                            </td>
                                        </tr>
                                    ))}
                                    {transactions.length === 0 && (
                                        <tr>
                                            <td colSpan={6} className="p-12 text-center text-slate-400 italic">No transactions recorded yet</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </CardContent>
                )}

                {activeTab === 'domains' && (
                    <CardContent className="p-0">
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead>
                                    <tr className="border-b border-slate-100 dark:border-slate-800">
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Domain Name</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Registrar</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Mapping</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Expiry</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Status</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400 text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {domains.map((d) => (
                                        <tr key={d.id} className="border-b border-slate-50 dark:border-slate-900 hover:bg-slate-50/50 dark:hover:bg-slate-900/50 transition-colors">
                                            <td className="p-6">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-10 h-10 bg-indigo-50 dark:bg-indigo-900/20 rounded-xl flex items-center justify-center text-indigo-600">
                                                        <Globe className="w-5 h-5" />
                                                    </div>
                                                    <span className="text-sm font-black text-slate-900 dark:text-white">{d.domain_name}</span>
                                                </div>
                                            </td>
                                            <td className="p-6 font-bold uppercase tracking-widest text-xs text-slate-500">{d.registrar || 'Direct'}</td>
                                            <td className="p-6">
                                                <Badge variant="outline" className="border-slate-200 dark:border-slate-800 font-bold uppercase tracking-tighter text-[9px]">
                                                    {d.target_service || 'Unassigned'} : {d.target_slug || '-'}
                                                </Badge>
                                            </td>
                                            <td className="p-6 text-xs font-bold">{d.expiry_date ? new Date(d.expiry_date).toLocaleDateString() : 'N/A'}</td>
                                            <td className="p-6">
                                                <Badge className="bg-emerald-500/10 text-emerald-600">ACTIVE</Badge>
                                            </td>
                                            <td className="p-6 text-right">
                                                <Button variant="ghost" size="icon"><MoreVertical className="w-4 h-4" /></Button>
                                            </td>
                                        </tr>
                                    ))}
                                    {domains.length === 0 && (
                                        <tr>
                                            <td colSpan={6} className="p-12 text-center text-slate-400 italic">No domain inventory found</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </CardContent>
                )}

                {activeTab === 'dunning' && (
                    <CardContent className="p-0">
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead>
                                    <tr className="border-b border-slate-100 dark:border-slate-800">
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Tenant / Invoice</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Amount</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Retry State</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Last Failure Reason</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400">Next Attempt</th>
                                        <th className="p-6 text-[10px] font-black uppercase tracking-widest text-slate-400 text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {dunning.map((d) => (
                                        <tr key={d.id} className="border-b border-slate-50 dark:border-slate-900">
                                            <td className="p-6">
                                                <div className="flex flex-col">
                                                    <span className="text-sm font-black italic">{d.tenant_name}</span>
                                                    <span className="text-[10px] text-slate-400 font-bold">INV-{d.id.slice(0, 8).toUpperCase()}</span>
                                                </div>
                                            </td>
                                            <td className="p-6">
                                                <span className="text-sm font-black">${d.amount.toFixed(2)}</span>
                                            </td>
                                            <td className="p-6">
                                                <div className="flex items-center gap-2">
                                                    <Badge className="bg-orange-500/10 text-orange-600 border-none font-bold italic">RETRY {d.retry_count}/3</Badge>
                                                </div>
                                            </td>
                                            <td className="p-6">
                                                <span className="text-[10px] font-bold text-red-500 bg-red-50 px-2 py-1 rounded-lg">{d.last_failure}</span>
                                            </td>
                                            <td className="p-6">
                                                <span className="text-xs font-bold">{new Date(d.next_retry).toLocaleString()}</span>
                                            </td>
                                            <td className="p-6 text-right">
                                                <Button
                                                    size="sm"
                                                    className="bg-indigo-600 hover:bg-indigo-700 rounded-xl font-black text-[10px] uppercase tracking-widest"
                                                    onClick={async () => {
                                                        const res = await adminApi.retryPayment(d.id);
                                                        if (!res.error) toast.success("Retry command dispatched");
                                                        else toast.error("Retry failed: " + res.error);
                                                    }}
                                                >
                                                    Manual Retry
                                                </Button>
                                            </td>
                                        </tr>
                                    ))}
                                    {dunning.length === 0 && (
                                        <tr>
                                            <td colSpan={6} className="p-20 text-center">
                                                <CheckCircle2 className="w-12 h-12 text-emerald-500/20 mx-auto mb-4" />
                                                <p className="text-slate-400 font-black uppercase tracking-widest text-xs">No active payment failures</p>
                                                <p className="text-[10px] text-slate-300 font-bold mt-1 uppercase">All subscriptions are currently up to date.</p>
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </CardContent>
                )}
            </Card>
        </div>
    );
}
