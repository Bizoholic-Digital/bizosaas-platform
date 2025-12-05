"use client"

import ServicePageTemplate from '@/components/ServicePageTemplate'
import { Bot, Target, BarChart, Zap, TrendingUp, Users, Globe, DollarSign } from 'lucide-react'

export default function AICampaignManagementPage() {
  return (
    <ServicePageTemplate
      serviceName="AI Campaign Management"
      serviceDescription="Transform your advertising with autonomous AI agents that create, optimize, and manage campaigns across Google Ads, Meta, LinkedIn, and 40+ other platforms - running 24/7 on autopilot."
      heroIcon={Bot}
      ctaPrimary="Get Free Campaign Audit"
      ctaSecondary="View Success Stories"
      rating="4.9/5 Rating"
      statsText="$500M+ Ad Spend Managed"
      heroHighlights={[
        '75% reduction in cost-per-acquisition',
        '300% increase in ROAS',
        'Automated 24/7 optimization'
      ]}

      featuresTitle="Intelligent AI Campaign Management Features"
      featuresDescription="Our AI-powered platform handles everything from keyword research to bid optimization while expert strategists guide your advertising strategy."
      features={[
        {
          icon: Target,
          title: 'Smart Targeting',
          description: 'AI analyzes audience behavior and automatically adjusts targeting parameters for maximum ROI.'
        },
        {
          icon: BarChart,
          title: 'Real-Time Optimization',
          description: 'Continuous performance monitoring with automatic bid adjustments and budget reallocation.'
        },
        {
          icon: Zap,
          title: 'Multi-Platform Management',
          description: 'Manage campaigns across Google, Meta, LinkedIn, TikTok, and 40+ platforms from one dashboard.'
        },
        {
          icon: TrendingUp,
          title: 'Predictive Analytics',
          description: 'AI predicts campaign performance and suggests optimizations before issues arise.'
        }
      ]}

      campaignTitle="High-Converting Campaign Types"
      campaignDescription="We create and manage various types of campaigns optimized for different business goals and customer journeys."
      campaignTypes={[
        {
          name: 'Search Campaigns',
          description: 'Dominate search results with AI-optimized keyword targeting and ad copy',
          results: ['50% lower CPC', '200% more conversions', '4.5x ROAS average']
        },
        {
          name: 'Display Campaigns',
          description: 'Reach your audience across millions of websites with smart display ads',
          results: ['80% brand awareness lift', '35% CTR improvement', '60% cost reduction']
        },
        {
          name: 'Social Media Ads',
          description: 'Engage users on Facebook, Instagram, LinkedIn, and TikTok with precision targeting',
          results: ['90% audience match rate', '45% engagement boost', '3.2x conversion rate']
        },
        {
          name: 'Retargeting Campaigns',
          description: 'Re-engage visitors with personalized ads based on their behavior',
          results: ['70% conversion rate', '25% cart recovery', '5x ROI on retargeting']
        }
      ]}

      benefitsTitle="Why Our AI + Expert Campaign Management Works"
      benefitsDescription="Traditional campaign management relies on manual optimization and guesswork. Our AI analyzes millions of data points in real-time, automatically adjusts bids, and optimizes targeting while expert strategists ensure alignment with your business goals."
      benefits={[
        'Reduce ad spend by 40-60% through AI optimization',
        'Increase conversion rates by 200-300%',
        '24/7 automated campaign monitoring',
        'Multi-platform campaign coordination',
        'Expert strategy oversight',
        'Transparent reporting and insights'
      ]}
      comparisonTitle="AI vs Traditional Campaign Management"
      comparisonItems={[
        { label: 'Optimization Speed', value: 'Real-Time' },
        { label: 'Platform Coverage', value: '40+ Platforms' },
        { label: 'Bid Adjustments', value: 'Automated' },
        { label: 'A/B Testing', value: 'Continuous' }
      ]}

      testimonials={[
        {
          name: 'Sarah Chen',
          role: 'Marketing Director',
          company: 'TechStart Inc',
          content: 'Our ROAS increased from 2.5x to 8.7x in just 3 months. The AI handles everything while we focus on strategy.',
          rating: 5
        },
        {
          name: 'Michael Rodriguez',
          role: 'CEO',
          company: 'GrowthCo',
          content: 'Cut our ad spend by 55% while doubling conversions. The AI optimization is incredible and the team is always available.',
          rating: 5
        },
        {
          name: 'Emily Thompson',
          role: 'VP of Marketing',
          company: 'ScaleUp Solutions',
          content: 'Managing campaigns across 12 platforms was a nightmare. Now the AI handles it all and performance has never been better.',
          rating: 5
        }
      ]}

      pricingTitle="Transparent AI Campaign Management Pricing"
      pricingDescription="No hidden fees. All plans include AI optimization + Expert strategy guidance."
      pricing={[
        {
          name: 'Starter',
          price: '$997',
          period: '/month',
          description: 'Perfect for small businesses',
          subscribers: 'Up to $10K ad spend/month',
          features: [
            '2-3 platform management',
            'Basic AI optimization',
            'Monthly strategy calls',
            'Standard reporting',
            'Email support'
          ]
        },
        {
          name: 'Professional',
          price: '$2,497',
          period: '/month',
          description: 'Ideal for growing businesses',
          subscribers: 'Up to $50K ad spend/month',
          features: [
            'Up to 8 platform management',
            'Advanced AI + custom strategy',
            'Weekly optimization calls',
            'Real-time dashboards',
            'Priority support',
            'Dedicated account manager'
          ],
          popular: true
        },
        {
          name: 'Enterprise',
          price: '$4,997',
          period: '/month',
          description: 'For large organizations',
          subscribers: 'Unlimited ad spend',
          features: [
            'All platforms included',
            'Full AI + Expert team',
            'Daily optimization',
            'Custom integrations',
            'White-label reporting',
            'Dedicated success team'
          ]
        }
      ]}

      faqs={[
        {
          question: 'How does AI campaign management differ from traditional management?',
          answer: 'Our AI analyzes millions of data points in real-time and makes instant optimizations that would take humans hours or days. It continuously tests, learns, and improves while expert strategists provide oversight and strategic direction.'
        },
        {
          question: 'What platforms do you support?',
          answer: 'We support 40+ advertising platforms including Google Ads, Meta (Facebook/Instagram), LinkedIn, TikTok, Twitter, Pinterest, Snapchat, Microsoft Ads, and many more. Our AI can manage campaigns across all platforms simultaneously.'
        },
        {
          question: 'How quickly will I see results?',
          answer: 'Most clients see measurable improvements within 2-4 weeks as the AI learns your audience and optimizes campaigns. Significant ROI improvements typically occur within 60-90 days as the system fully optimizes.'
        },
        {
          question: 'Do I need to provide ad creative?',
          answer: 'We can work with your existing creative or our team can create high-converting ad copy and visuals. Our AI tests multiple variations to find the best performers.'
        },
        {
          question: 'What kind of reporting do you provide?',
          answer: 'You get real-time access to comprehensive dashboards showing all key metrics. We also provide weekly summary reports and monthly strategy sessions to review performance and plan ahead.'
        },
        {
          question: 'Can I cancel anytime?',
          answer: 'Yes, all plans are month-to-month with no long-term contracts. We believe in earning your business every month through exceptional results.'
        }
      ]}

      ctaTitle="Ready to Transform Your Advertising?"
      ctaDescription="Get your free campaign audit and discover how our AI + Expert approach can reduce costs and boost conversions."
      ctaButtons={[
        { text: 'Get Free Campaign Audit', variant: 'secondary' },
        { text: 'Schedule Strategy Call', variant: 'outline' }
      ]}
    />
  )
}