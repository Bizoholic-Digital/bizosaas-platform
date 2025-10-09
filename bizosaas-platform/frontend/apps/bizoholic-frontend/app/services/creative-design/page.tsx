'use client'

/**
 * Creative Design Service Detail Page
 * Professional design services for all your marketing materials, from social media graphics to landing pages
 */

import { useEffect, useState } from 'react'
import Link from 'next/link'
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
  Palette,
  Image,
  Layers,
  FileImage,
  Monitor,
  Video,
  PenTool,
  Camera,
  Layout,
  Type
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

export default function CreativeDesignPage() {
  const [service, setService] = useState<ServiceData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchServiceData()
  }, [])

  const fetchServiceData = async () => {
    try {
      setLoading(true)
      
      // Try to fetch from Wagtail CMS first
      const response = await fetch('/api/brain/wagtail/services?slug=creative-design')
      
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
        id: "creative-design",
        title: "Creative Design",
        description: "Professional design services for all your marketing materials, from social media graphics to landing pages.",
        icon: "🎨",
        badge: "Creative",
        category: "Design & Branding",
        price_data: {
          starting_price: "₹14,999",
          currency: "INR",
          billing_period: "month"
        },
        features: [
          "Social Media Graphics & Templates",
          "Landing Page & Website Design",
          "Brand Identity & Logo Design",
          "Marketing Collateral Creation",
          "Email Template Design",
          "Video & Motion Graphics",
          "Print & Digital Advertising",
          "UI/UX Design & Prototyping"
        ],
        benefits: [
          "Professional brand consistency across channels",
          "Higher engagement with compelling visuals", 
          "Faster design turnaround with templates",
          "Cost-effective design solutions",
          "Scalable design systems and guidelines",
          "Expert design consultation and strategy"
        ],
        case_studies: [
          {
            client_name: "Fashion Retail Brand",
            industry: "E-commerce",
            results: "200% increase in social media engagement with new designs",
            metrics: "Click-through rate: +150%, Brand recall: +85%"
          },
          {
            client_name: "Tech Startup",
            industry: "SaaS",
            results: "300% improvement in landing page conversions",
            metrics: "Conversion rate: +185%, User engagement: +120%"
          }
        ],
        testimonials: [
          {
            client_name: "Emma Rodriguez",
            company: "Creative Studios",
            quote: "The design quality is exceptional. Our brand now has a professional, cohesive look across all channels that our customers love.",
            rating: 5
          },
          {
            client_name: "Alex Chen",
            company: "Design Forward",
            quote: "Fast turnaround, beautiful designs, and great communication. They understand our brand perfectly and deliver exactly what we need.",
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
                <Button size="lg" className="px-8 bg-primary text-primary-foreground hover:bg-primary/90">
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
                <Palette className="h-4 w-4 text-green-600" />
                <span>5000+ Designs Created</span>
              </div>
              <div className="flex items-center space-x-2">
                <Image className="h-4 w-4 text-green-600" />
                <span>50+ Design Formats</span>
              </div>
              <div className="flex items-center space-x-2">
                <Target className="h-4 w-4 text-green-600" />
                <span>24-Hour Turnaround</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Creative Design Campaign Types Section */}
      <section className="py-16">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Creative Design Campaign Types We Create
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Professional visual designs across all marketing channels and formats
            </p>
          </div>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Palette className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle className="text-lg">Brand Identity</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Logo design, color schemes, brand guidelines, and visual identity systems
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Layers className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle className="text-lg">Social Media Graphics</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Platform-specific posts, stories, covers, and promotional graphics
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <FileImage className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle className="text-lg">Marketing Collateral</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Brochures, flyers, banners, posters, and print advertising materials
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Monitor className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle className="text-lg">Web Design</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Landing pages, website layouts, UI/UX designs, and responsive interfaces
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Video className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle className="text-lg">Motion Graphics</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Animated videos, GIFs, motion logos, and dynamic visual content
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <PenTool className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle className="text-lg">Illustration</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Custom illustrations, icons, infographics, and artistic visual elements
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Camera className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle className="text-lg">Photo Editing</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Image retouching, background removal, color correction, and photo manipulation
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Layout className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle className="text-lg">Email Templates</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Responsive email designs, newsletters, promotional templates, and layouts
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-4xl">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                Comprehensive Design Features
              </h2>
              <p className="mt-4 text-lg text-muted-foreground">
                Everything you need for professional visual marketing
              </p>
            </div>

            <div className="grid gap-6 md:grid-cols-2 mb-12">
              {service?.features?.map((feature, index) => (
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
                {service?.benefits?.map((benefit, index) => (
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
                Real results from businesses using creative design services
              </p>
            </div>
            
            <div className="grid gap-8 md:grid-cols-2 mb-12">
              {service?.case_studies?.map((study, index) => (
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
              {service?.testimonials?.map((testimonial, index) => (
                <Card key={index} className="bg-muted/30">
                  <CardContent className="pt-6">
                    <div className="flex items-center mb-4">
                      {Array.from({ length: testimonial?.rating || 0 }).map((_, i) => (
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
                {service.price_data.starting_price}
              </div>
              <div className="text-muted-foreground mb-6">
                per {service.price_data.billing_period} • {service.price_data.currency}
              </div>
              <div className="space-y-3 mb-8">
                <Link href="/auth/register">
                  <Button size="lg" className="w-full bg-primary text-primary-foreground hover:bg-primary/90">
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
              Ready to Elevate Your Brand?
            </h2>
            <p className="mt-4 text-lg opacity-90">
              Join hundreds of businesses already using professional design services to stand out.
            </p>
            
            <div className="mt-8 flex items-center justify-center gap-4">
              <div className="flex items-center space-x-1">
                {[1,2,3,4,5].map((star) => (
                  <Star key={star} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                ))}
                <span className="ml-2 text-sm opacity-75">4.9/5 from 200+ reviews</span>
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