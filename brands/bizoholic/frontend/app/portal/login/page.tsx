'use client'

import { useEffect, useState, Suspense } from 'react'
import { LoginForm } from '@/components/auth/login-form'
import { signIn } from 'next-auth/react'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Card, CardContent } from '@/components/ui/card'
import { Github, Mail } from 'lucide-react'
import { getCurrentBrand, getBrandConfig, type Brand } from '@/lib/brand'

export default function PortalLoginPage() {
  const [brand, setBrand] = useState<Brand>('bizoholic')
  const [config, setConfig] = useState(getBrandConfig('bizoholic'))

  useEffect(() => {
    const currentBrand = getCurrentBrand()
    setBrand(currentBrand)
    setConfig(getBrandConfig(currentBrand))
  }, [])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 px-4">
      <div className="w-full max-w-md space-y-6">
        {/* Brand Logo & Welcome */}
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <Image
              src={config.logo}
              alt={config.name}
              width={240}
              height={60}
              className="h-12 w-auto"
              priority
            />
          </div>
          <h1 className="text-3xl font-bold">Welcome to {config.name}</h1>
          <p className="text-muted-foreground">
            {config.tagline}
          </p>
        </div>

        <Card className="shadow-xl">
          <CardContent className="p-6 space-y-6">
            {/* Demo Credentials Helper */}
            <Card className="bg-blue-50 dark:bg-blue-950 border-blue-200 dark:border-blue-800">
              <CardContent className="p-4">
                <h3 className="font-semibold text-blue-800 dark:text-blue-200 mb-2">Demo Credentials</h3>
                <div className="text-sm text-blue-700 dark:text-blue-300 space-y-1">
                  <div><strong>Admin:</strong> admin@bizoholic.com / AdminDemo2024!</div>
                  <div><strong>Client:</strong> client@bizosaas.com / ClientDemo2024!</div>
                </div>
              </CardContent>
            </Card>

            {/* Social Login */}
            <div className="grid grid-cols-2 gap-3">
              <Button
                variant="outline"
                className="w-full"
                onClick={() => signIn('github', { callbackUrl: '/dashboard' })}
              >
                <Github className="h-4 w-4 mr-2" />
                GitHub
              </Button>
              <Button
                variant="outline"
                className="w-full"
                onClick={() => signIn('google', { callbackUrl: '/dashboard' })}
              >
                <Mail className="h-4 w-4 mr-2" />
                Google
              </Button>
            </div>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <Separator className="w-full" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">Or continue with email</span>
              </div>
            </div>

            {/* Login Form */}
            <Suspense fallback={<div>Loading form...</div>}>
              <LoginForm />
            </Suspense>

            <div className="text-center">
              <p className="text-sm text-muted-foreground">
                Don't have an account?{' '}
                <Link href="/portal/register" className="text-primary hover:underline font-medium">
                  Sign up for free
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>

        <p className="text-center text-xs text-muted-foreground">
          By continuing, you agree to our{' '}
          <Link href="/terms" className="underline hover:text-primary">Terms of Service</Link>
          {' '}and{' '}
          <Link href="/privacy" className="underline hover:text-primary">Privacy Policy</Link>
        </p>
      </div>
    </div>
  )
}
