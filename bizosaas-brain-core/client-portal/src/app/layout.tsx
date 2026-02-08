import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '@/lib/auth'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: {
    default: 'BizOSaaS Client Portal - Digital Marketing Platform',
    template: '%s | BizOSaaS',
  },
  description: 'Multi-tenant digital marketing platform for businesses. Manage campaigns, analytics, CRM, and more in one place.',
  keywords: 'digital marketing, SaaS, CRM, analytics, campaign management, business automation',
  authors: [{ name: 'BizOSaaS Team' }],
  creator: 'BizOSaaS',
  publisher: 'BizOSaaS',
  applicationName: 'BizOSaaS Client Portal',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'BizOSaaS',
  },
  formatDetection: {
    telephone: false,
  },
  icons: {
    icon: '/portal/favicon.png',
    shortcut: '/portal/favicon.png',
    apple: '/portal/favicon.png',
  },
  manifest: '/portal/manifest.json',
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
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://portal.bizoholic.com',
    title: 'BizOSaaS Client Portal',
    description: 'Multi-tenant digital marketing platform for businesses',
    siteName: 'BizOSaaS',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BizOSaaS Client Portal',
    description: 'Multi-tenant digital marketing platform for businesses',
    creator: '@bizoholic',
  },
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#1e293b' },
  ],
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 5,
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.className} antialiased bg-white text-gray-900`}>
        <AuthProvider>
          <div className="min-h-screen flex flex-col">
            {children}
          </div>
        </AuthProvider>
      </body>
    </html>
  )
}