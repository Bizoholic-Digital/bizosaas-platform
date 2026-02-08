import React, { useMemo } from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { CampaignGoals } from '../types/onboarding';
import {
    Target, Users, ShoppingBag, Radio, Sparkles,
    ArrowRight, Lightbulb, Zap, TrendingUp, ShieldCheck, Mail, CreditCard,
    Globe
} from 'lucide-react';
import * as Icons from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';

import { Progress } from '@/components/ui/progress';

interface Props {
    data: CampaignGoals;
    onUpdate: (data: Partial<CampaignGoals>) => void;
}

const GOALS = [
    {
        id: 'lead_gen',
        label: 'Lead Generation',
        desc: 'Find prospects & inquiries',
        icon: Users,
        specialist: 'Growth Specialist',
        recommendations: ['Postmark (Email)', 'LinkedIn Ads', 'Typeform']
    },
    {
        id: 'brand_awareness',
        label: 'Brand Awareness',
        desc: 'Build name recognition',
        icon: Radio,
        specialist: 'Brand Orchestrator',
        recommendations: ['Google Display', 'Meta Ads', 'Canva Integration']
    },
    {
        id: 'ecommerce_sales',
        label: 'Drive Sales',
        desc: 'Scale online transactions',
        icon: ShoppingBag,
        specialist: 'E-commerce Specialist',
        recommendations: ['Klaviyo (Email)', 'Stripe Checkout', 'Google Merchant']
    },
    {
        id: 'app_installs',
        label: 'App Growth',
        desc: 'Acquire active app users',
        icon: Target,
        specialist: 'Product Marketer',
        recommendations: ['Apple Search Ads', 'Deep Linking', 'Firebase']
    },
];

