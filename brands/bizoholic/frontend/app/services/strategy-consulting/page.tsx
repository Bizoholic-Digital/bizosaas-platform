"use client"

import ServicePageTemplate from '@/components/ServicePageTemplate'
import { Lightbulb, Target, TrendingUp, Users, BarChart, Compass, Map, Rocket } from 'lucide-react'

export default function StrategyConsultingPage() {
    return (
        <ServicePageTemplate
            serviceName="Strategy Consulting"
            serviceDescription="Transform your marketing with expert strategy consulting backed by AI-powered market analysis, competitive intelligence, and data-driven recommendations for sustainable growth."
            heroIcon={Lightbulb}
            ctaPrimary="Get Free Strategy Session"
            ctaSecondary="View Case Studies"
            rating="4.9/5 Rating"
            statsText="500+ Strategies Delivered"
            heroHighlights={[
                'Data-driven strategic planning',
                'Competitive intelligence included',
                'Quarterly strategy reviews'
            ]}

            featuresTitle="Expert Strategy Consulting Services"
            featuresDescription="Our strategists combine years of experience with AI-powered insights to create winning marketing strategies tailored to your business."
            features={[
                {
                    icon: Target,
                    title: 'Market Positioning',
                    description: 'Define your unique value proposition and position your brand for maximum market impact.'
                },
                {
                    icon: Compass,
                    title: 'Growth Planning',
                    description: 'Create comprehensive growth roadmaps with clear milestones, tactics, and success metrics.'
                },
                {
                    icon: BarChart,
                    title: 'Competitive Analysis',
                    description: 'AI-powered competitive intelligence to identify opportunities and stay ahead of competitors.'
                },
                {
                    icon: Map,
                    title: 'Channel Strategy',
                    description: 'Optimize your marketing mix and allocate budget across channels for maximum ROI.'
                }
            ]}

            campaignTitle="Strategic Solutions We Provide"
            campaignDescription="From market entry to scaling, we provide strategic guidance for every stage of your business growth."
            campaignTypes={[
                {
                    name: 'Go-to-Market Strategy',
                    description: 'Launch new products or enter new markets with comprehensive GTM strategies',
                    results: ['Market analysis', 'Launch roadmap', '90-day action plan']
                },
                {
                    name: 'Growth Strategy',
                    description: 'Scale your business with data-driven growth strategies and tactics',
                    results: ['Revenue modeling', 'Channel optimization', 'Scalable systems']
                },
                {
                    name: 'Brand Strategy',
                    description: 'Build a powerful brand that resonates with your target audience',
                    results: ['Brand positioning', 'Messaging framework', 'Visual identity']
                },
                {
                    name: 'Digital Transformation',
                    description: 'Modernize your marketing with AI and automation strategies',
                    results: ['Technology roadmap', 'Process optimization', 'Change management']
                }
            ]}

            benefitsTitle="Why Our AI + Expert Strategy Works"
            benefitsDescription="Traditional consulting relies on outdated playbooks and gut feelings. Our strategists use AI to analyze market data, competitive landscapes, and customer behavior to create strategies grounded in real-time insights and proven frameworks."
            benefits={[
                'Get actionable strategies, not just reports',
                'Make decisions based on data, not assumptions',
                'Identify opportunities competitors miss',
                'Avoid costly strategic mistakes',
                'Accelerate growth with proven frameworks',
                'Ongoing support and strategy refinement'
            ]}
            comparisonTitle="AI-Powered vs Traditional Consulting"
            comparisonItems={[
                { label: 'Market Analysis', value: 'Real-Time' },
                { label: 'Insights', value: 'Data-Driven' },
                { label: 'Recommendations', value: 'Actionable' },
                { label: 'Support', value: 'Ongoing' }
            ]}

            testimonials={[
                {
                    name: 'Thomas Anderson',
                    role: 'CEO',
                    company: 'InnovateTech',
                    content: 'The strategy they developed helped us 3x revenue in 18 months. The AI insights revealed opportunities we never would have found.',
                    rating: 5
                },
                {
                    name: 'Rachel Green',
                    role: 'CMO',
                    company: 'GrowthVentures',
                    content: 'Finally, a consulting firm that delivers actionable strategies, not just PowerPoint decks. Our market share increased 40% in one year.',
                    rating: 5
                },
                {
                    name: 'David Park',
                    role: 'Founder',
                    company: 'StartupScale',
                    content: 'Their go-to-market strategy was spot-on. We launched successfully in 3 new markets and exceeded revenue targets by 150%.',
                    rating: 5
                }
            ]}

            pricingTitle="Transparent Strategy Consulting Pricing"
            pricingDescription="No hidden fees. All plans include AI-powered insights + Expert strategist guidance."
            pricing={[
                {
                    name: 'Strategy Sprint',
                    price: '$4,997',
                    period: '/one-time',
                    description: 'Perfect for focused initiatives',
                    subscribers: '2-week engagement',
                    features: [
                        'Comprehensive market analysis',
                        'Competitive intelligence',
                        'Strategic recommendations',
                        'Action plan & roadmap',
                        '30-day email support'
                    ]
                },
                {
                    name: 'Growth Partner',
                    price: '$9,997',
                    period: '/quarter',
                    description: 'Ideal for ongoing growth',
                    subscribers: '3-month engagement',
                    features: [
                        'Quarterly strategy development',
                        'Monthly strategy sessions',
                        'Ongoing market monitoring',
                        'Performance tracking',
                        'Unlimited email support',
                        'Dedicated strategist'
                    ],
                    popular: true
                },
                {
                    name: 'Strategic Advisor',
                    price: '$29,997',
                    period: '/year',
                    description: 'For long-term partnership',
                    subscribers: '12-month engagement',
                    features: [
                        'Annual strategic planning',
                        'Bi-weekly strategy calls',
                        'Full market intelligence',
                        'Executive presentations',
                        'Priority support',
                        'Senior strategist team'
                    ]
                }
            ]}

            faqs={[
                {
                    question: 'How is this different from traditional consulting?',
                    answer: 'Traditional consulting delivers reports. We deliver actionable strategies with ongoing support. Our AI provides real-time market insights that traditional consultants can\'t access, and we stay engaged to ensure successful implementation.'
                },
                {
                    question: 'What industries do you work with?',
                    answer: 'We work with B2B and B2C companies across technology, e-commerce, SaaS, professional services, healthcare, finance, and more. Our AI-powered approach adapts to any industry.'
                },
                {
                    question: 'How long does strategy development take?',
                    answer: 'Strategy Sprint delivers in 2 weeks. Growth Partner provides quarterly strategies. Strategic Advisor includes annual planning with ongoing refinement. Timeline depends on scope and complexity.'
                },
                {
                    question: 'Do you help with implementation?',
                    answer: 'Yes, all plans include implementation guidance. Growth Partner and Strategic Advisor plans include hands-on support to ensure successful execution of strategies.'
                },
                {
                    question: 'What if the strategy doesn\'t work?',
                    answer: 'We monitor performance and refine strategies based on results. Growth Partner and Strategic Advisor plans include ongoing optimization to ensure you achieve your goals.'
                },
                {
                    question: 'Can you work with our existing team?',
                    answer: 'Absolutely. We collaborate with your team, provide training, and transfer knowledge so your team can execute strategies effectively. We\'re partners, not replacements.'
                }
            ]}

            ctaTitle="Ready to Build a Winning Strategy?"
            ctaDescription="Get your free strategy session and discover how AI-powered insights can accelerate your growth."
            ctaButtons={[
                { text: 'Get Free Strategy Session', variant: 'secondary' },
                { text: 'View Case Studies', variant: 'outline' }
            ]}
        />
    )
}
