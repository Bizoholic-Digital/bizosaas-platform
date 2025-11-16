import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Header } from '@/components/layout/header'
import { cn } from '@/lib/utils'
import { Providers } from './providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'BizDirectory - Find Local Businesses',
  description: 'Discover and connect with local businesses in your area. Search restaurants, services, healthcare, retail stores and more.',
  keywords: ['business directory', 'local businesses', 'restaurants', 'services', 'healthcare', 'retail'],
  authors: [{ name: 'BizOSaaS Platform' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
  openGraph: {
    title: 'BizDirectory - Find Local Businesses',
    description: 'Discover and connect with local businesses in your area.',
    type: 'website',
    url: 'https://directory.bizosaas.com',
    siteName: 'BizDirectory',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BizDirectory - Find Local Businesses',
    description: 'Discover and connect with local businesses in your area.',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={cn(
        inter.className,
        "min-h-screen bg-background font-sans antialiased"
      )}>
        <Providers>
          <div className="relative flex min-h-screen flex-col">
            <Header />
            <main className="flex-1">
              {children}
            </main>
          <footer className="border-t bg-background">
            <div className="container max-w-7xl mx-auto px-4 py-8">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold">BizDirectory</h3>
                  <p className="text-sm text-muted-foreground">
                    Find and connect with local businesses in your community.
                  </p>
                </div>
                <div className="space-y-3">
                  <h4 className="text-sm font-semibold">Categories</h4>
                  <ul className="space-y-1 text-sm text-muted-foreground">
                    <li><a href="/categories/restaurants" className="hover:text-foreground">Restaurants</a></li>
                    <li><a href="/categories/healthcare" className="hover:text-foreground">Healthcare</a></li>
                    <li><a href="/categories/retail" className="hover:text-foreground">Retail</a></li>
                    <li><a href="/categories/services" className="hover:text-foreground">Services</a></li>
                  </ul>
                </div>
                <div className="space-y-3">
                  <h4 className="text-sm font-semibold">For Businesses</h4>
                  <ul className="space-y-1 text-sm text-muted-foreground">
                    <li><a href="/list-business" className="hover:text-foreground">List Your Business</a></li>
                    <li><a href="/business-owner" className="hover:text-foreground">Business Owner Portal</a></li>
                    <li><a href="/advertise" className="hover:text-foreground">Advertise</a></li>
                    <li><a href="/pricing" className="hover:text-foreground">Pricing</a></li>
                  </ul>
                </div>
                <div className="space-y-3">
                  <h4 className="text-sm font-semibold">Support</h4>
                  <ul className="space-y-1 text-sm text-muted-foreground">
                    <li><a href="/help" className="hover:text-foreground">Help Center</a></li>
                    <li><a href="/contact" className="hover:text-foreground">Contact Us</a></li>
                    <li><a href="/privacy" className="hover:text-foreground">Privacy Policy</a></li>
                    <li><a href="/terms" className="hover:text-foreground">Terms of Service</a></li>
                  </ul>
                </div>
              </div>
              <div className="border-t mt-8 pt-8 text-center text-sm text-muted-foreground">
                <p>&copy; 2024 BizDirectory. All rights reserved. Powered by BizOSaaS Platform.</p>
              </div>
            </div>
          </footer>
          </div>
        </Providers>
      </body>
    </html>
  )
}