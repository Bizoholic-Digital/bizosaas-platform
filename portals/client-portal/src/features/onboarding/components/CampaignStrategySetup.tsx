'use client';

import React from 'react';
import {
    Rocket, Sparkles, Target, BarChart3,
    ArrowRight, ShieldCheck, Zap,
    Facebook, Instagram, Globe, Twitter, Linkedin
} from 'lucide-react';
import { BusinessProfile } from './BusinessProfileSetup';

interface CampaignStrategySetupProps {
    profile: BusinessProfile;
    platforms: any[];
    budget: { dailyLimit: number; currency: string };
    onLaunch: () => void;
    isLaunching: boolean;
}

export function CampaignStrategySetup({
    profile,
    platforms,
    budget,
    onLaunch,
    isLaunching
}: CampaignStrategySetupProps) {
    const enabledPlatforms = platforms.filter(p => p.enabled);

    return (
        <div className="space-y-8 animate-in fade-in zoom-in-95 duration-700">
            <div className="text-center">
                <div className="inline-flex items-center px-4 py-1.5 bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-full text-sm font-bold mb-4">
                    <Sparkles className="w-4 h-4 mr-2" />
                    AI Strategy Generated
                </div>
                <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-3">
                    Your Launch Strategy is Ready! 🚀
                </h2>
                <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                    We've analyzed your business profile and goals to create a high-impact launch plan for {profile.name}.
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column: Summary & Audience */}
                <div className="lg:col-span-1 space-y-6">
                    <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-md border border-gray-200 dark:border-gray-700">
                        <h3 className="font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                            <Target className="w-5 h-5 mr-2 text-red-500" />
                            Target Audience
                        </h3>
                        <div className="space-y-3">
                            <div className="flex justify-between text-sm">
                                <span className="text-gray-500">Focus</span>
                                <span className="font-semibold capitalize">{profile.targetAudience.type.replace('-', ' ')}</span>
                            </div>
                            <div className="text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-900 p-3 rounded-lg border border-gray-100 dark:border-gray-800">
                                {profile.targetAudience.locations.join(', ') || 'No locations specified'}
                            </div>
                        </div>
                    </div>

                    <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-md border border-gray-200 dark:border-gray-700">
                        <h3 className="font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                            <BarChart3 className="w-5 h-5 mr-2 text-blue-500" />
                            Expected Outcomes
                        </h3>
                        <div className="space-y-4">
                            <div className="flex items-center group">
                                <div className="w-10 h-10 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center mr-3 group-hover:scale-110 transition-transform">
                                    <TrendingUp className="w-5 h-5 text-green-600" />
                                </div>
                                <div>
                                    <p className="text-sm font-bold text-gray-900 dark:text-white">+25% Reach</p>
                                    <p className="text-xs text-gray-500">Estimated first 30 days</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Column: Platform Breakdown & Launch */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-md border border-gray-200 dark:border-gray-700">
                        <h3 className="font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                            <Zap className="w-5 h-5 mr-2 text-yellow-500" />
                            Omnichannel Allocation
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {enabledPlatforms.map(platform => (
                                <div key={platform.id} className="p-4 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800 flex items-center">
                                    <div className="w-10 h-10 rounded-lg bg-white dark:bg-gray-800 flex items-center justify-center mr-4 shadow-sm">
                                        {platform.id === 'google' && <Globe className="w-5 h-5 text-blue-500" />}
                                        {platform.id === 'facebook' && <Facebook className="w-5 h-5 text-blue-600" />}
                                        {platform.id === 'instagram' && <Instagram className="w-5 h-5 text-pink-500" />}
                                        {(!['google', 'facebook', 'instagram'].includes(platform.id)) && <Zap className="w-5 h-5 text-amber-500" />}
                                    </div>
                                    <div className="flex-1">
                                        <p className="text-sm font-bold text-gray-900 dark:text-white capitalize">{platform.id}</p>
                                        <div className="flex items-center mt-1">
                                            <div className="flex-1 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full mr-3">
                                                <div className="h-full bg-blue-500 rounded-full" style={{ width: '40%' }} />
                                            </div>
                                            <span className="text-xs font-semibold text-gray-600 dark:text-gray-400">40%</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="bg-gradient-to-br from-blue-600 to-indigo-700 p-8 rounded-2xl shadow-xl text-white">
                        <div className="flex flex-col md:flex-row items-center justify-between mb-8">
                            <div className="mb-6 md:mb-0">
                                <p className="text-blue-100 text-sm font-medium mb-1">Total Daily Orbit</p>
                                <h4 className="text-4xl font-black">${budget.dailyLimit.toFixed(2)}</h4>
                            </div>
                            <div className="flex flex-col items-end">
                                <div className="flex items-center text-blue-100 text-sm mb-2">
                                    <ShieldCheck className="w-4 h-4 mr-1" />
                                    AI Optimization Active
                                </div>
                                <div className="flex items-center text-blue-100 text-sm">
                                    <Zap className="w-4 h-4 mr-1" />
                                    Real-time Bidding Enabled
                                </div>
                            </div>
                        </div>

                        <button
                            onClick={onLaunch}
                            disabled={isLaunching}
                            className="w-full bg-white text-blue-600 py-4 rounded-xl font-bold text-xl hover:bg-blue-50 transform hover:-translate-y-1 transition-all flex items-center justify-center shadow-lg active:scale-95 disabled:opacity-70 disabled:transform-none"
                        >
                            {isLaunching ? (
                                <>Launching Your Campaign...</>
                            ) : (
                                <>
                                    Approve & Launch 🚀
                                </>
                            )}
                        </button>
                        <p className="text-center text-xs text-blue-100/70 mt-4">
                            By clicking launch, you agree to start the campaigns on the selected platforms with the specified budget.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

// Helper icons missing from lucide
function TrendingUp(props: any) {
    return (
        <svg
            {...props}
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
            <polyline points="17 6 23 6 23 12" />
        </svg>
    );
}
