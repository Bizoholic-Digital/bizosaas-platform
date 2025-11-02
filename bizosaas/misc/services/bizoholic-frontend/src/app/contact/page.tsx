'use client'

import { useState } from 'react'
import Link from 'next/link'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import {
  Mail,
  Phone,
  Clock,
  MessageCircle,
  MapPin,
  Send,
  CheckCircle2,
  ChevronDown,
  Star,
  ArrowRight,
  Linkedin,
  Twitter,
  Facebook,
  Instagram
} from 'lucide-react'

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    phone: '',
    service: '',
    message: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [openFaq, setOpenFaq] = useState<number | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        setSubmitStatus('success')
        setFormData({ name: '', email: '', company: '', phone: '', service: '', message: '' })
      } else {
        setSubmitStatus('error')
      }
    } catch (error) {
      setSubmitStatus('error')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const faqs = [
    {
      question: 'How quickly will I get a response?',
      answer: 'We aim to respond to all inquiries within 24 hours during business days. For urgent matters, please use our live chat feature for immediate assistance.'
    },
    {
      question: 'What services do you offer?',
      answer: 'We offer comprehensive AI-powered marketing services including SEO optimization, paid advertising, social media management, content marketing, email campaigns, and reputation management. All powered by our 93+ AI agents.'
    },
    {
      question: 'Do you offer free consultations?',
      answer: 'Yes! We offer a free 30-minute consultation to discuss your marketing needs and show you how our AI platform can help your business grow. Book a call using the link below.'
    },
    {
      question: "What's your pricing model?",
      answer: 'We offer flexible pricing plans starting at $299/month. Our platform typically delivers 75% cost savings compared to traditional agencies while providing better results. Contact us for a custom quote tailored to your needs.'
    },
    {
      question: 'Do you work with my industry?',
      answer: 'Our AI-powered platform works across all industries including retail, professional services, healthcare, real estate, hospitality, and more. Our 500+ clients span dozens of different sectors.'
    }
  ]

  return (
    <>
      <Navigation />
      <main className="pt-20">
        {/* Breadcrumb */}
        <div className="container py-8">
          <Breadcrumb items={[{ label: 'Contact Us' }]} />
        </div>

        {/* Hero Section */}
        <section className="py-16 md:py-24 bg-gray-50">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h1 className="heading-1 mb-6">Get in Touch</h1>
              <p className="text-xl text-gray-600">
                Ready to transform your marketing? We typically respond within 24 hours and offer
                free consultations to discuss your needs.
              </p>
            </div>
          </div>
        </section>

        {/* Main Content Grid */}
        <section className="py-16 md:py-24">
          <div className="container px-4">
            <div className="grid lg:grid-cols-3 gap-12">
              {/* Contact Form - Takes 2 columns */}
              <div className="lg:col-span-2">
                <div className="card-premium p-8">
                  <h2 className="heading-2 mb-6">Send Us a Message</h2>

                  {submitStatus === 'success' && (
                    <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-xl flex items-start gap-3">
                      <CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                      <div>
                        <h3 className="font-semibold text-green-900">Message sent successfully!</h3>
                        <p className="text-sm text-green-700 mt-1">
                          We'll get back to you within 24 hours.
                        </p>
                      </div>
                    </div>
                  )}

                  {submitStatus === 'error' && (
                    <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl">
                      <p className="text-sm text-red-700">
                        There was an error sending your message. Please try again or email us directly at hello@bizoholic.com
                      </p>
                    </div>
                  )}

                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                          Full Name *
                        </label>
                        <input
                          type="text"
                          id="name"
                          name="name"
                          value={formData.name}
                          onChange={handleChange}
                          required
                          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                          placeholder="John Smith"
                        />
                      </div>

                      <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                          Email Address *
                        </label>
                        <input
                          type="email"
                          id="email"
                          name="email"
                          value={formData.email}
                          onChange={handleChange}
                          required
                          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                          placeholder="john@company.com"
                        />
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-2">
                          Company Name
                        </label>
                        <input
                          type="text"
                          id="company"
                          name="company"
                          value={formData.company}
                          onChange={handleChange}
                          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                          placeholder="Your Company Inc."
                        />
                      </div>

                      <div>
                        <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
                          Phone Number
                        </label>
                        <input
                          type="tel"
                          id="phone"
                          name="phone"
                          value={formData.phone}
                          onChange={handleChange}
                          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                          placeholder="+1 (555) 123-4567"
                        />
                      </div>
                    </div>

                    <div>
                      <label htmlFor="service" className="block text-sm font-medium text-gray-700 mb-2">
                        Service Interest
                      </label>
                      <select
                        id="service"
                        name="service"
                        value={formData.service}
                        onChange={handleChange}
                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                      >
                        <option value="">Select a service...</option>
                        <option value="seo">SEO Optimization</option>
                        <option value="paid-ads">Paid Advertising</option>
                        <option value="social-media">Social Media Management</option>
                        <option value="content">Content Marketing</option>
                        <option value="email">Email Marketing</option>
                        <option value="reputation">Reputation Management</option>
                        <option value="analytics">Analytics & Reporting</option>
                        <option value="all">Complete Marketing Suite</option>
                      </select>
                    </div>

                    <div>
                      <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                        Message *
                      </label>
                      <textarea
                        id="message"
                        name="message"
                        value={formData.message}
                        onChange={handleChange}
                        required
                        rows={6}
                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                        placeholder="Tell us about your marketing goals and challenges..."
                      />
                    </div>

                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="btn-primary w-full py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isSubmitting ? (
                        'Sending...'
                      ) : (
                        <>
                          Send Message
                          <Send className="ml-2 h-5 w-5" />
                        </>
                      )}
                    </button>
                  </form>
                </div>
              </div>

              {/* Contact Info Sidebar */}
              <div className="space-y-6">
                {/* Contact Methods */}
                <div className="card-premium p-6">
                  <h3 className="font-semibold text-gray-900 mb-4">Contact Information</h3>
                  <div className="space-y-4">
                    <div className="flex items-start gap-3">
                      <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <Mail className="h-5 w-5 text-primary-600" />
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">Email</div>
                        <a href="mailto:hello@bizoholic.com" className="text-sm text-primary-600 hover:text-primary-700">
                          hello@bizoholic.com
                        </a>
                      </div>
                    </div>

                    <div className="flex items-start gap-3">
                      <div className="w-10 h-10 bg-secondary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <Phone className="h-5 w-5 text-secondary-600" />
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">Phone</div>
                        <a href="tel:+15551234567" className="text-sm text-secondary-600 hover:text-secondary-700">
                          +1 (555) 123-4567
                        </a>
                      </div>
                    </div>

                    <div className="flex items-start gap-3">
                      <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <MessageCircle className="h-5 w-5 text-blue-600" />
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">Live Chat</div>
                        <a href="http://localhost:3005" target="_blank" rel="noopener noreferrer" className="text-sm text-blue-600 hover:text-blue-700">
                          Open Client Portal
                        </a>
                      </div>
                    </div>

                    <div className="flex items-start gap-3">
                      <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <MapPin className="h-5 w-5 text-purple-600" />
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">Location</div>
                        <p className="text-sm text-gray-600">
                          Remote-First Company<br />
                          Serving Businesses Worldwide
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Business Hours */}
                <div className="card-premium p-6">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                      <Clock className="h-5 w-5 text-green-600" />
                    </div>
                    <h3 className="font-semibold text-gray-900">Business Hours</h3>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Monday - Friday</span>
                      <span className="font-medium text-gray-900">9AM - 6PM EST</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Saturday - Sunday</span>
                      <span className="font-medium text-gray-900">Closed</span>
                    </div>
                    <div className="pt-3 mt-3 border-t border-gray-200">
                      <p className="text-xs text-gray-600">
                        Response time: Within 24 hours
                      </p>
                    </div>
                  </div>
                </div>

                {/* Social Media */}
                <div className="card-premium p-6">
                  <h3 className="font-semibold text-gray-900 mb-4">Follow Us</h3>
                  <div className="flex gap-3">
                    <a href="#" className="w-10 h-10 bg-blue-100 hover:bg-blue-200 rounded-lg flex items-center justify-center transition-colors">
                      <Linkedin className="h-5 w-5 text-blue-600" />
                    </a>
                    <a href="#" className="w-10 h-10 bg-sky-100 hover:bg-sky-200 rounded-lg flex items-center justify-center transition-colors">
                      <Twitter className="h-5 w-5 text-sky-600" />
                    </a>
                    <a href="#" className="w-10 h-10 bg-blue-100 hover:bg-blue-200 rounded-lg flex items-center justify-center transition-colors">
                      <Facebook className="h-5 w-5 text-blue-700" />
                    </a>
                    <a href="#" className="w-10 h-10 bg-pink-100 hover:bg-pink-200 rounded-lg flex items-center justify-center transition-colors">
                      <Instagram className="h-5 w-5 text-pink-600" />
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="py-16 md:py-24 bg-gray-50">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto">
              <div className="text-center mb-12">
                <h2 className="heading-2 mb-4">Frequently Asked Questions</h2>
                <p className="text-gray-600">Quick answers to common questions</p>
              </div>

              <div className="space-y-4">
                {faqs.map((faq, index) => (
                  <div key={index} className="card-premium overflow-hidden">
                    <button
                      onClick={() => setOpenFaq(openFaq === index ? null : index)}
                      className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-gray-50 transition-colors"
                    >
                      <span className="font-semibold text-gray-900">{faq.question}</span>
                      <ChevronDown
                        className={`h-5 w-5 text-gray-600 transition-transform ${
                          openFaq === index ? 'transform rotate-180' : ''
                        }`}
                      />
                    </button>
                    {openFaq === index && (
                      <div className="px-6 pb-4 text-gray-600">
                        {faq.answer}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Social Proof */}
        <section className="py-16 md:py-24">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto text-center">
              <div className="flex items-center justify-center gap-2 mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-6 w-6 fill-yellow-400 text-yellow-400" />
                ))}
              </div>
              <h2 className="heading-2 mb-4">Join 500+ Satisfied Clients</h2>
              <p className="text-xl text-gray-600 mb-6">
                "Bizoholic transformed our marketing in just 30 days. We saw a 4.8x ROI and cut our
                marketing costs by 75%. The AI automation is incredible!"
              </p>
              <p className="text-sm text-gray-600">
                — Sarah Johnson, Founder of TechStart Inc.
              </p>
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="py-20 md:py-28 bg-primary-600 text-white">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-4xl font-bold mb-6">
                Prefer to Talk? Book a Demo Call
              </h2>
              <p className="text-xl text-primary-100 mb-8">
                Schedule a free 30-minute consultation to see our AI platform in action
                and discuss your marketing goals.
              </p>
              <div className="flex flex-wrap gap-4 justify-center">
                <Link href="/services" className="btn-white">
                  Book Free Demo
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
                <Link href="/about" className="btn-white-outline">
                  Learn More About Us
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
