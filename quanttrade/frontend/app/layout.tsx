import './globals.css'
import type { Metadata } from 'next'

// Using system fonts to avoid network calls during Docker build
const inter = { variable: '--font-sans' }

export const metadata: Metadata = {
  title: 'QuantTrade - AI-Powered Trading Platform',
  description: 'Advanced AI trading platform with backtesting, portfolio management, and automated strategies',
  keywords: 'trading, AI, quantitative, backtesting, portfolio, algorithms',
  authors: [{ name: 'QuantTrade Team' }],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <script
          src="https://s3.tradingview.com/tv.js"
          async
        />
      </head>
      <body className={`${inter.className} bg-trading-dark text-white`}>
        {children}
      </body>
    </html>
  )
}