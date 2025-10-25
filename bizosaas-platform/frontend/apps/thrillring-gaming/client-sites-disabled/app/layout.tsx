import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { headers } from 'next/headers';
import { ClientProvider } from '../lib/client-context';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export async function generateMetadata(): Promise<Metadata> {
  const headersList = headers();
  const clientName = headersList.get('x-client-name') || 'BizOSaaS Client Portal';
  const clientId = headersList.get('x-client-id') || 'demo';
  
  return {
    title: `${clientName} - AI Marketing Platform`,
    description: 'Advanced AI Marketing Automation Platform with 47+ specialized agents',
    keywords: 'AI marketing, automation, CRM, e-commerce, business directory, lead generation',
    authors: [{ name: 'BizOSaaS Team' }],
    creator: 'BizOSaaS',
    publisher: 'BizOSaaS',
    robots: 'index, follow',
    viewport: 'width=device-width, initial-scale=1',
    themeColor: headersList.get('x-client-primary-color') || '#0ea5e9',
    icons: {
      icon: '/favicon.ico',
      apple: '/apple-touch-icon.png',
    },
    openGraph: {
      type: 'website',
      locale: 'en_US',
      title: `${clientName} - AI Marketing Platform`,
      description: 'Advanced AI Marketing Automation Platform with 47+ specialized agents',
      siteName: clientName,
      images: [
        {
          url: `/og-images/${clientId}-og.jpg`,
          width: 1200,
          height: 630,
          alt: `${clientName} Platform`,
        },
      ],
    },
    twitter: {
      card: 'summary_large_image',
      title: `${clientName} - AI Marketing Platform`,
      description: 'Advanced AI Marketing Automation Platform with 47+ specialized agents',
      images: [`/og-images/${clientId}-twitter.jpg`],
    },
  };
}

function ClientMetaTags() {
  const headersList = headers();
  
  return (
    <>
      <meta name="x-client-id" content={headersList.get('x-client-id') || 'demo'} />
      <meta name="x-client-name" content={headersList.get('x-client-name') || 'Demo Client'} />
      <meta name="x-client-template" content={headersList.get('x-client-template') || 'startup_focus'} />
      <meta name="x-client-primary-color" content={headersList.get('x-client-primary-color') || '#6366f1'} />
      <meta name="x-client-logo" content={headersList.get('x-client-logo') || '/logos/demo-logo.png'} />
      <meta name="x-client-features" content={headersList.get('x-client-features') || '["ai_agents"]'} />
      <meta name="x-routing-type" content={headersList.get('x-routing-type') || 'subdomain'} />
    </>
  );
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <ClientMetaTags />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
      </head>
      <body className={`${inter.className} antialiased bg-gray-50`}>
        <ClientProvider>
          <div className="min-h-screen flex flex-col">
            {children}
          </div>
        </ClientProvider>
      </body>
    </html>
  );
}