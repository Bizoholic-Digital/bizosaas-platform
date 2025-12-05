import { Metadata } from 'next'
import Link from 'next/link'
import { ArrowRight, Bot, Users, Target, Award, Lightbulb, TrendingUp } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'

export const metadata: Metadata = {
  title: 'About Us - Bizoholic Digital | AI-First Marketing Agency',
  description: 'Learn about our mission to revolutionize business growth through cutting-edge AI technology and autonomous marketing solutions.',
}

const values = [
  {
    icon: Bot,
    title: 'AI-First Innovation',
    description: 'We believe in the transformative power of artificial intelligence to solve complex business challenges.',
  },
  {
    icon: Users,
    title: 'Client Success',
    description: 'Your success is our success. We measure our impact by the growth and achievements of our clients.',
  },
  {
    icon: Target,
    title: 'Results-Driven',
    description: 'Every strategy, campaign, and decision is focused on delivering measurable results and ROI.',
  },
  {
    icon: Lightbulb,
    title: 'Continuous Learning',
    description: 'We stay at the forefront of technology and marketing trends to provide cutting-edge solutions.',
  },
]

const achievements = [
  { metric: '300%', label: 'Average ROI Increase' },
  { metric: '500+', label: 'Successful Projects' },
  { metric: '28+', label: 'AI Agents Developed' },
  { metric: '85%', label: 'Cost Reduction' },
]

export default function AboutPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      {/* Hero Section */}
      <section className="relative py-20 md:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5" />
        <div className="container relative">
          <div className="mx-auto max-w-3xl text-center">
            <Badge variant="outline" className="mb-6">
              About Bizoholic Digital
            </Badge>
            
            <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
              Pioneering the Future of 
              <span className="text-primary"> AI-Driven Marketing</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-muted-foreground mb-8">
              We're not just a marketing agency - we're innovation architects, 
              building autonomous solutions that revolutionize how businesses grow and succeed.
            </p>
          </div>
        </div>
      </section>

      {/* Story Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Our <span className="text-primary">Mission</span>
              </h2>
              <p className="text-lg text-muted-foreground mb-6">
                Founded with a vision to democratize advanced marketing technology, 
                Bizoholic Digital emerged from the belief that every business deserves 
                access to enterprise-level AI-powered marketing solutions.
              </p>
              <p className="text-lg text-muted-foreground mb-8">
                Our team of AI researchers, marketing strategists, and technology 
                experts work tirelessly to create autonomous systems that don't just 
                execute campaigns - they think, learn, and optimize continuously.
              </p>
              <Link href="/contact">
                <Button size="lg">
                  Start Your Transformation
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
            <div className="grid grid-cols-2 gap-4">
              {achievements.map((achievement, index) => (
                <div key={index} className="text-center p-6 bg-background rounded-lg shadow-sm">
                  <div className="text-3xl font-bold text-primary mb-2">
                    {achievement.metric}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {achievement.label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Our <span className="text-primary">Core Values</span>
            </h2>
            <p className="text-lg text-muted-foreground">
              The principles that guide everything we do and every solution we create.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {values.map((value, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center gap-4 mb-4">
                    <value.icon className="h-12 w-12 text-primary" />
                    <CardTitle className="text-xl">{value.title}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {value.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Built by <span className="text-primary">Experts</span>
            </h2>
            <p className="text-lg text-muted-foreground">
              Our diverse team combines deep technical expertise with creative marketing 
              insight to deliver breakthrough solutions.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-24 h-24 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <Bot className="h-12 w-12 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">AI Research Team</h3>
              <p className="text-muted-foreground">
                PhD-level researchers developing cutting-edge AI agents and automation systems.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-24 h-24 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <TrendingUp className="h-12 w-12 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Marketing Strategists</h3>
              <p className="text-muted-foreground">
                Industry veterans with decades of experience in digital marketing and growth.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-24 h-24 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <Award className="h-12 w-12 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Technology Leaders</h3>
              <p className="text-muted-foreground">
                Full-stack engineers and architects building scalable, enterprise-grade platforms.
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
              Ready to join the AI revolution?
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Let's discuss how our autonomous marketing solutions can transform 
              your business and drive unprecedented growth.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contact">
                <Button size="lg" className="btn-gradient">
                  Schedule Free Consultation
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
      
      <Footer />
    </div>
  )
}