import React from 'react';
import type { Metadata, Viewport } from 'next';
import './globals.css';
import { AdminNavigation } from '@/components/AdminNavigation';
import { PWAInstallPrompt } from '@/components/PWAInstallPrompt';
import { OfflineBanner } from '@/components/OfflineBanner';

import { Providers } from './providers';

// Using system fonts to avoid network calls during Docker build
const inter = { variable: '--font-sans' };

export const metadata: Metadata = {
  title: 'BizOSaaS Admin v5 [LIVE]',
  description: 'Super Admin Dashboard for BizOSaaS Multi-Tenant Platform - Workflow Management & AI Agent Control',
  keywords: ['BizOSaaS', 'Admin', 'Platform', 'Management', 'Multi-tenant', 'AI Workflows', 'Super Admin'],
  authors: [{ name: 'BizOSaaS Team' }],
  robots: 'noindex, nofollow', // Admin dashboard should not be indexed
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
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
      <body className="font-sans antialiased">
        <div className="w-full bg-yellow-400 text-black text-center font-bold py-2 text-xl block z-[9999]" style={{ display: 'block !important', position: 'relative' }}>
          ADMIN UI RELOADED - VERSION 5
        </div>
        <div className="fixed top-0 left-0 bg-red-600 text-white z-[9999] px-2 text-[10px]">
          SERVER_RENDER_OK
        </div>
        <Providers>
          {/* <OfflineBanner /> */}
          <div className="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900">
            <main className="flex-1">
              {children}
            </main>
          </div>
          {/* <PWAInstallPrompt /> */}
        </Providers>
      </body>
    </html>
  );
}