export interface CredentialStrategy {
    name: string;
    description: string;
    benefits: string[];
}

export const CREDENTIAL_STRATEGIES: Record<string, CredentialStrategy> = {
    bring_your_own_key: {
        name: 'Bring Your Own Key (BYOK)',
        description: 'Use your own API keys from providers like OpenAI, Anthropic, etc.',
        benefits: ['Maximum cost savings', 'Direct billing with providers', 'Keep your existing quotas']
    },
    platform_managed: {
        name: 'Platform Managed',
        description: 'We handle all API keys and billing for you.',
        benefits: ['Simplified billing', 'No setup required', 'Optimized model routing']
    },
    hybrid_mode: {
        name: 'Hybrid Mode',
        description: 'Use your own keys for some tasks, and platform keys for others.',
        benefits: ['Best of both worlds', 'Automatic failover', 'Flexible scaling']
    },
    auto_resolve: {
        name: 'Auto Resolve',
        description: 'Automatically choose the best strategy based on cost and performance.',
        benefits: ['Zero-touch optimization', 'Lowest possible latency', 'Budget-aware routing']
    }
};

export const SUPPORTED_PLATFORMS = [
    {
        id: 'openai',
        name: 'OpenAI',
        description: 'Connect your OpenAI account to use GPT-4o, GPT-3.5 Turbo, and DALL-E.',
        icon: '🤖',
        credentials: [
            { key: 'api_key', label: 'API Key', required: true, type: 'password', placeholder: 'sk-...' }
        ]
    },
    {
        id: 'anthropic',
        name: 'Anthropic',
        description: 'Connect your Anthropic account to use Claude 3 Opus, Sonnet, and Haiku.',
        icon: '🧠',
        credentials: [
            { key: 'api_key', label: 'API Key', required: true, type: 'password', placeholder: 'sk-ant-...' }
        ]
    }
];
