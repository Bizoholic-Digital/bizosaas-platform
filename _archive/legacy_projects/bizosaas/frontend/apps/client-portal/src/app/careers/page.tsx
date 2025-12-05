import { Metadata } from 'next'
import Navigation from '@/components/layout/Navigation'
import Footer from '@/components/layout/Footer'
import Link from 'next/link'
import { Briefcase, MapPin, Clock } from 'lucide-react'

export const metadata: Metadata = {
  title: 'Careers - Join Our Team | Bizoholic',
  description: 'Join Bizoholic and help businesses transform their marketing with AI automation.',
}

export default function CareersPage() {
  const jobs = [
    { title: 'Senior AI Engineer', location: 'Remote', type: 'Full-time', department: 'Engineering' },
    { title: 'Marketing Manager', location: 'San Francisco, CA', type: 'Full-time', department: 'Marketing' },
    { title: 'Customer Success Manager', location: 'Remote', type: 'Full-time', department: 'Customer Success' }
  ]

  return (
    <>
      <Navigation />
      <main className="min-h-screen bg-white">
        <section className="bg-gray-50 py-20">
          <div className="container">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl font-bold text-gray-900 mb-6">Join Our Team</h1>
              <p className="text-xl text-gray-700">Help us revolutionize marketing with AI automation</p>
            </div>
          </div>
        </section>
        <section className="py-20">
          <div className="container">
            <div className="max-w-4xl mx-auto space-y-6">
              {jobs.map((job, i) => (
                <div key={i} className="bg-white p-6 rounded-xl border border-gray-200 hover:shadow-lg transition-all">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                    <div className="mb-4 md:mb-0">
                      <h3 className="text-2xl font-bold text-gray-900 mb-2">{job.title}</h3>
                      <div className="flex flex-wrap gap-4 text-gray-600">
                        <span className="flex items-center"><MapPin className="w-4 h-4 mr-1" />{job.location}</span>
                        <span className="flex items-center"><Clock className="w-4 h-4 mr-1" />{job.type}</span>
                        <span className="flex items-center"><Briefcase className="w-4 h-4 mr-1" />{job.department}</span>
                      </div>
                    </div>
                    <Link href="/contact" className="btn-primary px-6 py-2">Apply Now</Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
