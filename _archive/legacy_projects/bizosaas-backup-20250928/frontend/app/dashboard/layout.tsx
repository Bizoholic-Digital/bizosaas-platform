import { Metadata } from 'next'
import { DashboardSidebar } from '@/components/dashboard-sidebar'
import { DashboardHeader } from '@/components/dashboard-header'
import { RouteGuard } from '@/components/route-guard'

export const metadata: Metadata = {
  title: {
    default: 'Dashboard',
    template: '%s | Bizoholic Dashboard',
  },
  description: 'Bizoholic AI Marketing Platform Dashboard - Manage your autonomous marketing campaigns',
}

interface DashboardLayoutProps {
  children: React.ReactNode
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <RouteGuard>
      <div className="flex min-h-screen bg-background">
        <DashboardSidebar />
        <div className="flex-1 flex flex-col lg:ml-72">
          <DashboardHeader />
          <main className="flex-1 overflow-auto p-6 lg:p-8">
            <div className="max-w-7xl mx-auto">
              {children}
            </div>
          </main>
        </div>
      </div>
    </RouteGuard>
  )
}