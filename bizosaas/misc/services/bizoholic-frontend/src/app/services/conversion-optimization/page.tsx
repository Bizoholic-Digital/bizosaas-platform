import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import Link from 'next/link'
import { Target, TrendingUp, MousePointer, BarChart3, CheckCircle, ArrowRight, Award, Quote } from 'lucide-react'

export const metadata: Metadata = {
  title: 'Conversion Rate Optimization (CRO) Services | Bizoholic',
  description: 'Maximize revenue from existing traffic with data-driven conversion optimization. A/B testing, heatmaps, and user journey analysis.',
}

export default function ConversionOptimizationPage() {
  const features = [
    {
      icon: <Target className="w-6 h-6" />,
      title: 'Heatmap & Session Recording',
      description: 'Understand exactly how visitors interact with your website through visual data'
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: 'A/B & Multivariate Testing',
      description: 'Test multiple variations to find what drives the highest conversions'
    },
    {
      icon: <MousePointer className="w-6 h-6" />,
      title: 'User Journey Optimization',
      description: 'Optimize every step of the customer journey from landing to conversion'
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: 'Conversion Funnel Analysis',
      description: 'Identify and fix bottlenecks in your conversion funnel with data-driven insights'
    }
  ]

  const benefits = [
    'Increase conversion rates by 50-200%',
    'Maximize ROI on existing traffic and ad spend',
    'Reduce bounce rates and cart abandonment',
    'Improve user experience and satisfaction',
    'Data-driven decision making, not guesswork',
    'Continuous testing and optimization'
  ]

  const process = [
    {
      step: 1,
      title: 'Audit & Analysis',
      description: 'Deep dive into analytics, heatmaps, and user behavior to identify opportunities'
    },
    {
      step: 2,
      title: 'Hypothesis Development',
      description: 'Create data-backed hypotheses for tests based on research and best practices'
    },
    {
      step: 3,
      title: 'Test & Measure',
      description: 'Run controlled A/B tests and multivariate experiments to validate hypotheses'
    },
    {
      step: 4,
      title: 'Implement & Scale',
      description: 'Roll out winning variations and continue iterative testing for ongoing improvement'
    }
  ]

  const pricing = [
    {
      name: 'Starter CRO',
      price: '$599',
      period: '/month',
      description: 'Perfect for landing pages',
      features: [
        'Landing page optimization',
        'Heatmap and scroll map analysis',
        'Basic A/B testing (2 tests/month)',
        'Conversion funnel analysis',
        'Monthly optimization report',
        'Recommendations for improvement'
      ],
      popular: false
    },
    {
      name: 'Growth CRO',
      price: '$1,299',
      period: '/month',
      description: 'For full-funnel optimization',
      features: [
        'Everything in Starter CRO',
        'Full website optimization',
        'Advanced A/B & multivariate testing (6 tests/month)',
        'Session recording analysis',
        'Form optimization',
        'Mobile optimization',
        'Bi-weekly strategy calls',
        'Priority support'
      ],
      popular: true
    },
    {
      name: 'Enterprise CRO',
      price: '$2,499',
      period: '/month',
      description: 'For advanced optimization',
      features: [
        'Everything in Growth CRO',
        'Unlimited testing',
        'Personalization and dynamic content',
        'Advanced user segmentation',
        'Multi-page funnel optimization',
        'Checkout flow optimization',
        'Dedicated CRO specialist',
        'Custom analytics dashboard',
        'Weekly optimization sprints'
      ],
      popular: false
    }
  ]

  const caseStudies = [
    {
      industry: 'SaaS Signup Flow',
      challenge: 'Low trial signup conversion rate at 2.1%, high form abandonment',
      solution: 'Multi-step form optimization, trust signals, social proof, and progressive disclosure testing',
      results: [
        'Conversion rate increased from 2.1% to 5.8% (176% lift)',
        'Form abandonment reduced by 62%',
        '$450,000 additional annual recurring revenue',
        'Payback period of 3 weeks on optimization investment'
      ]
    },
    {
      industry: 'E-commerce Checkout',
      challenge: 'High cart abandonment rate of 78%, complex checkout process',
      solution: 'Streamlined checkout, guest checkout option, trust badges, and progress indicators',
      results: [
        'Cart abandonment reduced by 45% (from 78% to 43%)',
        'Average order value increased 18%',
        'Checkout completion time reduced by 35%',
        '$280,000 in recovered revenue in first 6 months'
      ]
    }
  ]

  const testimonials = [
    {
      name: 'Chris Anderson',
      company: 'FlowMetrics SaaS',
      role: 'VP of Growth',
      quote: 'We were stuck at a 2% conversion rate for months. Bizoholic systematic testing approach nearly tripled our signups in 4 months. Every test is backed by data and the results speak for themselves. This is now our highest ROI marketing activity.',
      rating: 5
    },
    {
      name: 'Lisa Park',
      company: 'Urban Marketplace',
      role: 'Head of E-commerce',
      quote: 'Our cart abandonment was killing us. The checkout optimization they did recovered hundreds of thousands in lost revenue. The heatmaps showed us exactly where people were dropping off. Worth every penny and then some.',
      rating: 5
    }
  ]

  const faqs = [
    {
      question: 'How long does it take to see results?',
      answer: 'Initial insights and quick wins can appear within 2-4 weeks. Statistically significant A/B test results typically take 4-8 weeks depending on your traffic volume. CRO is an ongoing process - the best results come from continuous testing over 6-12 months.'
    },
    {
      question: 'How much traffic do I need for CRO?',
      answer: 'Ideally, at least 1,000 monthly conversions (or 10,000+ visitors) for reliable A/B testing. However, we can work with lower traffic sites using qualitative research methods like heatmaps, session recordings, and user testing to identify optimization opportunities.'
    },
    {
      question: 'What is the difference between A/B testing and multivariate testing?',
      answer: 'A/B testing compares two versions of a page (version A vs B). Multivariate testing tests multiple elements simultaneously to find the best combination. We start with A/B tests for major changes, then use multivariate testing for fine-tuning multiple elements.'
    },
    {
      question: 'Will CRO affect our SEO?',
      answer: 'Done correctly, CRO improves SEO by reducing bounce rates and increasing engagement - signals Google loves. We follow SEO best practices and always test changes to ensure they do not negatively impact rankings. In fact, improved user experience often leads to better SEO.'
    },
    {
      question: 'What tools do you use for CRO?',
      answer: 'We use industry-leading tools including Google Analytics, Hotjar (heatmaps), Optimizely or VWO (A/B testing), Microsoft Clarity, UserTesting, and custom analytics. All tools are included in our service - you do not need to purchase them separately.'
    },
    {
      question: 'Can you guarantee a specific conversion rate increase?',
      answer: 'No ethical CRO agency can guarantee specific numbers as results depend on many factors including traffic quality, industry, and current optimization level. However, our average client sees 30-100% conversion rate improvements within 6 months. We focus on continuous improvement, not one-time fixes.'
    },
    {
      question: 'What if tests do not show improvement?',
      answer: 'Not every test wins - that is the nature of experimentation. Failed tests are valuable learning opportunities. We analyze why tests did not work, develop new hypotheses, and continue testing. Our iterative approach ensures consistent improvement over time, even when individual tests fail.'
    }
  ]

  return (
    <>
      <Navigation />
      <main className="min-h-screen bg-white">
        {/* Breadcrumb */}
        <section className="pt-8">
          <div className="container">
            <Breadcrumb items={[
              { label: 'Home', href: '/' },
              { label: 'Services', href: '/services' },
              { label: 'Conversion Optimization' }
            ]} />
          </div>
        </section>

        {/* Hero Section */}
        <section className="bg-gray-50 py-20">
          <div className="container">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl font-bold text-gray-900 mb-6">
                Conversion Rate Optimization (CRO)
              </h1>
              <p className="text-xl text-gray-700 mb-8">
                Turn more visitors into customers with data-driven conversion optimization that maximizes revenue from your existing traffic
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/contact" className="btn-primary px-8 py-4 text-lg">
                  Get Free CRO Audit
                </Link>
                <Link href="/pricing" className="btn-secondary px-8 py-4 text-lg">
                  View Pricing
                </Link>
              </div>
              <p className="text-sm text-gray-600 mt-6">
                No credit card required • Free conversion analysis • See results in 30 days
              </p>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Complete CRO Solutions
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Everything you need to optimize conversions and maximize revenue
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <div key={index} className="bg-white p-6 rounded-xl border border-gray-200 hover:border-primary-500 hover:shadow-lg transition-all">
                  <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center text-primary-600 mb-4">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="py-20 bg-gray-50">
          <div className="container">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-4xl font-bold text-gray-900 mb-12 text-center">
                What You&apos;ll Achieve
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0 mt-1" />
                    <span className="text-lg text-gray-700">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Process Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Our CRO Process
              </h2>
              <p className="text-xl text-gray-600">
                A proven 4-step approach to conversion optimization
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {process.map((item, index) => (
                <div key={index} className="relative">
                  <div className="bg-white p-6 rounded-xl border-2 border-primary-200 hover:border-primary-500 transition-all">
                    <div className="w-12 h-12 bg-primary-600 rounded-full flex items-center justify-center text-white text-xl font-bold mb-4">
                      {item.step}
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {item.title}
                    </h3>
                    <p className="text-gray-600">
                      {item.description}
                    </p>
                  </div>
                  {index < process.length - 1 && (
                    <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                      <ArrowRight className="w-8 h-8 text-primary-300" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Pricing Section */}
        <section className="py-20 bg-gray-50">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                CRO Pricing Plans
              </h2>
              <p className="text-xl text-gray-600">
                Choose the plan that fits your optimization needs
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {pricing.map((plan, index) => (
                <div key={index} className={`bg-white rounded-2xl shadow-lg p-8 relative ${plan.popular ? 'border-2 border-primary-500 transform scale-105' : 'border border-gray-200'}`}>
                  {plan.popular && (
                    <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                      <span className="bg-primary-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                        Most Popular
                      </span>
                    </div>
                  )}
                  <div className="text-center mb-6">
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">
                      {plan.name}
                    </h3>
                    <p className="text-gray-600 mb-4">{plan.description}</p>
                    <div className="flex items-baseline justify-center">
                      <span className="text-5xl font-bold text-gray-900">{plan.price}</span>
                      <span className="text-gray-600 ml-2">{plan.period}</span>
                    </div>
                  </div>
                  <ul className="space-y-3 mb-8">
                    {plan.features.map((feature, idx) => (
                      <li key={idx} className="flex items-start space-x-3">
                        <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                        <span className="text-gray-700">{feature}</span>
                      </li>
                    ))}
                  </ul>
                  <Link
                    href="/contact"
                    className={`block w-full text-center py-3 px-6 rounded-lg font-semibold transition-colors ${plan.popular ? 'bg-primary-600 hover:bg-primary-700 text-white' : 'bg-gray-100 hover:bg-gray-200 text-gray-900'}`}
                  >
                    Get Started
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Case Studies Section */}
        <section className="py-20 bg-white">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Real Results from Real Clients
              </h2>
              <p className="text-xl text-gray-600">
                See how we have helped businesses multiply their conversions
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
              {caseStudies.map((study, index) => (
                <div key={index} className="card">
                  <div className="flex items-center mb-4">
                    <Award className="w-8 h-8 text-primary-600 mr-3" />
                    <h3 className="text-2xl font-bold text-gray-900">{study.industry}</h3>
                  </div>

                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-900 mb-2">The Challenge:</h4>
                    <p className="text-gray-600">{study.challenge}</p>
                  </div>

                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-900 mb-2">Our Solution:</h4>
                    <p className="text-gray-600">{study.solution}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">The Results:</h4>
                    <ul className="space-y-2">
                      {study.results.map((result, idx) => (
                        <li key={idx} className="flex items-start">
                          <CheckCircle className="w-5 h-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-700">{result}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Testimonials Section */}
        <section className="py-20 bg-gray-50">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                What Our Clients Say
              </h2>
              <p className="text-xl text-gray-600">
                Do not just take our word for it
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
              {testimonials.map((testimonial, index) => (
                <div key={index} className="bg-white rounded-2xl p-8 shadow-lg relative">
                  <Quote className="w-12 h-12 text-primary-200 absolute top-6 right-6" />
                  <div className="flex mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <svg key={i} className="w-5 h-5 text-yellow-400 fill-current" viewBox="0 0 20 20">
                        <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                      </svg>
                    ))}
                  </div>
                  <p className="text-gray-700 text-lg mb-6 italic">&quot;{testimonial.quote}&quot;</p>
                  <div>
                    <p className="font-semibold text-gray-900">{testimonial.name}</p>
                    <p className="text-gray-600">{testimonial.role}, {testimonial.company}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Frequently Asked Questions
              </h2>
              <p className="text-xl text-gray-600">
                Everything you need to know about conversion optimization
              </p>
            </div>

            <div className="max-w-4xl mx-auto space-y-6">
              {faqs.map((faq, index) => (
                <div key={index} className="bg-white rounded-xl p-6 shadow-md border border-gray-200">
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">
                    {faq.question}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {faq.answer}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-gray-50">
          <div className="container">
            <div className="cta-section">
              <h2 className="text-4xl font-bold mb-4">
                Ready to Multiply Your Conversions?
              </h2>
              <p className="text-xl mb-8 text-white/90">
                Get a free CRO audit and discover how to maximize your revenue
              </p>
              <Link
                href="/contact"
                className="inline-block bg-white text-primary-600 font-semibold px-8 py-4 rounded-lg hover:bg-gray-100 transition-colors"
              >
                Get Free CRO Audit
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
