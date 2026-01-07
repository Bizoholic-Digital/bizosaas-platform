import { create } from 'zustand'

export interface Agent {
    id: string
    name: string
    description: string
    status: 'active' | 'inactive' | 'error' | 'starting'
    domain: string
    team: string
    type: string
    performance: number // 0-100
    lastActive: string
    tools?: string[]
    tasks?: string[]
    implementationStatus: 'implemented' | 'planned' | 'skeleton'
}

export interface AgentStats {
    total: number
    active: number
    inactive: number
    error: number
    performance: number
}

interface AgentStore {
    agents: Agent[]
    isLoading: boolean
    error: string | null
    fetchAgents: () => Promise<void>
    getAgentStats: () => AgentStats
}

// Comprehensive agent data based on audit
const MOCK_AGENTS: Agent[] = [
    // 1. Marketing & Advertising (15 total)
    {
        id: 'mkt-1',
        name: 'Campaign Manager',
        description: 'Strategic oversight and budget allocation across all channels',
        status: 'inactive',
        domain: 'Marketing',
        team: 'Marketing & Advertising',
        type: 'Strategic',
        performance: 0,
        lastActive: 'Scheduled',
        implementationStatus: 'planned',
        tools: ['Google Ads API', 'Meta API'],
        tasks: ['Budget Optimization', 'Channel Allocation']
    },
    {
        id: 'mkt-2',
        name: 'Ad Copywriter',
        description: 'AI-powered generation of high-converting ad copy',
        status: 'active',
        domain: 'Marketing',
        team: 'Marketing & Advertising',
        type: 'Generative',
        performance: 94,
        lastActive: '2 mins ago',
        implementationStatus: 'skeleton',
        tools: ['OpenAI', 'Anthropic'],
        tasks: ['Ad Copy Generation', 'A/B Test Copy']
    },
    {
        id: 'mkt-3',
        name: 'Google Ads Specialist',
        description: 'Specialized optimization for search and display ads',
        status: 'inactive',
        domain: 'Marketing',
        team: 'Marketing & Advertising',
        type: 'Optimization',
        performance: 0,
        lastActive: 'Unprovisioned',
        implementationStatus: 'planned',
        tools: ['Google Ads API'],
        tasks: ['Keyword Bidding', 'Ad Placement']
    },
    {
        id: 'mkt-4',
        name: 'Meta Ads Specialist',
        description: 'Optimization for Facebook and Instagram advertising',
        status: 'inactive',
        domain: 'Marketing',
        team: 'Marketing & Advertising',
        type: 'Optimization',
        performance: 0,
        lastActive: 'Unprovisioned',
        implementationStatus: 'planned',
        tools: ['Meta Ads API'],
        tasks: ['Audience Targeting', 'Visual Asset Testing']
    },
    {
        id: 'mkt-5',
        name: 'LinkedIn Ads Specialist',
        description: 'B2B lead generation via LinkedIn',
        status: 'inactive',
        domain: 'Marketing',
        team: 'Marketing & Advertising',
        type: 'Optimization',
        performance: 0,
        lastActive: 'Unprovisioned',
        implementationStatus: 'planned',
        tools: ['LinkedIn Ads API'],
        tasks: ['Professional Targeting', 'Sponsored Content']
    },
    ...Array.from({ length: 10 }, (_, i) => ({
        id: `mkt-spec-${i + 6}`,
        name: `${['TikTok', 'Twitter', 'Pinterest', 'Reddit', 'Snapchat', 'Native', 'Programmatic', 'Affiliate', 'Influencer', 'Local'][i]} Ads Specialist`,
        description: 'Targeted ad optimization for specific platform ecosystems',
        status: 'inactive' as const,
        domain: 'Marketing',
        team: 'Marketing & Advertising',
        type: 'Specialist',
        performance: 0,
        lastActive: 'Unprovisioned',
        implementationStatus: 'planned' as const,
        tools: ['Platform API'],
        tasks: ['Ad Placement', 'Contextual Targeting']
    })),

    // 2. Content Creation (12 total)
    {
        id: 'cnt-1',
        name: 'Blog Writer',
        description: 'SEO-focused long-form article generation',
        status: 'active',
        domain: 'Content',
        team: 'Content Creation',
        type: 'Generative',
        performance: 88,
        lastActive: '1 hour ago',
        implementationStatus: 'skeleton',
        tools: ['WordPress API', 'Ghost'],
        tasks: ['Article Generation', 'Post Scheduling']
    },
    {
        id: 'cnt-2',
        name: 'Social Content Creator',
        description: 'Engagement-driven short-form content creation',
        status: 'active',
        domain: 'Content',
        team: 'Content Creation',
        type: 'Generative',
        performance: 91,
        lastActive: '15 mins ago',
        implementationStatus: 'skeleton',
        tools: ['Canva API', 'Buffer'],
        tasks: ['Caption Writing', 'Image Prompting']
    },
    {
        id: 'cnt-3',
        name: 'Video Script Writer',
        description: 'Structured scripts for YouTube, TikTok, and Reels',
        status: 'inactive',
        domain: 'Content',
        team: 'Content Creation',
        type: 'Generative',
        performance: 0,
        lastActive: 'Unprovisioned',
        implementationStatus: 'planned',
        tools: ['YouTube Data API'],
        tasks: ['Script Outlining', 'Hook Generation']
    },
    {
        id: 'cnt-4',
        name: 'Email Copywriter',
        description: 'Persuasive copy for newsletters and sales sequences',
        status: 'inactive',
        domain: 'Content',
        team: 'Content Creation',
        type: 'Generative',
        performance: 0,
        lastActive: 'Unprovisioned',
        implementationStatus: 'planned',
        tools: ['Resend API', 'Mailchimp'],
        tasks: ['Sequence Planning', 'Subject Line A/B Testing']
    },
    ...Array.from({ length: 8 }, (_, i) => ({
        id: `cnt-spec-${i + 5}`,
        name: `${['Press Release', 'White Paper', 'Case Study', 'Product Copy', 'Landing Page', 'Ad Creative', 'Script Doctor', 'Brand Guide'][i]} Specialist`,
        description: 'High-quality topical content generation',
        status: 'inactive' as const,
        domain: 'Content',
        team: 'Content Creation',
        type: 'Generative',
        performance: 0,
        lastActive: 'Unprovisioned',
        implementationStatus: 'planned' as const,
        tools: ['OpenAI'],
        tasks: ['Specialized Drafting', 'Tone Adjustment']
    })),

    // 3. SEO Team (10 total)
    {
        id: 'seo-1',
        name: 'SEO Strategist',
        description: 'Comprehensive keyword and growth strategy',
        status: 'active',
        domain: 'SEO',
        team: 'SEO Team',
        type: 'Analytical',
        performance: 92,
        lastActive: '10 mins ago',
        implementationStatus: 'skeleton',
        tools: ['SEMrush API', 'Ahrefs'],
        tasks: ['Strategy Mapping', 'Competitor Analysis']
    },
    {
        id: 'seo-2',
        name: 'Keyword Researcher',
        description: 'Deep-dive keyword discovery and intent mapping',
        status: 'active',
        domain: 'SEO',
        team: 'SEO Team',
        type: 'Analytical',
        performance: 95,
        lastActive: 'Just now',
        implementationStatus: 'skeleton',
        tools: ['Google Keyword Planner', 'Ubersuggest'],
        tasks: ['Intent Extraction', 'Volume Analysis']
    },
    {
        id: 'seo-3',
        name: 'Technical SEO Specialist',
        description: 'Site structure and performance auditing',
        status: 'active',
        domain: 'SEO',
        team: 'SEO Team',
        type: 'Analytical',
        performance: 89,
        lastActive: '2 days ago',
        implementationStatus: 'skeleton',
        tools: ['Google Search Console', 'Screaming Frog'],
        tasks: ['Crawl Optimization', 'Schema Markup']
    },
    ...Array.from({ length: 7 }, (_, i) => ({
        id: `seo-spec-${i + 4}`,
        name: `${['Local SEO', 'Backlink', 'Content Optimization', 'Mobile SEO', 'Multilingual', 'Voice Search', 'Video SEO'][i]} Specialist`,
        description: 'Targeted SEO optimization for technical sub-domains',
        status: 'inactive' as const,
        domain: 'SEO',
        team: 'SEO Team',
        type: 'Specialist',
        performance: 0,
        lastActive: 'Unprovisioned',
        implementationStatus: 'planned' as const,
        tools: ['Search Console'],
        tasks: ['Technical Audit', 'Ranking Track']
    })),

    // 4. E-commerce Team (8 total)
    {
        id: 'ecom-1',
        name: 'Amazon Optimization',
        description: 'Buy Box success and listing performance',
        status: 'active',
        domain: 'E-commerce',
        team: 'E-commerce Team',
        type: 'Optimization',
        performance: 95,
        lastActive: 'Just now',
        implementationStatus: 'skeleton',
        tools: ['Amazon SP-API'],
        tasks: ['Buy Box Monitoring', 'Competitor Price Analysis']
    },
    {
        id: 'ecom-2',
        name: 'Inventory Manager',
        description: 'Stock level optimization and fulfillment sync',
        status: 'active',
        domain: 'E-commerce',
        team: 'E-commerce Team',
        type: 'Operational',
        performance: 98,
        lastActive: 'Just now',
        implementationStatus: 'implemented',
        tools: ['Shopify', 'Amazon Seller'],
        tasks: ['Low Stock Alerts', 'Fulfillment Sync']
    },
    {
        id: 'ecom-3',
        name: 'Dynamic Pricing',
        description: 'Real-time price adjustments for margin maximization',
        status: 'active',
        domain: 'E-commerce',
        team: 'E-commerce Team',
        type: 'Optimization',
        performance: 92,
        lastActive: '5 mins ago',
        implementationStatus: 'skeleton',
        tools: ['Price Scrapers'],
        tasks: ['Margin Tracking', 'Competitor Matching']
    },
    ...Array.from({ length: 5 }, (_, i) => ({
        id: `ecom-spec-${i + 4}`,
        name: `${['Recommendation', 'Cart Recovery', 'Catalog Manager', 'Shipping Optimizer', 'Returns Agent'][i]} Specialist`,
        description: 'Specific e-commerce operational agent',
        status: 'inactive' as const,
        domain: 'E-commerce',
        team: 'E-commerce Team',
        type: 'Operational',
        performance: 0,
        lastActive: 'Unprovisioned',
        implementationStatus: 'planned' as const,
        tools: ['Shopify API'],
        tasks: ['Workflow Trigger', 'Data Sync']
    })),

    // 5. Analytics & Insights (8 total)
    {
        id: 'ana-1',
        name: 'Performance Analyst',
        description: 'Cross-platform metric tracking and synthesis',
        status: 'active',
        domain: 'Analytics',
        team: 'Analytics & Insights',
        type: 'Analytical',
        performance: 91,
        lastActive: '5 mins ago',
        implementationStatus: 'skeleton',
        tools: ['GA4', 'Mixpanel'],
        tasks: ['Data Synthesis', 'Traffic Attribution']
    },
    {
        id: 'ana-2',
        name: 'ROI Analysis Agent',
        description: 'Financial performance and contribution margin tracking',
        status: 'inactive',
        domain: 'Analytics',
        team: 'Analytics & Insights',
        type: 'Analytical',
        performance: 0,
        lastActive: 'Unprovisioned',
        implementationStatus: 'skeleton',
        tools: ['Stripe API', 'Quickbooks'],
        tasks: ['CPA Calculation', 'Revenue Attribution']
    },
    {
        id: 'ana-3',
        name: 'Churn Predictor',
        description: 'Behavioral analysis to prevent customer churn',
        status: 'active',
        domain: 'Analytics',
        team: 'Analytics & Insights',
        type: 'Data',
        performance: 87,
        lastActive: '1 day ago',
        implementationStatus: 'skeleton',
        tools: ['Prophet', 'Custom ML'],
        tasks: ['Risk Scoring', 'Retention Targeting']
    },
    ...Array.from({ length: 5 }, (_, i) => ({
        id: `ana-spec-${i + 4}`,
        name: `${['Visualization', 'Anomaly Detector', 'Cohort Analyst', 'Funnel Auditor', 'Report Generator'][i]} Agent`,
        description: 'Specialized data synthesis and reporting',
        status: 'active' as const,
        domain: 'Analytics',
        team: 'Analytics & Insights',
        type: 'Specialist',
        performance: 99,
        lastActive: 'Just now',
        implementationStatus: 'skeleton' as const,
        tools: ['Recharts'],
        tasks: ['Metric Drill-down', 'PDF Export']
    })),

    // 6. CRM & Sales (7 total)
    {
        id: 'crm-1',
        name: 'Contact Intelligence',
        description: 'Automated data enrichment and stakeholder mapping',
        status: 'active',
        domain: 'CRM',
        team: 'CRM & Sales',
        type: 'Data',
        performance: 89,
        lastActive: '12 mins ago',
        implementationStatus: 'skeleton',
        tools: ['Clearbit', 'Apollo'],
        tasks: ['Profile Enrichment', 'Org Chart Mapping']
    },
    {
        id: 'crm-2',
        name: 'Lead Scoring',
        description: 'Behavioral-based lead qualification and priority',
        status: 'active',
        domain: 'CRM',
        team: 'CRM & Sales',
        type: 'Analytical',
        performance: 94,
        lastActive: 'Just now',
        implementationStatus: 'skeleton',
        tools: ['Zoho CRM', 'Salesforce'],
        tasks: ['Scoring Update', 'Tagging']
    },
    ...Array.from({ length: 5 }, (_, i) => ({
        id: `crm-spec-${i + 3}`,
        name: `${['Sales Assistant', 'Sentiment Analyst', 'Escalation Bot', 'Meeting Setter', 'Renewal Bot'][i]} Agent`,
        description: 'Task-driven CRM agent for sales acceleration',
        status: 'inactive' as const,
        domain: 'CRM',
        team: 'CRM & Sales',
        type: 'Specialist',
        performance: 0,
        lastActive: 'Unprovisioned',
        implementationStatus: 'skeleton' as const,
        tools: ['HubSpot'],
        tasks: ['Activity Log', 'Outreach']
    })),

    // 7. Operations & Compliance (8 total)
    {
        id: 'ops-1',
        name: 'Customer Support Bot',
        description: 'First-response ticket triage and AI resolution',
        status: 'active',
        domain: 'Operations',
        team: 'Operations & Compliance',
        type: 'Conversational',
        performance: 87,
        lastActive: 'Just now',
        implementationStatus: 'skeleton',
        tools: ['HelpScout', 'Zendesk'],
        tasks: ['Intent Detection', 'Macro Suggestion']
    },
    {
        id: 'ops-2',
        name: 'Compliance Auditor',
        description: 'Continuous monitoring of security and regulatory logs',
        status: 'active',
        domain: 'Operations',
        team: 'Operations & Compliance',
        type: 'Security',
        performance: 99,
        lastActive: 'Just now',
        implementationStatus: 'skeleton',
        tools: ['Datadog', 'Snyk'],
        tasks: ['Vulnerability Scan', 'Policy Enforcement']
    },
    ...Array.from({ length: 6 }, (_, i) => ({
        id: `ops-spec-${i + 3}`,
        name: `${['Automation Spec', 'QA Analyst', 'Incident Manager', 'Knowledge Base', 'Resource Monitor', 'Process Auditor'][i]} Agent`,
        description: 'Backend operations and systems management',
        status: 'active' as const,
        domain: 'Operations',
        team: 'Operations & Compliance',
        type: 'Specialist',
        performance: 95,
        lastActive: 'Just now',
        implementationStatus: 'skeleton' as const,
        tools: ['Temporal'],
        tasks: ['Workflow Monitoring', 'Trace Analysis']
    })),

    // 8. Gamification & Engagement (5 total)
    {
        id: 'gam-1',
        name: 'Gamification Orchestrator',
        description: 'Central strategy for achievements and behavioral loops',
        status: 'active',
        domain: 'Platform',
        team: 'Gamification & Engagement',
        type: 'Orchestration',
        performance: 99,
        lastActive: 'Just now',
        implementationStatus: 'implemented',
        tools: ['Platform DB'],
        tasks: ['Loop Management', 'Incentive Sync']
    },
    {
        id: 'gam-2',
        name: 'Referral Manager',
        description: 'Optimizing viral growth and referral attribution',
        status: 'active',
        domain: 'Platform',
        team: 'Gamification & Engagement',
        type: 'Growth',
        performance: 92,
        lastActive: '1 hour ago',
        implementationStatus: 'implemented',
        tools: ['Referral API'],
        tasks: ['Attribution Check', 'Reward Issuance']
    },
    ...Array.from({ length: 3 }, (_, i) => ({
        id: `gam-spec-${i + 3}`,
        name: `${['Achievement Bot', 'Leaderboard Sys', 'Showcase Gen'][i]} Agent`,
        description: 'Engagement-focused platform agent',
        status: 'active' as const,
        domain: 'Platform',
        team: 'Gamification & Engagement',
        type: 'Operational',
        performance: 98,
        lastActive: 'Just now',
        implementationStatus: 'implemented' as const,
        tools: ['Redis'],
        tasks: ['Rank Calc', 'Milestone Check']
    })),

    // 9. Platform Core (10 total)
    {
        id: 'core-1',
        name: 'Personal AI Coordinator',
        description: 'Master orchestrator for all user-agent interactions',
        status: 'active',
        domain: 'Platform',
        team: 'Platform Core',
        type: 'Orchestration',
        performance: 97,
        lastActive: 'Just now',
        implementationStatus: 'implemented',
        tools: ['CrewAI', 'LangChain'],
        tasks: ['Agent Routing', 'Task Decomposition']
    },
    {
        id: 'core-2',
        name: 'Workflow Specialist',
        description: 'Ensures long-running task persistence and fault tolerance',
        status: 'active',
        domain: 'Platform',
        team: 'Platform Core',
        type: 'Operational',
        performance: 100,
        lastActive: 'Just now',
        implementationStatus: 'implemented',
        tools: ['Temporal'],
        tasks: ['Retry Orchestration', 'State Sync']
    },
    ...Array.from({ length: 38 }, (_, i) => ({
        id: `gen-${i + 1}`,
        name: `Niche Specialist Agent ${i + 41}`,
        description: 'Deeply targeted agent for platform specialization',
        status: 'inactive' as const,
        domain: 'Platform',
        team: 'Marketing & Advertising',
        type: 'Specialist',
        performance: 0,
        lastActive: 'Unprovisioned',
        implementationStatus: 'planned' as const,
        tools: [],
        tasks: []
    }))
]

export const useAgentStore = create<AgentStore>((set, get) => ({
    agents: [],
    isLoading: false,
    error: null,

    fetchAgents: async () => {
        set({ isLoading: true })
        try {
            // TODO: Replace with actual API call
            await new Promise(resolve => setTimeout(resolve, 1000))
            set({ agents: MOCK_AGENTS, isLoading: false })
        } catch (error) {
            set({ error: 'Failed to fetch agents', isLoading: false })
        }
    },

    getAgentStats: () => {
        const { agents } = get()
        const total = agents.length
        if (total === 0) {
            return { total: 0, active: 0, inactive: 0, error: 0, performance: 0 }
        }

        const active = agents.filter(a => a.status === 'active').length
        const inactive = agents.filter(a => a.status === 'inactive').length
        const error = agents.filter(a => a.status === 'error').length

        // Calculate average performance
        const totalPerformance = agents.reduce((sum, agent) => sum + agent.performance, 0)
        const avgPerformance = Math.round(totalPerformance / total)

        return {
            total,
            active,
            inactive,
            error,
            performance: avgPerformance
        }
    }
}))
