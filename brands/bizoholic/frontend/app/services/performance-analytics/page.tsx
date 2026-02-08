"use client"

import ServicePageTemplate from '@/components/ServicePageTemplate'
import { BarChart, TrendingUp, PieChart, Activity, LineChart, Database, Target, Zap } from 'lucide-react'

export default function PerformanceAnalyticsPage() {
  return (
    <ServicePageTemplate
      serviceName="Performance Analytics"
      serviceDescription="Transform raw data into actionable insights with AI-powered analytics that track, measure, and optimize every aspect of your marketing performance in real-time."
      heroIcon={BarChart}
      ctaPrimary="Get Free Analytics Audit"
      ctaSecondary="View Sample Dashboard"
      rating="4.9/5 Rating"
      statsText="2B+ Data Points Analyzed"
      heroHighlights={[
        'Real-time performance tracking',
        'Predictive analytics included',
        'Custom dashboards & reports'
      ]}

      featuresTitle="Intelligent Performance Analytics Features"
      featuresDescription="Our AI-powered platform analyzes millions of data points to provide actionable insights that drive better marketing decisions."
      features={[
        {
          icon: TrendingUp,
          title: 'Predictive Analytics',
          description: 'AI forecasts future performance and identifies opportunities before your competitors.'
        },
        {
          icon: PieChart,
          title: 'Multi-Channel Attribution',
          description: 'Understand the true impact of each marketing channel on conversions and revenue.'
        },
        {
          icon: Activity,
          title: 'Real-Time Dashboards',
          description: 'Monitor all your marketing metrics in one place with customizable, real-time dashboards.'
        },
        {
          icon: LineChart,
          title: 'Automated Reporting',
          description: 'Get comprehensive reports delivered automatically with AI-generated insights and recommendations.'
        }
      ]}

      campaignTitle="Analytics Solutions We Provide"
      campaignDescription="From basic tracking to advanced predictive analytics, we provide comprehensive solutions for data-driven marketing."
      campaignTypes={[
        {
          name: 'Campaign Performance',
          description: 'Track ROI, conversions, and engagement across all marketing campaigns',
          results: ['Real-time tracking', '95% data accuracy', 'Multi-platform integration']
        },
        {
          name: 'Customer Journey Analytics',
          description: 'Understand how customers interact with your brand across touchpoints',
          results: ['Full journey mapping', '360° customer view', 'Behavior prediction']
        },
        {
          name: 'Competitive Intelligence',
          description: 'Monitor competitor performance and identify market opportunities',
          results: ['Competitor tracking', 'Market trends', 'Opportunity alerts']
        },
        {
          name: 'ROI & Attribution',
          description: 'Measure true marketing ROI with advanced attribution modeling',
          results: ['Multi-touch attribution', 'Revenue tracking', 'Channel optimization']
        }
      ]}

      benefitsTitle="Why Our AI + Expert Analytics Works"
      benefitsDescription="Traditional analytics tools show you what happened. Our AI tells you why it happened, what will happen next, and what actions to take for better results."
      benefits={[
        'Make data-driven decisions with confidence',
        'Identify high-performing channels instantly',
        'Predict future trends and opportunities',
        'Optimize budget allocation automatically',
        'Track customer lifetime value',
        'Get actionable recommendations, not just data'
      ]}
      comparisonTitle="AI vs Traditional Analytics"
      comparisonItems={[
        { label: 'Insights Generation', value: 'Automated' },
        { label: 'Data Processing', value: 'Real-Time' },
        { label: 'Predictions', value: 'AI-Powered' },
        { label: 'Reporting', value: 'Automated' }
      ]}

      testimonials={[
        {
          name: 'Robert Chen',
          role: 'CMO',
          company: 'DataDriven Inc',
          content: 'Finally, analytics that actually help us make decisions. The AI insights have improved our ROI by 180% in 6 months.',
          rating: 5
        },
        {
          name: 'Amanda Foster',
          role: 'Marketing Director',
          company: 'GrowthMetrics',
          content: 'We can now see exactly which channels drive revenue. Cut wasted ad spend by 40% and doubled conversions.',
          rating: 5
        },
        {
          name: 'Kevin Martinez',
          role: 'VP of Marketing',
          company: 'InsightCo',
          content: 'The predictive analytics are game-changing. We identify opportunities weeks before competitors and act on them immediately.',
          rating: 5
        }
      ]}

      pricingTitle="Transparent Analytics Pricing"
      pricingDescription="No hidden fees. All plans include AI-powered insights + Expert analysis."
      pricing={[
        {
          name: 'Starter',
          price: '$497',
          period: '/month',
          description: 'Perfect for small businesses',
          subscribers: 'Up to 3 data sources',
          features: [
            'Real-time dashboards',
            'Basic AI insights',
            'Monthly reports',
            'Email support',
            '1 year data retention'
          ]
        },
        {
          name: 'Professional',
          price: '$1,297',
          period: '/month',
          description: 'Ideal for growing businesses',
          subscribers: 'Up to 10 data sources',
          features: [
            'Advanced AI predictions',
            'Custom dashboards',
            'Weekly insights reports',
            'Multi-touch attribution',
            'Priority support',
            'Unlimited data retention'
          ],
          popular: true
        },
        {
          name: 'Enterprise',
          price: '$2,997',
          period: '/month',
          description: 'For large organizations',
          subscribers: 'Unlimited data sources',
          features: [
            'Full AI + Data science team',
            'Custom integrations',
            'White-label reporting',
            'API access',
            'Dedicated analyst',
            'Custom models'
          ]
        }
      ]}

      faqs={[
        {
          question: 'What data sources can you integrate?',
          answer: 'We integrate with 100+ platforms including Google Analytics, Google Ads, Meta, LinkedIn, Salesforce, HubSpot, Shopify, and custom databases. Our AI can consolidate data from any source with an API.'
        },
        {
          question: 'How is this different from Google Analytics?',
          answer: 'Google Analytics shows you what happened. Our AI analyzes why it happened, predicts what will happen next, and recommends specific actions to improve performance. We also provide multi-platform attribution and predictive insights.'
        },
        {
          question: 'How accurate are the predictions?',
          answer: 'Our AI models achieve 85-95% accuracy for most predictions. Accuracy improves over time as the system learns from your specific data patterns and business cycles.'
        },
        {
          question: 'Can I customize the dashboards?',
          answer: 'Yes, all plans include customizable dashboards. You can create unlimited custom views, set up automated alerts, and share dashboards with your team.'
        },
        {
          question: 'How long does implementation take?',
          answer: 'Most implementations are complete within 1-2 weeks. We handle all the technical setup and data integration while you focus on your business.'
        },
        {
          question: 'Do you provide training?',
          answer: 'Yes, all plans include onboarding training. Professional and Enterprise plans include ongoing training sessions and dedicated support to help you maximize value from the platform.'
        }
      ]}

      ctaTitle="Ready to Make Data-Driven Decisions?"
      ctaDescription="Get your free analytics audit and discover insights hidden in your marketing data."
      ctaButtons={[
        { text: 'Get Free Analytics Audit', variant: 'secondary' },
        { text: 'Schedule Demo', variant: 'outline' }
      ]}
    />
  )
}