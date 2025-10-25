/**
 * CorelDove 404 Not Found Page
 * Custom branded error page with navigation back to main site
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
  Sparkles
} from 'lucide-react'

export default function NotFound() {
  const { config, loading } = useTenantTheme()

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl shadow-2xl border-0 bg-white/90 backdrop-blur-sm">
        <CardContent className="p-8 text-center">
          {/* Logo */}
          <div className="mb-8">
            <Image
              src={config.branding.logo || '/images/Coreldove-Simple-transparent.png'}
              alt={config.branding.companyName}
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
          <div className="mb-8 space-y-3">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Oops! Page Not Found
            </h1>
            <p className="text-lg text-gray-600 max-w-md mx-auto">
              The product or page you're looking for seems to have wandered off into the digital wilderness.
            </p>
            <div className="flex items-center justify-center text-sm text-gray-500 gap-1">
              <Sparkles className="w-4 h-4" />
              <span>Don't worry, we'll help you find what you need!</span>
              <Sparkles className="w-4 h-4" />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="space-y-4">
            {/* Primary Actions */}
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Link href="/">
                <Button className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 transform hover:scale-105">
                  <Home className="w-4 h-4 mr-2" />
                  Back to Home
                </Button>
              </Link>
              
              <Link href="/products">
                <Button variant="outline" className="w-full sm:w-auto border-blue-200 text-blue-600 hover:bg-blue-50 px-6 py-3 rounded-lg font-medium transition-all duration-200">
                  <ShoppingBag className="w-4 h-4 mr-2" />
                  Browse Products
                </Button>
              </Link>
            </div>

            {/* Secondary Actions */}
            <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
              <Link href="/categories">
                <Button variant="ghost" className="w-full sm:w-auto text-gray-600 hover:text-blue-600 hover:bg-blue-50 px-4 py-2 rounded-lg transition-all duration-200">
                  <Search className="w-4 h-4 mr-2" />
                  Search Categories
                </Button>
              </Link>
              
              <Link href="/contact">
                <Button variant="ghost" className="w-full sm:w-auto text-gray-600 hover:text-blue-600 hover:bg-blue-50 px-4 py-2 rounded-lg transition-all duration-200">
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Get Help
                </Button>
              </Link>
            </div>
          </div>

          {/* Footer Message */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <p className="text-sm text-gray-500">
              Lost? Our AI-powered search can help you find exactly what you're looking for.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}