import { Metadata } from 'next'
import Link from 'next/link'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'

export default function PricingPage() {
  const plans = [
    {
      name: 'Starter',
      price: '$299',
      period: 'per month',
      description: 'Perfect for small businesses starting their marketing journey',
      features: [
        'SEO Optimization (Basic)',
        'Social Media Management (2 platforms)',
        'Content Creation (4 posts/month)',
        'Monthly Performance Report',
        'Email Support',
        '1 Campaign Setup'
      ],
      cta: 'Get Started',
      highlighted: false
    },
    {
      name: 'Professional',
      price: '$599',
      period: 'per month',
      description: 'Ideal for growing businesses ready to scale',
      features: [
        'Everything in Starter',
        'PPC Management ($1,000 ad spend)',
        'Content Creation (12 posts/month)',
        'Social Media (4 platforms)',
        'Email Marketing Automation',
        'Weekly Performance Reports',
        'Priority Support',
        '3 Campaign Setups',
        'A/B Testing',
        'Advanced Analytics'
      ],
      cta: 'Start Free Trial',
      highlighted: true
    },
    {
      name: 'Enterprise',
      price: '$1,499',
      period: 'per month',
      description: 'For established businesses demanding excellence',
      features: [
        'Everything in Professional',
        'PPC Management ($5,000+ ad spend)',
        'Content Creation (25+ posts/month)',
        'All Social Platforms',
        'Advanced Marketing Automation',
        'Daily Performance Reports',
        'Dedicated Account Manager',
        'Unlimited Campaign Setups',
        'Custom Integrations',
        'White-Label Reports',
        'Strategic Consulting',
        'Priority Development'
      ],
      cta: 'Contact Sales',
      highlighted: false
    }
  ]

  return (
    <>
      <Navigation />
      <main className="container py-20">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-5xl font-bold text-gray-900 mb-4">
              Simple, Transparent Pricing
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Choose the perfect plan for your business. All plans include our AI-powered automation platform.
            </p>
            <div className="mt-6 flex items-center justify-center gap-4">
              <span className="text-green-600 font-semibold">✓ 75% cost reduction vs agencies</span>
              <span className="text-green-600 font-semibold">✓ ROI in 7 days</span>
              <span className="text-green-600 font-semibold">✓ 15-minute setup</span>
            </div>
          </div>

          {/* Pricing Cards */}
          <div className="grid md:grid-cols-3 gap-8 mb-16">
            {plans.map((plan) => (
              <div
                key={plan.name}
                className={`relative rounded-2xl p-8 ${
                  plan.highlighted
                    ? 'bg-primary-600 text-white shadow-2xl scale-105 border-4 border-primary-700'
                    : 'bg-white border-2 border-gray-200'
                }`}
              >
                {plan.highlighted && (
                  <div className="absolute -top-5 left-1/2 transform -translate-x-1/2 bg-yellow-400 text-gray-900 px-4 py-1 rounded-full text-sm font-bold">
                    MOST POPULAR
                  </div>
                )}

                <div className="text-center mb-8">
                  <h3 className={`text-2xl font-bold mb-2 ${plan.highlighted ? 'text-white' : 'text-gray-900'}`}>
                    {plan.name}
                  </h3>
                  <div className="mb-2">
                    <span className={`text-5xl font-bold ${plan.highlighted ? 'text-white' : 'text-gray-900'}`}>
                      {plan.price}
                    </span>
                    <span className={`text-lg ${plan.highlighted ? 'text-gray-100' : 'text-gray-600'}`}>
                      /{plan.period}
                    </span>
                  </div>
                  <p className={`text-sm ${plan.highlighted ? 'text-gray-100' : 'text-gray-600'}`}>
                    {plan.description}
                  </p>
                </div>

                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-start">
                      <span className={`mr-2 ${plan.highlighted ? 'text-yellow-400' : 'text-green-600'}`}>✓</span>
                      <span className={`text-sm ${plan.highlighted ? 'text-gray-100' : 'text-gray-700'}`}>
                        {feature}
                      </span>
                    </li>
                  ))}
                </ul>

                <Link
                  href={plan.name === 'Enterprise' ? '/contact' : '/signup'}
                  className={`block w-full text-center py-3 px-6 rounded-lg font-semibold transition-colors ${
                    plan.highlighted
                      ? 'bg-white text-primary-600 hover:bg-gray-100'
                      : 'bg-primary-600 text-white hover:bg-primary-700'
                  }`}
                >
                  {plan.cta}
                </Link>
              </div>
            ))}
          </div>

          {/* FAQ Section */}
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-8">Frequently Asked Questions</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold mb-2">Can I change plans later?</h3>
                <p className="text-gray-600">
                  Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately, and we'll prorate the difference.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">What payment methods do you accept?</h3>
                <p className="text-gray-600">
                  We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and wire transfers for Enterprise plans.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">Is there a setup fee?</h3>
                <p className="text-gray-600">
                  No setup fees! Your first month includes full onboarding, campaign setup, and training at no additional cost.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">What's your refund policy?</h3>
                <p className="text-gray-600">
                  We offer a 30-day money-back guarantee. If you're not satisfied, we'll refund your first month in full, no questions asked.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">Do you offer annual plans?</h3>
                <p className="text-gray-600">
                  Yes! Annual plans save you 20% compared to monthly billing. Contact our sales team for annual pricing.
                </p>
              </div>
            </div>
          </div>

          {/* CTA Section */}
          <div className="mt-16 bg-primary-600 rounded-2xl p-12 text-center text-white">
            <h2 className="text-3xl font-bold mb-4">Still have questions?</h2>
            <p className="text-xl mb-8 text-gray-100">
              Our team is here to help you choose the perfect plan for your business.
            </p>
            <div className="flex gap-4 justify-center">
              <Link href="/contact" className="btn-secondary bg-white text-primary-600 hover:bg-gray-100">
                Contact Sales
              </Link>
              <Link href="/signup" className="btn-secondary border-2 border-white text-white hover:bg-white hover:text-primary-600">
                Start Free Trial
              </Link>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}

export const metadata: Metadata = {
  title: 'Pricing - Bizoholic AI Marketing',
  description: 'Simple, transparent pricing for AI-powered marketing automation. Plans starting at $299/month with 75% cost reduction.',
}
