import type { Metadata, Viewport } from 'next';
import './globals.css';
import AuthProvider from '../components/auth/AuthProvider';

// Using system fonts to avoid network calls during Docker build
const inter = { variable: '--font-sans' };

// Force dynamic rendering for all pages (no static optimization)
export const dynamic = 'force-dynamic';
export const dynamicParams = true;
export const revalidate = 0;

export const metadata: Metadata = {
  title: 'Client Portal - Your Business Dashboard',
  description: 'Multi-tenant client portal for managing services, billing, and support tickets',
  keywords: ['Client Portal', 'Dashboard', 'Business Management', 'Multi-tenant'],
  authors: [{ name: 'BizOSaaS Team' }],
  robots: 'noindex, nofollow', // Client portal should not be indexed
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
