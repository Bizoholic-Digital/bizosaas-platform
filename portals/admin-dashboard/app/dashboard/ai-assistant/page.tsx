'use client';

import React from 'react';
import { AIAgentChat } from '@/components/AIAgentChat';

import { useSetHeader } from '@/lib/contexts/HeaderContext';

export default function AdminAIAssistantPage() {
    useSetHeader("Admin AI Command Center", "Orchestrating platform-wide agents and systems");

    return (
        <div className="flex flex-col h-[calc(100vh-64px)] bg-slate-50 dark:bg-slate-950 animate-in fade-in duration-300">
            {/* Chat Area */}
            <div className="flex-1 overflow-hidden relative">
                <AIAgentChat />
            </div>
        </div>
    );
}
