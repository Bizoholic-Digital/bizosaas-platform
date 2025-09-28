/**
 * Bizoholic Homepage - Dynamic Content from Wagtail CMS
 * Content is managed through BizOSaaS dashboard and served via Brain API
 */

'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { useTenantTheme } from '@/hooks/useTenantTheme'
import { Logo } from '@/components/ui/logo'
import { 
  ArrowRight, 
  Bot, 
  Users, 
  Zap, 
  Target, 
  BarChart3, 
  Globe,
  CheckCircle,
  Star
} from 'lucide-react'

// Types for CMS data
interface HomepageContent {
  title: string
  hero_title: string
  hero_subtitle: string
  hero_cta_text: string
  hero_cta_url: string
  features_title: string
  features: Array<{
    icon: string
    title: string
    description: string
  }>
  stats?: Array<{
    number: string
    label: string
    description: string
  }>
  show_service_status: boolean
  tenant_id: string
}

interface ServicePage {
  id: number
  title: string
  slug: string
  icon: string
  badge: string
  category: string
  service_description: string
  featured: boolean
  order: number
  price_data: {
    starting_price: string
    currency: string
    billing_period: string
  }
}

interface BlogPost {
  id: number
  title: string
  slug: string
  excerpt: string
  featured_image?: string
  published_date: string
  author: string
  category: string
  tags: string[]
  read_time: number
  featured: boolean
}

