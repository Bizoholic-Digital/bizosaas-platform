import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { OnboardingState } from '../types/onboarding';
import { CheckCircle2, ArrowRight, Brain, Target, TrendingUp, Zap, Sparkles, Database } from 'lucide-react';

interface Props {
    data: OnboardingState;
    onConfirm: () => void;
}

export function StrategyApprovalStep({ data, onConfirm }: Props) {
    const [isGenerating, setIsGenerating] = useState(true);
    const [strategyGenerated, setStrategyGenerated] = useState(false);

    useEffect(() => {
        // Simulate AI strategy generation
        const timer = setTimeout(() => {
            setIsGenerating(false);
            setStrategyGenerated(true);
        }, 2000);
        return () => clearTimeout(timer);
    }, []);

    // Calculate data completeness score
    const getDataScore = () => {
        let score = 0;
        if (data.profile.companyName) score += 15;
        if (data.profile.website) score += 15;
        if (data.digitalPresence.hasTracking) score += 10;
        if (data.tools.selectedMcps?.length > 0) score += 10;
        if (data.analytics.gtmId) score += 15;
        if (data.socialMedia.platforms.length > 0) score += 15;
        if (data.goals.primaryGoal) score += 10;
        if (data.goals.monthlyBudget > 0) score += 10;
        return score;
    };

    const dataScore = getDataScore();

    // AI Strategy inputs summary
    const strategyInputs = [
        {
            label: 'Business Profile',
            value: `${data.profile?.companyName || 'Not provided'} • ${data.profile?.industry || 'Not set'}`,
            icon: Database,
            complete: !!data.profile?.companyName
        },
        {
            label: 'Digital Presence',
            value: data.profile?.website || 'Not provided',
            icon: TrendingUp,
            complete: !!data.profile?.website
        },
        {
            label: 'Primary Goal',
            value: String(data.goals?.primaryGoal || '').replace('_', ' ').toUpperCase() || 'Not set',
            icon: Target,
            complete: !!data.goals?.primaryGoal
        },
        {
            label: 'Monthly Budget',
            value: `${data.goals?.currency || 'USD'} ${(data.goals?.monthlyBudget || 0).toLocaleString()}`,
            icon: Zap,
            complete: (data.goals?.monthlyBudget || 0) > 0
        },
        {
            label: 'Target Audience',
            value: `${data.goals?.targetAudience?.ageRange || 'Not set'} • ${(data.goals?.targetAudience?.locations || []).join(', ') || 'Global'}`,
            icon: Brain,
            complete: !!data.goals?.targetAudience?.ageRange
        },
        {
            label: 'Selected Tools',
            value: `${data.tools?.selectedMcps?.length || 0} integrations`,
            icon: Sparkles,
            complete: (data.tools?.selectedMcps?.length || 0) > 0
        }
    ];

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-8">
                {isGenerating ? (
                    <>
                        <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
                            <Brain size={32} className="animate-spin" />
                        </div>
                        <h2 className="text-2xl font-bold text-foreground">Strategy AI Analyzing...</h2>
                        <p className="text-muted-foreground">Processing your business data to create a custom strategy</p>
                    </>
                ) : (
                    <>
                        <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce">
                            <CheckCircle2 size={32} />
                        </div>
                        <h2 className="text-2xl font-bold text-foreground">AI Strategy Ready</h2>
                        <p className="text-muted-foreground">Your personalized growth strategy has been generated</p>
                    </>
                )}
            </div>

            {/* Data Completeness Score */}
            <Card className="border-blue-200 bg-blue-50/50">
                <CardContent className="pt-6">
                    <div className="flex items-center justify-between mb-3">
                        <span className="text-sm font-semibold text-blue-900">Data Completeness</span>
                        <span className="text-2xl font-bold text-blue-600">{dataScore}%</span>
                    </div>
                    <div className="w-full bg-blue-200 rounded-full h-2">
                        <div
                            className="bg-blue-600 h-2 rounded-full transition-all duration-1000"
                            style={{ width: `${dataScore}%` }}
                        />
                    </div>
                    <p className="text-xs text-blue-700 mt-2">
                        {dataScore >= 80 ? '✓ Excellent data quality for AI strategy generation' :
                            dataScore >= 60 ? '⚠ Good data, but more inputs improve strategy accuracy' :
                                '⚠ Limited data - strategy will be generic'}
                    </p>
                </CardContent>
            </Card>

            {/* Strategy Inputs Overview */}
            <div className="space-y-3">
                <h3 className="text-sm font-bold text-foreground flex items-center gap-2">
                    <Database size={16} />
                    Data Provided to Strategy AI Agent
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {strategyInputs.map((input, idx) => (
                        <Card key={idx} className={`transition-all ${input.complete ? 'border-green-200 bg-green-50/30' : 'border-gray-200 bg-gray-50/30'}`}>
                            <CardContent className="p-4 flex items-start gap-3">
                                <div className={`p-2 rounded-lg ${input.complete ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'}`}>
                                    <input.icon size={18} />
                                </div>
                                <div className="flex-1 min-w-0">
                                    <div className="text-xs text-muted-foreground uppercase tracking-wider">{input.label}</div>
                                    <div className="font-semibold text-sm text-foreground truncate">{input.value}</div>
                                </div>
                                {input.complete && <CheckCircle2 size={16} className="text-green-500 flex-shrink-0" />}
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>

            {/* AI-Generated Strategy Preview */}
            {strategyGenerated && (
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-6 relative overflow-hidden animate-in slide-in-from-bottom-4">
                    <div className="absolute top-0 right-0 w-32 h-32 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 transform translate-x-12 -translate-y-12"></div>

                    <div className="flex items-center gap-2 mb-4">
                        <Brain className="text-blue-600" size={24} />
                        <h3 className="font-bold text-blue-900 text-lg">AI-Generated Strategy</h3>
                    </div>

                    <div className="space-y-4">
                        <div className="bg-white/60 backdrop-blur-sm rounded-lg p-4 border border-blue-100">
                            <h4 className="text-sm font-bold text-blue-800 mb-2">Strategic Approach</h4>
                            <p className="text-blue-900 leading-relaxed">
                                Based on your <b>{data.goals.primaryGoal?.replace('_', ' ')}</b> goal with a
                                <b> {data.goals.currency}{data.goals.monthlyBudget.toLocaleString()}</b> monthly budget,
                                our AI recommends a {data.goals.monthlyBudget < 1000 ? 'lean, high-ROI' : 'multi-channel growth'} strategy
                                targeting <b>{data.goals.targetAudience.ageRange}</b> audience in <b>{data.goals.targetAudience.locations.join(', ') || 'Global markets'}</b>.
                            </p>
                        </div>

                        <div className="grid grid-cols-2 gap-3">
                            <div className="bg-white/60 backdrop-blur-sm p-3 rounded-lg border border-blue-100">
                                <span className="text-xs text-blue-600 font-bold uppercase tracking-wider block mb-1">Channels</span>
                                <span className="font-semibold text-blue-900">
                                    {data.socialMedia.platforms.length > 0
                                        ? data.socialMedia.platforms.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(', ')
                                        : 'SEO + Content Marketing'}
                                </span>
                            </div>
                            <div className="bg-white/60 backdrop-blur-sm p-3 rounded-lg border border-blue-100">
                                <span className="text-xs text-blue-600 font-bold uppercase tracking-wider block mb-1">Budget Split</span>
                                <span className="font-semibold text-blue-900">
                                    {data.goals.monthlyBudget < 1000 ? '80% Organic / 20% Paid' : '60% Acquisition / 40% Retention'}
                                </span>
                            </div>
                        </div>

                        <div className="bg-blue-600/10 backdrop-blur-sm p-4 rounded-lg border border-blue-300">
                            <span className="text-xs text-blue-700 font-bold uppercase tracking-wider block mb-2">AI Agents Assigned</span>
                            <div className="flex flex-wrap gap-2">
                                <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full font-medium">Research Agent</span>
                                <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full font-medium">Content Agent</span>
                                <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full font-medium">Analytics Agent</span>
                                {data.socialMedia.platforms.length > 0 && (
                                    <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full font-medium">Social Agent</span>
                                )}
                                {data.analytics.gtmId && (
                                    <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full font-medium">Tracking Agent</span>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-4 pt-6">
                <Button
                    onClick={onConfirm}
                    disabled={!strategyGenerated}
                    className="flex-1 h-12 text-base font-semibold"
                >
                    {strategyGenerated ? (
                        <>
                            Launch Platform <ArrowRight className="ml-2" size={20} />
                        </>
                    ) : (
                        'Generating Strategy...'
                    )}
                </Button>
            </div>

            <div className="text-center text-sm text-muted-foreground">
                <p>✓ All AI agents are configured and ready to execute</p>
                <p className="text-xs mt-1">Strategy will be refined continuously based on performance data</p>
            </div>
        </div>
    );
}
