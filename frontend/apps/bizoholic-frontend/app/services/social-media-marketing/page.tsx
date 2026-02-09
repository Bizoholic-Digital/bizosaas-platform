"use client"

import Link from 'next/link'
import { ArrowLeft, Users, CheckCircle, Star, Calendar, MessageSquare, TrendingUp, Zap } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/button'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'

const features = [
  {
    icon: Calendar,
    title: 'AI Content Creation',
    description: 'Generate engaging posts, captions, and visuals automatically based on your brand voice.'
  },
  {
    icon: MessageSquare,
    title: 'Smart Scheduling',
    description: 'AI determines optimal posting times for maximum engagement across all platforms.'
  },
  {
    icon: TrendingUp,
    title: 'Engagement Analytics',
    description: 'Real-time insights and automatic strategy adjustments based on performance data.'
  },
  {
    icon: Zap,
    title: 'Community Management',
    description: 'AI-powered response suggestions with expert oversight for authentic engagement.'
  },
]

const platforms = [
  {
    name: 'Facebook',
    description: 'Feed posts, Stories, Reels, and Events',
    metrics: ['2.9B+ users', 'High engagement', 'B2B & B2C']
  },
  {
    name: 'Instagram',
    description: 'Posts, Stories, Reels, and IGTV',
    metrics: ['2B+ users', 'Visual-first', 'High conversion']
  },
  {
    name: 'LinkedIn',
    description: 'Professional content and networking',
    metrics: ['900M+ users', 'B2B focused', 'Thought leadership']
  },
  {
    name: 'Twitter/X',
    description: 'Real-time updates and conversations',
    metrics: ['450M+ users', 'News & trends', 'Brand voice']
  },
  {
    name: 'TikTok',
    description: 'Short-form video content',
    metrics: ['1B+ users', 'Gen Z & Millennial', 'Viral potential']
  },
  {
    name: 'YouTube',
    description: 'Long-form and short video content',
    metrics: ['2.7B+ users', 'Educational', 'High retention']
  },
]

const benefits = [
  'Increase follower growth by 300%+',
  'Boost engagement rates by 150%',
  'AI-generated content calendar',
  'Automated posting & scheduling',
  'Expert content strategy',
  '24/7 community management'
]

const pricing = [
  {
    name: 'Starter',
    price: '$697',
    period: '/month',
    description: 'Perfect for small businesses',
    platforms: '3 platforms',
    features: [
      '20 posts per month',
      'Basic AI content creation',
      'Scheduled posting',
      'Monthly analytics',
      'Email support'
    ]
  },
  {
    name: 'Professional',
    price: '$1,297',
    period: '/month',
    description: 'Ideal for growing brands',
    platforms: '5 platforms',
    features: [
      '60 posts per month',
      'Advanced AI + custom graphics',
      'Stories & Reels included',
      'Community management',
      'Weekly reports',
      'Priority support'
    ],
    popular: true
  },
  {
    name: 'Enterprise',
    price: '$2,497',
    period: '/month',
    description: 'For large organizations',
    platforms: 'All platforms',
    features: [
      'Unlimited posts',
      'Full AI + Expert team',
      'Video content creation',
      'Influencer partnerships',
      'Custom campaigns',
      'Dedicated manager'
    ]
  }
]

