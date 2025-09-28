import React from 'react'
import Link from 'next/link'
import { useTenantTheme } from '@/hooks/useTenantTheme'

export function Footer() {
  const { config } = useTenantTheme()

  return (
    <footer className="border-t bg-background">
      <div className="container py-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div>
            <h3 className="font-semibold mb-4">Services</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="/services/seo">SEO Optimization</Link></li>
              <li><Link href="/services/content-marketing">Content Marketing</Link></li>
              <li><Link href="/services/social-media">Social Media</Link></li>
              <li><Link href="/services/ppc">PPC Management</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-4">Company</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="/about">About Us</Link></li>
              <li><Link href="/careers">Careers</Link></li>
              <li><Link href="/case-studies">Case Studies</Link></li>
              <li><Link href="/contact">Contact</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-4">Resources</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="/blog">Blog</Link></li>
              <li><Link href="/resources">Resources</Link></li>
              <li><Link href="/pricing">Pricing</Link></li>
              <li><Link href="/support">Support</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-4">Legal</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="/privacy">Privacy Policy</Link></li>
              <li><Link href="/terms">Terms of Service</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t pt-8 mt-8 text-center text-sm text-muted-foreground">
          <p>&copy; 2024 {config.branding.companyName}. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}