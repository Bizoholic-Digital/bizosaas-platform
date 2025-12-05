"use client"

import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Star, Quote } from 'lucide-react'
import Image from 'next/image'

interface Testimonial {
  id: string
  name: string
  role: string
  company: string
  content: string
  avatar?: string
  rating: number
  results?: string
}

const testimonials: Testimonial[] = [
  {
    id: '1',
    name: 'Sarah Johnson',
    role: 'Marketing Director',
    company: 'TechCorp Inc.',
    content: 'BizOSaaS transformed our marketing efficiency by 300%. The AI insights are absolutely game-changing for our campaigns.',
    avatar: '/avatars/sarah.jpg',
    rating: 5,
    results: '300% efficiency increase'
  },
  {
    id: '2',
    name: 'Mike Chen',
    role: 'CEO',
    company: 'StartupXYZ',
    content: 'The automated campaigns saved us 20 hours per week. Our ROI increased by 150% in just 3 months.',
    avatar: '/avatars/mike.jpg',
    rating: 5,
    results: '150% ROI increase'
  },
  {
    id: '3',
    name: 'Elena Rodriguez',
    role: 'Growth Manager',
    company: 'E-commerce Plus',
    content: 'Finally found a platform that actually understands our business. The AI agents work 24/7 and never miss an opportunity.',
    avatar: '/avatars/elena.jpg',
    rating: 5,
    results: '24/7 automation'
  },
  {
    id: '4',
    name: 'David Kim',
    role: 'Founder',
    company: 'DigitalFlow',
    content: 'Best investment we made this year. The platform pays for itself within the first month through optimized ad spend.',
    avatar: '/avatars/david.jpg',
    rating: 5,
    results: 'ROI in 30 days'
  }
]

const companyLogos = [
  { name: 'TechCorp', logo: '/logos/techcorp.svg' },
  { name: 'StartupXYZ', logo: '/logos/startupxyz.svg' },
  { name: 'E-commerce Plus', logo: '/logos/ecommerce-plus.svg' },
  { name: 'DigitalFlow', logo: '/logos/digitalflow.svg' },
  { name: 'GrowthLab', logo: '/logos/growthlab.svg' },
  { name: 'MarketPro', logo: '/logos/marketpro.svg' }
]

function TestimonialCard({ testimonial }: { testimonial: Testimonial }) {
  return (
    <Card className="h-full">
      <CardContent className="p-6">
        <div className="flex items-start space-x-4">
          <Quote className="h-8 w-8 text-primary flex-shrink-0 mt-1" />
          <div className="flex-1">
            <p className="text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">
              "{testimonial.content}"
            </p>
            
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary to-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                {testimonial.name.split(' ').map(n => n[0]).join('')}
              </div>
              <div>
                <div className="font-semibold text-gray-900 dark:text-gray-100">
                  {testimonial.name}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  {testimonial.role} at {testimonial.company}
                </div>
              </div>
            </div>
            
            <div className="flex items-center justify-between mt-4">
              <div className="flex items-center space-x-1">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                ))}
              </div>
              {testimonial.results && (
                <Badge variant="outline" className="text-xs">
                  {testimonial.results}
                </Badge>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export function SocialProofSection() {
  return (
    <section className="py-16 bg-gray-50 dark:bg-gray-900">
      <div className="container mx-auto px-4">
        {/* Company Logos */}
        <div className="text-center mb-16">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-8">
            Trusted by innovative companies worldwide
          </p>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8 items-center opacity-60">
            {companyLogos.map((company) => (
              <div key={company.name} className="flex items-center justify-center">
                <div className="w-24 h-12 bg-gray-200 dark:bg-gray-700 rounded flex items-center justify-center text-xs font-medium">
                  {company.name}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Testimonials Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center space-x-2 mb-4">
            <div className="flex text-yellow-400">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="h-6 w-6 fill-current" />
              ))}
            </div>
            <span className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              4.9/5
            </span>
            <span className="text-gray-600 dark:text-gray-400">
              from 200+ reviews
            </span>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">
            What Our Clients Say
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Join thousands of businesses that have transformed their marketing with our AI-powered platform
          </p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {testimonials.map((testimonial) => (
            <TestimonialCard key={testimonial.id} testimonial={testimonial} />
          ))}
        </div>

        {/* Stats Section */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-primary mb-2">200+</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Happy Clients</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary mb-2">$50M+</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Ad Spend Managed</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary mb-2">300%</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Avg. ROI Increase</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary mb-2">24/7</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">AI Monitoring</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}