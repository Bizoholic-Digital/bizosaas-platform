'use client'

/*
CoreLDove Standalone Frontend - E-commerce Platform
Dedicated CoreLDove interface with Saleor backend integration
*/

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { ShoppingCart, Package, BarChart3, Settings, Users, LogOut, ExternalLink } from 'lucide-react'
import Image from 'next/image'

interface User {
  name?: string;
  email?: string;
  id?: string;
}

export default function CoreLDoveStandalone() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(false)

  // Check authentication status
  useEffect(() => {
    // Check if user is logged into Saleor or has CoreLDove session
    const checkAuth = async () => {
      try {
        // Check CoreLDove session
        const response = await fetch('/api/auth/session')
        if (response.ok) {
          const userData = await response.json()
          setUser(userData)
          setIsAuthenticated(true)
        }
      } catch (error) {
        console.log('No active session')
      }
    }
    
    checkAuth()
  }, [])

  const handleLogin = () => {
    setLoading(true)
    // Redirect to CoreLDove auth flow
    window.location.href = '/coreldove-standalone/auth/login'
  }

  const handleSaleorAdmin = () => {
    // Open Saleor admin dashboard
    window.open('http://localhost:9020', '_blank')
  }

  const handleProductManagement = () => {
    // Navigate to AI-powered product sourcing dashboard
    window.location.href = '/coreldove'
  }

  const handleLogout = async () => {
    try {
      await fetch('/api/auth/logout', { method: 'POST' })
      setIsAuthenticated(false)
      setUser(null)
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-blue-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <Image
              src="/coreldove-logo.png"
              alt="CoreLDove"
              width={120}
              height={60}
              className="mx-auto mb-4"
            />
            <h1 className="text-3xl font-bold text-gray-900 mb-2">CoreLDove</h1>
            <p className="text-gray-600">AI-Powered E-commerce Automation Platform</p>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Welcome Back</CardTitle>
              <CardDescription>
                Sign in to access your e-commerce dashboard
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button 
                onClick={handleLogin} 
                className="w-full bg-red-600 hover:bg-red-700"
                disabled={loading}
              >
                {loading ? 'Signing In...' : 'Sign In to CoreLDove'}
              </Button>
              
              <div className="text-center text-sm text-gray-500">
                New to CoreLDove?{' '}
                <a href="/coreldove-standalone/register" className="text-red-600 hover:underline">
                  Create Account
                </a>
              </div>
            </CardContent>
          </Card>

          <div className="text-center text-xs text-gray-500">
            <p>Powered by Saleor • Built for Dropshipping Success</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Image
                src="/coreldove-logo.png"
                alt="CoreLDove"
                width={40}
                height={20}
                className="mr-3"
              />
              <h1 className="text-xl font-bold text-gray-900">CoreLDove Dashboard</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="bg-green-50 text-green-700">
                Online
              </Badge>
              <Button variant="ghost" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4 mr-2" />
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Dashboard */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.name || 'Admin'}! 👋
          </h2>
          <p className="text-gray-600">
            Your AI-powered e-commerce automation platform is ready
          </p>
        </div>

        {/* Quick Actions Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={handleSaleorAdmin}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Saleor Admin</CardTitle>
              <ExternalLink className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">Dashboard</div>
              <p className="text-xs text-muted-foreground">
                Manage products, orders, and inventory
              </p>
              <Button variant="outline" size="sm" className="mt-3 w-full">
                Open Saleor Admin
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={handleProductManagement}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">AI Product Sourcing</CardTitle>
              <Package className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">Workflow</div>
              <p className="text-xs text-muted-foreground">
                AI-powered product discovery and approval
              </p>
              <Button variant="outline" size="sm" className="mt-3 w-full">
                Open Sourcing Dashboard
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Analytics</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">$12.4K</div>
              <p className="text-xs text-muted-foreground">
                Revenue this month
              </p>
              <Button variant="outline" size="sm" className="mt-3 w-full">
                View Analytics
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* System Status */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Settings className="h-5 w-5 mr-2" />
                System Status
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm">Saleor API</span>
                <Badge variant="default" className="bg-green-100 text-green-800">Online</Badge>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm">AI Sourcing Service</span>
                <Badge variant="default" className="bg-green-100 text-green-800">Active</Badge>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm">Product Sync</span>
                <Badge variant="default" className="bg-green-100 text-green-800">Running</Badge>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm">Marketing Automation</span>
                <Badge variant="secondary">Ready</Badge>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Users className="h-5 w-5 mr-2" />
                Recent Activity
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-sm text-gray-600">
                • AI found 12 new products in Sports category
              </div>
              <div className="text-sm text-gray-600">
                • 5 products pending approval
              </div>
              <div className="text-sm text-gray-600">
                • Marketing campaigns generated for 3 products
              </div>
              <div className="text-sm text-gray-600">
                • Inventory sync completed successfully
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-sm text-gray-500">
          <p>CoreLDove v2.0 • Powered by Saleor • AI-Enhanced E-commerce</p>
        </footer>
      </main>
    </div>
  )
}