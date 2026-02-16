'use client'

import { useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Eye, EyeOff, Mail, Lock, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { useToast } from '@/hooks/use-toast'

export function LoginForm() {
  const [email, setEmail] = useState('admin@bizoholic.com')
  const [password, setPassword] = useState('AdminDemo2024!')
  const [showPassword, setShowPassword] = useState(false)
  const [rememberMe, setRememberMe] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()
  const searchParams = useSearchParams()
  const { toast } = useToast()

  // Get redirect parameters
  const redirectParam = searchParams?.get('redirect')
  const pathParam = searchParams?.get('path')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!email || !password) {
      toast({
        title: 'Fields required',
        description: 'Please enter both email and password.',
        variant: 'destructive',
      })
      return
    }

    setIsLoading(true)

    try {
      // Login via Next.js API route (which proxies to FastAPI auth service)
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Authentication failed')
      }

      const userData = await response.json()

      toast({
        title: 'Welcome back!',
        description: 'Successfully signed in to Bizoholic platform.',
      })

      // Redirect to dashboard or specified path
      const redirectPath = redirectParam || pathParam || '/portal/dashboard'
      console.log('Login successful, redirecting to:', redirectPath)

      // Use window.location for full page reload to ensure auth state is refreshed
      window.location.href = redirectPath
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Invalid credentials'
      toast({
        title: 'Sign in failed',
        description: errorMessage,
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="email">Email address</Label>
        <div className="relative">
          <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            id="email"
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="pl-10"
            required
            disabled={isLoading}
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="password">Password</Label>
        <div className="relative">
          <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            id="password"
            type={showPassword ? 'text' : 'password'}
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="pl-10 pr-10"
            required
            disabled={isLoading}
          />
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
            onClick={() => setShowPassword(!showPassword)}
            disabled={isLoading}
          >
            {showPassword ? (
              <EyeOff className="h-4 w-4 text-muted-foreground" />
            ) : (
              <Eye className="h-4 w-4 text-muted-foreground" />
            )}
          </Button>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Checkbox
            id="remember"
            checked={rememberMe}
            onCheckedChange={(checked) => setRememberMe(checked === true)}
            disabled={isLoading}
          />
          <Label htmlFor="remember" className="text-sm">
            Remember me
          </Label>
        </div>
      </div>

      <Button
        type="submit"
        className="w-full bg-blue-600 text-white hover:bg-blue-700 focus:bg-blue-700 active:bg-blue-800"
        disabled={isLoading}
        style={{ backgroundColor: '#2563eb', color: '#ffffff' }}
      >
        {isLoading ? (
          <>
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-background border-t-transparent" />
            Signing in...
          </>
        ) : (
          <>
            Sign In
            <ArrowRight className="ml-2 h-4 w-4" />
          </>
        )}
      </Button>

      {/* Demo credentials info */}
      <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
        <p className="text-sm text-blue-700">
          <strong>Demo Credentials:</strong><br />
          Email: admin@bizoholic.com<br />
          Password: AdminDemo2024!
        </p>
      </div>
    </form>
  )
}