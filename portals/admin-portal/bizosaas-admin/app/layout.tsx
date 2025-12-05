import type { Metadata } from 'next';
import './globals.css';
import { AdminNavigation } from '@/components/AdminNavigation';
import AuthProvider from '../shared/components/AuthProvider';

// Using system fonts to avoid network calls during Docker build
const inter = { variable: '--font-sans' };

export const metadata: Metadata = {
  title: 'BizOSaaS Admin - Platform Management',
  description: 'Super Admin Dashboard for BizOSaaS Multi-Tenant Platform - Workflow Management & AI Agent Control',
  keywords: ['BizOSaaS', 'Admin', 'Platform', 'Management', 'Multi-tenant', 'AI Workflows', 'Super Admin'],
  authors: [{ name: 'BizOSaaS Team' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'noindex, nofollow', // Admin dashboard should not be indexed
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="font-sans antialiased">
        <AuthProvider platform="bizosaas-admin">
          <AdminNavigation>
            {children}
          </AdminNavigation>
        </AuthProvider>
      </body>
    </html>
  );
}