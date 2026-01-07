'use client'

import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Activity, Shield, Users, Server, Globe, Database, Cpu, Zap, Brain, Layout, ShoppingCart } from 'lucide-react'
import { useSystemStatus } from '@/lib/hooks/useSystemStatus'
import { Progress } from '../ui/progress'

export default function DashboardOverview() {
  const { metrics, isLoading, getOverallHealth } = useSystemStatus();
  const health = getOverallHealth();

  const stats = [
    {
      title: "System Status",
      value: health.toUpperCase(),
      description: health === 'healthy' ? "All systems operational" : "Subsystem issues detected",
      icon: Shield,
      color: health === 'healthy' ? "text-green-500" : health === 'warning' ? "text-yellow-500" : "text-red-500",
      bg: health === 'healthy' ? "bg-green-50 dark:bg-green-900/20" : health === 'warning' ? "bg-yellow-50 dark:bg-yellow-900/20" : "bg-red-50 dark:bg-red-900/20"
    },
    {
      title: "Active Tenants",
      value: "5",
      description: "Across 4 brands",
      icon: Globe,
      color: "text-blue-500",
      bg: "bg-blue-50 dark:bg-blue-900/20"
    },
    {
      title: "Total Users",
      value: "142",
      description: "+12 this week",
      icon: Users,
      color: "text-purple-500",
      bg: "bg-purple-50 dark:bg-purple-900/20"
    },
    {
      title: "CPU Load",
      value: `${metrics.cpu}%`,
      description: "Optimized limits",
      icon: Cpu,
      color: "text-amber-500",
      bg: "bg-amber-50 dark:bg-amber-900/20"
    }
  ]

  const serviceIcons: Record<string, any> = {
    'Brain Hub': Brain,
    'CRM': Users,
    'CMS': Layout,
    'E-commerce': ShoppingCart,
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-700 slide-in-from-bottom-4">
      {/* Top Stats Row */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, i) => (
          <Card key={i} className="border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-semibold text-slate-500 uppercase tracking-wider">
                {stat.title}
              </CardTitle>
              <div className={`p-2 rounded-lg ${stat.bg}`}>
                <stat.icon className={`h-4 w-4 ${stat.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">{stat.value}</div>
              <p className="text-xs text-muted-foreground mt-1">
                {stat.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Service Grid Section */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="border-slate-200 dark:border-slate-800 shadow-sm">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Server className="h-5 w-5 text-indigo-500" />
              <CardTitle>Core Service Infrastructure</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="divide-y divide-slate-100 dark:divide-slate-800">
              {Object.entries(metrics.services).map(([name, status], i) => {
                const Icon = serviceIcons[name] || Activity;
                return (
                  <div key={i} className="py-4 flex items-center justify-between group cursor-default">
                    <div className="flex items-center gap-4">
                      <div className={`p-2 rounded-full ${status === 'healthy' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
                        <Icon className="h-5 w-5" />
                      </div>
                      <div>
                        <span className="font-semibold text-sm block text-slate-900 dark:text-white">{name}</span>
                        <span className="text-[10px] text-muted-foreground">Regional Gateway</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-6">
                      <div className="text-right hidden sm:block">
                        <div className="text-xs font-medium text-muted-foreground">Stability</div>
                        <div className="text-[14px] font-bold text-slate-900 dark:text-white">100%</div>
                      </div>
                      <div className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest ${status === 'healthy' ? 'bg-green-500 text-white shadow-sm shadow-green-200' : 'bg-red-500 text-white shadow-sm shadow-red-200'}`}>
                        {status === 'healthy' ? 'Online' : 'Offline'}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        <Card className="border-slate-200 dark:border-slate-800 bg-slate-900 text-white overflow-hidden relative shadow-lg">
          <div className="absolute top-0 right-0 p-8 opacity-10">
            <Zap className="h-32 w-32 text-indigo-400" />
          </div>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-indigo-400" />
              <CardTitle>Platform Performance</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-6 relative z-10">
            <div className="space-y-2">
              <div className="flex justify-between text-xs font-semibold text-slate-400 uppercase tracking-tighter">
                <span>API Response Latency</span>
                <span className="text-blue-400">124ms avg</span>
              </div>
              <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-blue-600 to-indigo-500 w-[85%] rounded-full shadow-[0_0_10px_rgba(59,130,246,0.5)]"></div>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs font-semibold text-slate-400 uppercase tracking-tighter">
                <span>Database Connectivity</span>
                <span className="text-green-400">100% stable</span>
              </div>
              <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-green-600 to-emerald-400 w-[100%] rounded-full shadow-[0_0_10px_rgba(16,185,129,0.5)]"></div>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs font-semibold text-slate-400 uppercase tracking-tighter">
                <span>Global Traffic Load</span>
                <span className="text-indigo-400">{metrics.apiRequests} requests/sec</span>
              </div>
              <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-indigo-600 to-purple-500 w-[45%] rounded-full shadow-[0_0_10px_rgba(99,102,241,0.5)]"></div>
              </div>
            </div>

            <div className="pt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm text-center">
                <div className="text-2xl font-black text-blue-400">99.99%</div>
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-1">Uptime</div>
              </div>
              <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm text-center">
                <div className="text-2xl font-black text-green-400">0</div>
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-1">Incidents</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}