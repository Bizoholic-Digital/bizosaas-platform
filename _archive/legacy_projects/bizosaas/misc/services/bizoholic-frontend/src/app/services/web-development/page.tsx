import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import Link from 'next/link'
import { Code, Smartphone, Zap, Shield, CheckCircle, ArrowRight, Award, Quote } from 'lucide-react'

export const metadata: Metadata = {
  title: 'Web Design & Development Services | Bizoholic',
  description: 'Build high-converting, lightning-fast websites with modern design and AI-powered optimization. Custom web development that drives results.',
}

export default function WebDevelopmentPage() {
  const features = [
    {
      icon: <Code className="w-6 h-6" />,
      title: 'Modern Responsive Design',
      description: 'Beautiful, mobile-first websites that look perfect on every device and screen size'
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: 'Performance Optimization',
      description: 'Lightning-fast load times with optimized code, images, and caching strategies'
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: 'SEO-Ready Architecture',
      description: 'Built from the ground up for search engine visibility and organic rankings'
    },
    {
      icon: <Smartphone className="w-6 h-6" />,
      title: 'Conversion-Focused UX',
      description: 'User experience designed to guide visitors toward taking action and converting'
    }
  ]

  const benefits = [
    'Professional online presence that builds trust',
    'Convert 2-3x more visitors into leads and customers',
    'Lightning-fast load times (under 2 seconds)',
    'Mobile-first design for modern users',
    'SEO-optimized for better search rankings',
    'Secure, scalable, and future-proof technology'
  ]

  const process = [
    {
      step: 1,
      title: 'Discovery & Planning',
      description: 'Understand your goals, audience, and requirements through detailed consultation'
    },
    {
      step: 2,
      title: 'Design & Prototyping',
      description: 'Create wireframes and visual designs that align with your brand and objectives'
    },
    {
      step: 3,
      title: 'Development & Testing',
      description: 'Build your website with clean code, test across devices, and optimize performance'
    },
    {
      step: 4,
      title: 'Launch & Support',
      description: 'Deploy your site, train your team, and provide ongoing maintenance and updates'
    }
  ]

  const pricing = [
    {
      name: 'Starter Website',
      price: '$2,999',
      period: 'one-time',
      description: 'Perfect for small businesses',
      features: [
        'Up to 5 custom pages',
        'Mobile-responsive design',
        'Contact form integration',
        'Basic SEO optimization',
        'Google Analytics setup',
        '30 days of support',
        'Content management system (CMS)'
      ],
      popular: false
    },
    {
      name: 'Growth Website',
      price: '$5,999',
      period: 'one-time',
      description: 'For growing businesses',
      features: [
        'Everything in Starter Website',
        'Up to 15 custom pages',
        'Advanced integrations (CRM, email, etc.)',
        'E-commerce capability (up to 50 products)',
        'Blog with unlimited posts',
        'Advanced SEO optimization',
        'Performance optimization',
        '90 days of support'
      ],
      popular: true
    },
    {
      name: 'Enterprise Website',
      price: 'Custom',
      period: 'pricing',
      description: 'For established brands',
      features: [
        'Everything in Growth Website',
        'Unlimited pages and custom features',
        'Full e-commerce platform (unlimited products)',
        'Custom API integrations',
        'Multi-language support',
        'Advanced security features',
        'Priority support',
        '6 months of support included'
      ],
      popular: false
    }
  ]

  const caseStudies = [
    {
      industry: 'Local Service Business',
      challenge: 'Outdated website, poor mobile experience, minimal online inquiries',
      solution: 'Complete website redesign with mobile-first approach, speed optimization, and conversion-focused design',
      results: [
        '280% increase in online inquiries within 3 months',
        'Page load time reduced from 8s to 1.2s',
        '65% of traffic now from mobile devices',
        'Bounce rate decreased from 72% to 28%'
      ]
    },
    {
      industry: 'E-commerce Store',
      challenge: 'Slow checkout process, high cart abandonment, poor search functionality',
      solution: 'Custom e-commerce platform with streamlined checkout, advanced search, and performance optimization',
      results: [
        '65% faster load times across all pages',
        '35% increase in conversion rate',
        'Cart abandonment reduced by 45%',
        '$180,000 additional revenue in first 6 months'
      ]
    }
  ]

  const testimonials = [
    {
      name: 'Patricia Anderson',
      company: 'Anderson Legal Services',
      role: 'Managing Partner',
      quote: 'Our old website was embarrassing. Bizoholic built us a stunning, professional site that actually converts visitors into clients. We now get 15-20 qualified leads per month directly from the website. Best investment we have made.',
      rating: 5
    },
    {
      name: 'Tom Wilson',
      company: 'Wilson Home Furnishings',
      role: 'Owner',
      quote: 'The new website is lightning fast and looks amazing on phones and tablets. Our online sales tripled in the first quarter. The team really understood our business and delivered exactly what we needed.',
      rating: 5
    }
  ]

  const faqs = [
    {
      question: 'How long does it take to build a website?',
      answer: 'Timeline depends on complexity. A Starter Website typically takes 3-4 weeks. A Growth Website takes 6-8 weeks. Enterprise websites can take 10-16 weeks depending on custom features and integrations. We provide a detailed timeline during the discovery phase.'
    },
    {
      question: 'Do you provide website hosting and maintenance?',
      answer: 'Yes! We offer managed hosting starting at $49/month which includes hosting, security updates, backups, and basic maintenance. We also offer comprehensive maintenance plans starting at $199/month for businesses that need ongoing updates and support.'
    },
    {
      question: 'Will I be able to update the website myself?',
      answer: 'Absolutely. We build all websites with user-friendly content management systems (typically WordPress or a headless CMS). We provide training and documentation so you can easily update text, images, and blog posts without any coding knowledge.'
    },
    {
      question: 'Is the website mobile-friendly?',
      answer: 'Yes, every website we build is fully responsive and mobile-first. With 60%+ of web traffic coming from mobile devices, we prioritize mobile experience. Your site will look and function perfectly on phones, tablets, laptops, and desktops.'
    },
    {
      question: 'What happens if I need changes after launch?',
      answer: 'All packages include post-launch support (30-180 days depending on package). During this time, we fix any bugs and make minor adjustments. After that, you can choose a maintenance plan or pay for updates on an hourly basis ($150/hour).'
    },
    {
      question: 'Can you integrate with my existing tools and systems?',
      answer: 'Yes! We integrate with popular tools like CRMs (Salesforce, HubSpot), email platforms (Mailchimp, Klaviyo), payment processors (Stripe, PayPal), booking systems, and more. Custom integrations are available in Growth and Enterprise packages.'
    },
    {
      question: 'What if I already have a website?',
      answer: 'We can either redesign your existing site or migrate your content to a completely new platform. We handle everything including content migration, URL redirects, SEO preservation, and ensuring zero downtime during the transition.'
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
              { label: 'Web Development' }
            ]} />
          </div>
        </section>

        {/* Hero Section */}
        <section className="bg-gray-50 py-20">
          <div className="container">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl font-bold text-gray-900 mb-6">
                Web Design & Development
              </h1>
              <p className="text-xl text-gray-700 mb-8">
                Transform your online presence with stunning, high-performing websites that convert visitors into customers
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/contact" className="btn-primary px-8 py-4 text-lg">
                  Get Free Website Audit
                </Link>
                <Link href="/pricing" className="btn-secondary px-8 py-4 text-lg">
                  View Pricing
                </Link>
              </div>
              <p className="text-sm text-gray-600 mt-6">
                No credit card required • Free consultation • Launch in 30 days
              </p>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Complete Web Development Solutions
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Everything you need for a professional, high-converting website
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
                Our Development Process
              </h2>
              <p className="text-xl text-gray-600">
                A proven 4-step approach to website success
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
                Web Development Pricing Plans
              </h2>
              <p className="text-xl text-gray-600">
                Choose the plan that fits your business needs
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
                See how we have helped businesses transform their online presence
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
                Everything you need to know about our web development services
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
                Ready to Transform Your Online Presence?
              </h2>
              <p className="text-xl mb-8 text-white/90">
                Get a free website audit and discover how we can help you succeed online
              </p>
              <Link
                href="/contact"
                className="inline-block bg-white text-primary-600 font-semibold px-8 py-4 rounded-lg hover:bg-gray-100 transition-colors"
              >
                Get Free Website Audit
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
