import { Metadata } from 'next'
import Link from 'next/link'
import { ArrowRight, Bot, BarChart3, Users, Zap, Shield, Globe } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'

export const metadata: Metadata = {
  title: 'BizoSaaS Platform - Autonomous AI Marketing Automation',
  description: 'Advanced AI-powered marketing automation platform with 28+ specialized agents, real-time analytics, and enterprise-grade security.',
}

const features = [
  {
    icon: Bot,
    title: 'AI Agent Orchestration',
    description: 'Intelligent agents handle campaign creation, optimization, and analysis autonomously.',
    badge: 'CrewAI Powered'
  },
  {
    icon: BarChart3,
    title: 'Real-time Analytics',
    description: 'Advanced reporting with predictive insights and performance optimization recommendations.',
    badge: 'Live Data'
  },
  {
    icon: Users,
    title: 'Multi-tenant CRM',
    description: 'Complete customer relationship management with lead scoring and pipeline automation.',
    badge: 'Enterprise Ready'
  },
  {
    icon: Zap,
    title: 'Campaign Automation',
    description: 'Automated Google Ads, Meta Ads, and LinkedIn campaigns with AI optimization.',
    badge: 'Multi-platform'
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
]

const stats = [
  { value: '10,000+', label: 'Active Users', sublabel: 'Growing monthly' },
  { value: '98.5%', label: 'Automation Rate', sublabel: 'Tasks automated' },
  { value: '40%', label: 'Cost Reduction', sublabel: 'Average savings' },
  { value: '2.3x', label: 'ROI Increase', sublabel: 'Campaign performance' },
]

const agents = [
  { name: 'Campaign Strategy Agent', description: 'Creates comprehensive marketing strategies' },
  { name: 'Content Creation Agent', description: 'Generates compelling ad copy and content' },
  { name: 'Performance Analytics Agent', description: 'Analyzes and optimizes campaign performance' },
  { name: 'Audience Targeting Agent', description: 'Identifies and segments target audiences' },
  { name: 'Budget Optimization Agent', description: 'Optimizes ad spend across platforms' },
  { name: 'A/B Testing Agent', description: 'Runs continuous optimization experiments' },
]

export default function BizoSaaSPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      {/* Hero Section */}
      <section className="relative py-20 md:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5" />
        <div className="container relative">
          <div className="mx-auto max-w-4xl text-center">
            <Badge variant="outline" className="mb-6">
              🚀 Now with CrewAI Integration
            </Badge>
            
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6">
              BizoSaaS
              <span className="text-primary"> Platform</span>
              <br />
              <span className="text-2xl md:text-3xl lg:text-4xl text-muted-foreground font-normal">
                Autonomous AI Marketing Automation
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Transform your marketing with 28+ specialized AI agents, intelligent campaign optimization, 
              and autonomous decision-making that works 24/7.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <Link href="/auth/register">
                <Button size="lg" className="btn-gradient">
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/demo">
                <Button variant="outline" size="lg">
                  Watch Demo
                </Button>
              </Link>
            </div>
            
            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-3xl mx-auto">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-2xl md:text-3xl font-bold text-primary mb-1">
                    {stat.value}
                  </div>
                  <div className="text-sm font-medium mb-1">{stat.label}</div>
                  <div className="text-xs text-muted-foreground">{stat.sublabel}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* AI Agents Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              <span className="text-primary">28+ Specialized AI Agents</span>
              <br />
              Working for Your Success
            </h2>
            <p className="text-lg text-muted-foreground">
              Each agent is trained for specific marketing tasks, collaborating intelligently
              to deliver unprecedented automation and results.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            {agents.map((agent, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    <Bot className="h-5 w-5 text-primary" />
                    {agent.name}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{agent.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="text-center">
            <Badge variant="secondary" className="text-sm px-4 py-2">
              + 22 More Specialized Agents for Complete Marketing Automation
            </Badge>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Everything you need for
              <span className="text-primary"> autonomous marketing</span>
            </h2>
            <p className="text-lg text-muted-foreground">
              Built with cutting-edge AI technology and enterprise-grade infrastructure
              for modern marketing teams.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="relative hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between mb-4">
                    <feature.icon className="h-10 w-10 text-primary" />
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
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to automate your marketing?
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Join thousands of businesses already using BizoSaaS platform to automate 
              and optimize their marketing campaigns with AI agents.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/auth/register">
                <Button size="lg" className="btn-gradient">
                  Start Your Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/contact">
                <Button variant="outline" size="lg">
                  Schedule Demo
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