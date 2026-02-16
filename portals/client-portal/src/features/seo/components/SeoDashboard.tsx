'use client';

import React, { useState, useEffect } from 'react';
import {
    Search,
    Globe,
    BarChart3,
    Link as LinkIcon,
    Plus,
    RefreshCw,
    FileText,
    Settings,
    ChevronRight,
    Loader2,
    ShieldCheck,
    AlertCircle,
    CheckCircle2
} from 'lucide-react';
import { brainGateway } from '@/lib/brain-gateway-client';

const SeoDashboard = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [auditUrl, setAuditUrl] = useState('');
    const [seedKeywords, setSeedKeywords] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [auditStatus, setAuditStatus] = useState<'idle' | 'running' | 'success' | 'error'>('idle');

    const handleRunAudit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!auditUrl) return;

        setIsSubmitting(true);
        setAuditStatus('running');
        try {
            await brainGateway.seo.triggerSiteAudit({ url: auditUrl });
            setAuditStatus('success');
            setAuditUrl('');
        } catch (error) {
            console.error('Audit failed:', error);
            setAuditStatus('error');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="p-8 max-w-7xl mx-auto min-h-screen bg-gray-50/50">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 tracking-tight">SEO Automation</h1>
                    <p className="text-gray-500 mt-1">Autonomous site audits, keyword research, and rank tracking.</p>
                </div>
                <div className="flex items-center gap-3">
                    <button className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-xl text-sm font-medium text-gray-600 hover:bg-gray-50 transition-all shadow-sm">
                        <RefreshCw className="w-4 h-4" />
                        Refresh Data
                    </button>
                    <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 rounded-xl text-sm font-medium text-white hover:bg-indigo-700 transition-all shadow-md shadow-indigo-100">
                        <Plus className="w-4 h-4" />
                        New Analysis
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column - Actions */}
                <div className="lg:col-span-2 space-y-8">
                    {/* Site Audit Card */}
                    <div className="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden">
                        <div className="p-6 border-b border-gray-50 flex items-center justify-between bg-gradient-to-r from-indigo-50/30 to-transparent">
                            <div className="flex items-center gap-3">
                                <div className="p-2.5 bg-indigo-100 rounded-2xl text-indigo-600">
                                    <Globe className="w-5 h-5" />
                                </div>
                                <h2 className="text-xl font-bold text-gray-900">Autonomous Site Audit</h2>
                            </div>
                        </div>
                        <div className="p-8">
                            <form onSubmit={handleRunAudit} className="space-y-4">
                                <div className="relative group">
                                    <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                        <Search className="h-5 w-5 text-gray-400 group-focus-within:text-indigo-500 transition-colors" />
                                    </div>
                                    <input
                                        type="url"
                                        placeholder="Enter website URL (e.g. https://example.com)"
                                        className="block w-full pl-11 pr-4 py-4 bg-gray-50 border-transparent rounded-2xl focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-gray-900"
                                        value={auditUrl}
                                        onChange={(e) => setAuditUrl(e.target.value)}
                                        required
                                    />
                                    <button
                                        type="submit"
                                        disabled={isSubmitting}
                                        className="absolute right-2 top-2 bottom-2 px-6 bg-indigo-600 text-white rounded-xl font-medium hover:bg-indigo-700 disabled:opacity-50 transition-all flex items-center gap-2 shadow-lg shadow-indigo-100"
                                    >
                                        {isSubmitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <ChevronRight className="w-5 h-5" />}
                                        Run Audit
                                    </button>
                                </div>
                                <div className="flex items-center gap-6 text-sm text-gray-500 px-2 mt-2">
                                    <div className="flex items-center gap-1.5 font-medium">
                                        <ShieldCheck className="w-4 h-4 text-emerald-500" />
                                        Core Web Vitals
                                    </div>
                                    <div className="flex items-center gap-1.5 font-medium">
                                        <ShieldCheck className="w-4 h-4 text-emerald-500" />
                                        On-Page Analysis
                                    </div>
                                    <div className="flex items-center gap-1.5 font-medium">
                                        <ShieldCheck className="w-4 h-4 text-emerald-500" />
                                        Link Verification
                                    </div>
                                </div>
                            </form>

                            {auditStatus === 'success' && (
                                <div className="mt-6 p-4 bg-emerald-50 rounded-2xl border border-emerald-100 flex items-center gap-3 text-emerald-700">
                                    <CheckCircle2 className="w-5 h-5" />
                                    Audit triggered! You'll be notified when the report is ready.
                                </div>
                            )}
                            {auditStatus === 'error' && (
                                <div className="mt-6 p-4 bg-rose-50 rounded-2xl border border-rose-100 flex items-center gap-3 text-rose-700">
                                    <AlertCircle className="w-5 h-5" />
                                    Something went wrong. Please check the URL and try again.
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Secondary Actions Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {/* Keyword Research */}
                        <div className="bg-white rounded-3xl border border-gray-100 shadow-sm p-6 flex flex-col hover:shadow-md transition-all group">
                            <div className="p-3 bg-amber-100 rounded-2xl text-amber-600 w-fit mb-4 group-hover:bg-amber-600 group-hover:text-white transition-colors">
                                <BarChart3 className="w-6 h-6" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-2">Keyword Intelligence</h3>
                            <p className="text-gray-500 text-sm mb-6 flex-grow">Autonomous keyword discovery, volume tracking, and clustering via AI.</p>
                            <button className="w-full py-3 bg-gray-50 text-gray-700 rounded-xl font-bold hover:bg-amber-600 hover:text-white transition-all flex items-center justify-center gap-2">
                                <Search className="w-4 h-4" />
                                Research Keywords
                            </button>
                        </div>

                        {/* Rank Tracker */}
                        <div className="bg-white rounded-3xl border border-gray-100 shadow-sm p-6 flex flex-col hover:shadow-md transition-all group">
                            <div className="p-3 bg-blue-100 rounded-2xl text-blue-600 w-fit mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                                <LinkIcon className="w-6 h-6" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-2">Rank Tracking</h3>
                            <p className="text-gray-500 text-sm mb-6 flex-grow">Monitor your search engine positions across target domains and regions.</p>
                            <button className="w-full py-3 bg-gray-50 text-gray-700 rounded-xl font-bold hover:bg-blue-600 hover:text-white transition-all flex items-center justify-center gap-2">
                                <RefreshCw className="w-4 h-4" />
                                Setup Tracking
                            </button>
                        </div>
                    </div>
                </div>

                {/* Right Column - Status & History */}
                <div className="space-y-8">
                    {/* Recent Audits */}
                    <div className="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden">
                        <div className="p-6 border-b border-gray-50">
                            <h3 className="font-bold text-gray-900 text-lg flex items-center gap-2">
                                <FileText className="w-5 h-5 text-gray-400" />
                                Audit History
                            </h3>
                        </div>
                        <div className="divide-y divide-gray-50">
                            <div className="p-4 hover:bg-gray-50 transition-colors cursor-pointer group">
                                <div className="flex justify-between items-center mb-1">
                                    <span className="font-bold text-gray-900 text-sm truncate">bizosaas.com</span>
                                    <span className="text-[10px] font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full uppercase">Report Ready</span>
                                </div>
                                <p className="text-xs text-gray-500">Completed 2 hours ago • 84 Pages</p>
                            </div>
                            <div className="p-4 hover:bg-gray-50 transition-colors cursor-pointer group">
                                <div className="flex justify-between items-center mb-1">
                                    <span className="font-bold text-gray-900 text-sm truncate">thrillring.com</span>
                                    <span className="text-[10px] font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full uppercase">Report Ready</span>
                                </div>
                                <p className="text-xs text-gray-500">Completed yesterday • 152 Pages</p>
                            </div>
                            <div className="p-6 text-center">
                                <button className="text-indigo-600 hover:text-indigo-700 text-sm font-bold flex items-center gap-1 mx-auto hover:gap-1.5 transition-all">
                                    View All Reports
                                    <ChevronRight className="w-4 h-4" />
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* Quick Config */}
                    <div className="bg-indigo-900 rounded-3xl p-8 text-white shadow-xl shadow-indigo-100 overflow-hidden relative group">
                        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:scale-110 transition-transform">
                            <Settings className="w-24 h-24" />
                        </div>
                        <h3 className="text-xl font-bold mb-3 relative z-10">Advanced Config</h3>
                        <p className="text-indigo-200 text-sm mb-6 relative z-10">Integrate Google Search Console & GA4 to unlock deep insights.</p>
                        <button className="w-full py-3 bg-white/10 hover:bg-white/20 text-white rounded-xl font-bold text-sm transition-all border border-white/10 relative z-10">
                            Connect Accounts
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SeoDashboard;
