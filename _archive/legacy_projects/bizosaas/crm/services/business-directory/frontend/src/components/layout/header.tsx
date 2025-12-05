'use client'

import React from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { 
  Search, 
  Menu, 
  X, 
  User, 
  Heart,
  MapPin,
  Phone,
  Mail
} from 'lucide-react'

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false)

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Search', href: '/search' },
    { name: 'Categories', href: '/categories' },
    { name: 'Events', href: '/events' },
    { name: 'Products', href: '/products' },
    { name: 'Coupons', href: '/coupons' },
    { name: 'Blog', href: '/blog' },
    { name: 'Community', href: '/community' },
  ]

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      {/* Top bar with contact info */}
      <div className="bg-bizbook-primary text-white py-2">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center text-sm">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1">
                <Phone className="w-4 h-4" />
                <span>+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center space-x-1">
                <Mail className="w-4 h-4" />
                <span>info@bizbook.com</span>
              </div>
            </div>
            <div className="hidden md:flex items-center space-x-4">
              <Link href="/add-business" className="hover:text-bizbook-secondary transition-colors">
                Add Business
              </Link>
              <Link href="/login" className="hover:text-bizbook-secondary transition-colors">
                Login
              </Link>
              <Link href="/register" className="hover:text-bizbook-secondary transition-colors">
                Register
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Main header */}
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-bizbook-primary text-white rounded-lg flex items-center justify-center font-bold">
              B
            </div>
            <div className="hidden sm:block">
              <h1 className="text-xl font-bold text-gray-900">BizBook</h1>
              <p className="text-sm text-gray-500">Business Directory</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="text-gray-700 hover:text-bizbook-primary transition-colors font-medium"
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Desktop Action Buttons */}
          <div className="hidden lg:flex items-center space-x-4">
            <Button variant="outline" size="sm">
              <Heart className="w-4 h-4 mr-2" />
              Favorites
            </Button>
            <Button size="sm">
              <User className="w-4 h-4 mr-2" />
              Account
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="lg:hidden">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="lg:hidden bg-white border-t">
          <nav className="container mx-auto px-4 py-4">
            <div className="flex flex-col space-y-4">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="text-gray-700 hover:text-bizbook-primary transition-colors font-medium py-2"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
              <div className="border-t pt-4 flex flex-col space-y-2">
                <Button variant="outline" size="sm" className="justify-start">
                  <Heart className="w-4 h-4 mr-2" />
                  Favorites
                </Button>
                <Button size="sm" className="justify-start">
                  <User className="w-4 h-4 mr-2" />
                  Account
                </Button>
                <Link href="/add-business" className="text-bizbook-primary font-medium py-2">
                  Add Business
                </Link>
              </div>
            </div>
          </nav>
        </div>
      )}
    </header>
  )
}

export default Header