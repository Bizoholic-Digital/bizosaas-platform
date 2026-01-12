'use client';

import React from 'react';
import { AIAgentChat } from '@/components/AIAgentChat';
import { useSetHeader } from '@/lib/contexts/HeaderContext';

export default function PersonalAIAssistantPage() {
    useSetHeader("AI Assistant", "Orchestrating 93+ Specialist Agents");

    // Full screen height minus header (approx 64px) and padding
    // We remove the default padding to allow the chat to be immersive
    return (
        <div className="flex flex-col h-[calc(100vh-64px)] bg-slate-50 dark:bg-slate-950 animate-in fade-in duration-300">
            {/* Chat Area - Flex Grow to fill space */}
            <div className="flex-1 overflow-hidden relative">
                <AIAgentChat />
            </div>
        </div>
    );
}
