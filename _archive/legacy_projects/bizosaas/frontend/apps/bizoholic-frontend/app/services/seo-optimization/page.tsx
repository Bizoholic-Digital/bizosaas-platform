'use client'

/**
 * SEO Optimization Service Detail Page
 * Comprehensive service page with features, pricing, case studies, and CTA
 */

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { 
  ArrowRight, 
  ArrowLeft,
  CheckCircle,
  Star,
  Users,
  Clock,
  Target,
  Bot,
  TrendingUp,
  BarChart3,
  Zap,
  Search,
  Globe,
  Link2,
  Award
} from 'lucide-react'

// Types for service data
interface ServiceData {
  id: string
  title: string
  description: string
  icon: string
  badge: string
  category: string
  price_data: {
    starting_price: string
    currency: string
    billing_period: string
  }
  features: string[]
  benefits: string[]
  case_studies: Array<{
    client_name: string
    industry: string
    results: string
    metrics: string
  }>
  testimonials: Array<{
    client_name: string
    company: string
    quote: string
    rating: number
  }>
}

export default function SEOOptimizationPage() {
  const [service, setService] = useState<ServiceData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchServiceData()
  }, [])

  const fetchServiceData = async () => {
    try {
      setLoading(true)
      
      // Try to fetch from Wagtail CMS first
      const response = await fetch('/api/brain/wagtail/services?slug=seo-optimization')
      
      if (response.ok) {
        const data = await response.json()
        const serviceData = data.services?.[0]
        
        if (serviceData) {
          setService(serviceData)
          return
        }
      }
      
      // Fallback to static data if CMS is unavailable
      setService({
        id: "seo-optimization",
        title: "AI-Powered SEO Optimization",
        description: "Dominate search rankings with intelligent SEO strategies, content optimization, and automated link building powered by advanced AI technology.",
        icon: "🔍",
        badge: "AI-Driven",
        category: "Search Marketing",
        price_data: {
          starting_price: "₹24,999",
          currency: "INR",
          billing_period: "month"
        },
        features: [
          "Comprehensive SEO Audits & Analysis",
          "AI-Powered Keyword Research",
          "Automated On-page Optimization",
          "Technical SEO Monitoring",
          "Content Gap Analysis & Strategy",
          "Competitive Intelligence",
          "Local SEO Optimization",
          "Link Building Automation",
          "Core Web Vitals Optimization",
          "Real-time Ranking Tracking"
        ],
        benefits: [
          "Increase organic traffic by 300% within 6 months",
          "Achieve first-page rankings for target keywords",
          "Improve domain authority and credibility", 
          "Reduce cost per acquisition through organic growth",
          "24/7 automated SEO monitoring and optimization",
          "Stay ahead of Google algorithm updates"
        ],
        case_studies: [
          {
            client_name: "Local Services Co",
            industry: "Home Services",
            results: "450% increase in organic leads, ranking #1 for 20+ keywords",
            metrics: "Organic traffic: +450%, Local visibility: +300%"
          },
          {
            client_name: "E-commerce Plus",
            industry: "Online Retail",
            results: "Increased organic revenue by ₹50 lakhs in 8 months",
            metrics: "Rankings: Top 3 for 150+ keywords, CTR: +85%"
          }
        ],
        testimonials: [
          {
            client_name: "Raj Patel",
            company: "TechSolutions India",
            quote: "Our website went from page 3 to page 1 for all major keywords within 4 months. The AI-powered SEO approach is phenomenal.",
            rating: 5
          },
          {
            client_name: "Priya Sharma",
            company: "HealthCare Hub",
            quote: "The automated SEO optimization saved us thousands in agency fees while delivering better results. Highly recommended!",
            rating: 5
          }
        ]
      })
      
    } catch (error) {
      console.error('Error fetching service data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex flex-col min-h-screen">
        <Header />
        
        {/* Loading Content */}
        <div className="container py-20">
          <div className="animate-pulse">
            <div className="h-8 bg-muted rounded w-1/3 mb-4"></div>
            <div className="h-4 bg-muted rounded w-2/3 mb-8"></div>
            <div className="space-y-4">
              <div className="h-4 bg-muted rounded w-full"></div>
              <div className="h-4 bg-muted rounded w-5/6"></div>
              <div className="h-4 bg-muted rounded w-4/6"></div>
            </div>
          </div>
        </div>
        
        <Footer />
      </div>
    )
  }

  if (!service) {
    return (
      <div className="flex flex-col min-h-screen">
        <Header />
        
        {/* 404 Content */}
        <div className="container py-20 text-center">
          <h1 className="text-4xl font-bold text-foreground mb-4">Service Not Found</h1>
          <p className="text-muted-foreground mb-8">The service you're looking for doesn't exist.</p>
          <Link href="/services">
            <Button>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Services
            </Button>
          </Link>
        </div>
        
        <Footer />
      </div>
    )
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      {/* Breadcrumb */}
      <section className="py-4 border-b bg-muted/30">
        <div className="container">
          <nav className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-foreground">Home</Link>
            <span>/</span>
            <Link href="/services" className="hover:text-foreground">Services</Link>
            <span>/</span>
            <span className="text-foreground">{service.title}</span>
          </nav>
        </div>
      </section>

      {/* Hero Section */}
      <section className="py-16 lg:py-20">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <div className="flex items-center justify-center space-x-4 mb-6">
              <div className="text-5xl">{service.icon}</div>
              <Badge variant="secondary" className="text-sm">
                {service.badge}
              </Badge>
            </div>
            
            <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl">
              {service.title}
            </h1>
            
            <p className="mt-6 text-lg leading-8 text-muted-foreground max-w-2xl mx-auto">
              {service.description}
            </p>
            
            <div className="mt-8 flex items-center justify-center gap-4">
              <Link href="/auth/register">
                <Button size="lg" className="px-8 btn-gradient">
                  Boost Your Rankings
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/contact">
                <Button variant="outline" size="lg">
                  Free SEO Audit
                </Button>
              </Link>
            </div>

            {/* Trust Indicators */}
            <div className="mt-10 flex items-center justify-center space-x-8 text-sm text-muted-foreground">
              <div className="flex items-center space-x-2">
                <Search className="h-4 w-4 text-green-600" />
                <span>1000+ Keywords Ranked</span>
              </div>
              <div className="flex items-center space-x-2">
                <TrendingUp className="h-4 w-4 text-green-600" />
                <span>300% Avg Traffic Increase</span>
              </div>
              <div className="flex items-center space-x-2">
                <Award className="h-4 w-4 text-green-600" />
                <span>95% Client Success Rate</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SEO Services Grid */}
      <section className="py-16 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Comprehensive SEO Services
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Every aspect of SEO optimized by intelligent AI systems
            </p>
          </div>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Search className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle className="text-lg">Keyword Research</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  AI-powered keyword discovery and competitive analysis
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Globe className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle className="text-lg">Technical SEO</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Site speed, mobile optimization, and technical fixes
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Link2 className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle className="text-lg">Link Building</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  High-quality backlinks from authoritative websites
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <BarChart3 className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle className="text-lg">Analytics & Reporting</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Real-time tracking and comprehensive performance reports
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="container">
          <div className="mx-auto max-w-4xl">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                Advanced SEO Optimization Features
              </h2>
              <p className="mt-4 text-lg text-muted-foreground">
                Cutting-edge AI technology for superior search engine performance
              </p>
            </div>

            <div className="grid gap-6 md:grid-cols-2 mb-12">
              {service.features.map((feature, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <span className="text-foreground">{feature}</span>
                </div>
              ))}
            </div>

            {/* Benefits */}
            {service.benefits && service.benefits.length > 0 && (
              <div className="bg-muted/30 rounded-lg p-8">
                <h3 className="text-2xl font-bold text-foreground mb-6 text-center">SEO Success Outcomes</h3>
                <div className="grid gap-4 md:grid-cols-2">
                  {service.benefits.map((benefit, index) => (
                    <div key={index} className="flex items-start space-x-3">
                      <TrendingUp className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                      <span className="text-foreground">{benefit}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Case Studies */}
      <section className="py-16 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-4xl">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                SEO Success Stories
              </h2>
              <p className="mt-4 text-lg text-muted-foreground">
                Real businesses achieving remarkable organic growth
              </p>
            </div>
            
            <div className="grid gap-8 md:grid-cols-2 mb-12">
              {service.case_studies && service.case_studies.length > 0 ? (
                service.case_studies.map((study, index) => (
                  <Card key={index} className="hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-lg">{study.client_name}</CardTitle>
                        <Badge variant="outline">{study.industry}</Badge>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-foreground mb-4">{study.results}</p>
                      <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                        <BarChart3 className="h-4 w-4" />
                        <span>{study.metrics}</span>
                      </div>
                    </CardContent>
                  </Card>
                ))
              ) : (
                <div className="col-span-2 text-center text-muted-foreground">
                  No case studies available at the moment.
                </div>
              )}
            </div>

            {/* Testimonials */}
            <div className="space-y-6">
              {service.testimonials && service.testimonials.length > 0 ? (
                service.testimonials.map((testimonial, index) => (
                  <Card key={index} className="bg-background">
                    <CardContent className="pt-6">
                      <div className="flex items-center mb-4">
                        {Array.from({ length: testimonial.rating }).map((_, i) => (
                          <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                        ))}
                      </div>
                      <blockquote className="text-foreground mb-4 text-lg">
                        "{testimonial.quote}"
                      </blockquote>
                      <cite className="text-muted-foreground">
                        <strong>{testimonial.client_name}</strong>, {testimonial.company}
                      </cite>
                    </CardContent>
                  </Card>
                ))
              ) : null}
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-16">
        <div className="container">
          <div className="mx-auto max-w-2xl">
            <div className="bg-muted/30 rounded-lg border p-8 text-center">
              <h3 className="text-2xl font-bold text-foreground mb-4">Professional SEO Services</h3>
              <div className="text-4xl font-bold text-primary mb-2">
                {service?.price_data?.starting_price || '₹29,999'}
              </div>
              <div className="text-muted-foreground mb-6">
                per {service?.price_data?.billing_period || 'month'} • {service?.price_data?.currency || 'INR'}
              </div>
              <div className="space-y-3 mb-8">
                <Link href="/auth/register">
                  <Button size="lg" className="w-full btn-gradient">
                    Start SEO Optimization
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
                <Link href="/contact">
                  <Button variant="outline" size="lg" className="w-full">
                    Get Free SEO Audit
                  </Button>
                </Link>
              </div>
              <p className="text-sm text-muted-foreground">
                30-day money-back guarantee • No setup fees • Cancel anytime
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-primary text-primary-foreground">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Dominate Search Rankings Today
            </h2>
            <p className="mt-4 text-lg opacity-90">
              Join hundreds of businesses achieving first-page rankings with AI-powered SEO.
            </p>
            
            <div className="mt-8 flex items-center justify-center gap-4">
              <div className="flex items-center space-x-1">
                {[1,2,3,4,5].map((star) => (
                  <Star key={star} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                ))}
                <span className="ml-2 text-sm opacity-75">4.9/5 from 800+ clients</span>
              </div>
            </div>
            
            <div className="mt-8">
              <Link href="/auth/register">
                <Button size="lg" variant="secondary" className="px-12">
                  Start Ranking Higher Today
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
      
      <Footer />
    </div>
  )
}