import { AuthGuard } from '@/components/auth/auth-guard'
import { PortalNav } from '@/components/portal/portal-nav'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Bizoholic Portal',
  description: 'Access your AI-powered marketing platform',
}

export default function PortalLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-background">
      <PortalNav />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  )
}
