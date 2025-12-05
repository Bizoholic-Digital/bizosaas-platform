import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "BizOSaaS Control Center - Autonomous AI Agents Platform",
  description: "Unified dashboard for managing AI agents, campaigns, leads, and multi-tenant operations in the BizOSaaS platform",
  keywords: ["AI agents", "marketing automation", "multi-tenant", "dashboard", "BizOSaaS"],
  authors: [{ name: "BizOSaaS Team" }],
  viewport: "width=device-width, initial-scale=1",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#0ea5e9" },
    { media: "(prefers-color-scheme: dark)", color: "#0284c7" },
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}