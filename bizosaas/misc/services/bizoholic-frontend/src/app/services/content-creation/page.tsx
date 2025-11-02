import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import Link from 'next/link'
import { FileText, Edit3, Target, BarChart, CheckCircle, ArrowRight, Award, Quote } from 'lucide-react'

export const metadata: Metadata = {
  title: 'Content Marketing & Creation Services | Bizoholic',
  description: 'Drive organic traffic and establish thought leadership with AI-powered content marketing. Blog posts, whitepapers, video scripts, and more.',
}

export default function ContentCreationPage() {
  const features = [
    {
      icon: <FileText className="w-6 h-6" />,
      title: 'AI-Assisted Content Creation',
      description: 'Create high-quality blog posts, articles, and whitepapers with AI-powered research and writing'
    },
    {
      icon: <Edit3 className="w-6 h-6" />,
      title: 'SEO Optimization Built-In',
      description: 'Every piece of content is optimized for search engines and user engagement'
    },
    {
      icon: <Target className="w-6 h-6" />,
      title: 'Multi-Format Content',
      description: 'Blog posts, infographics, videos, podcasts, ebooks, and social content'
    },
    {
      icon: <BarChart className="w-6 h-6" />,
      title: 'Editorial Calendar Management',
      description: 'Strategic content planning aligned with your business goals and audience needs'
    }
  ]

  const benefits = [
    'Increase organic traffic by 200-400%',
    'Establish thought leadership in your industry',
    'Generate high-quality leads with content magnets',
    'Build authority and trust with your audience',
    'Create evergreen assets that drive long-term ROI',
    'Comprehensive content strategy and analytics'
  ]

  const process = [
    {
      step: 1,
      title: 'Content Audit & Strategy',
      description: 'Analyze existing content, identify gaps, and develop strategic content roadmap'
    },
    {
      step: 2,
      title: 'Editorial Calendar Planning',
      description: 'Create comprehensive content calendar with topics, formats, and distribution channels'
    },
    {
      step: 3,
      title: 'Content Creation & Optimization',
      description: 'Produce high-quality content optimized for SEO, engagement, and conversions'
    },
    {
      step: 4,
      title: 'Publish & Amplify',
      description: 'Distribute content across channels, measure performance, and refine strategy'
    }
  ]

  const pricing = [
    {
      name: 'Starter Content',
      price: '$399',
      period: '/month',
      description: 'Perfect for small businesses',
      features: [
        '4 blog posts per month (800-1,200 words)',
        'SEO keyword research and optimization',
        'Meta descriptions and title tags',
        'Internal linking strategy',
        'Monthly performance report'
      ],
      popular: false
    },
    {
      name: 'Growth Content',
      price: '$799',
      period: '/month',
      description: 'For growing businesses',
      features: [
        'Everything in Starter Content',
        '8 blog posts per month (1,200-1,800 words)',
        '2 long-form whitepapers or ebooks per month',
        'Infographic or video script creation',
        'Content distribution strategy',
        'Email newsletter content',
        'Bi-weekly strategy calls'
      ],
      popular: true
    },
    {
      name: 'Enterprise Content',
      price: '$1,599',
      period: '/month',
      description: 'For established brands',
      features: [
        'Everything in Growth Content',
        'Unlimited blog posts and articles',
        '4 long-form content pieces per month',
        'Video scripts and podcast outlines',
        'Case study and whitepaper production',
        'Content repurposing across formats',
        'Dedicated content strategist',
        'Custom analytics dashboard'
      ],
      popular: false
    }
  ]

  const caseStudies = [
    {
      industry: 'SaaS Company',
      challenge: 'Zero organic traffic, no content strategy, difficulty establishing authority',
      solution: 'Comprehensive content marketing strategy with weekly blog posts and monthly whitepapers',
      results: [
        '320% increase in organic traffic in 9 months',
        '180 qualified leads generated from content',
        'Ranking on page 1 for 45 industry keywords',
        '$240,000 in pipeline attributed to content marketing'
      ]
    },
    {
      industry: 'B2B Professional Services',
      challenge: 'Long sales cycles, difficulty demonstrating expertise, limited lead generation',
      solution: 'Thought leadership content strategy with industry insights, case studies, and educational content',
      results: [
        '180 qualified leads from content downloads',
        '45% reduction in sales cycle length',
        '3x increase in inbound demo requests',
        'Positioned as industry thought leader in 6 months'
      ]
    }
  ]

  const testimonials = [
    {
      name: 'Rachel Thompson',
      company: 'CloudSync Technologies',
      role: 'VP of Marketing',
      quote: 'Before Bizoholic, we had no content strategy. Now we publish consistently, rank for dozens of keywords, and generate 30+ qualified leads per month from our blog alone. The quality and consistency are remarkable.',
      rating: 5
    },
    {
      name: 'Michael Chen',
      company: 'Strategic Consulting Group',
      role: 'Managing Partner',
      quote: 'Our content went from sporadic and mediocre to strategic and high-quality. We have become the go-to resource in our industry, and our sales team loves having quality content to share with prospects. The ROI has been outstanding.',
      rating: 5
    }
  ]

  const faqs = [
    {
      question: 'What types of content do you create?',
      answer: 'We create all forms of content including blog posts, articles, whitepapers, ebooks, case studies, infographics, video scripts, podcast outlines, social media content, email newsletters, landing page copy, and more. Every piece is customized to your brand voice and business goals.'
    },
    {
      question: 'How do you ensure content quality and accuracy?',
      answer: 'Our process includes extensive research, subject matter expert review, multi-stage editing, and fact-checking. We use AI to assist with research and optimization, but human writers and editors ensure quality, accuracy, and authenticity. Every piece goes through at least 3 rounds of review.'
    },
    {
      question: 'Will the content be unique and plagiarism-free?',
      answer: 'Absolutely. All content is 100% original and runs through plagiarism detection tools. We create unique perspectives and insights for your business. You own all content rights, and we never reuse content across clients.'
    },
    {
      question: 'How long does it take to see results from content marketing?',
      answer: 'You will start seeing engagement within the first 30 days. Organic traffic improvements typically appear within 60-90 days. Lead generation and authority building usually take 3-6 months. Content marketing is a long-term strategy with compounding benefits over time.'
    },
    {
      question: 'Do you handle content distribution and promotion?',
      answer: 'Yes! Our Growth and Enterprise plans include content distribution strategy across your blog, social media, email newsletters, and other channels. We also provide guidance on paid promotion opportunities to amplify your best-performing content.'
    },
    {
      question: 'Can you write in our industry or niche?',
      answer: 'Yes! We have successfully created content for 50+ industries including tech, healthcare, finance, legal, manufacturing, professional services, and more. Our research process ensures we understand your industry, audience, and competitive landscape. We can write technical content, thought leadership, or educational content depending on your needs.'
    },
    {
      question: 'What if we need to cancel or pause?',
      answer: 'All plans are month-to-month with no long-term contracts. You can cancel or pause anytime. However, we recommend at least 6 months to build content momentum and see measurable results. Most clients stay for years because content marketing delivers compounding ROI.'
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
              { label: 'Content Marketing' }
            ]} />
          </div>
        </section>

        {/* Hero Section */}
        <section className="bg-gray-50 py-20">
          <div className="container">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl font-bold text-gray-900 mb-6">
                Content Marketing & Creation
              </h1>
              <p className="text-xl text-gray-700 mb-8">
                Drive organic growth and establish industry authority with strategic, high-quality content that engages and converts
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/contact" className="btn-primary px-8 py-4 text-lg">
                  Get Free Content Audit
                </Link>
                <Link href="/pricing" className="btn-secondary px-8 py-4 text-lg">
                  View Pricing
                </Link>
              </div>
              <p className="text-sm text-gray-600 mt-6">
                No credit card required • Free strategy session • First article in 7 days
              </p>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Comprehensive Content Solutions
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Everything you need to create, optimize, and distribute high-performing content
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
                Our Content Marketing Process
              </h2>
              <p className="text-xl text-gray-600">
                A proven 4-step approach to content success
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
                Content Marketing Pricing Plans
              </h2>
              <p className="text-xl text-gray-600">
                Choose the plan that fits your content needs
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
                See how we have helped businesses grow through strategic content
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
                Everything you need to know about our content marketing services
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
                Ready to Build Your Content Engine?
              </h2>
              <p className="text-xl mb-8 text-white/90">
                Get a free content audit and discover how to grow with strategic content
              </p>
              <Link
                href="/contact"
                className="inline-block bg-white text-primary-600 font-semibold px-8 py-4 rounded-lg hover:bg-gray-100 transition-colors"
              >
                Get Free Content Audit
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
