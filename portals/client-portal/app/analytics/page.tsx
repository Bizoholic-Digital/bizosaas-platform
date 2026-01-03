'use client';

import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/ui/dashboard-layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import {
  BarChart3, TrendingUp, Users, MousePointerClick,
  RefreshCcw, AlertTriangle, ShieldCheck, Globe,
  Activity, ArrowUpRight, ArrowDownRight
} from 'lucide-react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, AreaChart, Area, BarChart, Bar,
  Cell, PieChart, Pie
} from 'recharts';
import { brainApi } from '@/lib/brain-api';
import { badgeVariants } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

// Mock data for charts - in real app this would come from the API
const trafficData = [
  { name: 'Mon', views: 4000, users: 2400 },
  { name: 'Tue', views: 3000, users: 1398 },
  { name: 'Wed', views: 2000, users: 9800 },
  { name: 'Thu', views: 2780, users: 3908 },
  { name: 'Fri', views: 1890, users: 4800 },
  { name: 'Sat', views: 2390, users: 3800 },
  { name: 'Sun', views: 3490, users: 4300 },
];

const sourceData = [
  { name: 'Direct', value: 400, color: '#3b82f6' },
  { name: 'Social', value: 300, color: '#10b981' },
  { name: 'Organic', value: 300, color: '#f59e0b' },
  { name: 'Referral', value: 200, color: '#8b5cf6' },
];

