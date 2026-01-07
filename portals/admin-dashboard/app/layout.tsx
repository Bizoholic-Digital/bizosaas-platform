import React from 'react';
import type { Metadata, Viewport } from 'next';
import './globals.css';

import { Providers } from './providers';
import { PWAInstallPrompt, PWAProvider } from '@/components/PWAInstallPrompt';
import { OfflineBanner } from '@/components/OfflineBanner';

// Using system fonts to avoid network calls during Docker build
const inter = { className: 'font-sans' };

export const metadata: Metadata = {
  title: 'Bizo Admin Hub [LIVE]',
  description: 'Elite Enterprise Platform Control Hub - Super Admin v5',
  keywords: ['BizOSaaS', 'Admin', 'Platform', 'Management', 'Multi-tenant', 'AI Workflows', 'Super Admin'],
  authors: [{ name: 'BizOSaaS Team' }],
  robots: 'noindex, nofollow', // Admin dashboard should not be indexed
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'BizOSaaS Admin',
  },
  formatDetection: {
    telephone: false,
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: '#2563eb',
};

// Force dynamic rendering for all pages - prevents static generation errors
export const dynamic = 'force-dynamic';
export const dynamicParams = true;

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          <PWAProvider>
            <OfflineBanner />
            {/* Main Content Area */}
            <div className="flex flex-1 flex-col overflow-hidden h-screen bg-gray-50 dark:bg-gray-900">
              <main className="flex-1 overflow-y-auto p-0">
                {children}
              </main>
            </div>
            <PWAInstallPrompt />
          </PWAProvider>
        </Providers>
      </body>
    </html>
  );
}