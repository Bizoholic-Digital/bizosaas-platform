export interface DiscoveryService {
    id: string;
    name: string;
    status: 'detected' | 'not_detected' | 'enabled' | 'error';
    cost?: string;
    requiresEnablement?: boolean;
}

export interface DiscoveryResults {
    google: DiscoveryService[];
    microsoft: DiscoveryService[];
    lastUpdated?: string;
}

export interface SocialLoginInfo {
    provider: 'google' | 'microsoft' | 'facebook' | 'apple' | 'none';
    email: string;
    name?: string;
    profileImageUrl?: string;
}

export interface AIAgentConfig {
    persona: 'csm' | 'marketing_manager' | 'sales_rep' | 'support_agent' | 'general_assistant';
    name: string;
    tone: 'professional' | 'friendly' | 'urgent' | 'witty';
    clientAdvocate: boolean;
    authorized?: boolean;
}

export interface BusinessProfile {
    companyName: string;
    industry: string;
    location: string;
    gmbLink?: string;
    website?: string;
    directoryUrl?: string;
    websiteType?: 'owned' | 'directory';
    phone?: string;
    description?: string;
}

export interface DigitalPresence {
    websiteDetected: boolean;
    cmsType?: 'wordpress' | 'shopify' | 'wix' | 'squarespace' | 'custom' | 'other';
    crmType?: 'hubspot' | 'salesforce' | 'zoho' | 'pipedrive' | 'fluentcrm' | 'none';
    hasTracking?: boolean;
}

export interface AnalyticsProperty {
    id: string;
    name: string;
    type?: string;
}

export interface AnalyticsConfig {
    gtmId?: string;
    gaId?: string;
    gscId?: string;
    fbId?: string;
    clarityId?: string;
    bingId?: string;
    setupLater: boolean;
    availableGtmContainers?: AnalyticsProperty[];
    availableGaProperties?: AnalyticsProperty[];
    availableGscSites?: AnalyticsProperty[];
    availableFbPixels?: AnalyticsProperty[];
    availableClarityProjects?: AnalyticsProperty[];
    availableBingProfiles?: AnalyticsProperty[];
    auditedServices?: {
        essential: Array<{ id: string, name: string, service: string, status: string }>;
        optional: Array<{ id: string, name: string, service: string, status: string }>;
    };
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
    selectedMcps?: string[];
    emailMarketing?: 'mailchimp' | 'klaviyo' | 'activecampaign' | 'none';
    adPlatforms: string[];
    wordpress?: {
        connected: boolean;
        siteUrl?: string;
        adminUrl?: string;
    };
    fluentCrm?: {
        connected: boolean;
        selectedMcps?: string[];
    };
    wooCommerce?: {
        connected: boolean;
        consumerKey?: string;
        consumerSecret?: string;
    };
}

export interface MarketplaceAsset {
    id: string;
    name: string;
    slug: string;
    type: 'theme' | 'plugin';
    price: number | 'free';
    provider: 'envato' | 'wordpress' | 'bizosaas' | 'other';
    affiliateLink?: string;
    isRecommended?: boolean;
    description?: string;
    image?: string;
}

export interface MarketplaceConfig {
    selectedThemes: string[]; // slugs
    selectedPlugins: string[]; // slugs
    useBridge: boolean;
}

export interface OnboardingState {
    currentStep: number;
    socialLogin?: SocialLoginInfo;
    profile: BusinessProfile;
    digitalPresence: DigitalPresence;
    discovery: DiscoveryResults;
    analytics: AnalyticsConfig;
    socialMedia: SocialMediaConfig;
    goals: CampaignGoals;
    tools: ToolIntegration;
    marketplace: MarketplaceConfig;
    agent: AIAgentConfig;
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
        directoryUrl: ''
    },
    digitalPresence: {
        websiteDetected: false,
    },
    discovery: {
        google: [],
        microsoft: [],
    },
    analytics: {
        gtmId: '',
        gaId: '',
        gscId: '',
        fbId: '',
        clarityId: '',
        bingId: '',
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
        selectedMcps: [],
        adPlatforms: [],
    },
    marketplace: {
        selectedThemes: [],
        selectedPlugins: [],
        useBridge: true, // Recommended by default
    },
    agent: {
        persona: 'csm',
        name: 'Alex',
        tone: 'professional',
        clientAdvocate: true
    },
    isComplete: false,
};
