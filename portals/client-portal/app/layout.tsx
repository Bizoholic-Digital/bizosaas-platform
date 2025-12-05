'use client';

import type { Metadata, Viewport } from 'next';
import './globals.css';
import { SessionProvider } from 'next-auth/react';

// Using system fonts to avoid network calls during Docker build
const inter = { variable: '--font-sans' };

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <SessionProvider>
          {/* Main Content Area */}
          <div className="flex flex-1 flex-col overflow-hidden">
            <main className="flex-1 overflow-y-auto p-0">
              {children}
            </main>
          </div>
        </SessionProvider>
      </body>
    </html>
  );
}

