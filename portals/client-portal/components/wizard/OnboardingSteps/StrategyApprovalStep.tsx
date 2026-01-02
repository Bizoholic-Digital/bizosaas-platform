import React from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { OnboardingState } from '../types/onboarding';
import { CheckCircle2, ArrowRight, Rocket } from 'lucide-react';

interface Props {
    data: OnboardingState;
    onConfirm: () => void;
}

export function StrategyApprovalStep({ data, onConfirm }: Props) {
    // Simple strategy synthesis logic
    const getStrategySummary = () => {
        let summary = `Focus on ${data.goals.primaryGoal.replace('_', ' ')} for ${data.profile.companyName} `;
        if (data.profile.industry) summary += `in the ${data.profile.industry} sector `;
        summary += `using `;

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
                <h2 className="text-2xl font-bold text-gray-900">Strategy Draft Ready</h2>
                <p className="text-gray-500">Based on your inputs, we've designed this initial plan.</p>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 rounded-xl p-6 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 transform translate-x-12 -translate-y-12"></div>

                <h3 className="font-bold text-blue-900 mb-2">Recommended Strategy</h3>
                <p className="text-blue-800 text-lg leading-relaxed font-medium">
                    {getStrategySummary()}
                </p>

                <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div className="bg-white/60 p-3 rounded-lg">
                        <span className="text-gray-500 block text-xs uppercase tracking-wider">Mission</span>
                        <p className="font-medium text-gray-900 line-clamp-2">
                            {data.profile.description || 'Promoting business growth and digital excellence.'}
                        </p>
                    </div>
                    <div className="bg-white/60 p-3 rounded-lg">
                        <span className="text-gray-500 block text-xs uppercase tracking-wider">Target Audience</span>
                        <p className="font-medium text-gray-900 line-clamp-2">
                            {data.profile.target_audience_desc || 'General market and niche prospects.'}
                        </p>
                    </div>
                    <div className="bg-white/60 p-3 rounded-lg">
                        <span className="text-gray-500 block text-xs uppercase tracking-wider">Focus Offering</span>
                        <p className="font-medium text-gray-900 line-clamp-2">
                            {data.profile.main_products_services || 'Core business solutions.'}
                        </p>
                    </div>
                    <div className="bg-white/60 p-3 rounded-lg">
                        <span className="text-gray-500 block text-xs uppercase tracking-wider">Active Channels</span>
                        <span className="font-semibold text-gray-900">
                            {data.socialMedia.platforms.length ? data.socialMedia.platforms.join(', ') : 'SEO & Content'}
                        </span>
                    </div>
                </div>
            </div>

            <div className="space-y-4">
                <h3 className="font-bold text-gray-900 flex items-center gap-2">
                    <Rocket className="text-blue-600 w-5 h-5" />
                    Live Execution Plan (Synced with Plane)
                </h3>
                <div className="space-y-2">
                    {[
                        { title: "Technical Infrastructure Setup", status: "queued", icon: "⚙️" },
                        { title: "Analytics & Tracking Integration", status: "queued", icon: "📈" },
                        { title: "Campaign Asset Creation", status: "queued", icon: "🎨" },
                        { title: "Channel Connection & Verification", status: "queued", icon: "🔗" }
                    ].map((task, i) => (
                        <div key={i} className="flex items-center justify-between p-3 bg-white border border-gray-100 rounded-lg shadow-sm group hover:border-blue-200 transition-colors">
                            <div className="flex items-center gap-3">
                                <span className="text-lg">{task.icon}</span>
                                <span className="text-sm font-medium text-gray-700">{task.title}</span>
                            </div>
                            <span className="text-[10px] font-bold uppercase tracking-widest text-gray-400 bg-gray-50 px-2 py-1 rounded">
                                {task.status}
                            </span>
                        </div>
                    ))}
                </div>
                <p className="text-xs text-center text-gray-400">
                    * Tasks will be automatically assigned to our AI Agents upon approval.
                </p>
            </div>
        </div>
    );
}
