'use client';

import React from 'react';
import { AIAgentChat } from '@/components/AIAgentChat';

export default function PersonalAIAssistantPage() {
    // Full screen height minus header (approx 64px) and padding
    // We remove the default padding to allow the chat to be immersive
    return (
        <div className="flex flex-col h-[calc(100vh-64px)] bg-slate-50 dark:bg-slate-950 animate-in fade-in duration-300">
            {/* Header Section - Minimal */}
            <div className="shrink-0 px-6 py-3 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex items-center justify-between">
                <div>
                    <h1 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
                        AI Command Center
                    </h1>
                    <p className="text-xs text-slate-500 dark:text-slate-400">Orchestrating 93+ BizOSaaS Agents</p>
                </div>
            </div>

            {/* Chat Area - Flex Grow to fill space */}
            <div className="flex-1 overflow-hidden relative">
                <AIAgentChat />
            </div>
        </div>
    );
}
