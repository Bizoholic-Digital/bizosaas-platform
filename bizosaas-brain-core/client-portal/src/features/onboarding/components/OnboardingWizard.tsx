'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import {
    Building2,
    MapPin,
    Zap,
    Shield,
    CheckCircle,
    ChevronRight,
    ChevronLeft,
    Loader2,
    Clock
} from 'lucide-react';
import { brainGateway } from '@/lib/brain-gateway-client';
import { BusinessProfileSetup } from './BusinessProfileSetup';
import { PlatformSelection } from './PlatformSelection';
import { CredentialsSetup } from './CredentialsSetup';
import { CampaignBudgetSetup } from './CampaignBudgetSetup';
import { CampaignStrategySetup } from './CampaignStrategySetup';

const STEPS = [
    { id: 'profile-basic', title: 'Business Profile', icon: Building2 },
    { id: 'profile-audience', title: 'Target Audience', icon: MapPin },
    { id: 'profile-hours', title: 'Hours & Attributes', icon: Clock },
    { id: 'profile-media', title: 'Social & Media', icon: Shield },
    { id: 'platforms', title: 'Platform Selection', icon: Zap },
    { id: 'credentials', title: 'Connect Platforms', icon: Shield },
    { id: 'campaign-budget', title: 'Campaign Budget', icon: CheckCircle },
    { id: 'strategy-summary', title: 'Final Strategy 🚀', icon: CheckCircle },
];