export function CampaignGoalsStep({ data, onUpdate }: Props) {
    const activeGoal = useMemo(() => GOALS.find(g => g.id === data.primaryGoal), [data.primaryGoal]);

    const budgetIntensity = useMemo(() => {
        if (data.monthlyBudget < 500) return { label: 'Initial Orbit', color: 'text-amber-500', desc: 'Starting focus on high-impact areas' };
        if (data.monthlyBudget < 2500) return { label: 'Steady Growth', color: 'text-blue-500', desc: 'Expanding reach across multiple channels' };
        if (data.monthlyBudget < 10000) return { label: 'Market Attack', color: 'text-purple-500', desc: 'Aggressive scaling for market dominance' };
        return { label: 'Hyper-Scale', color: 'text-green-500', desc: 'Total market immersion with AI-driven optimization' };
    }, [data.monthlyBudget]);

    return (
        <div className="space-y-10 animate-in fade-in slide-in-from-right-4 duration-700 max-w-4xl mx-auto">
            <div className="text-center space-y-2">
                <Badge variant="outline" className="px-3 py-1 border-blue-500/30 text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/10 font-black text-[10px] uppercase tracking-widest gap-2">
                    <Sparkles size={10} /> Strategy Design
                </Badge>
                <h2 className="text-3xl font-black text-foreground tracking-tight">Campaign Intelligence</h2>
                <p className="text-muted-foreground text-sm font-medium">Let's define the parameters for your AI Growth Specialist</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
                {/* Left Side: Goals & Budget */}
                <div className="lg:col-span-3 space-y-8">
                    <div className="space-y-4">
                        <Label className="text-[10px] font-black uppercase tracking-widest text-muted-foreground ml-1">Primary Objective</Label>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {GOALS.map((goal) => {
                                const isSelected = data.primaryGoal === goal.id;
                                const Icon = goal.icon;
                                return (
                                    <div
                                        key={goal.id}
                                        onClick={() => onUpdate({ primaryGoal: goal.id as any })}
                                        className={`
                                            cursor-pointer p-4 rounded-3xl transition-all duration-300 relative overflow-hidden group border-2
                                            ${isSelected
                                                ? 'border-blue-600 bg-blue-50/50 dark:bg-blue-900/10 shadow-lg shadow-blue-500/10'
                                                : 'border-slate-100 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-white dark:bg-slate-950'
                                            }
                                        `}
                                    >
                                        <div className="flex items-center gap-4 relative z-10">
                                            <div className={`p-3 rounded-2xl transition-all duration-500 ${isSelected ? 'bg-blue-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-500'}`}>
                                                <Icon size={20} />
                                            </div>
                                            <div className="text-left">
                                                <h4 className="font-bold text-sm text-foreground">{goal.label}</h4>
                                                <p className="text-[10px] text-muted-foreground font-medium">{goal.desc}</p>
                                            </div>
                                            {isSelected && <Zap className="w-4 h-4 ml-auto text-blue-600 animate-pulse" />}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>

                    <div className="space-y-6 pt-6 border-t border-slate-100 dark:border-slate-800">
                        <div className="flex justify-between items-end">
                            <div className="space-y-1">
                                <Label className="text-[10px] font-black uppercase tracking-widest text-muted-foreground ml-1">Monthly Ad Budget</Label>
                                <div className="flex items-center gap-2">
                                    <span className={`text-sm font-black uppercase tracking-tight ${budgetIntensity.color}`}>
                                        {budgetIntensity.label}
                                    </span>
                                    {data.monthlyBudget < 300 && (
                                        <Badge variant="outline" className="text-[8px] border-amber-500/50 text-amber-600 bg-amber-50 dark:bg-amber-900/10 font-bold px-1.5 py-0">
                                            AI Learning Warning
                                        </Badge>
                                    )}
                                </div>
                            </div>
                            <div className="flex flex-col items-end gap-1">
                                <span className="text-2xl font-black text-foreground">
                                    {data.monthlyBudget.toLocaleString()}
                                </span>
                                <Select
                                    value={data.currency}
                                    onValueChange={(val) => onUpdate({ currency: val })}
                                >
                                    <SelectTrigger className="h-6 w-16 text-[10px] font-bold border-none bg-muted/50 rounded-lg p-1">
                                        <SelectValue placeholder="USD" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="USD">USD ($)</SelectItem>
                                        <SelectItem value="EUR">EUR (€)</SelectItem>
                                        <SelectItem value="GBP">GBP (£)</SelectItem>
                                        <SelectItem value="INR">INR (₹)</SelectItem>
                                        <SelectItem value="AED">AED</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                        </div>
                        <Slider
                            value={[data.monthlyBudget]}
                            min={100}
                            max={50000}
                            step={50}
                            onValueChange={(val) => onUpdate({ monthlyBudget: val[0] })}
                            className="py-2"
                        />
                        <div className="p-3 rounded-2xl bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 space-y-2">
                            <p className="text-[10px] font-bold text-muted-foreground leading-relaxed flex items-center gap-2">
                                <TrendingUp size={14} className="text-blue-500" />
                                {budgetIntensity.desc}
                            </p>
                            {data.monthlyBudget < 300 && (
                                <p className="text-[9px] font-medium text-amber-600 dark:text-amber-400 bg-amber-500/5 p-2 rounded-xl italic">
                                    Note: Budgets under 300 {data.currency} may result in slower AI optimization due to limited data points.
                                </p>
                            )}
                        </div>
                    </div>

                    <div className="space-y-4 pt-6 border-t border-slate-100 dark:border-slate-800">
                        <Label className="text-[10px] font-black uppercase tracking-widest text-muted-foreground ml-1">Target Audience</Label>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label className="hidden text-left">Age Range</Label>
                                <Select
                                    value={data.targetAudience.ageRange}
                                    onValueChange={(val) => onUpdate({ targetAudience: { ...data.targetAudience, ageRange: val } })}
                                >
                                    <SelectTrigger className="h-12 rounded-2xl bg-white dark:bg-slate-950 border-slate-100 dark:border-slate-800 shadow-sm text-left">
                                        <SelectValue placeholder="Age Range" />
                                    </SelectTrigger>
                                    <SelectContent className="rounded-2xl border-slate-100">
                                        <SelectItem value="18-24">Gen Z (18-24)</SelectItem>
                                        <SelectItem value="25-34">Millennials (25-34)</SelectItem>
                                        <SelectItem value="35-44">Mid-Career (35-44)</SelectItem>
                                        <SelectItem value="45-54">Established (45-54)</SelectItem>
                                        <SelectItem value="55+">Seniors (55+)</SelectItem>
                                        <SelectItem value="all">Total Market (All)</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                            <div className="space-y-2">
                                <Label className="hidden text-left">Location</Label>
                                <div className="relative">
                                    <Input
                                        placeholder="Region / Country"
                                        className="h-12 rounded-2xl pl-10 bg-white dark:bg-slate-950 border-slate-100 dark:border-slate-800 shadow-sm"
                                        value={data.targetAudience.locations[0] || ''}
                                        onChange={(e) => onUpdate({ targetAudience: { ...data.targetAudience, locations: [e.target.value] } })}
                                    />
                                    <Globe className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Side: Agent Insight & Recommendations */}
                <div className="lg:col-span-2">
                    <div className="sticky top-4 space-y-4">
                        <div className="p-6 rounded-[2rem] bg-gradient-to-br from-slate-900 to-slate-800 dark:from-slate-900 dark:to-blue-900/20 text-white shadow-2xl relative overflow-hidden group">
                            <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:scale-110 transition-transform duration-700">
                                <Lightbulb size={120} />
                            </div>

                            <div className="relative z-10 space-y-6">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center shadow-lg shadow-blue-500/50">
                                        <Zap size={20} className="text-white" />
                                    </div>
                                    <div className="text-left">
                                        <p className="text-[10px] font-black uppercase opacity-60 tracking-widest leading-none mb-1">Assigned Specialist</p>
                                        <p className="text-lg font-black tracking-tight">{activeGoal?.specialist}</p>
                                    </div>
                                </div>

                                <div className="space-y-4 pt-4 border-t border-white/10">
                                    <p className="text-xs font-bold uppercase tracking-widest opacity-60 text-left flex items-center gap-2">
                                        <ArrowRight size={14} className="text-blue-400" />
                                        Strategic Power-Ups
                                    </p>
                                    <div className="space-y-2">
                                        {activeGoal?.recommendations.map((rec, i) => (
                                            <div key={rec} className="flex items-center gap-3 p-3 rounded-2xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                                                <div className="w-6 h-6 rounded-lg bg-blue-500/20 flex items-center justify-center">
                                                    {i === 0 ? <Mail size={12} className="text-blue-400" /> : i === 1 ? <TrendingUp size={12} className="text-blue-400" /> : <ShieldCheck size={12} className="text-blue-400" />}
                                                </div>
                                                <p className="text-xs font-bold text-left">{rec}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <p className="text-[10px] font-medium leading-relaxed italic opacity-80 text-left">
                                    "I've optimized your strategy to prioritize {activeGoal?.label.toLowerCase()}. We'll deploy targeted campaigns as soon as you launch."
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* AI Prediction Card */}
                    <div className="p-6 rounded-[2rem] bg-indigo-600/5 border border-indigo-600/10 space-y-4">
                        <div className="flex items-center gap-2">
                            <TrendingUp size={16} className="text-indigo-600" />
                            <h4 className="text-[10px] font-black uppercase tracking-widest text-indigo-700 dark:text-indigo-400">Projected Strategic Impact</h4>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-1">
                                <p className="text-[8px] font-bold text-muted-foreground uppercase tracking-widest leading-none">Conversion Lift</p>
                                <p className="text-xl font-black text-indigo-600">+{Math.floor((data.monthlyBudget / 1000) * 1.5 + 12)}%</p>
                            </div>
                            <div className="space-y-1">
                                <p className="text-[8px] font-bold text-muted-foreground uppercase tracking-widest leading-none">Audience Reach</p>
                                <p className="text-xl font-black text-indigo-600">{(data.monthlyBudget * 0.8 / 1000).toFixed(1)}M</p>
                            </div>
                        </div>
                        <div className="pt-2">
                            <Progress value={75} className="h-1 bg-indigo-100 dark:bg-indigo-900/20" />
                            <p className="text-[8px] font-bold text-indigo-700/40 uppercase tracking-widest mt-2">AI-Generated Forecast • 88% Confidence</p>
                        </div>
                    </div>

                    <div className="p-4 rounded-2xl bg-amber-500/5 border border-amber-500/10 flex gap-3">
                        <Zap size={18} className="text-amber-500 shrink-0" />
                        <p className="text-[10px] font-bold text-amber-900/60 dark:text-amber-500/60 leading-tight text-left">
                            You can finalize connecting these Power-Ups in your dashboard after launch.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
