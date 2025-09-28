import React from 'react'
import Link from 'next/link'
import { Logo } from '@/components/ui/logo'
import { Button } from '@/components/ui/button'

export function Header() {
  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
      <div className="container flex h-16 items-center">
        <Logo 
          href="/" 
          priority={true}
          showText={false}
          width={120}
          height={32}
          className=""
        />
        
        <nav className="ml-auto flex items-center space-x-6">
          <Link href="http://localhost:3000" className="text-sm font-medium hover:text-primary">
            BizOSaaS
          </Link>
          <Link href="/services" className="text-sm font-medium hover:text-primary">
            Services
          </Link>
          <Link href="/case-studies" className="text-sm font-medium hover:text-primary">
            Case Studies
          </Link>
          <Link href="/blog" className="text-sm font-medium hover:text-primary">
            Blog
          </Link>
          <Link href="/about" className="text-sm font-medium hover:text-primary">
            About
          </Link>
          <Link href="/contact" className="text-sm font-medium hover:text-primary">
            Contact
          </Link>
          <Link href="/login" className="text-sm font-medium hover:text-primary">
            Sign In
          </Link>
          <Link href="/auth/login">
            <Button size="sm">Get Started</Button>
          </Link>
        </nav>
      </div>
    </header>
  )
}