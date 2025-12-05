"use client"

import Link from 'next/link'
import { ArrowLeft, Bot, CheckCircle, Star, Mail, Users, BarChart, Zap } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/button'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'

const features = [
  {
    icon: Mail,
    title: 'AI Email Generation',
    description: 'Create personalized email campaigns with AI-powered copywriting and subject line optimization.'
  },
  {
    icon: Users,
    title: 'Smart Segmentation',
    description: 'Automatically segment your audience based on behavior, preferences, and engagement patterns.'
  },
  {
    icon: BarChart,
    title: 'Predictive Analytics',
    description: 'AI predicts the best send times, content, and frequency for maximum engagement.'
  },
  {
    icon: Zap,
    title: 'Automation Flows',
    description: 'Build complex email sequences that adapt based on subscriber actions and responses.'
  },
]

const campaignTypes = [
  {
    name: 'Welcome Series',
    description: 'Onboard new subscribers with personalized welcome sequences',
    results: ['85% open rate', '40% click rate', '25% conversion boost']
  },
  {
    name: 'Abandoned Cart',
    description: 'Recover lost sales with intelligent cart abandonment campaigns',
    results: ['70% open rate', '25% recovery rate', '15% revenue increase']
  },
  {
    name: 'Re-engagement',
    description: 'Win back inactive subscribers with AI-crafted re-engagement flows',
    results: ['55% reactivation', '30% list retention', '20% engagement boost']
  },
  {
    name: 'Product Launch',
    description: 'Build excitement and drive sales for new product releases',
    results: ['90% delivery rate', '45% open rate', '12% conversion rate']
  },
]

const benefits = [
  'Increase email open rates by 40%+',
  'Boost click-through rates by 60%',
  'AI-powered personalization',
  'Automated A/B testing',
  'Expert copywriting guidance',
  '24/7 campaign optimization'
]

const pricing = [
  {
    name: 'Starter',
    price: '$497',
    period: '/month',
    description: 'Perfect for small businesses',
    subscribers: 'Up to 5K subscribers',
    features: [
      '10 email campaigns/month',
      'Basic AI personalization',
      'Welcome series automation',
      'Monthly reporting',
      'Email support'
    ]
  },
  {
    name: 'Professional',
    price: '$997',
    period: '/month',
    description: 'Ideal for growing businesses',
    subscribers: 'Up to 25K subscribers',
    features: [
      'Unlimited email campaigns',
      'Advanced AI + custom copy',
      'Multi-step automations',
      'A/B testing included',
      'Weekly optimization',
      'Priority support'
    ],
    popular: true
  },
  {
    name: 'Enterprise',
    price: '$1,997',
    period: '/month',
    description: 'For large organizations',
    subscribers: 'Unlimited subscribers',
    features: [
      'Full AI + Expert team',
      'Custom email templates',
      'Advanced segmentation',
      'Deliverability optimization',
      'Dedicated manager',
      'Custom integrations'
    ]
  }
]

export default function EmailMarketingPage() {
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
            <span className="text-foreground">Email Marketing</span>
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
                <Bot className="h-4 w-4 mr-2" />
                AI + Expert Based Solution
              </Badge>
              
              <h1 className="text-4xl md:text-5xl font-bold mb-6">
                Email Marketing
              </h1>
              
              <p className="text-xl text-muted-foreground mb-8">
                Transform your email campaigns with intelligent automation, personalization, 
                and A/B testing powered by AI with expert copywriting and strategy guidance.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 mb-8">
                <Button size="lg" className="btn-gradient">
                  Get Free Email Audit
                </Button>
                <Button variant="outline" size="lg">
                  View Campaign Examples
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
                <div>50M+ Emails Delivered</div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-primary/10 to-accent/10 rounded-2xl p-8">
              <Bot className="h-16 w-16 text-primary mb-6" />
              <h3 className="text-2xl font-bold mb-4">Ready to Engage Your Audience?</h3>
              <p className="text-muted-foreground mb-6">
                Our AI creates personalized email campaigns that drive engagement 
                while expert copywriters ensure your message resonates with your audience.
              </p>
              <div className="space-y-3">
                {['40% higher open rates', '60% more clicks', 'Automated optimization'].map((benefit, index) => (
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
              Intelligent <span className="text-primary">Email Marketing</span> Features
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Our AI-powered platform handles everything from content creation to send-time 
              optimization while expert strategists guide your email marketing strategy.
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

      {/* Campaign Types Section */}
      <section className="py-20">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              High-Converting <span className="text-primary">Email Campaigns</span>
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              We create and manage various types of email campaigns optimized 
              for different stages of your customer journey.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {campaignTypes.map((campaign, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle className="text-xl">{campaign.name}</CardTitle>
                  <CardDescription className="text-base">{campaign.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {campaign.results.map((result, resultIndex) => (
                      <div key={resultIndex} className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500" />
                        <span className="text-sm font-medium">{result}</span>
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
                Why Our <span className="text-primary">AI + Expert</span> Email Marketing Works
              </h2>
              <p className="text-lg text-muted-foreground mb-8">
                Traditional email marketing relies on generic templates and guesswork. 
                Our AI analyzes subscriber behavior, optimizes send times, and personalizes 
                content while expert copywriters craft compelling messages that convert.
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
                <h3 className="text-xl font-bold mb-4">AI vs Traditional Email Marketing</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>Personalization</span>
                    <Badge variant="default">1:1 Scale</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>A/B Testing</span>
                    <Badge variant="default">Automated</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Send Time Optimization</span>
                    <Badge variant="default">AI-Powered</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Content Generation</span>
                    <Badge variant="default">Instant</Badge>
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
              Transparent <span className="text-primary">Email Marketing</span> Pricing
            </h2>
            <p className="text-lg text-muted-foreground">
              No hidden fees. All plans include AI optimization + Expert copywriting.
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
                    {plan.subscribers}
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
              Ready to Transform Your Email Marketing?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Get your free email audit and discover how our AI + Expert approach 
              can boost your email performance and drive more conversions.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" variant="secondary">
                Get Free Email Audit
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