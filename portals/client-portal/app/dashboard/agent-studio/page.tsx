'use client';

import React, { useState, useEffect } from 'react';
import {
    Bot, BarChart3, Users, Zap,
    MessageSquare, ShoppingCart, Settings,
    Play, AlertCircle, Sparkles, Filter, MoreHorizontal
} from 'lucide-react';
import { agentsApi, AgentConfig } from '@/lib/api/agents';

export default function AgentStudioPage() {
    const [agents, setAgents] = useState<AgentConfig[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState<'all' | 'marketing' | 'sales' | 'ops'>('all');

    useEffect(() => {
        fetchAgents();
    }, []);

    const fetchAgents = async () => {
        setLoading(true);
        const response = await agentsApi.getAgents();
        if (response.data) {
            setAgents(response.data);
        } else {
            setError(response.error || 'Failed to load agents');
        }
        setLoading(false);
    };

    const getAgentIcon = (id: string) => {
        switch (id) {
            case 'marketing-strategist': return <BarChart3 className="w-6 h-6" />;
            case 'content-creator': return <Sparkles className="w-6 h-6" />;
            case 'sales-assistant': return <Users className="w-6 h-6" />;
            case 'customer-support': return <MessageSquare className="w-6 h-6" />;
            case 'data-analyst': return <BarChart3 className="w-6 h-6" />;
            case 'ecommerce-optimizer': return <ShoppingCart className="w-6 h-6" />;
            case 'workflow-automator': return <Settings className="w-6 h-6" />;
            default: return <Bot className="w-6 h-6" />;
        }
    };

    const filteredAgents = agents.filter(agent => {
        if (activeTab === 'all') return true;
        if (activeTab === 'marketing') return ['marketing-strategist', 'content-creator'].includes(agent.id);
        if (activeTab === 'sales') return ['sales-assistant'].includes(agent.id);
        if (activeTab === 'ops') return ['customer-support', 'data-analyst', 'workflow-automator'].includes(agent.id);
        return true;
    });

    return (
        <div className="space-y-8 p-6 animate-in fade-in duration-500">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-3">
                        <Settings className="w-8 h-8 text-indigo-600" />
                        Agent Studio
                    </h1>
                    <p className="text-slate-500 mt-2 max-w-2xl">
                        Customize and configure your specialized AI agents. Adjust their prompts, tools, and permissions to align with your business goals.
                    </p>
                </div>

                <div className="flex items-center gap-2 bg-slate-100 p-1 rounded-xl">
                    <button
                        onClick={() => setActiveTab('all')}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === 'all' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                        All
                    </button>
                    <button
                        onClick={() => setActiveTab('marketing')}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === 'marketing' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                        Config
                    </button>
                    <button
                        onClick={() => setActiveTab('sales')}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === 'sales' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                        Tools
                    </button>
                    <button
                        onClick={() => setActiveTab('ops')}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === 'ops' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                        Audit
                    </button>
                </div>
            </div>

            {loading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[1, 2, 3, 4, 5, 6].map(i => (
                        <div key={i} className="bg-white rounded-2xl p-6 border border-slate-200 animate-pulse h-64"></div>
                    ))}
                </div>
            ) : error ? (
                <div className="bg-red-50 border border-red-200 rounded-2xl p-8 flex items-center justify-center text-red-600 gap-3">
                    <AlertCircle className="w-6 h-6" />
                    <p>{error}</p>
                    <button onClick={fetchAgents} className="ml-4 underline font-medium">Retry</button>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredAgents.map((agent) => (
                        <div
                            key={agent.id}
                            className="group bg-white rounded-2xl border border-slate-200 p-6 hover:shadow-xl hover:border-indigo-200 transition-all duration-300 relative overflow-hidden"
                        >
                            <div className="flex items-start justify-between mb-4">
                                <div
                                    className="p-3 rounded-xl text-white shadow-lg"
                                    style={{ backgroundColor: agent.color }}
                                >
                                    {getAgentIcon(agent.id)}
                                </div>
                                <button className="p-2 text-slate-400 hover:text-slate-900 transition-colors">
                                    <MoreHorizontal className="w-5 h-5" />
                                </button>
                            </div>

                            <h3 className="text-xl font-bold text-slate-900 transition-colors">
                                {agent.name}
                            </h3>
                            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mt-1">
                                {agent.role}
                            </p>

                            <div className="mt-8 space-y-4">
                                <div className="flex items-center justify-between text-sm">
                                    <span className="text-slate-500">Status</span>
                                    <span className="font-bold text-emerald-500">Healthy</span>
                                </div>
                                <div className="flex items-center justify-between text-sm">
                                    <span className="text-slate-500">Last Active</span>
                                    <span className="font-medium text-slate-700">2h ago</span>
                                </div>
                                <div className="flex items-center justify-between text-sm">
                                    <span className="text-slate-500">Memory usage</span>
                                    <span className="font-medium text-slate-700">650MB</span>
                                </div>
                            </div>

                            <div className="mt-8 pt-6 border-t border-slate-50 flex items-center gap-3">
                                <button
                                    className="flex-1 px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-900 rounded-xl text-sm font-bold transition-all active:scale-95"
                                >
                                    Configure
                                </button>
                                <button
                                    className="flex-1 px-4 py-2.5 bg-indigo-600 hover:bg-slate-900 text-white rounded-xl text-sm font-bold transition-all active:scale-95 shadow-md shadow-indigo-100"
                                >
                                    Logs
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
