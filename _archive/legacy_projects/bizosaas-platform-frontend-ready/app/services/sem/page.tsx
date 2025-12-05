"use client"

import Link from 'next/link'
import { ArrowLeft, Target, CheckCircle, Star, DollarSign, TrendingUp, Users, Zap } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'

const features = [
  {
    icon: DollarSign,
    title: 'AI Bid Optimization',
    description: 'Smart bidding algorithms automatically adjust bids in real-time for maximum ROI.'
  },
  {
    icon: Target,
    title: 'Advanced Targeting',
    description: 'AI-powered audience segmentation and targeting for precise ad delivery.'
  },
  {
    icon: Users,
    title: 'Competitor Intelligence',
    description: 'Real-time competitor analysis and automatic strategy adjustments.'
  },
  {
    icon: Zap,
    title: 'Campaign Automation',
    description: 'Fully automated campaign creation, testing, and optimization.'
  },
]

const platforms = [
  {
    name: 'Google Ads',
    description: 'Search, Display, Shopping, and Video campaigns',
    features: ['Smart Shopping', 'Performance Max', 'Responsive Search Ads', 'YouTube Ads']
  },
  {
    name: 'Microsoft Ads',
    description: 'Bing and partner network advertising',
    features: ['Search Campaigns', 'Audience Ads', 'Shopping Campaigns', 'Import from Google']
  },
  {
    name: 'Meta Ads',
    description: 'Facebook and Instagram advertising',
    features: ['Feed Ads', 'Stories', 'Reels', 'Messenger Ads']
  },
]

const benefits = [
  'Reduce cost-per-click by 30-50%',
  'Increase conversion rates by 200%+',
  'AI-powered ad copy testing',
  'Automated budget optimization',
  'Expert campaign strategy',
  '24/7 campaign monitoring'
]

const pricing = [
  {
    name: 'Starter',
    price: '$997',
    period: '/month',
    description: 'Perfect for small campaigns',
    adSpend: 'Up to $5k/month',
    features: [
      'Google Ads management',
      'Basic AI optimization',
      'Monthly reports',
      'Email support',
      'Landing page analysis'
    ]
  },
  {
    name: 'Professional',
    price: '$1,997',
    period: '/month',
    description: 'Ideal for growing businesses',
    adSpend: 'Up to $15k/month',
    features: [
      'Multi-platform management',
      'Advanced AI optimization',
      'Weekly reports',
      'Priority support',
      'Custom landing pages',
      'A/B testing automation'
    ],
    popular: true
  },
  {
    name: 'Enterprise',
    price: '$3,997',
    period: '/month',
    description: 'For large campaigns',
    adSpend: 'Unlimited ad spend',
    features: [
      'Full-service management',
      'Dedicated AI + Expert team',
      'Daily optimization',
      'Custom integrations',
      'Account manager',
      'Advanced attribution'
    ]
  }
]

export default function SEMPage() {
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
            <span className="text-foreground">SEM</span>
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
                <Target className="h-4 w-4 mr-2" />
                AI + Expert Based Solution
              </Badge>
              
              <h1 className="text-4xl md:text-5xl font-bold mb-6">
                SEM (Search Engine Marketing)
              </h1>
              
              <p className="text-xl text-muted-foreground mb-8">
                Maximize your advertising ROI with intelligent Google Ads and Bing Ads management 
                powered by AI bid optimization and expert campaign strategy.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 mb-8">
                <Button size="lg" className="btn-gradient">
                  Get Free Campaign Audit
                </Button>
                <Button variant="outline" size="lg">
                  View Success Stories
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
                <div>$50M+ Ad Spend Managed</div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-primary/10 to-accent/10 rounded-2xl p-8">
              <Target className="h-16 w-16 text-primary mb-6" />
              <h3 className="text-2xl font-bold mb-4">Ready to Scale Your Ads?</h3>
              <p className="text-muted-foreground mb-6">
                Our AI-powered SEM platform automatically optimizes your campaigns 
                for maximum ROI while expert strategists guide the overall direction.
              </p>
              <div className="space-y-3">
                {['50% lower CPCs', '200%+ higher conversions', 'Automated optimization'].map((benefit, index) => (
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
              Advanced <span className="text-primary">AI-Powered</span> SEM Features
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Our intelligent platform combines machine learning with expert strategy 
              to deliver superior advertising performance.
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
              Multi-Platform <span className="text-primary">Campaign Management</span>
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              We manage campaigns across all major advertising platforms 
              with platform-specific optimizations and strategies.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {platforms.map((platform, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle className="text-xl">{platform.name}</CardTitle>
                  <CardDescription>{platform.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {platform.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500" />
                        <span className="text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
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
                Why Our <span className="text-primary">AI + Expert</span> SEM Works
              </h2>
              <p className="text-lg text-muted-foreground mb-8">
                Traditional agencies rely on manual bid adjustments and gut feelings. 
                Our AI analyzes thousands of data points in real-time while expert 
                strategists provide human insight and creative direction.
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
                <h3 className="text-xl font-bold mb-4">AI vs Traditional SEM Management</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>Bid Adjustments</span>
                    <Badge variant="default">Real-time</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>A/B Testing Speed</span>
                    <Badge variant="default">10x Faster</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Budget Optimization</span>
                    <Badge variant="default">Automated</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Performance Analysis</span>
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
              Transparent <span className="text-primary">SEM Pricing</span>
            </h2>
            <p className="text-lg text-muted-foreground">
              No hidden fees. All plans include AI optimization + Expert strategy.
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
                    {plan.adSpend}
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
              Ready to Maximize Your Ad ROI?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Get your free campaign audit and discover how our AI + Expert approach 
              can transform your advertising performance.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" variant="secondary">
                Get Free Campaign Audit
              </Button>
              <Button size="lg" variant="outline" className="text-white border-white hover:bg-white hover:text-primary">
                Schedule Strategy Call
              </Button>
            </div>
          </div>
        </div>
      </section>
      
      <Footer />
    </div>
  )
}