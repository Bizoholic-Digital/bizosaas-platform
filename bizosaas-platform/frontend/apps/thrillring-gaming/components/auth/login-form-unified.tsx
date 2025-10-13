'use client'

import { useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/hooks/use-auth'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { 
  Eye, 
  EyeOff, 
  LogIn, 
  AlertCircle, 
  Loader2,
  Shield,
  Globe,
  Zap
} from 'lucide-react'

const PLATFORM_CONFIG = {
  bizoholic: {
    name: 'Bizoholic',
    description: 'AI Marketing Agency Platform',
    icon: Zap,
    color: 'blue'
  },
  coreldove: {
    name: 'CoreLDove',
    description: 'AI-Powered E-commerce Platform',
    icon: Globe,
    color: 'red'
  },
  temporal: {
    name: 'Temporal Dashboard',
    description: 'Workflow Management',
    icon: Shield,
    color: 'purple'
  }
}

interface LoginFormProps {
  defaultPlatform?: string
  onSuccess?: (user: any) => void
  showPlatformSelector?: boolean
}

export function UnifiedLoginForm({ 
  defaultPlatform = 'bizosaas',
  onSuccess,
  showPlatformSelector = true
}: LoginFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [platform, setPlatform] = useState(defaultPlatform)
  const [rememberMe, setRememberMe] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const { login } = useAuth()
  const router = useRouter()
  const searchParams = useSearchParams()
  const redirectTo = searchParams?.get('redirect') || '/dashboard'

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await login({
        email,
        password,
        platform,
        remember_me: rememberMe
      })

      if (onSuccess) {
        onSuccess(null) // User data will be available through useAuth hook
      } else {
        router.push(redirectTo)
      }
    } catch (err: any) {
      setError(err.message || 'Login failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const selectedPlatformConfig = PLATFORM_CONFIG[platform as keyof typeof PLATFORM_CONFIG]
  const PlatformIcon = selectedPlatformConfig?.icon || Shield

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-4">
          <div className="flex items-center justify-center">
            <div className="p-3 rounded-full bg-gradient-to-r from-blue-600 to-purple-600">
              <Shield className="h-8 w-8 text-white" />
            </div>
          </div>
          
          <div className="text-center">
            <CardTitle className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              BizOSaas Login
            </CardTitle>
            <CardDescription>
              Single Sign-On across all platforms
            </CardDescription>
          </div>

          {showPlatformSelector && (
            <div className="space-y-3">
              <Label className="text-sm font-medium">Select Platform</Label>
              <div className="grid grid-cols-1 gap-2">
                {Object.entries(PLATFORM_CONFIG).map(([key, config]) => {
                  const Icon = config.icon
                  const isSelected = platform === key
                  
                  return (
                    <button
                      key={key}
                      type="button"
                      onClick={() => setPlatform(key)}
                      className={`flex items-center space-x-3 p-3 rounded-lg border-2 transition-all ${
                        isSelected 
                          ? `border-${config.color}-500 bg-${config.color}-50` 
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <Icon className={`h-5 w-5 ${isSelected ? `text-${config.color}-600` : 'text-gray-500'}`} />
                      <div className="text-left flex-1">
                        <div className="font-medium text-sm">{config.name}</div>
                        <div className="text-xs text-muted-foreground">{config.description}</div>
                      </div>
                      {isSelected && (
                        <Badge variant="default" className={`bg-${config.color}-600`}>
                          Selected
                        </Badge>
                      )}
                    </button>
                  )
                })}
              </div>
            </div>
          )}
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  disabled={isLoading}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
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
                  id="remember" 
                  checked={rememberMe}
                  onCheckedChange={(checked) => setRememberMe(checked as boolean)}
                />
                <Label htmlFor="remember" className="text-sm">
                  Remember me
                </Label>
              </div>
              
              <Link 
                href="/auth/forgot-password" 
                className="text-sm text-blue-600 hover:underline"
              >
                Forgot password?
              </Link>
            </div>

            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Signing in...
                </>
              ) : (
                <>
                  <LogIn className="mr-2 h-4 w-4" />
                  Sign In
                </>
              )}
            </Button>

            <div className="text-center">
              <p className="text-sm text-muted-foreground">
                Don't have an account?{' '}
                <Link 
                  href="/auth/register" 
                  className="text-blue-600 hover:underline font-medium"
                >
                  Sign up
                </Link>
              </p>
            </div>

            {selectedPlatformConfig && (
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <PlatformIcon className="h-4 w-4 text-gray-600" />
                  <span className="text-sm font-medium text-gray-900">
                    Signing into {selectedPlatformConfig.name}
                  </span>
                </div>
                <p className="text-xs text-gray-600">
                  Your credentials will work across all BizOSaas platforms
                </p>
              </div>
            )}
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

// Simplified version for embedded use
export function CompactLoginForm({ onSuccess }: { onSuccess?: (user: any) => void }) {
  return (
    <UnifiedLoginForm 
      showPlatformSelector={false} 
      onSuccess={onSuccess}
    />
  )
}