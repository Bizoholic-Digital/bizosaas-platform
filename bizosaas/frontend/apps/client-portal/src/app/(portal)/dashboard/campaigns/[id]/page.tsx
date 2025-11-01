'use client'

import { useParams } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'

export default function CampaignDetailPage() {
  const params = useParams()
  const id = params.id as string
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        <Link href="/dashboard/campaigns" className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-6">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Campaigns
        </Link>
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Campaign Details</h1>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <p className="text-gray-600">Campaign ID: {id}</p>
          <p className="text-gray-600 mt-2">Detailed campaign metrics and performance data will be displayed here.</p>
        </div>
      </div>
    </div>
  )
}
