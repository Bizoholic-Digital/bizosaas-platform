/**
 * CorelDove 404 Not Found Page - E-commerce Optimized
 * Custom branded error page with shopping-focused navigation and recommendations
 */

'use client'

import Link from 'next/link'
import Image from 'next/image'
import { Button } from '../components/ui/button'
import { Card, CardContent } from '../components/ui/card'
import { useTenantTheme } from '../hooks/useTenantTheme'
import { 
  Home, 
  ArrowLeft, 
  Search,
  ShoppingBag,
  Compass,
  Sparkles,
  Package,
  Zap,
  TrendingUp,
  Tags,
  Gift
} from 'lucide-react'

export default function NotFound() {
  const { config } = useTenantTheme()
  const { branding } = config

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl shadow-2xl border-0 bg-white/90 backdrop-blur-sm">
        <CardContent className="p-8 text-center">
          {/* Logo */}
          <div className="mb-8">
            <Image
              src={branding.logo}
              alt="CorelDove"
              width={120}
              height={60}
              className="mx-auto"
              priority
            />
          </div>

          {/* 404 Icon */}
          <div className="mb-6">
            <div className="relative">
              <div className="text-8xl font-bold text-gray-100 select-none">404</div>
              <div className="absolute inset-0 flex items-center justify-center">
                <Compass className="w-16 h-16 text-blue-500 animate-spin" style={{ animationDuration: '3s' }} />
              </div>
            </div>
          </div>

          {/* Main Message */}
          <div className="mb-8 space-y-4">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Product Not Found
            </h1>
            <p className="text-lg text-gray-600 max-w-md mx-auto">
              The product you're looking for may have been moved, sold out, or is no longer available.
            </p>
            <div className="flex items-center justify-center text-sm text-gray-500 gap-1">
              <Sparkles className="w-4 h-4" />
              <span>But don't worry - we have thousands of other great products!</span>
              <Sparkles className="w-4 h-4" />
            </div>

            {/* Quick suggestions */}
            <div className="bg-red-50 p-4 rounded-lg mt-6">
              <h3 className="font-semibold text-red-800 mb-2">Popular Right Now:</h3>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div className="flex items-center text-red-600">
                  <Package className="w-3 h-3 mr-1" />
                  Mobile Accessories
                </div>
                <div className="flex items-center text-red-600">
                  <Zap className="w-3 h-3 mr-1" />
                  Electronics
                </div>
                <div className="flex items-center text-red-600">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  Home & Kitchen
                </div>
                <div className="flex items-center text-red-600">
                  <Tags className="w-3 h-3 mr-1" />
                  Best Deals
                </div>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="space-y-4">
            {/* Primary Actions */}
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Link href="/">
                <Button className="w-full sm:w-auto bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 transform hover:scale-105">
                  <Home className="w-4 h-4 mr-2" />
                  Back to Home
                </Button>
              </Link>
              
              <Link href="/products">
                <Button variant="outline" className="w-full sm:w-auto border-red-200 text-red-600 hover:bg-red-50 px-6 py-3 rounded-lg font-medium transition-all duration-200">
                  <ShoppingBag className="w-4 h-4 mr-2" />
                  Browse All Products
                </Button>
              </Link>
            </div>

            {/* Category Quick Links */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-4">
              <Link href="/category/mobile-accessories">
                <Button variant="ghost" size="sm" className="w-full text-gray-600 hover:text-red-600 hover:bg-red-50 transition-all duration-200">
                  <Package className="w-3 h-3 mr-1" />
                  Mobile
                </Button>
              </Link>
              
              <Link href="/category/electronics">
                <Button variant="ghost" size="sm" className="w-full text-gray-600 hover:text-red-600 hover:bg-red-50 transition-all duration-200">
                  <Zap className="w-3 h-3 mr-1" />
                  Electronics
                </Button>
              </Link>
              
              <Link href="/category/home-kitchen">
                <Button variant="ghost" size="sm" className="w-full text-gray-600 hover:text-red-600 hover:bg-red-50 transition-all duration-200">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  Home
                </Button>
              </Link>
              
              <Link href="/categories">
                <Button variant="ghost" size="sm" className="w-full text-gray-600 hover:text-red-600 hover:bg-red-50 transition-all duration-200">
                  <Search className="w-3 h-3 mr-1" />
                  All Categories
                </Button>
              </Link>
            </div>

            {/* Help Actions */}
            <div className="flex flex-col sm:flex-row gap-3 justify-center pt-4 border-t border-gray-200">
              <Link href="/contact">
                <Button variant="ghost" size="sm" className="text-gray-500 hover:text-red-600 hover:bg-red-50 px-4 py-2 rounded-lg transition-all duration-200">
                  <Gift className="w-4 h-4 mr-2" />
                  Get Help Finding Products
                </Button>
              </Link>
            </div>
          </div>

          {/* Footer Message */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <p className="text-sm text-gray-500">
              🤖 Our AI-powered search can help you discover products you'll love. Try browsing our categories or contact our support team!
            </p>
            <div className="mt-2 flex items-center justify-center gap-4 text-xs text-gray-400">
              <span>✅ Fast Shipping</span>
              <span>✅ Quality Products</span>
              <span>✅ 24/7 Support</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}