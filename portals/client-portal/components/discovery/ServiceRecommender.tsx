'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
    Sparkles,
    ArrowRight,
    Lightbulb,
    ShoppingCart,
    Mail,
    MessageSquare,
    Users,
    Zap,
    CheckCircle2,
    TrendingUp,
    Brain
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { brainApi } from '@/lib/brain-api';

interface Recommendation {
    id: string;
    name: string;
    description: string;
    category: string;
    icon: React.ReactNode;
    reason: string;
    impactScore: number;
    potentialGrowth: string;
    connected: boolean;
    color: string;
}

export const ServiceRecommender = () => {
    const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
    const [loading, setLoading] = useState(true);

    const getIcon = (type: string) => {
        switch (type) {
            case 'mail': return <Mail className="w-5 h-5" />;
            case 'message': return <MessageSquare className="w-5 h-5" />;
            case 'users': return <Users className="w-5 h-5" />;
            default: return <Zap className="w-5 h-5" />;
        }
    };

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const data = await brainApi.discovery.getRecommendations();
                const mapped = data.map((rec: any) => ({
                    ...rec,
                    icon: getIcon(rec.icon_type)
                }));
                setRecommendations(mapped);
            } catch (error) {
                console.error("Failed to fetch recommendations:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendations();
    }, []);

    if (loading) {
        return (
            <Card className="border-dashed border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50 overflow-hidden">
                <CardContent className="p-12 flex flex-col items-center justify-center space-y-4">
                    <div className="relative">
                        <div className="absolute inset-0 bg-indigo-500/20 blur-xl animate-pulse rounded-full" />
                        <Brain className="w-12 h-12 text-indigo-600 animate-bounce relative z-10" />
                    </div>
                    <div className="text-center space-y-2">
                        <h3 className="text-lg font-black uppercase italic tracking-tighter">Analyzing your Business Graph...</h3>
                        <p className="text-xs text-slate-500 font-medium italic">Our AI is identifying optimization gaps in your current stack.</p>
                    </div>
                </CardContent>
            </Card>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <div className="p-2 bg-indigo-600 rounded-lg shadow-lg shadow-indigo-500/20">
                        <Sparkles className="w-4 h-4 text-white" />
                    </div>
                    <div>
                        <h2 className="text-xl font-black uppercase italic tracking-tighter">AI Service <span className="text-indigo-600">Catalyst</span></h2>
                        <p className="text-[10px] uppercase font-bold text-slate-500 tracking-widest">Intelligent Growth Recommendations</p>
                    </div>
                </div>
                <Badge className="bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-300 border-none font-black italic text-[10px]">
                    POWERED BY BIZO-BRAIN v2
                </Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {recommendations.map((rec) => (
                    <Card key={rec.id} className="group relative border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xl overflow-hidden hover:shadow-2xl transition-all duration-500 hover:-translate-y-1">
                        <div className={`absolute top-0 left-0 w-full h-1 bg-${rec.color}-500`} />

                        <CardHeader className="pb-2">
                            <div className="flex justify-between items-start">
                                <div className={cn(
                                    "p-3 rounded-2xl shadow-inner",
                                    rec.color === 'amber' ? "bg-amber-50 dark:bg-amber-900/20 text-amber-600" :
                                        rec.color === 'purple' ? "bg-purple-50 dark:bg-purple-900/20 text-purple-600" :
                                            "bg-orange-50 dark:bg-orange-900/20 text-orange-600"
                                )}>
                                    {rec.icon}
                                </div>
                                <div className="text-right">
                                    <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none mb-1">Impact Score</div>
                                    <div className="text-2xl font-black italic text-slate-900 dark:text-white leading-none">{rec.impactScore}%</div>
                                </div>
                            </div>
                            <div className="pt-4">
                                <CardTitle className="text-lg font-black uppercase italic tracking-tighter truncate">{rec.name}</CardTitle>
                                <CardDescription className="text-xs font-medium italic line-clamp-2 h-8">{rec.description}</CardDescription>
                            </div>
                        </CardHeader>

                        <CardContent className="space-y-4">
                            <div className="p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-dashed border-slate-200 dark:border-slate-700">
                                <div className="flex items-center gap-2 mb-1">
                                    <Lightbulb className="w-3 h-3 text-indigo-500" />
                                    <span className="text-[10px] font-black uppercase text-indigo-600 tracking-tight">AI Reasoning</span>
                                </div>
                                <p className="text-[10px] text-slate-600 dark:text-slate-400 leading-relaxed font-bold italic">
                                    "{rec.reason}"
                                </p>
                            </div>

                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-1.5">
                                    <TrendingUp className="w-4 h-4 text-emerald-500" />
                                    <span className="text-xs font-black text-emerald-600 uppercase tracking-tighter italic">{rec.potentialGrowth}</span>
                                </div>
                                <Button variant="ghost" className="h-8 px-2 group-hover:bg-indigo-50 dark:group-hover:bg-indigo-900/20 group-hover:text-indigo-600 transition-colors">
                                    <span className="text-[10px] font-black uppercase tracking-widest mr-1">Activate</span>
                                    <ArrowRight className="w-3 h-3 transition-transform group-hover:translate-x-1" />
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
};
