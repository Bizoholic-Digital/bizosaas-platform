'use client'

import { motion } from 'framer-motion'

export default function SocialProof() {
  const stats = [
    { value: '500+', label: 'Businesses Served' },
    { value: '75%', label: 'Average Cost Savings' },
    { value: '7 Days', label: 'Average ROI Timeline' },
    { value: '4.9/5', label: 'Customer Rating' },
  ]

  return (
    <section className="section bg-primary-600">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="heading-lg text-white mb-4">
            Trusted by Growing Businesses Worldwide
          </h2>
          <p className="text-large text-blue-100 max-w-3xl mx-auto">
            Join hundreds of businesses that have transformed their marketing with AI
          </p>
        </motion.div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="text-4xl lg:text-5xl font-bold text-white mb-2">
                {stat.value}
              </div>
              <div className="text-blue-100 font-medium">{stat.label}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}