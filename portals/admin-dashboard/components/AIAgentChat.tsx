"use client";

import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Loader2, Sparkles, ChevronRight, MessageSquare } from 'lucide-react';

interface Message {
    id: string;
    role: 'user' | 'agent';
    content: string;
    agentName?: string;
    timestamp: Date;
    suggestions?: string[];
}

export const AIAgentChat: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: '1',
            role: 'agent',
            content: "Hello Admin! I'm the BizOSaas Platform Assistant. I can help you manage agents, monitor system health, or orchestrate administrative tasks. How can I assist you today?",
            agentName: 'Platform Assistant',
            timestamp: new Date(),
            suggestions: ['Check System Health', 'List Active Agents', 'View Recent Logs']
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSend = async (text: string = input) => {
        if (!text.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: text,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            // Lazy load the API to avoid server-side issues
            const { brainApi } = await import('@/lib/brain-api');

            const apiRes = await brainApi.agents.chat('personal_assistant', text);

            const agentMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'agent',
                content: apiRes.message || "I've processed your administrative request.",
                agentName: 'Assistant',
                timestamp: new Date(),
                suggestions: apiRes.suggestions
            };

            setMessages(prev => [...prev, agentMessage]);
        } catch (error) {
            console.error('Chat error:', error);
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'agent',
                content: "I'm having trouble connecting to the Brain Gateway. Please ensure the service is running and properly configured.",
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full w-full bg-slate-900/50 backdrop-blur-xl border border-slate-800/50 shadow-2xl">
            {/* Header */}
            <div className="px-6 py-4 border-b border-slate-800 bg-slate-900/80 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center border border-indigo-500/50 shadow-[0_0_15px_rgba(99,102,241,0.3)]">
                        <Bot className="w-6 h-6 text-indigo-400" />
                    </div>
                    <div>
                        <h3 className="font-semibold text-white flex items-center gap-2">
                            Platform AI Assistant
                            <span className="flex h-2 w-2 rounded-full bg-emerald-500"></span>
                        </h3>
                        <p className="text-xs text-slate-400">System orchestration & admin support</p>
                    </div>
                </div>
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800/50 border border-slate-700">
                    <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                    <span className="text-[10px] font-medium text-amber-400 uppercase tracking-wider">Super Admin</span>
                </div>
            </div>

            {/* Messages */}
            <div
                ref={scrollRef}
                className="flex-1 overflow-y-auto p-6 space-y-6 scroll-smooth custom-scrollbar"
            >
                {messages.map((msg) => (
                    <div
                        key={msg.id}
                        className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div className={`flex gap-3 max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 border ${msg.role === 'user'
                                ? 'bg-slate-700 border-slate-600'
                                : 'bg-indigo-500/10 border-indigo-500/30'
                                }`}>
                                {msg.role === 'user' ? <User className="w-4 h-4 text-slate-300" /> : <Bot className="w-4 h-4 text-indigo-400" />}
                            </div>
                            <div className="space-y-2">
                                <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${msg.role === 'user'
                                    ? 'bg-indigo-600 text-white rounded-tr-none'
                                    : 'bg-slate-800 text-slate-200 border border-slate-700 rounded-tl-none'
                                    }`}>
                                    {msg.content}
                                </div>
                                {msg.suggestions && msg.suggestions.length > 0 && (
                                    <div className="flex flex-wrap gap-2 pt-1">
                                        {msg.suggestions.map((suggestion, idx) => (
                                            <button
                                                key={idx}
                                                onClick={() => handleSend(suggestion)}
                                                className="text-xs px-3 py-1.5 rounded-full bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 transition-all hover:scale-105 active:scale-95 flex items-center gap-1.5"
                                            >
                                                <ChevronRight className="w-3 h-3 text-indigo-400" />
                                                {suggestion}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="flex gap-3 items-center text-slate-400">
                            <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center">
                                <Loader2 className="w-4 h-4 animate-spin text-indigo-400" />
                            </div>
                            <span className="text-xs italic">Coordinating with Brain Gateway...</span>
                        </div>
                    </div>
                )}
            </div>

            {/* Input */}
            <div className="p-4 border-t border-slate-800 bg-slate-900/50 pb-0 lg:pb-4">
                <form
                    onSubmit={(e) => { e.preventDefault(); handleSend(); }}
                    className="relative"
                >
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type an administrative command or question..."
                        className="w-full bg-slate-800/80 border border-slate-700 rounded-xl px-4 py-3.5 pr-12 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 placeholder:text-slate-500 transition-all"
                    />
                    <button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className="absolute right-2 top-1.5 p-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-700 disabled:opacity-50 transition-all text-white shadow-lg"
                    >
                        <Send className="w-4 h-4" />
                    </button>
                </form>
                <p className="text-[10px] text-center text-slate-500 mt-3 flex items-center justify-center gap-1.5">
                    <MessageSquare className="w-3 h-3" />
                    Administrative actions are logged and audited.
                </p>
            </div>
        </div>
    );
};