export default function AnalyticsPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchOverview = async () => {
    setLoading(true);
    try {
      const overview = await brainApi.analytics.getOverview();
      setData(overview);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch analytics:', err);
      setError('Could not connect to analytics service');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOverview();
  }, []);

  if (loading && !data) {
    return (
      <DashboardLayout title="Analytics Dashboard" description="Loading your business intelligence...">
        <div className="p-6 space-y-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {[...Array(4)].map((_, i) => (
              <Card key={i} className="animate-pulse">
                <CardHeader className="h-20 bg-slate-50 dark:bg-slate-900/50" />
                <CardContent className="h-16" />
              </Card>
            ))}
          </div>
          <Card className="h-[400px] animate-pulse bg-slate-50 dark:bg-slate-900/50" />
        </div>
      </DashboardLayout>
    );
  }

  const metrics = data?.metrics || {
    pageViews: 0,
    uniqueVisitors: 0,
    conversions: 0,
    revenue: 0,
    bounceRate: '0%',
    avgSessionDuration: '0m'
  };

  return (
    <DashboardLayout title="Analytics Dashboard" description="Aggregated business performance across all sources">
      <div className="p-6 space-y-6">
        {/* Source Status Bar */}
        <div className="flex flex-wrap gap-2 items-center bg-white dark:bg-slate-900 p-3 rounded-lg border border-slate-200 dark:border-slate-800">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider mr-2">Connected Sources:</span>
          {data?.sources?.map((source: any) => (
            <div key={source.id} className={cn(
              "flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-bold border transition-all",
              source.connected
                ? "bg-green-50 text-green-700 border-green-200 dark:bg-green-900/20 dark:text-green-400 dark:border-green-800"
                : "bg-slate-50 text-slate-400 border-slate-200 dark:bg-slate-800/50 dark:text-slate-500 dark:border-slate-800"
            )}>
              {source.connected ? <ShieldCheck className="w-3 h-3" /> : <RefreshCcw className="w-3 h-3" />}
              {source.name}
            </div>
          ))}
          <button
            onClick={fetchOverview}
            className="ml-auto p-1.5 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-md transition-colors"
          >
            <RefreshCcw className={cn("w-4 h-4 text-slate-400", loading && "animate-spin")} />
          </button>
        </div>

        {error && (
          <div className="bg-amber-50 border border-amber-200 text-amber-800 px-4 py-3 rounded-lg flex items-center gap-3">
            <AlertTriangle className="w-5 h-5" />
            <p className="text-sm font-medium">{error}</p>
          </div>
        )}

        {/* Main KPIs */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            title="Total Page Views"
            value={metrics.pageViews.toLocaleString()}
            icon={<Globe className="w-4 h-4" />}
            trend="+12.5%"
            positive={true}
          />
          <MetricCard
            title="Unique Visitors"
            value={metrics.uniqueVisitors.toLocaleString()}
            icon={<Users className="w-4 h-4" />}
            trend="+8.2%"
            positive={true}
          />
          <MetricCard
            title="Total Revenue"
            value={`$${metrics.revenue.toLocaleString()}`}
            icon={<TrendingUp className="w-4 h-4" />}
            trend="+22.4%"
            positive={true}
          />
          <MetricCard
            title="Conversions"
            value={metrics.conversions.toLocaleString()}
            icon={<MousePointerClick className="w-4 h-4" />}
            trend="-2.1%"
            positive={false}
          />
        </div>

        {/* Charts Section */}
        <div className="grid gap-6 lg:grid-cols-3">
          <Card className="lg:col-span-2 border-slate-200 dark:border-slate-800 overflow-hidden group">
            <CardHeader className="pb-2">
              <div className="flex justify-between items-center">
                <div>
                  <CardTitle className="text-lg font-bold">Traffic Growth</CardTitle>
                  <CardDescription>Views vs Users over the last 7 days</CardDescription>
                </div>
                <div className="flex gap-2">
                  <div className="flex items-center gap-1.5 text-xs font-medium text-blue-500">
                    <div className="w-2 h-2 rounded-full bg-blue-500" /> Views
                  </div>
                  <div className="flex items-center gap-1.5 text-xs font-medium text-indigo-400">
                    <div className="w-2 h-2 rounded-full bg-indigo-400" /> Users
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent className="pt-4">
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={trafficData}>
                    <defs>
                      <linearGradient id="colorViews" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.1} />
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                    <XAxis
                      dataKey="name"
                      axisLine={false}
                      tickLine={false}
                      tick={{ fill: '#94a3b8', fontSize: 12 }}
                      dy={10}
                    />
                    <YAxis
                      axisLine={false}
                      tickLine={false}
                      tick={{ fill: '#94a3b8', fontSize: 12 }}
                    />
                    <Tooltip
                      contentStyle={{
                        borderRadius: '12px',
                        border: 'none',
                        boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
                        backgroundColor: '#fff'
                      }}
                    />
                    <Area
                      type="monotone"
                      dataKey="views"
                      stroke="#3b82f6"
                      strokeWidth={3}
                      fillOpacity={1}
                      fill="url(#colorViews)"
                    />
                    <Area
                      type="monotone"
                      dataKey="users"
                      stroke="#818cf8"
                      strokeWidth={2}
                      strokeDasharray="5 5"
                      fill="transparent"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card className="border-slate-200 dark:border-slate-800">
            <CardHeader>
              <CardTitle className="text-lg font-bold">Traffic Source</CardTitle>
              <CardDescription>Acquisition breakdown</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[250px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={sourceData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={80}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {sourceData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 grid grid-cols-2 gap-4">
                {sourceData.map((item) => (
                  <div key={item.name} className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color }} />
                    <span className="text-xs font-bold text-slate-600 dark:text-slate-400">{item.name}</span>
                    <span className="text-xs font-bold ml-auto">{item.value}%</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Secondary Metrics */}
        <div className="grid gap-6 md:grid-cols-2">
          <Card className="border-slate-200 dark:border-slate-800">
            <CardHeader>
              <CardTitle className="text-sm font-bold uppercase tracking-widest text-slate-500">Live Activity Feed</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-4 p-3 rounded-lg bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-800">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                <div className="flex-1">
                  <p className="text-sm font-bold">New user session started</p>
                  <p className="text-xs text-slate-500">Organic Search • London, UK</p>
                </div>
                <span className="text-[10px] font-bold text-slate-400">JUST NOW</span>
              </div>
              <div className="flex items-center gap-4 p-3 rounded-lg border border-transparent">
                <div className="w-2 h-2 rounded-full bg-blue-400" />
                <div className="flex-1">
                  <p className="text-sm font-bold">Page View: /dashboard/cms</p>
                  <p className="text-xs text-slate-500">Returning User • Chrome / MacOS</p>
                </div>
                <span className="text-[10px] font-bold text-slate-400">2M AGO</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-slate-200 dark:border-slate-800 bg-gradient-to-br from-indigo-600 to-blue-700 text-white shadow-xl shadow-blue-200/20 dark:shadow-none">
            <CardContent className="p-8 flex flex-col justify-between h-full">
              <div>
                <Activity className="w-8 h-8 mb-4 opacity-80" />
                <h3 className="text-2xl font-bold mb-2">Predictive Insight</h3>
                <p className="text-indigo-100 text-sm leading-relaxed">
                  Based on current traffic patterns, your conversions are expected to increase by <span className="font-bold text-white">14%</span> over the next 48 hours.
                  We recommend optimizing your <strong>Wagtail</strong> landing pages for better mobile retention.
                </p>
              </div>
              <div className="mt-8">
                <button className="w-full py-3 bg-white text-blue-700 font-bold rounded-xl text-sm hover:bg-indigo-50 transition-colors shadow-lg">
                  View Optimization Report
                </button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}

function MetricCard({ title, value, icon, trend, positive }: any) {
  return (
    <Card className="border-slate-200 dark:border-slate-800 hover:shadow-lg transition-all group">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-xs font-bold text-slate-500 uppercase tracking-wider">{title}</CardTitle>
        <div className="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg group-hover:bg-blue-600 group-hover:text-white transition-colors">
          {icon}
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">{value}</div>
        <div className="flex items-center mt-2">
          {positive ? (
            <ArrowUpRight className="w-4 h-4 text-green-500 mr-1" />
          ) : (
            <ArrowDownRight className="w-4 h-4 text-red-500 mr-1" />
          )}
          <span className={cn("text-xs font-bold", positive ? "text-green-500" : "text-red-500")}>
            {trend}
          </span>
          <span className="text-[10px] font-medium text-slate-400 ml-2 uppercase">vs last month</span>
        </div>
      </CardContent>
    </Card>
  );
}
