/**
 * CorelDove About Page - Company Information & Values
 * SEO-optimized about page with company story, team, and values
 */

'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'
import { Badge } from '../../components/ui/badge'
import Header from '../../components/navigation/header'
import { useTenantTheme } from '../../hooks/useTenantTheme'
import { 
  ArrowRight, 
  Users,
  Target,
  Heart,
  Award,
  Globe,
  ShieldCheck,
  Truck,
  Headphones,
  Mail,
  Phone,
  MapPin,
  Star,
  ShoppingCart,
  Send
} from 'lucide-react'

interface TeamMember {
  id: string
  name: string
  role: string
  bio: string
  image?: string
  social?: {
    linkedin?: string
    twitter?: string
  }
}

interface Stat {
  label: string
  value: string
  icon: React.ReactNode
}

export default function AboutPage() {
  const { config } = useTenantTheme()
  const [activeSection, setActiveSection] = useState('story')
  const [formData, setFormData] = useState({ name: '', email: '', message: '' })

  const stats: Stat[] = [
    {
      label: 'Happy Customers',
      value: '50K+',
      icon: <Users className="h-6 w-6" />
    },
    {
      label: 'Products Available',
      value: '10K+',
      icon: <Target className="h-6 w-6" />
    },
    {
      label: 'Years of Excellence',
      value: '8+',
      icon: <Award className="h-6 w-6" />
    },
    {
      label: 'Countries Served',
      value: '25+',
      icon: <Globe className="h-6 w-6" />
    }
  ]

  const values = [
    {
      title: 'Quality First',
      description: 'Every product is carefully curated and tested to meet our high standards.',
      icon: <ShieldCheck className="h-8 w-8 text-red-500" />
    },
    {
      title: 'Customer-Centric',
      description: 'Your satisfaction is our priority. We listen, adapt, and deliver excellence.',
      icon: <Heart className="h-8 w-8 text-red-500" />
    },
    {
      title: 'Fast & Reliable',
      description: 'Quick delivery and dependable service you can count on, every time.',
      icon: <Truck className="h-8 w-8 text-red-500" />
    },
    {
      title: '24/7 Support',
      description: 'Our dedicated team is here to help you whenever you need assistance.',
      icon: <Headphones className="h-8 w-8 text-red-500" />
    }
  ]

  const teamMembers: TeamMember[] = [
    {
      id: '1',
      name: 'Sarah Johnson',
      role: 'CEO & Founder',
      bio: 'With over 15 years in e-commerce, Sarah founded CorelDove to revolutionize online shopping.',
      image: '/placeholder-team-sarah.jpg'
    },
    {
      id: '2',
      name: 'Michael Chen',
      role: 'CTO',
      bio: 'Michael leads our technology vision, ensuring cutting-edge solutions for our customers.',
      image: '/placeholder-team-michael.jpg'
    },
    {
      id: '3',
      name: 'Emily Rodriguez',
      role: 'Head of Operations',
      bio: 'Emily oversees our global operations, ensuring smooth delivery worldwide.',
      image: '/placeholder-team-emily.jpg'
    },
    {
      id: '4',
      name: 'David Park',
      role: 'Chief Marketing Officer',
      bio: 'David crafts our brand story and connects us with customers around the world.',
      image: '/placeholder-team-david.jpg'
    }
  ]

  return (
    <div className="flex flex-col min-h-screen">
      <Header currentPath="/about" />

      {/* Breadcrumb */}
      <div className="border-b bg-muted/30 py-4">
        <div className="container">
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-foreground">Home</Link>
            <ArrowRight className="h-4 w-4" />
            <span className="text-foreground">About</span>
          </div>
        </div>
      </div>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="py-16 bg-red-50">
          <div className="container text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              About <span className="text-red-500">CorelDove</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-8">
              We're passionate about bringing you the best products from around the world, 
              with exceptional service and unbeatable value.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-red-500 hover:bg-red-600">
                Shop Now
              </Button>
              <Button size="lg" variant="outline">
                <Mail className="mr-2 h-4 w-4" />
                Contact Us
              </Button>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-16">
          <div className="container">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="flex justify-center mb-4 text-red-500">
                    {stat.icon}
                  </div>
                  <div className="text-3xl font-bold text-red-500 mb-2">{stat.value}</div>
                  <div className="text-muted-foreground">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Navigation Tabs */}
        <section className="py-8 border-b">
          <div className="container">
            <div className="flex flex-wrap justify-center gap-4">
              {[
                { id: 'story', label: 'Our Story' },
                { id: 'values', label: 'Our Values' },
                { id: 'team', label: 'Our Team' },
                { id: 'contact', label: 'Contact Info' }
              ].map((section) => (
                <Button
                  key={section.id}
                  variant={activeSection === section.id ? 'default' : 'outline'}
                  onClick={() => setActiveSection(section.id)}
                  className={activeSection === section.id ? 'bg-red-500 hover:bg-red-600' : ''}
                >
                  {section.label}
                </Button>
              ))}
            </div>
          </div>
        </section>

        {/* Content Sections */}
        <section className="py-16">
          <div className="container">
            {/* Our Story */}
            {activeSection === 'story' && (
              <div className="max-w-4xl mx-auto">
                <h2 className="text-3xl font-bold mb-8 text-center">Our Story</h2>
                <div className="grid md:grid-cols-2 gap-12 items-center">
                  <div>
                    <div className="aspect-video relative rounded-lg overflow-hidden bg-muted">
                      <div className="w-full h-full bg-red-100 flex items-center justify-center">
                        <div className="text-center">
                          <Target className="h-16 w-16 text-red-500 mx-auto mb-4" />
                          <p className="text-muted-foreground">Company Story Image</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-6">
                    <p className="text-lg text-muted-foreground">
                      Founded in 2016, CorelDove began as a simple idea: to make high-quality products 
                      accessible to everyone, everywhere. What started as a small online marketplace has 
                      grown into a trusted global platform.
                    </p>
                    <p className="text-lg text-muted-foreground">
                      Our journey has been driven by one core belief - that exceptional products and 
                      outstanding customer service should go hand in hand. Today, we serve millions 
                      of customers worldwide, but our commitment remains unchanged.
                    </p>
                    <p className="text-lg text-muted-foreground">
                      Every product on CorelDove is carefully selected by our team of experts who 
                      understand quality, value, and what our customers truly want.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Our Values */}
            {activeSection === 'values' && (
              <div className="max-w-6xl mx-auto">
                <h2 className="text-3xl font-bold mb-8 text-center">Our Values</h2>
                <p className="text-lg text-muted-foreground text-center mb-12 max-w-3xl mx-auto">
                  These core values guide everything we do and shape how we serve our customers every day.
                </p>
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                  {values.map((value, index) => (
                    <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                      <CardHeader>
                        <div className="flex justify-center mb-4">
                          {value.icon}
                        </div>
                        <CardTitle className="text-xl">{value.title}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <p className="text-muted-foreground">{value.description}</p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {/* Our Team */}
            {activeSection === 'team' && (
              <div className="max-w-6xl mx-auto">
                <h2 className="text-3xl font-bold mb-8 text-center">Meet Our Team</h2>
                <p className="text-lg text-muted-foreground text-center mb-12 max-w-3xl mx-auto">
                  The passionate people behind CorelDove who work tirelessly to bring you the best shopping experience.
                </p>
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                  {teamMembers.map((member) => (
                    <Card key={member.id} className="text-center hover:shadow-lg transition-shadow">
                      <CardHeader>
                        <div className="aspect-square relative rounded-full overflow-hidden mx-auto mb-4 w-24 h-24 bg-muted">
                          <div className="w-full h-full bg-red-100 flex items-center justify-center">
                            <Users className="h-10 w-10 text-red-500" />
                          </div>
                        </div>
                        <CardTitle className="text-xl">{member.name}</CardTitle>
                        <Badge variant="outline" className="mx-auto">{member.role}</Badge>
                      </CardHeader>
                      <CardContent>
                        <p className="text-sm text-muted-foreground">{member.bio}</p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {/* Contact Info */}
            {activeSection === 'contact' && (
              <div className="max-w-4xl mx-auto">
                <h2 className="text-3xl font-bold mb-8 text-center">Get In Touch</h2>
                <p className="text-lg text-muted-foreground text-center mb-12">
                  We'd love to hear from you. Choose the best way to reach out to us.
                </p>
                <div className="grid md:grid-cols-3 gap-8">
                  <Card className="text-center hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex justify-center mb-4">
                        <Mail className="h-8 w-8 text-red-500" />
                      </div>
                      <CardTitle>Email Us</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-muted-foreground mb-4">
                        Send us an email and we'll respond within 24 hours.
                      </p>
                      <Button variant="outline" className="w-full">
                        support@coreldove.com
                      </Button>
                    </CardContent>
                  </Card>

                  <Card className="text-center hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex justify-center mb-4">
                        <Phone className="h-8 w-8 text-red-500" />
                      </div>
                      <CardTitle>Call Us</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-muted-foreground mb-4">
                        Speak directly with our support team.
                      </p>
                      <Button variant="outline" className="w-full">
                        1-800-COREL-DOVE
                      </Button>
                    </CardContent>
                  </Card>

                  <Card className="text-center hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex justify-center mb-4">
                        <MapPin className="h-8 w-8 text-red-500" />
                      </div>
                      <CardTitle>Visit Us</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-muted-foreground mb-4">
                        Come visit our headquarters.
                      </p>
                      <Button variant="outline" className="w-full">
                        View Address
                      </Button>
                    </CardContent>
                  </Card>
                </div>
              </div>
            )}
          </div>
        </section>

        {/* Contact Form Section */}
        <section className="py-16 bg-red-50">
          <div className="container">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-3xl font-bold mb-8 text-center">Send Us a Message</h2>
              <p className="text-lg text-muted-foreground text-center mb-12">
                Have a question or feedback? We'd love to hear from you.
              </p>
              <div className="grid lg:grid-cols-2 gap-12">
                <Card className="p-6">
                  <CardHeader>
                    <CardTitle>Contact Form</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <label className="text-sm font-medium mb-2 block">Name</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-red-500 focus:border-red-500"
                        placeholder="Your full name"
                        value={formData.name}
                        onChange={(e) => setFormData({...formData, name: e.target.value})}
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium mb-2 block">Email</label>
                      <input
                        type="email"
                        className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-red-500 focus:border-red-500"
                        placeholder="your.email@example.com"
                        value={formData.email}
                        onChange={(e) => setFormData({...formData, email: e.target.value})}
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium mb-2 block">Message</label>
                      <textarea
                        rows={4}
                        className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-red-500 focus:border-red-500"
                        placeholder="Tell us how we can help you..."
                        value={formData.message}
                        onChange={(e) => setFormData({...formData, message: e.target.value})}
                      />
                    </div>
                    <Button className="w-full bg-red-500 hover:bg-red-600">
                      <Send className="mr-2 h-4 w-4" />
                      Send Message
                    </Button>
                  </CardContent>
                </Card>

                <div className="space-y-6">
                  <Card className="p-6">
                    <h3 className="font-semibold mb-4 flex items-center">
                      <ShoppingCart className="mr-2 h-5 w-5 text-red-500" />
                      Shop Popular Categories
                    </h3>
                    <div className="grid grid-cols-2 gap-3">
                      {[
                        { name: 'Electronics', href: '/products?category=electronics' },
                        { name: 'Fashion', href: '/products?category=fashion' },
                        { name: 'Home & Garden', href: '/products?category=home-garden' },
                        { name: 'Sports & Outdoors', href: '/products?category=sports-outdoors' }
                      ].map((category) => (
                        <Button key={category.name} variant="outline" size="sm" asChild className="h-auto py-3">
                          <Link href={category.href} className="text-center">
                            {category.name}
                          </Link>
                        </Button>
                      ))}
                    </div>
                  </Card>

                  <Card className="p-6">
                    <h3 className="font-semibold mb-4 flex items-center">
                      <Star className="mr-2 h-5 w-5 text-red-500" />
                      Trending Products
                    </h3>
                    <div className="space-y-3">
                      {[
                        { name: 'Wireless Headphones Pro', price: '$199', rating: 4.8 },
                        { name: 'Smart Fitness Watch', price: '$299', rating: 4.9 },
                        { name: 'Portable Bluetooth Speaker', price: '$89', rating: 4.7 }
                      ].map((product, index) => (
                        <div key={index} className="flex justify-between items-center py-2 border-b last:border-b-0">
                          <div>
                            <p className="font-medium text-sm">{product.name}</p>
                            <div className="flex items-center gap-1">
                              <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                              <span className="text-xs text-muted-foreground">{product.rating}</span>
                            </div>
                          </div>
                          <span className="font-semibold text-red-500">{product.price}</span>
                        </div>
                      ))}
                    </div>
                    <Button variant="outline" className="w-full mt-4" asChild>
                      <Link href="/products">View All Products</Link>
                    </Button>
                  </Card>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16">
          <div className="container text-center">
            <h2 className="text-3xl font-bold mb-4">Ready to Start Shopping?</h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
              Join millions of satisfied customers who trust CorelDove for their shopping needs.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild className="bg-red-500 hover:bg-red-600">
                <Link href="/products">Browse Products</Link>
              </Button>
              <Button size="lg" variant="outline" asChild>
                <Link href="/categories">Shop Categories</Link>
              </Button>
            </div>
          </div>
        </section>
      </main>

      {/* Footer - CorelDove branded with improved spacing */}
      <footer className="border-t border-gray-800 bg-gray-900">
        <div className="container py-16">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 pt-8">
            <div>
              <h3 className="font-semibold mb-6 text-white">Shop</h3>
              <ul className="space-y-3 text-sm text-gray-400">
                <li><Link href="/products" className="hover:text-white transition-colors">All Products</Link></li>
                <li><Link href="/categories" className="hover:text-white transition-colors">Categories</Link></li>
                <li><Link href="/deals" className="hover:text-white transition-colors">Special Deals</Link></li>
                <li><Link href="/new-arrivals" className="hover:text-white transition-colors">New Arrivals</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-6 text-white">Company</h3>
              <ul className="space-y-3 text-sm text-gray-400">
                <li><Link href="/about" className="hover:text-white transition-colors">About Us</Link></li>
                <li><Link href="/careers" className="hover:text-white transition-colors">Careers</Link></li>
                <li><Link href="/press" className="hover:text-white transition-colors">Press</Link></li>
                <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-6 text-white">Support</h3>
              <ul className="space-y-3 text-sm text-gray-400">
                <li><Link href="/help" className="hover:text-white transition-colors">Help Center</Link></li>
                <li><Link href="/returns" className="hover:text-white transition-colors">Returns</Link></li>
                <li><Link href="/shipping" className="hover:text-white transition-colors">Shipping Info</Link></li>
                <li><Link href="/track" className="hover:text-white transition-colors">Track Order</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-6 text-white">Legal</h3>
              <ul className="space-y-3 text-sm text-gray-400">
                <li><Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                <li><Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
                <li><Link href="/refund" className="hover:text-white transition-colors">Refund Policy</Link></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 pt-12 mt-12 pb-8 text-center text-sm text-gray-400">
            <p>&copy; 2024 {config.branding.companyName}. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}