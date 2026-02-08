import type { Metadata } from 'next'
import { cn } from '@/lib/utils'
import { Providers } from './providers'
import { Toaster } from '@/components/ui/sonner'
import { Navbar } from '@/components/layout/Navbar'
import { Footer } from '@/components/layout/Footer'
import { getPlatformMetadata, getPlatformClassName } from '@/lib/platform'
import { Inter, JetBrains_Mono } from 'next/font/google'
import './globals.css'

// Using system fonts to avoid network calls during Docker build
const fontSans = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
})

const fontMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
})

export const metadata: Metadata = {
  metadataBase: new URL('http://localhost:3000'),
  title: {
    default: 'ThrillRing - Global Gaming Platform',
    template: '%s | ThrillRing',
  },
  description: 'The ultimate destination for competitive gaming. Tournaments, leaderboards, news, and more.',
  keywords: ['gaming', 'esports', 'tournaments', 'leaderboard', 'thrillring', 'bizosaas'],
  authors: [{ name: 'ThrillRing Team' }],
  creator: 'ThrillRing',
  icons: {
    icon: '/favicons/bizosaas-favicon.ico', // Update when thrillring favicon exists
    shortcut: '/favicons/bizosaas-favicon.ico',
    apple: '/favicons/bizosaas-favicon.png',
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://www.thrillring.com',
    title: 'ThrillRing - Global Gaming Platform',
    description: 'Join tournaments, climb global leaderboards, and get the latest gaming news.',
    siteName: 'ThrillRing',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'ThrillRing - Global Gaming Platform',
    description: 'Join tournaments, climb global leaderboards, and get the latest gaming news.',
  },
  robots: {
    index: true,
    follow: true,
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
            <Navbar />
            <div className="flex-1">{children}</div>
            <Footer />
          </div>
          <Toaster />
        </Providers>
      </body>
    </html>
  )
}