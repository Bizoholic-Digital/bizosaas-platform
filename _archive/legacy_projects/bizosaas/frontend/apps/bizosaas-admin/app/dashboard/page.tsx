import { Metadata } from 'next'
import DashboardOverview from '../../components/dashboard/DashboardOverview'
import ServiceHealthMonitor from '../../components/dashboard/ServiceHealthMonitor'

export const metadata: Metadata = {
  title: 'Dashboard | BizOSaaS Admin',
  description: 'Central admin dashboard for BizOSaaS platform management',
}

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="p-6 space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">BizOSaaS Admin Dashboard</h1>
          <p className="text-gray-600">Monitor and manage all platform services</p>
        </div>

        <DashboardOverview />

        <ServiceHealthMonitor />
      </div>
    </div>
  )
}