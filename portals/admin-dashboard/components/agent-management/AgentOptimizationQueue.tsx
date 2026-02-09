'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
    Sparkles,
    CheckCircle,
    XCircle,
    ArrowRight,
    Zap,
    Shield,
    DollarSign,
    AlertTriangle,
    Clock
} from 'lucide-react';
import { toast } from 'sonner';

interface OptimizationSuggestion {
    id: string;
    type: 'performance' | 'security' | 'cost' | 'reliability';
    title: string;
    description: string;
    impact: string;
    confidence: number;
    metrics: { label: string; before: string; after: string }[];
    status: 'pending' | 'approved' | 'rejected';
    timestamp: string;
}

const MOCK_SUGGESTIONS: OptimizationSuggestion[] = [
    {
        id: 'opt-1',
        type: 'performance',
        title: 'Increase Context Window',
        description: 'Analysis shows 15% of requests are truncated. Increasing context window to 8k tokens will improve coherence.',
        impact: 'High',
        confidence: 92,
        metrics: [
            { label: 'Avg coherence', before: '85%', after: '94%' },
            { label: 'Truncation rate', before: '15%', after: '0%' }
        ],
        status: 'pending',
        timestamp: '2h ago'
    },
    {
        id: 'opt-2',
        type: 'cost',
        title: 'Enable Response Caching',
        description: '30% of queries are repetitive. Enabling caching with 5m TTL will reduce API costs.',
        impact: 'Medium',
        confidence: 88,
        metrics: [
            { label: 'API Cost/Day', before: '$12.50', after: '$8.75' },
            { label: 'Avg Latency', before: '450ms', after: '120ms' }
        ],
        status: 'pending',
        timestamp: '5h ago'
    },
    {
        id: 'opt-3',
        type: 'security',
        title: 'Tighten IP Whitelist',
        description: 'Anomaly detection flagged requests from non-standard regions. Recommend restricting IP range.',
        impact: 'Critical',
        confidence: 99,
        metrics: [
            { label: 'Attack Surface', before: 'Global', after: 'Region-Locked' }
        ],
        status: 'pending',
        timestamp: '1d ago'
    }
];

export function AgentOptimizationQueue({ agentId }: { agentId: string }) {
    const [suggestions, setSuggestions] = useState<OptimizationSuggestion[]>(MOCK_SUGGESTIONS);

    const handleAction = (id: string, action: 'approved' | 'rejected') => {
        setSuggestions(suggestions.map(s =>
            s.id === id ? { ...s, status: action } : s
        ));
        toast.success(`Optimization ${action} successfully`);
    };

    const pendingCount = suggestions.filter(s => s.status === 'pending').length;

    const getTypeIcon = (type: string) => {
        switch (type) {
            case 'performance': return <Zap className="w-4 h-4 text-blue-500" />;
            case 'security': return <Shield className="w-4 h-4 text-red-500" />;
            case 'cost': return <DollarSign className="w-4 h-4 text-green-500" />;
            default: return <Sparkles className="w-4 h-4 text-purple-500" />;
        }
    };

    const getTypeColor = (type: string) => {
        switch (type) {
            case 'performance': return 'bg-blue-50 text-blue-700 border-blue-200';
            case 'security': return 'bg-red-50 text-red-700 border-red-200';
            case 'cost': return 'bg-green-50 text-green-700 border-green-200';
            default: return 'bg-purple-50 text-purple-700 border-purple-200';
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-lg font-medium">Pending Optimizations</h3>
                    <p className="text-sm text-gray-500">AI-suggested improvements awaiting approval</p>
                </div>
                <Badge variant="secondary" className="px-3 py-1">
                    {pendingCount} Pending
                </Badge>
            </div>

            {suggestions.length === 0 ? (
                <div className="text-center py-12 border rounded-lg bg-gray-50 border-dashed">
                    <CheckCircle className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                    <p className="text-gray-500 dark:text-gray-400">All optimizations handled!</p>
                </div>
            ) : (
                <div className="space-y-4">
                    {suggestions.filter(s => s.status === 'pending').map((suggestion) => (
                        <Card key={suggestion.id} className="overflow-hidden border-l-4 border-l-blue-500">
                            <CardHeader className="pb-3 bg-gray-50/50">
                                <div className="flex items-start justify-between">
                                    <div className="flex items-start gap-4">
                                        <div className={`p-2 rounded-lg bg-white border shadow-sm`}>
                                            {getTypeIcon(suggestion.type)}
                                        </div>
                                        <div>
                                            <div className="flex items-center gap-2">
                                                <CardTitle className="text-base">{suggestion.title}</CardTitle>
                                                <Badge variant="outline" className={getTypeColor(suggestion.type)}>
                                                    {suggestion.type.toUpperCase()}
                                                </Badge>
                                                <Badge variant="outline" className="text-gray-500 bg-gray-100">
                                                    {suggestion.confidence}% Confidence
                                                </Badge>
                                            </div>
                                            <CardDescription className="mt-1">
                                                {suggestion.description}
                                            </CardDescription>
                                        </div>
                                    </div>
                                    <div className="text-xs text-gray-400 flex items-center">
                                        <Clock className="w-3 h-3 mr-1" />
                                        {suggestion.timestamp}
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent className="pt-4">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div className="space-y-3">
                                        <h4 className="text-sm font-medium text-gray-500">Predicted Metrics</h4>
                                        <div className="space-y-2">
                                            {suggestion.metrics.map((metric, idx) => (
                                                <div key={idx} className="flex items-center justify-between text-sm p-2 bg-gray-50 rounded">
                                                    <span className="text-gray-600">{metric.label}</span>
                                                    <div className="flex items-center gap-2">
                                                        <span className="text-gray-400 line-through">{metric.before}</span>
                                                        <ArrowRight className="w-3 h-3 text-gray-400" />
                                                        <span className="font-semibold text-gray-900">{metric.after}</span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                    <div className="flex flex-col justify-end items-end space-y-3">
                                        <div className="flex items-center gap-3 w-full justify-end">
                                            <Button
                                                variant="outline"
                                                className="border-red-200 text-red-600 hover:bg-red-50 hover:text-red-700"
                                                onClick={() => handleAction(suggestion.id, 'rejected')}
                                            >
                                                <XCircle className="w-4 h-4 mr-2" />
                                                Reject
                                            </Button>
                                            <Button
                                                className="bg-blue-600 hover:bg-blue-700"
                                                onClick={() => handleAction(suggestion.id, 'approved')}
                                            >
                                                <CheckCircle className="w-4 h-4 mr-2" />
                                                Approve Optimization
                                            </Button>
                                        </div>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                    {pendingCount === 0 && (
                        <div className="text-center py-8 text-gray-500">
                            No pending optimizations.
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
