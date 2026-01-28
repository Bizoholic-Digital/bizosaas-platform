import React, { useState, useEffect, useMemo } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { OnboardingState } from '../types/onboarding';
import {
    CheckCircle2, ArrowRight, Brain, Target, TrendingUp, Zap,
    Sparkles, Database, ShieldCheck, Rocket,
    Activity, Cpu, Lock, FileText, ShoppingBag, ShoppingCart, Users, BarChart3, ClipboardList, Settings, Search
} from 'lucide-react';
import * as Icons from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

interface Props {
    data: OnboardingState;
    onConfirm: () => void;
}

export function StrategyApprovalStep({ data, onConfirm }: Props) {
    const [isGenerating, setIsGenerating] = useState(true);
    const [strategyGenerated, setStrategyGenerated] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => {
            setIsGenerating(false);
            setStrategyGenerated(true);
        }, 3000);
        return () => clearTimeout(timer);
    }, []);

    const dataScore = useMemo(() => {
        let score = 0;
        if (data.profile.companyName) score += 20;
        if (data.profile.website) score += 20;
        if (data.digitalPresence.cmsType) score += 15;
        if (data.tools.selectedMcps && data.tools.selectedMcps.length > 0) score += 15;
        if (data.analytics.gaId || data.analytics.gtmId) score += 15;
        if (data.goals.primaryGoal) score += 15;
        return score;
    }, [data.profile, data.digitalPresence, data.tools, data.analytics, data.goals]);

    const strategyInputs = [
        { label: 'Infrastructure', value: data.digitalPresence.cmsType?.toUpperCase() || 'Custom', icon: Cpu },
        { label: 'Growth Objective', value: data.goals.primaryGoal?.replace('_', ' ').toUpperCase(), icon: Target },
        { label: 'Target Market', value: data.goals.targetAudience.locations[0] || 'Global', icon: Activity },
        { label: 'Ad Intensity', value: (data.goals?.monthlyBudget || 0) < 2500 ? 'Growth' : 'Market Attack', icon: TrendingUp },
    ];

    return (
        <div className="space-y-10 animate-in fade-in slide-in-from-right-4 duration-1000 max-w-4xl mx-auto">
            {/* Header Section */}
            <div className="text-center space-y-4">
                <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900 text-white text-[10px] font-black uppercase tracking-widest border border-white/10 shadow-2xl">
                    {isGenerating ? (
                        <>
                            <div className="w-2 h-2 rounded-full bg-blue-500 animate-ping" />
                            AI Strategy Synthesis In Progress
                        </>
                    ) : (
                        <>
                            <ShieldCheck size={12} className="text-green-500" />
                            Strategic Pre-Flight Approved
                        </>
                    )}
                </div>
                <h2 className="text-4xl font-black text-foreground tracking-tight leading-none">Final Strategy Approval</h2>
                <p className="text-muted-foreground text-sm font-medium">Your platform is provisioned and ready for deployment.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-6 gap-8">
                {/* Left: Pre-Flight Checklist */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="p-6 rounded-[2.5rem] bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 space-y-6">
                        <div className="space-y-1 text-left">
                            <p className="text-[10px] font-black uppercase tracking-widest text-muted-foreground opacity-60">Strategy Confidence</p>
                            <div className="flex items-center justify-between">
                                <span className="text-3xl font-black text-foreground">{dataScore}%</span>
                                <Badge variant="outline" className={`border-none ${dataScore > 80 ? 'bg-green-500/10 text-green-600' : 'bg-amber-500/10 text-amber-600'} font-black px-2 py-0 text-[10px]`}>
                                    {dataScore > 80 ? 'HIGH' : 'STABLE'}
                                </Badge>
                            </div>
                            <Progress value={dataScore} className="h-1.5 bg-slate-200 dark:bg-slate-800" />
                        </div>

                        <div className="space-y-4 pt-4 border-t border-slate-200 dark:border-slate-800">
                            {strategyInputs.map((input, i) => (
                                <div key={i} className="flex items-center gap-3">
                                    <div className="p-2 rounded-xl bg-white dark:bg-slate-950 shadow-sm border border-slate-100 dark:border-slate-800">
                                        <input.icon size={14} className="text-blue-500" />
                                    </div>
                                    <div className="text-left">
                                        <p className="text-[8px] font-black text-muted-foreground uppercase tracking-widest leading-none mb-1">{input.label}</p>
                                        <p className="text-[11px] font-bold text-foreground truncate max-w-[120px]">{input.value}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="p-4 rounded-3xl bg-blue-600/5 border border-blue-600/10 flex items-start gap-3">
                        <Lock size={16} className="text-blue-600 mt-1" />
                        <p className="text-[10px] font-bold text-blue-900/60 dark:text-blue-400/60 leading-relaxed text-left italic">
                            All credentials and API keys are secured via HashiCorp Vault.
                        </p>
                    </div>
                </div>

                {/* Right: AI Output Simulation */}
                <div className="lg:col-span-4 space-y-6">
                    {isGenerating ? (
                        <div className="h-full min-h-[400px] flex flex-col items-center justify-center p-12 rounded-[3rem] border-2 border-dashed border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50">
                            <div className="relative">
                                <Brain size={64} className="text-blue-600 animate-pulse mb-6" />
                                <div className="absolute inset-0 border-4 border-blue-500/30 rounded-full animate-ping scale-150 opacity-20" />
                            </div>
                            <h3 className="text-lg font-black uppercase tracking-tight mb-2">Analyzing Marketplace Context...</h3>
                            <div className="flex gap-1">
                                {[1, 2, 3].map(i => (
                                    <div key={i} className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: `${i * 0.15}s` }} />
                                ))}
                            </div>
                        </div>
                    ) : (
                        <div className="space-y-6 animate-in fade-in zoom-in-95 duration-1000">
                            {/* Strategy Card */}
                            <Card className="rounded-[3rem] border-none bg-gradient-to-br from-blue-600 to-indigo-700 shadow-2xl shadow-blue-500/20 overflow-hidden relative">
                                <div className="absolute top-0 right-0 p-12 opacity-10 rotate-12">
                                    <Sparkles size={160} className="text-white" />
                                </div>
                                <CardContent className="p-10 space-y-8 relative z-10 text-white">
                                    <div className="flex items-center gap-4">
                                        <div className="p-3 rounded-2xl bg-white/20 backdrop-blur-md">
                                            <Rocket size={24} className="text-white" />
                                        </div>
                                        <div className="text-left">
                                            <h3 className="text-xl font-black tracking-tight leading-none mb-1">Deployment Roadmap</h3>
                                            <p className="text-[10px] uppercase font-black tracking-widest opacity-60">BizOSaaS Brain v1.2</p>
                                        </div>
                                    </div>

                                    <div className="space-y-4">
                                        <p className="text-[10px] font-black uppercase tracking-widest opacity-60 text-left">Activating Specialist Workforce</p>
                                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                            {data.tools.selectedMcps?.slice(0, 4).map((mcp, i) => {
                                                const mapping: Record<string, { label: string, icon: any }> = {
                                                    'wordpress': { label: 'Content Creator', icon: Icons.FileText },
                                                    'shopify': { label: 'Store Manager', icon: Icons.ShoppingBag },
                                                    'woocommerce': { label: 'E-com Specialist', icon: Icons.ShoppingCart },
                                                    'fluentcrm': { label: 'Lead Specialist', icon: Icons.Users },
                                                    'google-analytics-4': { label: 'Data Analyst', icon: Icons.BarChart3 },
                                                    'plane': { label: 'Work Strategist', icon: Icons.ClipboardList },
                                                    'google-tag-manager': { label: 'Tech Architect', icon: Icons.Settings },
                                                    'google-search-console': { label: 'SEO Optimizer', icon: Icons.Search },
                                                };
                                                const agent = mapping[mcp] || { label: mcp.split('-').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(' '), icon: Icons.Cpu };
                                                const AgentIcon = agent.icon;
                                                return (
                                                    <div key={i} className="p-3 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 flex flex-col items-center gap-2 group hover:bg-white/20 transition-all cursor-default">
                                                        <div className="p-2 rounded-xl bg-white/20">
                                                            <AgentIcon size={16} className="text-white" />
                                                        </div>
                                                        <p className="text-[9px] font-black uppercase tracking-tight text-center leading-tight">{agent.label}</p>
                                                        <div className="flex gap-0.5 mt-1">
                                                            <div className="w-1 h-1 rounded-full bg-green-400 animate-pulse" />
                                                            <div className="w-1 h-1 rounded-full bg-green-400/40" />
                                                            <div className="w-1 h-1 rounded-full bg-green-400/20" />
                                                        </div>
                                                    </div>
                                                );
                                            })}
                                            {(!data.tools.selectedMcps || data.tools.selectedMcps.length === 0) && (
                                                <div className="col-span-full py-4 text-center opacity-40 italic text-xs">No specific specialists selected. Using General Intelligence.</div>
                                            )}
                                        </div>
                                    </div>

                                    <div className="pt-6 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-6">
                                        <div className="flex items-center gap-6">
                                            <div className="space-y-1 text-left">
                                                <p className="text-[10px] font-black uppercase tracking-widest opacity-60">Neural Capacity</p>
                                                <p className="font-black text-lg">Optimized</p>
                                            </div>
                                            <div className="h-8 w-px bg-white/10 hidden md:block" />
                                            <div className="space-y-1 text-left">
                                                <p className="text-[10px] font-black uppercase tracking-widest opacity-60">Status</p>
                                                <p className="font-black text-lg flex items-center gap-2">
                                                    <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" /> READY
                                                </p>
                                            </div>
                                        </div>
                                        <Button
                                            onClick={onConfirm}
                                            className="bg-white text-blue-600 hover:bg-slate-100 rounded-full py-6 px-10 font-black uppercase text-xs tracking-widest shadow-xl transition-all hover:scale-105 active:scale-95"
                                        >
                                            Ignition & Launch <ArrowRight size={16} className="ml-2" />
                                        </Button>
                                    </div>
                                </CardContent>
                            </Card>

                            <div className="grid grid-cols-3 gap-3">
                                {[
                                    { label: 'Cloud Workers', icon: Activity, value: 'Operational' },
                                    { label: 'RAG Specialists', icon: Brain, value: 'Standby' },
                                    { label: 'CRM Sync', icon: Database, value: 'Enabled' }
                                ].map((stat, i) => (
                                    <div key={i} className="p-4 rounded-[2rem] bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex flex-col items-center gap-2">
                                        <stat.icon size={16} className="text-blue-500" />
                                        <div className="text-center">
                                            <p className="text-[8px] font-black text-muted-foreground uppercase tracking-widest mb-0.5">{stat.label}</p>
                                            <p className="text-[10px] font-black text-foreground">{stat.value}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>

            <p className="text-[10px] font-bold text-muted-foreground/40 text-center uppercase tracking-widest">
                By clicking launch, you authorize the BizOSaaS Brain to provision all selected tools and specialists.
            </p>
        </div>
    );
}
