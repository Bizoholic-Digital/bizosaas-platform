'use client';

import React from 'react';
import { AIAgentChat } from '@/components/AIAgentChat';
import { Bot, Sparkles, MessageCircle } from 'lucide-react';

export default function PersonalAIAssistantPage() {
    return (
        <div className="space-y-6 p-6 animate-in fade-in duration-500">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 pb-6">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-3">
                        <Bot className="w-8 h-8 text-indigo-600" />
                        Personal AI Assistant
                    </h1>
                    <p className="text-slate-500 mt-2 max-w-2xl">
                        Your intelligent business companion. I can help you manage campaigns, get insights, and automate tasks across your platform.
                    </p>
                </div>
            </div>

            <div className="max-w-4xl mx-auto w-full mt-8">
                <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-200">
                    <div className="bg-indigo-600 p-4 flex items-center gap-3 text-white">
                        <MessageCircle className="w-5 h-5" />
                        <span className="font-bold">BizOSaaS Intelligent Chat</span>
                        <div className="ml-auto flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                            <span className="text-xs font-medium opacity-90">Active & Learning</span>
                        </div>
                    </div>
                    <AIAgentChat />
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
                <div className="p-6 bg-slate-50 rounded-2xl border border-slate-200 hover:border-indigo-200 transition-all">
                    <Sparkles className="w-6 h-6 text-indigo-500 mb-4" />
                    <h3 className="font-bold text-slate-900">Campaign Insights</h3>
                    <p className="text-sm text-slate-600 mt-2">"Analyze my Google Ads performance and suggest optimizations."</p>
                </div>
                <div className="p-6 bg-slate-50 rounded-2xl border border-slate-200 hover:border-indigo-200 transition-all">
                    <Sparkles className="w-6 h-6 text-indigo-500 mb-4" />
                    <h3 className="font-bold text-slate-900">Content Generation</h3>
                    <p className="text-sm text-slate-600 mt-2">"Draft a high-conversion email for my New Year sale."</p>
                </div>
                <div className="p-6 bg-slate-50 rounded-2xl border border-slate-200 hover:border-indigo-200 transition-all">
                    <Sparkles className="w-6 h-6 text-indigo-500 mb-4" />
                    <h3 className="font-bold text-slate-900">Task Automation</h3>
                    <p className="text-sm text-slate-600 mt-2">"Sync my new leads from Facebook to the CRM."</p>
                </div>
            </div>
        </div>
    );
}
