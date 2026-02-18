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

import Script from 'next/script'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const gtmId = process.env.NEXT_PUBLIC_GTM_ID || 'GTM-XXXXXXX'

  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <Script id="gtm" strategy="afterInteractive">
          {`
            (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
            new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
            'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
            })(window,document,'script','dataLayer','${gtmId}');
          `}
        </Script>
      </head>
      <body className={`${inter.className} antialiased`} data-theme="marketing">
        <noscript>
          <iframe
            src={`https://www.googletagmanager.com/ns.html?id=${gtmId}`}
            height="0"
            width="0"
            style={{ display: 'none', visibility: 'hidden' }}
          />
        </noscript>
        <AuthProvider>
          <div className="min-h-screen flex flex-col">
            {children}
          </div>
        </AuthProvider>
      </body>
    </html>
  )
}