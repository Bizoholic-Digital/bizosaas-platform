'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Sparkles, ArrowRight, Zap, Lightbulb } from 'lucide-react';
import { connectorsApi } from '@/lib/api/connectors';
import { toast } from 'sonner';

interface Recommendation {
    id: string;
    name: string;
    description: string;
    category: string;
    reason: string;
    impactScore: number;
    potentialGrowth: string;
    connected: boolean;
    color: string;
    icon_type: string;
    is_detected?: boolean;
}

export function DiscoveryWidget() {
    const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadRecommendations = async () => {
            try {
                const res = await connectorsApi.getRecommendations();
                if (res.data && Array.isArray(res.data)) {
                    setRecommendations(res.data);
                }
            } catch (error) {
                console.error("Failed to load recommendations", error);
            } finally {
                setLoading(false);
            }
        };

        loadRecommendations();
    }, []);

    if (loading || recommendations.length === 0) return null;

    return (
        <div className="mb-8 space-y-4">
            <div className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-indigo-500" />
                <h2 className="text-xl font-semibold bg-gradient-to-r from-indigo-500 to-purple-600 bg-clip-text text-transparent">
                    Magic Discovery
                </h2>
                <Badge variant="secondary" className="bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300 border-0">
                    AI Insights
                </Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendations.map((rec) => (
                    <Card key={rec.id} className={`group relative overflow-hidden border-indigo-100 dark:border-indigo-900/50 bg-gradient-to-br from-white to-indigo-50/30 dark:from-slate-950 dark:to-indigo-900/10 hover:shadow-md transition-all`}>
                        {rec.is_detected && (
                            <div className="absolute top-0 right-0 p-3">
                                <Badge className="bg-green-100 text-green-700 hover:bg-green-100 border-green-200 shadow-sm animate-pulse">
                                    <Zap className="w-3 h-3 mr-1 fill-green-700" /> Detected
                                </Badge>
                            </div>
                        )}

                        <CardHeader className="pb-3">
                            <div className="flex items-start justify-between">
                                <div className="space-y-1">
                                    <Badge variant="outline" className="mb-2 text-xs font-normal text-muted-foreground">
                                        {rec.category}
                                    </Badge>
                                    <CardTitle className="text-base font-bold flex items-center gap-2">
                                        {rec.name}
                                    </CardTitle>
                                </div>
                                <div className={`p-2 rounded-full bg-${rec.color}-100 text-${rec.color}-600 dark:bg-${rec.color}-900/20`}>
                                    <Lightbulb className="w-4 h-4" />
                                </div>
                            </div>
                            <CardDescription className="line-clamp-2 text-xs mt-2">
                                {rec.description}
                            </CardDescription>
                        </CardHeader>

                        <CardContent className="pb-3">
                            <div className="p-3 bg-white/50 dark:bg-slate-900/50 rounded-lg border border-indigo-100/50 dark:border-indigo-900/20">
                                <div className="flex items-start gap-2">
                                    <Sparkles className="w-3 h-3 text-indigo-500 mt-0.5 flex-shrink-0" />
                                    <p className="text-xs font-medium text-slate-700 dark:text-slate-300">
                                        "{rec.reason}"
                                    </p>
                                </div>
                                <div className="mt-3 flex items-center justify-between text-xs">
                                    <div className="flex flex-col">
                                        <span className="text-muted-foreground">Impact Score</span>
                                        <span className="font-bold text-indigo-600">{rec.impactScore}/100</span>
                                    </div>
                                    <div className="flex flex-col text-right">
                                        <span className="text-muted-foreground">Potential</span>
                                        <span className="font-bold text-green-600">{rec.potentialGrowth}</span>
                                    </div>
                                </div>
                            </div>
                        </CardContent>

                        <CardFooter>
                            <Button size="sm" className="w-full bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm group-hover:shadow-indigo-500/25 transition-all">
                                Connect Now <ArrowRight className="w-3 h-3 ml-2 group-hover:translate-x-1 transition-transform" />
                            </Button>
                        </CardFooter>
                    </Card>
                ))}
            </div>

            <div className="h-px w-full bg-slate-200 dark:bg-slate-800 my-6" />
        </div>
    );
}
