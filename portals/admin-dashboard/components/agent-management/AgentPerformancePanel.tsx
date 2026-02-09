'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import {
    LineChart,
    Line,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    AreaChart,
    Area,
    PieChart,
    Pie,
    Cell
} from 'recharts';
import { ArrowUpRight, ArrowDownRight, TrendingUp, DollarSign, Activity } from 'lucide-react';

// Mock data generator
const generateDailyData = (days: number) => {
    const data = [];
    const now = new Date();
    for (let i = days; i >= 0; i--) {
        const date = new Date(now);
        date.setDate(date.getDate() - i);
        data.push({
            date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
            ctr: (Math.random() * 5 + 2).toFixed(2), // 2-7%
            conversion: (Math.random() * 3 + 1).toFixed(2), // 1-4%
            revenue: Math.floor(Math.random() * 1000 + 500),
            tasks: Math.floor(Math.random() * 100 + 50),
            errors: Math.floor(Math.random() * 5),
        });
    }
    return data;
};

const DATA = generateDailyData(14); // Last 14 days

const SUCCESS_METRICS = [
    { name: 'Successful', value: 85, color: '#22c55e' },
    { name: 'Failed', value: 5, color: '#ef4444' },
    { name: 'Retried', value: 10, color: '#eab308' },
];

export function AgentPerformancePanel({ agentId }: { agentId: string }) {
    return (
        <div className="space-y-6">
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <KPICard
                    title="Total Revenue"
                    value="$12,450"
                    change="+12.5%"
                    trend="up"
                    icon={DollarSign}
                    color="text-green-600 bg-green-50"
                />
                <KPICard
                    title="Avg. CTR"
                    value="4.2%"
                    change="+0.8%"
                    trend="up"
                    icon={TrendingUp}
                    color="text-blue-600 bg-blue-50"
                />
                <KPICard
                    title="Conversion Rate"
                    value="2.8%"
                    change="-0.3%"
                    trend="down"
                    icon={Activity}
                    color="text-purple-600 bg-purple-50"
                />
                <KPICard
                    title="Task Success"
                    value="98.5%"
                    change="+0.2%"
                    trend="up"
                    icon={ArrowUpRight}
                    color="text-orange-600 bg-orange-50"
                />
            </div>

            {/* Charts Row 1 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>CTR & Conversion Trends</CardTitle>
                        <CardDescription>Daily performance over the last 14 days</CardDescription>
                    </CardHeader>
                    <CardContent className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={DATA}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                <XAxis dataKey="date" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis yAxisId="left" fontSize={12} tickLine={false} axisLine={false} unit="%" />
                                <YAxis yAxisId="right" orientation="right" fontSize={12} tickLine={false} axisLine={false} unit="%" />
                                <Tooltip
                                    contentStyle={{ backgroundColor: 'white', borderRadius: '8px', border: '1px solid #e5e7eb' }}
                                />
                                <Legend />
                                <Line yAxisId="left" type="monotone" dataKey="ctr" name="CTR" stroke="#3b82f6" strokeWidth={2} dot={false} />
                                <Line yAxisId="right" type="monotone" dataKey="conversion" name="Conversion" stroke="#8b5cf6" strokeWidth={2} dot={false} />
                            </LineChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Revenue Generation</CardTitle>
                        <CardDescription>Daily revenue attributed to this agent</CardDescription>
                    </CardHeader>
                    <CardContent className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={DATA}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                <XAxis dataKey="date" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `$${value}`} />
                                <Tooltip
                                    cursor={{ fill: '#f3f4f6' }}
                                    contentStyle={{ backgroundColor: 'white', borderRadius: '8px', border: '1px solid #e5e7eb' }}
                                />
                                <Bar dataKey="revenue" name="Revenue" fill="#22c55e" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>
            </div>

            {/* Charts Row 2 */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="md:col-span-1">
                    <CardHeader>
                        <CardTitle>Task Execution Breakdown</CardTitle>
                    </CardHeader>
                    <CardContent className="h-[250px] relative">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={SUCCESS_METRICS}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={80}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {SUCCESS_METRICS.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                                <Tooltip />
                                <Legend verticalAlign="bottom" height={36} />
                            </PieChart>
                        </ResponsiveContainer>
                        <div className="absolute inset-0 flex items-center justify-center pointer-events-none pb-8">
                            <div className="text-center">
                                <span className="text-3xl font-bold text-gray-900">98%</span>
                                <p className="text-xs text-gray-500">Success</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="md:col-span-2">
                    <CardHeader>
                        <CardTitle>Resource Efficiency</CardTitle>
                        <CardDescription>Tasks processed vs Error rate</CardDescription>
                    </CardHeader>
                    <CardContent className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={DATA}>
                                <defs>
                                    <linearGradient id="colorTasks" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.8} />
                                        <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                <XAxis dataKey="date" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis fontSize={12} tickLine={false} axisLine={false} />
                                <Tooltip />
                                <Area type="monotone" dataKey="tasks" stroke="#0ea5e9" fillOpacity={1} fill="url(#colorTasks)" />
                                <Line type="monotone" dataKey="errors" stroke="#ef4444" strokeWidth={2} dot={false} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}

function KPICard({ title, value, change, trend, icon: Icon, color }: any) {
    return (
        <Card>
            <CardContent className="p-6">
                <div className="flex items-center justify-between pb-2">
                    <p className="text-sm font-medium text-gray-500">{title}</p>
                    <div className={`p-2 rounded-lg ${color}`}>
                        <Icon className="w-4 h-4" />
                    </div>
                </div>
                <div className="flex items-baseline space-x-2">
                    <h3 className="text-2xl font-bold">{value}</h3>
                    <span className={`text-xs font-medium flex items-center ${trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                        {trend === 'up' ? <ArrowUpRight className="w-3 h-3 mr-1" /> : <ArrowDownRight className="w-3 h-3 mr-1" />}
                        {change}
                    </span>
                </div>
            </CardContent>
        </Card>
    );
}
