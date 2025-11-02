'use client'

import { useParams } from 'next/navigation'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'

export default function CaseStudyPage() {
  const params = useParams()
  const slug = params.slug as string
  return (
    <>
      <Navigation />
      <main className="min-h-screen bg-white">
        <section className="bg-gray-50 py-12">
          <div className="container">
            <Link href="/case-studies" className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-6">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Case Studies
            </Link>
            <div className="max-w-4xl">
              <h1 className="text-5xl font-bold text-gray-900 mb-6">SaaS Company Achieves 300% Growth</h1>
              <p className="text-xl text-gray-700">How TechStart Solutions transformed their marketing with AI automation</p>
            </div>
          </div>
        </section>
        <section className="py-20">
          <div className="container max-w-4xl">
            <div className="prose prose-lg max-w-none">
              <h2>Challenge</h2>
              <p>TechStart Solutions needed to scale their marketing efforts without increasing costs.</p>
              <h2>Solution</h2>
              <p>We implemented AI-powered marketing automation across all channels.</p>
              <h2>Results</h2>
              <ul>
                <li>300% increase in revenue</li>
                <li>250% more qualified leads</li>
                <li>40% reduction in customer acquisition cost</li>
              </ul>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
