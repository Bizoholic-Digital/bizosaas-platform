'use client';

import React, { useState, useCallback, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import {
    Building2, Globe, BarChart3, Plug, Rocket, Target, Layout, Sparkles, AlertTriangle
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

    const triggerTrackingAudit = useCallback(async (url: string, force = false) => {
        if (!force && (state.analytics.auditedServices || isAuditing || auditAttempted.current)) return;

        if (force) {
            // Reset for force rerun
            auditAttempted.current = true;
        } else {
            auditAttempted.current = true;
        }

        setIsAuditing(true);
        try {
            const res = await fetch('/api/brain/onboarding/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ website_url: url })
            });
            const data = await res.json();

            if (data.status === 'success' && data.scanned_tags) {
                const tags = data.scanned_tags;
                const plugins = tags.plugins || [];
                const essential: any[] = [];
                const optional: any[] = [];

                // GTMs
                tags.gtm.forEach((id: string, i: number) => {
                    essential.push({ id: `gtm-${i}`, name: id, service: 'GTM', status: 'active' });
                });
                // GA4s
                tags.ga4.forEach((id: string, i: number) => {
                    essential.push({ id: `ga4-${i}`, name: id, service: 'GA4', status: 'active' });
                });
                // UA
                tags.ua.forEach((id: string, i: number) => {
                    optional.push({ id: `ua-${i}`, name: id, service: 'UA', status: 'detected' });
                });
                // Meta
                tags.meta.forEach((id: string, i: number) => {
                    optional.push({ id: `meta-${i}`, name: id, service: 'Meta', status: 'detected' });
                });
                // Clarity
                tags.clarity.forEach((id: string, i: number) => {
                    optional.push({ id: `clarity-${i}`, name: id, service: 'Clarity', status: 'detected' });
                });

                // Auto-detect platforms based on the website audit
                // If any WP plugin is detected, ensure cms is wordpress
                const hasWpPlugins = plugins.length > 0;
                const detectedCms = tags.cms !== 'none' ? tags.cms : (hasWpPlugins ? 'wordpress' : state.digitalPresence.cmsType);

                // Add CMS/Platform to essentials for top-level visibility
                if (detectedCms && detectedCms !== 'none') {
                    if (!essential.some(s => s.id === `cms-${detectedCms}`)) {
                        essential.push({ id: `cms-${detectedCms}`, name: detectedCms, service: detectedCms.toUpperCase(), status: 'active' });
                    }
                }

                // Add ALL detected plugins to essentials for maximum visibility
                plugins.forEach((p: any) => {
                    const slug = p.slug?.toLowerCase();
                    // Map Fluent Forms or FluentCRM to the foundation if found
                    const isCore = ['woocommerce', 'fluent-crm', 'fluentcrm', 'fluentform', 'elementor', 'elementor-pro', 'astra-pro', 'bizosaas-connect', 'google-site-kit'].includes(slug);
                    if (isCore) {
                        if (!essential.some(s => s.id === `p-${slug}`)) {
                            essential.push({ id: `p-${slug}`, name: p.name, service: p.name, status: 'active' });
                        }
                    } else {
                        optional.push({ id: `p-${slug}`, name: p.name, service: p.name, status: 'detected' });
                    }
                });

                updateAnalytics({
                    gtmId: tags.gtm[0] || state.analytics.gtmId,
                    gaId: tags.ga4[0] || state.analytics.gaId,
                    fbId: tags.meta[0] || state.analytics.fbId,
                    clarityId: tags.clarity[0] || state.analytics.clarityId,
                    auditedServices: { essential, optional }
                });

                updateDigitalPresence({
                    cmsType: detectedCms,
                    crmType: plugins.some((p: any) => ['fluent-crm', 'fluentcrm', 'fluentform', 'fluentformpro'].includes(p.slug?.toLowerCase())) ? 'fluentcrm' : state.digitalPresence.crmType,
                    ecommerceType: plugins.some((p: any) => p.slug?.toLowerCase() === 'woocommerce') ? 'woocommerce' : state.digitalPresence.ecommerceType,
                    isBizOSaaSActive: !!tags.is_bridge_active || plugins.some((p: any) => p.slug?.toLowerCase() === 'bizosaas-connect'),
                    hasTracking: true
                });
            }
        } catch (e) {
            console.error("Audit failed", e);
        } finally {
            setIsAuditing(false);
        }
    }, [state.analytics.auditedServices, state.analytics.gtmId, state.analytics.gaId, state.analytics.fbId, state.analytics.clarityId, state.digitalPresence.cmsType, state.digitalPresence.crmType, state.digitalPresence.ecommerceType, isAuditing, updateAnalytics, updateDigitalPresence]);

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
        // Trigger if we are on step 1 (Presence) and have a website URL
        const isPresenceStep = state.currentStep === 1;
        const hasWebsite = !!state.profile.website;
        const notAudited = !state.analytics.auditedServices;

        if (isPresenceStep && hasWebsite && notAudited && !isAuditing && !auditAttempted.current) {
            // Auto-enable tracking switch to show the scanning UI
            if (!state.digitalPresence.hasTracking) {
                updateDigitalPresence({ hasTracking: true });
            }
            triggerTrackingAudit(state.profile.website);
        }
    }, [state.currentStep, state.profile.website, state.digitalPresence.hasTracking, isAuditing, triggerTrackingAudit, updateDigitalPresence]);

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

        // 3. Detect from E-commerce
        if (state.digitalPresence.ecommerceType === 'woocommerce' && !newSelectedMcps.has('woocommerce')) {
            newSelectedMcps.add('woocommerce');
            changed = true;
        }

        // 3. Detect from Tracking Audit (GTM, GA4)
        if (state.analytics.auditedServices) {
            const allServices = [...(state.analytics.auditedServices.essential || []), ...(state.analytics.auditedServices.optional || [])];

            if (allServices.some(s => s.service?.toUpperCase() === 'GTM') && !newSelectedMcps.has('google-tag-manager')) {
                newSelectedMcps.add('google-tag-manager');
                changed = true;
            }
            if (allServices.some(s => ['GA4', 'GA', 'GOOGLE ANALYTICS'].includes(s.service?.toUpperCase())) && !newSelectedMcps.has('google-analytics-4')) {
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
            case 1: return <DigitalPresenceStep data={state.digitalPresence} websiteUrl={state.profile.website} onUpdate={updateDigitalPresence} isAuditing={isAuditing} auditedServices={state.analytics.auditedServices} onRerunAudit={() => triggerTrackingAudit(state.profile.website || '', true)} />;
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
        <div className="min-h-[100dvh] bg-background flex flex-col items-center justify-center p-0 md:p-8 relative overflow-x-hidden">
            {/* Context-Aware Theme Toggle (Global Position) */}
            <div className="absolute top-4 right-4 md:top-8 md:right-8 z-50">
                <ThemeToggle />
            </div>

            <div className="fixed inset-0 -z-10 bg-[radial-gradient(circle_at_20%_20%,rgba(59,130,246,0.05)_0%,transparent_50%)]" />

            <div className="w-full md:max-w-5xl z-10 flex flex-col items-center">
                <Card className="w-full shadow-2xl bg-card/80 backdrop-blur-xl border-border/50 overflow-hidden min-h-[600px] md:min-h-[650px] flex flex-col rounded-none md:rounded-3xl border-0 md:border">
                    <CardContent className="p-0 flex-1 flex flex-col">
                        <div className="w-full flex flex-col pt-8 md:pt-10 px-6 md:px-12">
                            <div className="flex justify-between items-end mb-6">
                                <div className="flex flex-col">
                                    <h1 className="text-2xl md:text-4xl font-black uppercase tracking-tight text-foreground leading-none">
                                        {(STEPS[state.currentStep] || DEFAULT_STEP).title}
                                    </h1>
                                    <p className="text-xs md:text-sm text-muted-foreground font-bold uppercase tracking-widest mt-2">
                                        Phase {(state.currentStep || 0) + 1} <span className="mx-1 text-muted-foreground/30">/</span> {STEPS.length}
                                    </p>
                                </div>
                                <div className="hidden md:flex items-center gap-2 mb-1">
                                    <div className="flex -space-x-1">
                                        {STEPS.map((_, i) => (
                                            <div key={i} className={`h-1.5 w-8 rounded-full transition-all duration-500 ${i <= state.currentStep ? 'bg-blue-600 shadow-[0_0_10px_rgba(37,99,235,0.4)]' : 'bg-muted'}`} />
                                        ))}
                                    </div>
                                </div>
                            </div>
                            <div className="h-1 bg-muted w-full rounded-full overflow-hidden mb-2">
                                <div className="h-full bg-blue-600 transition-all duration-700 ease-in-out" style={{ width: `${((state.currentStep + 1) / STEPS.length) * 100}%` }} />
                            </div>
                        </div>
                        <div className="flex-1 p-4 md:p-10 flex flex-col">{renderStepContent()}</div>
                        <div className="border-t bg-muted/10 p-6 md:p-10 flex flex-col sm:flex-row justify-between items-center gap-6">
                            <div className="flex items-center gap-2">
                                {state.currentStep === 0 ? (
                                    <Button
                                        variant="ghost"
                                        onClick={resetOnboarding}
                                        className="text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-950/30"
                                    >
                                        <Sparkles className="w-4 h-4 mr-2" />
                                        Reset Form
                                    </Button>
                                ) : (
                                    <Button variant="outline" onClick={prevStep} disabled={isSubmitting}>Back</Button>
                                )}
                            </div>
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
