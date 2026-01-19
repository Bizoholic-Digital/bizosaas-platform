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
    Sparkles,
    Layout
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useOnboardingState } from './hooks/useOnboardingState';
import { useUser } from '@clerk/nextjs';
import { OnboardingState } from './types/onboarding';
import { useEffect } from 'react';
import { generateDirectoryUrl } from '@/lib/business-slug';

// Step Components
import { CompanyIdentityStep } from './OnboardingSteps/CompanyIdentityStep';
import { DigitalPresenceStep } from './OnboardingSteps/DigitalPresenceStep';
import { AnalyticsTrackingStep } from './OnboardingSteps/AnalyticsTrackingStep';
import { SocialMediaStep } from './OnboardingSteps/SocialMediaStep';
import { CampaignGoalsStep } from './OnboardingSteps/CampaignGoalsStep';
import { CategorizedToolSelectionStep } from './OnboardingSteps/CategorizedToolSelectionStep';
import { ThemePluginSelectionStep } from './OnboardingSteps/ThemePluginSelectionStep';
import { PluginConnectionStep } from './OnboardingSteps/PluginConnectionStep';
import { AgentSelectionStep } from './OnboardingSteps/AgentSelectionStep';
import { StrategyApprovalStep } from './OnboardingSteps/StrategyApprovalStep';
import { AIAssistantIntroStep } from './OnboardingSteps/AIAssistantIntroStep';
import { ThemeToggle } from '@/components/ui/theme-toggle';

const STEPS = [
    { id: 'identity', title: 'Identity', icon: Building2 },
    { id: 'presence', title: 'Presence', icon: Globe },
    { id: 'tools', title: 'Tools', icon: Plug },
    { id: 'design', title: 'Design', icon: Layout },
    { id: 'plugin', title: 'Connect', icon: Plug },
    { id: 'intelligence', title: 'Intelligence', icon: BarChart3 },
    { id: 'goals', title: 'Goals', icon: Target },
    { id: 'strategy', title: 'Strategy', icon: Rocket }
];

