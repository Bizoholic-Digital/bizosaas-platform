'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Users, Target, TrendingUp, Filter, Search, MoreVertical } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { useSetHeader } from '@/lib/contexts/HeaderContext';

export default function GlobalCRMPage() {
    useSetHeader("Global CRM Monitor", "Centralized visibility into customer relations across the platform.");

    return (
        <div className="p-6 space-y-6">
            <div className="grid gap-4 md:grid-cols-3">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Global Leads</CardTitle>
                        <Users className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">12,458</div>
                        <p className="text-xs text-muted-foreground">+180 from last 24h</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Global Conversions</CardTitle>
                        <Target className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">4.2%</div>
                        <p className="text-xs text-muted-foreground">+0.5% from last month</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Potential Revenue</CardTitle>
                        <TrendingUp className="h-4 w-4 text-emerald-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">$1.2M</div>
                        <p className="text-xs text-muted-foreground">In pipeline across all tenants</p>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <div>
                            <CardTitle>Global Lead Activity</CardTitle>
                            <CardDescription>Live feed of CRM interactions across the network</CardDescription>
                        </div>
                        <div className="flex gap-2">
                            <div className="relative">
                                <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                                <Input placeholder="Search emails..." className="pl-9 w-64 h-9" />
                            </div>
                            <Button variant="outline" size="sm">
                                <Filter className="w-4 h-4 mr-2" />
                                Filter
                            </Button>
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="rounded-md border">
                        <table className="w-full text-sm">
                            <thead className="bg-slate-50 dark:bg-slate-900 border-b">
                                <tr>
                                    <th className="text-left p-4 font-medium uppercase tracking-tighter text-[10px] text-slate-500">Contact</th>
                                    <th className="text-left p-4 font-medium uppercase tracking-tighter text-[10px] text-slate-500">Tenant</th>
                                    <th className="text-left p-4 font-medium uppercase tracking-tighter text-[10px] text-slate-500">Source</th>
                                    <th className="text-left p-4 font-medium uppercase tracking-tighter text-[10px] text-slate-500">Last Action</th>
                                    <th className="text-right p-4 font-medium uppercase tracking-tighter text-[10px] text-slate-500">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y">
                                {[
                                    { email: 'user@example.com', tenant: 'Bizo-Main', source: 'FluentCRM', action: 'Form Submit', time: '2m ago' },
                                    { email: 'client@gmail.com', tenant: 'Agency-X', source: 'HubSpot', action: 'Email Open', time: '15m ago' },
                                    { email: 'lead@sales.io', tenant: 'Retail-Corp', source: 'Custom MCP', action: 'Chat Connect', time: '1h ago' }
                                ].map((row, i) => (
                                    <tr key={i} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                                        <td className="p-4 font-bold">{row.email}</td>
                                        <td className="p-4"><Badge variant="outline" className="font-bold">{row.tenant}</Badge></td>
                                        <td className="p-4 text-slate-500">{row.source}</td>
                                        <td className="p-4">
                                            <div className="flex flex-col">
                                                <span className="font-medium">{row.action}</span>
                                                <span className="text-[10px] text-slate-400">{row.time}</span>
                                            </div>
                                        </td>
                                        <td className="p-4 text-right">
                                            <Button variant="ghost" size="icon"><MoreVertical className="w-4 h-4" /></Button>
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
