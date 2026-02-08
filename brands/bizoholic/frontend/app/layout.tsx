import type { Metadata } from 'next'
import { Inter, JetBrains_Mono } from 'next/font/google'
import { cn } from '@/lib/utils'
import { Providers } from './providers'
import { Toaster } from '@/components/ui/sonner'
import './globals.css'

const fontSans = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
})

const fontMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
})

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'https://bizoholic.com'),
  title: {
    default: 'BizOSaaS - Multi-Tenant Business Platform',
    template: '%s | BizOSaaS',
  },
  description: 'Comprehensive SaaS platform for managing multiple business operations with AI automation',
  keywords: ['SaaS platform', 'multi-tenant', 'business automation', 'AI platform', 'enterprise'],
  authors: [{ name: 'BizOSaaS Team' }],
  creator: 'BizOSaaS',
  icons: {
    icon: '/favicons/bizosaas-favicon.ico',
    shortcut: '/favicons/bizosaas-favicon.ico',
    apple: '/favicons/bizosaas-favicon.png',
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://app.bizoholic.com',
    title: 'BizOSaaS - Multi-Tenant Business Platform',
    description: 'Comprehensive SaaS platform for managing multiple business operations with AI automation',
    siteName: 'BizOSaaS',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BizOSaaS - Multi-Tenant Business Platform',
    description: 'Comprehensive SaaS platform for managing multiple business operations with AI automation',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

interface RootLayoutProps {
  children: React.ReactNode
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head />
      <body
        className={cn(
          'min-h-screen bg-background font-sans antialiased',
          fontSans.variable,
          fontMono.variable
        )}
      >
        <Providers>
          <div className="relative flex min-h-screen flex-col">
            <div className="flex-1">{children}</div>
          </div>
          <Toaster />
        </Providers>
      </body>
    </html>
  )
}