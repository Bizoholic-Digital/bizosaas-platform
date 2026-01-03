'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
    Search,
    Plus,
    Settings2,
    Bot,
    Cpu,
    ShieldCheck,
    Zap,
    Eye,
    Power,
    Activity,
    BrainCircuit,
    Layers,
    Server,
    ExternalLink
} from 'lucide-react';

const mockAgents = [
    {
        id: 'seo-expert',
        name: 'SEO Strategist',
        category: 'Marketing',
        status: 'Active',
        uptime: '99.9%',
        load: '12%',
        tasks: 1240,
        version: 'v2.4.0',
        color: 'blue'
    },
    {
        id: 'marketing-strategist',
        name: 'Marketing Orchestrator',
        category: 'Strategy',
        status: 'Active',
        uptime: '100%',
        load: '45%',
        tasks: 310,
        version: 'v1.2.1',
        color: 'purple'
    },
    {
        id: 'compliance-agent',
        name: 'Privacy & GDPR Expert',
        category: 'Legal',
        status: 'Active',
        uptime: '98.5%',
        load: '5%',
        tasks: 45,
        version: 'v0.9.0',
        color: 'emerald'
    },
    {
        id: 'social-media-bot',
        name: 'Social Auto-Pilot',
        category: 'Social',
        status: 'Inactive',
        uptime: '0%',
        load: '0%',
        tasks: 0,
        version: 'v1.0.0',
        color: 'orange'
    },
];

export default function AdminAgentsPage() {
    const [searchTerm, setSearchTerm] = useState('');

    return (
        <div className="p-8 space-y-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">AI Agent Fleet</h1>
                    <p className="text-muted-foreground">Manage global AI worker profiles, deployment versions, and system-wide utilization.</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline">
                        <Cpu className="w-4 h-4 mr-2" />
                        Cluster Monitor
                    </Button>
                    <Button className="bg-blue-600 hover:bg-blue-700">
                        <Plus className="w-4 h-4 mr-2" />
                        Deploy New Agent
                    </Button>
                </div>
            </div>

            {/* Platform Health Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center gap-3">
                            <div className="p-2 rounded-lg bg-blue-50 text-blue-600">
                                <Server className="w-5 h-5" />
                            </div>
                            <div>
                                <p className="text-xs font-medium text-muted-foreground uppercase">Nodes Active</p>
                                <p className="text-xl font-bold">12 / 12</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center gap-3">
                            <div className="p-2 rounded-lg bg-emerald-50 text-emerald-600">
                                <Zap className="w-5 h-5" />
                            </div>
                            <div>
                                <p className="text-xs font-medium text-muted-foreground uppercase">Total Throughput</p>
                                <p className="text-xl font-bold">450 tps</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center gap-3">
                            <div className="p-2 rounded-lg bg-purple-50 text-purple-600">
                                <BrainCircuit className="w-5 h-5" />
                            </div>
                            <div>
                                <p className="text-xs font-medium text-muted-foreground uppercase">Model Latency</p>
                                <p className="text-xl font-bold">84ms</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center gap-3">
                            <div className="p-2 rounded-lg bg-orange-50 text-orange-600">
                                <Activity className="w-5 h-5" />
                            </div>
                            <div>
                                <p className="text-xs font-medium text-muted-foreground uppercase">Error Rate</p>
                                <p className="text-xl font-bold">0.02%</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Search and Filters */}
            <div className="flex items-center gap-4">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <Input
                        placeholder="Search agents by name, capability, or tenant distribution..."
                        className="pl-10"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <Button variant="outline">
                    <Layers className="w-4 h-4 mr-2" />
                    By Category
                </Button>
                <Button variant="outline">
                    <ShieldCheck className="w-4 h-4 mr-2" />
                    Compliance Only
                </Button>
            </div>

            {/* Agents Table */}
            <Card>
                <CardHeader className="pb-0">
                    <CardTitle>Global Registry</CardTitle>
                    <CardDescription>24 agent definitions across 8 specialized domains.</CardDescription>
                </CardHeader>
                <CardContent className="p-0">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead>
                                <tr className="border-b bg-slate-50/50 dark:bg-slate-900/50">
                                    <th className="p-4 text-xs font-semibold uppercase text-muted-foreground">Agent Profile</th>
                                    <th className="p-4 text-xs font-semibold uppercase text-muted-foreground">Domain</th>
                                    <th className="p-4 text-xs font-semibold uppercase text-muted-foreground">Deployment</th>
                                    <th className="p-4 text-xs font-semibold uppercase text-muted-foreground">Load</th>
                                    <th className="p-4 text-xs font-semibold uppercase text-muted-foreground">Tasks</th>
                                    <th className="p-4 text-xs font-semibold uppercase text-muted-foreground text-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y">
                                {mockAgents.map((agent) => (
                                    <tr key={agent.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                                        <td className="p-4">
                                            <div className="flex items-center gap-3">
                                                <div className={`p-2 rounded-md bg-${agent.color}-100 dark:bg-${agent.color}-900/30 text-${agent.color}-600 dark:text-${agent.color}-400`}>
                                                    <Bot className="w-5 h-5" />
                                                </div>
                                                <div>
                                                    <p className="font-semibold">{agent.name}</p>
                                                    <p className="text-[10px] font-mono text-muted-foreground">{agent.id}</p>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="p-4">
                                            <Badge variant="outline">{agent.category}</Badge>
                                        </td>
                                        <td className="p-4">
                                            <div className="flex flex-col">
                                                <div className="flex items-center gap-2">
                                                    <div className={`w-1.5 h-1.5 rounded-full ${agent.status === 'Active' ? 'bg-emerald-500' : 'bg-slate-300'}`} />
                                                    <span className="text-sm">{agent.status}</span>
                                                </div>
                                                <span className="text-[10px] text-muted-foreground">Version {agent.version}</span>
                                            </div>
                                        </td>
                                        <td className="p-4 text-sm font-medium">{agent.load}</td>
                                        <td className="p-4 text-sm">{agent.tasks.toLocaleString()}</td>
                                        <td className="p-4">
                                            <div className="flex items-center justify-end gap-2">
                                                <Button size="icon" variant="ghost" className="h-8 w-8 text-blue-600">
                                                    <Eye className="h-4 w-4" />
                                                </Button>
                                                <Button size="icon" variant="ghost" className="h-8 w-8">
                                                    <Settings2 className="h-4 w-4" />
                                                </Button>
                                                <Button size="icon" variant="ghost" className={`h-8 w-8 ${agent.status === 'Active' ? 'text-red-500' : 'text-emerald-500'}`}>
                                                    <Power className="h-4 w-4" />
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

            <div className="flex items-center justify-center pt-4">
                <Button variant="outline" className="text-xs">
                    Show All 24 Agents
                    <ExternalLink className="w-3 h-3 ml-2" />
                </Button>
            </div>
        </div>
    );
}
