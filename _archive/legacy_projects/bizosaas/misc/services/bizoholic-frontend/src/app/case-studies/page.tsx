import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Case Studies - Client Success Stories | Bizoholic',
  description: 'See how businesses achieve remarkable results with Bizoholic AI-powered marketing.',
}

export default function CaseStudiesPage() {
  const caseStudies = [
    {
      slug: 'saas-company-300-percent-growth',
      title: 'SaaS Company Achieves 300% Growth in 6 Months',
      client: 'TechStart Solutions',
      industry: 'SaaS',
      results: { metric1: '+300% Revenue', metric2: '+250% Leads', metric3: '-40% CAC' },
      image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800'
    },
    {
      slug: 'ecommerce-roi-improvement',
      title: 'E-commerce Store Doubles ROAS with AI Optimization',
      client: 'Fashion Forward',
      industry: 'E-commerce',
      results: { metric1: '+200% ROAS', metric2: '+150% Orders', metric3: '-35% CPA' },
      image: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800'
    }
  ]

  return (
    <>
      <Navigation />
      <main className="min-h-screen bg-white">
        <section className="bg-gray-50 py-20">
          <div className="container">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl font-bold text-gray-900 mb-6">Case Studies</h1>
              <p className="text-xl text-gray-700">Real results from real businesses using Bizoholic</p>
            </div>
          </div>
        </section>
        <section className="py-20">
          <div className="container">
            <div className="grid md:grid-cols-2 gap-8">
              {caseStudies.map((study) => (
                <Link key={study.slug} href={`/case-studies/${study.slug}`} className="group block bg-white rounded-xl border border-gray-200 hover:shadow-xl transition-all overflow-hidden">
                  <img src={study.image} alt={study.title} className="w-full aspect-video object-cover" />
                  <div className="p-6">
                    <span className="text-sm text-primary-600 font-semibold">{study.industry}</span>
                    <h3 className="text-2xl font-bold text-gray-900 mt-2 mb-4">{study.title}</h3>
                    <div className="grid grid-cols-3 gap-4 pt-4 border-t">
                      {Object.values(study.results).map((result, i) => (
                        <div key={i} className="text-center">
                          <div className="text-2xl font-bold text-primary-600">{result}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
