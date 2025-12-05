import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'CorelDove - Smart E-commerce Solutions',
  description: 'AI-powered e-commerce platform with intelligent sourcing and inventory management. Discover quality products with smart automation.',
  keywords: ['ecommerce', 'AI sourcing', 'inventory management', 'products', 'automation'],
  authors: [{ name: 'CorelDove Team' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
  icons: {
    icon: '/favicons/coreldove-favicon.png',
    shortcut: '/favicons/coreldove-favicon.png',
    apple: '/favicons/coreldove-favicon.png',
  },
  openGraph: {
    title: 'CorelDove - Smart E-commerce Solutions',
    description: 'AI-powered e-commerce platform with intelligent sourcing and inventory management',
    url: 'https://coreldove.com',
    siteName: 'CorelDove',
    images: [
      {
        url: '/og-image-coreldove.jpg',
        width: 1200,
        height: 630,
        alt: 'CorelDove - Smart E-commerce Solutions',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'CorelDove - Smart E-commerce Solutions',
    description: 'AI-powered e-commerce platform with intelligent sourcing and inventory management',
    images: ['/og-image-coreldove.jpg'],
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}