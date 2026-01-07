'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
    Building2,
    Globe,
    BarChart3,
    Share2,
    Target,
    Plug,
    Rocket,
    Megaphone,
    Bot,
    Sparkles
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useOnboardingState } from './hooks/useOnboardingState';
import { useUser } from '@clerk/nextjs';
import { OnboardingState } from './types/onboarding';
import { useEffect } from 'react';

// Step Components
import { CompanyIdentityStep } from './OnboardingSteps/CompanyIdentityStep';
import { DigitalPresenceStep } from './OnboardingSteps/DigitalPresenceStep';
import { AnalyticsTrackingStep } from './OnboardingSteps/AnalyticsTrackingStep';
import { SocialMediaStep } from './OnboardingSteps/SocialMediaStep';
import { CampaignGoalsStep } from './OnboardingSteps/CampaignGoalsStep';
import { CategorizedToolSelectionStep } from './OnboardingSteps/CategorizedToolSelectionStep';
import { AgentSelectionStep } from './OnboardingSteps/AgentSelectionStep';
import { StrategyApprovalStep } from './OnboardingSteps/StrategyApprovalStep';
import { AIAssistantIntroStep } from './OnboardingSteps/AIAssistantIntroStep';

const STEPS = [
    { id: 'identity', title: 'Identity', icon: Building2 },
    { id: 'presence', title: 'Presence', icon: Globe },
    { id: 'tools', title: 'Select Tools', icon: Plug },
    { id: 'ai_intro', title: 'AI Team', icon: Sparkles }, // New Step
    { id: 'analytics', title: 'Analytics', icon: BarChart3 },
    { id: 'social', title: 'Social', icon: Share2 },
    { id: 'goals', title: 'Goals', icon: Target },
    { id: 'agent', title: 'AI Agent', icon: Bot },
    { id: 'approval', title: 'Strategy', icon: Rocket }
];

