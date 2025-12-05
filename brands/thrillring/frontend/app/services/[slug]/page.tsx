'use client'

/**
 * Dynamic Service Page
 * Loads service content from Wagtail CMS via Brain API based on slug
 */

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  ArrowRight, 
  ArrowLeft,
  CheckCircle,
  Star,
  Users,
  Clock,
  Target
} from 'lucide-react'

// Types for service data
interface ServicePage {
  id: number
  title: string
  slug: string
  icon: string
  badge: string
  category: string
  service_description: string
  detailed_description?: string
  features?: string[]
  benefits?: string[]
  pricing_tiers?: Array<{
    name: string
    price: string
    currency: string
    billing_period: string
    features: string[]
    popular?: boolean
  }>
  case_studies?: Array<{
    client_name: string
    industry: string
    results: string
    metrics: string
  }>
  testimonials?: Array<{
    client_name: string
    company: string
    quote: string
    rating: number
  }>
  featured: boolean
  order: number
  price_data: {
    starting_price: string
    currency: string
    billing_period: string
  }
  meta_title?: string
  meta_description?: string
}

export default function ServicePage() {
  const params = useParams()
  const slug = params.slug as string
  
  const [service, setService] = useState<ServicePage | null>(null)
  const [relatedServices, setRelatedServices] = useState<ServicePage[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (slug) {
      fetchServiceData()
    }
  }, [slug])

  const fetchServiceData = async () => {
    try {
      setLoading(true)
      
      // Fetch all services and find the one matching the slug
      const servicesRes = await fetch('/api/brain/wagtail/services')
      
      if (servicesRes.ok) {
        const servicesData = await servicesRes.json()
        const currentService = servicesData.services?.find((s: ServicePage) => s.slug === slug)
        
        if (currentService) {
          setService(currentService)
          
          // Get related services (same category, excluding current)
          const related = servicesData.services?.filter(
            (s: ServicePage) => s.category === currentService.category && s.slug !== slug
          ).slice(0, 3) || []
          
          setRelatedServices(related)
        }
      }
    } catch (error) {
      console.error('Error fetching service data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        {/* Header */}
        <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
          <div className="container flex h-16 items-center justify-between">
            <Link href="/" className="flex items-center space-x-2">
              <Image
                src="/bizoholic-logo-hq.png"
                alt="Bizoholic Digital Logo"
                width={40}
                height={40}
                className="h-8 w-auto"
                priority
              />
              <span className="font-bold text-xl text-foreground">Bizoholic Digital</span>
            </Link>
          </div>
        </header>

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
      </div>
    )
  }

  if (!service) {
    return (
      <div className="min-h-screen bg-background">
        {/* Header */}
        <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
          <div className="container flex h-16 items-center justify-between">
            <Link href="/" className="flex items-center space-x-2">
              <Image
                src="/bizoholic-logo-hq.png"
                alt="Bizoholic Digital Logo"
                width={40}
                height={40}
                className="h-8 w-auto"
                priority
              />
              <span className="font-bold text-xl text-foreground">Bizoholic Digital</span>
            </Link>
          </div>
        </header>

        {/* 404 Content */}
        <div className="container py-20 text-center">
          <h1 className="text-4xl font-bold text-foreground mb-4">Service Not Found</h1>
          <p className="text-muted-foreground mb-8">The service you're looking for doesn't exist.</p>
          <Link href="/">
            <Button>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Homepage
            </Button>
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center space-x-2">
            <Image
              src="/bizoholic-logo-hq.png"
              alt="Bizoholic Digital Logo"
              width={40}
              height={40}
              className="h-8 w-auto"
              priority
            />
            <span className="font-bold text-xl text-foreground">Bizoholic Digital</span>
          </Link>
          
          <nav className="hidden md:flex items-center space-x-6 text-sm font-medium">
            <Link href="/#services" className="text-foreground/60 hover:text-foreground">Services</Link>
            <Link href="/#about" className="text-foreground/60 hover:text-foreground">About</Link>
            <Link href="/#contact" className="text-foreground/60 hover:text-foreground">Contact</Link>
          </nav>
          
          <div className="flex items-center space-x-4">
            <Link href="/auth/login">
              <Button variant="outline" size="sm">
                Sign In
              </Button>
            </Link>
            <Link href="/auth/login">
              <Button size="sm">
                Get Started
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Breadcrumb */}
      <section className="py-4 border-b bg-muted/30">
        <div className="container">
          <nav className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-foreground">Home</Link>
            <span>/</span>
            <Link href="/#services" className="hover:text-foreground">Services</Link>
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
              {service.service_description}
            </p>
            
            <div className="mt-8 flex items-center justify-center gap-4">
              <Link href="/auth/login">
                <Button size="lg" className="px-8">
                  Get Started Today
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Button variant="outline" size="lg">
                Learn More
              </Button>
            </div>

            {/* Trust Indicators */}
            <div className="mt-10 flex items-center justify-center space-x-8 text-sm text-muted-foreground">
              <div className="flex items-center space-x-2">
                <Users className="h-4 w-4 text-green-600" />
                <span>1000+ Clients</span>
              </div>
              <div className="flex items-center space-x-2">
                <Clock className="h-4 w-4 text-green-600" />
                <span>24/7 Support</span>
              </div>
              <div className="flex items-center space-x-2">
                <Target className="h-4 w-4 text-green-600" />
                <span>Proven Results</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Service Details */}
      <section className="py-16 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-4xl">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                What's Included
              </h2>
              <p className="mt-4 text-lg text-muted-foreground">
                Comprehensive {service.title.toLowerCase()} solutions tailored to your business needs
              </p>
            </div>

            {/* Key Features */}
            <div className="grid gap-6 md:grid-cols-2 mb-12">
              {[
                "AI-Powered Campaign Optimization",
                "Real-Time Performance Analytics", 
                "Multi-Platform Integration",
                "24/7 Automated Monitoring",
                "Custom Strategy Development",
                "Dedicated Account Management"
              ].map((feature, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <span className="text-foreground">{feature}</span>
                </div>
              ))}
            </div>

            {/* Pricing */}
            <div className="bg-background rounded-lg border p-8 text-center">
              <h3 className="text-2xl font-bold text-foreground mb-4">Simple, Transparent Pricing</h3>
              <div className="text-4xl font-bold text-primary mb-2">
                {service.price_data.starting_price}
              </div>
              <div className="text-muted-foreground mb-6">
                per {service.price_data.billing_period} • {service.price_data.currency}
              </div>
              <Link href="/auth/login">
                <Button size="lg" className="px-8">
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <p className="text-sm text-muted-foreground mt-4">
                14-day free trial • No credit card required • Cancel anytime
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Related Services */}
      {relatedServices.length > 0 && (
        <section className="py-16">
          <div className="container">
            <div className="mx-auto max-w-2xl text-center mb-12">
              <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                Related Services
              </h2>
              <p className="mt-4 text-lg text-muted-foreground">
                Explore other services in the {service.category} category
              </p>
            </div>
            
            <div className="grid gap-6 md:grid-cols-3">
              {relatedServices.map((relatedService) => (
                <Link key={relatedService.id} href={`/services/${relatedService.slug}`}>
                  <Card className="hover:shadow-lg transition-shadow cursor-pointer group">
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <div className="text-3xl">{relatedService.icon}</div>
                        <Badge variant="secondary">{relatedService.badge}</Badge>
                      </div>
                      <CardTitle className="group-hover:text-primary transition-colors">
                        {relatedService.title}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-muted-foreground mb-4 line-clamp-3">
                        {relatedService.service_description}
                      </p>
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-primary">
                          From {relatedService.price_data.starting_price}/{relatedService.price_data.billing_period}
                        </span>
                        <ArrowRight className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="py-16 bg-primary text-primary-foreground">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Ready to Get Started?
            </h2>
            <p className="mt-4 text-lg opacity-90">
              Join thousands of businesses already using our {service.title.toLowerCase()} solutions.
            </p>
            
            <div className="mt-8 flex items-center justify-center gap-4">
              <div className="flex items-center space-x-1">
                {[1,2,3,4,5].map((star) => (
                  <Star key={star} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                ))}
                <span className="ml-2 text-sm opacity-75">4.9/5 from 1,000+ reviews</span>
              </div>
            </div>
            
            <div className="mt-8">
              <Link href="/auth/login">
                <Button size="lg" variant="secondary" className="px-12">
                  Start Your Free Trial Today
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-muted/30">
        <div className="container py-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Image
                src="/bizoholic-logo-hq.png"
                alt="Bizoholic Digital Logo"
                width={32}
                height={32}
                className="h-6 w-auto"
              />
              <span className="font-semibold text-foreground">Bizoholic Digital</span>
            </div>
            
            <p className="text-sm text-muted-foreground">
              © 2024 Bizoholic Digital. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}