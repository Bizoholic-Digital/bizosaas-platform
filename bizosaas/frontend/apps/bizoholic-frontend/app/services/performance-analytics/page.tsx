'use client'

/**
 * Performance Analytics Service Detail Page
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
  BarChart3,
  TrendingUp,
  PieChart,
  Activity
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

export default function PerformanceAnalyticsPage() {
  const [service, setService] = useState<ServiceData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchServiceData()
  }, [])

  const fetchServiceData = async () => {
    try {
      setLoading(true)
      
      // Try to fetch from Wagtail CMS first
      const response = await fetch('/api/brain/wagtail/services?slug=performance-analytics')
      
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
        id: "performance-analytics",
        title: "Performance Analytics",
        description: "Advanced AI-powered analytics that provide deep insights into campaign performance, audience behavior, and ROI optimization.",
        icon: "📊",
        badge: "Data-Driven",
        category: "Analytics",
        price_data: {
          starting_price: "₹19,999",
          currency: "INR",
          billing_period: "month"
        },
        features: [
          "Real-time Performance Dashboards",
          "Multi-channel Attribution Modeling",
          "Predictive Analytics & Forecasting",
          "Custom KPI Tracking",
          "Automated Report Generation",
          "Cross-platform Data Integration",
          "Advanced Segmentation Analysis",
          "ROI & ROAS Optimization"
        ],
        benefits: [
          "Make data-driven decisions with confidence",
          "Identify high-performing channels instantly", 
          "Predict campaign outcomes before launch",
          "Optimize budget allocation across platforms",
          "Reduce reporting time by 85%",
          "Increase overall marketing ROI by 35%"
        ],
        case_studies: [
          {
            client_name: "E-commerce Giant",
            industry: "Retail",
            results: "45% increase in marketing efficiency through data insights",
            metrics: "Marketing ROI: +35%, Attribution accuracy: 95%"
          },
          {
            client_name: "SaaS Company",
            industry: "Technology",
            results: "Reduced customer acquisition cost by 40%",
            metrics: "CAC: -40%, LTV increase: +60%"
          }
        ],
        testimonials: [
          {
            client_name: "David Johnson",
            company: "MarketingPro",
            quote: "The performance analytics have completely transformed how we understand our marketing. We can see exactly what's working and what isn't.",
            rating: 5
          },
          {
            client_name: "Emma Watson",
            company: "GrowthTech",
            quote: "The predictive analytics feature has saved us thousands by helping us avoid poor-performing campaigns.",
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
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/contact">
                <Button variant="outline" size="lg">
                  Schedule Demo
                </Button>
              </Link>
            </div>

            {/* Trust Indicators */}
            <div className="mt-10 flex items-center justify-center space-x-8 text-sm text-muted-foreground">
              <div className="flex items-center space-x-2">
                <Users className="h-4 w-4 text-green-600" />
                <span>1000+ Data Points</span>
              </div>
              <div className="flex items-center space-x-2">
                <Clock className="h-4 w-4 text-green-600" />
                <span>Real-time Insights</span>
              </div>
              <div className="flex items-center space-x-2">
                <Target className="h-4 w-4 text-green-600" />
                <span>95% Attribution Accuracy</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-4xl">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                Advanced Analytics Features
              </h2>
              <p className="mt-4 text-lg text-muted-foreground">
                Everything you need for comprehensive performance analysis
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
            <div className="bg-background rounded-lg border p-8">
              <h3 className="text-2xl font-bold text-foreground mb-6 text-center">Key Benefits</h3>
              <div className="grid gap-4 md:grid-cols-2">
                {service.benefits.map((benefit, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <TrendingUp className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Case Studies */}
      <section className="py-16">
        <div className="container">
          <div className="mx-auto max-w-4xl">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                Success Stories
              </h2>
              <p className="mt-4 text-lg text-muted-foreground">
                Real results from businesses using performance analytics
              </p>
            </div>
            
            <div className="grid gap-8 md:grid-cols-2 mb-12">
              {service.case_studies.map((study, index) => (
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
              ))}
            </div>

            {/* Testimonials */}
            <div className="space-y-6">
              {service.testimonials.map((testimonial, index) => (
                <Card key={index} className="bg-muted/30">
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
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-16 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl">
            <div className="bg-background rounded-lg border p-8 text-center">
              <h3 className="text-2xl font-bold text-foreground mb-4">Simple, Transparent Pricing</h3>
              <div className="text-4xl font-bold text-primary mb-2">
                {service?.price_data?.starting_price || '₹29,999'}
              </div>
              <div className="text-muted-foreground mb-6">
                per {service?.price_data?.billing_period || 'month'} • {service?.price_data?.currency || 'INR'}
              </div>
              <div className="space-y-3 mb-8">
                <Link href="/auth/register">
                  <Button size="lg" className="w-full btn-gradient">
                    Start 14-Day Free Trial
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
                <Link href="/contact">
                  <Button variant="outline" size="lg" className="w-full">
                    Schedule Strategy Call
                  </Button>
                </Link>
              </div>
              <p className="text-sm text-muted-foreground">
                14-day free trial • No credit card required • Cancel anytime
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
              Ready to Unlock Your Data?
            </h2>
            <p className="mt-4 text-lg opacity-90">
              Join hundreds of businesses making data-driven decisions with advanced analytics.
            </p>
            
            <div className="mt-8 flex items-center justify-center gap-4">
              <div className="flex items-center space-x-1">
                {[1,2,3,4,5].map((star) => (
                  <Star key={star} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                ))}
                <span className="ml-2 text-sm opacity-75">4.9/5 from 300+ reviews</span>
              </div>
            </div>
            
            <div className="mt-8">
              <Link href="/auth/register">
                <Button size="lg" variant="secondary" className="px-12">
                  Get Started Today - Free Trial
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