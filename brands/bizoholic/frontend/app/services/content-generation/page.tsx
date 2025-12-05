"use client"

import ServicePageTemplate from '@/components/ServicePageTemplate'
import { PenTool, FileText, Image, Video, Sparkles, Palette, Layout, Type } from 'lucide-react'

export default function ContentGenerationPage() {
  return (
    <ServicePageTemplate
      serviceName="Content Generation"
      serviceDescription="Create high-quality, engaging content for blogs, social media, email campaigns, and website copy that converts visitors into customers - powered by AI with expert editing."
      heroIcon={PenTool}
      ctaPrimary="Get Free Content Sample"
      ctaSecondary="View Content Examples"
      rating="4.9/5 Rating"
      statsText="10M+ Content Pieces Created"
      heroHighlights={[
        '90% faster content creation',
        'SEO-optimized automatically',
        'Expert human editing included'
      ]}

      featuresTitle="Intelligent Content Generation Features"
      featuresDescription="Our AI creates compelling content while expert editors ensure quality, brand voice consistency, and engagement."
      features={[
        {
          icon: FileText,
          title: 'Blog & Article Writing',
          description: 'AI generates long-form content optimized for SEO and reader engagement with expert editing.'
        },
        {
          icon: Image,
          title: 'Social Media Content',
          description: 'Create engaging posts, captions, and visuals for all social platforms automatically.'
        },
        {
          icon: Video,
          title: 'Video Scripts',
          description: 'Generate compelling video scripts and storyboards for YouTube, TikTok, and ads.'
        },
        {
          icon: Type,
          title: 'Ad Copy Creation',
          description: 'AI-powered ad copy that converts with A/B testing and performance optimization.'
        }
      ]}

      campaignTitle="Content Types We Create"
      campaignDescription="From blog posts to social media, we create every type of content your business needs."
      campaignTypes={[
        {
          name: 'Blog Articles',
          description: 'SEO-optimized long-form content that ranks and converts',
          results: ['2000+ word articles', '95% readability score', '3x organic traffic']
        },
        {
          name: 'Social Media Posts',
          description: 'Engaging content for Facebook, Instagram, LinkedIn, and Twitter',
          results: ['Daily content calendar', '200% engagement boost', 'Brand voice consistency']
        },
        {
          name: 'Email Campaigns',
          description: 'Personalized email content that drives opens and clicks',
          results: ['45% open rates', '25% click rates', 'Automated sequences']
        },
        {
          name: 'Website Copy',
          description: 'Conversion-optimized landing pages and website content',
          results: ['60% conversion lift', 'SEO optimized', 'Brand aligned']
        }
      ]}

      benefitsTitle="Why Our AI + Expert Content Generation Works"
      benefitsDescription="Traditional content creation is slow and expensive. Our AI generates high-quality content in minutes while expert editors ensure it matches your brand voice and engages your audience."
      benefits={[
        'Create content 10x faster than traditional methods',
        'Maintain consistent brand voice across all channels',
        'SEO optimization built into every piece',
        'Expert editing for quality assurance',
        'Unlimited revisions included',
        'Multi-language support available'
      ]}
      comparisonTitle="AI vs Traditional Content Creation"
      comparisonItems={[
        { label: 'Speed', value: '10x Faster' },
        { label: 'Cost', value: '70% Less' },
        { label: 'SEO Optimization', value: 'Automatic' },
        { label: 'Consistency', value: '100%' }
      ]}

      testimonials={[
        {
          name: 'David Park',
          role: 'Content Director',
          company: 'MediaHub',
          content: 'We went from publishing 4 blog posts per month to 20, with better quality and engagement. The AI + editor combo is perfect.',
          rating: 5
        },
        {
          name: 'Lisa Martinez',
          role: 'Marketing Manager',
          company: 'BrandBoost',
          content: 'Our social media engagement tripled. The AI creates content that actually resonates with our audience.',
          rating: 5
        },
        {
          name: 'James Wilson',
          role: 'CEO',
          company: 'ContentFirst',
          content: 'Cut content costs by 65% while increasing output 5x. The quality is consistently excellent.',
          rating: 5
        }
      ]}

      pricingTitle="Transparent Content Generation Pricing"
      pricingDescription="No hidden fees. All plans include AI generation + Expert editing."
      pricing={[
        {
          name: 'Starter',
          price: '$697',
          period: '/month',
          description: 'Perfect for small businesses',
          subscribers: 'Up to 20 pieces/month',
          features: [
            '20 content pieces/month',
            'Blog posts & social media',
            'Basic SEO optimization',
            'Expert editing included',
            'Email support'
          ]
        },
        {
          name: 'Professional',
          price: '$1,497',
          period: '/month',
          description: 'Ideal for growing businesses',
          subscribers: 'Up to 60 pieces/month',
          features: [
            '60 content pieces/month',
            'All content types',
            'Advanced SEO + keywords',
            'Priority editing',
            'Content calendar',
            'Dedicated editor'
          ],
          popular: true
        },
        {
          name: 'Enterprise',
          price: '$2,997',
          period: '/month',
          description: 'For large organizations',
          subscribers: 'Unlimited content',
          features: [
            'Unlimited content pieces',
            'Multi-language support',
            'Custom brand guidelines',
            'White-label options',
            'API access',
            'Dedicated content team'
          ]
        }
      ]}

      faqs={[
        {
          question: 'How does AI content generation work?',
          answer: 'Our AI analyzes your brand voice, target audience, and content goals to generate high-quality content. Expert editors then review and refine each piece to ensure it meets our quality standards and matches your brand perfectly.'
        },
        {
          question: 'Will the content be original and plagiarism-free?',
          answer: 'Yes, all content is 100% original and passes plagiarism checks. Our AI creates unique content based on your specifications, and we run every piece through plagiarism detection tools.'
        },
        {
          question: 'Can you match my brand voice?',
          answer: 'Absolutely. We analyze your existing content and work with you to create detailed brand guidelines. The AI learns your voice and our editors ensure consistency across all content.'
        },
        {
          question: 'What if I need revisions?',
          answer: 'All plans include unlimited revisions. If content doesn\'t meet your expectations, we\'ll revise it until you\'re completely satisfied.'
        },
        {
          question: 'How quickly can you create content?',
          answer: 'Most content pieces are delivered within 24-48 hours. Rush orders can be accommodated for an additional fee.'
        },
        {
          question: 'Do you provide content strategy?',
          answer: 'Yes, Professional and Enterprise plans include content strategy consultation to help you plan topics, keywords, and content calendars for maximum impact.'
        }
      ]}

      ctaTitle="Ready to Scale Your Content Creation?"
      ctaDescription="Get your free content sample and see how our AI + Expert approach creates engaging content that converts."
      ctaButtons={[
        { text: 'Get Free Content Sample', variant: 'secondary' },
        { text: 'Schedule Content Strategy Call', variant: 'outline' }
      ]}
    />
  )
}