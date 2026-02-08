/**
 * CorelDove Contact Page - Customer Support and Business Inquiries
 * Integrates with Django CRM backend via Brain API for lead management
 */

'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'
import { Input } from '../../components/ui/input'
import { Badge } from '../../components/ui/badge'
import { useTenantTheme } from '../../hooks/useTenantTheme'
import Header from '../../components/navigation/header'
import Footer from '../../components/navigation/footer'
import { 
  ArrowRight, 
  ShoppingCart, 
  Send,
  Phone,
  Mail,
  MapPin,
  Clock,
  MessageCircle,
  Headphones,
  Users,
  Star,
  Package
} from 'lucide-react'

interface ContactForm {
  name: string
  email: string
  phone: string
  subject: string
  message: string
  inquiryType: 'general' | 'support' | 'business' | 'returns'
}

export default function ContactPage() {
  const { config } = useTenantTheme()
  
  const [formData, setFormData] = useState<ContactForm>({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: '',
    inquiryType: 'general'
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    try {
      // TODO: Integrate with Django CRM backend via Brain API
      const response = await fetch('/api/brain/crm/leads', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          source: 'contact_page',
          status: 'new',
          tags: ['website_inquiry', formData.inquiryType]
        }),
      })

      if (response.ok) {
        setSubmitStatus('success')
        setFormData({
          name: '',
          email: '',
          phone: '',
          subject: '',
          message: '',
          inquiryType: 'general'
        })
      } else {
        setSubmitStatus('error')
      }
    } catch (error) {
      console.error('Error submitting contact form:', error)
      setSubmitStatus('error')
    } finally {
      setIsSubmitting(false)
    }
  }

  const contactMethods = [
    {
      icon: Phone,
      title: 'Phone Support',
      description: 'Speak directly with our customer service team',
      value: '+1 (555) 123-4567',
      available: '24/7 Support Available',
      color: 'bg-blue-50 text-blue-600'
    },
    {
      icon: Mail,
      title: 'Email Support',
      description: 'Send us a detailed message for complex inquiries',
      value: 'support@coreldove.com',
      available: 'Response within 24 hours',
      color: 'bg-green-50 text-green-600'
    },
    {
      icon: MessageCircle,
      title: 'Live Chat',
      description: 'Get instant answers to your questions',
      value: 'Start Chat',
      available: 'Available Mon-Fri 9AM-6PM EST',
      color: 'bg-red-50 text-red-600'
    },
    {
      icon: Headphones,
      title: 'Technical Support',
      description: 'Specialized help for technical issues',
      value: 'technical@coreldove.com',
      available: 'Expert technicians standing by',
      color: 'bg-purple-50 text-purple-600'
    }
  ]

  const officeLocations = [
    {
      city: 'New York',
      address: '123 Broadway, Suite 456',
      address2: 'New York, NY 10001',
      phone: '+1 (555) 123-4567',
      hours: 'Mon-Fri: 9AM-6PM EST'
    },
    {
      city: 'Los Angeles',
      address: '456 Sunset Blvd, Floor 12',
      address2: 'Los Angeles, CA 90028',
      phone: '+1 (555) 987-6543',
      hours: 'Mon-Fri: 9AM-6PM PST'
    },
    {
      city: 'Chicago',
      address: '789 Michigan Ave, Suite 200',
      address2: 'Chicago, IL 60611',
      phone: '+1 (555) 456-7890',
      hours: 'Mon-Fri: 9AM-6PM CST'
    }
  ]

  const inquiryTypes = [
    { value: 'general', label: 'General Inquiry' },
    { value: 'support', label: 'Customer Support' },
    { value: 'business', label: 'Business Partnership' },
    { value: 'returns', label: 'Returns & Refunds' }
  ]

  return (
    <div className="flex flex-col min-h-screen">
      <Header currentPath="/contact" />

      {/* Breadcrumb */}
      <div className="border-b bg-muted/30 py-4">
        <div className="container">
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-foreground">Home</Link>
            <ArrowRight className="h-4 w-4" />
            <span className="text-foreground">Contact</span>
          </div>
        </div>
      </div>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="py-16 bg-white">
          <div className="container">
            <div className="text-center max-w-3xl mx-auto mb-16">
              <h1 className="text-4xl font-bold mb-4">
                Get in <span className="text-red-500">Touch</span>
              </h1>
              <p className="text-xl text-muted-foreground mb-8">
                We're here to help! Whether you have questions about our products, need support, 
                or want to explore business opportunities, our team is ready to assist.
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <Badge variant="secondary" className="text-sm">
                  <Clock className="w-4 h-4 mr-1" />
                  24/7 Support
                </Badge>
                <Badge variant="secondary" className="text-sm">
                  <Users className="w-4 h-4 mr-1" />
                  Expert Team
                </Badge>
                <Badge variant="secondary" className="text-sm">
                  <Star className="w-4 h-4 mr-1" />
                  5-Star Rated
                </Badge>
              </div>
            </div>

            {/* Contact Methods */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
              {contactMethods.map((method, index) => (
                <Card key={index} className="text-center hover:shadow-lg transition-all duration-300">
                  <CardContent className="pt-6">
                    <div className={`w-16 h-16 ${method.color} rounded-full flex items-center justify-center mx-auto mb-4`}>
                      <method.icon className="h-8 w-8" />
                    </div>
                    <h3 className="font-semibold mb-2">{method.title}</h3>
                    <p className="text-sm text-muted-foreground mb-3">{method.description}</p>
                    <p className="font-medium text-red-500 mb-2">{method.value}</p>
                    <p className="text-xs text-muted-foreground">{method.available}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        {/* Contact Form & Office Locations */}
        <section className="py-16 bg-gray-50">
          <div className="container">
            <div className="grid lg:grid-cols-2 gap-12">
              {/* Contact Form */}
              <div>
                <Card className="p-8">
                  <CardHeader className="px-0 pt-0">
                    <CardTitle className="text-2xl">Send us a Message</CardTitle>
                    <p className="text-muted-foreground">
                      Fill out the form below and we'll get back to you as soon as possible.
                    </p>
                  </CardHeader>
                  <CardContent className="px-0 pb-0">
                    {submitStatus === 'success' && (
                      <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                        <p className="text-green-800 font-medium">Message sent successfully!</p>
                        <p className="text-green-600 text-sm mt-1">We'll respond within 24 hours.</p>
                      </div>
                    )}
                    {submitStatus === 'error' && (
                      <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                        <p className="text-red-800 font-medium">Failed to send message</p>
                        <p className="text-red-600 text-sm mt-1">Please try again or contact us directly.</p>
                      </div>
                    )}
                    
                    <form onSubmit={handleSubmit} className="space-y-6">
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-medium mb-2 block">Name *</label>
                          <Input
                            type="text"
                            placeholder="Your full name"
                            value={formData.name}
                            onChange={(e) => setFormData({...formData, name: e.target.value})}
                            required
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium mb-2 block">Email *</label>
                          <Input
                            type="email"
                            placeholder="your.email@example.com"
                            value={formData.email}
                            onChange={(e) => setFormData({...formData, email: e.target.value})}
                            required
                          />
                        </div>
                      </div>
                      
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-medium mb-2 block">Phone</label>
                          <Input
                            type="tel"
                            placeholder="+1 (555) 123-4567"
                            value={formData.phone}
                            onChange={(e) => setFormData({...formData, phone: e.target.value})}
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium mb-2 block">Inquiry Type</label>
                          <select
                            className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-red-500 focus:border-red-500"
                            value={formData.inquiryType}
                            onChange={(e) => setFormData({...formData, inquiryType: e.target.value as ContactForm['inquiryType']})}
                          >
                            {inquiryTypes.map((type) => (
                              <option key={type.value} value={type.value}>
                                {type.label}
                              </option>
                            ))}
                          </select>
                        </div>
                      </div>

                      <div>
                        <label className="text-sm font-medium mb-2 block">Subject *</label>
                        <Input
                          type="text"
                          placeholder="Brief description of your inquiry"
                          value={formData.subject}
                          onChange={(e) => setFormData({...formData, subject: e.target.value})}
                          required
                        />
                      </div>

                      <div>
                        <label className="text-sm font-medium mb-2 block">Message *</label>
                        <textarea
                          className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-red-500 focus:border-red-500 min-h-[120px]"
                          placeholder="Please provide detailed information about your inquiry..."
                          value={formData.message}
                          onChange={(e) => setFormData({...formData, message: e.target.value})}
                          required
                        />
                      </div>

                      <Button 
                        type="submit" 
                        className="w-full bg-red-500 hover:bg-red-600 text-white"
                        disabled={isSubmitting}
                      >
                        {isSubmitting ? (
                          <>
                            <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                            Sending...
                          </>
                        ) : (
                          <>
                            <Send className="mr-2 h-4 w-4" />
                            Send Message
                          </>
                        )}
                      </Button>
                    </form>
                  </CardContent>
                </Card>
              </div>

              {/* Office Locations */}
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold mb-4">Our Locations</h2>
                  <p className="text-muted-foreground mb-6">
                    Visit us at any of our offices or reach out to your nearest location.
                  </p>
                </div>

                {officeLocations.map((office, index) => (
                  <Card key={index} className="p-6">
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 bg-red-50 rounded-lg flex items-center justify-center flex-shrink-0">
                        <MapPin className="h-6 w-6 text-red-500" />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-lg mb-2">{office.city} Office</h3>
                        <div className="space-y-2 text-sm text-muted-foreground">
                          <p className="flex items-center">
                            <MapPin className="h-4 w-4 mr-2 text-gray-400" />
                            {office.address}<br />
                            <span className="ml-6">{office.address2}</span>
                          </p>
                          <p className="flex items-center">
                            <Phone className="h-4 w-4 mr-2 text-gray-400" />
                            {office.phone}
                          </p>
                          <p className="flex items-center">
                            <Clock className="h-4 w-4 mr-2 text-gray-400" />
                            {office.hours}
                          </p>
                        </div>
                      </div>
                    </div>
                  </Card>
                ))}

                {/* FAQ Quick Links */}
                <Card className="p-6 bg-red-50">
                  <h3 className="font-semibold mb-4">Need Quick Answers?</h3>
                  <div className="space-y-3">
                    <Link href="/help/shipping" className="block text-sm text-red-600 hover:text-red-700">
                      → Shipping & Delivery Information
                    </Link>
                    <Link href="/help/returns" className="block text-sm text-red-600 hover:text-red-700">
                      → Returns & Exchanges Policy
                    </Link>
                    <Link href="/help/sizing" className="block text-sm text-red-600 hover:text-red-700">
                      → Size Guides & Product Info
                    </Link>
                    <Link href="/help/account" className="block text-sm text-red-600 hover:text-red-700">
                      → Account & Order Management
                    </Link>
                  </div>
                </Card>
              </div>
            </div>
          </div>
        </section>

        {/* Popular Categories CTA */}
        <section className="py-16 bg-white">
          <div className="container">
            <div className="text-center mb-12">
              <h2 className="text-2xl font-bold mb-4">
                Browse While You Wait
              </h2>
              <p className="text-muted-foreground">
                Explore our popular categories while we prepare your response
              </p>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { name: 'Electronics', slug: 'electronics', count: '1,250+ items' },
                { name: 'Fashion', slug: 'fashion', count: '890+ items' },
                { name: 'Home & Garden', slug: 'home-garden', count: '650+ items' },
                { name: 'Sports', slug: 'sports-outdoors', count: '420+ items' }
              ].map((category) => (
                <Link
                  key={category.slug}
                  href={`/products?category=${category.slug}`}
                  className="group text-center p-6 rounded-lg border hover:border-red-500 hover:shadow-md transition-all duration-300"
                >
                  <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-3 group-hover:bg-red-500 group-hover:text-white transition-colors">
                    <Package className="h-6 w-6" />
                  </div>
                  <h3 className="font-medium mb-1 group-hover:text-red-500 transition-colors">
                    {category.name}
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    {category.count}
                  </p>
                </Link>
              ))}
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  )
}