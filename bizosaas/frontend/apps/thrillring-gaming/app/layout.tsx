import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'ThrillRing - Ultimate Gaming Arena',
  description: 'Join millions of gamers in epic tournaments, climb leaderboards, and experience the thrill of competitive gaming.',
  keywords: 'gaming, esports, tournaments, leaderboards, competitive gaming, thrillring',
  authors: [{ name: 'ThrillRing Team' }],
  openGraph: {
    title: 'ThrillRing - Ultimate Gaming Arena',
    description: 'Join millions of gamers in epic tournaments, climb leaderboards, and experience the thrill of competitive gaming.',
    type: 'website',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'ThrillRing - Ultimate Gaming Arena',
    description: 'Join millions of gamers in epic tournaments, climb leaderboards, and experience the thrill of competitive gaming.',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <Providers>
          <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900">
            {children}
          </div>
        </Providers>
      </body>
    </html>
  )
}