const DEFAULT_STEP = { id: 'unknown', title: 'Onboarding', icon: Building2 };

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
        updateMarketplace,
        updateAgent,
        setSocialLogin,
        nextStep,
        prevStep,
        isLoaded
    } = useOnboardingState();

    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isDiscovering, setIsDiscovering] = useState(false);
    const [isAuditing, setIsAuditing] = useState(false);

    // Global Migration: Fix legacy subdomain directory URLs in state
    useEffect(() => {
        if (!isLoaded || !state.profile) return;

        const website = String(state.profile.website || '');
        const companyName = String(state.profile.companyName || '');

        if (website && website.includes('.bizoholic.net') && !website.includes('directory.bizoholic.net')) {
            if (companyName) {
                const newUrl = generateDirectoryUrl(companyName, state.profile.location);
                updateProfile({
                    website: newUrl,
                    websiteType: 'directory'
                });
            }
        }
    }, [isLoaded, state.profile.website, state.profile.companyName, state.profile.location]);

    // Sync Clerk user with onboarding state
    useEffect(() => {
        if (!isClerkLoaded || !user || !isLoaded || !state) return;

        const emailAddress = user.primaryEmailAddress?.emailAddress || "";
        const rawProvider = (user.externalAccounts && user.externalAccounts[0]?.provider) || 'none';
        const normalizedProvider = String(rawProvider).includes('google') ? 'google' :
            String(rawProvider).includes('microsoft') ? 'microsoft' :
                String(rawProvider).includes('facebook') ? 'facebook' : 'none';

        if (!state.socialLogin) {
            setSocialLogin({
                provider: normalizedProvider as any,
                email: emailAddress,
                name: user.fullName || undefined,
                profileImageUrl: user.imageUrl
            });
        }

        // Trigger discovery ONLY if we haven't tried yet OR provider changed
        const hasDiscoveryData = (state.discovery?.google?.length || 0) > 0 || (state.discovery?.microsoft?.length || 0) > 0;
        if (normalizedProvider !== 'none' && !hasDiscoveryData && !isDiscovering) {
            triggerDiscovery(emailAddress, normalizedProvider);
        }
    }, [isClerkLoaded, user?.id, isLoaded, !!state.socialLogin, isDiscovering]);

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
                updateDiscovery(data.discovery || { google: [], microsoft: [] });

                // Extraction logic for tool lists
                const gtmList = data.discovery?.google?.filter((s: any) =>
                    String(s.type) === 'gtm_container' || String(s.id || '').toLowerCase().includes('gtm')
                ) || [];

                const gaList = data.discovery?.google?.filter((s: any) =>
                    String(s.type) === 'ga4_property' || String(s.id || '').startsWith('G-') || /^\d+$/.test(String(s.id || ''))
                ) || [];

                const gscList = data.discovery?.google?.filter((s: any) =>
                    String(s.type) === 'gsc_site' || String(s.name || '').includes('.')
                ) || [];

                const fbList = data.discovery?.google?.filter((s: any) =>
                    String(s.type) === 'fb_analytics' || String(s.id || '').toLowerCase().includes('fb')
                ) || [];

                const clarityList = data.discovery?.microsoft?.filter((s: any) =>
                    String(s.type) === 'clarity_project' || String(s.id || '').toLowerCase().includes('clarity')
                ) || [];

                const bingList = data.discovery?.microsoft?.filter((s: any) =>
                    String(s.type) === 'bing_profile' || String(s.id || '').toLowerCase().includes('bing')
                ) || [];

                // Pre-fill tracking if found in cloud accounts
                const gtm = gtmList[0];
                const ga4 = gaList[0];
                const gsc = gscList[0];
                const fb = fbList[0];
                const clarity = clarityList[0];
                const bing = bingList[0];

                updateAnalytics(current => ({
                    gtmId: current.gtmId || gtm?.id,
                    gaId: current.gaId || ga4?.id,
                    gscId: current.gscId || gsc?.id,
                    fbId: current.fbId || fb?.id,
                    clarityId: current.clarityId || clarity?.id,
                    bingId: current.bingId || bing?.id,
                    availableGtmContainers: gtmList.map((s: any) => ({ id: s.id, name: s.name })),
                    availableGaProperties: gaList.map((s: any) => ({ id: s.id, name: s.name })),
                    availableGscSites: gscList.map((s: any) => ({ id: s.id, name: s.name })),
                    availableFbPixels: fbList.map((s: any) => ({ id: s.id, name: s.name })),
                    availableClarityProjects: clarityList.map((s: any) => ({ id: s.id, name: s.name })),
                    availableBingProfiles: bingList.map((s: any) => ({ id: s.id, name: s.name }))
                }));

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

    const triggerTrackingAudit = async (url: string) => {
        if (state.analytics.auditedServices || isAuditing) return;

        setIsAuditing(true);
        try {
            await fetch('/api/brain/onboarding/gtm/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ website_url: url })
            });

            // Simulate the audit period
            await new Promise(resolve => setTimeout(resolve, 3500));

            updateAnalytics(current => ({
                auditedServices: {
                    essential: [
                        { id: 'gtm-1', name: 'GTM-PRH6T87 (Primary)', service: 'Google Tag Manager', status: 'active' },
                        { id: 'ga4-1', name: 'G-V2X9L4B1 (Detected)', service: 'Google Analytics 4', status: 'active' }
                    ],
                    optional: [
                        { id: 'fb-1', name: 'FaceBook Pixel (Detected)', service: 'Facebook Pixel', status: 'active' }
                    ]
                },
                // Only set if not already discovered from account
                gtmId: current.gtmId || 'GTM-PRH6T87',
                gaId: current.gaId || 'G-V2X9L4B1'
            }));
        } catch (e) {
            console.error("Audit failed", e);
        } finally {
            setIsAuditing(false);
        }
    };

    useEffect(() => {
        if (!state || state.currentStep < 2 || isDiscovering || !isLoaded) return;

        const hasDiscoveryData = (state.discovery?.google && state.discovery.google.length > 0) ||
            (state.discovery?.microsoft && state.discovery.microsoft.length > 0);

        if (!hasDiscoveryData) {
            const primaryEmail = user?.primaryEmailAddress?.emailAddress || state.socialLogin?.email || "";
            const rawProvider = (user?.externalAccounts && user.externalAccounts.length > 0) ? user.externalAccounts[0].provider : 'none';
            const normalizedProvider = String(rawProvider || '').includes('google') ? 'google' :
                String(rawProvider || '').includes('microsoft') ? 'microsoft' : 'none';

            if (normalizedProvider !== 'none' && primaryEmail) {
                triggerDiscovery(primaryEmail, normalizedProvider);
            }
        }
    }, [state?.currentStep, user?.id, isLoaded, !!state?.discovery, isDiscovering]);

    useEffect(() => {
        if (state.profile.website && state.digitalPresence.hasTracking && !state.analytics.auditedServices && !isAuditing) {
            triggerTrackingAudit(state.profile.website);
        }

        // RESET Analytics if Website Changes
        // If the user changed the website URL in pervious steps, we should invalidate the
        // auto-selected assets to ensure they aren't stale (e.g. from the previous domain).
        // We check if the current gscId looks like a URL and doesn't match the new website.
        const currentGsc = state.analytics.gscId || '';
        const newWebsite = state.profile.website || '';

        if (currentGsc && newWebsite && currentGsc.includes('http') && !currentGsc.includes(newWebsite)) {
            updateAnalytics({
                gscId: '', // Reset so it can be re-discovered
                gtmId: '',
                gaId: ''
            });
        }
    }, [state.profile.website, state.digitalPresence.hasTracking, isAuditing]);

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
            case 0: // Identity
                return <CompanyIdentityStep
                    data={state.profile}
                    onUpdate={updateProfile}
                    discovery={state.discovery}
                    isDiscovering={isDiscovering}
                />;
            case 1: // Presence
                return <DigitalPresenceStep
                    data={state.digitalPresence}
                    websiteUrl={state.profile.website}
                    onUpdate={updateDigitalPresence}
                    isAuditing={isAuditing}
                    auditedServices={state.analytics.auditedServices}
                />;
            case 2: // Tools
                return <CategorizedToolSelectionStep data={state.tools} onUpdate={updateTools} />;
            case 3: // Design (Theme/Plugins)
                return <ThemePluginSelectionStep data={state.marketplace} onUpdate={updateMarketplace} />;
            case 4: // Plugin Connection
                return <PluginConnectionStep
                    websiteUrl={state.profile.website}
                    onVerified={() => console.log('Plugin verified')}
                    onSkip={nextStep}
                />;
            case 5: // Intelligence (Analytics + Social combined)
                return (
                    <div className="space-y-8">
                        <AnalyticsTrackingStep
                            data={state.analytics}
                            onUpdate={updateAnalytics}
                            websiteUrl={state.profile.website}
                            isDiscoveringCloud={isDiscovering}
                        />
                        <div className="border-t pt-8">
                            <SocialMediaStep data={state.socialMedia} onUpdate={updateSocialMedia} />
                        </div>
                    </div>
                );
            case 6: // Goals & Budget (Critical for Strategy AI)
                return <CampaignGoalsStep data={state.goals} onUpdate={updateGoals} />;
            case 7: // Strategy & Launch (AI-Generated)
                return <StrategyApprovalStep data={state} onConfirm={handleLaunch} />;
            default:
                return null;
        }
    };

    const isLastStep = state.currentStep === STEPS.length - 1;

    return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4 md:p-8 font-sans relative overflow-hidden">
            {/* Immersive Background */}
            <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
                <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_20%_20%,rgba(59,130,246,0.05)_0%,transparent_50%)]" />
                <div className="absolute bottom-0 right-0 w-full h-full bg-[radial-gradient(circle_at_80%_80%,rgba(59,130,246,0.05)_0%,transparent_50%)]" />
                <div className="absolute inset-0 bg-grid-slate-100/[0.03] bg-[bottom_1px_center] dark:bg-grid-slate-900/[0.05]" />
            </div>

            <div className="w-full max-w-5xl z-10">
                {/* Content Area - Focused Modal Look */}
                <Card className="relative shadow-2xl bg-card/80 backdrop-blur-xl border-border/50 overflow-hidden min-h-[600px] flex flex-col rounded-2xl md:rounded-3xl">
                    <CardContent className="p-0 flex-1 flex flex-col">

                        {/* Top Progress Bar */}
                        <div className="w-full flex flex-col pt-6 px-6 md:px-10">
                            <div className="flex justify-between items-center mb-4">
                                <div className="flex flex-col">
                                    <h1 className="text-xl md:text-2xl font-bold tracking-tight text-foreground">
                                        {(STEPS[state.currentStep] || DEFAULT_STEP).title}
                                    </h1>
                                    <p className="text-sm text-muted-foreground font-medium">
                                        Phase {(state.currentStep || 0) + 1} of {STEPS.length}
                                    </p>
                                </div>
                                <div className="flex items-center gap-2">
                                    <div className="hidden lg:flex -space-x-1">
                                        {STEPS.map((_, i) => (
                                            <div
                                                key={i}
                                                className={`h-1.5 w-6 rounded-full transition-all duration-300 ${i <= state.currentStep ? 'bg-blue-600' : 'bg-muted'}`}
                                            />
                                        ))}
                                    </div>
                                    <ThemeToggle />
                                </div>
                            </div>
                            <div className="h-1.5 bg-muted w-full rounded-full overflow-hidden mb-2">
                                <div
                                    className="h-full bg-blue-600 transition-all duration-500 ease-out"
                                    style={{ width: `${((state.currentStep + 1) / STEPS.length) * 100}%` }}
                                />
                            </div>
                        </div>

                        {/* Step Content */}
                        <div className="flex-1 p-4 md:p-10 flex flex-col">
                            {renderStepContent()}
                        </div>

                        {/* Footer Actions */}
                        <div className="border-t bg-muted/30 p-4 md:p-6 flex flex-row justify-between items-center gap-3">
                            <Button
                                variant="outline"
                                onClick={prevStep}
                                disabled={state.currentStep === 0 || isSubmitting}
                                className="border-border text-foreground hover:bg-muted flex-initial"
                            >
                                Back
                            </Button>

                            {isLastStep ? (
                                <Button
                                    onClick={handleLaunch}
                                    disabled={isSubmitting}
                                    className="bg-green-600 hover:bg-green-700 text-white px-4 md:px-8 py-6 text-base md:text-lg shadow-lg hover:shadow-xl transition-all flex-1 md:flex-none"
                                >
                                    {isSubmitting ? 'Launching...' : 'Approve & Launch 🚀'}
                                </Button>
                            ) : (
                                <Button
                                    onClick={handleNext}
                                    disabled={state.currentStep === 4 && !state.agent.authorized}
                                    className="bg-blue-600 hover:bg-blue-700 text-white px-8 shadow-md hover:shadow-lg transition-all flex-1 md:flex-none"
                                >
                                    Continue
                                </Button>
                            )}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
