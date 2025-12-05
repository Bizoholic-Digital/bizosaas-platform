'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import { getResources, type Resource } from '@/lib/wagtail-client'
import {
  Search,
  FileText,
  Video,
  Download,
  Calculator,
  BookOpen,
  ArrowRight,
  TrendingDown
} from 'lucide-react'

const resourceTypeConfig = {
  guide: { icon: FileText, color: 'text-blue-600', bgColor: 'bg-blue-100', label: 'Guide' },
  webinar: { icon: Video, color: 'text-purple-600', bgColor: 'bg-purple-100', label: 'Webinar' },
  ebook: { icon: BookOpen, color: 'text-green-600', bgColor: 'bg-green-100', label: 'Ebook' },
  template: { icon: Download, color: 'text-orange-600', bgColor: 'bg-orange-100', label: 'Template' },
  calculator: { icon: Calculator, color: 'text-red-600', bgColor: 'bg-red-100', label: 'Calculator' },
}

export default function ResourcesPage() {
  const [resources, setResources] = useState<Resource[]>([])
  const [selectedType, setSelectedType] = useState<string>('')
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    async function loadResources() {
      setIsLoading(true)
      const data = await getResources({ type: selectedType || undefined })
      setResources(data.results)
      setIsLoading(false)
    }

    loadResources()
  }, [selectedType])

  const filteredResources = resources.filter(resource =>
    searchQuery === '' ||
    resource.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    resource.description.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <>
      <Navigation />
      <main className="pt-20">
        {/* Breadcrumb */}
        <div className="container py-8">
          <Breadcrumb items={[{ label: 'Resources' }]} />
        </div>

        {/* Hero Section */}
        <section className="py-16 md:py-24 bg-gray-50">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h1 className="heading-1 mb-6">Free Marketing Resources</h1>
              <p className="text-xl text-gray-600 mb-8">
                Download our collection of guides, templates, calculators, and tools to help you
                grow your business with data-driven marketing strategies.
              </p>

              {/* Search Bar */}
              <div className="max-w-2xl mx-auto">
                <div className="relative">
                  <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search resources..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-12 pr-4 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Filter Tabs */}
        <section className="py-8 bg-white border-b border-gray-200 sticky top-16 z-10">
          <div className="container">
            <div className="flex flex-wrap gap-3 justify-center">
              <button
                onClick={() => setSelectedType('')}
                className={`px-6 py-2 rounded-full transition-colors ${
                  selectedType === ''
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                All Resources
              </button>
              {Object.entries(resourceTypeConfig).map(([key, config]) => (
                <button
                  key={key}
                  onClick={() => setSelectedType(key)}
                  className={`px-6 py-2 rounded-full transition-colors flex items-center gap-2 ${
                    selectedType === key
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  <config.icon className="h-4 w-4" />
                  {config.label}s
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* Resources Grid */}
        <section className="py-16 md:py-24">
          <div className="container px-4">
            {isLoading ? (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                <p className="mt-4 text-gray-600">Loading resources...</p>
              </div>
            ) : filteredResources.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-600">No resources found matching your search.</p>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                {filteredResources.map((resource) => {
                  const config = resourceTypeConfig[resource.type]
                  const Icon = config.icon

                  return (
                    <article
                      key={resource.id}
                      className="card-premium overflow-hidden group hover:shadow-xl transition-all duration-300"
                    >
                      {/* Icon Header */}
                      <div className={`${config.bgColor} p-8 flex items-center justify-center`}>
                        <Icon className={`h-16 w-16 ${config.color}`} />
                      </div>

                      {/* Content */}
                      <div className="p-6">
                        {/* Type Badge */}
                        <div className="flex items-center justify-between mb-3">
                          <span className={`inline-block px-3 py-1 ${config.bgColor} ${config.color} text-xs font-medium rounded-full`}>
                            {config.label}
                          </span>
                          {resource.downloads && (
                            <div className="flex items-center text-xs text-gray-500">
                              <TrendingDown className="h-4 w-4 mr-1" />
                              {resource.downloads.toLocaleString()} downloads
                            </div>
                          )}
                        </div>

                        {/* Title */}
                        <h2 className="text-lg font-semibold text-gray-900 mb-3 group-hover:text-primary-600 transition-colors line-clamp-2">
                          <Link href={`/resources/${resource.slug}`}>
                            {resource.title}
                          </Link>
                        </h2>

                        {/* Description */}
                        <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                          {resource.description}
                        </p>

                        {/* CTA Button */}
                        <Link
                          href={`/resources/${resource.slug}`}
                          className={`inline-flex items-center ${config.color} hover:opacity-80 font-medium text-sm group/btn`}
                        >
                          Download Free
                          <ArrowRight className="ml-2 h-4 w-4 group-hover/btn:translate-x-1 transition-transform" />
                        </Link>
                      </div>
                    </article>
                  )
                })}
              </div>
            )}
          </div>
        </section>

        {/* Can't Find Section */}
        <section className="py-16 md:py-20 bg-gray-50">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="heading-2 mb-4">Can't Find What You Need?</h2>
              <p className="text-lg text-gray-600 mb-8">
                We're constantly adding new resources. Let us know what you're looking for,
                and we'll create it for you.
              </p>
              <Link href="/contact" className="btn-primary">
                Request a Resource
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 md:py-28 bg-primary-600 text-white">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-4xl font-bold mb-6">
                Want More Than Just Resources?
              </h2>
              <p className="text-xl text-primary-100 mb-8">
                Our AI-powered platform delivers complete marketing automation with 93+ agents
                working 24/7 for your business. No downloads required.
              </p>
              <div className="flex flex-wrap gap-4 justify-center">
                <Link href="/contact" className="btn-white">
                  Get Started Free
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
                <Link href="/services" className="btn-white-outline">
                  View Our Services
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
