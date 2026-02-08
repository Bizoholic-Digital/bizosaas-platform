/**
 * AI Agent Registry
 * Central registry for all 93+ AI agents with capabilities, tools, and service requirements
 */

import type { AIAgent, AgentCategory } from './types';

// ============================================================================
// Agent Registry - All 93 Agents
// ============================================================================

export const AGENT_REGISTRY: Record<string, AIAgent> = {
    // ==========================================================================
    // 1. GENERAL & PERSONAL ASSISTANT (1 agent)
    // ==========================================================================

    personal_assistant: {
        id: 'personal_assistant',
        name: 'Personal AI Assistant',
        description: 'Main coordinator that routes requests to specialized agents',
        category: 'general',
        capabilities: [
            {
                id: 'intent_analysis',
                name: 'Intent Analysis',
                description: 'Analyzes user intent and routes to appropriate agents'
            },
            {
                id: 'agent_coordination',
                name: 'Agent Coordination',
                description: 'Coordinates multiple agents for complex tasks'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'free',
        permissions: [],
        status: 'active',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['coordinator', 'general'],
        },
        systemPrompt: 'You are a helpful AI assistant that coordinates with specialized agents to help users with their business needs.',
    },

    // ==========================================================================
    // 2. MARKETING & ADVERTISING (15 agents)
    // ==========================================================================

    campaign_manager: {
        id: 'campaign_manager',
        name: 'Campaign Manager',
        description: 'Creates and optimizes marketing campaigns across all channels',
        category: 'marketing',
        capabilities: [
            {
                id: 'campaign_creation',
                name: 'Campaign Creation',
                description: 'Creates comprehensive marketing campaigns'
            },
            {
                id: 'performance_analysis',
                name: 'Performance Analysis',
                description: 'Analyzes campaign performance and provides insights'
            }
        ],
        requiredTools: ['analytics', 'reporting'],
        requiredServices: ['analytics_api'],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: ['view_campaigns', 'create_campaigns'],
        status: 'active',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'campaigns'],
        },
    },

    google_ads_specialist: {
        id: 'google_ads_specialist',
        name: 'Google Ads Specialist',
        description: 'Expert in Google Ads campaign creation and optimization',
        category: 'marketing',
        capabilities: [
            {
                id: 'google_ads_campaigns',
                name: 'Google Ads Campaigns',
                description: 'Creates and manages Google Ads campaigns',
                requiredTools: ['google_ads_api'],
                requiredServices: ['google_ads']
            },
            {
                id: 'keyword_bidding',
                name: 'Keyword Bidding',
                description: 'Optimizes keyword bidding strategies'
            }
        ],
        requiredTools: ['google_ads_api'],
        requiredServices: ['google_ads'],
        requiredAPIs: [
            {
                service: 'google_ads',
                keyType: 'developer_token',
                required: true,
                fallbackToPlatform: true
            }
        ],
        costTier: 'premium',
        permissions: ['view_google_ads', 'manage_google_ads'],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'google-ads', 'ppc'],
        },
    },

    meta_ads_specialist: {
        id: 'meta_ads_specialist',
        name: 'Meta Ads Specialist',
        description: 'Expert in Facebook and Instagram advertising',
        category: 'marketing',
        capabilities: [
            {
                id: 'meta_campaigns',
                name: 'Meta Campaigns',
                description: 'Creates Facebook/Instagram ad campaigns'
            },
            {
                id: 'audience_targeting',
                name: 'Audience Targeting',
                description: 'Advanced audience targeting and segmentation'
            }
        ],
        requiredTools: ['meta_ads_api'],
        requiredServices: ['meta_ads'],
        requiredAPIs: [
            {
                service: 'meta_ads',
                keyType: 'access_token',
                required: true,
                fallbackToPlatform: true
            }
        ],
        costTier: 'premium',
        permissions: ['view_meta_ads', 'manage_meta_ads'],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'meta-ads', 'social-media'],
        },
    },

    linkedin_ads_specialist: {
        id: 'linkedin_ads_specialist',
        name: 'LinkedIn Ads Specialist',
        description: 'B2B advertising expert for LinkedIn campaigns',
        category: 'marketing',
        capabilities: [
            {
                id: 'linkedin_campaigns',
                name: 'LinkedIn Campaigns',
                description: 'Creates B2B-focused LinkedIn ad campaigns'
            },
            {
                id: 'lead_gen_forms',
                name: 'Lead Gen Forms',
                description: 'Optimizes LinkedIn lead generation forms'
            }
        ],
        requiredTools: ['linkedin_ads_api'],
        requiredServices: ['linkedin_ads'],
        requiredAPIs: [
            {
                service: 'linkedin_ads',
                keyType: 'access_token',
                required: true,
                fallbackToPlatform: true
            }
        ],
        costTier: 'premium',
        permissions: ['view_linkedin_ads', 'manage_linkedin_ads'],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'linkedin', 'b2b'],
        },
    },

    tiktok_ads_specialist: {
        id: 'tiktok_ads_specialist',
        name: 'TikTok Ads Specialist',
        description: 'Expert in TikTok advertising and viral content',
        category: 'marketing',
        capabilities: [
            {
                id: 'tiktok_campaigns',
                name: 'TikTok Campaigns',
                description: 'Creates engaging TikTok ad campaigns'
            }
        ],
        requiredTools: ['tiktok_ads_api'],
        requiredServices: ['tiktok_ads'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: ['view_tiktok_ads', 'manage_tiktok_ads'],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'tiktok', 'video'],
        },
    },

    youtube_ads_specialist: {
        id: 'youtube_ads_specialist',
        name: 'YouTube Ads Specialist',
        description: 'Video advertising expert for YouTube campaigns',
        category: 'marketing',
        capabilities: [
            {
                id: 'youtube_campaigns',
                name: 'YouTube Campaigns',
                description: 'Creates video ad campaigns on YouTube'
            }
        ],
        requiredTools: ['youtube_ads_api'],
        requiredServices: ['youtube_ads'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: ['view_youtube_ads', 'manage_youtube_ads'],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'youtube', 'video'],
        },
    },

    display_ads_specialist: {
        id: 'display_ads_specialist',
        name: 'Display Ads Specialist',
        description: 'Expert in display advertising and banner ads',
        category: 'marketing',
        capabilities: [
            {
                id: 'display_campaigns',
                name: 'Display Campaigns',
                description: 'Creates display ad campaigns'
            }
        ],
        requiredTools: ['display_ads_api'],
        requiredServices: ['display_ads'],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: ['view_display_ads', 'manage_display_ads'],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'display-ads'],
        },
    },

    native_ads_specialist: {
        id: 'native_ads_specialist',
        name: 'Native Ads Specialist',
        description: 'Expert in native advertising and sponsored content',
        category: 'marketing',
        capabilities: [
            {
                id: 'native_campaigns',
                name: 'Native Campaigns',
                description: 'Creates native ad campaigns'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'native-ads'],
        },
    },

    programmatic_buyer: {
        id: 'programmatic_buyer',
        name: 'Programmatic Buyer',
        description: 'Automated programmatic ad buying specialist',
        category: 'marketing',
        capabilities: [
            {
                id: 'programmatic_buying',
                name: 'Programmatic Buying',
                description: 'Automates ad buying across platforms'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'programmatic'],
        },
    },

    affiliate_marketing_manager: {
        id: 'affiliate_marketing_manager',
        name: 'Affiliate Marketing Manager',
        description: 'Manages affiliate marketing programs and partnerships',
        category: 'marketing',
        capabilities: [
            {
                id: 'affiliate_management',
                name: 'Affiliate Management',
                description: 'Manages affiliate programs and tracking'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'affiliate'],
        },
    },

    influencer_marketing_coordinator: {
        id: 'influencer_marketing_coordinator',
        name: 'Influencer Marketing Coordinator',
        description: 'Coordinates influencer marketing campaigns',
        category: 'marketing',
        capabilities: [
            {
                id: 'influencer_campaigns',
                name: 'Influencer Campaigns',
                description: 'Manages influencer partnerships and campaigns'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'influencer'],
        },
    },

    brand_strategist: {
        id: 'brand_strategist',
        name: 'Brand Strategist',
        description: 'Develops brand strategy and positioning',
        category: 'marketing',
        capabilities: [
            {
                id: 'brand_strategy',
                name: 'Brand Strategy',
                description: 'Creates comprehensive brand strategies'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'branding'],
        },
    },

    conversion_rate_optimizer: {
        id: 'conversion_rate_optimizer',
        name: 'Conversion Rate Optimizer',
        description: 'Optimizes conversion rates across all channels',
        category: 'marketing',
        capabilities: [
            {
                id: 'cro_analysis',
                name: 'CRO Analysis',
                description: 'Analyzes and optimizes conversion rates'
            }
        ],
        requiredTools: ['analytics'],
        requiredServices: ['analytics_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'cro', 'optimization'],
        },
    },

    ad_copywriter: {
        id: 'ad_copywriter',
        name: 'Ad Copywriter',
        description: 'Creates compelling ad copy for all platforms',
        category: 'marketing',
        capabilities: [
            {
                id: 'ad_copy_creation',
                name: 'Ad Copy Creation',
                description: 'Writes high-converting ad copy'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'copywriting'],
        },
    },

    marketing_automation_specialist: {
        id: 'marketing_automation_specialist',
        name: 'Marketing Automation Specialist',
        description: 'Automates marketing workflows and campaigns',
        category: 'marketing',
        capabilities: [
            {
                id: 'marketing_automation',
                name: 'Marketing Automation',
                description: 'Creates automated marketing workflows'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['marketing', 'automation'],
        },
    },

    // ==========================================================================
    // 3. CONTENT CREATION (12 agents)
    // ==========================================================================

    blog_writer: {
        id: 'blog_writer',
        name: 'Blog Content Writer',
        description: 'Creates SEO-optimized blog posts and articles',
        category: 'content',
        capabilities: [
            {
                id: 'blog_creation',
                name: 'Blog Creation',
                description: 'Writes engaging blog posts'
            },
            {
                id: 'seo_optimization',
                name: 'SEO Optimization',
                description: 'Optimizes content for search engines'
            }
        ],
        requiredTools: [],
        requiredServices: ['cms_api'],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: ['create_content'],
        status: 'active',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['content', 'blogging', 'seo'],
        },
    },

    social_media_content_creator: {
        id: 'social_media_content_creator',
        name: 'Social Media Content Creator',
        description: 'Creates engaging social media content',
        category: 'content',
        capabilities: [
            {
                id: 'social_content',
                name: 'Social Content',
                description: 'Creates platform-specific social media content'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['content', 'social-media'],
        },
    },

    video_script_writer: {
        id: 'video_script_writer',
        name: 'Video Script Writer',
        description: 'Writes scripts for video content',
        category: 'content',
        capabilities: [
            {
                id: 'video_scripts',
                name: 'Video Scripts',
                description: 'Creates engaging video scripts'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['content', 'video'],
        },
    },

    email_copywriter: {
        id: 'email_copywriter',
        name: 'Email Copywriter',
        description: 'Creates compelling email marketing content',
        category: 'content',
        capabilities: [
            {
                id: 'email_content',
                name: 'Email Content',
                description: 'Writes high-converting email copy'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['content', 'email'],
        },
    },

    landing_page_copywriter: {
        id: 'landing_page_copywriter',
        name: 'Landing Page Copywriter',
        description: 'Creates conversion-focused landing page copy',
        category: 'content',
        capabilities: [
            {
                id: 'landing_page_copy',
                name: 'Landing Page Copy',
                description: 'Writes high-converting landing page content'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['content', 'landing-pages', 'conversion'],
        },
    },

    product_description_writer: {
        id: 'product_description_writer',
        name: 'Product Description Writer',
        description: 'Creates compelling product descriptions',
        category: 'content',
        capabilities: [
            {
                id: 'product_descriptions',
                name: 'Product Descriptions',
                description: 'Writes SEO-optimized product descriptions'
            }
        ],
        requiredTools: [],
        requiredServices: ['ecommerce_api'],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['content', 'ecommerce'],
        },
    },

    press_release_writer: {
        id: 'press_release_writer',
        name: 'Press Release Writer',
        description: 'Writes professional press releases',
        category: 'content',
        capabilities: [
            {
                id: 'press_releases',
                name: 'Press Releases',
                description: 'Creates newsworthy press releases'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['content', 'pr'],
        },
    },

    white_paper_writer: {
        id: 'white_paper_writer',
        name: 'White Paper Writer',
        description: 'Creates in-depth white papers and research documents',
        category: 'content',
        capabilities: [
            {
                id: 'white_papers',
                name: 'White Papers',
                description: 'Writes authoritative white papers'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['content', 'research'],
        },
    },

    case_study_writer: {
        id: 'case_study_writer',
        name: 'Case Study Writer',
        description: 'Creates compelling customer case studies',
        category: 'content',
        capabilities: [
            {
                id: 'case_studies',
                name: 'Case Studies',
                description: 'Writes detailed case studies'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['content', 'case-studies'],
        },
    },

    content_strategist: {
        id: 'content_strategist',
        name: 'Content Strategist',
        description: 'Develops comprehensive content strategies',
        category: 'content',
        capabilities: [
            {
                id: 'content_strategy',
                name: 'Content Strategy',
                description: 'Creates content calendars and strategies'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['content', 'strategy'],
        },
    },

    content_editor: {
        id: 'content_editor',
        name: 'Content Editor',
        description: 'Edits and improves existing content',
        category: 'content',
        capabilities: [
            {
                id: 'content_editing',
                name: 'Content Editing',
                description: 'Edits and polishes content'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['content', 'editing'],
        },
    },

    content_translator: {
        id: 'content_translator',
        name: 'Content Translator',
        description: 'Translates content into multiple languages',
        category: 'content',
        capabilities: [
            {
                id: 'content_translation',
                name: 'Content Translation',
                description: 'Translates content while maintaining tone and context'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['content', 'translation'],
        },
    },

    // ==========================================================================
    // 4. SEO (10 agents)
    // ==========================================================================

    seo_strategist: {
        id: 'seo_strategist',
        name: 'SEO Strategist',
        description: 'Develops comprehensive SEO strategies',
        category: 'seo',
        capabilities: [
            {
                id: 'seo_strategy',
                name: 'SEO Strategy',
                description: 'Creates comprehensive SEO strategies'
            },
            {
                id: 'seo_audit',
                name: 'SEO Audit',
                description: 'Performs detailed SEO audits'
            }
        ],
        requiredTools: ['seo_tools'],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'active',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['seo', 'strategy'],
        },
    },

    keyword_researcher: {
        id: 'keyword_researcher',
        name: 'Keyword Researcher',
        description: 'Researches and analyzes keywords for SEO',
        category: 'seo',
        capabilities: [
            {
                id: 'keyword_research',
                name: 'Keyword Research',
                description: 'Discovers high-value keywords'
            }
        ],
        requiredTools: ['keyword_tools'],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['seo', 'keywords'],
        },
    },

    onpage_seo_optimizer: {
        id: 'onpage_seo_optimizer',
        name: 'On-Page SEO Optimizer',
        description: 'Optimizes on-page SEO elements',
        category: 'seo',
        capabilities: [
            {
                id: 'onpage_optimization',
                name: 'On-Page Optimization',
                description: 'Optimizes meta tags, headers, and content'
            }
        ],
        requiredTools: [],
        requiredServices: ['cms_api'],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['seo', 'on-page'],
        },
    },

    technical_seo_specialist: {
        id: 'technical_seo_specialist',
        name: 'Technical SEO Specialist',
        description: 'Handles technical SEO optimization',
        category: 'seo',
        capabilities: [
            {
                id: 'technical_seo',
                name: 'Technical SEO',
                description: 'Optimizes site speed, structure, and crawlability'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['seo', 'technical'],
        },
    },

    link_building_specialist: {
        id: 'link_building_specialist',
        name: 'Link Building Specialist',
        description: 'Develops link building strategies',
        category: 'seo',
        capabilities: [
            {
                id: 'link_building',
                name: 'Link Building',
                description: 'Creates backlink strategies'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['seo', 'link-building'],
        },
    },

    local_seo_specialist: {
        id: 'local_seo_specialist',
        name: 'Local SEO Specialist',
        description: 'Optimizes for local search results',
        category: 'seo',
        capabilities: [
            {
                id: 'local_seo',
                name: 'Local SEO',
                description: 'Optimizes Google My Business and local listings'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['seo', 'local'],
        },
    },

    seo_content_optimizer: {
        id: 'seo_content_optimizer',
        name: 'SEO Content Optimizer',
        description: 'Optimizes content for search engines',
        category: 'seo',
        capabilities: [
            {
                id: 'content_optimization',
                name: 'Content Optimization',
                description: 'Optimizes content for target keywords'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['seo', 'content'],
        },
    },

    seo_auditor: {
        id: 'seo_auditor',
        name: 'SEO Auditor',
        description: 'Performs comprehensive SEO audits',
        category: 'seo',
        capabilities: [
            {
                id: 'seo_auditing',
                name: 'SEO Auditing',
                description: 'Conducts detailed SEO audits'
            }
        ],
        requiredTools: ['seo_tools'],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['seo', 'audit'],
        },
    },

    schema_markup_specialist: {
        id: 'schema_markup_specialist',
        name: 'Schema Markup Specialist',
        description: 'Implements structured data markup',
        category: 'seo',
        capabilities: [
            {
                id: 'schema_markup',
                name: 'Schema Markup',
                description: 'Implements schema.org structured data'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['seo', 'schema'],
        },
    },

    voice_search_optimizer: {
        id: 'voice_search_optimizer',
        name: 'Voice Search Optimizer',
        description: 'Optimizes content for voice search',
        category: 'seo',
        capabilities: [
            {
                id: 'voice_search',
                name: 'Voice Search',
                description: 'Optimizes for voice search queries'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['seo', 'voice-search'],
        },
    },

    // ==========================================================================
    // 5. SOCIAL MEDIA (8 agents)
    // ==========================================================================

    social_media_manager: {
        id: 'social_media_manager',
        name: 'Social Media Manager',
        description: 'Manages social media presence across all platforms',
        category: 'social_media',
        capabilities: [
            {
                id: 'social_management',
                name: 'Social Management',
                description: 'Manages multi-platform social media presence'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['social-media', 'management'],
        },
    },

    community_manager: {
        id: 'community_manager',
        name: 'Community Manager',
        description: 'Manages online communities and engagement',
        category: 'social_media',
        capabilities: [
            {
                id: 'community_engagement',
                name: 'Community Engagement',
                description: 'Manages community interactions and engagement'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['social-media', 'community'],
        },
    },

    instagram_specialist: {
        id: 'instagram_specialist',
        name: 'Instagram Specialist',
        description: 'Expert in Instagram marketing and content',
        category: 'social_media',
        capabilities: [
            {
                id: 'instagram_marketing',
                name: 'Instagram Marketing',
                description: 'Creates Instagram-specific content and strategies'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['social-media', 'instagram'],
        },
    },

    twitter_specialist: {
        id: 'twitter_specialist',
        name: 'Twitter/X Specialist',
        description: 'Expert in Twitter/X marketing and engagement',
        category: 'social_media',
        capabilities: [
            {
                id: 'twitter_marketing',
                name: 'Twitter Marketing',
                description: 'Creates Twitter-specific content and engagement strategies'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['social-media', 'twitter'],
        },
    },

    linkedin_specialist: {
        id: 'linkedin_specialist',
        name: 'LinkedIn Specialist',
        description: 'Expert in LinkedIn content and B2B networking',
        category: 'social_media',
        capabilities: [
            {
                id: 'linkedin_marketing',
                name: 'LinkedIn Marketing',
                description: 'Creates LinkedIn-specific B2B content'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['social-media', 'linkedin', 'b2b'],
        },
    },

    pinterest_specialist: {
        id: 'pinterest_specialist',
        name: 'Pinterest Specialist',
        description: 'Expert in Pinterest marketing and visual content',
        category: 'social_media',
        capabilities: [
            {
                id: 'pinterest_marketing',
                name: 'Pinterest Marketing',
                description: 'Creates Pinterest-specific visual content'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['social-media', 'pinterest'],
        },
    },

    tiktok_specialist: {
        id: 'tiktok_specialist',
        name: 'TikTok Specialist',
        description: 'Expert in TikTok content creation and trends',
        category: 'social_media',
        capabilities: [
            {
                id: 'tiktok_content',
                name: 'TikTok Content',
                description: 'Creates viral TikTok content'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['social-media', 'tiktok'],
        },
    },

    social_listening_analyst: {
        id: 'social_listening_analyst',
        name: 'Social Listening Analyst',
        description: 'Monitors and analyzes social media conversations',
        category: 'social_media',
        capabilities: [
            {
                id: 'social_listening',
                name: 'Social Listening',
                description: 'Monitors brand mentions and sentiment'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['social-media', 'analytics'],
        },
    },

    // ==========================================================================
    // 6. ANALYTICS & INSIGHTS (6 agents)
    // ==========================================================================

    data_analyst: {
        id: 'data_analyst',
        name: 'Data Analyst',
        description: 'Analyzes business data and provides insights',
        category: 'analytics',
        capabilities: [
            {
                id: 'data_analysis',
                name: 'Data Analysis',
                description: 'Analyzes business metrics and KPIs'
            }
        ],
        requiredTools: ['analytics'],
        requiredServices: ['analytics_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'active',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['analytics', 'data'],
        },
    },

    google_analytics_specialist: {
        id: 'google_analytics_specialist',
        name: 'Google Analytics Specialist',
        description: 'Expert in Google Analytics setup and analysis',
        category: 'analytics',
        capabilities: [
            {
                id: 'ga4_analysis',
                name: 'GA4 Analysis',
                description: 'Analyzes Google Analytics 4 data'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [
            {
                service: 'google_analytics',
                keyType: 'measurement_id',
                required: true,
                fallbackToPlatform: true
            }
        ],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['analytics', 'google-analytics'],
        },
    },

    conversion_analyst: {
        id: 'conversion_analyst',
        name: 'Conversion Analyst',
        description: 'Analyzes and optimizes conversion funnels',
        category: 'analytics',
        capabilities: [
            {
                id: 'conversion_analysis',
                name: 'Conversion Analysis',
                description: 'Analyzes conversion funnels and drop-off points'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['analytics', 'conversion'],
        },
    },

    attribution_analyst: {
        id: 'attribution_analyst',
        name: 'Attribution Analyst',
        description: 'Analyzes marketing attribution and ROI',
        category: 'analytics',
        capabilities: [
            {
                id: 'attribution_modeling',
                name: 'Attribution Modeling',
                description: 'Creates attribution models for marketing channels'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['analytics', 'attribution'],
        },
    },

    predictive_analytics_specialist: {
        id: 'predictive_analytics_specialist',
        name: 'Predictive Analytics Specialist',
        description: 'Uses AI to predict future trends and outcomes',
        category: 'analytics',
        capabilities: [
            {
                id: 'predictive_modeling',
                name: 'Predictive Modeling',
                description: 'Creates predictive models for business metrics'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['analytics', 'predictive', 'ai'],
        },
    },

    customer_insights_analyst: {
        id: 'customer_insights_analyst',
        name: 'Customer Insights Analyst',
        description: 'Analyzes customer behavior and preferences',
        category: 'analytics',
        capabilities: [
            {
                id: 'customer_analysis',
                name: 'Customer Analysis',
                description: 'Analyzes customer behavior patterns'
            }
        ],
        requiredTools: [],
        requiredServices: ['crm_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['analytics', 'customer'],
        },
    },

    competitive_intelligence_analyst: {
        id: 'competitive_intelligence_analyst',
        name: 'Competitive Intelligence Analyst',
        description: 'Analyzes competitor strategies and market position',
        category: 'analytics',
        capabilities: [
            {
                id: 'competitive_analysis',
                name: 'Competitive Analysis',
                description: 'Analyzes competitor strategies'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['analytics', 'competitive'],
        },
    },

    dashboard_builder: {
        id: 'dashboard_builder',
        name: 'Dashboard Builder',
        description: 'Creates custom analytics dashboards',
        category: 'analytics',
        capabilities: [
            {
                id: 'dashboard_creation',
                name: 'Dashboard Creation',
                description: 'Creates custom analytics dashboards'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['analytics', 'dashboards'],
        },
    },

    // ==========================================================================
    // 7. EMAIL MARKETING (6 agents)
    // ==========================================================================

    email_campaign_manager: {
        id: 'email_campaign_manager',
        name: 'Email Campaign Manager',
        description: 'Manages email marketing campaigns',
        category: 'email_marketing',
        capabilities: [
            {
                id: 'email_campaigns',
                name: 'Email Campaigns',
                description: 'Creates and manages email campaigns'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['email', 'campaigns'],
        },
    },

    email_template_designer: {
        id: 'email_template_designer',
        name: 'Email Template Designer',
        description: 'Designs email templates',
        category: 'email_marketing',
        capabilities: [
            {
                id: 'email_design',
                name: 'Email Design',
                description: 'Designs responsive email templates'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['email', 'design'],
        },
    },

    email_deliverability_specialist: {
        id: 'email_deliverability_specialist',
        name: 'Email Deliverability Specialist',
        description: 'Optimizes email deliverability',
        category: 'email_marketing',
        capabilities: [
            {
                id: 'deliverability_optimization',
                name: 'Deliverability Optimization',
                description: 'Optimizes email deliverability rates'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['email', 'deliverability'],
        },
    },

    email_ab_testing_specialist: {
        id: 'email_ab_testing_specialist',
        name: 'Email A/B Testing Specialist',
        description: 'Conducts A/B testing for email campaigns',
        category: 'email_marketing',
        capabilities: [
            {
                id: 'email_ab_testing',
                name: 'Email A/B Testing',
                description: 'Designs and analyzes email A/B tests'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['email', 'testing'],
        },
    },

    newsletter_curator: {
        id: 'newsletter_curator',
        name: 'Newsletter Curator',
        description: 'Curates content for newsletters',
        category: 'email_marketing',
        capabilities: [
            {
                id: 'newsletter_curation',
                name: 'Newsletter Curation',
                description: 'Curates and creates newsletter content'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['email', 'newsletter'],
        },
    },

    email_list_manager: {
        id: 'email_list_manager',
        name: 'Email List Manager',
        description: 'Manages email lists and segmentation',
        category: 'email_marketing',
        capabilities: [
            {
                id: 'list_management',
                name: 'List Management',
                description: 'Manages email lists and segmentation'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['email', 'list-management'],
        },
    },

    // ==========================================================================
    // 8. CRM (6 agents)
    // ==========================================================================

    lead_qualifier: {
        id: 'lead_qualifier',
        name: 'Lead Qualification Agent',
        description: 'Qualifies and scores leads',
        category: 'crm',
        capabilities: [
            {
                id: 'lead_scoring',
                name: 'Lead Scoring',
                description: 'Scores and qualifies leads'
            }
        ],
        requiredTools: [],
        requiredServices: ['crm_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'active',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['crm', 'leads'],
        },
    },

    lead_nurturing_agent: {
        id: 'lead_nurturing_agent',
        name: 'Lead Nurturing Agent',
        description: 'Nurtures leads through the sales funnel',
        category: 'crm',
        capabilities: [
            {
                id: 'lead_nurturing',
                name: 'Lead Nurturing',
                description: 'Creates nurture campaigns for leads'
            }
        ],
        requiredTools: [],
        requiredServices: ['crm_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['crm', 'nurturing'],
        },
    },

    sales_assistant: {
        id: 'sales_assistant',
        name: 'Sales Assistant',
        description: 'Assists sales team with insights and automation',
        category: 'crm',
        capabilities: [
            {
                id: 'sales_assistance',
                name: 'Sales Assistance',
                description: 'Provides sales insights and automation'
            }
        ],
        requiredTools: [],
        requiredServices: ['crm_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['crm', 'sales'],
        },
    },

    customer_success_agent: {
        id: 'customer_success_agent',
        name: 'Customer Success Agent',
        description: 'Manages customer success and retention',
        category: 'crm',
        capabilities: [
            {
                id: 'customer_success',
                name: 'Customer Success',
                description: 'Manages customer onboarding and success'
            }
        ],
        requiredTools: [],
        requiredServices: ['crm_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['crm', 'customer-success'],
        },
    },

    churn_prediction_agent: {
        id: 'churn_prediction_agent',
        name: 'Churn Prediction Agent',
        description: 'Predicts and prevents customer churn',
        category: 'crm',
        capabilities: [
            {
                id: 'churn_prediction',
                name: 'Churn Prediction',
                description: 'Predicts customer churn risk'
            }
        ],
        requiredTools: [],
        requiredServices: ['crm_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['crm', 'churn', 'predictive'],
        },
    },

    upsell_crosssell_agent: {
        id: 'upsell_crosssell_agent',
        name: 'Upsell & Cross-sell Agent',
        description: 'Identifies upsell and cross-sell opportunities',
        category: 'crm',
        capabilities: [
            {
                id: 'upsell_crosssell',
                name: 'Upsell & Cross-sell',
                description: 'Identifies revenue expansion opportunities'
            }
        ],
        requiredTools: [],
        requiredServices: ['crm_api', 'ecommerce_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['crm', 'upsell', 'revenue'],
        },
    },

    // ==========================================================================
    // 9. E-COMMERCE (8 agents)
    // ==========================================================================

    product_recommender: {
        id: 'product_recommender',
        name: 'Product Recommendation Engine',
        description: 'Recommends products based on user behavior',
        category: 'ecommerce',
        capabilities: [
            {
                id: 'product_recommendations',
                name: 'Product Recommendations',
                description: 'Generates personalized product recommendations'
            }
        ],
        requiredTools: [],
        requiredServices: ['ecommerce_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'active',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['ecommerce', 'recommendations'],
        },
    },

    dynamic_pricing_optimizer: {
        id: 'dynamic_pricing_optimizer',
        name: 'Dynamic Pricing Optimizer',
        description: 'Optimizes product pricing dynamically',
        category: 'ecommerce',
        capabilities: [
            {
                id: 'dynamic_pricing',
                name: 'Dynamic Pricing',
                description: 'Optimizes pricing based on market conditions'
            }
        ],
        requiredTools: [],
        requiredServices: ['ecommerce_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['ecommerce', 'pricing'],
        },
    },

    inventory_management_agent: {
        id: 'inventory_management_agent',
        name: 'Inventory Management Agent',
        description: 'Manages inventory levels and forecasting',
        category: 'ecommerce',
        capabilities: [
            {
                id: 'inventory_management',
                name: 'Inventory Management',
                description: 'Manages inventory and forecasts demand'
            }
        ],
        requiredTools: [],
        requiredServices: ['ecommerce_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['ecommerce', 'inventory'],
        },
    },

    cart_abandonment_recovery: {
        id: 'cart_abandonment_recovery',
        name: 'Cart Abandonment Recovery',
        description: 'Recovers abandoned shopping carts',
        category: 'ecommerce',
        capabilities: [
            {
                id: 'cart_recovery',
                name: 'Cart Recovery',
                description: 'Creates cart recovery campaigns'
            }
        ],
        requiredTools: [],
        requiredServices: ['ecommerce_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['ecommerce', 'cart-recovery'],
        },
    },

    review_management_agent: {
        id: 'review_management_agent',
        name: 'Review Management Agent',
        description: 'Manages product reviews and ratings',
        category: 'ecommerce',
        capabilities: [
            {
                id: 'review_management',
                name: 'Review Management',
                description: 'Manages and responds to product reviews'
            }
        ],
        requiredTools: [],
        requiredServices: ['ecommerce_api'],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['ecommerce', 'reviews'],
        },
    },

    product_catalog_optimizer: {
        id: 'product_catalog_optimizer',
        name: 'Product Catalog Optimizer',
        description: 'Optimizes product catalog and organization',
        category: 'ecommerce',
        capabilities: [
            {
                id: 'catalog_optimization',
                name: 'Catalog Optimization',
                description: 'Optimizes product catalog structure'
            }
        ],
        requiredTools: [],
        requiredServices: ['ecommerce_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['ecommerce', 'catalog'],
        },
    },

    shipping_fulfillment_optimizer: {
        id: 'shipping_fulfillment_optimizer',
        name: 'Shipping & Fulfillment Optimizer',
        description: 'Optimizes shipping and fulfillment processes',
        category: 'ecommerce',
        capabilities: [
            {
                id: 'shipping_optimization',
                name: 'Shipping Optimization',
                description: 'Optimizes shipping costs and delivery times'
            }
        ],
        requiredTools: [],
        requiredServices: ['ecommerce_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['ecommerce', 'shipping'],
        },
    },

    marketplace_manager: {
        id: 'marketplace_manager',
        name: 'Marketplace Manager',
        description: 'Manages multi-marketplace presence',
        category: 'ecommerce',
        capabilities: [
            {
                id: 'marketplace_management',
                name: 'Marketplace Management',
                description: 'Manages listings across multiple marketplaces'
            }
        ],
        requiredTools: [],
        requiredServices: ['ecommerce_api'],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['ecommerce', 'marketplace'],
        },
    },

    // ==========================================================================
    // 10. DESIGN & CREATIVE (5 agents)
    // ==========================================================================

    ai_graphic_designer: {
        id: 'ai_graphic_designer',
        name: 'AI Graphic Designer',
        description: 'Creates graphics and visual designs',
        category: 'design',
        capabilities: [
            {
                id: 'graphic_design',
                name: 'Graphic Design',
                description: 'Creates custom graphics and designs'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['design', 'graphics'],
        },
    },

    banner_ad_designer: {
        id: 'banner_ad_designer',
        name: 'Banner Ad Designer',
        description: 'Designs banner ads for advertising',
        category: 'design',
        capabilities: [
            {
                id: 'banner_design',
                name: 'Banner Design',
                description: 'Creates banner ad designs'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['design', 'ads'],
        },
    },

    social_media_graphics_designer: {
        id: 'social_media_graphics_designer',
        name: 'Social Media Graphics Designer',
        description: 'Creates social media graphics',
        category: 'design',
        capabilities: [
            {
                id: 'social_graphics',
                name: 'Social Graphics',
                description: 'Creates platform-specific social media graphics'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['design', 'social-media'],
        },
    },

    logo_designer: {
        id: 'logo_designer',
        name: 'Logo Designer',
        description: 'Creates logo designs',
        category: 'design',
        capabilities: [
            {
                id: 'logo_design',
                name: 'Logo Design',
                description: 'Creates custom logo designs'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['design', 'branding'],
        },
    },

    infographic_designer: {
        id: 'infographic_designer',
        name: 'Infographic Designer',
        description: 'Creates data visualizations and infographics',
        category: 'design',
        capabilities: [
            {
                id: 'infographic_design',
                name: 'Infographic Design',
                description: 'Creates data-driven infographics'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['design', 'infographics'],
        },
    },

    // ==========================================================================
    // 11. AUTOMATION & WORKFLOWS (4 agents)
    // ==========================================================================

    workflow_automation_specialist: {
        id: 'workflow_automation_specialist',
        name: 'Workflow Automation Specialist',
        description: 'Automates business workflows',
        category: 'automation',
        capabilities: [
            {
                id: 'workflow_automation',
                name: 'Workflow Automation',
                description: 'Creates automated business workflows'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['automation', 'workflows'],
        },
    },

    task_scheduling_agent: {
        id: 'task_scheduling_agent',
        name: 'Task Scheduling Agent',
        description: 'Schedules and manages tasks',
        category: 'automation',
        capabilities: [
            {
                id: 'task_scheduling',
                name: 'Task Scheduling',
                description: 'Schedules and automates tasks'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['automation', 'scheduling'],
        },
    },

    automated_report_generator: {
        id: 'automated_report_generator',
        name: 'Automated Report Generator',
        description: 'Generates automated reports',
        category: 'automation',
        capabilities: [
            {
                id: 'report_generation',
                name: 'Report Generation',
                description: 'Generates automated business reports'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['automation', 'reporting'],
        },
    },

    integration_manager: {
        id: 'integration_manager',
        name: 'Integration Manager',
        description: 'Manages third-party integrations',
        category: 'automation',
        capabilities: [
            {
                id: 'integration_management',
                name: 'Integration Management',
                description: 'Manages API integrations and data sync'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['automation', 'integrations'],
        },
    },

    // ==========================================================================
    // 12. RESEARCH & ANALYSIS (3 agents)
    // ==========================================================================

    market_research_agent: {
        id: 'market_research_agent',
        name: 'Market Research Agent',
        description: 'Conducts market research and analysis',
        category: 'research',
        capabilities: [
            {
                id: 'market_research',
                name: 'Market Research',
                description: 'Conducts comprehensive market research'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['research', 'market'],
        },
    },

    competitor_research_agent: {
        id: 'competitor_research_agent',
        name: 'Competitor Research Agent',
        description: 'Researches competitor strategies',
        category: 'research',
        capabilities: [
            {
                id: 'competitor_research',
                name: 'Competitor Research',
                description: 'Researches competitor strategies and tactics'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['research', 'competitive'],
        },
    },

    trend_analysis_agent: {
        id: 'trend_analysis_agent',
        name: 'Trend Analysis Agent',
        description: 'Analyzes market trends and patterns',
        category: 'research',
        capabilities: [
            {
                id: 'trend_analysis',
                name: 'Trend Analysis',
                description: 'Identifies and analyzes market trends'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['research', 'trends'],
        },
    },

    // ==========================================================================
    // 13. CUSTOMER SUPPORT (4 agents)
    // ==========================================================================

    customer_support_chatbot: {
        id: 'customer_support_chatbot',
        name: 'Customer Support Chatbot',
        description: 'Provides automated customer support',
        category: 'customer_support',
        capabilities: [
            {
                id: 'customer_support',
                name: 'Customer Support',
                description: 'Provides automated customer support responses'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['support', 'chatbot'],
        },
    },

    support_ticket_classifier: {
        id: 'support_ticket_classifier',
        name: 'Support Ticket Classifier',
        description: 'Classifies and routes support tickets',
        category: 'customer_support',
        capabilities: [
            {
                id: 'ticket_classification',
                name: 'Ticket Classification',
                description: 'Classifies and prioritizes support tickets'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['support', 'tickets'],
        },
    },

    knowledge_base_manager: {
        id: 'knowledge_base_manager',
        name: 'Knowledge Base Manager',
        description: 'Manages knowledge base content',
        category: 'customer_support',
        capabilities: [
            {
                id: 'knowledge_management',
                name: 'Knowledge Management',
                description: 'Creates and manages knowledge base articles'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'standard',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['support', 'knowledge-base'],
        },
    },

    customer_sentiment_analyzer: {
        id: 'customer_sentiment_analyzer',
        name: 'Customer Sentiment Analyzer',
        description: 'Analyzes customer sentiment',
        category: 'customer_support',
        capabilities: [
            {
                id: 'sentiment_analysis',
                name: 'Sentiment Analysis',
                description: 'Analyzes customer sentiment from interactions'
            }
        ],
        requiredTools: [],
        requiredServices: [],
        requiredAPIs: [],
        costTier: 'premium',
        permissions: [],
        status: 'inactive',
        metadata: {
            version: '1.0.0',
            author: 'BizOSaaS',
            lastUpdated: '2024-12-04',
            tags: ['support', 'sentiment', 'analytics'],
        },
    },
};

// ============================================================================
// Helper Functions
// ============================================================================

export function getAgentById(agentId: string): AIAgent | undefined {
    return AGENT_REGISTRY[agentId];
}

export function getAgentsByCategory(category: AgentCategory): AIAgent[] {
    return Object.values(AGENT_REGISTRY).filter(agent => agent.category === category);
}

export function getActiveAgents(): AIAgent[] {
    return Object.values(AGENT_REGISTRY).filter(agent => agent.status === 'active');
}

export function getAllAgents(): AIAgent[] {
    return Object.values(AGENT_REGISTRY);
}

export function searchAgents(query: string): AIAgent[] {
    const lowerQuery = query.toLowerCase();
    return Object.values(AGENT_REGISTRY).filter(agent =>
        agent.name.toLowerCase().includes(lowerQuery) ||
        agent.description.toLowerCase().includes(lowerQuery) ||
        agent.metadata.tags.some(tag => tag.includes(lowerQuery))
    );
}
