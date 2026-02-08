/**
 * Static Homepage Component
 * Original Bizoholic website homepage content as a reusable component
 */

"use client"

import Link from 'next/link'
import { ArrowRight, Bot, Lightbulb, TrendingUp, Users, Zap, Target, BarChart } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { useEffect, useState } from 'react'
import { strapiAPI, Service } from '@/lib/strapi'

// Icon mapping for Strapi services
const iconMap: Record<string, any> = {
  Bot,
  TrendingUp,
  Target,
  BarChart,
  Lightbulb,
  Users,
  Zap,
}

// Digital Marketing Services with AI + Expert Based Solutions
const digitalMarketingServices = [
  {
    icon: TrendingUp,
    title: 'SEO (Search Engine Optimization)',
    description: 'AI-powered keyword research, content optimization, and technical SEO combined with expert strategy to dominate search rankings.',
    badge: 'AI + Expert Based Solution',
    link: '/services/seo'
  },
  {
    icon: Target,
    title: 'SEM (Search Engine Marketing)',
    description: 'Intelligent Google Ads and Bing Ads management with AI bid optimization and expert campaign strategy for maximum ROI.',
    badge: 'AI + Expert Based Solution',
    link: '/services/sem'
  },
  {
    icon: Users,
    title: 'Social Media Marketing',
    description: 'Automated content creation, posting schedules, and engagement strategies powered by AI with expert social media guidance.',
    badge: 'AI + Expert Based Solution',
    link: '/services/social-media-marketing'
  },
  {
    icon: Zap,
    title: 'Social Media Optimization',
    description: 'AI-driven profile optimization, hashtag research, and engagement analysis combined with expert brand positioning.',
    badge: 'AI + Expert Based Solution',
    link: '/services/social-media-optimization'
  },
  {
    icon: Bot,
    title: 'Email Marketing',
    description: 'Intelligent email automation, personalization, and A/B testing powered by AI with expert copywriting and strategy.',
    badge: 'AI + Expert Based Solution',
    link: '/services/email-marketing'
  },
  {
    icon: Lightbulb,
    title: 'Content Marketing',
    description: 'AI-generated content ideas, automated blog writing, and content optimization guided by expert content strategists.',
    badge: 'AI + Expert Based Solution',
    link: '/services/content-marketing'
  },
  {
    icon: BarChart,
    title: 'App Store Optimization',
    description: 'AI-powered ASO keyword research, app description optimization, and performance tracking with expert mobile marketing insights.',
    badge: 'AI + Expert Based Solution',
    link: '/services/app-store-optimization'
  },
]

// Additional services for expanded offering
const additionalServices = [
  {
    icon: Bot,
    title: 'AI Marketing Automation',
    description: 'Complete marketing automation with 28+ specialized AI agents working autonomously to optimize your campaigns.',
    badge: 'AI-First'
  },
  {
    icon: TrendingUp,
    title: 'Business Growth Strategy',
    description: 'Strategic consulting and growth planning with AI-driven insights and expert recommendations.',
    badge: 'Strategic'
  },
]

const benefits = [
  { value: '300%', label: 'ROI Increase', sublabel: 'Average client growth' },
  { value: '85%', label: 'Cost Reduction', sublabel: 'Marketing efficiency' },
  { value: '24/7', label: 'AI Operations', sublabel: 'Autonomous work' },
  { value: '500+', label: 'Happy Clients', sublabel: 'Success stories' },
]

