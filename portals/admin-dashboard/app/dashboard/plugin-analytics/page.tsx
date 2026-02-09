'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { connectorsApi } from '@/lib/api/connectors';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    LineChart, Line, Cell
} from 'recharts';
import { RefreshCw, TrendingUp, TrendingDown, Eye, MousePointer2, Download, Star } from 'lucide-react';
import { toast } from 'sonner';

export default function PluginAnalyticsPage() {
    const [metrics, setMetrics] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const loadMetrics = async () => {
        setLoading(true);
        try {
            const res = await connectorsApi.getMarketplaceMetrics();
            if (res.data) {
                setMetrics(res.data);
            }
        } catch (error) {
            toast.error("Failed to load plugin metrics");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadMetrics();
    }, []);

    if (loading) return (
        <div className="flex items-center justify-center p-12">
            <RefreshCw className="h-8 w-8 animate-spin text-primary" />
        </div>
    );

    const totalViews = metrics?.reduce((acc, curr) => acc + (curr?.views || 0), 0) || 0;
    const totalClicks = metrics?.reduce((acc, curr) => acc + (curr?.clicks || 0), 0) || 0;
    const avgConversion = totalViews > 0 ? ((totalClicks / totalViews) * 100).toFixed(1) : "0.0";

    const topRequested = metrics.length > 0
        ? [...metrics].sort((a, b) => (b.demand_score || 0) - (a.demand_score || 0))[0]
        : null;

    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Plugin & Theme Marketplace</h1>
                    <p className="text-muted-foreground">Manage platform extensions and monitor installation demand.</p>
                </div>
                <div className="flex gap-2">
                    <Button onClick={loadMetrics} variant="outline">
                        <RefreshCw className="mr-2 h-4 w-4" /> Refresh Data
                    </Button>
                    <Button>
                        <Download className="mr-2 h-4 w-4" /> Add New Asset
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Total Views</CardTitle>
                        <Eye className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{totalViews}</div>
                        <p className="text-xs text-muted-foreground">+20.1% from last month</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Interest (Clicks)</CardTitle>
                        <MousePointer2 className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{totalClicks}</div>
                        <p className="text-xs text-muted-foreground">+12% from last month</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
                        <TrendingUp className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{avgConversion}%</div>
                        <p className="text-xs text-muted-foreground">+2% growth</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Top Requested</CardTitle>
                        <Star className="h-4 w-4 text-yellow-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold truncate">{topRequested?.name || 'N/A'}</div>
                        <p className="text-xs text-muted-foreground">Highest demand score</p>
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>Demand by Plugin</CardTitle>
                        <CardDescription>Views vs Clicks per specialized connector</CardDescription>
                    </CardHeader>
                    <CardContent className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={metrics}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="views" fill="#8884d8" name="Views" />
                                <Bar dataKey="clicks" fill="#82ca9d" name="Interests" />
                            </BarChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Strategy Prioritization</CardTitle>
                        <CardDescription>Demand Score based on intent levels</CardDescription>
                    </CardHeader>
                    <CardContent className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={metrics} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis type="number" />
                                <YAxis dataKey="name" type="category" width={100} />
                                <Tooltip />
                                <Bar dataKey="demand_score" name="Demand Score">
                                    {metrics.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.demand_score > 80 ? '#ef4444' : '#3b82f6'} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Detailed Breakdown</CardTitle>
                    <CardDescription>Raw metrics for individual plugin requests.</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="relative w-full overflow-auto">
                        <table className="w-full caption-bottom text-sm">
                            <thead className="[&_tr]:border-b">
                                <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Plugin Name</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Views</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Interests</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Install Attempts</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Trend</th>
                                    <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Demand Score</th>
                                </tr>
                            </thead>
                            <tbody className="[&_tr:last-child]:border-0">
                                {metrics.map((m) => (
                                    <tr key={m.slug} className="border-b transition-colors hover:bg-muted/50">
                                        <td className="p-4 align-middle font-medium">
                                            <div className="flex flex-col">
                                                <span>{m.name}</span>
                                                <span className="text-[10px] text-muted-foreground uppercase">{m.category || 'Plugin'}</span>
                                            </div>
                                        </td>
                                        <td className="p-4 align-middle">{m.views || 0}</td>
                                        <td className="p-4 align-middle">{m.clicks || 0}</td>
                                        <td className="p-4 align-middle text-center">{m.install_attempts || 0}</td>
                                        <td className="p-4 align-middle">
                                            <div className="flex items-center gap-1">
                                                {(m.trend || '').startsWith('+') ? <TrendingUp className="h-3 w-3 text-green-500" /> : <TrendingDown className="h-3 w-3 text-red-500" />}
                                                <span className={(m.trend || '').startsWith('+') ? 'text-green-600' : 'text-red-600'}>{m.trend || '0%'}</span>
                                            </div>
                                        </td>
                                        <td className="p-4 align-middle">
                                            <Badge variant={m.demand_score > 80 ? 'default' : 'secondary'} className={m.demand_score > 80 ? 'bg-red-500 hover:bg-red-600' : ''}>
                                                {m.demand_score || 0}
                                            </Badge>
                                        </td>
                                        <td className="p-4 align-middle text-right">
                                            <Button variant="ghost" size="sm">Manage</Button>
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
