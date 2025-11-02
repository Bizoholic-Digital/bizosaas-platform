'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Breadcrumb from '@/components/ui/Breadcrumb'
import { getResource, downloadResource, type Resource } from '@/lib/wagtail-client'
import {
  FileText,
  Video,
  Download,
  Calculator,
  BookOpen,
  ArrowRight,
  CheckCircle,
  Mail,
  User
} from 'lucide-react'

const resourceTypeConfig = {
  guide: { icon: FileText, color: 'text-blue-600', bgColor: 'bg-blue-100', label: 'Guide' },
  webinar: { icon: Video, color: 'text-purple-600', bgColor: 'bg-purple-100', label: 'Webinar' },
  ebook: { icon: BookOpen, color: 'text-green-600', bgColor: 'bg-green-100', label: 'Ebook' },
  template: { icon: Download, color: 'text-orange-600', bgColor: 'bg-orange-100', label: 'Template' },
  calculator: { icon: Calculator, color: 'text-red-600', bgColor: 'bg-red-100', label: 'Calculator' },
}

export default function ResourceDetailPage() {
  const params = useParams()
  const slug = params?.slug as string

  const [resource, setResource] = useState<Resource | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [showDownloadForm, setShowDownloadForm] = useState(false)
  const [formData, setFormData] = useState({ name: '', email: '' })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [downloadComplete, setDownloadComplete] = useState(false)

  useEffect(() => {
    async function loadResource() {
      setIsLoading(true)
      const data = await getResource(slug)
      setResource(data)
      setIsLoading(false)
    }

    if (slug) {
      loadResource()
    }
  }, [slug])

  const handleDownload = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    const result = await downloadResource(slug, formData.email, formData.name)

    if (result.success) {
      setDownloadComplete(true)
      if (result.download_url) {
        window.open(result.download_url, '_blank')
      }
    }

    setIsSubmitting(false)
  }

  if (isLoading) {
    return (
      <>
        <Navigation />
        <main className="pt-20">
          <div className="container py-16">
            <div className="max-w-4xl mx-auto">
              <div className="animate-pulse">
                <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
                <div className="h-64 bg-gray-200 rounded mb-8"></div>
              </div>
            </div>
          </div>
        </main>
        <Footer />
      </>
    )
  }

  if (!resource) {
    return (
      <>
        <Navigation />
        <main className="pt-20">
          <div className="container py-16">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">Resource Not Found</h1>
              <p className="text-xl text-gray-600 mb-8">
                The resource you're looking for doesn't exist or has been removed.
              </p>
              <Link href="/resources" className="btn-primary">
                <ArrowRight className="mr-2 h-5 w-5 rotate-180" />
                Back to Resources
              </Link>
            </div>
          </div>
        </main>
        <Footer />
      </>
    )
  }

  const config = resourceTypeConfig[resource.type]
  const Icon = config.icon

  return (
    <>
      <Navigation />
      <main className="pt-20">
        {/* Breadcrumb */}
        <div className="container py-8">
          <Breadcrumb
            items={[
              { label: 'Resources', href: '/resources' },
              { label: resource.title }
            ]}
          />
        </div>

        {/* Resource Header */}
        <section className="py-16 md:py-24 bg-gray-50">
          <div className="container px-4">
            <div className="max-w-4xl mx-auto">
              <div className="flex items-center gap-3 mb-6">
                <div className={`w-12 h-12 ${config.bgColor} rounded-xl flex items-center justify-center`}>
                  <Icon className={`h-6 w-6 ${config.color}`} />
                </div>
                <span className={`px-4 py-2 ${config.bgColor} ${config.color} rounded-full text-sm font-bold`}>
                  {config.label}
                </span>
              </div>

              <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                {resource.title}
              </h1>

              <p className="text-xl text-gray-600 mb-8">
                {resource.description}
              </p>

              {resource.downloads && (
                <div className="flex items-center gap-6 text-gray-600">
                  <div className="flex items-center gap-2">
                    <Download className="h-5 w-5" />
                    <span>{resource.downloads.toLocaleString()} downloads</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* What's Included */}
        {resource.whats_included && resource.whats_included.length > 0 && (
          <section className="py-16 md:py-24 bg-white">
            <div className="container px-4">
              <div className="max-w-4xl mx-auto">
                <h2 className="text-3xl font-bold text-gray-900 mb-8">What's Included</h2>

                <div className="grid md:grid-cols-2 gap-4">
                  {resource.whats_included.map((item, index) => (
                    <div key={index} className="flex items-start gap-3">
                      <CheckCircle className="h-6 w-6 text-green-500 flex-shrink-0 mt-1" />
                      <span className="text-gray-700">{item}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Download Section */}
        <section className="py-20 md:py-28 bg-primary-600 text-white">
          <div className="container px-4">
            <div className="max-w-2xl mx-auto">
              {!downloadComplete ? (
                !showDownloadForm ? (
                  <div className="text-center">
                    <h2 className="text-3xl font-bold mb-4">
                      Ready to Download?
                    </h2>
                    <p className="text-xl text-primary-100 mb-8">
                      Get instant access to this {config.label.toLowerCase()} and start implementing these strategies today.
                    </p>
                    <button
                      onClick={() => setShowDownloadForm(true)}
                      className="btn-white"
                    >
                      <Download className="mr-2 h-5 w-5" />
                      Download Now
                    </button>
                  </div>
                ) : (
                  <div>
                    <h2 className="text-3xl font-bold mb-4 text-center">
                      Download {resource.title}
                    </h2>
                    <p className="text-primary-100 mb-8 text-center">
                      Enter your details below to get instant access
                    </p>

                    <form onSubmit={handleDownload} className="bg-white rounded-2xl p-8 shadow-2xl">
                      <div className="space-y-6">
                        <div>
                          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                            Your Name
                          </label>
                          <div className="relative">
                            <User className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                            <input
                              type="text"
                              id="name"
                              required
                              value={formData.name}
                              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                              className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900"
                              placeholder="John Doe"
                            />
                          </div>
                        </div>

                        <div>
                          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                            Email Address
                          </label>
                          <div className="relative">
                            <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                            <input
                              type="email"
                              id="email"
                              required
                              value={formData.email}
                              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                              className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900"
                              placeholder="john@company.com"
                            />
                          </div>
                        </div>

                        <button
                          type="submit"
                          disabled={isSubmitting}
                          className="w-full bg-primary-600 text-white px-8 py-4 rounded-xl font-medium hover:bg-primary-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          {isSubmitting ? 'Processing...' : 'Download Now'}
                        </button>

                        <p className="text-xs text-gray-500 text-center">
                          By downloading, you agree to receive marketing emails from Bizoholic. Unsubscribe anytime.
                        </p>
                      </div>
                    </form>
                  </div>
                )
              ) : (
                <div className="text-center">
                  <CheckCircle className="h-16 w-16 text-green-400 mx-auto mb-6" />
                  <h2 className="text-3xl font-bold mb-4">
                    Download Started!
                  </h2>
                  <p className="text-xl text-primary-100 mb-8">
                    Check your email for the download link and additional resources.
                  </p>
                  <Link href="/resources" className="btn-white">
                    Browse More Resources
                  </Link>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Related CTA */}
        <section className="py-16 md:py-24 bg-gray-50">
          <div className="container px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Want More Than Just Resources?
              </h2>
              <p className="text-xl text-gray-600 mb-8">
                Our AI-powered platform delivers complete marketing automation with 93+ agents
                working 24/7 for your business.
              </p>
              <div className="flex flex-wrap gap-4 justify-center">
                <Link href="/contact" className="btn-primary">
                  Get Started Free
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
                <Link href="/services" className="btn-secondary">
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
