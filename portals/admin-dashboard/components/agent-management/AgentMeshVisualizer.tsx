'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Network, Zap, Shield, Beaker, MessageSquare, ArrowRight, Activity, Bot, Target, RefreshCw } from 'lucide-react';
import { agentsApi } from '@/lib/api/agents';
import { toast } from 'sonner';

interface AgentNode {
    id: string;
    name: string;
    role: string;
    status: 'active' | 'idle' | 'error';
    type: 'supervisor' | 'specialist';
}

interface AgentEdge {
    from: string;
    to: string;
    action: string;
    status: 'active' | 'pending' | 'success';
}

export default function AgentMeshVisualizer() {
    const [nodes, setNodes] = useState<AgentNode[]>([
        { id: 'ceo', name: 'CEO Orchestrator', role: 'Global Strategy', status: 'active', type: 'supervisor' },
        { id: 'crm', name: 'CRM Supervisor', role: 'Sales & Leads', status: 'active', type: 'supervisor' },
        { id: 'lead-score', name: 'Lead Scoring', role: 'Qualification', status: 'active', type: 'specialist' },
        { id: 'lead-assign', name: 'Lead Assignment', role: 'Distribution', status: 'active', type: 'specialist' },
        { id: 'cms', name: 'CMS Supervisor', role: 'Content & SEO', status: 'active', type: 'supervisor' },
        { id: 'content', name: 'Content Creation', role: 'Generation', status: 'idle', type: 'specialist' },
    ]);

    const [edges, setEdges] = useState<AgentEdge[]>([
        { from: 'ceo', to: 'crm', action: 'Delegate Lead Qualification', status: 'success' },
        { from: 'crm', to: 'lead-score', action: 'Score Incoming Lead', status: 'active' },
        { from: 'lead-score', to: 'lead-assign', action: 'Route Qualified Lead', status: 'pending' },
        { from: 'ceo', to: 'cms', action: 'Initiate Content Strategy', status: 'success' },
        { from: 'cms', to: 'content', action: 'Generate Blog Post', status: 'pending' },
    ]);

    const [loading, setLoading] = useState(false);

    const loadMeshData = async () => {
        setLoading(true);
        try {
            const res = await agentsApi.getAgentMesh();
            if (res.data) {
                setNodes(res.data.nodes);
                setEdges(res.data.edges);
                toast.success("Agent Mesh synchronized with live environment");
            } else {
                console.warn("Failed to load mesh data", res.error);
                toast.error("Failed to load Agent Mesh data");
            }
        } catch (error) {
            console.warn("Real mesh data unavailable, using cached view.", error);
            toast.error("Agent Mesh synchronization failed");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadMeshData();
    }, []);

    const handleAgentClick = (agent: AgentNode) => {
        toast.info(`Inspecting agent: ${agent.name}`, {
            description: `Type: ${agent.type} | Status: ${agent.status}`,
            icon: <Bot className="w-4 h-4" />
        });
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-black text-slate-900 dark:text-white uppercase italic tracking-tighter">
                        Agent <span className="text-indigo-600">Mesh</span> Visualizer
                    </h2>
                    <p className="text-sm text-slate-500 font-medium">Real-time interaction matrix and specialist agent coordination</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={loadMeshData} disabled={loading}>
                        <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                        Refresh Mesh
                    </Button>
                    <Button size="sm" className="bg-indigo-600">
                        <Zap className="w-4 h-4 mr-2" />
                        Test Mesh
                    </Button>
                </div>
            </div>

            <Card className="border-none shadow-xl bg-slate-950 min-h-[600px] relative overflow-hidden flex items-center justify-center">
                {/* Background Grid */}
                <div className="absolute inset-0 opacity-10 pointer-events-none" style={{ backgroundImage: 'linear-gradient(to right, #4f46e5 1px, transparent 1px), linear-gradient(to bottom, #4f46e5 1px, transparent 1px)', backgroundSize: '40px 40px' }} />

                {/* Mesh Content */}
                <div className="relative z-10 w-full h-full p-8 flex flex-wrap justify-center gap-16">
                    {nodes.filter(n => n.type === 'supervisor').map(supervisor => (
                        <div key={supervisor.id} className="flex flex-col items-center gap-12">
                            {/* Supervisor Node */}
                            <div className="relative" onClick={() => handleAgentClick(supervisor)}>
                                <Card className={`w-64 border-2 cursor-pointer group hover:scale-105 transition-all ${supervisor.status === 'active' ? 'border-indigo-500 shadow-lg shadow-indigo-500/20' : 'border-slate-800'}`}>
                                    <div className="absolute -top-2 -right-2 w-4 h-4 bg-emerald-500 rounded-full border-2 border-slate-950 animate-pulse" />
                                    <CardContent className="p-4 flex items-center gap-4">
                                        <div className="p-2 bg-indigo-600 rounded-lg group-hover:rotate-12 transition-transform">
                                            <Target className="w-6 h-6 text-white" />
                                        </div>
                                        <div>
                                            <h4 className="font-bold text-slate-100">{supervisor.name}</h4>
                                            <p className="text-[10px] uppercase font-black text-indigo-400">{supervisor.role}</p>
                                        </div>
                                    </CardContent>
                                </Card>
                            </div>

                            {/* specialist agents grid */}
                            <div className="grid grid-cols-1 gap-6">
                                {nodes.filter(n => n.type === 'specialist' && edges.some(e => e.to === n.id && e.from === supervisor.id)).map(specialist => (
                                    <div key={specialist.id} className="relative" onClick={() => handleAgentClick(specialist)}>
                                        <Card className="w-56 border border-slate-800 bg-slate-900/50 hover:border-indigo-500 transition-all cursor-pointer hover:-translate-y-1">
                                            <CardContent className="p-3 flex items-center gap-3">
                                                <div className="p-1.5 bg-slate-800 rounded-md">
                                                    <Bot className="w-4 h-4 text-slate-400" />
                                                </div>
                                                <div>
                                                    <h5 className="font-bold text-xs text-slate-100">{specialist.name}</h5>
                                                    <Badge variant="outline" className="text-[8px] h-4 bg-slate-800 border-none text-slate-400">{specialist.role}</Badge>
                                                </div>
                                            </CardContent>
                                        </Card>
                                        {/* Animation line between supervisor and specialist */}
                                        <div className="absolute -top-6 left-1/2 -translate-x-1/2 w-0.5 h-6 bg-indigo-500/30" />
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pb-20">
                <Card className="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800">
                    <CardHeader>
                        <CardTitle className="text-sm font-black uppercase flex items-center">
                            <MessageSquare className="w-4 h-4 mr-2 text-indigo-600" />
                            Active Communications
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {edges.map((edge, i) => (
                            <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800">
                                <div className="flex items-center gap-3">
                                    <span className="text-[10px] font-black uppercase text-slate-400">{edge.from}</span>
                                    <ArrowRight className="w-3 h-3 text-slate-300" />
                                    <span className="text-[10px] font-black uppercase text-indigo-500">{edge.to}</span>
                                </div>
                                <span className="text-xs font-medium text-slate-600 dark:text-slate-300">{edge.action}</span>
                                <Badge className={edge.status === 'active' ? 'bg-indigo-500' : edge.status === 'success' ? 'bg-emerald-500' : 'bg-slate-500'}>
                                    {edge.status}
                                </Badge>
                            </div>
                        ))}
                    </CardContent>
                </Card>

                <Card className="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white">
                    <CardHeader>
                        <CardTitle className="text-sm font-black uppercase flex items-center">
                            <Shield className="w-4 h-4 mr-2 text-indigo-600" />
                            Mesh Health Analytics
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="flex justify-between items-end">
                            <div>
                                <p className="text-[10px] uppercase font-black text-slate-400">Communication Latency</p>
                                <p className="text-2xl font-black italic">42ms</p>
                            </div>
                            <div className="text-right">
                                <p className="text-[10px] uppercase font-black text-slate-400">Data Integrity</p>
                                <p className="text-2xl font-black italic">99.9%</p>
                            </div>
                        </div>
                        <div className="space-y-2">
                            <div className="flex justify-between text-[10px] font-black uppercase">
                                <span>Bandwidth Usage</span>
                                <span className="text-indigo-600">64%</span>
                            </div>
                            <div className="h-1.5 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                                <div className="h-full bg-indigo-600 w-[64%]" />
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