export default function SocialMediaMarketingPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      {/* Breadcrumb */}
      <div className="bg-muted/30 py-4">
        <div className="container">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-primary">Home</Link>
            <span>/</span>
            <Link href="/#services" className="hover:text-primary">Services</Link>
            <span>/</span>
            <span className="text-foreground">Social Media Marketing</span>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <section className="py-20 md:py-32">
        <div className="container">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <Link href="/#services" className="inline-flex items-center gap-2 text-muted-foreground hover:text-primary mb-6">
                <ArrowLeft className="h-4 w-4" />
                Back to Services
              </Link>
              
              <Badge variant="outline" className="mb-4">
                <Users className="h-4 w-4 mr-2" />
                AI + Expert Based Solution
              </Badge>
              
              <h1 className="text-4xl md:text-5xl font-bold mb-6">
                Social Media Marketing
              </h1>
              
              <p className="text-xl text-muted-foreground mb-8">
                Build your brand presence with automated content creation, posting schedules, 
                and engagement strategies powered by AI with expert social media guidance.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 mb-8">
                <Button size="lg" className="btn-gradient">
                  Get Free Social Audit
                </Button>
                <Button variant="outline" size="lg">
                  View Content Examples
                </Button>
              </div>
              
              <div className="flex items-center gap-6 text-sm">
                <div className="flex items-center gap-2">
                  <div className="flex text-yellow-400">
                    {Array.from({ length: 5 }).map((_, i) => (
                      <Star key={i} className="h-4 w-4 fill-current" />
                    ))}
                  </div>
                  <span>4.9/5 Rating</span>
                </div>
                <div>1M+ Posts Created</div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-primary/10 to-accent/10 rounded-2xl p-8">
              <Users className="h-16 w-16 text-primary mb-6" />
              <h3 className="text-2xl font-bold mb-4">Ready to Go Viral?</h3>
              <p className="text-muted-foreground mb-6">
                Our AI creates engaging content while experts guide your social strategy 
                to build authentic connections with your audience.
              </p>
              <div className="space-y-3">
                {['300% follower growth', '150% more engagement', 'Viral content potential'].map((benefit, index) => (
                  <div key={index} className="flex items-center gap-2">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <span className="text-sm">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Smart <span className="text-primary">Social Media</span> Features
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Our AI-powered platform handles content creation, scheduling, and engagement 
              while expert strategists guide your brand voice and community building.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="text-center">
                <CardHeader>
                  <feature.icon className="h-12 w-12 text-primary mx-auto mb-4" />
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Platforms Section */}
      <section className="py-20">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Multi-Platform <span className="text-primary">Social Presence</span>
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              We manage your presence across all major social platforms 
              with platform-specific content and engagement strategies.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {platforms.map((platform, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle className="text-xl">{platform.name}</CardTitle>
                  <CardDescription>{platform.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {platform.metrics.map((metric, metricIndex) => (
                      <div key={metricIndex} className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-primary"></div>
                        <span className="text-sm">{metric}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Why Our <span className="text-primary">AI + Expert</span> Approach Works
              </h2>
              <p className="text-lg text-muted-foreground mb-8">
                Traditional social media agencies post generic content and hope for the best. 
                Our AI analyzes trending topics, audience behavior, and optimal timing while 
                expert strategists ensure your brand voice remains authentic and engaging.
              </p>
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <CheckCircle className="h-6 w-6 text-green-500 mt-0.5" />
                    <span className="text-lg">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="space-y-6">
              <Card className="p-6">
                <h3 className="text-xl font-bold mb-4">AI vs Traditional Social Media</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>Content Creation Speed</span>
                    <Badge variant="default">10x Faster</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Posting Consistency</span>
                    <Badge variant="default">100%</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Trend Detection</span>
                    <Badge variant="default">Real-time</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Engagement Analysis</span>
                    <Badge variant="default">Continuous</Badge>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Choose Your <span className="text-primary">Social Media Plan</span>
            </h2>
            <p className="text-lg text-muted-foreground">
              Transparent pricing with no hidden fees. All plans include AI + Expert support.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {pricing.map((plan, index) => (
              <Card key={index} className={`relative ${plan.popular ? 'border-primary shadow-lg scale-105' : ''}`}>
                {plan.popular && (
                  <Badge className="absolute -top-3 left-1/2 -translate-x-1/2">
                    Most Popular
                  </Badge>
                )}
                <CardHeader className="text-center">
                  <CardTitle className="text-2xl">{plan.name}</CardTitle>
                  <CardDescription>{plan.description}</CardDescription>
                  <div className="py-4">
                    <span className="text-4xl font-bold">{plan.price}</span>
                    <span className="text-muted-foreground">{plan.period}</span>
                  </div>
                  <Badge variant="outline" className="text-xs">
                    {plan.platforms}
                  </Badge>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3 mb-6">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500" />
                        <span className="text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
                  <Button className="w-full" variant={plan.popular ? 'default' : 'outline'}>
                    Start {plan.name} Plan
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="bg-gradient-to-r from-primary to-accent rounded-2xl p-12 text-center text-white">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to Amplify Your Social Presence?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Get your free social media audit and see how our AI + Expert approach 
              can transform your brand's online presence.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" variant="secondary">
                Get Free Social Audit
              </Button>
              <Button size="lg" variant="outline" className="text-white border-white hover:bg-white hover:text-primary">
                Schedule Strategy Session
              </Button>
            </div>
          </div>
        </div>
      </section>
      
      <Footer />
    </div>
  )
}