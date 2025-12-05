/**
 * Bizoholic Portfolio Page
 * Showcase of successful marketing campaigns and client results
 */

'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'

export default function PortfolioPage() {
  const [selectedCategory, setSelectedCategory] = useState('all')

  const categories = [
    { id: 'all', name: 'All Projects' },
    { id: 'ecommerce', name: 'E-commerce' },
    { id: 'saas', name: 'SaaS' },
    { id: 'healthcare', name: 'Healthcare' },
    { id: 'fintech', name: 'Fintech' },
    { id: 'real-estate', name: 'Real Estate' }
  ]

  const projects = [
    {
      id: 1,
      title: 'TechFlow SaaS Growth',
      category: 'saas',
      client: 'TechFlow Solutions',
      industry: 'Project Management Software',
      challenge: 'Low user acquisition and poor conversion rates',
      solution: 'Complete funnel optimization, content marketing strategy, and paid acquisition campaigns',
      results: {
        metric1: { label: 'User Growth', value: '340%', period: '6 months' },
        metric2: { label: 'Conversion Rate', value: '8.5%', period: 'from 2.1%' },
        metric3: { label: 'Revenue Increase', value: '$2.3M', period: 'annual recurring' }
      },
      image: '/images/portfolio/techflow.jpg',
      testimonial: 'Bizoholic transformed our entire marketing approach. The results speak for themselves.',
      testimonialAuthor: 'Sarah Chen, CEO TechFlow'
    },
    {
      id: 2,
      title: 'HealthPlus Digital Transformation',
      category: 'healthcare',
      client: 'HealthPlus Medical',
      industry: 'Telemedicine Platform',
      challenge: 'Trust building and patient acquisition in competitive market',
      solution: 'Authority-building content, doctor testimonials, and targeted healthcare advertising',
      results: {
        metric1: { label: 'Patient Acquisition', value: '450%', period: '12 months' },
        metric2: { label: 'Trust Score', value: '95%', period: 'patient satisfaction' },
        metric3: { label: 'Revenue Growth', value: '$5.8M', period: 'first year' }
      },
      image: '/images/portfolio/healthplus.jpg',
      testimonial: 'The team understood our unique healthcare marketing challenges perfectly.',
      testimonialAuthor: 'Dr. Michael Rodriguez, CMO'
    },
    {
      id: 3,
      title: 'FinanceMax Lead Generation',
      category: 'fintech',
      client: 'FinanceMax Solutions',
      industry: 'Personal Finance App',
      challenge: 'High customer acquisition costs and low lifetime value',
      solution: 'Sophisticated audience segmentation, lifecycle marketing, and retention optimization',
      results: {
        metric1: { label: 'CAC Reduction', value: '65%', period: 'cost per customer' },
        metric2: { label: 'LTV Increase', value: '230%', period: 'customer lifetime value' },
        metric3: { label: 'App Downloads', value: '1.2M', period: '8 months' }
      },
      image: '/images/portfolio/financemax.jpg',
      testimonial: 'ROI-focused approach that transformed our unit economics completely.',
      testimonialAuthor: 'Jennifer Park, Growth Director'
    },
    {
      id: 4,
      title: 'ShopSmart E-commerce Scale',
      category: 'ecommerce',
      client: 'ShopSmart Retail',
      industry: 'Fashion E-commerce',
      challenge: 'Seasonal sales fluctuations and inventory management',
      solution: 'Predictive analytics, cross-selling automation, and omnichannel marketing',
      results: {
        metric1: { label: 'Sales Growth', value: '280%', period: 'year over year' },
        metric2: { label: 'Average Order Value', value: '+185%', period: 'per transaction' },
        metric3: { label: 'Customer Retention', value: '78%', period: 'repeat purchases' }
      },
      image: '/images/portfolio/shopsmart.jpg',
      testimonial: 'From struggling startup to industry leader in just 18 months.',
      testimonialAuthor: 'David Kim, Founder'
    },
    {
      id: 5,
      title: 'PropertyPro Real Estate Lead Engine',
      category: 'real-estate',
      client: 'PropertyPro Realty',
      industry: 'Real Estate Services',
      challenge: 'Low-quality leads and long sales cycles',
      solution: 'Lead qualification automation, nurture sequences, and local SEO dominance',
      results: {
        metric1: { label: 'Qualified Leads', value: '520%', period: 'increase' },
        metric2: { label: 'Sales Cycle', value: '-45%', period: 'reduction' },
        metric3: { label: 'Commission Revenue', value: '$12M', period: 'additional annual' }
      },
      image: '/images/portfolio/propertypro.jpg',
      testimonial: 'Lead quality and volume exceeded all our expectations.',
      testimonialAuthor: 'Lisa Thompson, Sales Director'
    },
    {
      id: 6,
      title: 'CloudSync SaaS Expansion',
      category: 'saas',
      client: 'CloudSync Technologies',
      industry: 'Cloud Storage Platform',
      challenge: 'International expansion and enterprise sales',
      solution: 'Multi-market strategy, ABM campaigns, and sales enablement',
      results: {
        metric1: { label: 'Enterprise Clients', value: '150+', period: 'new acquisitions' },
        metric2: { label: 'International Revenue', value: '400%', period: 'growth' },
        metric3: { label: 'Deal Size', value: '3.5x', period: 'average increase' }
      },
      image: '/images/portfolio/cloudsync.jpg',
      testimonial: 'Global expansion became seamless with their strategic approach.',
      testimonialAuthor: 'Robert Chang, VP Sales'
    }
  ]

  const filteredProjects = selectedCategory === 'all' 
    ? projects 
    : projects.filter(project => project.category === selectedCategory)

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
              <Link href="/portfolio" className="text-indigo-600 font-medium">Portfolio</Link>
              <Link href="/pricing" className="text-gray-600 hover:text-indigo-600 transition-colors">Pricing</Link>
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
              Success <span className="text-indigo-600">Stories</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
              Discover how we've helped businesses across industries become addicted to growth 
              through data-driven marketing strategies and innovative campaigns.
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
              <div className="text-center">
                <div className="text-3xl font-bold text-indigo-600 mb-2">500+</div>
                <div className="text-gray-600">Projects Delivered</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-indigo-600 mb-2">$50M+</div>
                <div className="text-gray-600">Revenue Generated</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-indigo-600 mb-2">95%</div>
                <div className="text-gray-600">Client Satisfaction</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-indigo-600 mb-2">300%</div>
                <div className="text-gray-600">Average ROI</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Filter Section */}
      <section className="py-12 bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap justify-center gap-4">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-6 py-3 rounded-full font-medium transition-all duration-200 ${
                  selectedCategory === category.id
                    ? 'bg-indigo-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {category.name}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Portfolio Grid */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid gap-12">
            {filteredProjects.map((project, index) => (
              <div key={project.id} className={`grid lg:grid-cols-2 gap-12 items-center ${index % 2 === 1 ? 'lg:grid-flow-col-dense' : ''}`}>
                {/* Project Image */}
                <div className={`${index % 2 === 1 ? 'lg:col-start-2' : ''}`}>
                  <div className="aspect-video bg-gradient-to-br from-indigo-100 to-cyan-100 rounded-2xl flex items-center justify-center">
                    <div className="text-center p-8">
                      <div className="w-20 h-20 bg-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="white" className="w-10 h-10">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
                        </svg>
                      </div>
                      <h3 className="text-xl font-bold text-gray-900 mb-2">{project.client}</h3>
                      <p className="text-gray-600">{project.industry}</p>
                    </div>
                  </div>
                </div>

                {/* Project Details */}
                <div className={`${index % 2 === 1 ? 'lg:col-start-1 lg:row-start-1' : ''}`}>
                  <div className="mb-4">
                    <span className="inline-block bg-indigo-100 text-indigo-600 px-3 py-1 rounded-full text-sm font-medium mb-4">
                      {categories.find(cat => cat.id === project.category)?.name}
                    </span>
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">{project.title}</h2>
                  </div>

                  <div className="space-y-6">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">Challenge</h3>
                      <p className="text-gray-600">{project.challenge}</p>
                    </div>

                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">Solution</h3>
                      <p className="text-gray-600">{project.solution}</p>
                    </div>

                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Results</h3>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div className="text-center p-4 bg-gray-50 rounded-lg">
                          <div className="text-2xl font-bold text-indigo-600 mb-1">{project.results.metric1.value}</div>
                          <div className="text-sm text-gray-600">{project.results.metric1.label}</div>
                          <div className="text-xs text-gray-500">{project.results.metric1.period}</div>
                        </div>
                        <div className="text-center p-4 bg-gray-50 rounded-lg">
                          <div className="text-2xl font-bold text-indigo-600 mb-1">{project.results.metric2.value}</div>
                          <div className="text-sm text-gray-600">{project.results.metric2.label}</div>
                          <div className="text-xs text-gray-500">{project.results.metric2.period}</div>
                        </div>
                        <div className="text-center p-4 bg-gray-50 rounded-lg">
                          <div className="text-2xl font-bold text-indigo-600 mb-1">{project.results.metric3.value}</div>
                          <div className="text-sm text-gray-600">{project.results.metric3.label}</div>
                          <div className="text-xs text-gray-500">{project.results.metric3.period}</div>
                        </div>
                      </div>
                    </div>

                    <div className="bg-indigo-50 p-6 rounded-lg border-l-4 border-indigo-600">
                      <blockquote className="text-gray-700 italic mb-3">
                        "{project.testimonial}"
                      </blockquote>
                      <cite className="text-indigo-600 font-medium">- {project.testimonialAuthor}</cite>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-indigo-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Be Our Next Success Story?
          </h2>
          <p className="text-xl text-indigo-100 mb-8 max-w-2xl mx-auto">
            Join hundreds of businesses that have transformed their marketing with Bizoholic. 
            Let's create your success story together.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/contact">
              <button className="bg-white text-indigo-600 px-8 py-4 rounded-lg font-medium hover:bg-gray-50 transition-colors">
                Start Your Project
              </button>
            </Link>
            <Link href="/pricing">
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-medium hover:bg-white hover:text-indigo-600 transition-colors">
                View Pricing
              </button>
            </Link>
          </div>
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