export default function StaticHomePage() {
  const [services, setServices] = useState<any[]>([...digitalMarketingServices, ...additionalServices])
  const [loading, setLoading] = useState(false)
  
  useEffect(() => {
    // Enhanced service loading with proper fallback
    console.log('Initializing digital marketing services...')
    
    // Set services immediately with fallback data to prevent loading state issues
    setServices([...digitalMarketingServices, ...additionalServices])
    setLoading(false)
    
    // Optionally try to enhance with Strapi data in the background
    const enhanceWithStrapiData = async () => {
      try {
        const strapiServices = await strapiAPI.services.getAll('bizoholic')
        
        if (strapiServices && strapiServices.length >= 7) {
          const transformedServices = strapiServices.map((service: Service) => ({
            icon: iconMap[service.icon || 'Bot'] || Bot,
            title: service.title,
            description: service.description,
            badge: service.badge || service.category || 'AI + Expert Based Solution',
            link: service.title === 'SEO (Search Engine Optimization)' ? '/services/seo' :
                  service.title === 'SEM (Search Engine Marketing)' ? '/services/sem' :
                  service.title === 'Social Media Marketing' ? '/services/social-media-marketing' :
                  service.title === 'Social Media Optimization' ? '/services/social-media-optimization' :
                  service.title === 'Email Marketing' ? '/services/email-marketing' :
                  service.title === 'Content Marketing' ? '/services/content-marketing' :
                  service.title === 'App Store Optimization' ? '/services/app-store-optimization' :
                  undefined
          }))
          console.log('Enhanced with Strapi services:', transformedServices.length)
          setServices(transformedServices)
        }
      } catch (error) {
        console.log('Strapi enhancement failed, keeping fallback services:', error)
      }
    }
    
    // Run enhancement in background without affecting initial render
    enhanceWithStrapiData()
  }, [])
  
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      {/* Hero Section */}
      <section className="relative py-20 md:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5" />
        <div className="container relative">
          <div className="mx-auto max-w-4xl text-center">
            <Badge variant="outline" className="mb-6">
              🚀 AI-First Marketing Agency
            </Badge>
            
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6">
              Revolutionizing 
              <span className="text-primary"> Businesses</span>
              <br />
              with AI-Powered
              <br />
              <span className="text-primary">Solutions</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Transform your business with cutting-edge AI-powered strategies and solutions. 
              We're not just a marketing agency - we're your innovation partner.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <Link href="/contact">
                <Button size="lg" className="btn-gradient">
                  Get Free Consultation
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/bizosaas">
                <Button variant="outline" size="lg">
                  Explore Our Platform
                </Button>
              </Link>
            </div>
            
            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-3xl mx-auto">
              {benefits.map((benefit, index) => (
                <div key={index} className="text-center">
                  <div className="text-2xl md:text-3xl font-bold text-primary mb-1">
                    {benefit.value}
                  </div>
                  <div className="text-sm font-medium mb-1">{benefit.label}</div>
                  <div className="text-xs text-muted-foreground">{benefit.sublabel}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="py-20 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Our <span className="text-primary">AI-Powered</span> Services
            </h2>
            <p className="text-lg text-muted-foreground">
              We combine human creativity with artificial intelligence to deliver 
              unprecedented results for your business growth.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {loading ? (
              // Loading skeleton
              Array.from({ length: 6 }).map((_, index) => (
                <Card key={`skeleton-${index}`} className="relative">
                  <CardHeader>
                    <div className="flex items-center justify-between mb-4">
                      <div className="h-10 w-10 bg-muted rounded-md animate-pulse" />
                      <div className="h-6 w-16 bg-muted rounded-full animate-pulse" />
                    </div>
                    <div className="h-6 w-32 bg-muted rounded animate-pulse" />
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="h-4 w-full bg-muted rounded animate-pulse" />
                      <div className="h-4 w-3/4 bg-muted rounded animate-pulse" />
                      <div className="h-4 w-1/2 bg-muted rounded animate-pulse" />
                    </div>
                  </CardContent>
                </Card>
              ))
            ) : (
              services.map((service, index) => {
                const ServiceCard = service.link ? 
                  ({ children }: { children: React.ReactNode }) => (
                    <Link href={service.link}>
                      <Card className="relative hover:shadow-lg transition-shadow cursor-pointer group">
                        {children}
                      </Card>
                    </Link>
                  ) :
                  ({ children }: { children: React.ReactNode }) => (
                    <Card className="relative hover:shadow-lg transition-shadow">
                      {children}
                    </Card>
                  )

                return (
                  <ServiceCard key={index}>
                    <CardHeader>
                      <div className="flex items-center justify-between mb-4">
                        <service.icon className="h-10 w-10 text-primary group-hover:scale-110 transition-transform" />
                        <Badge 
                          variant={service.badge === 'AI + Expert Based Solution' ? 'default' : 'secondary'} 
                          className="text-xs"
                        >
                          {service.badge}
                        </Badge>
                      </div>
                      <CardTitle className="text-xl group-hover:text-primary transition-colors">
                        {service.title}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-base mb-4">
                        {service.description}
                      </CardDescription>
                      {service.link && (
                        <div className="flex items-center text-primary text-sm font-medium group-hover:gap-2 transition-all">
                          Learn More <ArrowRight className="ml-1 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                        </div>
                      )}
                    </CardContent>
                  </ServiceCard>
                )
              })
            )}
          </div>
        </div>
      </section>

      {/* Platform Highlight */}
      <section className="py-20">
        <div className="container">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <Badge variant="outline" className="mb-4">
                Introducing BizoSaaS Platform
              </Badge>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Meet Our 
                <span className="text-primary"> Autonomous Marketing Platform</span>
              </h2>
              <p className="text-lg text-muted-foreground mb-8">
                Our flagship product - BizoSaaS - is an autonomous AI marketing platform 
                powered by 28+ specialized agents. It handles everything from strategy 
                creation to campaign optimization, working 24/7 for your success.
              </p>
              <div className="space-y-4 mb-8">
                <div className="flex items-start gap-3">
                  <Bot className="h-6 w-6 text-primary mt-0.5" />
                  <div>
                    <h4 className="font-semibold">28+ AI Marketing Agents</h4>
                    <p className="text-muted-foreground">Specialized agents for every marketing task</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <Zap className="h-6 w-6 text-primary mt-0.5" />
                  <div>
                    <h4 className="font-semibold">Autonomous Operation</h4>
                    <p className="text-muted-foreground">Works 24/7 without human intervention</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <BarChart className="h-6 w-6 text-primary mt-0.5" />
                  <div>
                    <h4 className="font-semibold">Real-time Analytics</h4>
                    <p className="text-muted-foreground">Live performance tracking and optimization</p>
                  </div>
                </div>
              </div>
              <Link href="/bizosaas">
                <Button size="lg">
                  Explore BizoSaaS Platform
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
            <div className="bg-gradient-to-br from-primary/10 to-accent/10 rounded-2xl p-8 text-center">
              <Bot className="h-24 w-24 text-primary mx-auto mb-6" />
              <h3 className="text-2xl font-bold mb-4">Ready to Experience AI Marketing?</h3>
              <p className="text-muted-foreground mb-6">
                See how our AI agents can transform your marketing campaigns
              </p>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="bg-background/50 rounded-lg p-3">
                  <div className="font-bold text-primary">Campaign Strategy</div>
                  <div className="text-muted-foreground">AI-powered</div>
                </div>
                <div className="bg-background/50 rounded-lg p-3">
                  <div className="font-bold text-primary">Content Creation</div>
                  <div className="text-muted-foreground">Automated</div>
                </div>
                <div className="bg-background/50 rounded-lg p-3">
                  <div className="font-bold text-primary">Performance Analysis</div>
                  <div className="text-muted-foreground">Real-time</div>
                </div>
                <div className="bg-background/50 rounded-lg p-3">
                  <div className="font-bold text-primary">Optimization</div>
                  <div className="text-muted-foreground">Continuous</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to revolutionize your business?
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Let's discuss how our AI-powered solutions can transform your business 
              and drive unprecedented growth.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contact">
                <Button size="lg" className="btn-gradient">
                  Schedule Free Consultation
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/about">
                <Button variant="outline" size="lg">
                  Learn About Us
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