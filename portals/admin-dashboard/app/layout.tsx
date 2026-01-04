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

import { brainApi } from '@/lib/brain-api';

// Helper to convert Hex to HSL for shadcn variables
function hexToHsl(hex: string): string {
  let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  if (!result) return "221.2 83.2% 53.3%"; // Default blue

  let r = parseInt(result[1], 16);
  let g = parseInt(result[2], 16);
  let b = parseInt(result[3], 16);

  r /= 255; g /= 255; b /= 255;

  let max = Math.max(r, g, b), min = Math.min(r, g, b);
  let h = 0, s = 0, l = (max + min) / 2;

  if (max !== min) {
    let d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break;
      case g: h = (b - r) / d + 2; break;
      case b: h = (r - g) / d + 4; break;
    }
    h /= 6;
  }

  return `${(h * 360).toFixed(1)} ${(s * 100).toFixed(1)}% ${(l * 100).toFixed(1)}%`;
}

export async function generateMetadata(): Promise<Metadata> {
  let config: any = {};
  try {
    // Use the same public config as the Client Portal for standardized branding
    config = await brainApi.public.getConfig();
  } catch (e) {
    console.error("Failed to load admin metadata config", e);
  }

  return {
    title: config.portal_title ? `${config.portal_title} Admin` : 'BizOSaaS Admin v5 [LIVE]',
    description: 'Super Admin Dashboard for BizOSaaS Multi-Tenant Platform',
    icons: {
      icon: config.favicon_url || '/favicon.ico',
    },
    robots: 'noindex, nofollow',
  };
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
};

// Force dynamic rendering for all pages - prevents static generation errors
export const dynamic = 'force-dynamic';
export const dynamicParams = true;

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  let config: any = {};
  let primaryHsl = "221.2 83.2% 53.3%"; // Default Blue

  try {
    config = await brainApi.public.getConfig();
    if (config.primary_color) {
      primaryHsl = hexToHsl(config.primary_color);
    }
  } catch (e) {
    console.error("Failed to load admin layout config", e);
  }

  const fontStyle = config.font_family ? `body { font-family: '${config.font_family}', sans-serif !important; }` : '';

  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <style dangerouslySetInnerHTML={{
          __html: `
          :root {
            --primary: ${primaryHsl};
            --ring: ${primaryHsl};
            --primary-color: ${config.primary_color || '#2563eb'};
          }
          .dark {
            --primary: ${primaryHsl};
            --ring: ${primaryHsl};
            --primary-color: ${config.primary_color || '#2563eb'};
          }
          ${fontStyle}
        `}} />
      </head>
      <body className="font-sans antialiased h-screen overflow-hidden">
        <ClerkProvider
          publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY}
          appearance={{
            elements: {
              formButtonPrimary: 'bg-primary hover:bg-primary/90 text-sm normal-case shadow-none',
              card: 'shadow-2xl border border-gray-100 dark:border-gray-800',
              headerTitle: 'text-gray-900 dark:text-white font-black tracking-tight',
            },
            variables: {
              colorPrimary: config.primary_color || '#2563eb',
              borderRadius: '0.75rem',
            }
          }}
        >
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