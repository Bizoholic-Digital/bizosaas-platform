'use client'

import Link from 'next/link'

export default function CampaignsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Campaigns</h1>
          <Link href="/dashboard/campaigns/new" className="btn-primary">Create Campaign</Link>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <p className="text-gray-600">Active campaigns list will be displayed here.</p>
        </div>
      </div>
    </div>
  )
}
