'use client'

import { useAuth } from '@bizoholic-digital/auth'
import Link from 'next/link'
import { BarChart3, Users, TrendingUp, DollarSign, ArrowRight } from 'lucide-react'

export default function DashboardPage() {
  const { user } = useAuth()

  const stats = [
    { label: 'Total Projects', value: '12', change: '+3', icon: <BarChart3 /> },
    { label: 'Active Campaigns', value: '8', change: '+2', icon: <TrendingUp /> },
    { label: 'Total Leads', value: '1,245', change: '+145', icon: <Users /> },
    { label: 'Revenue', value: '$24,500', change: '+15%', icon: <DollarSign /> }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.name || 'User'}!
          </h1>
          <p className="text-gray-600">Here&apos;s what&apos;s happening with your marketing</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, i) => (
            <div key={i} className="bg-white p-6 rounded-xl border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center text-primary-600">
                  {stat.icon}
                </div>
                <span className="text-green-600 text-sm font-semibold">{stat.change}</span>
              </div>
              <p className="text-gray-600 text-sm mb-1">{stat.label}</p>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
            </div>
          ))}
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Projects</h2>
            <div className="space-y-4">
              {['SEO Campaign Q1', 'PPC Ads - Summer Sale', 'Email Automation'].map((project, i) => (
                <div key={i} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <span className="font-medium">{project}</span>
                  <Link href="/dashboard/projects" className="text-primary-600 hover:text-primary-700">
                    View <ArrowRight className="w-4 h-4 inline" />
                  </Link>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
            <div className="space-y-3">
              <Link href="/dashboard/campaigns/new" className="block btn-primary py-3 text-center">
                Create New Campaign
              </Link>
              <Link href="/dashboard/reports" className="block btn-secondary py-3 text-center">
                View Reports
              </Link>
              <Link href="/dashboard/analytics" className="block btn-secondary py-3 text-center">
                Analytics Dashboard
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
