export interface BusinessProfile {
    companyName: string;
    industry: string;
    location: string;
    gmbLink?: string;
    website?: string;
    phone?: string;
    description?: string;
}

export interface DigitalPresence {
    websiteDetected: boolean;
    cmsType?: 'wordpress' | 'shopify' | 'wix' | 'squarespace' | 'custom' | 'other';
    crmType?: 'hubspot' | 'salesforce' | 'zoho' | 'pipedrive' | 'none';
    hasTracking?: boolean;
}

export interface AnalyticsConfig {
    gaId?: string;
    gscId?: string;
    setupLater: boolean;
}

export interface SocialMediaConfig {
    platforms: string[];
    facebookPageId?: string;
    instagramHandle?: string;
    linkedinCompanyId?: string;
    twitterHandle?: string;
    tiktokHandle?: string;
    setupLater: boolean;
}

export interface CampaignGoals {
    primaryGoal: 'lead_gen' | 'brand_awareness' | 'ecommerce_sales' | 'app_installs';
    secondaryGoals: string[];
    monthlyBudget: number;
    currency: string;
    targetAudience: {
        locations: string[];
        ageRange: string;
        interests: string[];
    };
}

export interface ToolIntegration {
    emailMarketing?: 'mailchimp' | 'klaviyo' | 'activecampaign' | 'none';
    adPlatforms: string[];
    wordpress?: {
        connected: boolean;
        siteUrl?: string;
        adminUrl?: string;
    };
    fluentCrm?: {
        connected: boolean;
    };
    wooCommerce?: {
        connected: boolean;
        consumerKey?: string;
        consumerSecret?: string;
    };
}

export interface AgentConfig {
    persona: 'marketing_manager' | 'sales_rep' | 'support_agent' | 'general_assistant';
    name: string;
    tone: 'professional' | 'friendly' | 'urgent' | 'witty';
}

export interface OnboardingState {
    currentStep: number;
    profile: BusinessProfile;
    digitalPresence: DigitalPresence;
    analytics: AnalyticsConfig;
    socialMedia: SocialMediaConfig;
    goals: CampaignGoals;
    tools: ToolIntegration;
    agent: AgentConfig; // New field
    isComplete: boolean;
}

export type StepId =
    | 'identity'
    | 'presence'
    | 'analytics'
    | 'social'
    | 'goals'
    | 'tools'
    | 'approval';

export const INITIAL_STATE: OnboardingState = {
    currentStep: 0,
    profile: {
        companyName: '',
        industry: '',
        location: '',
    },
    digitalPresence: {
        websiteDetected: false,
    },
    analytics: {
        setupLater: false,
    },
    socialMedia: {
        platforms: [],
        setupLater: false,
    },
    goals: {
        primaryGoal: 'lead_gen',
        secondaryGoals: [],
        monthlyBudget: 1000,
        currency: 'USD',
        targetAudience: {
            locations: [],
            ageRange: '25-45',
            interests: [],
        },
    },
    tools: {
        adPlatforms: [],
    },
    agent: {
        persona: 'marketing_manager',
        name: 'Alex',
        tone: 'professional'
    },
    isComplete: false,
};
