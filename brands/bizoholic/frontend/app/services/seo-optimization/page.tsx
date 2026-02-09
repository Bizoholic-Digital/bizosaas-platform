"use client"

import ServicePageTemplate from '@/components/ServicePageTemplate'
import { Search, TrendingUp, Link, FileText, BarChart, Globe, Target, Zap } from 'lucide-react'

export default function SEOOptimizationPage() {
  return (
    <ServicePageTemplate
      serviceName="SEO Optimization"
      serviceDescription="Dominate search rankings with AI-powered SEO strategies, technical optimization, and content creation that drives organic traffic and converts visitors into customers."
      heroIcon={Search}
      ctaPrimary="Get Free SEO Audit"
      ctaSecondary="View Rankings Report"
      rating="4.9/5 Rating"
      statsText="10K+ Keywords Ranked #1"
      heroHighlights={[
        '300% average traffic increase',
        'First page rankings guaranteed',
        'Technical + content SEO included'
      ]}

      featuresTitle="Comprehensive SEO Services"
      featuresDescription="Our AI analyzes search algorithms and competitor strategies to create SEO campaigns that deliver sustainable, long-term results."
      features={[
        {
          icon: FileText,
          title: 'Keyword Research',
          description: 'AI-powered keyword discovery and competitive analysis to find high-value opportunities.'
        },
        {
          icon: Zap,
          title: 'Technical SEO',
          description: 'Site speed optimization, mobile responsiveness, and technical fixes that improve rankings.'
        },
        {
          icon: Link,
          title: 'Link Building',
          description: 'High-quality backlinks from authoritative websites to boost domain authority.'
        },
        {
          icon: BarChart,
          title: 'Analytics & Reporting',
          description: 'Real-time tracking and comprehensive performance reports with actionable insights.'
        }
      ]}

      campaignTitle="SEO Solutions We Provide"
      campaignDescription="From local SEO to enterprise-level optimization, we provide comprehensive solutions for every business size and industry."
      campaignTypes={[
        {
          name: 'Local SEO',
          description: 'Dominate local search results and Google Maps for your service area',
          results: ['Top 3 local rankings', '500% more calls', 'Google Business optimization']
        },
        {
          name: 'E-commerce SEO',
          description: 'Optimize product pages and category pages for maximum visibility and sales',
          results: ['Product page rankings', '200% organic revenue', 'Shopping feed optimization']
        },
        {
          name: 'Enterprise SEO',
          description: 'Large-scale SEO for websites with thousands of pages and complex structures',
          results: ['10K+ keyword rankings', 'Technical architecture', 'International SEO']
        },
        {
          name: 'Content SEO',
          description: 'Create and optimize content that ranks and converts',
          results: ['Featured snippets', 'Topical authority', 'Content clusters']
        }
      ]}

      benefitsTitle="Why Our AI + Expert SEO Works"
      benefitsDescription="Traditional SEO relies on outdated tactics and manual analysis. Our AI continuously monitors algorithm updates, analyzes competitors, and optimizes your site in real-time while expert SEO strategists ensure sustainable, white-hat practices."
      benefits={[
        'Rank on page 1 for high-value keywords',
        'Increase organic traffic by 300%+',
        'Improve conversion rates with better targeting',
        'Build sustainable long-term rankings',
        'Stay ahead of algorithm updates',
        'Transparent reporting and ROI tracking'
      ]}
      comparisonTitle="AI vs Traditional SEO"
      comparisonItems={[
        { label: 'Keyword Research', value: 'AI-Powered' },
        { label: 'Optimization', value: 'Continuous' },
        { label: 'Algorithm Updates', value: 'Real-Time' },
        { label: 'Reporting', value: 'Automated' }
      ]}

      testimonials={[
        {
          name: 'Michael Brown',
          role: 'CEO',
          company: 'RankFirst',
          content: 'Went from page 5 to page 1 for our top keywords in 4 months. Organic traffic increased 450% and leads tripled.',
          rating: 5
        },
        {
          name: 'Laura Davis',
          role: 'Marketing Director',
          company: 'SearchPro',
          content: 'Finally found an SEO partner that delivers real results. Our organic revenue is up 280% and still growing.',
          rating: 5
        },
        {
          name: 'Chris Wilson',
          role: 'E-commerce Manager',
          company: 'ShopGrowth',
          content: 'Product pages now rank for hundreds of keywords. Organic sales increased from 20% to 65% of total revenue.',
          rating: 5
        }
      ]}

      pricingTitle="Transparent SEO Pricing"
      pricingDescription="No hidden fees. All plans include AI optimization + Expert SEO strategist guidance."
      pricing={[
        {
          name: 'Local',
          price: '$1,497',
          period: '/month',
          description: 'Perfect for local businesses',
          subscribers: 'Up to 20 keywords',
          features: [
            'Local SEO optimization',
            'Google Business Profile',
            'Citation building',
            'Monthly reporting',
            'Email support'
          ]
        },
        {
          name: 'Growth',
          price: '$2,997',
          period: '/month',
          description: 'Ideal for growing businesses',
          subscribers: 'Up to 50 keywords',
          features: [
            'National SEO campaigns',
            'Technical SEO audit & fixes',
            'Content optimization',
            'Link building',
            'Bi-weekly reporting',
            'Dedicated SEO manager'
          ],
          popular: true
        },
        {
          name: 'Enterprise',
          price: '$5,997',
          period: '/month',
          description: 'For large organizations',
          subscribers: 'Unlimited keywords',
          features: [
            'Enterprise-level SEO',
            'International SEO',
            'Custom strategy',
            'Advanced link building',
            'Weekly reporting',
            'Senior SEO team'
          ]
        }
      ]}

      faqs={[
        {
          question: 'How long does it take to see results?',
          answer: 'Most clients see measurable improvements within 60-90 days. Significant ranking improvements typically occur within 4-6 months. SEO is a long-term strategy that builds sustainable, compounding results.'
        },
        {
          question: 'Do you guarantee first page rankings?',
          answer: 'We guarantee measurable improvements in rankings, traffic, and conversions. While we can\'t guarantee specific positions (no ethical SEO company can), our track record shows 95% of clients achieve page 1 rankings for their target keywords within 6 months.'
        },
        {
          question: 'What\'s included in technical SEO?',
          answer: 'Technical SEO includes site speed optimization, mobile responsiveness, crawlability fixes, schema markup, XML sitemaps, robots.txt optimization, canonical tags, and resolving technical errors that prevent ranking.'
        },
        {
          question: 'Do you use black hat tactics?',
          answer: 'Never. We only use white-hat, Google-approved SEO techniques. Our strategies focus on creating genuine value for users and building sustainable rankings that won\'t be penalized.'
        },
        {
          question: 'How do you handle algorithm updates?',
          answer: 'Our AI monitors algorithm updates in real-time and automatically adjusts strategies. We also have expert SEO strategists who analyze major updates and ensure your site stays compliant and competitive.'
        },
        {
          question: 'Can you help with content creation?',
          answer: 'Yes, all plans include content optimization recommendations. Growth and Enterprise plans include full content creation services with SEO-optimized articles, blog posts, and landing pages.'
        }
      ]}

      ctaTitle="Ready to Dominate Search Rankings?"
      ctaDescription="Get your free SEO audit and discover opportunities to increase organic traffic and revenue."
      ctaButtons={[
        { text: 'Get Free SEO Audit', variant: 'secondary' },
        { text: 'Schedule SEO Consultation', variant: 'outline' }
      ]}
    />
  )
}