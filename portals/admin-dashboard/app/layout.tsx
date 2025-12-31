import React from 'react';
import type { Metadata, Viewport } from 'next';
import './globals.css';
import { AdminNavigation } from '@/components/AdminNavigation';
import { PWAInstallPrompt } from '@/components/PWAInstallPrompt';
import { OfflineBanner } from '@/components/OfflineBanner';
import { ClerkProvider } from '@clerk/nextjs';

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
      <body className="font-sans antialiased h-screen overflow-hidden">
        <ClerkProvider publishableKey="pk_test_Yml6b3NhYXMtY29yZS0xNy5jbGVyay5hY2NvdW50cy5kZXYk">
          <Providers>
            <OfflineBanner />
            <div className="flex flex-1 flex-col overflow-hidden h-screen bg-gray-50 dark:bg-gray-900">
              <main className="flex-1 overflow-y-auto p-0">
                {children}
              </main>
            </div>
            <PWAInstallPrompt />
          </Providers>
        </ClerkProvider>
      </body>
    </html>
  );
}