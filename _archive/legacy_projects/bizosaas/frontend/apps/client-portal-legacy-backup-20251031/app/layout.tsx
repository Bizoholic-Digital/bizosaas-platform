import type { Metadata, Viewport } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import AuthProvider from '../components/auth/AuthProvider';

const inter = Inter({ subsets: ['latin'] });

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
