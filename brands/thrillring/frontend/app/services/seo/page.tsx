"use client"

import Link from 'next/link'
import { ArrowLeft, TrendingUp, CheckCircle, Star, BarChart, Target, Users, Zap } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'

const features = [
  {
    icon: BarChart,
    title: 'AI Keyword Research',
    description: 'Advanced AI algorithms analyze millions of keywords to find the best opportunities for your business.'
  },
  {
    icon: Target,
    title: 'Content Optimization',
    description: 'Real-time content optimization suggestions powered by AI and validated by SEO experts.'
  },
  {
    icon: Users,
    title: 'Competitor Analysis',
    description: 'AI-driven competitor research reveals their strategies and identifies gaps you can exploit.'
  },
  {
    icon: Zap,
    title: 'Technical SEO Audit',
    description: 'Automated technical SEO audits with expert interpretation and prioritized fix recommendations.'
  },
]

const benefits = [
  'Increase organic traffic by 200-500%',
  'Improve search rankings for target keywords',
  'AI-powered content creation and optimization',
  'Technical SEO issues fixed automatically',
  'Expert SEO strategy and guidance',
  '24/7 monitoring and optimization'
]

const pricing = [
  {
    name: 'Starter',
    price: '$497',
    period: '/month',
    description: 'Perfect for small businesses',
    features: [
      '10 target keywords',
      'Basic AI content optimization',
      'Monthly SEO reports',
      'Technical SEO audit',
      'Email support'
    ]
  },
  {
    name: 'Professional',
    price: '$997',
    period: '/month',
    description: 'Ideal for growing businesses',
    features: [
      '50 target keywords',
      'Advanced AI optimization',
      'Weekly SEO reports',
      'Comprehensive technical SEO',
      'Priority support',
      'Competitor analysis'
    ],
    popular: true
  },
  {
    name: 'Enterprise',
    price: '$1,997',
    period: '/month',
    description: 'For large organizations',
    features: [
      'Unlimited keywords',
      'Full AI + Expert team',
      'Daily optimization',
      'Custom integrations',
      'Dedicated account manager',
      'White-label reporting'
    ]
  }
]

export default function SEOPage() {
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
            <span className="text-foreground">SEO</span>
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
                <TrendingUp className="h-4 w-4 mr-2" />
                AI + Expert Based Solution
              </Badge>
              
              <h1 className="text-4xl md:text-5xl font-bold mb-6">
                SEO (Search Engine Optimization)
              </h1>
              
              <p className="text-xl text-muted-foreground mb-8">
                Dominate search rankings with AI-powered keyword research, content optimization, 
                and technical SEO combined with expert strategy and guidance.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 mb-8">
                <Button size="lg" className="btn-gradient">
                  Get Free SEO Audit
                </Button>
                <Button variant="outline" size="lg">
                  View Case Studies
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
                <div>500+ Success Stories</div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-primary/10 to-accent/10 rounded-2xl p-8">
              <TrendingUp className="h-16 w-16 text-primary mb-6" />
              <h3 className="text-2xl font-bold mb-4">Ready to Rank Higher?</h3>
              <p className="text-muted-foreground mb-6">
                Our AI-powered SEO platform combined with expert guidance delivers 
                results that traditional SEO agencies can't match.
              </p>
              <div className="space-y-3">
                {['200-500% traffic increase', 'First page rankings', '24/7 AI optimization'].map((benefit, index) => (
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
              Powerful <span className="text-primary">AI-Driven</span> SEO Features
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Our combination of artificial intelligence and SEO expertise delivers 
              unmatched results for your search engine visibility.
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

      {/* Benefits Section */}
      <section className="py-20">
        <div className="container">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Why Choose Our <span className="text-primary">AI + Expert</span> SEO?
              </h2>
              <p className="text-lg text-muted-foreground mb-8">
                Traditional SEO agencies rely on manual processes and outdated strategies. 
                We combine cutting-edge AI technology with proven SEO expertise to deliver 
                results faster and more efficiently.
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
                <h3 className="text-xl font-bold mb-4">Traditional SEO vs Our AI + Expert Approach</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>Keyword Research Speed</span>
                    <Badge variant="default">10x Faster</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Content Optimization</span>
                    <Badge variant="default">Real-time</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Technical Issues Detection</span>
                    <Badge variant="default">Instant</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Strategy Updates</span>
                    <Badge variant="default">Continuous</Badge>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Choose Your <span className="text-primary">SEO Plan</span>
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
      <section className="py-20">
        <div className="container">
          <div className="bg-gradient-to-r from-primary to-accent rounded-2xl p-12 text-center text-white">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to Dominate Search Results?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Get your free SEO audit and see how our AI + Expert approach can transform your rankings.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" variant="secondary">
                Get Free SEO Audit
              </Button>
              <Button size="lg" variant="outline" className="text-white border-white hover:bg-white hover:text-primary">
                Schedule Consultation
              </Button>
            </div>
          </div>
        </div>
      </section>
      
      <Footer />
    </div>
  )
}