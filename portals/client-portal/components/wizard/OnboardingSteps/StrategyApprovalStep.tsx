import React from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { OnboardingState } from '../types/onboarding';
import { CheckCircle2, ArrowRight } from 'lucide-react';

interface Props {
    data: OnboardingState;
    onConfirm: () => void;
}

export function StrategyApprovalStep({ data, onConfirm }: Props) {
    // Simple strategy synthesis logic
    const getStrategySummary = () => {
        let summary = `Focus on ${data.goals.primaryGoal.replace('_', ' ')} using `;
        if (data.socialMedia.platforms.length > 0) {
            summary += data.socialMedia.platforms.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(', ');
        } else {
            summary += "organic search and content";
        }

        if (data.goals.monthlyBudget < 500) {
            summary += ". Lean budget strategy: Retargeting + High intent search.";
        } else {
            summary += ". Growth budget strategy: Multi-channel acquisition.";
        }
        return summary;
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-8">
                <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce">
                    <CheckCircle2 size={32} />
                </div>
                <h2 className="text-2xl font-bold text-foreground">Strategy Draft Ready</h2>
                <p className="text-muted-foreground">Based on your inputs, we've designed this initial plan.</p>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 rounded-xl p-6 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 transform translate-x-12 -translate-y-12"></div>

                <h3 className="font-bold text-blue-900 mb-2">Recommended Strategy</h3>
                <p className="text-blue-800 text-lg leading-relaxed font-medium">
                    {getStrategySummary()}
                </p>

                <div className="mt-6 grid grid-cols-2 gap-4 text-sm">
                    <div className="bg-card/60 p-3 rounded-lg">
                        <span className="text-muted-foreground block text-xs uppercase tracking-wider">Channels</span>
                        <span className="font-semibold text-foreground capitalize">
                            {data.socialMedia.platforms.length ? data.socialMedia.platforms.join(', ') : 'SEO & Content'}
                        </span>
                    </div>
                    <div className="bg-card/60 p-3 rounded-lg">
                        <span className="text-muted-foreground block text-xs uppercase tracking-wider">Budget Allocation</span>
                        <span className="font-semibold text-foreground">
                            70% Acquisition / 30% Retargeting
                        </span>
                    </div>
                    <div className="bg-card/60 p-3 rounded-lg col-span-2 border border-blue-200/50 bg-blue-500/5">
                        <span className="text-blue-600/80 block text-[10px] uppercase font-bold tracking-widest mb-1">Technical Foundation</span>
                        <span className="font-semibold text-blue-900 dark:text-blue-100 flex items-center gap-1.5">
                            {data.analytics.gtmId || 'Auto-Provision GTM'}
                            {data.marketplace.useBridge && <span className="text-xs font-normal opacity-60">• BizOSaaS Bridge Active</span>}
                            {data.marketplace.selectedThemes.length > 0 && <span className="text-xs font-normal opacity-60">• {data.marketplace.selectedThemes[0]} Theme</span>}
                        </span>
                    </div>
                </div>
            </div>

            <div className="text-center text-sm text-muted-foreground py-4">
                Our AI Agents are ready to execute this plan upon your approval.
            </div>
        </div>
    );
}
