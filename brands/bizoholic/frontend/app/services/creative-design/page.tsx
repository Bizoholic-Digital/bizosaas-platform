"use client"

import ServicePageTemplate from '@/components/ServicePageTemplate'
import { Palette, Image, Layout, Sparkles, PenTool, Layers, Paintbrush, Wand2 } from 'lucide-react'

export default function CreativeDesignPage() {
    return (
        <ServicePageTemplate
            serviceName="Creative Design"
            serviceDescription="Transform your brand with stunning visual content - from social media graphics to complete brand identities - powered by AI design tools with expert creative direction."
            heroIcon={Palette}
            ctaPrimary="Get Free Design Sample"
            ctaSecondary="View Portfolio"
            rating="4.9/5 Rating"
            statsText="50K+ Designs Created"
            heroHighlights={[
                '10x faster design delivery',
                'Unlimited revisions included',
                'Brand consistency guaranteed'
            ]}

            featuresTitle="Professional Creative Design Services"
            featuresDescription="Our designers combine creative expertise with AI-powered tools to deliver stunning visuals that capture attention and drive engagement."
            features={[
                {
                    icon: Paintbrush,
                    title: 'Brand Identity',
                    description: 'Create cohesive brand identities including logos, color palettes, typography, and brand guidelines.'
                },
                {
                    icon: Image,
                    title: 'Social Media Graphics',
                    description: 'Eye-catching social media content designed for maximum engagement across all platforms.'
                },
                {
                    icon: Layout,
                    title: 'Marketing Materials',
                    description: 'Professional designs for ads, brochures, presentations, and all marketing collateral.'
                },
                {
                    icon: Wand2,
                    title: 'AI-Enhanced Design',
                    description: 'Leverage AI tools for rapid iteration, variations, and optimization while maintaining creative quality.'
                }
            ]}

            campaignTitle="Design Solutions We Provide"
            campaignDescription="From brand identity to marketing materials, we create every type of visual content your business needs."
            campaignTypes={[
                {
                    name: 'Brand Identity Design',
                    description: 'Complete brand identity packages that make your business memorable',
                    results: ['Logo design', 'Brand guidelines', 'Visual system']
                },
                {
                    name: 'Social Media Design',
                    description: 'Scroll-stopping social content that drives engagement and followers',
                    results: ['Daily graphics', 'Story templates', 'Ad creatives']
                },
                {
                    name: 'Marketing Collateral',
                    description: 'Professional marketing materials that convert prospects into customers',
                    results: ['Landing pages', 'Email templates', 'Ad campaigns']
                },
                {
                    name: 'Web & UI Design',
                    description: 'Beautiful, conversion-optimized website and app designs',
                    results: ['Website design', 'UI/UX design', 'Mobile responsive']
                }
            ]}

            benefitsTitle="Why Our AI + Expert Design Works"
            benefitsDescription="Traditional design is slow and expensive. Our designers use AI to rapidly create variations and iterate, while applying creative expertise to ensure every design is on-brand, engaging, and effective."
            benefits={[
                'Get designs 10x faster than traditional agencies',
                'Unlimited revisions until you\'re satisfied',
                'Maintain brand consistency across all materials',
                'Scale design production without scaling costs',
                'Access to senior designers and creative directors',
                'Source files and full ownership included'
            ]}
            comparisonTitle="AI-Enhanced vs Traditional Design"
            comparisonItems={[
                { label: 'Delivery Speed', value: '10x Faster' },
                { label: 'Revisions', value: 'Unlimited' },
                { label: 'Variations', value: 'Instant' },
                { label: 'Consistency', value: '100%' }
            ]}

            testimonials={[
                {
                    name: 'Emma Thompson',
                    role: 'Brand Director',
                    company: 'StyleCo',
                    content: 'Our rebrand was completed in 3 weeks instead of 3 months. The quality is exceptional and our engagement is up 250%.',
                    rating: 5
                },
                {
                    name: 'Alex Rivera',
                    role: 'Marketing Manager',
                    company: 'VisualFirst',
                    content: 'We get professional designs daily for less than the cost of one full-time designer. The AI + human combo is perfect.',
                    rating: 5
                },
                {
                    name: 'Sophie Chen',
                    role: 'CEO',
                    company: 'BrandBuilders',
                    content: 'Finally found a design partner that understands our vision and delivers consistently. Our brand has never looked better.',
                    rating: 5
                }
            ]}

            pricingTitle="Transparent Creative Design Pricing"
            pricingDescription="No hidden fees. All plans include AI-powered design + Expert creative direction."
            pricing={[
                {
                    name: 'Starter',
                    price: '$997',
                    period: '/month',
                    description: 'Perfect for small businesses',
                    subscribers: 'Up to 20 designs/month',
                    features: [
                        '20 design requests/month',
                        'Social media graphics',
                        'Marketing materials',
                        'Unlimited revisions',
                        'Email support'
                    ]
                },
                {
                    name: 'Professional',
                    price: '$2,497',
                    period: '/month',
                    description: 'Ideal for growing businesses',
                    subscribers: 'Up to 60 designs/month',
                    features: [
                        '60 design requests/month',
                        'All design types',
                        'Brand guideline development',
                        'Priority delivery',
                        'Dedicated designer',
                        'Video calls included'
                    ],
                    popular: true
                },
                {
                    name: 'Enterprise',
                    price: '$4,997',
                    period: '/month',
                    description: 'For large organizations',
                    subscribers: 'Unlimited designs',
                    features: [
                        'Unlimited design requests',
                        'Full creative team',
                        'White-label options',
                        'Custom brand system',
                        'Creative director oversight',
                        'Same-day delivery available'
                    ]
                }
            ]}

            faqs={[
                {
                    question: 'What types of designs can you create?',
                    answer: 'We create everything - logos, brand identities, social media graphics, ads, brochures, presentations, website designs, email templates, infographics, and more. If it\'s visual, we can design it.'
                },
                {
                    question: 'How does the unlimited revisions work?',
                    answer: 'You can request as many revisions as needed until you\'re 100% satisfied with the design. We want you to love every piece we create.'
                },
                {
                    question: 'How fast can you deliver designs?',
                    answer: 'Most designs are delivered within 24-48 hours. Simple graphics can be delivered same-day. Complex projects like brand identities take 1-2 weeks.'
                },
                {
                    question: 'Do I own the designs?',
                    answer: 'Yes, you own all designs and receive source files. You can use them however you like with no additional fees or licensing restrictions.'
                },
                {
                    question: 'Can you match my existing brand?',
                    answer: 'Absolutely. We analyze your existing brand materials and create designs that perfectly match your brand guidelines and visual identity.'
                },
                {
                    question: 'What if I need a specific file format?',
                    answer: 'We provide designs in all common formats - PNG, JPG, PDF, SVG, and source files (AI, PSD, Figma). Just let us know what you need.'
                }
            ]}

            ctaTitle="Ready to Elevate Your Brand?"
            ctaDescription="Get your free design sample and see how our AI + Expert designers can transform your visual content."
            ctaButtons={[
                { text: 'Get Free Design Sample', variant: 'secondary' },
                { text: 'View Full Portfolio', variant: 'outline' }
            ]}
        />
    )
}
