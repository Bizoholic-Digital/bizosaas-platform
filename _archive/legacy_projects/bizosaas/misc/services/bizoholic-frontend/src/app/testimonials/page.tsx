import { Metadata } from 'next'
import Link from 'next/link'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'

export default function TestimonialsPage() {
  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'CEO',
      company: 'TechStart Solutions',
      image: '/avatars/sarah.jpg',
      rating: 5,
      quote: 'Bizoholic transformed our marketing completely. We went from spending $10,000/month with an agency to just $599 with better results. ROI came in 5 days!',
      results: '350% increase in leads, 75% cost reduction',
      industry: 'SaaS'
    },
    {
      name: 'Michael Chen',
      role: 'Marketing Director',
      company: 'GrowthCo',
      image: '/avatars/michael.jpg',
      rating: 5,
      quote: 'The AI automation is incredible. We\'re generating 3x more content, running campaigns across 6 platforms, and I have more time to focus on strategy.',
      results: '3x content output, 6 platform coverage',
      industry: 'E-commerce'
    },
    {
      name: 'Emma Rodriguez',
      role: 'Founder',
      company: 'LocalBiz Hub',
      image: '/avatars/emma.jpg',
      rating: 5,
      quote: 'As a small business, we couldn\'t afford a full marketing team. Bizoholic gave us enterprise-level marketing at a fraction of the cost.',
      results: '200% revenue growth in 3 months',
      industry: 'Local Services'
    },
    {
      name: 'David Park',
      role: 'CMO',
      company: 'FinTech Innovations',
      image: '/avatars/david.jpg',
      rating: 5,
      quote: 'The dashboard and analytics are game-changing. We can see exactly what\'s working in real-time and optimize on the fly. Our conversion rate doubled.',
      results: '100% increase in conversion rate',
      industry: 'FinTech'
    },
    {
      name: 'Jennifer Williams',
      role: 'Owner',
      company: 'Bella Beauty Salon',
      image: '/avatars/jennifer.jpg',
      rating: 5,
      quote: 'Setup took literally 12 minutes. Within a week, we had 50 new bookings. The social media automation alone saves me 10 hours a week.',
      results: '50 new customers in week 1',
      industry: 'Beauty & Wellness'
    },
    {
      name: 'Robert Martinez',
      role: 'VP of Growth',
      company: 'ScaleUp Inc',
      image: '/avatars/robert.jpg',
      rating: 5,
      quote: 'We tried 3 other marketing automation platforms. Bizoholic is the only one that actually delivered on its promises. Highly recommend.',
      results: '5x ROI, 40% time savings',
      industry: 'B2B SaaS'
    },
    {
      name: 'Lisa Thompson',
      role: 'Managing Partner',
      company: 'Legal Solutions Group',
      image: '/avatars/lisa.jpg',
      rating: 5,
      quote: 'The content quality is outstanding. The AI writes better than our previous copywriter, and we\'re publishing 4x more content.',
      results: '4x content volume, better quality',
      industry: 'Legal Services'
    },
    {
      name: 'James Anderson',
      role: 'Founder',
      company: 'FitLife Gym',
      image: '/avatars/james.jpg',
      rating: 5,
      quote: 'I was skeptical about AI marketing, but the results speak for themselves. 120 new memberships in 2 months. Best decision we made.',
      results: '120 new memberships in 60 days',
      industry: 'Fitness'
    },
    {
      name: 'Amanda Lee',
      role: 'Director of Marketing',
      company: 'EduTech Learning',
      image: '/avatars/amanda.jpg',
      rating: 5,
      quote: 'The email automation campaigns are brilliant. Open rates up 45%, click-through rates doubled. And it runs itself!',
      results: '45% open rate increase',
      industry: 'Education'
    }
  ]

  const stats = [
    { value: '500+', label: 'Happy Clients' },
    { value: '4.9/5', label: 'Average Rating' },
    { value: '98%', label: 'Client Retention' },
    { value: '7 Days', label: 'Average ROI Time' }
  ]

  return (
    <>
      <Navigation />
      <main className="container py-20">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Trusted by 500+ Growing Businesses
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Real stories from real businesses that transformed their marketing with Bizoholic
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16 max-w-4xl mx-auto">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-4xl font-bold text-primary-600 mb-2">{stat.value}</div>
              <div className="text-gray-600">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Testimonials Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-shadow">
              {/* Rating */}
              <div className="flex mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <span key={i} className="text-yellow-400 text-xl">★</span>
                ))}
              </div>

              {/* Quote */}
              <p className="text-gray-700 mb-4 italic">
                "{testimonial.quote}"
              </p>

              {/* Results */}
              <div className="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
                <div className="text-sm font-semibold text-green-800 mb-1">Results:</div>
                <div className="text-sm text-green-700">{testimonial.results}</div>
              </div>

              {/* Author */}
              <div className="flex items-center">
                <div className="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center mr-3">
                  <span className="text-primary-600 font-bold text-lg">
                    {testimonial.name.split(' ').map(n => n[0]).join('')}
                  </span>
                </div>
                <div>
                  <div className="font-semibold text-gray-900">{testimonial.name}</div>
                  <div className="text-sm text-gray-600">{testimonial.role}</div>
                  <div className="text-sm text-gray-500">{testimonial.company}</div>
                </div>
              </div>

              {/* Industry Tag */}
              <div className="mt-4">
                <span className="inline-block bg-gray-100 text-gray-600 text-xs px-3 py-1 rounded-full">
                  {testimonial.industry}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Video Testimonials Section */}
        <div className="bg-gray-50 rounded-2xl p-12 mb-16">
          <h2 className="text-3xl font-bold text-center mb-8">Video Testimonials</h2>
          <p className="text-center text-gray-600 mb-8">Coming soon: Watch our clients share their success stories</p>
          <div className="grid md:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-gray-200 rounded-lg aspect-video flex items-center justify-center">
                <span className="text-gray-400">Video {i}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Case Studies CTA */}
        <div className="bg-primary-600 rounded-2xl p-12 text-center text-white mb-16">
          <h2 className="text-3xl font-bold mb-4">Want to See Detailed Case Studies?</h2>
          <p className="text-xl mb-8 text-gray-100">
            Dive deep into how we helped businesses like yours achieve remarkable results
          </p>
          <Link href="/case-studies" className="btn-secondary bg-white text-primary-600 hover:bg-gray-100">
            View Case Studies
          </Link>
        </div>

        {/* Trust Signals */}
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-center mb-8">Why Businesses Choose Bizoholic</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-4xl mb-3">🚀</div>
              <h3 className="font-semibold mb-2">Fast Results</h3>
              <p className="text-gray-600 text-sm">Average ROI in just 7 days</p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-3">💰</div>
              <h3 className="font-semibold mb-2">Cost Effective</h3>
              <p className="text-gray-600 text-sm">75% cheaper than traditional agencies</p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-3">🤖</div>
              <h3 className="font-semibold mb-2">AI-Powered</h3>
              <p className="text-gray-600 text-sm">Latest technology, always improving</p>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center mt-16">
          <h2 className="text-3xl font-bold mb-4">Ready to Join Our Success Stories?</h2>
          <p className="text-xl text-gray-600 mb-8">
            Start your free trial today and see results in days, not months
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/signup" className="btn-primary">
              Start Free Trial
            </Link>
            <Link href="/pricing" className="btn-secondary">
              View Pricing
            </Link>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}

export const metadata: Metadata = {
  title: 'Testimonials - Bizoholic Success Stories',
  description: 'Read success stories from 500+ businesses that transformed their marketing with Bizoholic AI automation. Average ROI in 7 days.',
}
