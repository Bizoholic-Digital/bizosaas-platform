import { Metadata } from 'next'
import DashboardOverview from '../../components/dashboard/DashboardOverview'

export const metadata: Metadata = {
  title: 'Dashboard | BizOSaaS Admin',
  description: 'Central admin dashboard for BizOSaaS platform management',
}

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">BizOSaaS Admin Dashboard</h1>
        <DashboardOverview />
      </div>
    </div>
  )
}