'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Sparkles, Loader2, Trash2, RefreshCw } from 'lucide-react';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
    agent_used?: string;
    data?: any;
    suggestions?: string[];
}

interface AIChatProps {
    activeTab?: string;
}

export const AIChat: React.FC<AIChatProps> = ({ activeTab }) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [conversationId, setConversationId] = useState<string | null>(null);
    const [selectedAgent, setSelectedAgent] = useState('general');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        // Load chat history when component mounts
        loadChatHistory();
    }, []);

    const loadChatHistory = async () => {
        try {
            const response = await fetch('/api/brain/ai/chat');
            if (response.ok) {
                const data = await response.json();
                if (data.messages && data.messages.length > 0) {
                    setMessages(data.messages);
                    setConversationId(data.conversation_id);
                }
            }
        } catch (error) {
            console.error('Failed to load chat history:', error);
        }
    };

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch('/api/brain/ai/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: input,
                    conversation_id: conversationId,
                    agent_type: selectedAgent,
                    context: {
                        current_tab: activeTab
                    }
                })
            });

            if (response.ok) {
                const data = await response.json();

                const assistantMessage: Message = {
                    id: (Date.now() + 1).toString(),
                    role: 'assistant',
                    content: data.response,
                    timestamp: new Date().toISOString(),
                    agent_used: data.agent_used,
                    data: data.data,
                    suggestions: data.suggestions
                };

                setMessages(prev => [...prev, assistantMessage]);
                setConversationId(data.conversation_id);
            } else {
                const errorMessage: Message = {
                    id: (Date.now() + 1).toString(),
                    role: 'assistant',
                    content: 'Sorry, I encountered an error. Please try again.',
                    timestamp: new Date().toISOString()
                };
                setMessages(prev => [...prev, errorMessage]);
            }
        } catch (error) {
            console.error('Chat error:', error);
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please try again.',
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleClearChat = async () => {
        if (!conversationId) {
            setMessages([]);
            return;
        }

        try {
            await fetch(`/api/brain/ai/chat?conversation_id=${conversationId}`, {
                method: 'DELETE'
            });
            setMessages([]);
            setConversationId(null);
        } catch (error) {
            console.error('Failed to clear chat:', error);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const handleSuggestionClick = (suggestion: string) => {
        setInput(suggestion);
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800">
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                        <Sparkles className="w-5 h-5 text-white" />
                    </div>
                    <div>
                        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">AI Assistant</h2>
                        <p className="text-xs text-gray-500 dark:text-gray-400">Powered by 93+ AI Agents</p>
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    <button
                        onClick={loadChatHistory}
                        className="p-2 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
                        title="Refresh"
                    >
                        <RefreshCw className="w-4 h-4" />
                    </button>
                    <button
                        onClick={handleClearChat}
                        className="p-2 text-gray-500 hover:text-red-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
                        title="Clear chat"
                    >
                        <Trash2 className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {/* Agent Selector */}
            <div className="p-3 border-b border-gray-200 dark:border-gray-800">
                <select
                    value={selectedAgent}
                    onChange={(e) => setSelectedAgent(e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                >
                    <option value="general">General Assistant</option>
                    <option value="crm">CRM Specialist</option>
                    <option value="ecommerce">E-commerce Expert</option>
                    <option value="analytics">Data Analyst</option>
                    <option value="content">Content Creator</option>
                    <option value="automation">Automation Expert</option>
                </select>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full text-center">
                        <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900/30 dark:to-purple-900/30 rounded-full flex items-center justify-center mb-4">
                            <Bot className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                            How can I help you today?
                        </h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400 max-w-md mb-6">
                            I can help you analyze data, automate tasks, generate content, and much more using 93+ specialized AI agents.
                        </p>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 w-full max-w-2xl">
                            {[
                                'Show me top 10 leads from last month',
                                'Analyze my sales performance',
                                'Create a marketing email template',
                                'What are my best-selling products?'
                            ].map((suggestion, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => handleSuggestionClick(suggestion)}
                                    className="p-3 text-left text-sm border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                                >
                                    {suggestion}
                                </button>
                            ))}
                        </div>
                    </div>
                ) : (
                    <>
                        {messages.map((message) => (
                            <div
                                key={message.id}
                                className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                {message.role === 'assistant' && (
                                    <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                                        <Bot className="w-4 h-4 text-white" />
                                    </div>
                                )}
                                <div
                                    className={`max-w-[70%] rounded-lg p-3 ${message.role === 'user'
                                            ? 'bg-blue-600 text-white'
                                            : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white'
                                        }`}
                                >
                                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                                    {message.agent_used && (
                                        <p className="text-xs mt-2 opacity-70">
                                            Agent: {message.agent_used}
                                        </p>
                                    )}
                                    {message.suggestions && message.suggestions.length > 0 && (
                                        <div className="mt-3 space-y-1">
                                            <p className="text-xs font-medium opacity-70">Suggestions:</p>
                                            {message.suggestions.map((suggestion, idx) => (
                                                <button
                                                    key={idx}
                                                    onClick={() => handleSuggestionClick(suggestion)}
                                                    className="block w-full text-left text-xs p-2 rounded bg-white/10 hover:bg-white/20 transition-colors"
                                                >
                                                    {suggestion}
                                                </button>
                                            ))}
                                        </div>
                                    )}
                                </div>
                                {message.role === 'user' && (
                                    <div className="w-8 h-8 bg-gray-300 dark:bg-gray-700 rounded-full flex items-center justify-center flex-shrink-0">
                                        <User className="w-4 h-4 text-gray-600 dark:text-gray-300" />
                                    </div>
                                )}
                            </div>
                        ))}
                        {isLoading && (
                            <div className="flex gap-3">
                                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                                    <Bot className="w-4 h-4 text-white" />
                                </div>
                                <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-3">
                                    <Loader2 className="w-4 h-4 animate-spin text-gray-600 dark:text-gray-400" />
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </>
                )}
            </div>

            {/* Input */}
            <div className="p-4 border-t border-gray-200 dark:border-gray-800">
                <div className="flex gap-2">
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Ask me anything..."
                        rows={1}
                        className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                        style={{ minHeight: '44px', maxHeight: '120px' }}
                    />
                    <button
                        onClick={handleSend}
                        disabled={!input.trim() || isLoading}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                    >
                        {isLoading ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                            <Send className="w-4 h-4" />
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};
