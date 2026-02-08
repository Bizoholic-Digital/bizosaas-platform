export type SubscriptionTier = 'tier_1' | 'tier_2' | 'tier_3';

export interface TierConfig {
    name: string;
    price: string;
    features: string[];
}

export const TIER_CONFIGS: Record<SubscriptionTier, TierConfig> = {
    tier_1: {
        name: 'Starter',
        price: 'Free',
        features: ['basic_chat', 'standard_support']
    },
    tier_2: {
        name: 'Professional',
        price: '$49/mo',
        features: ['ai_agents', 'advanced_analytics', 'custom_integrations']
    },
    tier_3: {
        name: 'Enterprise',
        price: 'Custom',
        features: ['white_label', 'dedicated_support', 'unlimited_agents']
    }
};

export function useFeatureAccess() {
    // Use dynamic casting to avoid linting errors with literal comparisons
    const currentTier = 'tier_1' as SubscriptionTier;

    const hasFeature = (feature: string): boolean => {
        // Simple check based on tier hierarchy
        if (currentTier === 'tier_3') return true;
        if (currentTier === 'tier_2') {
            const tier2Features = ['ai_agents', 'analytics', 'custom_integrations'];
            return tier2Features.includes(feature) || TIER_CONFIGS.tier_1.features.includes(feature);
        }
        return TIER_CONFIGS.tier_1.features.includes(feature) || feature === 'basic_chat';
    };

    const getUpgradeSuggestions = (): { shouldUpgrade: boolean, nextTier: SubscriptionTier | null, reasons: string[] } => {
        return {
            shouldUpgrade: currentTier !== 'tier_3',
            nextTier: currentTier === 'tier_1' ? 'tier_2' : currentTier === 'tier_2' ? 'tier_3' : null,
            reasons: [
                'Unlock advanced AI capabilities',
                'Access real-time business insights',
                'Connect with custom external systems'
            ]
        };
    };

    return { hasFeature, getUpgradeSuggestions, currentTier };
}
