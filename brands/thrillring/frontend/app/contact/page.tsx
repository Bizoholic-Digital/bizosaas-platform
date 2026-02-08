import { Metadata } from 'next'
import Link from 'next/link'
import { ArrowRight, Mail, Phone, MapPin, Clock, Bot } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { ContactForm } from '@/components/contact/ContactForm'

export const metadata: Metadata = {
  title: 'Contact Us - Bizoholic Digital | Get Your Free AI Marketing Consultation',
  description: 'Ready to revolutionize your marketing with AI? Contact our experts for a free consultation and discover how autonomous marketing can transform your business.',
}

const contactInfo = [
  {
    icon: Mail,
    title: 'Email Us',
    description: 'Get in touch for partnerships and inquiries',
    detail: 'hello@bizoholic.com',
    action: 'mailto:hello@bizoholic.com'
  },
  {
    icon: Phone,
    title: 'Call Us',
    description: 'Speak directly with our AI marketing experts',
    detail: '+1 (555) 123-4567',
    action: 'tel:+15551234567'
  },
  {
    icon: MapPin,
    title: 'Visit Us',
    description: 'Our headquarters and innovation center',
    detail: 'San Francisco, CA',
    action: null
  },
  {
    icon: Clock,
    title: 'Business Hours',
    description: 'We\'re here when you need us',
    detail: 'Mon-Fri: 9AM-6PM PST',
    action: null
  },
]

const consultationTypes = [
  {
    title: 'Free Strategy Consultation',
    description: 'Get personalized recommendations for your marketing challenges',
    duration: '45 minutes',
    price: 'Free',
    features: [
      'Marketing audit & analysis',
      'AI opportunities assessment',
      'Custom strategy recommendations',
      'ROI projections'
    ]
  },
  {
    title: 'Platform Demo',
    description: 'See our BizoSaaS platform in action with your data',
    duration: '30 minutes',
    price: 'Free',
    features: [
      'Live platform demonstration',
      'Custom use case walkthrough',
      'Integration possibilities',
      'Q&A session'
    ]
  },
  {
    title: 'Technical Deep Dive',
    description: 'Detailed technical discussion for enterprise implementations',
    duration: '60 minutes',
    price: 'Free',
    features: [
      'Architecture overview',
      'Security & compliance',
      'Integration requirements',
      'Implementation timeline'
    ]
  },
]

export default function ContactPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      {/* Hero Section */}
      <section className="relative py-20 md:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5" />
        <div className="container relative">
          <div className="mx-auto max-w-3xl text-center">
            <Badge variant="outline" className="mb-6">
              Let's Talk Business
            </Badge>
            
            <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
              Ready to Transform
              <span className="text-primary"> Your Marketing?</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-muted-foreground mb-8">
              Get your free consultation with our AI marketing experts and discover 
              how autonomous marketing can revolutionize your business growth.
            </p>
            
            <Badge variant="secondary" className="text-sm">
              ✨ Free Strategy Session • No Commitment Required
            </Badge>
          </div>
        </div>
      </section>

      {/* Contact Methods */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              <span className="text-primary">Get in Touch</span>
            </h2>
            <p className="text-lg text-muted-foreground">
              Choose the best way to connect with our team of AI marketing experts.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {contactInfo.map((info, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <info.icon className="h-12 w-12 text-primary mx-auto mb-4" />
                  <CardTitle className="text-xl">{info.title}</CardTitle>
                  <CardDescription>{info.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  {info.action ? (
                    <a 
                      href={info.action}
                      className="text-lg font-semibold text-primary hover:text-primary/80 transition-colors"
                    >
                      {info.detail}
                    </a>
                  ) : (
                    <div className="text-lg font-semibold">{info.detail}</div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Consultation Types */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Free <span className="text-primary">Consultations</span>
            </h2>
            <p className="text-lg text-muted-foreground">
              Choose the type of consultation that best fits your needs and goals.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {consultationTypes.map((consultation, index) => (
              <Card key={index} className="relative hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between mb-4">
                    <Badge variant="secondary" className="text-xs">
                      {consultation.duration}
                    </Badge>
                    <Badge variant="outline" className="text-xs text-green-600 border-green-600">
                      {consultation.price}
                    </Badge>
                  </div>
                  <CardTitle className="text-xl mb-2">{consultation.title}</CardTitle>
                  <CardDescription className="text-base">
                    {consultation.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 mb-6">
                    {consultation.features.map((feature, i) => (
                      <li key={i} className="flex items-center gap-2 text-sm">
                        <div className="w-1.5 h-1.5 bg-primary rounded-full" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                  <Button className="w-full">
                    Schedule Now
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Form */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="grid lg:grid-cols-2 gap-12 items-start">
            <ContactForm />
          </div>
        </div>
      </section>

      {/* Quick Actions */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Or get started right now
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Ready to experience the power of autonomous marketing? 
              Start your free trial or explore our platform.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/auth/register">
                <Button size="lg" className="btn-gradient">
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/bizosaas">
                <Button variant="outline" size="lg">
                  Explore Platform
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