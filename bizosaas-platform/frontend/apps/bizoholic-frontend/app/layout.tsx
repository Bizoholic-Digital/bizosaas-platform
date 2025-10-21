import React from 'react';

export const metadata = {
  title: 'Bizoholic | AI Marketing Platform',
  description: 'AI-powered marketing automation platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
