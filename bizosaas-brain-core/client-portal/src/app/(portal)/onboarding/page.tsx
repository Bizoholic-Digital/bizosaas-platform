'use client';

import { OnboardingWizard } from '@/features/onboarding/components/OnboardingWizard';

export default function OnboardingPage() {
    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <div className="container mx-auto px-4 py-12">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white mb-4">
                        Welcome to Antigravity
                    </h1>
                    <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                        Let's get your business set up for success. Follow these steps to configure your digital presence.
                    </p>
                </div>

                <OnboardingWizard />
            </div>
        </div>
    );
}
