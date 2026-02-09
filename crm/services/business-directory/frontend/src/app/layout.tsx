import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Header from '@/components/layout/header'
import Footer from '@/components/layout/footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'BizBook - Business Directory | Find Local Businesses Near You',
  description: 'Discover amazing local businesses in your area. Search through thousands of verified businesses, read reviews, and connect with trusted service providers.',
  keywords: 'business directory, local businesses, reviews, services, companies, local search',
  authors: [{ name: 'BizBook Team' }],
  creator: 'BizBook',
  publisher: 'BizBook',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
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
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://bizbook.com',
    title: 'BizBook - Business Directory',
    description: 'Find and connect with local businesses in your area',
    siteName: 'BizBook',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BizBook - Business Directory',
    description: 'Find and connect with local businesses in your area',
    creator: '@bizbook',
  },
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex flex-col min-h-screen">
          <Header />
          <main className="flex-grow">
            {children}
          </main>
          <Footer />
        </div>
      </body>
    </html>
  )
}