export default function BizoholicHomepage() {
  const { config } = useTenantTheme()
  const [homepageContent, setHomepageContent] = useState<HomepageContent | null>(null)
  const [servicePages, setServicePages] = useState<ServicePage[]>([])
  const [blogPosts, setBlogPosts] = useState<BlogPost[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchHomepageContent()
  }, [])

  const fetchHomepageContent = async () => {
    try {
      setLoading(true)
      
      // Fetch homepage content, service pages, and blog posts from Brain API
      const [homepageRes, servicesRes, blogRes] = await Promise.all([
        fetch('/api/brain/wagtail/homepage'),
        fetch('/api/brain/wagtail/services'),
        fetch('/api/brain/wagtail/blog')
      ])
      
      if (homepageRes.ok) {
        const homepageData = await homepageRes.json()
        setHomepageContent(homepageData.homepage)
      }
      
      if (servicesRes.ok) {
        const servicesData = await servicesRes.json()
        // Get featured services for homepage display
        const featuredServices = servicesData.services?.filter((s: ServicePage) => s.featured) || []
        setServicePages(featuredServices.slice(0, 6))
      }
      
      if (blogRes.ok) {
        const blogData = await blogRes.json()
        // Get featured blog posts for homepage display
        const featuredPosts = blogData.posts?.filter((p: BlogPost) => p.featured) || []
        setBlogPosts(featuredPosts.slice(0, 3))
      }
    } catch (error) {
      console.error('Error fetching homepage content:', error)
      // Keep loading as false to show fallback content
    } finally {
      setLoading(false)
    }
  }

  // Fallback content if CMS is unavailable - using tenant-specific branding
  const fallbackContent: HomepageContent = {
    title: `${config.branding.companyName} - ${config.branding.tagline}`,
    hero_title: config.branding.companyName === 'BizOSaaS' ? 'Transform Your Business Operations with AI' : 'Transform Your Business with AI Marketing',
    hero_subtitle: config.branding.description || `${config.branding.companyName} empowers businesses with autonomous AI agents that handle marketing campaigns, content creation, SEO optimization, and lead generation - all running 24/7 on autopilot.`,
    hero_cta_text: "Start Free Trial",
    hero_cta_url: "/auth/login",
    features_title: config.branding.companyName === 'BizOSaaS' ? 'Everything You Need to Manage Your Business' : 'Everything You Need to Dominate Digital Marketing',
    features: [
      {
        icon: "🤖",
        title: "AI Campaign Management",
        description: "Autonomous agents create, optimize, and manage your advertising campaigns across Google Ads, Meta, LinkedIn, and 40+ other platforms."
      },
      {
        icon: "🎯",
        title: "Content Generation", 
        description: "AI-powered content creation for blogs, social media, email campaigns, and website copy that converts visitors into customers."
      },
      {
        icon: "📊",
        title: "Performance Analytics",
        description: "Real-time analytics and insights with automated reporting that helps you understand what's working and what needs optimization."
      }
    ],
    show_service_status: true,
    tenant_id: "bizoholic"
  }

  // Use CMS content if available, otherwise use fallback
  const content = homepageContent || fallbackContent

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header - Bizoholic branded */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center">
          <Logo 
            href="/" 
            priority={true}
            showText={false}
            width={120}
            height={32}
            className=""
          />
          
          <nav className="ml-auto flex items-center space-x-6">
            <Link href="/services" className="text-sm font-medium hover:text-primary">
              Services
            </Link>
            <Link href="/case-studies" className="text-sm font-medium hover:text-primary">
              Case Studies
            </Link>
            <Link href="/blog" className="text-sm font-medium hover:text-primary">
              Blog
            </Link>
            <Link href="/about" className="text-sm font-medium hover:text-primary">
              About
            </Link>
            <Link href="/contact" className="text-sm font-medium hover:text-primary">
              Contact
            </Link>
            <Link href="/auth/login">
              <Button size="sm">Get Started</Button>
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section - Dynamic content from Wagtail */}
      <section className="py-20 lg:py-28 bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <Badge variant="outline" className="mb-6">
              <Bot className="mr-2 h-3 w-3" />
              AI-Powered Marketing Automation
            </Badge>
            
            <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-7xl">
              {content.hero_title.split(' ').slice(0, -2).join(' ')}{' '}
              <span className="text-primary">{content.hero_title.split(' ').slice(-2).join(' ')}</span>
            </h1>
            
            <p className="mt-6 text-lg leading-8 text-muted-foreground max-w-2xl mx-auto">
              {content.hero_subtitle}
            </p>
            
            <div className="mt-10 flex items-center justify-center gap-6">
              <Link href={content.hero_cta_url}>
                <Button size="lg" className="px-8 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  {content.hero_cta_text}
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Button variant="outline" size="lg">
                Watch Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section - Dynamic content from Wagtail */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              {content.features_title}
            </h2>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {content.features.map((feature, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="text-4xl mb-4">{feature.icon}</div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Services Section - Dynamic from Wagtail CMS */}
      {servicePages.length > 0 && (
        <section className="py-20">
          <div className="container">
            <div className="mx-auto max-w-2xl text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Our <span className="text-primary">Services</span>
              </h2>
              <p className="text-lg text-muted-foreground">
                Comprehensive marketing solutions powered by AI technology
              </p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {servicePages.map((service) => (
                <Card key={service.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-3xl">{service.icon}</span>
                      <Badge variant="secondary">{service.badge}</Badge>
                    </div>
                    <CardTitle className="text-xl">{service.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground mb-4">{service.service_description}</p>
                    <div className="flex items-center justify-between">
                      <span className="font-semibold">
                        From {service.price_data.starting_price}
                      </span>
                      <Link href={`/services/${service.slug}`}>
                        <Button variant="outline" size="sm">
                          Learn More
                        </Button>
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Blog Section - Dynamic from Wagtail CMS */}
      {blogPosts.length > 0 && (
        <section className="py-20 bg-muted/30">
          <div className="container">
            <div className="mx-auto max-w-2xl text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Latest <span className="text-primary">Insights</span>
              </h2>
              <p className="text-lg text-muted-foreground">
                Stay updated with the latest marketing trends and strategies
              </p>
            </div>
            
            <div className="grid md:grid-cols-3 gap-8">
              {blogPosts.map((post) => (
                <Card key={post.id} className="hover:shadow-lg transition-shadow">
                  {post.featured_image && (
                    <div className="aspect-video relative overflow-hidden rounded-t-lg">
                      <Image
                        src={post.featured_image}
                        alt={post.title}
                        fill
                        className="object-cover"
                      />
                    </div>
                  )}
                  <CardHeader>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                      <span>{post.category}</span>
                      <span>•</span>
                      <span>{post.read_time} min read</span>
                    </div>
                    <CardTitle className="text-lg line-clamp-2">{post.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground line-clamp-3 mb-4">{post.excerpt}</p>
                    <Link href={`/blog/${post.slug}`}>
                      <Button variant="outline" size="sm">
                        Read More
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to transform your marketing?
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Join thousands of businesses already using AI to drive growth
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contact">
                <Button size="lg" className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  Start Free Consultation
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/auth/register">
                <Button variant="outline" size="lg">
                  Start Free Trial
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer - Bizoholic branded */}
      <footer className="border-t bg-background">
        <div className="container py-16">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-semibold mb-4">Services</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/services/seo">SEO Optimization</Link></li>
                <li><Link href="/services/content-marketing">Content Marketing</Link></li>
                <li><Link href="/services/social-media">Social Media</Link></li>
                <li><Link href="/services/ppc">PPC Management</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/about">About Us</Link></li>
                <li><Link href="/careers">Careers</Link></li>
                <li><Link href="/case-studies">Case Studies</Link></li>
                <li><Link href="/contact">Contact</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Resources</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/blog">Blog</Link></li>
                <li><Link href="/resources">Resources</Link></li>
                <li><Link href="/pricing">Pricing</Link></li>
                <li><Link href="/support">Support</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Legal</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/privacy">Privacy Policy</Link></li>
                <li><Link href="/terms">Terms of Service</Link></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t pt-8 mt-8 text-center text-sm text-muted-foreground">
            <p>&copy; 2024 {config.branding.companyName}. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}