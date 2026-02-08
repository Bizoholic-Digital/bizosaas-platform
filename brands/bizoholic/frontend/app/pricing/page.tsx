/**
 * Bizoholic Pricing Page
 * Marketing service packages and pricing tiers with FastAPI Brain Gateway integration
 */

'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'

export default function PricingPage() {
  const [billingPeriod, setBillingPeriod] = useState<'monthly' | 'annually'>('monthly')
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null)

  const pricingPlans = [
    {
      id: 'starter',
      name: 'Starter Growth',
      description: 'Perfect for small businesses ready to scale their marketing',
      monthlyPrice: 2999,
      annualPrice: 29999,
      features: [
        'Social Media Management (3 platforms)',
        'Basic SEO Optimization',
        'Monthly Content Calendar',
        'Email Marketing Setup',
        'Performance Analytics Dashboard',
        'Monthly Strategy Call',
        'Basic Lead Generation',
        '5 Blog Posts/Month'
      ],
      popular: false,
      cta: 'Start Growing',
      color: 'gray'
    },
    {
      id: 'professional',
      name: 'Professional Scale',
      description: 'For growing businesses serious about marketing dominance',
      monthlyPrice: 5999,
      annualPrice: 59999,
      features: [
        'Social Media Management (5 platforms)',
        'Advanced SEO + Local SEO',
        'Bi-weekly Content Calendar',
        'Email Marketing Automation',
        'Advanced Analytics + Reporting',
        'Bi-weekly Strategy Calls',
        'Lead Generation + Nurturing',
        '10 Blog Posts/Month',
        'Paid Advertising Management',
        'Conversion Rate Optimization',
        'Competitor Analysis',
        'A/B Testing'
      ],
      popular: true,
      cta: 'Get Professional',
      color: 'indigo'
    },
    {
      id: 'enterprise',
      name: 'Enterprise Domination',
      description: 'For companies ready to dominate their market completely',
      monthlyPrice: 12999,
      annualPrice: 129999,
      features: [
        'Unlimited Social Media Management',
        'Enterprise SEO + Technical SEO',
        'Daily Content Creation',
        'Advanced Marketing Automation',
        'Custom Analytics Dashboard',
        'Weekly Strategy Sessions',
        'Full-Funnel Lead Generation',
        '20+ Blog Posts/Month',
        'Multi-Channel Paid Campaigns',
        'Advanced CRO + Landing Pages',
        'Market Research + Insights',
        'Custom Integration Development',
        'Dedicated Account Manager',
        'Priority Support',
        'Custom Reporting'
      ],
      popular: false,
      cta: 'Dominate Market',
      color: 'purple'
    }
  ]

  const addOns = [
    {
      name: 'Video Content Creation',
      monthlyPrice: 1999,
      description: '4 professional videos per month for social media and ads'
    },
    {
      name: 'Influencer Partnership Management',
      monthlyPrice: 2499,
      description: 'Find, negotiate, and manage influencer partnerships'
    },
    {
      name: 'Advanced Analytics & BI',
      monthlyPrice: 999,
      description: 'Custom dashboards with predictive analytics and insights'
    },
    {
      name: 'Reputation Management',
      monthlyPrice: 1499,
      description: 'Monitor and manage online reviews and brand reputation'
    }
  ]

  const handlePlanSelection = async (planId: string) => {
    setSelectedPlan(planId)

    // Track interest
    try {
      await fetch('/api/brain/wagtail/pricing-interest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan_id: planId, billing_period: billingPeriod })
      })
    } catch (e) { }

    // Redirect to Client Portal with plan selection
    window.location.href = `https://app.bizoholic.net/signup?plan=${planId}&billing=${billingPeriod}`
  }

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
    }).format(price / 100)
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Image
                src="/images/Bizoholic_Digital_-_Color-transparent.png"
                alt="Bizoholic Digital"
                width={150}
                height={60}
                priority
              />
            </div>
            <nav className="hidden md:flex space-x-8">
              <Link href="/" className="text-gray-600 hover:text-indigo-600 transition-colors">Home</Link>
              <Link href="/about" className="text-gray-600 hover:text-indigo-600 transition-colors">About</Link>
              <Link href="/portfolio" className="text-gray-600 hover:text-indigo-600 transition-colors">Portfolio</Link>
              <Link href="/pricing" className="text-indigo-600 font-medium">Pricing</Link>
              <Link href="/blog" className="text-gray-600 hover:text-indigo-600 transition-colors">Blog</Link>
              <Link href="/contact" className="text-gray-600 hover:text-indigo-600 transition-colors">Contact</Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-indigo-50 to-cyan-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              Get Addicted to <span className="text-indigo-600">Growth</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
              Choose the perfect marketing package to transform your business into a growth machine.
              Every plan is designed to deliver measurable results and sustainable success.
            </p>

            {/* Billing Toggle */}
            <div className="flex items-center justify-center mb-12">
              <span className="text-gray-600 mr-3">Monthly</span>
              <button
                onClick={() => setBillingPeriod(billingPeriod === 'monthly' ? 'annually' : 'monthly')}
                className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 ${billingPeriod === 'annually' ? 'bg-indigo-600' : 'bg-gray-200'
                  }`}
              >
                <span
                  className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${billingPeriod === 'annually' ? 'translate-x-5' : 'translate-x-0'
                    }`}
                />
              </button>
              <span className="text-gray-600 ml-3">
                Annually
                <span className="text-indigo-600 font-medium ml-1">(Save 17%)</span>
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-3 gap-8">
            {pricingPlans.map((plan) => {
              const price = billingPeriod === 'monthly' ? plan.monthlyPrice : plan.annualPrice
              const isPopular = plan.popular

              return (
                <div
                  key={plan.id}
                  className={`relative rounded-2xl shadow-lg overflow-hidden ${isPopular
                      ? 'ring-2 ring-indigo-600 scale-105'
                      : 'border border-gray-200 hover:shadow-xl transition-shadow'
                    }`}
                >
                  {isPopular && (
                    <div className="absolute top-0 left-0 right-0 bg-indigo-600 text-white text-center py-2 text-sm font-medium">
                      Most Popular
                    </div>
                  )}

                  <div className="bg-white p-8">
                    <div className={`${isPopular ? 'pt-6' : ''}`}>
                      <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                      <p className="text-gray-600 mb-6">{plan.description}</p>

                      <div className="flex items-baseline mb-6">
                        <span className="text-4xl font-bold text-gray-900">
                          {formatPrice(price)}
                        </span>
                        <span className="text-gray-600 ml-2">
                          /{billingPeriod === 'monthly' ? 'month' : 'year'}
                        </span>
                      </div>

                      <button
                        onClick={() => handlePlanSelection(plan.id)}
                        className={`w-full py-4 px-6 rounded-lg font-medium transition-all duration-200 mb-8 ${isPopular
                            ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                            : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                          } ${selectedPlan === plan.id ? 'ring-2 ring-indigo-500' : ''}`}
                      >
                        {plan.cta}
                      </button>

                      <div className="space-y-4">
                        <h4 className="font-semibold text-gray-900 mb-3">What's included:</h4>
                        {plan.features.map((feature, index) => (
                          <div key={index} className="flex items-start">
                            <svg className="w-5 h-5 text-indigo-600 mr-3 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                            <span className="text-gray-700">{feature}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Add-ons Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Boost Your Results
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Supercharge any plan with our premium add-ons for even better results
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {addOns.map((addon, index) => (
              <div key={index} className="bg-white rounded-lg p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-semibold text-gray-900">{addon.name}</h3>
                  <span className="text-2xl font-bold text-indigo-600">
                    {formatPrice(addon.monthlyPrice)}/mo
                  </span>
                </div>
                <p className="text-gray-600">{addon.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Frequently Asked Questions
            </h2>
          </div>

          <div className="space-y-8">
            {[
              {
                question: "What's included in the setup process?",
                answer: "Every plan includes a comprehensive onboarding process with strategy development, account setup, initial content creation, and team training. We'll have you up and running within 2 weeks."
              },
              {
                question: "Can I change plans anytime?",
                answer: "Absolutely! You can upgrade or downgrade your plan at any time. Changes take effect at your next billing cycle, and we'll help transition any ongoing campaigns."
              },
              {
                question: "Do you offer month-to-month contracts?",
                answer: "Yes, all our plans are available month-to-month with no long-term commitment required. However, annual plans offer significant savings and better results with consistent strategy execution."
              },
              {
                question: "What happens if I'm not satisfied?",
                answer: "We offer a 30-day satisfaction guarantee. If you're not completely satisfied with our service in the first month, we'll refund your investment and help you transition smoothly."
              },
              {
                question: "Do you work with businesses in my industry?",
                answer: "We work with businesses across all industries including B2B, B2C, e-commerce, healthcare, finance, real estate, and more. Our strategies are customized for your specific market and audience."
              }
            ].map((faq, index) => (
              <div key={index} className="border-b border-gray-200 pb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">{faq.question}</h3>
                <p className="text-gray-600">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-indigo-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Transform Your Marketing?
          </h2>
          <p className="text-xl text-indigo-100 mb-8 max-w-2xl mx-auto">
            Join hundreds of businesses that have become addicted to growth with Bizoholic.
            Start your success story today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/contact">
              <button className="bg-white text-indigo-600 px-8 py-4 rounded-lg font-medium hover:bg-gray-50 transition-colors">
                Get Started Now
              </button>
            </Link>
            <Link href="/portfolio">
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-medium hover:bg-white hover:text-indigo-600 transition-colors">
                See Our Results
              </button>
            </Link>
          </div>
          <p className="text-indigo-200 text-sm mt-6">
            No setup fees • 30-day guarantee • Cancel anytime
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <Image
                src="/images/Bizoholic_Digital_-_Color-transparent.png"
                alt="Bizoholic Digital"
                width={150}
                height={60}
                className="mb-4"
              />
              <p className="text-gray-400">
                Making businesses addicted to success through innovative marketing strategies.
              </p>
            </div>
            <div>
              <h4 className="font-bold mb-4">Services</h4>
              <ul className="space-y-2 text-gray-400">
                <li>Digital Strategy</li>
                <li>Social Media Marketing</li>
                <li>SEO & Content</li>
                <li>Paid Advertising</li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/about" className="hover:text-white">About</Link></li>
                <li><Link href="/portfolio" className="hover:text-white">Portfolio</Link></li>
                <li><Link href="/pricing" className="hover:text-white">Pricing</Link></li>
                <li><Link href="/blog" className="hover:text-white">Blog</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Contact</h4>
              <ul className="space-y-2 text-gray-400">
                <li>hello@bizoholic.com</li>
                <li>+1 (555) 123-4567</li>
                <li>San Francisco, CA</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Bizoholic Digital. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}