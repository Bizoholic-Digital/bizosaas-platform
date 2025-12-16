import type { Metadata, Viewport } from 'next';
import './globals.css';
import { Providers } from './providers';
import { PWAInstallPrompt } from '@/components/PWAInstallPrompt';
import { OfflineBanner } from '@/components/OfflineBanner';
import { auth } from '@/lib/auth';

// Simple font mock to avoid build issues, ensures Tailwind finds 'font-sans'
const inter = { className: 'font-sans' };

export const metadata: Metadata = {
  title: 'BizOSaaS Platform',
  description: 'Unified Enterprise SaaS Platform',
  manifest: '/manifest.json',
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: '#2563eb',
};

export const dynamic = 'force-dynamic';

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();
  console.log('[SERVER-LAYOUT] Session fetch result:', {
    hasSession: !!session,
    user: session?.user?.email,
    id: session?.user?.id
  });

  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers session={session}>
          <OfflineBanner />
          {/* Main Content Area */}
          <div className="flex flex-1 flex-col overflow-hidden h-screen">
            <main className="flex-1 overflow-y-auto p-0">
              {children}
            </main>
          </div>
          <PWAInstallPrompt />
        </Providers>
      </body>
    </html>
  );
}
