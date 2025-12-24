'use client';

import React, { useState, useEffect } from 'react';
import {
    Bot, Search, BarChart3, Users, Zap,
    MessageSquare, ShoppingCart, Settings,
    Play, CheckCircle2, AlertCircle, Clock,
    ChevronRight, Sparkles, Filter, MoreHorizontal,
    Target, Globe, Shield, Activity
} from 'lucide-react';
import { agentsApi, AgentConfig } from '../lib/api/agents';
import { useAuth } from './auth/AuthProvider';
import { AIAgentChat } from './AIAgentChat';

const AIAgentHub: React.FC = () => {
    const [agents, setAgents] = useState<AgentConfig[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedAgent, setSelectedAgent] = useState<AgentConfig | null>(null);
    const [activeTab, setActiveTab] = useState<'all' | 'marketing' | 'sales' | 'ops'>('all');

    const { user } = useAuth();

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
            case 'data-analyst': return <Activity className="w-6 h-6" />;
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
                        <Bot className="w-8 h-8 text-indigo-600" />
                        AI Agent Hub
                    </h1>
                    <p className="text-slate-500 mt-2 max-w-2xl">
                        Hire specialized AI agents to automate your business. These autonomous systems use our high-value connectors to deliver real-time insights and actions.
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
                        Marketing
                    </button>
                    <button
                        onClick={() => setActiveTab('sales')}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === 'sales' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                        Sales
                    </button>
                    <button
                        onClick={() => setActiveTab('ops')}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === 'ops' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                        Ops
                    </button>
                </div>
            </div>

            <div className="max-w-4xl mx-auto w-full">
                <AIAgentChat />
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
                            <div
                                className="absolute top-0 right-0 w-24 h-24 -mr-8 -mt-8 rounded-full opacity-5 group-hover:opacity-10 transition-opacity"
                                style={{ backgroundColor: agent.color }}
                            ></div>

                            <div className="flex items-start justify-between mb-4">
                                <div
                                    className="p-3 rounded-xl text-white shadow-lg"
                                    style={{ backgroundColor: agent.color }}
                                >
                                    {getAgentIcon(agent.id)}
                                </div>
                                <div className="flex flex-col items-end">
                                    <span className="text-[10px] uppercase tracking-wider font-bold text-slate-400">Status</span>
                                    <div className="flex items-center gap-1.5 text-emerald-500 font-medium text-xs">
                                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
                                        Available
                                    </div>
                                </div>
                            </div>

                            <h3 className="text-xl font-bold text-slate-900 group-hover:text-indigo-600 transition-colors">
                                {agent.name}
                            </h3>
                            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mt-1">
                                {agent.role}
                            </p>

                            <p className="text-slate-600 text-sm mt-4 line-clamp-2">
                                {agent.description}
                            </p>

                            <div className="mt-6 flex flex-wrap gap-2">
                                {agent.capabilities.slice(0, 3).map((cap, i) => (
                                    <span key={i} className="px-2.5 py-1 bg-slate-50 text-slate-600 rounded-lg text-[10px] font-bold border border-slate-100 uppercase">
                                        {cap}
                                    </span>
                                ))}
                                {agent.capabilities.length > 3 && (
                                    <span className="px-2.5 py-1 bg-slate-50 text-slate-400 rounded-lg text-[10px] font-bold border border-slate-100">
                                        +{agent.capabilities.length - 3} MORE
                                    </span>
                                )}
                            </div>

                            <div className="mt-8 pt-6 border-t border-slate-50 flex items-center justify-between">
                                <div className="flex -space-x-2">
                                    {agent.tools.slice(0, 4).map((tool, i) => (
                                        <div
                                            key={i}
                                            className="w-8 h-8 rounded-full bg-white border-2 border-slate-100 flex items-center justify-center text-[10px] font-bold text-slate-500 shadow-sm overflow-hidden"
                                            title={tool}
                                        >
                                            {tool.charAt(0).toUpperCase()}
                                        </div>
                                    ))}
                                </div>

                                <button
                                    className="flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-slate-900 text-white rounded-xl text-sm font-bold shadow-md shadow-indigo-100 transition-all active:scale-95 group/btn"
                                >
                                    <Play className="w-4 h-4 fill-current group-hover/btn:scale-110 transition-transform" />
                                    Hire Agent
                                </button>
                            </div>
                        </div>
                    ))}

                    {/* Premium Workflow Teaser */}
                    <div className="bg-gradient-to-br from-slate-900 to-indigo-900 rounded-2xl p-6 text-white flex flex-col justify-between shadow-2xl relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-4">
                            <Sparkles className="w-8 h-8 text-indigo-300 opacity-20 group-hover:opacity-100 transition-opacity" />
                        </div>

                        <div>
                            <div className="bg-indigo-500/30 w-fit p-3 rounded-xl mb-6">
                                <Zap className="w-6 h-6 text-indigo-300" />
                            </div>
                            <h3 className="text-2xl font-bold mb-2">Autonomous Workflows</h3>
                            <p className="text-indigo-100/70 text-sm leading-relaxed">
                                Unlock multi-agent "Crews" for complex tasks like complete Digital Audits, Competitor Analysis, and Multi-Channel Campaign Launches.
                            </p>
                        </div>

                        <button className="mt-8 w-full py-4 bg-white text-indigo-900 rounded-xl font-bold text-sm tracking-wide hover:bg-indigo-50 transition-colors flex items-center justify-center gap-2">
                            Upgrade to Agency-Level
                            <Zap className="w-4 h-4 flex-shrink-0" />
                        </button>
                    </div>
                </div>
            )}

            {/* Recommended Actions */}
            <div className="bg-indigo-50/50 rounded-3xl p-8 border border-indigo-100 relative overflow-hidden">
                <div className="absolute right-0 top-0 -mr-16 -mt-16 w-64 h-64 bg-indigo-200/20 rounded-full blur-3xl"></div>
                <div className="relative flex flex-col lg:flex-row items-center justify-between gap-8">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-900">Recommended Next Step</h2>
                        <p className="text-slate-600 mt-2">Our AI suggests starting with a Digital Registry Audit to verify your presence across 30+ US platforms.</p>
                    </div>
                    <button className="px-8 py-4 bg-slate-900 text-white rounded-2xl font-bold text-base shadow-lg shadow-slate-200 flex items-center gap-3 hover:scale-105 transition-all active:scale-95">
                        <Globe className="w-5 h-5 text-indigo-400" />
                        Launch Audit System
                    </button>
                </div>
            </div>
        </div>
    );
};

export default AIAgentHub;
