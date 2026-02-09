'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { 
  Search, 
  ShoppingCart, 
  Heart, 
  User, 
  Menu, 
  X, 
  ChevronDown,
  Brain,
  Package,
  Smartphone,
  Home,
  Dumbbell,
  Heart as HealthIcon
} from 'lucide-react'
import { Button } from '../ui/button'
import { Badge } from '../ui/badge'

interface NavigationHeaderProps {
  cartCount?: number
  wishlistCount?: number
  isAuthenticated?: boolean
  user?: any
  onAuthAction?: () => void
}

export default function NavigationHeader({
  cartCount = 0,
  wishlistCount = 0,
  isAuthenticated = false,
  user = null,
  onAuthAction
}: NavigationHeaderProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [isSearchFocused, setIsSearchFocused] = useState(false)
  const router = useRouter()

  const categories = [
    { name: 'Electronics', slug: 'electronics', icon: Smartphone, count: '50+' },
    { name: 'Furniture', slug: 'furniture', icon: Home, count: '30+' },
    { name: 'Sports & Fitness', slug: 'sports', icon: Dumbbell, count: '40+' },
    { name: 'Health & Wellness', slug: 'health', icon: HealthIcon, count: '25+' },
    { name: 'Home & Living', slug: 'home', icon: Package, count: '60+' }
  ]

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      router.push(`/catalog?search=${encodeURIComponent(searchQuery.trim())}`)
      setSearchQuery('')
      setIsSearchFocused(false)
    }
  }

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-center py-2 text-sm font-medium">
        🚀 AI-Powered Product Sourcing | Free Shipping on Orders $50+ | 
        <span className="ml-2 font-bold">Use Code: LAUNCH30</span>
      </div>

      {/* Main Header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2 flex-shrink-0">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <Brain className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
              CoreLDove
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link 
              href="/catalog" 
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
            >
              All Products
            </Link>
            <div className="relative group">
              <button className="flex items-center space-x-1 text-gray-700 hover:text-blue-600 font-medium transition-colors">
                <span>Categories</span>
                <ChevronDown className="h-4 w-4" />
              </button>
              {/* Categories Dropdown */}
              <div className="absolute top-full left-0 mt-1 w-64 bg-white rounded-lg shadow-lg border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                <div className="p-2">
                  {categories.map((category) => (
                    <Link
                      key={category.slug}
                      href={`/catalog?category=${category.slug}`}
                      className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <category.icon className="h-5 w-5 text-gray-400" />
                      <div className="flex-1">
                        <div className="font-medium text-gray-900">{category.name}</div>
                        <div className="text-sm text-gray-500">{category.count} products</div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            </div>
            <Link 
              href="/deals" 
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
            >
              Hot Deals
            </Link>
            <Link 
              href="/about" 
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
            >
              About
            </Link>
          </nav>

          {/* Search Bar */}
          <div className="flex-1 max-w-lg mx-8 hidden lg:block">
            <form onSubmit={handleSearch} className="relative">
              <input
                type="text"
                placeholder="Search for products, brands, or categories..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onFocus={() => setIsSearchFocused(true)}
                onBlur={() => setTimeout(() => setIsSearchFocused(false), 200)}
                className="w-full px-4 py-2 pl-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <Search className="absolute left-4 top-2.5 h-5 w-5 text-gray-400" />
              <Button 
                type="submit"
                size="sm"
                className="absolute right-2 top-1 bg-blue-600 hover:bg-blue-700"
              >
                Search
              </Button>
              
              {/* Search Suggestions */}
              {isSearchFocused && searchQuery && (
                <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                  <div className="p-2">
                    <div className="text-sm text-gray-500 mb-2">Popular searches</div>
                    {['wireless headphones', 'office chair', 'smartwatch', 'yoga mat'].map((suggestion) => (
                      <button
                        key={suggestion}
                        onClick={() => {
                          setSearchQuery(suggestion)
                          router.push(`/catalog?search=${encodeURIComponent(suggestion)}`)
                          setIsSearchFocused(false)
                        }}
                        className="block w-full text-left p-2 hover:bg-gray-50 rounded text-sm"
                      >
                        <Search className="h-4 w-4 inline mr-2 text-gray-400" />
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </form>
          </div>

          {/* User Actions */}
          <div className="flex items-center space-x-4">
            {/* Mobile Search Button */}
            <Button variant="ghost" size="sm" className="lg:hidden">
              <Search className="h-5 w-5" />
            </Button>

            {/* Wishlist */}
            <Link href="/wishlist" className="relative p-2 text-gray-600 hover:text-red-500 transition-colors">
              <Heart className="h-6 w-6" />
              {wishlistCount > 0 && (
                <Badge className="absolute -top-1 -right-1 h-5 w-5 flex items-center justify-center p-0 bg-red-500 text-white text-xs">
                  {wishlistCount > 9 ? '9+' : wishlistCount}
                </Badge>
              )}
            </Link>

            {/* Cart */}
            <Link href="/cart" className="relative p-2 text-gray-600 hover:text-blue-600 transition-colors">
              <ShoppingCart className="h-6 w-6" />
              {cartCount > 0 && (
                <Badge className="absolute -top-1 -right-1 h-5 w-5 flex items-center justify-center p-0 bg-blue-600 text-white text-xs">
                  {cartCount > 9 ? '9+' : cartCount}
                </Badge>
              )}
            </Link>

            {/* User Menu */}
            <div className="relative group">
              {isAuthenticated ? (
                <button className="flex items-center space-x-2 p-2 text-gray-600 hover:text-gray-900 transition-colors">
                  <User className="h-6 w-6" />
                  <span className="hidden sm:block text-sm font-medium">
                    {user?.name || user?.email?.split('@')[0] || 'Account'}
                  </span>
                  <ChevronDown className="h-4 w-4" />
                </button>
              ) : (
                <Button onClick={onAuthAction} variant="outline" size="sm">
                  <User className="h-4 w-4 mr-2" />
                  Sign In
                </Button>
              )}

              {/* User Dropdown */}
              {isAuthenticated && (
                <div className="absolute right-0 top-full mt-1 w-48 bg-white rounded-lg shadow-lg border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                  <div className="p-2">
                    <Link href="/account" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded">
                      My Account
                    </Link>
                    <Link href="/orders" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded">
                      Order History
                    </Link>
                    <Link href="/wishlist" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded">
                      Wishlist
                    </Link>
                    <hr className="my-2" />
                    <button 
                      onClick={onAuthAction}
                      className="block w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded"
                    >
                      Sign Out
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="sm"
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-200">
          <div className="max-w-7xl mx-auto px-4 py-4 space-y-4">
            {/* Mobile Search */}
            <form onSubmit={handleSearch} className="relative">
              <input
                type="text"
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-4 py-2 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
            </form>

            {/* Mobile Navigation */}
            <nav className="space-y-2">
              <Link 
                href="/catalog" 
                className="block py-2 text-gray-700 hover:text-blue-600 font-medium transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                All Products
              </Link>
              {categories.map((category) => (
                <Link
                  key={category.slug}
                  href={`/catalog?category=${category.slug}`}
                  className="flex items-center space-x-2 py-2 text-gray-700 hover:text-blue-600 transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  <category.icon className="h-4 w-4" />
                  <span>{category.name}</span>
                </Link>
              ))}
              <Link 
                href="/deals" 
                className="block py-2 text-gray-700 hover:text-blue-600 font-medium transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                Hot Deals
              </Link>
              <Link 
                href="/about" 
                className="block py-2 text-gray-700 hover:text-blue-600 font-medium transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                About
              </Link>
            </nav>
          </div>
        </div>
      )}
    </header>
  )
}