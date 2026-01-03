'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import {
    BarChart3,
    TrendingUp,
    DollarSign,
    Users,
    Activity,
    ArrowUpRight,
    ArrowDownRight,
    Zap,
    Globe,
    CreditCard
} from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    LineChart,
    Line,
    AreaChart,
    Area
} from 'recharts';

const mockRevenueData = [
    { month: 'Jan', revenue: 45000, users: 120, events: 15000 },
    { month: 'Feb', revenue: 52000, users: 145, events: 18000 },
    { month: 'Mar', revenue: 48000, users: 160, events: 21000 },
    { month: 'Apr', revenue: 61000, users: 190, events: 25000 },
    { month: 'May', revenue: 75000, users: 230, events: 32000 },
    { month: 'Jun', revenue: 89000, users: 280, events: 45000 },
];

const topTenants = [
    { name: 'Acme Corp', revenue: '$12,450', growth: '+12%', status: 'Active' },
    { name: 'Global Tech', revenue: '$8,900', growth: '+8%', status: 'Active' },
    { name: 'Local Shop', revenue: '$4,200', growth: '+25%', status: 'Trial' },
    { name: 'Digital Nomads', revenue: '$3,800', growth: '-2%', status: 'Active' },
];

export default function RevenueDashboard() {
    return (
        <div className="p-8 space-y-8">
            <div className="flex flex-col gap-2">
                <h1 className="text-3xl font-bold tracking-tight">Platform Economics</h1>
                <p className="text-muted-foreground">Monitor global revenue, usage-based billing, and multi-tenant performance.</p>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card className="bg-slate-900 border-slate-800 text-white">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium text-slate-400">Total ARR</CardTitle>
                        <DollarSign className="w-4 h-4 text-emerald-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">$1.2M</div>
                        <p className="text-xs text-emerald-400 flex items-center mt-1">
                            <ArrowUpRight className="w-3 h-3 mr-1" /> +18.2% from last month
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Usage Revenue (Lago)</CardTitle>
                        <Zap className="w-4 h-4 text-blue-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">$42,350</div>
                        <p className="text-xs text-muted-foreground flex items-center mt-1">
                            8.2M billable events this month
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Active Tenants</CardTitle>
                        <Users className="w-4 h-4 text-purple-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">1,284</div>
                        <p className="text-xs text-emerald-600 flex items-center mt-1">
                            <ArrowUpRight className="w-3 h-3 mr-1" /> +42 new this week
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Churn Rate</CardTitle>
                        <Activity className="w-4 h-4 text-orange-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">1.2%</div>
                        <p className="text-xs text-emerald-600 flex items-center mt-1">
                            <ArrowDownRight className="w-3 h-3 mr-1" /> -0.4% improvement
                        </p>
                    </CardContent>
                </Card>
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <Card className="lg:col-span-2">
                    <CardHeader>
                        <CardTitle>Revenue Forecast</CardTitle>
                        <CardDescription>Monthly recurring revenue vs usage-based billing</CardDescription>
                    </CardHeader>
                    <CardContent className="h-[350px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={mockRevenueData}>
                                <defs>
                                    <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.1} />
                                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} opacity={0.2} />
                                <XAxis dataKey="month" axisLine={false} tickLine={false} />
                                <YAxis axisLine={false} tickLine={false} tickFormatter={(v) => `$${v / 1000}k`} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#fff', borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                                />
                                <Area type="monotone" dataKey="revenue" stroke="#3b82f6" fillOpacity={1} fill="url(#colorRev)" strokeWidth={3} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Top Revenue Tenants</CardTitle>
                        <CardDescription>Global leaders by billing volume</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-6">
                            {topTenants.map((tenant, i) => (
                                <div key={i} className="flex items-center justify-between">
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-xs font-bold">
                                            {tenant.name[0]}
                                        </div>
                                        <div>
                                            <p className="text-sm font-semibold">{tenant.name}</p>
                                            <Badge variant="outline" className="text-[10px] py-0">{tenant.status}</Badge>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-sm font-bold">{tenant.revenue}</p>
                                        <p className="text-xs text-emerald-600">{tenant.growth}</p>
                                    </div>
                                </div>
                            ))}
                            <button className="w-full text-center text-sm text-blue-600 font-medium py-2 hover:underline">
                                View Tenant Analytics
                            </button>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Regional Performance */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardHeader className="pb-2">
                        <div className="flex items-center gap-2">
                            <Globe className="w-4 h-4 text-slate-400" />
                            <CardTitle className="text-sm font-medium">North America</CardTitle>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="text-xl font-bold">$742k</div>
                        <Progress value={65} className="h-1.5 mt-2" />
                        <p className="text-[10px] text-muted-foreground mt-2">61% of total revenue</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="pb-2">
                        <div className="flex items-center gap-2">
                            <Globe className="w-4 h-4 text-slate-400" />
                            <CardTitle className="text-sm font-medium">Europe (GDPR compliant)</CardTitle>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="text-xl font-bold">$285k</div>
                        <Progress value={25} className="h-1.5 mt-2" />
                        <p className="text-[10px] text-muted-foreground mt-2">24% of total revenue</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="pb-2">
                        <div className="flex items-center gap-2">
                            <Globe className="w-4 h-4 text-slate-400" />
                            <CardTitle className="text-sm font-medium">LATAM / Asia</CardTitle>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="text-xl font-bold">$173k</div>
                        <Progress value={15} className="h-1.5 mt-2" />
                        <p className="text-[10px] text-muted-foreground mt-2">15% of total revenue</p>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}

function Progress({ value, className }: { value: number, className?: string }) {
    return (
        <div className={`w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden ${className}`}>
            <div
                className="bg-blue-600 h-full transition-all duration-500"
                style={{ width: `${value}%` }}
            />
        </div>
    );
}
