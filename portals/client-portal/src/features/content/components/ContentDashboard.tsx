'use client';

import React, { useState, useEffect } from 'react';
import {
    FileText,
    Plus,
    Search,
    Filter,
    CheckCircle2,
    Clock,
    AlertCircle,
    ChevronRight,
    RefreshCw,
    MoreVertical,
    ArrowUpRight,
    Eye,
    Check,
    X,
    MessageSquare,
    UserCircle
} from 'lucide-react';
import Link from 'next/link';
import { contentClient } from '@/lib/brain-gateway-client/clients/content';
import { cn } from '@/lib/utils';

// Types for local dashboard state
interface ContentWorkflow {
    id: string;
    topic: string;
    phase: string;
    status: string;
    updatedAt: string;
}

export function ContentDashboard() {
    const [activeWorkflows, setActiveWorkflows] = useState<ContentWorkflow[]>([]);
    const [contentItems, setContentItems] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isCreating, setIsCreating] = useState(false);
    const [newTopic, setNewTopic] = useState('');

    // Fetch initial data
    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        setIsLoading(true);
        try {
            // In a real app, we'd fetch actual workflows. For now, we'll mock some data
            // mixed with real API calls where possible.
            const listRes = await contentClient.list({ limit: 5 });
            setContentItems(listRes.items);

            // Mock active workflows for demonstration
            setActiveWorkflows([
                {
                    id: 'content-tenant-20240212001',
                    topic: 'The Future of AI in SaaS',
                    phase: 'outline_review',
                    status: 'running',
                    updatedAt: new Date().toISOString()
                },
                {
                    id: 'content-tenant-20240212002',
                    topic: 'SEO Strategies for 2025',
                    phase: 'writing',
                    status: 'running',
                    updatedAt: new Date().toISOString()
                }
            ]);
        } catch (error) {
            console.error('Failed to fetch content data:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleStartWorkflow = async () => {
        if (!newTopic) return;
        setIsCreating(true);
        try {
            const res = await contentClient.createAutonomous({
                topic: newTopic,
                require_approval: true
            });
            // Add to local state (optimistic or refresh)
            setActiveWorkflows(prev => [
                {
                    id: res.workflow_id,
                    topic: newTopic,
                    phase: 'research',
                    status: 'running',
                    updatedAt: new Date().toISOString()
                },
                ...prev
            ]);
            setNewTopic('');
        } catch (error) {
            console.error('Failed to start workflow:', error);
        } finally {
            setIsCreating(false);
        }
    };

    const handleApprove = async (workflowId: string, phase: string) => {
        try {
            await contentClient.approvePhase({
                workflow_id: workflowId,
                phase: phase,
                notes: 'Approved via Dashboard'
            });
            // Refresh status after signal
            fetchDashboardData();
        } catch (error) {
            console.error('Approval failed:', error);
        }
    };

    const handleReject = async (workflowId: string, phase: string) => {
        try {
            await contentClient.rejectPhase({
                workflow_id: workflowId,
                phase: phase,
                notes: 'Needs more detail'
            });
            fetchDashboardData();
        } catch (error) {
            console.error('Rejection failed:', error);
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            {/* Header Section */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Content Intelligence</h1>
                    <p className="text-gray-500 mt-1">Autonomous AI pipeline for brand-aligned content creation.</p>
                </div>

                <div className="flex items-center gap-3">
                    <div className="relative group">
                        <input
                            type="text"
                            placeholder="Topic for new content..."
                            className="pl-4 pr-10 py-2.5 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none w-64 transition-all shadow-sm"
                            value={newTopic}
                            onChange={(e) => setNewTopic(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleStartWorkflow()}
                        />
                        <button
                            onClick={handleStartWorkflow}
                            disabled={isCreating || !newTopic}
                            className="absolute right-2 top-2 p-1.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
                        >
                            {isCreating ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
                        </button>
                    </div>

                    <Link
                        href="/dashboard/content/persona"
                        className="flex items-center gap-2 px-4 py-2.5 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 transition-all shadow-sm text-sm font-medium text-gray-700 hover:text-indigo-600 hover:border-indigo-200"
                    >
                        <UserCircle className="w-5 h-5 text-indigo-500" />
                        Brand Persona
                    </Link>
                </div>
            </div>

            {/* Stats Section */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                    { label: 'Published Articles', value: contentItems.length, icon: FileText, color: 'text-blue-600', bg: 'bg-blue-50' },
                    { label: 'Active Automations', value: activeWorkflows.length, icon: Bot, color: 'text-indigo-600', bg: 'bg-indigo-50' },
                    { label: 'Pending Reviews', value: activeWorkflows.filter(w => w.phase.includes('review')).length, icon: AlertCircle, color: 'text-amber-600', bg: 'bg-amber-50' }
                ].map((stat, i) => (
                    <div key={i} className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between">
                            <div className={cn("p-3 rounded-xl", stat.bg)}>
                                <stat.icon className={cn("w-6 h-6", stat.color)} />
                            </div>
                            <span className="text-2xl font-bold text-gray-900">{stat.value}</span>
                        </div>
                        <p className="text-sm font-medium text-gray-500 mt-4">{stat.label}</p>
                    </div>
                ))}
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                {/* Active Workflows - Left/Main Column */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="flex items-center justify-between">
                        <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
                            <RefreshCw className="w-5 h-5 text-indigo-500" />
                            Active Pipelines
                        </h2>
                        <button
                            onClick={fetchDashboardData}
                            className="text-sm text-indigo-600 hover:text-indigo-700 font-medium flex items-center gap-1"
                        >
                            <RefreshCw className="w-3.5 h-3.5" />
                            Refresh
                        </button>
                    </div>

                    <div className="space-y-4">
                        {activeWorkflows.length === 0 ? (
                            <div className="bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 p-12 text-center">
                                <Bot className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                                <h3 className="text-lg font-medium text-gray-900">No active pipelines</h3>
                                <p className="text-gray-500 max-w-xs mx-auto mt-1">Start a new autonomous content workflow to see it here.</p>
                            </div>
                        ) : (
                            activeWorkflows.map((workflow) => (
                                <div key={workflow.id} className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden border-l-4 border-l-indigo-500 transition-all hover:translate-x-1">
                                    <div className="p-5">
                                        <div className="flex items-start justify-between">
                                            <div>
                                                <h3 className="font-bold text-gray-900 text-lg">{workflow.topic}</h3>
                                                <div className="flex items-center gap-3 mt-2">
                                                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 uppercase tracking-wider">
                                                        {workflow.phase.replace('_', ' ')}
                                                    </span>
                                                    <span className="text-xs text-gray-400 flex items-center gap-1">
                                                        <Clock className="w-3 h-3" />
                                                        Updated {new Date(workflow.updatedAt).toLocaleTimeString()}
                                                    </span>
                                                </div>
                                            </div>

                                            <div className="flex gap-2">
                                                {workflow.phase.includes('review') && (
                                                    <>
                                                        <button
                                                            onClick={() => handleApprove(workflow.id, workflow.phase)}
                                                            className="p-2 bg-green-50 text-green-600 rounded-xl hover:bg-green-100 transition-colors border border-green-200"
                                                            title="Approve Phase"
                                                        >
                                                            <Check className="w-5 h-5" />
                                                        </button>
                                                        <button
                                                            onClick={() => handleReject(workflow.id, workflow.phase)}
                                                            className="p-2 bg-red-50 text-red-600 rounded-xl hover:bg-red-100 transition-colors border border-red-200"
                                                            title="Request Revision"
                                                        >
                                                            <X className="w-5 h-5" />
                                                        </button>
                                                    </>
                                                )}
                                                <button className="p-2 text-gray-400 hover:text-gray-600">
                                                    <MoreVertical className="w-5 h-5" />
                                                </button>
                                            </div>
                                        </div>

                                        {/* Progress Bar / Indicator */}
                                        <div className="mt-6 flex items-center gap-4">
                                            <div className="flex-1 bg-gray-100 h-2 rounded-full overflow-hidden">
                                                <div
                                                    className="bg-indigo-500 h-full rounded-full transition-all duration-1000"
                                                    style={{ width: workflow.phase === 'research' ? '25%' : workflow.phase === 'outline_review' ? '50%' : workflow.phase === 'writing' ? '75%' : '90%' }}
                                                />
                                            </div>
                                            <span className="text-xs font-bold text-indigo-600 whitespace-nowrap uppercase tracking-tighter">
                                                In Progress
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>

                {/* Content Library - Right Column */}
                <div className="space-y-6">
                    <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
                        <FileText className="w-5 h-5 text-indigo-500" />
                        Recent Content
                    </h2>

                    <div className="space-y-4">
                        {contentItems.slice(0, 4).map((item) => (
                            <div key={item.id} className="group bg-white p-4 rounded-xl border border-gray-100 shadow-sm hover:border-indigo-200 transition-all cursor-pointer">
                                <div className="flex items-start justify-between">
                                    <div className="space-y-1">
                                        <h4 className="font-medium text-gray-900 line-clamp-1 group-hover:text-indigo-600 transition-colors">{item.title}</h4>
                                        <p className="text-xs text-gray-400">{new Date(item.created_at).toLocaleDateString()}</p>
                                    </div>
                                    <ArrowUpRight className="w-4 h-4 text-gray-300 group-hover:text-indigo-500 transition-all" />
                                </div>
                                <div className="flex items-center gap-2 mt-3">
                                    <span className={cn(
                                        "px-2 py-0.5 rounded text-[10px] font-bold uppercase",
                                        item.status === 'published' ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-600"
                                    )}>
                                        {item.status}
                                    </span>
                                    <span className="text-[10px] text-gray-400 uppercase font-bold">{item.content_type}</span>
                                </div>
                            </div>
                        ))}

                        <button className="w-full py-4 bg-gray-50 text-gray-500 rounded-xl border border-gray-100 hover:bg-white hover:border-indigo-200 hover:text-indigo-600 transition-all text-sm font-medium">
                            View All Content Library
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

// Minimal placeholder component for Bot icon if not exported from lucide
function Bot({ className }: { className?: string }) {
    return (
        <svg
            className={className}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <path d="M12 8V4H8" />
            <rect width="16" height="12" x="4" y="8" rx="2" />
            <path d="M2 14h2" />
            <path d="M20 14h2" />
            <path d="M15 13v2" />
            <path d="M9 13v2" />
        </svg>
    );
}
