'use client'

import React, { Suspense } from 'react'
import { signIn } from 'next-auth/react'
import { ThemeToggle } from '@/components/theme-toggle'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import { LockIcon, Github, Chrome } from 'lucide-react'

function LoginForm() {
  const handleLogin = (provider: string = 'authentik') => {
    // We use the 'authentik' provider in NextAuth, but Authentik itself 
    // will handle the social login selection. 
    signIn('authentik', { callbackUrl: '/dashboard' })
  }

  return (
    <Card className="w-[420px] shadow-2xl bg-white/70 dark:bg-black/70 backdrop-blur-md border-0 ring-1 ring-white/20">
      <CardHeader className="space-y-1 text-center pb-8">
        <div className="flex justify-center mb-6">
          <div className="p-4 bg-gradient-to-tr from-blue-600 to-cyan-400 rounded-2xl shadow-lg ring-4 ring-blue-500/20">
            <LockIcon className="w-8 h-8 text-white" />
          </div>
        </div>
        <CardTitle className="text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-500 dark:from-white dark:to-gray-400">
          BizOSaaS Client Portal
        </CardTitle>
        <CardDescription className="text-base font-medium">
          Secure access to your business ecosystem
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-6">
        <div className="grid grid-cols-2 gap-4">
          <Button
            variant="outline"
            className="flex items-center justify-center gap-2 h-12 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900 transition-all active:scale-95"
            onClick={() => handleLogin()}
          >
            <Chrome className="w-5 h-5 text-blue-500" />
            <span className="font-semibold">Google</span>
          </Button>
          <Button
            variant="outline"
            className="flex items-center justify-center gap-2 h-12 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900 transition-all active:scale-95"
            onClick={() => handleLogin()}
          >
            <Github className="w-5 h-5" />
            <span className="font-semibold">GitHub</span>
          </Button>
        </div>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-slate-200 dark:border-slate-800" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-white/0 px-2 text-muted-foreground backdrop-blur-none bg-inherit">
              Or continue with
            </span>
          </div>
        </div>

        <Button
          className="w-full text-lg font-bold h-14 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-xl transition-all hover:scale-[1.02] active:scale-[0.98]"
          size="lg"
          onClick={() => handleLogin()}
        >
          Sign in with Enterprise SSO
        </Button>
      </CardContent>
      <CardFooter className="flex flex-col space-y-4 pt-4 text-center text-sm text-muted-foreground">
        <p className="px-8 text-center text-sm leading-6">
          By clicking continue, you agree to our{' '}
          <a href="#" className="underline underline-offset-4 hover:text-primary">
            Terms of Service
          </a>{' '}
          and{' '}
          <a href="#" className="underline underline-offset-4 hover:text-primary">
            Privacy Policy
          </a>
          .
        </p>
      </CardFooter>
    </Card>
  )
}

export default function LoginPage() {
  return (
    <div className="relative min-h-screen w-full overflow-hidden flex items-center justify-center p-4">
      {/* Dynamic Animated Background */}
      <div className="fixed inset-0 bg-slate-50 dark:bg-slate-950 -z-20" />
      <div className="fixed inset-0 -z-10">
        <div className="absolute top-0 -left-1/4 w-[500px] h-[500px] bg-blue-400/20 dark:bg-blue-600/10 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-0 -right-1/4 w-[500px] h-[500px] bg-indigo-400/20 dark:bg-indigo-600/10 rounded-full blur-[120px] animate-pulse delay-700" />
      </div>

      <div className="absolute top-8 right-8 z-50">
        <ThemeToggle />
      </div>

      <div className="z-10 w-full max-w-[420px]" data-testid="login-form">
        <Suspense fallback={
          <div className="flex flex-col items-center gap-4">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
            <p className="text-sm font-medium animate-pulse">Initializing secure session...</p>
          </div>
        }>
          <LoginForm />
        </Suspense>
      </div>
    </div>
  )
}