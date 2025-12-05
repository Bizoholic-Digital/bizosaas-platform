/**
 * CorelDove Footer Component - Consistent Site Footer
 * Includes navigation links and company information
 */

'use client'

import Link from 'next/link'
import { useTenantTheme } from '../../hooks/useTenantTheme'

export default function Footer() {
  const { config } = useTenantTheme()

  return (
    <footer className="border-t border-gray-800 bg-gray-900">
      <div className="container py-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 pt-8">
          <div>
            <h3 className="font-semibold mb-6 text-white">Shop</h3>
            <ul className="space-y-3 text-sm text-gray-400">
              <li><Link href="/products" className="hover:text-white transition-colors">All Products</Link></li>
              <li><Link href="/categories" className="hover:text-white transition-colors">Categories</Link></li>
              <li><Link href="/deals" className="hover:text-white transition-colors">Special Deals</Link></li>
              <li><Link href="/new-arrivals" className="hover:text-white transition-colors">New Arrivals</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-6 text-white">Company</h3>
            <ul className="space-y-3 text-sm text-gray-400">
              <li><Link href="/about" className="hover:text-white transition-colors">About Us</Link></li>
              <li><Link href="/careers" className="hover:text-white transition-colors">Careers</Link></li>
              <li><Link href="/press" className="hover:text-white transition-colors">Press</Link></li>
              <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-6 text-white">Support</h3>
            <ul className="space-y-3 text-sm text-gray-400">
              <li><Link href="/help" className="hover:text-white transition-colors">Help Center</Link></li>
              <li><Link href="/returns" className="hover:text-white transition-colors">Returns</Link></li>
              <li><Link href="/shipping" className="hover:text-white transition-colors">Shipping Info</Link></li>
              <li><Link href="/track" className="hover:text-white transition-colors">Track Order</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-6 text-white">Legal</h3>
            <ul className="space-y-3 text-sm text-gray-400">
              <li><Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
              <li><Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
              <li><Link href="/refund" className="hover:text-white transition-colors">Refund Policy</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 pt-12 mt-12 pb-8 text-center text-sm text-gray-400">
          <p>&copy; 2025 {config.branding.companyName}. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}