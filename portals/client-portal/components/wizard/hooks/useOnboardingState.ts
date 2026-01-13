import { useState, useEffect } from 'react';
import { OnboardingState, INITIAL_STATE } from '../types/onboarding';

const STORAGE_KEY = 'bizosaas_onboarding_state';

export function useOnboardingState() {
    const [state, setState] = useState<OnboardingState>(INITIAL_STATE);
    const [isLoaded, setIsLoaded] = useState(false);

    // Load from localStorage on mount
    useEffect(() => {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            if (saved) {
                const parsed = JSON.parse(saved);
                // Deep-ish merge to ensure new top-level objects (like marketplace) exist
                setState(prev => ({
                    ...prev,
                    ...parsed,
                    // Ensure sub-objects also merge safely if they are complex
                    profile: { ...prev.profile, ...(parsed.profile || {}) },
                    digitalPresence: { ...prev.digitalPresence, ...(parsed.digitalPresence || {}) },
                    analytics: { ...prev.analytics, ...(parsed.analytics || {}) },
                    marketplace: { ...prev.marketplace, ...(parsed.marketplace || {}) },
                    tools: { ...prev.tools, ...(parsed.tools || {}) },
                    agent: { ...prev.agent, ...(parsed.agent || {}) },
                    discovery: { ...prev.discovery, ...(parsed.discovery || {}) }
                }));
            }
        } catch (e) {
            console.error('Failed to load onboarding state', e);
        } finally {
            setIsLoaded(true);
        }
    }, []);

    // Save to localStorage on change
    useEffect(() => {
        if (isLoaded) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        }
    }, [state, isLoaded]);

    const updateProfile = (profile: Partial<OnboardingState['profile']>) => {
        setState(prev => ({ ...prev, profile: { ...prev.profile, ...profile } }));
    };

    const updateDigitalPresence = (presence: Partial<OnboardingState['digitalPresence']>) => {
        setState(prev => ({ ...prev, digitalPresence: { ...prev.digitalPresence, ...presence } }));
    };

    const updateAnalytics = (analytics: Partial<OnboardingState['analytics']>) => {
        setState(prev => ({ ...prev, analytics: { ...prev.analytics, ...analytics } }));
    };

    const updateSocialMedia = (social: Partial<OnboardingState['socialMedia']>) => {
        setState(prev => ({ ...prev, socialMedia: { ...prev.socialMedia, ...social } }));
    };

    const updateGoals = (goals: Partial<OnboardingState['goals']>) => {
        setState(prev => ({ ...prev, goals: { ...prev.goals, ...goals } }));
    };

    const updateTools = (tools: Partial<OnboardingState['tools']>) => {
        setState(prev => ({ ...prev, tools: { ...prev.tools, ...tools } }));
    };

    const updateAgent = (agent: Partial<OnboardingState['agent']>) => {
        setState(prev => ({ ...prev, agent: { ...prev.agent, ...agent } }));
    };

    const updateMarketplace = (marketplace: Partial<OnboardingState['marketplace']>) => {
        setState(prev => ({ ...prev, marketplace: { ...prev.marketplace, ...marketplace } }));
    };

    const updateDiscovery = (discovery: Partial<OnboardingState['discovery']>) => {
        setState(prev => ({ ...prev, discovery: { ...prev.discovery, ...discovery } }));
    };

    const setSocialLogin = (social: OnboardingState['socialLogin']) => {
        setState(prev => ({ ...prev, socialLogin: social }));
    };

    const nextStep = () => {
        setState(prev => ({ ...prev, currentStep: prev.currentStep + 1 }));
    };

    const prevStep = () => {
        setState(prev => ({ ...prev, currentStep: Math.max(0, prev.currentStep - 1) }));
    };

    const resetOnboarding = () => {
        setState(INITIAL_STATE);
        localStorage.removeItem(STORAGE_KEY);
    };

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
