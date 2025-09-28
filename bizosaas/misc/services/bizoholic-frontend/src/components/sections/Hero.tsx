'use client'

import Link from 'next/link'
import { ArrowRight, Play } from 'lucide-react'
import { motion } from 'framer-motion'

interface HeroProps {
  data?: {
    title: string
    subtitle: string
    cta_primary: string
    cta_secondary: string
  }
}

export default function Hero({ data }: HeroProps) {
  const heroData = data || {
    title: "Transform Your Marketing with AI Automation",
    subtitle: "Get 75% cost savings, ROI within 7 days, and setup in 15 minutes. The smartest marketing platform for small businesses.",
    cta_primary: "Get Started Free",
    cta_secondary: "View Demo"
  }

  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-blue-50 via-white to-indigo-50 pt-20 pb-16 lg:pt-24 lg:pb-20">
      {/* Background decorations */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
        <div className="absolute top-1/3 right-1/4 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-300"></div>
      </div>

      <div className="relative container">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Content */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center lg:text-left"
          >
            {/* Badge */}
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.4, delay: 0.2 }}
              className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-primary-100 text-primary-800 mb-6"
            >
              🚀 AI Marketing Revolution
            </motion.div>

            {/* Main headline */}
            <motion.h1 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="heading-xl text-gray-900 mb-6"
            >
              {heroData.title}
            </motion.h1>

            {/* Subtitle */}
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="text-large text-gray-600 mb-8 max-w-2xl lg:max-w-none"
            >
              {heroData.subtitle}
            </motion.p>

            {/* CTAs */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start"
            >
              <Link href="/contact" className="btn-primary group">
                {heroData.cta_primary}
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Link>
              <button className="btn-secondary group">
                <Play className="mr-2 h-4 w-4" />
                {heroData.cta_secondary}
              </button>
            </motion.div>

            {/* Trust indicators */}
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.6 }}
              className="mt-8 pt-8 border-t border-gray-200"
            >
              <p className="text-sm text-gray-500 mb-4">Trusted by 500+ businesses worldwide</p>
              <div className="flex items-center justify-center lg:justify-start space-x-6 opacity-60">
                <div className="text-sm font-medium">★★★★★ 4.9/5</div>
                <div className="text-sm">500+ Reviews</div>
                <div className="text-sm">24/7 Support</div>
              </div>
            </motion.div>
          </motion.div>

          {/* Visual/Demo */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative"
          >
            <div className="relative bg-white rounded-2xl shadow-2xl p-8 backdrop-blur-sm border border-gray-100">
              {/* Mock dashboard preview */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="h-3 bg-gray-200 rounded w-1/3"></div>
                  <div className="flex space-x-1">
                    <div className="w-3 h-3 bg-red-400 rounded-full"></div>
                    <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
                    <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="h-4 bg-blue-200 rounded w-3/4"></div>
                  <div className="h-4 bg-green-200 rounded w-1/2"></div>
                  <div className="h-4 bg-purple-200 rounded w-2/3"></div>
                </div>
                <div className="grid grid-cols-2 gap-4 mt-6">
                  <div className="bg-gradient-to-r from-blue-100 to-blue-200 p-4 rounded-lg">
                    <div className="text-2xl font-bold text-blue-800">75%</div>
                    <div className="text-sm text-blue-600">Cost Savings</div>
                  </div>
                  <div className="bg-gradient-to-r from-green-100 to-green-200 p-4 rounded-lg">
                    <div className="text-2xl font-bold text-green-800">7 Days</div>
                    <div className="text-sm text-green-600">ROI Timeline</div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Floating elements */}
            <div className="absolute -top-4 -right-4 w-20 h-20 bg-yellow-400 rounded-full opacity-20 animate-bounce delay-1000"></div>
            <div className="absolute -bottom-4 -left-4 w-16 h-16 bg-pink-400 rounded-full opacity-20 animate-bounce delay-500"></div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}