'use client'

/*
CoreLDove Standalone Login Page
Authenticates users and redirects to CoreLDove dashboard or Saleor admin
*/

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Checkbox } from '@/components/ui/checkbox'
import { Eye, EyeOff, ArrowLeft, ExternalLink } from 'lucide-react'
import Image from 'next/image'
import Link from 'next/link'

export default function CoreLDoveLogin() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false
  })
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      // First try to authenticate with CoreLDove backend
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          platform: 'coreldove'
        }),
      })

      if (response.ok) {
        const userData = await response.json()
        
        // Store session and redirect to CoreLDove dashboard
        localStorage.setItem('coreldove_user', JSON.stringify(userData))
        window.location.href = '/coreldove-standalone'
      } else {
        const errorData = await response.json()
        setError(errorData.message || 'Login failed')
      }
    } catch (error) {
      console.error('Login error:', error)
      setError('Network error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleSaleorLogin = () => {
    // Direct redirect to Saleor admin with default credentials
    window.open('http://localhost:9020', '_blank')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-blue-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-6">
        {/* Back to main */}
        <Link href="/coreldove-standalone" className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to CoreLDove
        </Link>

        {/* Header */}
        <div className="text-center">
          <Image
            src="/coreldove-logo.png"
            alt="CoreLDove"
            width={120}
            height={60}
            className="mx-auto mb-4"
          />
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Sign In</h1>
          <p className="text-gray-600">Access your CoreLDove e-commerce dashboard</p>
        </div>

        {/* Login Form */}
        <Card>
          <CardHeader>
            <CardTitle>CoreLDove Account</CardTitle>
            <CardDescription>
              Sign in to manage your AI-powered e-commerce platform
            </CardDescription>
          </CardHeader>
          <CardContent>
            {error && (
              <Alert className="mb-4 border-red-200 bg-red-50">
                <AlertDescription className="text-red-700">
                  {error}
                </AlertDescription>
              </Alert>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="email">Email Address</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  required
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="admin@coreldove.local"
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="password">Password</Label>
                <div className="relative mt-1">
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={formData.password}
                    onChange={handleInputChange}
                    placeholder="Enter your password"
                    className="pr-10"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4 text-gray-400" />
                    ) : (
                      <Eye className="h-4 w-4 text-gray-400" />
                    )}
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="rememberMe"
                    checked={formData.rememberMe}
                    onCheckedChange={(checked) =>
                      setFormData(prev => ({ ...prev, rememberMe: !!checked }))
                    }
                  />
                  <Label htmlFor="rememberMe" className="text-sm">
                    Remember me
                  </Label>
                </div>

                <Link href="/coreldove-standalone/auth/forgot" className="text-sm text-red-600 hover:underline">
                  Forgot password?
                </Link>
              </div>

              <Button
                type="submit"
                className="w-full bg-red-600 hover:bg-red-700"
                disabled={loading}
              >
                {loading ? 'Signing In...' : 'Sign In'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Alternative Access */}
        <Card className="border-blue-200">
          <CardHeader>
            <CardTitle className="flex items-center text-blue-700">
              <ExternalLink className="h-5 w-5 mr-2" />
              Quick Access
            </CardTitle>
            <CardDescription>
              Direct access to Saleor administration panel
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button
              onClick={handleSaleorLogin}
              variant="outline"
              className="w-full border-blue-300 text-blue-700 hover:bg-blue-50"
            >
              Open Saleor Admin Dashboard
            </Button>
            <p className="text-xs text-gray-500 mt-2 text-center">
              Default credentials: admin@coreldove.local / admin
            </p>
          </CardContent>
        </Card>

        {/* Register Link */}
        <div className="text-center text-sm text-gray-600">
          New to CoreLDove?{' '}
          <Link href="/coreldove-standalone/auth/register" className="text-red-600 hover:underline">
            Create an account
          </Link>
        </div>

        {/* Footer */}
        <div className="text-center text-xs text-gray-500">
          <p>CoreLDove • AI-Powered E-commerce • Built with Saleor</p>
        </div>
      </div>
    </div>
  )
}