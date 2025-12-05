import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'CoreLDove - AI-Powered E-commerce Platform',
  description: 'AI-driven dropshipping automation platform powered by Saleor',
  keywords: 'e-commerce, dropshipping, AI automation, Saleor, CoreLDove',
  authors: [{ name: 'CoreLDove Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function CoreLDoveStandaloneLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="coreldove-standalone">
      {children}
    </div>
  )
}