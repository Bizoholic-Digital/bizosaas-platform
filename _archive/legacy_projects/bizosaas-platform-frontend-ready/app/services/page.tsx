import { Metadata } from 'next'
import Link from 'next/link'
import { ArrowRight, Bot, Target, TrendingUp, BarChart, Lightbulb, Users, Zap, Shield, Globe } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'

export const metadata: Metadata = {
  title: 'Services - Bizoholic Digital | AI-Powered Marketing Solutions',
  description: 'Discover our comprehensive suite of AI-powered marketing services designed to revolutionize your business growth and digital presence.',
}

const agencyServices = [
  {
    icon: Bot,
    title: 'AI-Powered Digital Marketing',
    description: 'Complete digital marketing campaigns managed by autonomous AI agents that work 24/7 to optimize your results.',
    features: ['Automated campaign creation', 'Real-time optimization', 'Cross-platform management', 'Performance reporting'],
    badge: 'AI-First'
  },
  {
    icon: TrendingUp,
    title: 'Business Growth Strategy',
    description: 'Strategic consulting and growth planning with AI-driven insights to identify opportunities and scale your business.',
    features: ['Market analysis', 'Growth planning', 'Competitive intelligence', 'Strategic roadmaps'],
    badge: 'Strategic'
  },
  {
    icon: Target,
    title: 'Campaign Optimization',
    description: 'Advanced campaign management across Google Ads, Meta, LinkedIn, and other platforms with AI optimization.',
    features: ['Multi-platform campaigns', 'Budget optimization', 'Audience targeting', 'Creative testing'],
    badge: 'Multi-platform'
  },
  {
    icon: BarChart,
    title: 'Advanced Analytics',
    description: 'Real-time performance tracking with predictive analytics and actionable optimization recommendations.',
    features: ['Real-time dashboards', 'Predictive insights', 'Custom reporting', 'ROI tracking'],
    badge: 'Real-time'
  },
  {
    icon: Lightbulb,
    title: 'Innovation Consulting',
    description: 'Transform your business processes with cutting-edge AI technology and automation solutions.',
    features: ['Process automation', 'AI integration', 'Digital transformation', 'Technology roadmaps'],
    badge: 'Innovation'
  },
  {
    icon: Users,
    title: 'Customer Success',
    description: 'Dedicated support and success management to ensure you achieve your growth objectives.',
    features: ['Dedicated success manager', '24/7 support', 'Training & onboarding', 'Performance reviews'],
    badge: 'Support'
  },
]

const platformFeatures = [
  {
    icon: Bot,
    title: 'AI Agent Orchestration',
    description: '28+ specialized agents handling campaign creation, optimization, and analysis autonomously.',
    badge: 'CrewAI Powered'
  },
  {
    icon: Shield,
    title: 'Enterprise Security',
    description: 'SOC 2 compliant with advanced encryption, audit trails, and access controls.',
    badge: 'SOC 2'
  },
  {
    icon: Globe,
    title: 'Global Scale',
    description: 'Cloud-native architecture built for scale with 99.9% uptime guarantee.',
    badge: 'Kubernetes'
  },
  {
    icon: Zap,
    title: 'Real-time Processing',
    description: 'Lightning-fast data processing and campaign adjustments in real-time.',
    badge: 'High Performance'
  },
]

export default function ServicesPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      {/* Hero Section */}
      <section className="relative py-20 md:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5" />
        <div className="container relative">
          <div className="mx-auto max-w-3xl text-center">
            <Badge variant="outline" className="mb-6">
              Our Services & Solutions
            </Badge>
            
            <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
              AI-Powered Marketing
              <span className="text-primary"> Services</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-muted-foreground mb-8">
              From strategic consulting to autonomous marketing automation, 
              we provide comprehensive solutions to accelerate your business growth.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contact">
                <Button size="lg" className="btn-gradient">
                  Get Started Today
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/bizosaas">
                <Button variant="outline" size="lg">
                  Explore Our Platform
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Agency Services */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Full-Service <span className="text-primary">Marketing Agency</span>
            </h2>
            <p className="text-lg text-muted-foreground">
              Comprehensive marketing services powered by AI technology to drive your business forward.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {agencyServices.map((service, index) => (
              <Card key={index} className="relative hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between mb-4">
                    <service.icon className="h-10 w-10 text-primary" />
                    <Badge variant="secondary" className="text-xs">
                      {service.badge}
                    </Badge>
                  </div>
                  <CardTitle className="text-xl mb-2">{service.title}</CardTitle>
                  <CardDescription className="text-base mb-4">
                    {service.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-sm text-muted-foreground">
                    {service?.features?.map((feature, i) => (
                      <li key={i} className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 bg-primary rounded-full" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Platform Features */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              <span className="text-primary">BizoSaaS Platform</span> Features
            </h2>
            <p className="text-lg text-muted-foreground">
              Our autonomous marketing platform combines 28+ AI agents with enterprise-grade infrastructure.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8 mb-12">
            {platformFeatures.map((feature, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between mb-4">
                    <feature.icon className="h-12 w-12 text-primary" />
                    <Badge variant="secondary" className="text-xs">
                      {feature.badge}
                    </Badge>
                  </div>
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

          <div className="text-center">
            <Link href="/bizosaas">
              <Button size="lg" variant="outline">
                Learn More About Our Platform
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              How We <span className="text-primary">Work</span>
            </h2>
            <p className="text-lg text-muted-foreground">
              Our proven process ensures successful implementation and optimal results.
            </p>
          </div>
          
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-primary">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Discovery</h3>
              <p className="text-muted-foreground">
                We analyze your business, goals, and current marketing performance.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-primary">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Strategy</h3>
              <p className="text-muted-foreground">
                AI-driven strategy development tailored to your specific objectives.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-primary">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Implementation</h3>
              <p className="text-muted-foreground">
                Rapid deployment of AI agents and automation systems.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-primary">4</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Optimization</h3>
              <p className="text-muted-foreground">
                Continuous monitoring, learning, and optimization for maximum ROI.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to transform your marketing?
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Let's discuss which services and solutions are right for your business goals.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contact">
                <Button size="lg" className="btn-gradient">
                  Schedule Free Strategy Call
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
      
      <Footer />
    </div>
  )
}