'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, Bot, BarChart3, Search, Mail, Share2, PenTool } from 'lucide-react'

// Icon mapping for dynamic content
const iconMap: Record<string, any> = {
  'Bot': Bot,
  'BarChart3': BarChart3,
  'Search': Search,
  'Mail': Mail,
  'Share2': Share2,
  'PenTool': PenTool,
}

const fallbackServices = [
  {
    title: 'AI Campaign Management',
    description: 'Autonomous AI agents that create, optimize, and manage your marketing campaigns across all platforms 24/7.',
    icon: 'Bot',
    href: '/services/ai-campaign-management',
    badge: 'AI-First'
  },
  {
    title: 'Performance Analytics',
    description: 'Advanced AI-powered analytics that provide deep insights into campaign performance and ROI optimization.',
    icon: 'BarChart3',
    href: '/services/performance-analytics',
    badge: 'Data-Driven'
  },
  {
    title: 'SEO Optimization',
    description: 'Dominate search rankings with intelligent SEO strategies, content optimization, and automated link building.',
    icon: 'Search',
    href: '/services/seo-optimization',
    badge: 'Growth'
  },
  {
    title: 'Content Generation',
    description: 'Create high-quality, engaging content for your blog, social media, and email campaigns in seconds.',
    icon: 'PenTool',
    href: '/services/content-generation',
    badge: 'Creative'
  },
  {
    title: 'Social Media Marketing',
    description: 'Build your brand presence with automated content creation, posting schedules, and engagement strategies.',
    icon: 'Share2',
    href: '/services/social-media-marketing',
    badge: 'Social'
  },
  {
    title: 'Email Marketing',
    description: 'Personalized email campaigns that nurture leads and drive conversions with AI-powered optimization.',
    icon: 'Mail',
    href: '/services/email-marketing',
    badge: 'Conversion'
  }
]

export default function ServicesPage() {
  const [services, setServices] = useState(fallbackServices)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const response = await fetch('/api/brain/wagtail/services')
        if (response.ok) {
          const data = await response.json()
          if (data.services && data.services.length > 0) {
            // Map CMS services to component format
            const mappedServices = data.services.map((service: any) => ({
              title: service.title,
              description: service.service_description || service.description,
              icon: service.icon || 'Bot',
              href: `/services/${service.slug}`,
              badge: service.badge || service.category
            }))
            setServices(mappedServices)
          }
        }
      } catch (error) {
        console.error('Error fetching services:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchServices()
  }, [])

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      {/* Hero Section */}
      <section className="py-20 bg-muted/30">
        <div className="container text-center">
          <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl mb-6">
            Our AI-Powered Services
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
            Comprehensive digital marketing solutions powered by advanced artificial intelligence to scale your business.
          </p>
          <div className="flex justify-center gap-4">
            <Link href="http://localhost:3003/register">
              <Button size="lg" className="btn-gradient">
                Get Started
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/contact">
              <Button variant="outline" size="lg">
                Contact Sales
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-20">
        <div className="container">
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {services.map((service, index) => {
              const IconComponent = typeof service.icon === 'string' ? iconMap[service.icon] || Bot : service.icon
              return (
                <Link key={index} href={service.href} className="group">
                  <Card className="h-full transition-all hover:shadow-lg hover:border-primary/50">
                    <CardHeader>
                      <div className="flex items-center justify-between mb-4">
                        <div className="p-3 rounded-lg bg-primary/10 text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                          <IconComponent className="h-6 w-6" />
                        </div>
                        <Badge variant="secondary">{service.badge}</Badge>
                      </div>
                      <CardTitle className="text-xl group-hover:text-primary transition-colors">
                        {service.title}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-base mb-4">
                        {service.description}
                      </CardDescription>
                      <div className="flex items-center text-sm font-medium text-primary">
                        Learn more <ArrowRight className="ml-1 h-4 w-4 transition-transform group-hover:translate-x-1" />
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              )
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary text-primary-foreground">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Transform Your Marketing?</h2>
          <p className="text-xl opacity-90 mb-10 max-w-2xl mx-auto">
            Join thousands of businesses using our AI platform to drive growth and efficiency.
          </p>
          <Link href="http://localhost:3003/register">
            <Button size="lg" variant="secondary" className="px-8">
              Start Free Trial
            </Button>
          </Link>
        </div>
      </section>

      <Footer />
    </div>
  )
}
