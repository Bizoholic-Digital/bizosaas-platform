import type { Metadata, Viewport } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import PWAProvider from '@/components/PWAProvider';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Bizoholic - AI-Powered Marketing Agency',
  description: 'Transform your marketing with AI automation, lead generation, and campaign optimization',
  keywords: ['AI Marketing', 'Lead Generation', 'Campaign Management', 'Marketing Automation'],
  authors: [{ name: 'Bizoholic Team' }],
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'Bizoholic Marketing',
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
    type: 'website',
    siteName: 'Bizoholic Marketing',
    title: 'AI-Powered Marketing Agency',
    description: 'Transform your marketing with AI automation, lead generation, and campaign optimization',
    images: ['/icons/icon-512x512.svg'],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Bizoholic - AI-Powered Marketing Agency',
    description: 'Transform your marketing with AI automation, lead generation, and campaign optimization',
    images: ['/icons/icon-512x512.svg'],
  },
};

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
  children: React.ReactNode;
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
        <meta name="apple-mobile-web-app-title" content="Bizoholic Marketing" />
        <meta name="msapplication-TileColor" content="#3b82f6" />
        <meta name="msapplication-config" content="/browserconfig.xml" />
      </head>
      <body className={inter.className}>
        <PWAProvider>
          {children}
        </PWAProvider>
      </body>
    </html>
  );
}