'use client'

import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Activity, Shield, Users, Server, Globe, Database, Cpu, Zap } from 'lucide-react'

export default function DashboardOverview() {
  const stats = [
    {
      title: "System Status",
      value: "Healthy",
      description: "Gateway & Auth Online",
      icon: Shield,
      color: "text-green-500",
      bg: "bg-green-50 dark:bg-green-900/20"
    },
    {
      title: "Active Tenants",
      value: "5",
      description: "Across 4 brands",
      icon: Users,
      color: "text-blue-500",
      bg: "bg-blue-50 dark:bg-blue-900/20"
    },
    {
      title: "Total Users",
      value: "142",
      description: "+12 this week",
      icon: Activity,
      color: "text-purple-500",
      bg: "bg-purple-50 dark:bg-purple-900/20"
    },
    {
      title: "CPU Load",
      value: "12%",
      description: "Optimized limits",
      icon: Cpu,
      color: "text-amber-500",
      bg: "bg-amber-50 dark:bg-amber-900/20"
    }
  ]

  const services = [
    { name: "Brain Gateway", status: "Online", port: "8000", load: "Low" },
    { name: "Auth Service", status: "Online", port: "8008", load: "Stable" },
    { name: "AI Agents", status: "Online", port: "8009", load: "Idle" },
    { name: "PostgreSQL", status: "Online", port: "5432", load: "Stable" },
    { name: "Redis Cache", status: "Online", port: "6379", load: "Fast" },
    { name: "Traefik Proxy", status: "Online", port: "443", load: "Secure" },
  ]

  return (
    <div className="space-y-8">
      {/* Top Stats Row */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, i) => (
          <Card key={i} className="border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-slate-500 uppercase tracking-wider">
                {stat.title}
              </CardTitle>
              <div className={`p-2 rounded-lg ${stat.bg}`}>
                <stat.icon className={`h-4 w-4 ${stat.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold tracking-tight">{stat.value}</div>
              <p className="text-xs text-muted-foreground mt-1">
                {stat.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Service Grid Section */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="border-slate-200 dark:border-slate-800">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Server className="h-5 w-5 text-blue-500" />
              <CardTitle>Core Service Infrastructure</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="divide-y divide-slate-100 dark:divide-slate-800">
              {services.map((service, i) => (
                <div key={i} className="py-3 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full b-green-500 animate-pulse bg-green-500"></div>
                    <span className="font-medium text-sm">{service.name}</span>
                  </div>
                  <div className="flex items-center gap-4 text-xs">
                    <span className="text-slate-400">Port {service.port}</span>
                    <span className="px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-medium tracking-wide">
                      {service.load}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="border-slate-200 dark:border-slate-800 bg-slate-950 text-white overflow-hidden relative">
          <div className="absolute top-0 right-0 p-8 opacity-10">
            <Zap className="h-32 w-32" />
          </div>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-blue-400" />
              <CardTitle>Platform Performance</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <div className="flex justify-between text-xs font-medium text-slate-400">
                <span>API Response Time</span>
                <span className="text-blue-400">124ms avg</span>
              </div>
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-blue-500 w-[85%] rounded-full"></div>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs font-medium text-slate-400">
                <span>Database Connectivity</span>
                <span className="text-green-400">100% stable</span>
              </div>
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-green-500 w-[100%] rounded-full"></div>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs font-medium text-slate-400">
                <span>Storage Utilization</span>
                <span className="text-amber-400">24.2 GB / 100 GB</span>
              </div>
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-amber-500 w-[24%] rounded-full"></div>
              </div>
            </div>

            <div className="pt-4 grid grid-cols-2 gap-4">
              <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 text-center">
                <div className="text-lg font-bold text-blue-400">99.99%</div>
                <div className="text-[10px] text-slate-500 uppercase">Uptime</div>
              </div>
              <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 text-center">
                <div className="text-lg font-bold text-green-400">0</div>
                <div className="text-[10px] text-slate-500 uppercase">Incidents</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}