import { TenantProvider } from '@/contexts/TenantContext'
import Sidebar from '@/components/portal/Sidebar'
import TenantSelector from '@/components/portal/TenantSelector'
import { Bell, Search, User } from 'lucide-react'

export default function PortalLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <TenantProvider>
      <div className="min-h-screen bg-gray-50">
        {/* Sidebar */}
        <Sidebar />

        {/* Main content area */}
        <div className="lg:pl-64">
          {/* Top bar */}
          <header className="sticky top-0 z-30 bg-white border-b border-gray-200">
            <div className="flex items-center justify-between px-4 py-3 lg:px-6">
              {/* Left: Tenant Selector */}
              <div className="w-64">
                <TenantSelector />
              </div>

              {/* Right: Search, Notifications, User menu */}
              <div className="flex items-center gap-4">
                {/* Search */}
                <button className="p-2 rounded-lg hover:bg-gray-100 transition-colors">
                  <Search className="h-5 w-5 text-gray-600" />
                </button>

                {/* Notifications */}
                <button className="relative p-2 rounded-lg hover:bg-gray-100 transition-colors">
                  <Bell className="h-5 w-5 text-gray-600" />
                  <span className="absolute top-1 right-1 h-2 w-2 bg-red-500 rounded-full"></span>
                </button>

                {/* User menu */}
                <button className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-100 transition-colors">
                  <div className="h-8 w-8 rounded-full bg-solid-900 flex items-center justify-center">
                    <User className="h-5 w-5 text-white" />
                  </div>
                </button>
              </div>
            </div>
          </header>

          {/* Page content */}
          <main className="p-4 lg:p-6">
            {children}
          </main>
        </div>
      </div>
    </TenantProvider>
  )
}
