import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import Link from 'next/link'
import { BarChart3, PieChart, TrendingUp, Eye, CheckCircle, ArrowRight, Award, Quote } from 'lucide-react'

export const metadata: Metadata = {
  title: 'Marketing Analytics & Reporting Services | Bizoholic',
  description: 'Make data-driven decisions with AI-powered analytics and automated reporting. Track performance, measure ROI, and gain actionable insights.',
}

export default function AnalyticsPage() {
  const features = [
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: 'Cross-Channel Analytics Integration',
      description: 'Consolidate data from all marketing channels into unified dashboards and reports'
    },
    {
      icon: <PieChart className="w-6 h-6" />,
      title: 'Custom Dashboard Creation',
      description: 'Build personalized dashboards that display the metrics that matter most to your business'
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: 'Automated Reporting',
      description: 'Receive scheduled reports automatically with insights and recommendations'
    },
    {
      icon: <Eye className="w-6 h-6" />,
      title: 'Predictive Analytics',
      description: 'Forecast future performance and identify trends before they happen with AI-powered predictions'
    }
  ]

  const benefits = [
    'Make data-driven decisions with confidence',
    'Track ROI across all marketing channels',
    'Identify top-performing campaigns and optimize spend',
    'Discover hidden opportunities in your data',
    'Save 10+ hours per week on manual reporting',
    'Get actionable insights, not just numbers'
  ]

  const process = [
    {
      step: 1,
      title: 'Data Audit & Integration',
      description: 'Connect all data sources and audit tracking for accuracy and completeness'
    },
    {
      step: 2,
      title: 'Dashboard Design',
      description: 'Create custom dashboards aligned with your KPIs and business objectives'
    },
    {
      step: 3,
      title: 'Automation Setup',
      description: 'Configure automated reports, alerts, and scheduled data refreshes'
    },
    {
      step: 4,
      title: 'Insights & Optimization',
      description: 'Ongoing analysis, insights delivery, and recommendations for improvement'
    }
  ]

  const pricing = [
    {
      name: 'Starter Analytics',
      price: '$299',
      period: '/month',
      description: 'Perfect for small businesses',
      features: [
        'Google Analytics 4 setup and configuration',
        '1 custom dashboard (5-10 metrics)',
        'Monthly performance reports',
        'Basic cross-channel tracking',
        'Email report delivery',
        'Up to 3 data sources'
      ],
      popular: false
    },
    {
      name: 'Growth Analytics',
      price: '$599',
      period: '/month',
      description: 'For growing businesses',
      features: [
        'Everything in Starter Analytics',
        '3 custom dashboards (unlimited metrics)',
        'Weekly automated reports',
        'Advanced multi-channel attribution',
        'Real-time alerts and notifications',
        'Up to 10 data sources',
        'Conversion tracking optimization',
        'Bi-weekly strategy calls'
      ],
      popular: true
    },
    {
      name: 'Enterprise Analytics',
      price: '$1,299',
      period: '/month',
      description: 'For data-driven organizations',
      features: [
        'Everything in Growth Analytics',
        'Unlimited custom dashboards',
        'Daily reports with AI insights',
        'Predictive analytics and forecasting',
        'Custom data integrations and API access',
        'Unlimited data sources',
        'Dedicated analytics specialist',
        'Executive reporting and presentations',
        'Custom modeling and analysis'
      ],
      popular: false
    }
  ]

  const caseStudies = [
    {
      industry: 'Multi-Channel Retailer',
      challenge: 'Unable to track ROI across 8 marketing channels, conflicting data, no attribution model',
      solution: 'Unified analytics platform with custom attribution modeling and automated cross-channel reporting',
      results: [
        'Identified $120,000/month revenue opportunity from underutilized channels',
        'Reduced marketing waste by 28% through better attribution',
        '85% reduction in time spent on manual reporting',
        'Improved decision-making speed from weeks to hours'
      ]
    },
    {
      industry: 'B2B Service Business',
      challenge: 'No visibility into marketing ROI, wasting budget on underperforming campaigns',
      solution: 'Custom analytics dashboard with lead source tracking and revenue attribution',
      results: [
        'Saved $35,000/year by cutting non-performing campaigns',
        'Increased marketing ROI from 1.8x to 4.2x',
        'Discovered that 60% of revenue came from 20% of lead sources',
        'Optimized spend allocation for 3x better efficiency'
      ]
    }
  ]

  const testimonials = [
    {
      name: 'Marcus Johnson',
      company: 'TechFlow Solutions',
      role: 'CMO',
      quote: 'Before Bizoholic, we were flying blind. Now we have real-time visibility into every marketing dollar spent and can make decisions based on data, not gut feel. The custom dashboards saved our team 15+ hours per week on reporting.',
      rating: 5
    },
    {
      name: 'Sophie Chen',
      company: 'GreenLeaf Retail',
      role: 'Director of Marketing',
      quote: 'The multi-channel attribution model they built completely changed how we allocate our budget. We discovered channels we thought were underperforming were actually our best converters. ROI improved by 200% in 6 months.',
      rating: 5
    }
  ]

  const faqs = [
    {
      question: 'What data sources can you integrate?',
      answer: 'We integrate with virtually any data source including Google Analytics, Google Ads, Facebook Ads, LinkedIn Ads, Shopify, WooCommerce, Salesforce, HubSpot, Mailchimp, and 100+ other platforms. We can also work with custom APIs and databases.'
    },
    {
      question: 'Will I still have access to my analytics tools?',
      answer: 'Absolutely! We do not lock you into proprietary platforms. We build on top of industry-standard tools (Google Analytics, Looker Studio, etc.) and you maintain full access. We simply configure, optimize, and create custom views for your specific needs.'
    },
    {
      question: 'How long does implementation take?',
      answer: 'Basic setup (Starter package) takes 1-2 weeks. Comprehensive implementations (Growth and Enterprise) typically take 3-4 weeks depending on the number of data sources and complexity of requirements. You will start seeing value immediately once dashboards are live.'
    },
    {
      question: 'Do I need technical knowledge to use the dashboards?',
      answer: 'No! We design dashboards to be intuitive and user-friendly. We provide training and documentation so anyone on your team can access insights without technical expertise. Our goal is to make data accessible to everyone, not just data analysts.'
    },
    {
      question: 'What is the difference between this and Google Analytics?',
      answer: 'Google Analytics is a powerful tool, but it only tracks website data. We integrate data from ALL your marketing channels (ads, social, email, CRM, etc.) into unified dashboards. Plus, we configure everything correctly, create custom views, and provide ongoing insights and recommendations - not just raw data.'
    },
    {
      question: 'Can you track offline conversions and phone calls?',
      answer: 'Yes! We integrate call tracking systems, offline conversion imports, and CRM data to provide a complete view of your marketing performance. This is especially valuable for businesses with phone sales or in-person conversions.'
    },
    {
      question: 'What if our data is inaccurate or incomplete?',
      answer: 'That is common! Part of our process is a comprehensive data audit where we identify and fix tracking issues. We clean up historical data where possible and implement proper tracking going forward. Most clients discover their data was 20-40% inaccurate before working with us.'
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
              { label: 'Analytics & Reporting' }
            ]} />
          </div>
        </section>

        {/* Hero Section */}
        <section className="bg-gray-50 py-20">
          <div className="container">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl font-bold text-gray-900 mb-6">
                Marketing Analytics & Reporting
              </h1>
              <p className="text-xl text-gray-700 mb-8">
                Transform data into decisions with AI-powered analytics that provide clear visibility into marketing performance and ROI
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/contact" className="btn-primary px-8 py-4 text-lg">
                  Get Free Analytics Audit
                </Link>
                <Link href="/pricing" className="btn-secondary px-8 py-4 text-lg">
                  View Pricing
                </Link>
              </div>
              <p className="text-sm text-gray-600 mt-6">
                No credit card required • Free data audit • First dashboard in 7 days
              </p>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Complete Analytics Solutions
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Everything you need to track, measure, and optimize marketing performance
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
                Our Analytics Process
              </h2>
              <p className="text-xl text-gray-600">
                A proven 4-step approach to analytics success
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
                Analytics Pricing Plans
              </h2>
              <p className="text-xl text-gray-600">
                Choose the plan that fits your analytics needs
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
                See how we have helped businesses leverage data for better decisions
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
                Everything you need to know about our analytics services
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
                Ready to Make Data-Driven Decisions?
              </h2>
              <p className="text-xl mb-8 text-white/90">
                Get a free analytics audit and discover what your data is really telling you
              </p>
              <Link
                href="/contact"
                className="inline-block bg-white text-primary-600 font-semibold px-8 py-4 rounded-lg hover:bg-gray-100 transition-colors"
              >
                Get Free Analytics Audit
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
