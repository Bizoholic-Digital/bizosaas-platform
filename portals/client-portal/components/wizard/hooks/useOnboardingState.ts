import React, { useState, useEffect, useCallback } from 'react';
import { OnboardingState, INITIAL_STATE } from '../types/onboarding';
import { generateDirectoryUrl } from '@/lib/business-slug';

const STORAGE_KEY = 'bizosaas_onboarding_v2'; // Changed from v1 to force a clean break
const STATE_VERSION = 'v1.3-multi-detection'; // Increment this to force reset stale data

export function useOnboardingState() {
    const [state, setState] = useState<OnboardingState>(INITIAL_STATE);
    const [isLoaded, setIsLoaded] = useState(false);

    // Load from localStorage on mount
    useEffect(() => {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            if (saved) {
                const parsed = JSON.parse(saved);

                // 1. CRITICAL: Reset state if version mismatch
                if (!parsed || parsed.version !== STATE_VERSION) {
                    console.warn('[Onboarding] State version mismatch. Resetting...');
                    localStorage.removeItem(STORAGE_KEY);
                    setState(INITIAL_STATE);
                    setIsLoaded(true);
                    return;
                }

                // 2. Safe merge with validation
                if (parsed && typeof parsed === 'object') {
                    setState(prev => {
                        let merged = {
                            ...prev,
                            ...parsed,
                            profile: { ...prev.profile, ...(parsed.profile && typeof parsed.profile === 'object' ? parsed.profile : {}) },
                            digitalPresence: { ...prev.digitalPresence, ...(parsed.digitalPresence && typeof parsed.digitalPresence === 'object' ? parsed.digitalPresence : {}) },
                            analytics: { ...prev.analytics, ...(parsed.analytics && typeof parsed.analytics === 'object' ? parsed.analytics : {}) },
                            marketplace: { ...prev.marketplace, ...(parsed.marketplace && typeof parsed.marketplace === 'object' ? parsed.marketplace : {}) },
                            tools: { ...prev.tools, ...(parsed.tools && typeof parsed.tools === 'object' ? parsed.tools : {}) },
                            agent: { ...prev.agent, ...(parsed.agent && typeof parsed.agent === 'object' ? parsed.agent : {}) },
                            discovery: (parsed.discovery && typeof parsed.discovery === 'object')
                                ? parsed.discovery
                                : { google: [], microsoft: [] }
                        };

                        // 3. INTERNAL MIGRATION: Fix legacy subdomain directory URLs
                        if (merged.profile.website?.includes('.bizoholic.net') && !merged.profile.website?.includes('directory.bizoholic.net')) {
                            merged.profile.website = generateDirectoryUrl(merged.profile.companyName, merged.profile.location);
                            merged.profile.websiteType = 'directory';
                        }

                        return merged;
                    });
                }
            }
        } catch (e) {
            console.error('[Onboarding] Failed to load/merge onboarding state. Resetting to defaults.', e);
            localStorage.removeItem(STORAGE_KEY);
            setState(INITIAL_STATE);
        } finally {
            setIsLoaded(true);
        }
    }, []);

    // Save to localStorage on change with loop protection
    const updateCountRef = React.useRef(0);
    const lastUpdateRef = React.useRef(0);

    useEffect(() => {
        if (isLoaded) {
            const now = Date.now();
            if (now - lastUpdateRef.current < 100) {
                updateCountRef.current++;
            } else {
                updateCountRef.current = 0;
            }
            lastUpdateRef.current = now;

            if (updateCountRef.current > 40) {
                console.error('[Onboarding] INFINITE LOOP DETECTED!', {
                    step: state.currentStep,
                    profile: state.profile.companyName,
                    website: state.profile.website,
                    discovery: !!state.discovery
                });
                // Force break - do not save or update further
                if (updateCountRef.current > 60) throw new Error("Onboarding state update loop aborted to prevent crash.");
                return;
            }

            localStorage.setItem(STORAGE_KEY, JSON.stringify({ ...state, version: STATE_VERSION }));
        }
    }, [state, isLoaded]);

    const updateProfile = useCallback((profile: Partial<OnboardingState['profile']> | ((prev: OnboardingState['profile']) => Partial<OnboardingState['profile']>)) => {
        setState(prev => {
            const updates = typeof profile === 'function' ? profile(prev.profile) : profile;
            const isChanged = Object.keys(updates).some(key => (updates as any)[key] !== (prev.profile as any)[key]);
            if (!isChanged) return prev;
            return {
                ...prev,
                profile: { ...prev.profile, ...updates }
            };
        });
    }, []);

    const updateDigitalPresence = useCallback((presence: Partial<OnboardingState['digitalPresence']> | ((prev: OnboardingState['digitalPresence']) => Partial<OnboardingState['digitalPresence']>)) => {
        setState(prev => {
            const updates = typeof presence === 'function' ? presence(prev.digitalPresence) : presence;
            const isChanged = Object.keys(updates).some(key => (updates as any)[key] !== (prev.digitalPresence as any)[key]);
            if (!isChanged) return prev;
            return {
                ...prev,
                digitalPresence: { ...prev.digitalPresence, ...updates }
            };
        });
    }, []);

    const updateAnalytics = useCallback((analytics: Partial<OnboardingState['analytics']> | ((prev: OnboardingState['analytics']) => Partial<OnboardingState['analytics']>)) => {
        setState(prev => {
            const updates = typeof analytics === 'function' ? analytics(prev.analytics) : analytics;
            const isChanged = Object.keys(updates).some(key => (updates as any)[key] !== (prev.analytics as any)[key]);
            if (!isChanged) return prev;
            return {
                ...prev,
                analytics: { ...prev.analytics, ...updates }
            };
        });
    }, []);

    const updateSocialMedia = useCallback((social: Partial<OnboardingState['socialMedia']> | ((prev: OnboardingState['socialMedia']) => Partial<OnboardingState['socialMedia']>)) => {
        setState(prev => {
            const updates = typeof social === 'function' ? social(prev.socialMedia) : social;
            const isChanged = Object.keys(updates).some(key => (updates as any)[key] !== (prev.socialMedia as any)[key]);
            if (!isChanged) return prev;
            return {
                ...prev,
                socialMedia: { ...prev.socialMedia, ...updates }
            };
        });
    }, []);

    const updateGoals = useCallback((goals: Partial<OnboardingState['goals']> | ((prev: OnboardingState['goals']) => Partial<OnboardingState['goals']>)) => {
        setState(prev => {
            const updates = typeof goals === 'function' ? goals(prev.goals) : goals;
            // Goals has nested targetAudience, simple check might fail, but let's do at least shallow for now
            const isChanged = Object.keys(updates).some(key => (updates as any)[key] !== (prev.goals as any)[key]);
            if (!isChanged) return prev;
            return {
                ...prev,
                goals: { ...prev.goals, ...updates }
            };
        });
    }, []);

    const updateTools = useCallback((tools: Partial<OnboardingState['tools']> | ((prev: OnboardingState['tools']) => Partial<OnboardingState['tools']>)) => {
        setState(prev => {
            const updates = typeof tools === 'function' ? tools(prev.tools) : tools;
            const isChanged = Object.keys(updates).some(key => {
                if (Array.isArray((updates as any)[key])) {
                    return JSON.stringify((updates as any)[key]) !== JSON.stringify((prev.tools as any)[key]);
                }
                return (updates as any)[key] !== (prev.tools as any)[key];
            });
            if (!isChanged) return prev;
            return {
                ...prev,
                tools: { ...prev.tools, ...updates }
            };
        });
    }, []);

    const updateAgent = useCallback((agent: Partial<OnboardingState['agent']> | ((prev: OnboardingState['agent']) => Partial<OnboardingState['agent']>)) => {
        setState(prev => {
            const updates = typeof agent === 'function' ? agent(prev.agent) : agent;
            const isChanged = Object.keys(updates).some(key => (updates as any)[key] !== (prev.agent as any)[key]);
            if (!isChanged) return prev;
            return {
                ...prev,
                agent: { ...prev.agent, ...updates }
            };
        });
    }, []);

    const updateMarketplace = useCallback((marketplace: Partial<OnboardingState['marketplace']> | ((prev: OnboardingState['marketplace']) => Partial<OnboardingState['marketplace']>)) => {
        setState(prev => {
            const updates = typeof marketplace === 'function' ? marketplace(prev.marketplace) : marketplace;
            const isChanged = Object.keys(updates).some(key => (updates as any)[key] !== (prev.marketplace as any)[key]);
            if (!isChanged) return prev;
            return {
                ...prev,
                marketplace: { ...prev.marketplace, ...updates }
            };
        });
    }, []);

    const updateDiscovery = useCallback((discovery: Partial<OnboardingState['discovery']> | ((prev: OnboardingState['discovery']) => Partial<OnboardingState['discovery']>)) => {
        setState(prev => {
            const updates = typeof discovery === 'function' ? discovery(prev.discovery) : discovery;
            // Discovery is complex, use JSON stringify for change detection
            if (JSON.stringify(updates) === JSON.stringify(prev.discovery)) return prev;
            return {
                ...prev,
                discovery: { ...prev.discovery, ...updates }
            };
        });
    }, []);

    const setSocialLogin = useCallback((social: OnboardingState['socialLogin']) => {
        setState(prev => {
            if (JSON.stringify(social) === JSON.stringify(prev.socialLogin)) return prev;
            return { ...prev, socialLogin: social };
        });
    }, []);

    const nextStep = useCallback(() => {
        setState(prev => ({ ...prev, currentStep: prev.currentStep + 1 }));
    }, []);

    const prevStep = useCallback(() => {
        setState(prev => ({ ...prev, currentStep: Math.max(0, prev.currentStep - 1) }));
    }, []);

    const resetOnboarding = useCallback(() => {
        setState(INITIAL_STATE);
        localStorage.removeItem(STORAGE_KEY);
    }, []);

    return {
        state,
        isLoaded,
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
        resetOnboarding
    };
}
