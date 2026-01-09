'use client';

import React, { useEffect, useState } from 'react';
import { Zap, ExternalLink, RefreshCw, AlertTriangle, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { brainApi } from '@/lib/brain-api';
import { useAuth } from '@clerk/nextjs';
import { toast } from 'sonner';

interface Optimization {
    id: string;
    workflow_id?: string;
    workflow_name?: string;
    type: 'reliability' | 'performance' | 'general';
    severity: 'high' | 'medium' | 'low';
    message: string;
    action: string;
}

export function WorkflowOptimizationPanel() {
    const { getToken } = useAuth();
    const [suggestions, setSuggestions] = useState<Optimization[]>([]);
    const [loading, setLoading] = useState(true);

    const loadOptimizations = async () => {
        setLoading(true);
        try {
            const token = await getToken();
            const data = await brainApi.workflows.getOptimizations(token as string);
            setSuggestions(data);
        } catch (error) {
            console.error(error);
            toast.error("Failed to load optimizations");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadOptimizations();
    }, []);

    if (loading) {
        return (
            <div className="bg-purple-50 dark:bg-purple-900/10 border border-purple-100 dark:border-purple-800/20 rounded-2xl p-6 mt-8 animate-pulse">
                <div className="flex gap-4">
                    <div className="h-10 w-10 bg-purple-100 dark:bg-purple-900/40 rounded-full shrink-0" />
                    <div className="space-y-2 flex-1">
                        <div className="h-4 bg-purple-100 dark:bg-purple-900/40 rounded w-1/4" />
                        <div className="h-3 bg-purple-100 dark:bg-purple-900/40 rounded w-3/4" />
                    </div>
                </div>
            </div>
        );
    }

    if (suggestions.length === 0) return null;

    // Display the highest severity suggestion first
    const topSuggestion = suggestions.sort((a, b) => {
        const severityMap = { high: 3, medium: 2, low: 1 };
        return severityMap[b.severity] - severityMap[a.severity];
    })[0];

    return (
        <div className="bg-purple-50 dark:bg-purple-900/10 border border-purple-100 dark:border-purple-800/20 rounded-2xl p-6 mt-8">
            <div className="flex flex-col md:flex-row gap-4 items-start">
                <div className="h-10 w-10 bg-purple-100 dark:bg-purple-900/40 rounded-full flex items-center justify-center shrink-0">
                    <Zap className="h-5 w-5 text-purple-600" />
                </div>
                <div className="flex-1">
                    <div className="flex items-center gap-2">
                        <h4 className="font-bold text-purple-900 dark:text-purple-100">AI-Powered Suggestion</h4>
                        {topSuggestion.severity === 'high' && <span className="px-2 py-0.5 rounded-full bg-red-100 text-red-600 text-[10px] font-bold uppercase">Critical</span>}
                    </div>

                    <p className="text-sm text-purple-800 dark:text-purple-300 mt-1 leading-relaxed">
                        {topSuggestion.message}
                    </p>

                    <div className="flex items-center gap-4 mt-3">
                        <Button size="sm" variant="link" className="text-purple-700 dark:text-purple-400 p-0 h-auto font-bold group">
                            {topSuggestion.action} <ExternalLink className="ml-1 h-3 w-3 group-hover:translate-x-0.5 transition-transform" />
                        </Button>
                        {suggestions.length > 1 && (
                            <span className="text-xs text-purple-400">
                                +{suggestions.length - 1} more suggestions available
                            </span>
                        )}
                    </div>
                </div>
                <Button variant="ghost" size="icon" onClick={loadOptimizations} className="text-purple-400 hover:text-purple-600">
                    <RefreshCw className="h-4 w-4" />
                </Button>
            </div>
        </div>
    );
}
