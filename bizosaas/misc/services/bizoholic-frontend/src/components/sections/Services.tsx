'use client'

import { motion } from 'framer-motion'
import { ArrowRight, Star } from 'lucide-react'
import Link from 'next/link'

interface ServicesProps {
  data?: {
    title: string
    items: Array<{
      title: string
      description: string
      price: string
      badge?: string
    }>
  }
}

export default function Services({ data }: ServicesProps) {
  const services = data?.items || [
    {
      title: 'SEO Optimization & Local SEO',
      description: 'Boost your search rankings with AI-powered SEO optimization. Our advanced algorithms analyze your website, competitors, and search trends to deliver 200% better organic traffic within 90 days.',
      price: '$299/month',
      badge: 'Most Popular'
    },
    {
      title: 'Paid Advertising (PPC) Management',
      description: 'Maximize your ad spend with AI-driven PPC campaigns. Our intelligent bidding algorithms reduce cost-per-click by 45% while increasing conversions by 180%.',
      price: '$599/month',
      badge: 'High ROI'
    }
  ]

  return (
    <section className="section bg-gray-50">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="heading-lg text-gray-900 mb-4">
            {data?.title || 'Complete Marketing Automation Suite'}
          </h2>
          <p className="text-large text-gray-600 max-w-3xl mx-auto">
            Everything you need to dominate your market with AI-powered marketing
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {services.map((service, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.2 }}
              viewport={{ once: true }}
              className="relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 group"
            >
              {/* Badge */}
              {service.badge && (
                <div className="absolute -top-4 left-6">
                  <div className="bg-gradient-to-r from-yellow-400 to-orange-400 text-white px-4 py-2 rounded-full text-sm font-bold shadow-lg">
                    {service.badge}
                  </div>
                </div>
              )}

              {/* Content */}
              <div className="pt-4">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-gray-900 group-hover:text-primary-600 transition-colors">
                    {service.title}
                  </h3>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-primary-600">{service.price}</div>
                  </div>
                </div>

                <p className="text-gray-600 mb-6 leading-relaxed">
                  {service.description}
                </p>

                {/* Features list */}
                <div className="space-y-3 mb-6">
                  <div className="flex items-center">
                    <Star className="h-5 w-5 text-yellow-400 mr-2" />
                    <span className="text-sm text-gray-600">AI-powered optimization</span>
                  </div>
                  <div className="flex items-center">
                    <Star className="h-5 w-5 text-yellow-400 mr-2" />
                    <span className="text-sm text-gray-600">24/7 monitoring & reporting</span>
                  </div>
                  <div className="flex items-center">
                    <Star className="h-5 w-5 text-yellow-400 mr-2" />
                    <span className="text-sm text-gray-600">Dedicated account manager</span>
                  </div>
                </div>

                {/* CTA */}
                <Link 
                  href={`/services/${service.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`}
                  className="inline-flex items-center text-primary-600 font-medium hover:text-primary-700 transition-colors group/link"
                >
                  Learn more
                  <ArrowRight className="ml-2 h-4 w-4 group-hover/link:translate-x-1 transition-transform" />
                </Link>
              </div>
            </motion.div>
          ))}
        </div>

        {/* All services CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="text-center mt-12"
        >
          <Link href="/services" className="btn-primary">
            View All Services
            <ArrowRight className="ml-2 h-4 w-4" />
          </Link>
        </motion.div>
      </div>
    </section>
  )
}