'use client';

import React, { useState, useCallback, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import {
    Building2, Globe, BarChart3, Plug, Rocket, Target, Layout
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useOnboardingState } from './hooks/useOnboardingState';
import { useAuth } from '../auth/AuthProvider';

// Step Components
import { CompanyIdentityStep } from './OnboardingSteps/CompanyIdentityStep';
import { DigitalPresenceStep } from './OnboardingSteps/DigitalPresenceStep';
import { AnalyticsTrackingStep } from './OnboardingSteps/AnalyticsTrackingStep';
import { SocialMediaStep } from './OnboardingSteps/SocialMediaStep';
import { CampaignGoalsStep } from './OnboardingSteps/CampaignGoalsStep';
import { CategorizedToolSelectionStep } from './OnboardingSteps/CategorizedToolSelectionStep';
import { ThemePluginSelectionStep } from './OnboardingSteps/ThemePluginSelectionStep';
import { PluginConnectionStep } from './OnboardingSteps/PluginConnectionStep';
import { StrategyApprovalStep } from './OnboardingSteps/StrategyApprovalStep';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle
} from '@/components/ui/dialog';
import { AlertTriangle } from 'lucide-react';

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
    const { user, isLoading: isAuthLoading } = useAuth();
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
        setSocialLogin,
        nextStep,
        prevStep,
        resetOnboarding,
        isLoaded
    } = useOnboardingState();

    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isDiscovering, setIsDiscovering] = useState(false);
    const [isAuditing, setIsAuditing] = useState(false);
    const [showToolConfirm, setShowToolConfirm] = useState(false);
    const [autoSelectedMcps, setAutoSelectedMcps] = useState<string[]>([]);

    // Safety flags to prevent infinite loops if API returns empty results
    const discoveryAttempted = useRef(false);
    const auditAttempted = useRef(false);

    // User Syncing re-enabled
    useEffect(() => {
        if (isAuthLoading || !user || !isLoaded || !state) return;
        if (!state.socialLogin) {
            setSocialLogin({
                provider: 'none',
                email: user.email || "",
                name: user.name || undefined,
                profileImageUrl: user.image || ''
            });
        }
    }, [isAuthLoading, user?.id, isLoaded, !!state?.socialLogin, setSocialLogin]);

    const triggerDiscovery = useCallback(async (email: string, provider: string) => {
        if (isDiscovering || discoveryAttempted.current) return;
        discoveryAttempted.current = true;
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

                // Only set if not already present
                const gtmList = data.discovery?.google?.filter((s: any) =>
                    String(s.type) === 'gtm_container' || String(s.id || '').toLowerCase().includes('gtm')
                ) || [];
                const gaList = data.discovery?.google?.filter((s: any) =>
                    String(s.type) === 'ga4_property' || String(s.id || '').startsWith('G-')
                ) || [];

                updateAnalytics(current => ({
                    gtmId: current.gtmId || gtmList[0]?.id,
                    gaId: current.gaId || gaList[0]?.id,
                }));

                if (data.profile) updateProfile(data.profile);
            }
        } catch (e) {
            console.error("Discovery failed", e);
        } finally {
            setIsDiscovering(false);
        }
    }, [isDiscovering, updateDiscovery, updateAnalytics, updateProfile]);

    const triggerTrackingAudit = useCallback(async (url: string) => {
        if (state.analytics.auditedServices || isAuditing || auditAttempted.current) return;
        auditAttempted.current = true;
        setIsAuditing(true);
        try {
            await fetch('/api/brain/onboarding/gtm/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ website_url: url })
            });
            await new Promise(resolve => setTimeout(resolve, 2000));
            updateAnalytics({
                auditedServices: {
                    essential: [
                        { id: 'gtm-1', name: 'GTM-PRH6T87', service: 'GTM', status: 'active' },
                        { id: 'ga-1', name: 'G-XXXXXXXXXX', service: 'GA4', status: 'active' }
                    ],
                    optional: []
                }
            });
            // Auto-detect platforms based on the website audit
            updateDigitalPresence({
                cmsType: 'wordpress',
                crmType: 'fluentcrm',
                hasTracking: true
            });
        } catch (e) {
            console.error("Audit failed", e);
        } finally {
            setIsAuditing(false);
        }
    }, [state.analytics.auditedServices, isAuditing, updateAnalytics]);

    // Auto-Discovery Trigger
    useEffect(() => {
        if (!state || state.currentStep < 2 || isDiscovering || !isLoaded || discoveryAttempted.current) return;
        const hasDiscoveryData = (state.discovery?.google?.length || 0) > 0;
        if (!hasDiscoveryData && user?.email) {
            triggerDiscovery(user.email, 'none');
        }
    }, [state?.currentStep, user?.id, isLoaded, isDiscovering, triggerDiscovery]);

    // Handle Auto-Audit Trigger
    useEffect(() => {
        if (state.profile.website && state.digitalPresence.hasTracking && !state.analytics.auditedServices && !isAuditing && !auditAttempted.current) {
            triggerTrackingAudit(state.profile.website);
        }
    }, [state.profile.website, state.digitalPresence.hasTracking, isAuditing, triggerTrackingAudit]);

    // AUTO-SELECTION LOGIC: Map detected services to MCP slugs
    useEffect(() => {
        if (!isLoaded || !state) return;

        const newSelectedMcps = new Set(state.tools.selectedMcps || []);
        let changed = false;

        // 1. Detect from CMS
        if (state.digitalPresence.cmsType === 'wordpress' && !newSelectedMcps.has('wordpress')) {
            newSelectedMcps.add('wordpress');
            changed = true;
        } else if (state.digitalPresence.cmsType === 'shopify' && !newSelectedMcps.has('shopify')) {
            newSelectedMcps.add('shopify');
            changed = true;
        }

        // 2. Detect from CRM
        if (state.digitalPresence.crmType === 'fluentcrm' && !newSelectedMcps.has('fluentcrm')) {
            newSelectedMcps.add('fluentcrm');
            changed = true;
        } else if (state.digitalPresence.crmType === 'hubspot' && !newSelectedMcps.has('hubspot')) {
            newSelectedMcps.add('hubspot');
            changed = true;
        }

        // 3. Detect from Tracking Audit (GTM, GA4)
        if (state.analytics.auditedServices) {
            const allServices = [...state.analytics.auditedServices.essential, ...state.analytics.auditedServices.optional];

            if (allServices.some(s => s.service === 'GTM') && !newSelectedMcps.has('google-tag-manager')) {
                newSelectedMcps.add('google-tag-manager');
                changed = true;
            }
            if (allServices.some(s => s.service === 'GA4' || s.service === 'GA') && !newSelectedMcps.has('google-analytics-4')) {
                newSelectedMcps.add('google-analytics-4');
                changed = true;
            }
        }

        // 4. Default Business Tools (e.g. Plane.so for Project Management)
        if (!newSelectedMcps.has('plane')) {
            newSelectedMcps.add('plane');
            changed = true;
        }

        if (changed) {
            updateTools({ selectedMcps: Array.from(newSelectedMcps) });
            // Track what we auto-selected to detect manual changes later
            if (autoSelectedMcps.length === 0) {
                setAutoSelectedMcps(Array.from(newSelectedMcps));
            }
        }
    }, [
        state?.digitalPresence.cmsType,
        state?.digitalPresence.crmType,
        state?.analytics.auditedServices,
        isLoaded
    ]);

    if (!isLoaded || isAuthLoading) return null;

    const handleLaunch = async () => {
        setIsSubmitting(true);
        try {
            const res = await fetch('/api/brain/onboarding/complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(state)
            });
            window.location.href = '/dashboard';
        } catch (e) {
            window.location.href = '/dashboard';
        } finally {
            setIsSubmitting(false);
        }
    };

    const renderStepContent = () => {
        switch (state.currentStep) {
            case 0: return <CompanyIdentityStep data={state.profile} onUpdate={updateProfile} onReset={resetOnboarding} discovery={state.discovery} isDiscovering={isDiscovering} />;
            case 1: return <DigitalPresenceStep data={state.digitalPresence} websiteUrl={state.profile.website} onUpdate={updateDigitalPresence} isAuditing={isAuditing} auditedServices={state.analytics.auditedServices} />;
            case 2: return <CategorizedToolSelectionStep data={state.tools} onUpdate={updateTools} state={state} />;
            case 3: return <ThemePluginSelectionStep data={state.marketplace} onUpdate={updateMarketplace} />;
            case 4: return <PluginConnectionStep websiteUrl={state.profile.website} onVerified={() => nextStep()} onSkip={nextStep} />;
            case 5: return (
                <div className="space-y-8">
                    <AnalyticsTrackingStep data={state.analytics} onUpdate={updateAnalytics} websiteUrl={state.profile.website} isDiscoveringCloud={isDiscovering} />
                    <div className="border-t pt-8"><SocialMediaStep data={state.socialMedia} onUpdate={updateSocialMedia} /></div>
                </div>
            );
            case 6: return <CampaignGoalsStep data={state.goals} onUpdate={updateGoals} />;
            case 7: return <StrategyApprovalStep data={state} onConfirm={handleLaunch} />;
            default: return null;
        }
    };

    const isLastStep = state.currentStep === STEPS.length - 1;

    return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4 md:p-8 font-sans relative overflow-hidden">
            <div className="fixed inset-0 -z-10 bg-[radial-gradient(circle_at_20%_20%,rgba(59,130,246,0.05)_0%,transparent_50%)]" />
            <div className="w-full max-w-5xl z-10">
                <Card className="relative shadow-2xl bg-card/80 backdrop-blur-xl border-border/50 overflow-hidden min-h-[600px] flex flex-col rounded-2xl md:rounded-3xl">
                    <CardContent className="p-0 flex-1 flex flex-col">
                        <div className="w-full flex flex-col pt-6 px-6 md:px-10">
                            <div className="flex justify-between items-center mb-4">
                                <div className="flex flex-col">
                                    <h1 className="text-xl md:text-2xl font-bold tracking-tight text-foreground">{(STEPS[state.currentStep] || DEFAULT_STEP).title}</h1>
                                    <p className="text-sm text-muted-foreground font-medium">Phase {(state.currentStep || 0) + 1} of {STEPS.length}</p>
                                </div>
                                <div className="flex items-center gap-2">
                                    <div className="hidden lg:flex -space-x-1">
                                        {STEPS.map((_, i) => (
                                            <div key={i} className={`h-1.5 w-6 rounded-full transition-all duration-300 ${i <= state.currentStep ? 'bg-blue-600' : 'bg-muted'}`} />
                                        ))}
                                    </div>
                                    <ThemeToggle />
                                </div>
                            </div>
                            <div className="h-1.5 bg-muted w-full rounded-full overflow-hidden mb-2">
                                <div className="h-full bg-blue-600 transition-all duration-500 ease-out" style={{ width: `${((state.currentStep + 1) / STEPS.length) * 100}%` }} />
                            </div>
                        </div>
                        <div className="flex-1 p-4 md:p-10 flex flex-col">{renderStepContent()}</div>
                        <div className="border-t bg-muted/30 p-4 md:p-6 flex flex-row justify-between items-center gap-3">
                            <Button variant="outline" onClick={prevStep} disabled={state.currentStep === 0 || isSubmitting}>Back</Button>
                            {isLastStep ? (
                                <Button onClick={handleLaunch} disabled={isSubmitting} className="bg-green-600 hover:bg-green-700 text-white px-8 py-6 text-lg shadow-lg">
                                    {isSubmitting ? 'Launching...' : 'Approve & Launch 🚀'}
                                </Button>
                            ) : (
                                <Button
                                    onClick={() => {
                                        // Specific confirmation for Tool Selection step (Step 2)
                                        if (state.currentStep === 2) {
                                            const current = JSON.stringify([...(state.tools.selectedMcps || [])].sort());
                                            const original = JSON.stringify([...autoSelectedMcps].sort());
                                            if (current !== original) {
                                                setShowToolConfirm(true);
                                                return;
                                            }
                                        }
                                        nextStep();
                                    }}
                                    disabled={state.currentStep === 4 && !state.agent.authorized}
                                    className="bg-blue-600 hover:bg-blue-700 text-white px-8 shadow-md"
                                >
                                    Continue
                                </Button>
                            )}
                        </div>

                        {/* Selection Confirmation Dialog */}
                        <Dialog open={showToolConfirm} onOpenChange={setShowToolConfirm}>
                            <DialogContent className="max-w-md">
                                <DialogHeader>
                                    <DialogTitle className="flex items-center gap-2 uppercase font-black text-xl tracking-tighter">
                                        <AlertTriangle className="text-amber-500" /> Confirm Stack Selection
                                    </DialogTitle>
                                    <DialogDescription className="text-base font-medium">
                                        You have modified the recommended tech stack for your business. Are you sure you want to proceed with these changes?
                                    </DialogDescription>
                                </DialogHeader>
                                <div className="py-4 space-y-3">
                                    <div className="p-4 bg-muted/50 rounded-2xl border border-dashed text-sm">
                                        <p className="font-bold mb-2">Summary of changes:</p>
                                        <ul className="space-y-1 text-xs">
                                            {state.tools.selectedMcps?.filter(s => !autoSelectedMcps.includes(s)).map(s => (
                                                <li key={s} className="text-green-600 font-bold">+ Added {s}</li>
                                            ))}
                                            {autoSelectedMcps.filter(s => !state.tools.selectedMcps?.includes(s)).map(s => (
                                                <li key={s} className="text-red-500 font-bold">- Removed {s}</li>
                                            ))}
                                        </ul>
                                    </div>
                                </div>
                                <DialogFooter className="gap-2 sm:gap-0">
                                    <Button variant="ghost" onClick={() => setShowToolConfirm(false)} className="font-bold">Review Changes</Button>
                                    <Button onClick={() => { setShowToolConfirm(false); nextStep(); }} className="bg-blue-600 hover:bg-blue-700 font-bold">Confirm & Continue</Button>
                                </DialogFooter>
                            </DialogContent>
                        </Dialog>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
