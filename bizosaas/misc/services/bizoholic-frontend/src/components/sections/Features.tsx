'use client'

import { motion } from 'framer-motion'
import { CheckCircle, Zap, Target, Rocket } from 'lucide-react'

interface FeaturesProps {
  data?: {
    title: string
    items: Array<{
      icon: string
      title: string
      description: string
    }>
  }
}

export default function Features({ data }: FeaturesProps) {
  const features = data?.items || [
    {
      icon: '🚀',
      title: '75% Cost Reduction',
      description: 'Our AI agents replace expensive marketing teams while delivering better results'
    },
    {
      icon: '⚡',
      title: '7-Day ROI',
      description: 'See measurable returns within the first week of implementation'
    },
    {
      icon: '🎯',
      title: '15-Min Setup',
      description: 'Get up and running in minutes, not months'
    }
  ]

  return (
    <section className="section bg-white">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="heading-lg text-gray-900 mb-4">
            {data?.title || 'Why Choose Bizoholic AI?'}
          </h2>
          <p className="text-large text-gray-600 max-w-3xl mx-auto">
            Our AI-powered platform delivers results that traditional marketing can't match
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="text-center group"
            >
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-primary-500 to-blue-600 rounded-2xl mb-6 group-hover:scale-110 transition-transform duration-300">
                <span className="text-2xl">{feature.icon}</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">{feature.title}</h3>
              <p className="text-gray-600 leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        {/* Additional benefits */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="mt-16 bg-gradient-to-r from-primary-50 to-blue-50 rounded-2xl p-8"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="flex items-center">
              <CheckCircle className="h-6 w-6 text-green-500 mr-3 flex-shrink-0" />
              <span className="text-gray-700 font-medium">24/7 AI Monitoring</span>
            </div>
            <div className="flex items-center">
              <CheckCircle className="h-6 w-6 text-green-500 mr-3 flex-shrink-0" />
              <span className="text-gray-700 font-medium">Real-time Analytics</span>
            </div>
            <div className="flex items-center">
              <CheckCircle className="h-6 w-6 text-green-500 mr-3 flex-shrink-0" />
              <span className="text-gray-700 font-medium">Automated Optimization</span>
            </div>
            <div className="flex items-center">
              <CheckCircle className="h-6 w-6 text-green-500 mr-3 flex-shrink-0" />
              <span className="text-gray-700 font-medium">Multi-platform Integration</span>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}