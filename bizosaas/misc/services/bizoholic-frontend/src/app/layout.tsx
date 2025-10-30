import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '@bizosaas/auth'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Bizoholic - AI-Powered Marketing Automation',
  description: 'Transform your marketing with AI automation. Get 75% cost savings, ROI within 7 days, and setup in 15 minutes. The smartest marketing platform for small businesses.',
  keywords: 'AI marketing automation, digital marketing SaaS, marketing campaigns, lead generation, SEO optimization',
  authors: [{ name: 'Bizoholic Team' }],
  creator: 'Bizoholic',
  publisher: 'Bizoholic',
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
    url: 'https://bizoholic.com',
    title: 'Bizoholic - AI-Powered Marketing Automation',
    description: 'Transform your marketing with AI automation. Get 75% cost savings and ROI within 7 days.',
    siteName: 'Bizoholic',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Bizoholic - AI-Powered Marketing Automation',
    description: 'Transform your marketing with AI automation. Get 75% cost savings and ROI within 7 days.',
    creator: '@bizoholic',
  },
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