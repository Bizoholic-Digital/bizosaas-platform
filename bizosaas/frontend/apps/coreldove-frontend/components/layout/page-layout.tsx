/**
 * CorelDove Page Layout Component - Consistent Header/Footer Wrapper
 * Use this component to wrap all pages for consistent navigation
 */

'use client'

import { usePathname } from 'next/navigation'
import Header from '../navigation/header'
import Footer from '../navigation/footer'

interface PageLayoutProps {
  children: React.ReactNode
  className?: string
}

export default function PageLayout({ children, className = '' }: PageLayoutProps) {
  const pathname = usePathname()

  return (
    <div className={`min-h-screen bg-white ${className}`}>
      <Header currentPath={pathname} />
      <main className="flex-1">
        {children}
      </main>
      <Footer />
    </div>
  )
}