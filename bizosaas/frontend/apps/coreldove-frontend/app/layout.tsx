import type { Metadata, Viewport } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import PWAProvider from '@/components/PWAProvider';

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'CorelDove - Smart E-commerce Solutions',
  description: 'AI-powered e-commerce platform with intelligent sourcing and inventory management. Discover quality products with smart automation.',
  keywords: ['ecommerce', 'AI sourcing', 'inventory management', 'products', 'automation'],
  authors: [{ name: 'CorelDove Team' }],
  manifest: '/manifest.json',
  robots: 'index, follow',
  icons: {
    icon: '/icons/icon-192x192.svg',
    shortcut: '/icons/icon-192x192.svg',
    apple: '/icons/icon-192x192.svg',
  },
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'CorelDove Store',
    startupImage: [
      {
        url: '/icons/icon-512x512.svg',
        media: '(device-width: 390px) and (device-height: 844px) and (-webkit-device-pixel-ratio: 3)',
      },
    ],
  },
  formatDetection: {
    telephone: false,
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

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#3b82f6' },
    { media: '(prefers-color-scheme: dark)', color: '#1e40af' },
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        {/* PWA Meta Tags */}
        <link rel="apple-touch-icon" href="/icons/icon-192x192.svg" />
        <link rel="icon" type="image/svg+xml" href="/icons/icon-192x192.svg" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="CorelDove Store" />
        <meta name="msapplication-TileColor" content="#3b82f6" />
        <meta name="msapplication-config" content="/browserconfig.xml" />
      </head>
      <body className={inter.className}>
        <PWAProvider>
          {children}
        </PWAProvider>
      </body>
    </html>
  )
}