export function OnboardingWizard() {
    const router = useRouter();
    const { user, isLoaded: isClerkLoaded } = useUser();
    const {
        state,
        updateProfile,
        updateDigitalPresence,
        updateDiscovery,
        updateAnalytics,
        updateSocialMedia,
        updateGoals,
        updateTools,
        updateAgent,
        setSocialLogin,
        nextStep,
        prevStep,
        isLoaded
    } = useOnboardingState();

    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isDiscovering, setIsDiscovering] = useState(false);

    // Sync Clerk user with onboarding state
    useEffect(() => {
        if (isClerkLoaded && user && !state.socialLogin) {
            const primaryEmail = user.primaryEmailAddress?.emailAddress || "";
            const provider = user.externalAccounts[0]?.provider || 'none';

            setSocialLogin({
                provider: provider.includes('google') ? 'google' :
                    provider.includes('microsoft') ? 'microsoft' :
                        provider.includes('facebook') ? 'facebook' : 'none',
                email: primaryEmail,
                name: user.fullName || undefined,
                profileImageUrl: user.imageUrl
            });

            // If we have a provider, trigger initial discovery
            if (provider !== 'none') {
                triggerDiscovery(primaryEmail, provider);
            }
        }
    }, [isClerkLoaded, user, state.socialLogin, setSocialLogin]);

    const triggerDiscovery = async (email: string, provider: string) => {
        setIsDiscovering(true);
        try {
            const res = await fetch('/api/brain/onboarding/discover', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, provider })
            });
            if (res.ok) {
                const data = await res.json();
                updateDiscovery(data.discovery);
                // Also update profile if names/details were found
                if (data.profile) {
                    updateProfile(data.profile);
                }
            }
        } catch (e) {
            console.error("Discovery failed", e);
        } finally {
            setIsDiscovering(false);
        }
    };

    if (!isLoaded || !isClerkLoaded) return null;

    const handleNext = () => {
        // Basic validation could go here
        nextStep();
    };

    const handleLaunch = async () => {
        setIsSubmitting(true);
        try {
            // Post all data to backend
            const res = await fetch('/api/brain/onboarding/complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(state)
            });

            if (res.ok) {
                router.push('/dashboard');
            } else {
                console.error("Failed to complete onboarding");
                // Fallback for demo/dev if API not ready
                router.push('/dashboard');
            }
        } catch (e) {
            console.error(e);
            router.push('/dashboard');
        } finally {
            setIsSubmitting(false);
        }
    };

    const renderStepContent = () => {
        switch (state.currentStep) {
            case 0:
                return <CompanyIdentityStep
                    data={state.profile}
                    onUpdate={updateProfile}
                    discovery={state.discovery}
                    isDiscovering={isDiscovering}
                />;
            case 1:
                return <DigitalPresenceStep
                    data={state.digitalPresence}
                    websiteUrl={state.profile.website}
                    onUpdate={updateDigitalPresence}
                />;
            case 2: // New Tools Step
                return <CategorizedToolSelectionStep data={state.tools} onUpdate={updateTools} />;
            case 3:
                return (
                    <AIAssistantIntroStep
                        discovery={state.discovery}
                        agent={state.agent}
                        onUpdate={updateAgent}
                        onNext={nextStep}
                    />
                );
            case 4:
                return <AnalyticsTrackingStep data={state.analytics} onUpdate={updateAnalytics} />;
            case 5:
                return <SocialMediaStep data={state.socialMedia} onUpdate={updateSocialMedia} />;
            case 6:
                return <CampaignGoalsStep data={state.goals} onUpdate={updateGoals} />;
            case 7:
                return <AgentSelectionStep data={state.agent} onUpdate={updateAgent} />;
            case 8:
                return <StrategyApprovalStep data={state} onConfirm={handleLaunch} />;
            default:
                return null;
        }
    };

    const isLastStep = state.currentStep === STEPS.length - 1;

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4 md:p-8 font-sans">

            {/* Header */}
            <div className="w-full max-w-5xl flex justify-between items-center mb-8">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">B</div>
                    <span className="font-bold text-xl text-gray-900 tracking-tight">BizOSaaS</span>
                </div>
                <div className="text-sm text-gray-400 font-medium">
                    Step {state.currentStep + 1} of {STEPS.length}
                </div>
            </div>

            <div className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-12 gap-8">

                {/* Sidebar Navigation */}
                <div className="hidden lg:block lg:col-span-3 space-y-1">
                    {STEPS.map((step, idx) => {
                        const isActive = idx === state.currentStep;
                        const isCompleted = idx < state.currentStep;

                        return (
                            <div
                                key={step.id}
                                className={`flex items-center gap-3 p-3 rounded-lg transition-colors ${isActive ? 'bg-white shadow-sm text-blue-700' :
                                    isCompleted ? 'text-gray-600' : 'text-gray-400'
                                    }`}
                            >
                                <div className={`p-1.5 rounded-md ${isActive ? 'bg-blue-100' :
                                    isCompleted ? 'bg-green-100 text-green-600' : 'bg-transparent'
                                    }`}>
                                    <step.icon size={18} />
                                </div>
                                <span className={`text-sm font-medium ${isActive ? 'font-semibold' : ''}`}>
                                    {step.title}
                                </span>
                            </div>
                        );
                    })}
                </div>

                {/* Main Card */}
                <div className="lg:col-span-9">
                    <Card className="shadow-xl bg-white border-0 overflow-hidden min-h-[500px] flex flex-col">
                        <CardContent className="p-0 flex-1 flex flex-col">

                            {/* Progress Bar (Mobile) */}
                            <div className="lg:hidden h-1.5 bg-gray-100 w-full">
                                <div
                                    className="h-full bg-blue-600 transition-all duration-300"
                                    style={{ width: `${((state.currentStep + 1) / STEPS.length) * 100}%` }}
                                />
                            </div>

                            {/* Step Content */}
                            <div className="flex-1 p-6 md:p-10 flex flex-col justify-center">
                                {renderStepContent()}
                            </div>

                            {/* Footer Actions */}
                            <div className="border-t bg-gray-50/50 p-6 flex justify-between items-center">
                                <Button
                                    variant="ghost"
                                    onClick={prevStep}
                                    disabled={state.currentStep === 0 || isSubmitting}
                                    className="text-gray-500 hover:text-gray-700"
                                >
                                    Back
                                </Button>

                                {isLastStep ? (
                                    <Button
                                        onClick={handleLaunch}
                                        disabled={isSubmitting}
                                        className="bg-green-600 hover:bg-green-700 text-white px-8 py-6 text-lg shadow-lg hover:shadow-xl transition-all w-full md:w-auto"
                                    >
                                        {isSubmitting ? 'Launching...' : 'Approve & Launch 🚀'}
                                    </Button>
                                ) : (
                                    <Button
                                        onClick={handleNext}
                                        className="bg-blue-600 hover:bg-blue-700 text-white px-8 shadow-md hover:shadow-lg transition-all"
                                    >
                                        Continue
                                    </Button>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
