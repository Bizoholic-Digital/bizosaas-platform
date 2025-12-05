"use client"

import ServicePageTemplate from '@/components/ServicePageTemplate'
import { Zap, Workflow, GitBranch, Mail, Users, Clock, Target, RefreshCw } from 'lucide-react'

export default function MarketingAutomationPage() {
    return (
        <ServicePageTemplate
            serviceName="Marketing Automation"
            serviceDescription="Build intelligent marketing workflows that nurture leads, personalize customer experiences, and drive conversions automatically - powered by AI with expert strategy guidance."
            heroIcon={Zap}
            ctaPrimary="Get Free Automation Audit"
            ctaSecondary="View Workflow Examples"
            rating="4.9/5 Rating"
            statsText="5M+ Workflows Automated"
            heroHighlights={[
                '80% time savings on repetitive tasks',
                'Personalized at scale',
                '24/7 automated nurturing'
            ]}

            featuresTitle="Intelligent Marketing Automation Features"
            featuresDescription="Our AI-powered platform creates sophisticated automation workflows that adapt to customer behavior and optimize for conversions."
            features={[
                {
                    icon: Workflow,
                    title: 'Smart Workflows',
                    description: 'Build complex automation sequences that adapt based on customer actions and preferences.'
                },
                {
                    icon: GitBranch,
                    title: 'Behavioral Triggers',
                    description: 'Automatically respond to customer behavior with personalized messages and offers.'
                },
                {
                    icon: Users,
                    title: 'Lead Scoring',
                    description: 'AI automatically scores and prioritizes leads based on engagement and conversion likelihood.'
                },
                {
                    icon: RefreshCw,
                    title: 'Continuous Optimization',
                    description: 'Workflows automatically optimize based on performance data and AI recommendations.'
                }
            ]}

            campaignTitle="Automation Workflows We Build"
            campaignDescription="From lead nurturing to customer retention, we create automated workflows for every stage of the customer journey."
            campaignTypes={[
                {
                    name: 'Lead Nurturing',
                    description: 'Automatically nurture leads with personalized content until they\'re sales-ready',
                    results: ['60% more qualified leads', '45% faster sales cycle', '3x conversion rate']
                },
                {
                    name: 'Onboarding Sequences',
                    description: 'Welcome and educate new customers with automated onboarding flows',
                    results: ['85% completion rate', '50% faster activation', '40% higher retention']
                },
                {
                    name: 'Re-engagement Campaigns',
                    description: 'Win back inactive customers with intelligent re-engagement automation',
                    results: ['35% reactivation rate', '25% revenue recovery', 'Automated triggers']
                },
                {
                    name: 'Cross-sell & Upsell',
                    description: 'Increase customer lifetime value with automated product recommendations',
                    results: ['45% upsell rate', '30% revenue increase', 'AI-powered recommendations']
                }
            ]}

            benefitsTitle="Why Our AI + Expert Automation Works"
            benefitsDescription="Traditional automation is rigid and generic. Our AI creates dynamic workflows that adapt to each customer's behavior, preferences, and stage in the journey while expert strategists ensure alignment with your business goals."
            benefits={[
                'Save 20+ hours per week on manual tasks',
                'Nurture leads automatically 24/7',
                'Personalize at scale without manual effort',
                'Increase conversion rates by 200%+',
                'Improve customer retention by 40%',
                'Scale marketing without scaling headcount'
            ]}
            comparisonTitle="AI vs Traditional Automation"
            comparisonItems={[
                { label: 'Personalization', value: 'Dynamic' },
                { label: 'Optimization', value: 'Continuous' },
                { label: 'Lead Scoring', value: 'AI-Powered' },
                { label: 'Adaptability', value: 'Real-Time' }
            ]}

            testimonials={[
                {
                    name: 'Jennifer Lee',
                    role: 'VP of Marketing',
                    company: 'AutoScale',
                    content: 'Our team of 3 now does the work of 15. The automation handles everything while we focus on strategy. Lead quality is up 200%.',
                    rating: 5
                },
                {
                    name: 'Marcus Johnson',
                    role: 'Growth Director',
                    company: 'ScaleUp Inc',
                    content: 'Cut our customer acquisition cost by 60% while tripling conversion rates. The AI workflows are incredibly sophisticated.',
                    rating: 5
                },
                {
                    name: 'Sarah Williams',
                    role: 'Marketing Manager',
                    company: 'GrowthHub',
                    content: 'We went from manually sending emails to fully automated, personalized customer journeys. Revenue per customer increased 85%.',
                    rating: 5
                }
            ]}

            pricingTitle="Transparent Automation Pricing"
            pricingDescription="No hidden fees. All plans include AI workflows + Expert strategy guidance."
            pricing={[
                {
                    name: 'Starter',
                    price: '$797',
                    period: '/month',
                    description: 'Perfect for small businesses',
                    subscribers: 'Up to 5K contacts',
                    features: [
                        '10 active workflows',
                        'Basic AI personalization',
                        'Email automation',
                        'Lead scoring',
                        'Email support'
                    ]
                },
                {
                    name: 'Professional',
                    price: '$1,797',
                    period: '/month',
                    description: 'Ideal for growing businesses',
                    subscribers: 'Up to 25K contacts',
                    features: [
                        'Unlimited workflows',
                        'Advanced AI + custom logic',
                        'Multi-channel automation',
                        'Predictive lead scoring',
                        'CRM integration',
                        'Dedicated strategist'
                    ],
                    popular: true
                },
                {
                    name: 'Enterprise',
                    price: '$3,997',
                    period: '/month',
                    description: 'For large organizations',
                    subscribers: 'Unlimited contacts',
                    features: [
                        'Full AI + Expert team',
                        'Custom integrations',
                        'Advanced segmentation',
                        'API access',
                        'White-label options',
                        'Dedicated automation team'
                    ]
                }
            ]}

            faqs={[
                {
                    question: 'What can be automated?',
                    answer: 'Almost everything - email campaigns, social media posting, lead nurturing, customer onboarding, re-engagement, cross-selling, data entry, reporting, and much more. If it\'s repetitive, we can automate it.'
                },
                {
                    question: 'How long does setup take?',
                    answer: 'Basic workflows can be live within 1-2 weeks. Complex multi-channel automation typically takes 3-4 weeks. We handle all the technical setup and integration work.'
                },
                {
                    question: 'Will it integrate with my existing tools?',
                    answer: 'Yes, we integrate with 500+ platforms including all major CRMs, email platforms, e-commerce systems, and marketing tools. Custom integrations are available for Enterprise plans.'
                },
                {
                    question: 'How personalized can the automation be?',
                    answer: 'Very personalized. Our AI can customize content, timing, channel, and messaging based on individual behavior, preferences, demographics, purchase history, and engagement patterns.'
                },
                {
                    question: 'What if I need to make changes?',
                    answer: 'All plans include unlimited workflow modifications. You can request changes anytime, and we\'ll implement them within 24-48 hours.'
                },
                {
                    question: 'How do you ensure deliverability?',
                    answer: 'We follow email best practices, maintain sender reputation, use authentication protocols (SPF, DKIM, DMARC), and monitor deliverability metrics to ensure your messages reach inboxes.'
                }
            ]}

            ctaTitle="Ready to Automate Your Marketing?"
            ctaDescription="Get your free automation audit and discover how to save 20+ hours per week while increasing conversions."
            ctaButtons={[
                { text: 'Get Free Automation Audit', variant: 'secondary' },
                { text: 'Schedule Strategy Call', variant: 'outline' }
            ]}
        />
    )
}
