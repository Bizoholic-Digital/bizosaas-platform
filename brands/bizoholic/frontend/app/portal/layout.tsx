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
      {children}
    </div>
  )
}
