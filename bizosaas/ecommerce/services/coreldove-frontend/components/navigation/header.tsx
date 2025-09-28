/**
 * CorelDove Header Component - Responsive Navigation
 * Includes cart integration and mobile-responsive menu
 */

'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '../ui/button'
import { useTenantTheme } from '../../hooks/useTenantTheme'
import { useCartTotals } from '../../lib/stores/cart-store'
import { 
  ShoppingCart, 
  Menu,
  X,
  User,
  Search
} from 'lucide-react'

interface HeaderProps {
  currentPath?: string
}

export default function Header({ currentPath = '/' }: HeaderProps) {
  const { config } = useTenantTheme()
  const { totalItems } = useCartTotals()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navigation = [
    { name: 'Products', href: '/products' },
    { name: 'Categories', href: '/categories' },
    { name: 'About', href: '/about' },
    { name: 'Contact', href: '/contact' },
  ]

  const isActivePath = (href: string) => {
    if (href === '/') return currentPath === '/'
    return currentPath.startsWith(href)
  }

  return (
    <header className="border-b border-gray-800 bg-gray-900/95 backdrop-blur supports-[backdrop-filter]:bg-gray-900/90 sticky top-0 z-50">
      <div className="container">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <Image
              src={config.branding.logo}
              alt={config.branding.companyName}
              width={120}
              height={40}
              className="h-8 w-auto object-contain"
              priority
              onError={(e) => {
                // Fallback to text logo if image fails to load
                e.currentTarget.style.display = 'none'
                e.currentTarget.nextElementSibling?.classList.remove('hidden')
              }}
            />
            <span className="hidden text-xl font-bold text-red-400">
              <span className="text-red-400">Corel</span><span className="text-blue-400">Dove</span>
            </span>
          </Link>
          
          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={`text-sm font-medium transition-colors ${
                  isActivePath(item.href)
                    ? 'text-red-400'
                    : 'text-gray-300 hover:text-white'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-4">
            {/* Search Button (Desktop) */}
            <Button
              variant="ghost"
              size="sm"
              className="hidden md:inline-flex text-gray-300 hover:text-white hover:bg-gray-800"
            >
              <Search className="h-4 w-4" />
            </Button>

            {/* Cart */}
            <Link href="/cart" className="relative">
              <Button variant="ghost" size="sm" className="relative text-gray-300 hover:text-white hover:bg-gray-800">
                <ShoppingCart className="h-4 w-4" />
                {totalItems > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center text-[10px] font-medium">
                    {totalItems > 99 ? '99+' : totalItems}
                  </span>
                )}
              </Button>
            </Link>

            {/* User Account */}
            <Link href="/auth/login">
              <Button size="sm" className="hidden md:inline-flex bg-red-600 hover:bg-red-700 text-white">
                <User className="h-4 w-4 mr-2" />
                Sign In
              </Button>
            </Link>

            {/* Mobile Menu Toggle */}
            <Button
              variant="ghost"
              size="sm"
              className="md:hidden text-gray-300 hover:text-white hover:bg-gray-800"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-gray-800 bg-gray-900/95 backdrop-blur">
            <div className="py-4 space-y-1">
              {/* Search (Mobile) */}
              <div className="px-4 pb-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search products..."
                    className="w-full pl-10 pr-4 py-2 bg-gray-800 text-gray-100 placeholder-gray-400 rounded-md text-sm border-0 focus:ring-2 focus:ring-red-500"
                  />
                </div>
              </div>

              {/* Navigation Links */}
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`block px-4 py-2 text-base font-medium transition-colors ${
                    isActivePath(item.href)
                      ? 'text-red-400 bg-gray-800'
                      : 'text-gray-300 hover:text-white hover:bg-gray-800'
                  }`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}

              {/* Mobile Sign In */}
              <div className="px-4 pt-4 border-t">
                <Link href="/auth/login" onClick={() => setMobileMenuOpen(false)}>
                  <Button className="w-full bg-red-600 hover:bg-red-700 text-white">
                    <User className="h-4 w-4 mr-2" />
                    Sign In
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  )
}