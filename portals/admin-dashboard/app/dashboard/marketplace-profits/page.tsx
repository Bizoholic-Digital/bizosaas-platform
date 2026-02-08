'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import {
    DollarSign,
    TrendingUp,
    TrendingDown,
    PieChart,
    ArrowUpRight,
    ArrowDownRight,
    Search,
    Download,
    Calendar,
    Filter,
    HelpCircle
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { useSetHeader } from '@/lib/contexts/HeaderContext';
import { adminApi } from '@/lib/api/admin';
import { toast } from 'sonner';
import { useRef } from 'react';

export default function MarketplaceProfitsPage() {
    useSetHeader("Profitability & Reconciliation", "Deep-dive into SKU-level net margins across all connected marketplaces.");

    const [profits, setProfits] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [selectedMarketplace, setSelectedMarketplace] = useState('FLIPKART');
    const fileInputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        loadProfits();
    }, []);

    const loadProfits = async () => {
        try {
            const res = await adminApi.getSkuProfitability();
            if (res.data) {
                // Formatting data if needed or setting directly
                setProfits(res.data.map(p => ({
                    sku: p.sku,
                    name: p.name,
                    sales: Math.floor(Math.random() * 1000), // Random for demo if not in API
                    revenue: p.avg_selling_price * 100, // Mocked
                    margin: p.channel_stats[0]?.margin || 0,
                    status: p.overall_health === 'high' ? 'high_profit' : 'warning',
                    rto: p.rto_rate * 100
                })));
            }
        } catch (e) {
            console.error("Failed to load profits", e);
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        setUploading(true);
        try {
            const res = await adminApi.uploadSettlementFile(selectedMarketplace.toLowerCase(), file);
            if (res.data?.status === 'completed') {
                toast.success(`Successfully reconciled ${file.name} for ${selectedMarketplace}`);
                // Refresh data
                loadProfits();
            }
        } catch (error) {
            toast.error("Failed to upload settlement file");
            console.error(error);
        } finally {
            setUploading(false);
            if (fileInputRef.current) fileInputRef.current.value = '';
        }
    };

    const getStatusBadge = (status: string) => {
        switch (status) {
            case 'high_profit': return <Badge className="bg-emerald-500 text-white border-none font-bold">TOP PERFORMER</Badge>;
            case 'profitable': return <Badge className="bg-emerald-500/10 text-emerald-600 border-none font-bold">PROFITABLE</Badge>;
            case 'warning': return <Badge className="bg-amber-500/10 text-amber-600 border-none font-bold">THIN MARGIN</Badge>;
            case 'critical': return <Badge className="bg-rose-500/10 text-rose-600 border-none font-bold">AT LOSS</Badge>;
            default: return <Badge variant="outline">{status}</Badge>;
        }
    };

    return (
        <div className="p-6 space-y-6 bg-slate-50 dark:bg-slate-950 min-h-full">
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-4">
                        <div className="flex justify-between items-start">
                            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Net Profit (MTD)</p>
                            <DollarSign className="w-4 h-4 text-emerald-500" />
                        </div>
                        <h3 className="text-xl font-black mt-1">₹8,45,200</h3>
                        <div className="flex items-center gap-1 mt-1">
                            <ArrowUpRight className="w-3 h-3 text-emerald-500" />
                            <span className="text-[10px] text-emerald-500 font-bold">+18.4%</span>
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-4">
                        <div className="flex justify-between items-start">
                            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Avg Margin</p>
                            <PieChart className="w-4 h-4 text-blue-500" />
                        </div>
                        <h3 className="text-xl font-black mt-1">44.2%</h3>
                        <div className="flex items-center gap-1 mt-1">
                            <ArrowDownRight className="w-3 h-3 text-rose-500" />
                            <span className="text-[10px] text-rose-500 font-bold">-2.1% due to RTO</span>
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm">
                    <CardContent className="p-4">
                        <div className="flex justify-between items-start">
                            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Discrepancy Alerts</p>
                            <TrendingDown className="w-4 h-4 text-rose-500" />
                        </div>
                        <h3 className="text-xl font-black mt-1">14</h3>
                        <p className="text-[10px] text-gray-400 font-bold mt-1">Found in Flipkart payout</p>
                    </CardContent>
                </Card>

                <Card className="bg-indigo-600 text-white border-none shadow-sm">
                    <CardContent className="p-4">
                        <div className="flex justify-between items-start">
                            <p className="text-[10px] font-black text-indigo-200 uppercase tracking-widest">Settlement Forecast</p>
                            <TrendingUp className="w-4 h-4 text-white" />
                        </div>
                        <h3 className="text-xl font-black mt-1">₹12.4L</h3>
                        <p className="text-[10px] text-indigo-200 font-bold mt-1">Expected by Friday</p>
                    </CardContent>
                </Card>
            </div>

            {/* Reconciliation Tools */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm rounded-3xl">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <div>
                            <CardTitle className="text-sm font-black uppercase tracking-widest text-gray-400">Payout Reconciled</CardTitle>
                        </div>
                        <HelpCircle className="w-4 h-4 text-gray-300" />
                    </CardHeader>
                    <CardContent>
                        <div className="p-4 bg-slate-50 dark:bg-slate-800 rounded-2xl border border-dashed border-gray-200 flex flex-col items-center justify-center py-8">
                            <Download className={cn("w-8 h-8 text-gray-300 mb-3", uploading && "animate-bounce text-indigo-500")} />
                            <p className="text-xs font-bold text-gray-500 uppercase tracking-widest">
                                {uploading ? "Processing Settlement..." : `Drop ${selectedMarketplace} CSV Here`}
                            </p>
                            <input
                                type="file"
                                ref={fileInputRef}
                                className="hidden"
                                accept=".csv"
                                onChange={handleFileUpload}
                            />
                            <Button
                                size="sm"
                                disabled={uploading}
                                onClick={() => fileInputRef.current?.click()}
                                className="mt-4 bg-slate-900 hover:bg-black rounded-xl text-[10px] font-black uppercase tracking-widest"
                            >
                                {uploading ? "Uploading..." : "Browse Files"}
                            </Button>
                        </div>
                        <div className="flex gap-2">
                            {['MEESHO', 'FLIPKART', 'AMAZON IN'].map(m => (
                                <Badge
                                    key={m}
                                    variant="outline"
                                    onClick={() => setSelectedMarketplace(m)}
                                    className={cn(
                                        "text-[9px] font-black px-3 py-1 cursor-pointer hover:bg-slate-50",
                                        selectedMarketplace === m && "border-indigo-500 text-indigo-600 bg-indigo-50"
                                    )}
                                >
                                    {m}
                                </Badge>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-none shadow-sm rounded-3xl">
                    <CardHeader>
                        <CardTitle className="text-sm font-black uppercase tracking-widest text-gray-400">Profit Distribution</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {[
                                { name: 'Shopify (Direct)', val: 65, color: 'bg-emerald-500' },
                                { name: 'Meesho', val: 18, color: 'bg-pink-500' },
                                { name: 'Flipkart', val: 12, color: 'bg-blue-500' },
                                { name: 'Others', val: 5, color: 'bg-slate-300' }
                            ].map((c) => (
                                <div key={c.name} className="space-y-1">
                                    <div className="flex justify-between text-[10px] font-bold text-gray-500">
                                        <span>{c.name}</span>
                                        <span>{c.val}%</span>
                                    </div>
                                    <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                                        <div className={cn("h-full rounded-full", c.color)} style={{ width: `${c.val}%` }} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* SKU Profitability Table */}
            <Card className="border-none shadow-sm rounded-3xl bg-white dark:bg-slate-900 overflow-hidden">
                <div className="p-4 border-b border-gray-50 dark:border-gray-800 flex items-center justify-between">
                    <div className="flex items-center gap-4 flex-1">
                        <CardTitle className="text-sm font-black uppercase tracking-widest text-gray-400">SKU Economics</CardTitle>
                        <div className="relative flex-1 max-w-sm">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-400" />
                            <Input placeholder="Search SKU..." className="pl-9 h-8 text-xs bg-slate-50 border-none rounded-lg" />
                        </div>
                    </div>
                    <div className="flex gap-2">
                        <Button variant="outline" size="sm" className="h-8 rounded-lg text-[10px] font-black uppercase tracking-widest"><Filter className="w-3 h-3 mr-1" /> Multi-channel</Button>
                        <Button variant="outline" size="sm" className="h-8 rounded-lg text-[10px] font-black uppercase tracking-widest"><Calendar className="w-3 h-3 mr-1" /> This Month</Button>
                    </div>
                </div>
                <CardContent className="p-0">
                    <table className="w-full text-left">
                        <thead className="bg-slate-50 dark:bg-slate-950 text-[10px] font-black text-gray-400 uppercase tracking-widest">
                            <tr>
                                <th className="px-6 py-4">SKU / Product</th>
                                <th className="px-6 py-4">Unit Sales</th>
                                <th className="px-6 py-4">Gross Revenue</th>
                                <th className="px-6 py-4">Net Margin</th>
                                <th className="px-6 py-4">RTO Impact</th>
                                <th className="px-6 py-4">Health</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-50 dark:divide-gray-800">
                            {profits.map((p) => (
                                <tr key={p.sku} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                                    <td className="px-6 py-4">
                                        <div className="space-y-0.5">
                                            <div className="text-sm font-black text-gray-900 dark:text-gray-100">{p.sku}</div>
                                            <div className="text-xs text-gray-400 font-medium">{p.name}</div>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 font-bold text-sm text-gray-700 dark:text-gray-300">{p.sales}</td>
                                    <td className="px-6 py-4 font-black text-sm text-gray-900 dark:text-gray-100">₹{p.revenue.toLocaleString()}</td>
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-2">
                                            <span className={cn("text-sm font-black", p.margin > 30 ? "text-emerald-600" : "text-amber-600")}>{p.margin}%</span>
                                            <div className="w-16 bg-slate-100 h-1 rounded-full">
                                                <div className={cn("h-full", p.margin > 30 ? "bg-emerald-500" : "bg-amber-500")} style={{ width: `${p.margin}%` }} />
                                            </div>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className={cn("text-xs font-bold", p.rto > 20 ? "text-rose-500" : "text-gray-500")}>-{p.rto}%</span>
                                    </td>
                                    <td className="px-6 py-4">{getStatusBadge(p.status)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </CardContent>
            </Card>
        </div>
    );
}
