import { Metadata } from 'next';
import { OnboardingWizard } from '@/components/wizard/OnboardingWizard';

export const metadata: Metadata = {
    title: 'Setup Your Workspace | BizOSaaS',
    description: 'Complete your business profile to activate AI agents',
};

export default function OnboardingPage() {
    return <OnboardingWizard />;
}