export function OnboardingWizard() {
    const router = useRouter();
    const [currentStep, setCurrentStep] = useState(0);
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // State for different steps
    const [businessProfile, setBusinessProfile] = useState<any>({
        name: '',
        description: '',
        category: '',
        subcategory: '',
        keywords: [],
        address: { street: '', city: '', state: '', zipCode: '', country: 'US' },
        contact: { phone: '', email: '', website: '' },
        hours: {},
        serviceAreas: [],
        photos: [],
        specialHours: [],
        attributes: {},
        socialMedia: {},
        targetAudience: { type: 'country-wide', locations: [] },
        budget: { dailyLimit: 10, currency: 'USD' }
    });

    const [platforms, setPlatforms] = useState<any[]>([]);
    const [aiRecommendations, setAiRecommendations] = useState<any>(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);

    useEffect(() => {
        async function loadData() {
            try {
                const [profile, status] = await Promise.all([
                    brainGateway.onboarding.getBusinessProfile(),
                    brainGateway.onboarding.getStatus()
                ]);

                if (profile) {
                    setBusinessProfile((prev: any) => ({ ...prev, ...profile }));
                }

                // Map status to current step if needed
                // For now start at 0
                setIsLoading(false);
            } catch (err) {
                console.error('Failed to load onboarding data:', err);
                setIsLoading(false);
            }
        }
        loadData();
    }, []);

    const handleNext = async () => {
        if (currentStep === STEPS.length - 1) {
            handleComplete();
            return;
        }

        setIsSaving(true);
        try {
            if (currentStep === 0) {
                await brainGateway.onboarding.updateBusinessProfile(businessProfile);
            } else if (currentStep === 1) {
                await brainGateway.onboarding.saveDigitalPresence({ platforms: platforms.filter(p => p.enabled).map(p => p.id) });
            }

            setCurrentStep(prev => prev + 1);
            setError(null);
        } catch (err) {
            setError('Failed to save progress. Please try again.');
        } finally {
            setIsSaving(false);
        }
    };

    const handleBack = () => {
        setCurrentStep(prev => Math.max(0, prev - 1));
    };

    const handleComplete = async () => {
        setIsSaving(true);
        try {
            await brainGateway.onboarding.complete();
            router.push('/dashboard');
        } catch (err) {
            setError('Failed to complete onboarding. Please try again.');
        } finally {
            setIsSaving(false);
        }
    };

    const handleAnalyze = async () => {
        setIsAnalyzing(true);
        try {
            const recommendations = await brainGateway.onboarding.discover(businessProfile);
            setAiRecommendations(recommendations);
        } catch (err) {
            console.error('Analysis failed:', err);
        } finally {
            setIsAnalyzing(false);
        }
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
        );
    }

    return (
        <div className="max-w-5xl mx-auto px-4 py-8">
            {/* Step Indicator */}
            <div className="mb-12">
                <div className="flex items-center justify-between relative">
                    {STEPS.map((step, index) => {
                        const Icon = step.icon;
                        const isCompleted = index < currentStep;
                        const isActive = index === currentStep;

                        return (
                            <div key={step.id} className="flex flex-col items-center relative z-10">
                                <div className={`w-12 h-12 rounded-full flex items-center justify-center transition-colors ${isCompleted ? 'bg-green-500 text-white' :
                                    isActive ? 'bg-blue-600 text-white' :
                                        'bg-gray-200 dark:bg-gray-700 text-gray-500'
                                    }`}>
                                    {isCompleted ? <CheckCircle className="w-6 h-6" /> : <Icon className="w-6 h-6" />}
                                </div>
                                <span className={`mt-2 text-sm font-medium ${isActive ? 'text-blue-600 dark:text-blue-400' : 'text-gray-500'
                                    }`}>
                                    {step.title}
                                </span>
                            </div>
                        );
                    })}
                    {/* Progress Line */}
                    <div className="absolute top-6 left-0 w-full h-0.5 bg-gray-200 dark:bg-gray-700 -z-0">
                        <div
                            className="h-full bg-green-500 transition-all duration-300"
                            style={{ width: `${(currentStep / (STEPS.length - 1)) * 100}%` }}
                        />
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
                <div className="p-8">
                    {error && (
                        <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-400 text-sm">
                            {error}
                        </div>
                    )}

                    {currentStep === 0 && (
                        <BusinessProfileSetup
                            profile={businessProfile}
                            onUpdate={setBusinessProfile}
                            onValidate={() => businessProfile.name && businessProfile.description}
                            forcedTab="basic"
                        />
                    )}

                    {currentStep === 1 && (
                        <BusinessProfileSetup
                            profile={businessProfile}
                            onUpdate={setBusinessProfile}
                            onValidate={() => businessProfile.targetAudience.locations.length > 0}
                            forcedTab="basic" // Audience is inside basic for now, or I can split it later
                        />
                    )}

                    {currentStep === 2 && (
                        <BusinessProfileSetup
                            profile={businessProfile}
                            onUpdate={setBusinessProfile}
                            onValidate={() => true}
                            forcedTab="hours"
                        />
                    )}

                    {currentStep === 3 && (
                        <BusinessProfileSetup
                            profile={businessProfile}
                            onUpdate={setBusinessProfile}
                            onValidate={() => true}
                            forcedTab="attributes"
                        />
                    )}

                    {currentStep === 4 && (
                        <PlatformSelection
                            platforms={platforms}
                            onUpdate={setPlatforms}
                            aiRecommendations={aiRecommendations}
                            businessProfile={businessProfile}
                            onAnalyze={handleAnalyze}
                            isAnalyzing={isAnalyzing}
                        />
                    )}

                    {currentStep === 5 && (
                        <CredentialsSetup
                            platforms={platforms.filter(p => p.enabled)}
                            onConnect={async (id) => { console.log('Connect', id) }}
                            onDisconnect={async (id) => { console.log('Disconnect', id) }}
                            isConnecting={false}
                            businessProfile={businessProfile}
                        />
                    )}

                    {currentStep === 6 && (
                        <CampaignBudgetSetup
                            budget={businessProfile.budget}
                            onUpdate={(budget) => setBusinessProfile({ ...businessProfile, budget })}
                        />
                    )}

                    {currentStep === 7 && (
                        <CampaignStrategySetup
                            profile={businessProfile}
                            platforms={platforms}
                            budget={businessProfile.budget}
                            onLaunch={handleComplete}
                            isLaunching={isSaving}
                        />
                    )}
                </div>

                {/* Footer Actions */}
                <div className="bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 p-6 flex items-center justify-between">
                    <button
                        onClick={handleBack}
                        disabled={currentStep === 0 || isSaving}
                        className="flex items-center text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white font-medium disabled:opacity-50"
                    >
                        <ChevronLeft className="w-5 h-5 mr-1" />
                        Back
                    </button>

                    <button
                        onClick={handleNext}
                        disabled={isSaving}
                        className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 font-bold flex items-center disabled:opacity-50"
                    >
                        {isSaving ? (
                            <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                        ) : currentStep === STEPS.length - 1 ? (
                            'Complete Setup'
                        ) : (
                            <>
                                Next
                                <ChevronRight className="w-5 h-5 ml-1" />
                            </>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
